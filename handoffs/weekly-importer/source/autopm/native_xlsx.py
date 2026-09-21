"""Surgical XLSX updates for native pivots/external links unsupported by round trips.

Only reviewed input cells, affected formula caches, update/date styles and recalc flags
change. No macros, formulas or external links are executed by this module.
"""
from copy import deepcopy
from datetime import datetime, timedelta
import json
import math
import os
from pathlib import Path
import re
import tempfile
import warnings
import xml.etree.ElementTree as ET
from zipfile import ZipFile

from .workbook import WorkbookError
from .tracker import fingerprint, verify_sources, read_tracker

NS='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
UPDATE_FILL_RGB='FFC6EFCE'
def q(name):return '{'+NS+'}'+name
CELL=re.compile(r'<(?:[\w]+:)?c\b[^>]*?\br="([A-Z]+\d+)"[^>]*?(?:/>|>.*?</(?:[\w]+:)?c>)',re.S)


def _value(cell,strings):
    if cell is None:return None
    kind=cell.get('t');node=cell.find(q('v'))
    if kind=='inlineStr':return ''.join(n.text or '' for n in cell.iter(q('t')))
    if node is None or node.text is None:return None
    if kind=='s':return strings[int(node.text)]
    if kind in {'str','e','d'}:return node.text
    if kind=='b':return node.text=='1'
    return float(node.text)


def _set_value(cell,value,*,formula=False):
    for child in list(cell):
        if child.tag in {q('v'),q('is')}:cell.remove(child)
    if value is None:
        cell.attrib.pop('t',None);return
    if isinstance(value,str):
        if re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',value):raise WorkbookError('候选值包含 Excel 不支持的控制字符。')
        if formula:
            cell.set('t','e' if value in {'#VALUE!','#REF!','#DIV/0!','#N/A'} else 'str')
            ET.SubElement(cell,q('v')).text=value
        else:
            cell.set('t','inlineStr')
            ET.SubElement(ET.SubElement(cell,q('is')),q('t'),{'{http://www.w3.org/XML/1998/namespace}space':'preserve'}).text=value
    elif isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value):
        cell.set('t','n');ET.SubElement(cell,q('v')).text=format(value,'.15g')
    else:raise WorkbookError('候选值不是可写入的文本或有限数值。')


def _calculate(formula,values,epoch):
    f=formula.lstrip('=');ref=r'(\$?[A-Z]+\$?\d+)'
    month=re.fullmatch(r'IF\(ISNUMBER\('+ref+r'\),\s*DATE\(YEAR\(\1\),\s*MONTH\(\1\),\s*1\),\s*""\)',f,re.I)
    week=re.fullmatch(r'IF\(ISNUMBER\('+ref+r'\),\s*YEAR\(\1\)&" WK"&TEXT\(WEEKNUM\(\1,2\),"00"\),\s*""\)',f,re.I)
    if month or week:
        value=values.get((month or week)[1].replace('$',''))
        if not isinstance(value,(int,float)) or isinstance(value,bool):return ''
        dt=epoch+timedelta(days=value)
        if month:return (datetime(dt.year,dt.month,1)-epoch).days
        wn=((dt-datetime(dt.year,1,1)).days+datetime(dt.year,1,1).weekday())//7+1
        return f'{dt.year} WK{wn:02d}'
    delta=re.fullmatch(r'SUM\('+ref+'-'+ref+r'\)/7',f,re.I)
    subtract=re.fullmatch(ref+r'-(\d+)',f)
    def number(v):
        if v in (None,''):return 0
        if isinstance(v,(int,float)) and not isinstance(v,bool):return v
        raise ValueError('non-numeric input')
    try:
        if delta:return (number(values.get(delta[1].replace('$','')))-number(values.get(delta[2].replace('$',''))))/7
        if subtract:return number(values.get(subtract[1].replace('$','')))-int(subtract[2])
    except ValueError:return '#VALUE!'
    raise NotImplementedError('Formula requires Excel recalculation')


def write_copy(plan,destination):
    import openpyxl
    from openpyxl.styles.numbers import is_date_format, BUILTIN_FORMATS
    from openpyxl.utils.cell import range_boundaries, coordinate_to_tuple
    from openpyxl.utils.datetime import to_excel
    audit=Path(str(destination)+'.autopm.json')
    if destination.exists() or audit.exists():raise WorkbookError('目标文件或同步记录已存在，请使用新的文件名。')
    if not plan['changes'] and not plan.get('roundtrip',{}).get('bindings'):raise WorkbookError('没有单元格变更或可回写基线。')
    source=Path(plan['tracker_path']);part=plan['sheet_part'].lstrip('/')
    with warnings.catch_warnings():
        warnings.simplefilter('ignore',UserWarning)
        wb=openpyxl.load_workbook(source,read_only=True,data_only=False,keep_links=False)
    try:
        epoch=wb.epoch
        # XML below contains exact formula cells; avoid inflated Excel dimensions.
        formulas={}
    finally:wb.close()
    with ZipFile(source) as original:
        xml=original.read(part).decode('utf-8');root=ET.fromstring(xml)
        protection=root.find(q('sheetProtection'))
        if protection is not None and protection.get('sheet','0') in {'1','true'}:
            raise WorkbookError('总表主表已保护，请先在 Excel 中解除保护。')
        cells={c.get('r'):c for c in root.iter(q('c'))}
        formulas={ref:'='+(cell.find(q('f')).text or '') for ref,cell in cells.items() if cell.find(q('f')) is not None}
        # Expand shared formulas for dependency checks, keeping their XML intact.
        shared={node.get('si'):(ref,formulas[ref]) for ref,cell in cells.items()
                if (node:=cell.find(q('f'))) is not None and node.get('t')=='shared' and node.text}
        from openpyxl.formula.translate import Translator
        for ref in formulas:
            node=cells[ref].find(q('f'))
            if not node.text and node.get('si') in shared:
                origin,expression=shared[node.get('si')]
                formulas[ref]=Translator(expression,origin=origin).translate_formula(ref)
        row_styles={int(r.get('r')):int(r.get('s')) for r in root.iter(q('row'))
                    if r.get('s') is not None and r.get('customFormat','0') in {'1','true'}}
        column_styles=[(int(c.get('min')),int(c.get('max')),int(c.get('style')))
                       for c in root.iter(q('col')) if c.get('style') is not None]
        def effective_style(cell,row,col):
            if cell.get('s') is not None:return int(cell.get('s'))
            if row in row_styles:return row_styles[row]
            return next((style for first,last,style in column_styles if first<=col<=last),0)
        strings=[]
        if 'xl/sharedStrings.xml' in original.namelist():
            strings=[''.join(t.text or '' for t in item.iter(q('t'))) for item in ET.fromstring(original.read('xl/sharedStrings.xml'))]
        values={ref:_value(cell,strings) for ref,cell in cells.items()}
        protected=[]
        for node in root.iter(q('f')):
            if node.get('ref'):protected.append(range_boundaries(node.get('ref')))
        for node in root.iter(q('mergeCell')):
            protected.append(range_boundaries(node.get('ref')))
        styles_xml=original.read('xl/styles.xml').decode('utf-8');style_root=ET.fromstring(styles_xml)
        styles=list(style_root.find(q('cellXfs')));extra_styles=[];style_map={}
        fills=list(style_root.find(q('fills')));extra_fills=[]
        highlight_fill=ET.Element(q('fill'))
        pattern_fill=ET.SubElement(highlight_fill,q('patternFill'),{'patternType':'solid'})
        ET.SubElement(pattern_fill,q('fgColor'),{'rgb':UPDATE_FILL_RGB})
        ET.SubElement(pattern_fill,q('bgColor'),{'indexed':'64'})
        def style_key(node):
            return (node.tag,tuple(sorted(node.attrib.items())),(node.text or '').strip(),
                    tuple(style_key(child) for child in node))
        fill_id=next((i for i,fill in enumerate(fills) if style_key(fill)==style_key(highlight_fill)),len(fills))
        if fill_id==len(fills):extra_fills.append(highlight_fill)
        style_ids={style_key(style):i for i,style in enumerate(styles)}
        custom={int(n.get('numFmtId')):n.get('formatCode') for n in style_root.iter(q('numFmt'))}
        def update_style(index,is_date):
            key=(index,is_date)
            if key not in style_map:
                new=deepcopy(styles[index]);number_format=int(new.get('numFmtId','0'))
                if is_date and not is_date_format(custom.get(number_format,BUILTIN_FORMATS.get(number_format,''))):
                    new.set('numFmtId','14');new.set('applyNumberFormat','1')
                new.set('fillId',str(fill_id));new.set('applyFill','1')
                signature=style_key(new)
                if signature not in style_ids:
                    style_ids[signature]=len(styles)+len(extra_styles);extra_styles.append(new)
                style_map[key]=style_ids[signature]
            return style_map[key]
        replacements={};changed=set()
        for change in plan['changes']:
            ref=change['cell'];row,col=coordinate_to_tuple(ref)
            if ref in changed:raise WorkbookError('同一目标单元格出现多个变更，请重新预览。')
            if any(c1<=col<=c2 and r1<=row<=r2 for c1,r1,c2,r2 in protected):
                raise WorkbookError(f'{ref} 位于合并或公式范围内，无法直接写入。')
            previous=cells.get(ref)
            if ref in formulas or (previous is not None and previous.find(q('f')) is not None):raise WorkbookError(f'{ref} 是公式，不能覆盖。')
            edited=deepcopy(previous) if previous is not None else ET.Element(q('c'),{'r':ref})
            value=change['after']
            if change['is_date']:
                value=to_excel(datetime.fromisoformat(value),epoch)
            edited.set('s',str(update_style(effective_style(edited,row,col),change['is_date'])))
            _set_value(edited,value);replacements[ref]=ET.tostring(edited,encoding='unicode');values[ref]=value;changed.add(ref)
        # Follow dependencies within the main sheet. Unknown formulas have their
        # affected cache cleared; Excel must recalculate, never execute source text.
        affected=set(changed);pending={}
        while True:
            found={ref:f for ref,f in formulas.items() if ref not in affected and
                   {r.replace('$','') for r in re.findall(r'\$?[A-Z]+\$?\d+',f)}&affected}
            if not found:break
            pending.update(found);affected.update(found)
        recalculated=0;needs_excel=[]
        for ref,f in pending.items():
            edited=deepcopy(cells[ref])
            try:
                dependencies={r.replace('$','') for r in re.findall(r'\$?[A-Z]+\$?\d+',f)}
                if dependencies&set(needs_excel):raise NotImplementedError('Uncalculated dependency')
                value=_calculate(f,values,epoch);recalculated+=1
            except (NotImplementedError,ValueError,OverflowError):value=None;needs_excel.append(ref)
            _set_value(edited,value,formula=True);values[ref]=value;replacements[ref]=ET.tostring(edited,encoding='unicode')
        updated=CELL.sub(lambda m:replacements.get(m[1],m[0]),xml)
        for ref,text in replacements.items():
            if ref in cells:continue
            row,col=coordinate_to_tuple(ref)
            pattern=re.compile(r'<(?:\w+:)?row\b[^>]*\br="'+str(row)+r'"[^>]*>.*?</(?:\w+:)?row>',re.S)
            match=pattern.search(updated)
            if not match:raise WorkbookError(f'未找到 {ref} 所在行，已停止导出。')
            rowxml=match[0]
            pos=next((m.start() for m in CELL.finditer(rowxml) if coordinate_to_tuple(m[1])[1]>col),rowxml.rfind('</'))
            updated=updated[:match.start()]+rowxml[:pos]+text+rowxml[pos:]+updated[match.end():]
        before_other=CELL.sub(lambda m:'' if m[1] in replacements else m[0],xml)
        after_other=CELL.sub(lambda m:'' if m[1] in replacements else m[0],updated)
        if before_other!=after_other:raise WorkbookError('导出校验失败：非目标内容出现变化。')
        parts={part:updated.encode('utf-8')}
        for name,existing,extras in [('fills',fills,extra_fills),('cellXfs',styles,extra_styles)]:
            if not extras:continue
            pattern=re.compile(r'(<(?:\w+:)?'+name+r'\b[^>]*)(>)(.*?)(</(?:\w+:)?'+name+r'>)',re.S)
            def style_replace(m):
                opening=re.sub(r'\bcount="\d+"','count="'+str(len(existing)+len(extras))+'"',m[1])
                if not re.search(r'\bcount=',opening):opening+=' count="'+str(len(existing)+len(extras))+'"'
                return opening+m[2]+m[3]+''.join(ET.tostring(s,encoding='unicode') for s in extras)+m[4]
            styles_xml,count=pattern.subn(style_replace,styles_xml,count=1)
            if count!=1:raise WorkbookError('无法安全补充更新高亮或日期格式。')
        if extra_styles or extra_fills:
            parts['xl/styles.xml']=styles_xml.encode('utf-8')
        book_xml=original.read('xl/workbook.xml').decode('utf-8')
        book_root=ET.fromstring(book_xml);calc=book_root.find(q('calcPr'))
        calc=deepcopy(calc) if calc is not None else ET.Element(q('calcPr'))
        calc.set('fullCalcOnLoad','1');calc.set('forceFullCalc','1')
        calc_text=ET.tostring(calc,encoding='unicode')
        pattern=re.compile(r'<(?:\w+:)?calcPr\b[^>]*(?:/>|>.*?</(?:\w+:)?calcPr>)',re.S)
        if pattern.search(book_xml):book_xml=pattern.sub(lambda _:calc_text,book_xml,count=1)
        else:book_xml=re.sub(r'(</(?:\w+:)?workbook>)',lambda m:calc_text+m[1],book_xml,count=1)
        parts['xl/workbook.xml']=book_xml.encode('utf-8')
        destination.parent.mkdir(parents=True,exist_ok=True)
        fd,temp=tempfile.mkstemp(prefix='.autopm-',suffix='.xlsx',dir=destination.parent);os.close(fd)
        temporary=Path(temp);audit_temp=None;published_audit=False
        try:
            with ZipFile(temporary,'w') as out:
                for item in original.infolist():out.writestr(deepcopy(item),parts.get(item.filename,original.read(item.filename)))
            with ZipFile(temporary) as out:
                if out.testzip() is not None:raise WorkbookError('导出 ZIP 校验失败。')
                if any(out.read(name)!=original.read(name) for name in original.namelist() if name not in parts):raise WorkbookError('非目标部件保留校验失败。')
                check={c.get('r'):c for c in ET.fromstring(out.read(part)).iter(q('c'))}
                checked_styles=ET.fromstring(out.read('xl/styles.xml'))
                checked_xfs=list(checked_styles.find(q('cellXfs')))
                checked_fills=list(checked_styles.find(q('fills')))
                for ref in changed:
                    if _value(check[ref],strings)!=values[ref]:raise WorkbookError(f'{ref} 导出值校验失败。')
                    xf=checked_xfs[int(check[ref].get('s','0'))]
                    if style_key(checked_fills[int(xf.get('fillId','0'))])!=style_key(highlight_fill):
                        raise WorkbookError(f'{ref} 更新高亮校验失败。')
                for ref in formulas:
                    if ET.tostring(cells[ref].find(q('f')))!=ET.tostring(check[ref].find(q('f'))):raise WorkbookError('公式保留校验失败。')
            verify_sources(plan)
            result={'output':str(destination),'changed_cells':len(changed),'recalculated_caches':recalculated,
                    'highlighted_cells':len(changed),'highlight_color':UPDATE_FILL_RGB,
                    'formula_caches_requiring_excel':needs_excel,'preserved_parts':len(original.namelist())-len(parts),
                    'output_sha256':fingerprint(temporary),'audit':str(audit),'requires_excel_refresh':True}
            result['content_sha256']=read_tracker(temporary)['content_sha256']
            record={**plan,**result,'versions':plan['versions']}
            fd,temp_audit=tempfile.mkstemp(prefix='.autopm-',suffix='.json',dir=destination.parent);os.close(fd);audit_temp=Path(temp_audit)
            audit_temp.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
            # Atomic no-clobber publication; a conflicting destination never loses data.
            publish=os.rename if os.name=='nt' else os.link
            publish(audit_temp,audit);published_audit=True
            publish(temporary,destination)
            return result
        except Exception:
            if published_audit:audit.unlink(missing_ok=True)
            raise
        finally:
            temporary.unlink(missing_ok=True)
            if audit_temp:audit_temp.unlink(missing_ok=True)

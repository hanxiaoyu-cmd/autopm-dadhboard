"""AutoPM Bridge: explicit mappings, reviewable plans, lossless XLSX copy updates.

No module import or parser performs remote writes. No matching by similarity.
"""
from __future__ import annotations
import collections, copy, datetime as dt, hashlib, json, os, pathlib, re, time, unicodedata
import urllib.request, urllib.error, urllib.parse, zipfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
N = {'m': NS}
ROW_RE=re.compile(rb'<row\b[^>]*?(?:/>|>.*?</row>)',re.S)
def xml_segments(stream):
    """Yield original XML bytes without loading a 1 GB worksheet into memory."""
    buf=b''
    while True:
        chunk=stream.read(1024*1024);buf+=chunk
        while True:
            m=ROW_RE.search(buf)
            if not m:break
            if m.start():yield False,buf[:m.start()]
            yield True,m.group(0);buf=buf[m.end():]
        if not chunk:
            if buf:yield False,buf
            break
        # Keep any partial row; flush prefixes/suffixes without rows.
        start=buf.find(b'<row')
        if start>0:yield False,buf[:start];buf=buf[start:]
        elif start<0 and len(buf)>64:yield False,buf[:-64];buf=buf[-64:]
def norm(v):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFKC', str(v or '')).replace('\u200b','')).strip().casefold()
def line_norm(v): return str(v or '').replace('\r\n','\n').replace('\r','\n')
def pid(v):
    s=str(v or '').strip().upper()
    return s if re.fullmatch(r'[NS]XA\d{4,}',s) else ''
def colnum(ref):
    n=0
    for c in re.match('[A-Z]+',ref)[0]: n=n*26+ord(c)-64
    return n
def colletter(n):
    s=''
    while n: n,r=divmod(n-1,26); s=chr(65+r)+s
    return s
def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()
def save_json(path,obj):
    p=pathlib.Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def rich_text(e):
    # Preserve full text and an unstruck candidate separately.
    full=''.join(t.text or '' for t in e.iter('{'+NS+'}t'))
    runs=e.findall('m:r',N)
    if not runs: return full,full
    active=[]
    for run in runs:
        strike=run.find('m:rPr/m:strike',N)
        if strike is None or strike.get('val') in ('0','false'):
            active.append(''.join(t.text or '' for t in run.iter('{'+NS+'}t')))
    return full,''.join(active)

def _apply_tint(rgb,tint):
    values=[int(rgb[i:i+2],16) for i in (0,2,4)]
    tint=float(tint or 0)
    if tint<0: values=[round(v*(1+tint)) for v in values]
    elif tint>0: values=[round(v*(1-tint)+255*tint) for v in values]
    return values

def _is_green(values):
    r,g,b=values
    return g>r*1.04 and g>b*1.02 and g-r>=6

class Book:
    def __init__(self,path):
        self.path=pathlib.Path(path); self.z=zipfile.ZipFile(path)
        w=ET.fromstring(self.z.read('xl/workbook.xml'))
        prop=w.find('m:workbookPr',N)
        self.epoch=dt.datetime(1904,1,1) if prop is not None and prop.get('date1904') in ('1','true') else dt.datetime(1899,12,30)
        rel={r.get('Id'):r.get('Target') for r in ET.fromstring(self.z.read('xl/_rels/workbook.xml.rels'))}
        self.sheets={}
        for s in w.find('m:sheets',N):
            target=rel[s.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')]
            self.sheets[s.get('name')]=target.lstrip('/') if target.startswith('/') else 'xl/'+target
        self.strings=[]
        if 'xl/sharedStrings.xml' in self.z.namelist():
            with self.z.open('xl/sharedStrings.xml') as f:
                for _,e in ET.iterparse(f,events=('end',)):
                    if e.tag=='{'+NS+'}si': self.strings.append(rich_text(e)); e.clear()
        self.styles=[]; self.green=set()
        if 'xl/styles.xml' in self.z.namelist():
            theme=[]
            if 'xl/theme/theme1.xml' in self.z.namelist():
                drawing={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
                colors=ET.fromstring(self.z.read('xl/theme/theme1.xml')).find('.//a:clrScheme',drawing)
                for item in colors or []:
                    color=list(item)[0] if len(item) else None
                    if color is None:theme.append(None)
                    elif color.tag.endswith('sysClr'):theme.append(color.get('lastClr'))
                    else:theme.append(color.get('val'))
            styles=ET.fromstring(self.z.read('xl/styles.xml'))
            fills=styles.find('m:fills',N)
            for i,fill in enumerate(fills if fills is not None else []):
                fg=fill.find('m:patternFill/m:fgColor',N)
                if fg is not None:
                    rgb=fg.get('rgb','')[-6:]
                    values=None
                    if len(rgb)==6: values=_apply_tint(rgb,fg.get('tint'))
                    elif fg.get('theme','').isdigit():
                        n=int(fg.get('theme'))
                        if n<len(theme) and theme[n] and len(theme[n])==6: values=_apply_tint(theme[n],fg.get('tint'))
                    if values and _is_green(values): self.green.add(i)
            self.styles=[int(x.get('fillId','0')) for x in styles.find('m:cellXfs',N)]
    def rows(self,sheet):
        with self.z.open(self.sheets[sheet]) as f:
            for _,e in ET.iterparse(f,events=('end',)):
                if e.tag!='{'+NS+'}row': continue
                row={}
                for c in e.findall('m:c',N):
                    ref=c.get('r'); typ=c.get('t'); v=c.find('m:v',N); form=c.find('m:f',N)
                    raw=v.text if v is not None and v.text is not None else ''
                    active=raw
                    if typ=='s': raw,active=self.strings[int(raw)] if raw else ('','')
                    elif typ=='inlineStr': raw,active=rich_text(c)
                    st=int(c.get('s','0'))
                    formula=(form.text if form.text is not None else '[shared]') if form is not None else None
                    row[colnum(ref)]={'ref':ref,'raw':raw,'active':active,'type':typ,'formula':formula,'style':st,'green':st<len(self.styles) and self.styles[st] in self.green}
                yield int(e.get('r')),row
                e.clear()
    def close(self): self.z.close()
    def tracker_rows(self,sheet):
        # Identify the Project Number column in the first 10 rows; after that
        # only materialize records containing a valid project ID.
        pc=None
        with self.z.open(self.sheets[sheet]) as f:
            for isrow,raw in xml_segments(f):
                if not isrow:continue
                rr=int(re.search(rb'\br="(\d+)"',raw)[1])
                if rr>10:
                    if pc is None:raise ValueError('Project Number column was not found.')
                    key=re.search(rb'<c\b[^>]*\br="'+colletter(pc).encode()+str(rr).encode()+rb'"[^>]*?(?:/>|>.*?</c>)',raw,re.S)
                    if key is None:continue
                    el=ET.fromstring(key.group(0));v=el.find('v');s=v.text if v is not None else ''
                    if el.get('t')=='s':s=self.strings[int(s)][0] if s else ''
                    elif el.get('t')=='inlineStr':s=''.join(el.itertext())
                    if not pid(s):continue
                e=ET.fromstring(raw);row={}
                for c in e.findall('c'):
                    ref=c.get('r');typ=c.get('t');v=c.find('v');form=c.find('f')
                    value=v.text if v is not None and v.text else '';active=value
                    if typ=='s':value,active=self.strings[int(value)] if value else ('','')
                    elif typ=='inlineStr':value=active=''.join(t.text or '' for t in c.iter('t'))
                    formula=(form.text if form.text is not None else '[shared]') if form is not None else None
                    row[colnum(ref)]={'ref':ref,'raw':value,'active':active,'type':typ,'formula':formula,'style':int(c.get('s','0'))}
                    if rr<=10 and norm(value)=='project number':pc=colnum(ref)
                yield rr,row

def read_date(cell,epoch,default_year=None):
    raw=cell.get('active','').strip()
    # If every rich-text run was struck through, keep the known historical date.
    if not raw and cell.get('raw','').strip():raw=cell.get('raw','').strip()
    if not raw or norm(raw) in ('tbc','tbd','n/a','na','none','-','0'): return None,'blank_or_unscheduled'
    if cell.get('type')=='e': return None,'excel_error'
    if cell.get('formula') and not raw: return None,'formula_has_no_cache'
    if re.fullmatch(r'\d{4,5}(?:\.0+)?',raw):
        n=float(raw)
        if 1<=n<=100000:return (epoch+dt.timedelta(days=n)).date().isoformat(),None
    if cell.get('type') not in ('s','str','inlineStr','d'):
        try:
            n=float(raw)
            if n<1 or n>100000: return None,'invalid_excel_date'
            return (epoch+dt.timedelta(days=n)).date().isoformat(),None
        except ValueError: pass
    # Weekly cells can contain a malformed/struck old plan followed by a valid
    # replacement. Keep every parseable date and use the last valid one.
    candidates=[]
    saw_date_like=False
    for line in re.split(r'[\r\n]+',raw):
        line=line.strip()
        if not line: continue
        line=re.sub(r'(?i)sept','Sep',line)
        line=re.sub(r'(?i)\b(?:spe)\b','Sep',line)
        line=re.sub(r'(?i)\b(?:jlu|jiul)\b','Jul',line)
        line=re.sub(r'\s*-\s*','-',line)
        result=None
        for fmt in ('%Y-%m-%d','%d-%b-%y','%d-%b-%Y','%Y/%m/%d','%m/%d/%Y','%d %b %Y','%b %d, %Y','%b-%d-%Y','%b-%d-%y'):
            try: result=dt.datetime.strptime(line,fmt).date().isoformat(); break
            except ValueError: pass
        if result is None and default_year:
            for fmt in ('%d-%b','%d %b','%b %d','%b-%d'):
                try:
                    parsed=dt.datetime.strptime(line,fmt).date().replace(year=int(default_year));result=parsed.isoformat();break
                except ValueError:pass
        if result is None:
            saw_date_like=saw_date_like or bool(re.search(r'\d',line))
            continue
        candidates.append(result)
    # Weekly reports conventionally show old date first and latest date last.
    if candidates:return candidates[-1],None
    return (None,'ambiguous_or_yearless_date') if saw_date_like else (None,'blank_or_unscheduled')

# Canonical -> live field ID and expected type. IDs survive field renaming.
FIELDS={
 'name':('fldyj1QuRUzX1JfqZ','singleLineText'), 'status':('fldDVSUxh30SM3ZU8','singleSelect'),
 'type':('fld6lQExjypHxF9AM','singleSelect'), 'brand':('flduVdC4pbOyXnjfa','singleSelect'),
 'skus':('fldaqmBIKitHamqGX','singleLineText'),
 'model':('fldrFWOA4VAD3XlVI','singleLineText'),
 'sub_category':('fldq1Mdwt4PJy0MZK','singleSelect'),
 'country':('fldL99IASyNhXsz0K','singleSelect'),
 'date_added':('fldZkFfENa7Kqath2','date'),
 'npi':('fldenZLrAjz2vSB1I','multipleRecordLinks'), 'npd':('fldCAsseki0gHRqwA','multipleRecordLinks'),
 'pmo':('fldoEpjuy5AUxO7lH','multipleRecordLinks'),
 'sc':('fldTYr6Rui2zWzL1O','multipleRecordLinks'),
 'factory':('fldsH98MhQc6DwFDp','multipleRecordLinks'),
 'capacity':('fldMqZW8GnIah2tUS','number'),
 'award':('fldtItr7q3SUUgaJf','date'), 'mp':('fld65xhUcqGNNMHh5','date'),
 'previous_mp':('fldDz5v2DpLGcWADj','date'), 'tra':('fldRcroQNEkkMrom4','date'),
 'cut_steel':('fldlIrDxiKi5fQVxS','date'), 'fot':('fldFBFajlCdatfJ9D','date'),
 'eb1':('fldGkh9D4cumJhRaD','date'), 'eb2':('fldRVZjpM4eU8NFk9','date'), 'eb3':('fldJu1b9IboBukBjX','date'),
 'transfer_load':('fldmKnDsAbh4zcT1Y','date'), 'transfer_arrival':('fldFOaJW8EGSsSvqb','date'),
 'pilot':('fld8fmw6vlFtlhDFV','date'), 'mpra':('fld24PSgs18BCwCwf','date'),
 'p1_cad':('fldt06BW0g1iVrYqa','date'),'p1_build':('fld6bwzXVLx7ofs64','date'),
 'p2_cad':('fldxwiHofSvXBsdvV','date'),'p2_build':('fld8LIzCqCJuv10kG','date'),
 'p3_cad':('fldfwb8rZBfpcMycN','date'),'p3_build':('fldZP4r8ZT1XgQBN6','date'),
 'last_p':('fldjo6Z3uaVTIqEtE','date'),'last_p_build':('fld3yIGbcDlPZAKjY','date'),
}
DYNAMIC_FIELDS={
 'start':('Kick Off Date (Manual)','date'),
 'dqtp':('DQTP Finish Date (Manual)','date'),
 'mp_aw':('MP AW Date (Manual)','date'),
 'compliance':('Compliance Complete Date (Manual)','date'),
 'engineering_update':('Update This Week (Manual)','multilineText'),
 'current_progress':('Current Progress (Manual)','multilineText'),
 'tooling':('Tooling (Manual)','singleLineText'),
 'weekly_updated':('Weekly Report Update Date (System)','date'),
}
ALL_PROJECT_CONCEPTS=set(FIELDS)|set(DYNAMIC_FIELDS)
PROJECT_DISPLAY_NAMES={
 'name':'Project Name (Manual)','status':'Project Status (Manual)','type':'Project Type (Manual)',
 'brand':'Brand (Manual)','skus':'Project SKU (Manual)','model':'Model / Family (Manual)',
 'sub_category':'Sub-category (Manual)','country':'Manufacture Country (Manual)',
 'npi':'NPI Owner (Manual)','npd':'NPD Owner','pmo':'PMO Owner (Manual)','sc':'SC Owner (Manual)',
 'factory':'Factory (Manual)','capacity':'Capacity / Forecast (Manual)','tooling':'Tooling (Manual)',
 'current_progress':'Current Progress (Manual)','award':'Start Date (Manual)','mp':'MP Start Date (Manual)',
}
SOURCE_FIELDS={**FIELDS,
 'category':('fldDUtUHgxCqUb73g','multipleLookupValues'),
 'program_code':('fldYsNwklhqxcl0qW','multipleLookupValues'),
 'ale_id':('fldQzxBcSvKhHEjI3','multipleLookupValues'),
 'launch_year':('fldcdgWyrq0IrCezY','multipleLookupValues'),
}
PID_FIELD='fldrbN8jUpydlGNk2'
LAST_UPDATED_FIELD='fldEqjdLtiOzUDQeZ'
PEOPLE_NAME='fldcRUbxKXgWqxjXl'; PEOPLE_DEPARTMENT='fldN56mYHDJ0vnNV1'
FACTORY_NAME='fld2GDuYwBhoUwhq0'; FACTORY_CODE='fldAwh01Lzi3zdmHc'; FACTORY_OLD='fldyZvn9f8NTr9BvL'
TASK_FIELDS={
 'name':'fldMHYYFALdG1pcM0','due':'fld30ugjjB5HD9h1t','owners':'fld8TOPNvLUyfjpj0',
 'start':'fldk4gkMw7jQg2SXv',
 'completed_by':'fldVQnGdBMtSIvOCB','milestone':'fldJdUIiYTo77f2NN','project':'fldZmIf1cjO1baWz9',
}
ISSUE_FIELDS={
 'record':'fld6TUPutbZeb0OXH','status':'fldwzeQr9Ue4RUnBw','action':'fldTcwJCg6OdpoGaO',
 'owners':'fldboKxfGDcOgpaNw','record_date':'fldwUmgjS8KPRiFFf','project':'fldbZYuFwTSkfRTw6',
 'target_date':'fldiSAxlci41MJWYt',
 'severity':'fldPXDw07OQgAc1hN',
}
LABELS={
 'name':['Project','Project Name'], 'skus':['SKUs'], 'status':['Status'], 'type':['Type'],
 'factory':['Fty.'], 'npi':['NPI Lead'], 'npd':['NPD Lead'], 'pmo':['PMO'],
 'engineering_update':['Eng Update This Week'], 'tooling':['Tooling'], 'capacity':['Capacity'],
}
MILESTONES={
 'award':['Award'], 'start':['Kick off','Kick Off To Factory','Eng , OEM Kick Off'],
 'us_kickoff':['US Kick Off To CN'], 'tra':['TRA / ECN DD','TRA/ ECN DD','ECN DD','ECN DD Approved','TRA'],
 'cut_steel':['Cut Steel'], 'fot':['FOT'], 'eb1':['EB1','EB1 Building'], 'eb2':['EB2','EB2 Building'],
 'eb3':['EB3'], 'pilot':['Pilot'], 'mpra':['MPRA / ECN IMP','MPRA , ECN','MPRA / ECN','ECN IMP'],
 'mp':['New MP Start','MP Start','MP Start Eng Ready'], 'previous_mp':['Old MP Start','Previous MP Start Date','Previous MP date'],
 'transfer_load':['Tooling Transfer Load'], 'transfer_arrival':['Tooling Transfer Arrival'],
 'dqtp':['DQTP','DQTP Finish'], 'mp_aw':['MP AW','MP AW& AW Tracker upload'],
 'p1_cad':['P1 CAD DROP'], 'p1_build':['P1 BUILD DATE'], 'p2_cad':['P2 CAD DROP'],
 'p2_build':['P2 BUILD DATE'], 'p3_cad':['P3 CAD DROP'], 'p3_build':['P3 BUILD DATE'],
 'last_p':['Last P'], 'last_p_build':['Last P BUILD DATE'],
 'eb1_aw':['EB1 AW','EB AW'], 'sample_po':['Sample PO approved','Sample PO approval'], 'boilerplate':['Translated RL&IB Boilerplate','Translated IB, RL+ Boilerplate'],
 'compliance':['Compliance Complete','Compliance complete','Compliance Finish','Compliance finished'],
}
def milestone_norm(s):
    s=re.sub(r'\((?:CN|VN|TH|Eng Ready)\)','',str(s),flags=re.I)
    return re.sub(r'[^a-z0-9]','',norm(s))
MS_INDEX={milestone_norm(a):k for k,aliases in MILESTONES.items() for a in aliases}
LABEL_INDEX={norm(a):k for k,aliases in LABELS.items() for a in aliases}

CANONICAL_MILESTONE={
 'award':'Award','start':'Kick off','us_kickoff':'Kick off','tra':'TRA / ECN DD','cut_steel':'Cut Steel','fot':'FOT',
 'eb1':'EB1','eb2':'EB2','eb3':'EB3','dqtp':'DQTP report','compliance':'Compliance report',
 'transfer_load':'Tooling Transfer Load','transfer_arrival':'Tooling Transfer Arrival','pilot':'Pilot',
 'mpra':'MPRA / ECN','mp_aw':'MP AW release','eb1_aw':'MP AW release','mp':'MP Start',
 'previous_mp':'Previous MP Date','p1_cad':'P1 CAD DROP','p1_build':'P1 BUILD DATE',
 'p2_cad':'P2 CAD DROP','p2_build':'P2 BUILD DATE','p3_cad':'P3 CAD DROP','p3_build':'P3 BUILD DATE',
 'last_p':'Last P','last_p_build':'Last P BUILD DATE',
}

def classify_dated_task(header,concept=None):
    """Return (task_name, fixed_milestone, ignored) for a red-section date column."""
    raw=re.sub(r'\s+',' ',str(header or '')).strip(); key=milestone_norm(raw)
    if not raw:return raw,None,True
    if 'eb35' in key or 'samplepo' in key:return raw,None,True
    # Explicit business decisions override broad keyword matching.
    if key in ('dr','drapproval','drapprove'):return raw,None,False
    if key in ('p1','p1build'):return 'P1 BUILD DATE','P1 BUILD DATE',False
    if key in ('p2','p2build'):return 'P2 BUILD DATE','P2 BUILD DATE',False
    if key in ('p3','p3build'):return 'P3 BUILD DATE','P3 BUILD DATE',False
    if key in ('colordevelopment','riskbuyforcolorcomponent'):return raw,None,False
    if key.startswith('dr') and ('formp' in key or 'releasemp' in key or key=='drmp'):
        return 'MP Start','MP Start',False
    if key.startswith('mpstart') or key.startswith('newmpstart'):return 'MP Start','MP Start',False
    if key.startswith('mpra'):return 'MPRA / ECN','MPRA / ECN',False
    if 'previousmp' in key:return 'Previous MP Date','Previous MP Date',False
    if (any(x in key for x in ('fpo','firmporelease','porelease')) or key=='releasepo') and not any(x in key for x in ('toolingpo','pocompletion')):
        return 'FPO Release','FPO Release',False
    if any(x in key for x in ('artwork','mpaw','awtracker','awupload','awrelease','awformp','ebaw')):
        return 'MP AW release','MP AW release',False
    if any(x in key for x in ('compliance','certificate','cert','chemicaltest','safetytest','biotest')):
        return raw,'Compliance report',False
    if 'dqtp' in key or any(x in key for x in ('verificationperformancetest','verificationperformacetest')):return 'DQTP report','DQTP report',False
    if any(x in key for x in ('colorchipapprove','cmfsampleapproved','goldensampleconfirm','colorconfirm','colorcmfapproval','colorapprove')):
        return raw,'Color approval',False
    if ('tooling' in key or 'remotetransfer' in key) and any(x in key for x in ('arrival','eta')):
        return 'Tooling Transfer Arrival','Tooling Transfer Arrival',False
    if ('tooling' in key or 'remotetransfer' in key) and any(x in key for x in ('load','loading','etd')):
        return 'Tooling Transfer Load','Tooling Transfer Load',False
    if 'cutsteel' in key or 'cuttingsteel' in key or key=='ordersteel':return 'Cut Steel','Cut Steel',False
    if key.startswith('fot') or 'remotefot' in key or 'panelfot' in key:return 'FOT','FOT',False
    if key in ('ddapproval','ddapprove') or 'ecndd' in key or key.startswith('traecn'):
        return 'TRA / ECN DD','TRA / ECN DD',False
    if 'translatedaw' in key or 'awfilerelease' in key:return 'MP AW release','MP AW release',False
    if (key.startswith('eb1') and 'aw' not in key) or key=='ebbuild':return 'EB1','EB1',False
    if key.startswith('eb2'):return 'EB2','EB2',False
    if key.startswith('eb3'):return 'EB3','EB3',False
    if concept in CANONICAL_MILESTONE:
        milestone=CANONICAL_MILESTONE[concept]
        return milestone,milestone,False
    return raw,None,False

def normalize_skus(value):
    """Normalize weekly-report SKU shorthand without consulting or creating PMO SKU links."""
    tokens=[re.sub(r'\s+','',x).upper() for x in re.split(r'[/,;\n]+',str(value or '')) if x.strip()]
    if not tokens:return ''
    first=tokens[0]; root=None
    m=re.fullmatch(r'(.+?\d+)([A-Z][A-Z0-9]*)',first)
    if m:root=m.group(1)
    out=[]
    for i,token in enumerate(tokens):
        # Only very short color/variant suffixes inherit the first SKU root.
        # Full models such as ES300 must never become FS353ES300.
        if i and root and len(token)<=4 and re.fullmatch(r'[A-Z]{1,3}\d?',token):token=root+token
        if token not in out:out.append(token)
    return ', '.join(out)

def parse_weekly(path):
    b=Book(path)
    try:
        if 'Report' not in b.sheets: raise ValueError('The Report sheet is missing. No alternative sheet will be guessed.')
        rows=list(b.rows('Report')); starts=[]
        for i,(r,cells) in enumerate(rows):
            if any(norm(c['raw'])=='project number' for c in cells.values()): starts.append(i)
        projects=[]; warnings=[]
        for k,i in enumerate(starts):
            block=rows[i:starts[k+1] if k+1<len(starts) else len(rows)]
            r0,head=block[0]; ids=[pid(c['raw']) for c in head.values() if pid(c['raw'])]
            p={'pid':ids[0] if len(set(ids))==1 else '', 'source':str(pathlib.Path(path).resolve()),'row':r0,'values':{},'cells':{},'unmapped':{},'issues':[],'milestones':{},'dated_tasks':[],'sections':[]}
            for col,c in sorted(head.items()):
                if norm(c['raw']) in ('update on','update'):
                    following=[v for nc,v in sorted(head.items()) if nc>col and v['raw']]
                    if following:
                        p['updated_on']=read_date(following[0],b.epoch)[0]
                        if p['updated_on']: p['values']['weekly_updated']=p['updated_on']
            for c in head.values():
                if norm(c['raw']) in ('shark','ninja'): p['values']['brand']=c['raw'].strip().title()
            for rr,cells in block[1:4]:
                keys=sorted(cells)
                for n,col in enumerate(keys):
                    field=LABEL_INDEX.get(norm(cells[col]['raw']))
                    if not field: continue
                    for nc in keys[n+1:]:
                        v=cells[nc]
                        if v['raw']:
                            if norm(v['raw']) not in LABEL_INDEX and v['type']!='e':
                                value=v['raw'].strip()
                                p['values'][field]=normalize_skus(value) if field=='skus' else value
                                p['cells'][field]=v['ref']
                            break
            # A milestone header is recognized semantically; dates may be two rows below it.
            for bi,(rr,cells) in enumerate(block[1:10],1):
                matched=[(col,MS_INDEX.get(milestone_norm(c['raw']))) for col,c in cells.items()]
                matched=[(col,key) for col,key in matched if key]
                if len(matched)<2: continue
                header_cols=sorted((col,c) for col,c in cells.items() if c['raw'])
                for col,header_cell in header_cols:
                    key=MS_INDEX.get(milestone_norm(header_cell['raw']))
                    found=None;parse_error=None;error_cell=None
                    for dr,dc in block[bi+1:bi+4]:
                        if col not in dc or not dc[col]['raw'].strip():continue
                        candidate=dc[col]
                        default_year=int(str(p.get('updated_on'))[:4]) if p.get('updated_on') else None
                        candidate_value,candidate_error=read_date(candidate,b.epoch,default_year)
                        if candidate_value:
                            found=(candidate,candidate_value);break
                        # Continuation labels such as (CN)/(VN) are not bad dates.
                        if candidate_error!='blank_or_unscheduled':
                            parse_error=candidate_error;error_cell=candidate
                    if found:
                        found,value=found
                        task_name,milestone,ignored=classify_dated_task(header_cell['raw'],key)
                        if not ignored:
                            task={'date':value,'cell':found['ref'],'header':header_cell['raw'],'task_name':task_name,'milestone':milestone,'green':bool(found.get('green')),'concept':key}
                            p['dated_tasks'].append(task)
                        if key and key in ALL_PROJECT_CONCEPTS:
                            p['cells'][key]=found['ref'];p['values'][key]=value
                            p['milestones'][key]={'date':value,'cell':found['ref'],'header':header_cell['raw'],'green':bool(found.get('green'))}
                    elif error_cell:
                        label=key or 'dated_task_'+error_cell['ref']
                        p['unmapped'][label]={'raw':error_cell['raw'],'cell':error_cell['ref'],'reason':parse_error}
                        warnings.append({'pid':p['pid'],'cell':error_cell['ref'],'reason':parse_error,'raw':error_cell['raw']})
                break
            # Current Progress is Project-level current-state text, not a Task or Issue.
            for ci,(rr,cells) in enumerate(block):
                progress_cols=[col for col,c in cells.items() if norm(c['raw'])=='current progress']
                if not progress_cols:continue
                lo=progress_cols[0]; jira=[col for col,c in cells.items() if norm(c['raw'])=='jira summary'];hi=jira[0] if jira else 999
                chunks=[];first_cell=None
                for nr,ncells in block[ci+1:]:
                    if any(re.sub(r'[^a-z]','',norm(c['raw'])) in ('keyissues','keyissuestasks') for c in ncells.values()):break
                    for col,c in sorted(ncells.items()):
                        if lo<=col<hi and c['raw'] and c['type']!='e':
                            chunks.append(c['raw']);first_cell=first_cell or c['ref']
                if chunks:
                    p['values']['current_progress']='\n'.join(chunks).strip();p['cells']['current_progress']=first_cell
                break
            issue_header=None
            for rr,cells in block:
                if any(re.sub(r'[^a-z]','',norm(c['raw'])) in ('keyissues','keyissuestasks') for c in cells.values()): issue_header=(rr,cells); continue
                if any(norm(c['raw']) in ('safety & 3rd party test','first crd date','current progress','jira summary') for c in cells.values()): issue_header=None
                if issue_header and rr>issue_header[0]:
                    labels=sorted((col,norm(c['raw'])) for col,c in issue_header[1].items() if c['raw'])
                    values={};source_cells={}
                    for n,(lo,label) in enumerate(labels):
                        hi=labels[n+1][0] if n+1<len(labels) else 999
                        selected=[c for col,c in sorted(cells.items()) if lo<=col<hi and c['raw'] and c['type']!='e']
                        text='\n'.join(c['raw'] for c in selected)
                        if text:
                            values[label]=text
                            if selected:source_cells[label]=selected[0]
                    if values:
                        # Stop at an unrelated section instead of treating it as an Issue.
                        issue_text=next((v for label,v in values.items() if label.startswith('key issue')),None)
                        if issue_text:p['issues'].append({'row':rr,'values':values,'cells':source_cells})
                # Current Progress is handled above; Jira/Safety/CRD/13-week grey sections are intentionally ignored.
            # Keep every unrepresented source field in the plan; never silently drop it.
            for key,value in p['values'].items():
                if key not in ALL_PROJECT_CONCEPTS: p['unmapped'][key]={'raw':value,'cell':p['cells'].get(key),'reason':'no_confirmed_target_field'}
            if not p['pid']: warnings.append({'row':r0,'reason':'missing_or_ambiguous_project_id','name':p['values'].get('name')})
            projects.append(p)
        if not projects: raise ValueError('No Project Number header was found. Parsing stopped.')
        return {'source':str(pathlib.Path(path).resolve()),'sha256':digest(path),'projects':projects,'warnings':warnings}
    finally: b.close()

class Airtable:
    def __init__(self,config,log=None):
        self.config=config; c=config.get('airtable_credentials',config)
        self.log=log or (lambda msg:None)
        self.token=os.environ.get('AIRTABLE_TOKEN') or c.get('token','')
        self.base=c.get('base_id','appOMWiK4CTOH7iQu'); self.table=c.get('projects_table_id','tbllvOHZdwfBRWGM0')
        self.tasks=c.get('tasks_table_id','tblS2my1r93KothyZ'); self.issues=c.get('issues_table_id','tblqYHGaZL6FoTZHV')
        if not self.token: raise ValueError('Provide an Airtable token in the configuration file.')
    def request(self,path,method='GET',body=None):
        url='https://api.airtable.com/v0/'+path
        for attempt in range(4):
            req=urllib.request.Request(url,data=json.dumps(body).encode() if body is not None else None,headers={'Authorization':'Bearer '+self.token,'Content-Type':'application/json'},method=method)
            try:
                with urllib.request.urlopen(req,timeout=45) as resp: return json.load(resp)
            except urllib.error.HTTPError as e:
                if method=='GET' and e.code in (429,500,502,503,504) and attempt<3:
                    time.sleep(30 if e.code==429 else 2**attempt); continue
                detail=e.read().decode('utf-8','replace')[:500]
                raise RuntimeError(f'Airtable HTTP {e.code}: {detail}') from None
    def schema(self): return self.request('meta/bases/'+self.base+'/tables')
    def records(self,table,fields=None):
        out=[]; offset=None
        while True:
            q={'pageSize':100,'returnFieldsByFieldId':'true'}
            if offset: q['offset']=offset
            if fields:q['fields[]']=list(fields)
            data=self.request(self.base+'/'+table+'?'+urllib.parse.urlencode(q,doseq=True))
            out.extend(data['records']); offset=data.get('offset')
            self.log(f'{table}: {len(out)} records')
            if not offset: break
            time.sleep(.22)
        return out
    def snapshot(self,include_tasks=True,include_issues=True):
        schema=self.schema(); tables={t['id']:t for t in schema['tables']}
        project=tables[self.table]; links={}
        project_specs=dict(FIELDS)
        byname={norm(f['name']):f for f in project['fields']}
        for concept,(name,typ) in DYNAMIC_FIELDS.items():
            f=byname.get(norm(name))
            if f and f['type']==typ: project_specs[concept]=(f['id'],typ)
        wanted={f[0] for f in project_specs.values()}
        for f in project['fields']:
            if f['id'] in wanted and f['type']=='multipleRecordLinks':
                tid=f['options']['linkedTableId']
                if tid not in links:
                    fields=[tables[tid]['primaryFieldId']]
                    if tid==next((t['id'] for t in tables.values() if t['name']=='People'),None): fields += [PEOPLE_DEPARTMENT]
                    if tid==next((t['id'] for t in tables.values() if t['name']=='Factories'),None): fields += [FACTORY_CODE,FACTORY_OLD]
                    links[tid]=self.records(tid,fields)
        available={f['id'] for f in project['fields']}
        wanted=(wanted|{PID_FIELD,LAST_UPDATED_FIELD})&available
        task_available={f['id'] for f in tables[self.tasks]['fields']}
        issue_available={f['id'] for f in tables[self.issues]['fields']}
        return {
            'base':self.base,'table':self.table,'tasks_table':self.tasks,'issues_table':self.issues,
            'captured_at':dt.datetime.now(dt.timezone.utc).isoformat(),'schema':schema,
            'project_specs':project_specs,
            'projects':self.records(self.table,wanted),'links':links,
            'tasks':self.records(self.tasks,set(TASK_FIELDS.values())&task_available) if include_tasks else [],
            'issues':self.records(self.issues,set(ISSUE_FIELDS.values())&issue_available) if include_issues else [],
        }

ROLE_DEPARTMENTS={'npi':'NPI','npd':'NPD','pmo':'PMO'}
DEPARTMENT_PREFIXES=('PMO','NPI','NPD','DQTP','COMPLIANCE','CMF','SC','QUALITY','PD','ENG','PACKAGE','PLANNING','ID','ME','VAVE','TOOLING')
TASK_MILESTONES={
 'award':['Award'],'start':['Kick off'],'dqtp':['DQTP report'],'mp_aw':['MP AW release'],
 'compliance':['Compliance report'],'tra':['TRA','TRA / ECN DD'],'cut_steel':['Cut Steel'],'fot':['FOT'],
 'eb1':['EB1'],'eb2':['EB2'],'eb3':['EB3'],'pilot':['Pilot'],'mpra':['MPRA / ECN'],'mp':['MP Start'],
 'transfer_load':['Tooling Transfer Load'],'transfer_arrival':['Tooling Transfer Arrival'],
 'p1_cad':['P1 CAD DROP'],'p1_build':['P1 BUILD DATE'],'p2_cad':['P2 CAD DROP'],'p2_build':['P2 BUILD DATE'],
 'p3_cad':['P3 CAD DROP'],'p3_build':['P3 BUILD DATE'],'last_p':['Last P'],'last_p_build':['Last P BUILD DATE'],
}

def _tokens(value):
    return re.findall(r'[a-z0-9]+',unicodedata.normalize('NFKC',str(value or '')).casefold())

def _abbreviation_match(source,candidate):
    s=_tokens(source); c=_tokens(candidate)
    if not s or not c:return False
    if len(s)==1:return s[0] in (c[0],c[-1])
    # Source tokens may be initials/prefixes, but must align in order.
    pos=0
    for token in s:
        while pos<len(c) and not c[pos].startswith(token):pos+=1
        if pos==len(c):return False
        pos+=1
    return True

def _split_people(value):
    return [x.strip() for x in re.split(r'[;,\n]+',str(value or '')) if x.strip()]

def _strip_department(value):
    text=str(value or '').strip(); dept=None
    m=re.match(r'^('+'|'.join(DEPARTMENT_PREFIXES)+r')\s*[-:]\s*(.+)$',text,re.I)
    if m:dept=m.group(1).upper();text=m.group(2).strip()
    return text,dept

def resolve_people(value,records,department=None):
    resolved=[];display=[]
    for raw in _split_people(value):
        name,inline_dept=_strip_department(raw); expected=norm(inline_dept or department)
        pool=[r for r in records if not expected or norm(r['fields'].get(PEOPLE_DEPARTMENT))==expected]
        exact=[r for r in pool if norm(r['fields'].get(PEOPLE_NAME))==norm(name)]
        candidates=exact if len(exact)==1 else [r for r in pool if _abbreviation_match(name,r['fields'].get(PEOPLE_NAME))]
        if len(candidates)!=1:return None,None,{'name':raw,'department':inline_dept or department,'candidate_names':[r['fields'].get(PEOPLE_NAME) for r in candidates[:20]]}
        resolved.append(candidates[0]['id']);display.append(candidates[0]['fields'].get(PEOPLE_NAME))
    return resolved,display,None

def resolve_factory(value,records):
    candidates=[]
    for r in records:
        aliases=[r['fields'].get(FACTORY_NAME),r['fields'].get(FACTORY_CODE),r['fields'].get(FACTORY_OLD)]
        if any(norm(value)==norm(x) for x in aliases if x):candidates.append(r)
    if len(candidates)!=1:return None,None,{'value':value,'candidate_names':[r['fields'].get(FACTORY_NAME) for r in candidates[:20]]}
    return [candidates[0]['id']],[candidates[0]['fields'].get(FACTORY_NAME)],None

def _issue_value(issue,prefix):
    return next((v for k,v in issue.get('values',{}).items() if k.startswith(prefix)),None)

def _issue_cell(issue,prefix):
    return next((v for k,v in issue.get('cells',{}).items() if k.startswith(prefix)),None)

def issue_text_clean(value):
    return re.sub(r'^\s*\d+\s*[\.\)\]:-]\s*','',str(value or '').strip())

def issue_key(value):
    return re.sub(r'[^a-z0-9]+','',norm(issue_text_clean(value)))

def capacity_number(value):
    text=str(value or '').strip().replace(',','')
    m=re.fullmatch(r'(\d+(?:\.\d+)?)\s*[kK](?:\s*/?\s*(?:m|month))?',text)
    if m:return float(m.group(1))*1000
    try:return float(text)
    except ValueError:return None

def _task_milestone(concept,entry):
    names=TASK_MILESTONES.get(concept,[])
    if concept=='tra' and 'ecn' in norm(entry.get('header')):return ['TRA / ECN DD','TRA']
    return names

def make_airtable_plan(parsed,snapshot):
    tables={t['id']:t for t in snapshot['schema']['tables']}
    project_table=tables[snapshot['table']]; schemas={tid:{f['id']:f for f in t['fields']} for tid,t in tables.items()}
    project_fields_by_name={norm(f['name']):f for f in project_table['fields']}
    project_specs=snapshot.get('project_specs',FIELDS)
    existing=collections.defaultdict(list)
    for r in snapshot['projects']: existing[pid(r['fields'].get(PID_FIELD))].append(r)
    incoming=collections.Counter(p['pid'] for p in parsed['projects'])
    changes=[]; skipped=[]; blockers=[]
    people_table=next((t for t in tables.values() if t.get('name')=='People'),None)
    factory_table=next((t for t in tables.values() if t.get('name')=='Factories'),None)
    people=snapshot.get('links',{}).get(people_table['id'],[]) if people_table else []
    factories=snapshot.get('links',{}).get(factory_table['id'],[]) if factory_table else []
    link_display={}
    for table_id,records in snapshot.get('links',{}).items():
        for linked in records:
            fields=linked.get('fields',{})
            preferred=fields.get(PEOPLE_NAME) or fields.get(FACTORY_NAME)
            link_display[linked['id']]=preferred or next((str(v) for v in fields.values() if v not in (None,'',[])),linked['id'])
    tasks=snapshot.get('tasks',[]);issues=snapshot.get('issues',[])
    tasks_by_project=collections.defaultdict(list);issues_by_project=collections.defaultdict(list)
    for r in tasks:
        for project_id in r['fields'].get(TASK_FIELDS['project'],[]):tasks_by_project[project_id].append(r)
    for r in issues:
        for project_id in r['fields'].get(ISSUE_FIELDS['project'],[]):issues_by_project[project_id].append(r)

    def add_update(pid_value,table_id,record,field_id,new,display_new=None,source_cell=None,display_field_name=None):
        field=schemas[table_id][field_id];old=record['fields'].get(field_id)
        if old!=new:
            display_old=old
            if field['type']=='multipleRecordLinks' and isinstance(old,list):display_old=', '.join(link_display.get(x,x) for x in old)
            changes.append({'op':'update','table':table_id,'pid':pid_value,'record':record['id'],'field':field_id,'field_name':display_field_name or field['name'],'type':field['type'],'old':old,'display_old':display_old,'new':new,'display_new':display_new if display_new is not None else new,'source_cell':source_cell})

    for p in parsed['projects']:
        key=p['pid']; matches=existing.get(key,[])
        if not key or incoming[key]!=1 or len(matches)!=1:
            skipped.append({'pid':key,'reason':'missing_id_or_duplicate_or_no_target','row':p['row'],'target_count':len(matches)}); continue
        rec=matches[0];project_record_id=rec['id']
        weekly_spec=project_specs.get('weekly_updated')
        target_updated=rec['fields'].get(weekly_spec[0]) if weekly_spec else rec['fields'].get(LAST_UPDATED_FIELD)
        if p.get('updated_on') and target_updated and p['updated_on']<str(target_updated)[:10]:
            skipped.append({'pid':key,'reason':'source_report_older_than_airtable_last_updated','report_date':p['updated_on'],'target_date':target_updated});continue
        for concept,value in p['values'].items():
            spec=project_specs.get(concept)
            if not spec:
                if concept in DYNAMIC_FIELDS:
                    required_name,required_type=DYNAMIC_FIELDS[concept];current=project_fields_by_name.get(norm(required_name))
                    reason='required_project_field_wrong_type' if current else 'required_project_field_not_created'
                    item={'pid':key,'concept':concept,'field_name':required_name,'field_type':required_type,'actual_type':current.get('type') if current else None,'value':value,'reason':reason}
                    skipped.append(item);blockers.append(item)
                continue
            fid,typ=spec;field=schemas[snapshot['table']].get(fid);reason=None;display=value;detail=None
            if not field or field['type']!=typ:reason='target_field_missing_or_type_changed'
            elif concept=='capacity':
                parsed_capacity=capacity_number(value)
                if parsed_capacity is None:reason='capacity_not_numeric'
                else:value=parsed_capacity;display=parsed_capacity
            elif typ=='singleSelect':
                options={norm(x['name']):x['name'] for x in field['options']['choices']}
                v={'delay':'delayed'}.get(norm(value),norm(value)) if concept=='status' else norm(value)
                if v not in options:reason='select_option_not_found'
                else:value=display=options[v]
            elif typ=='multipleRecordLinks':
                tid=field['options']['linkedTableId']
                if people_table and tid==people_table['id']:
                    value,names,detail=resolve_people(value,people,ROLE_DEPARTMENTS.get(concept));display=', '.join(names or [])
                elif factory_table and tid==factory_table['id']:
                    value,names,detail=resolve_factory(value,factories);display=', '.join(names or [])
                else:detail={'value':value}
                if value is None:reason='linked_record_not_unique_after_department_match'
            if reason:
                skipped.append({'pid':key,'concept':concept,'value':display or p['values'][concept],'reason':reason,'detail':detail});continue
            if value not in (None,'',[]):add_update(key,snapshot['table'],rec,fid,value,display,p['cells'].get(concept),PROJECT_DISPLAY_NAMES.get(concept,DYNAMIC_FIELDS.get(concept,(field['name'],))[0]))

        # Weekly issues belong in the Issues table, not in Project text fields.
        for issue in p.get('issues',[]):
            issue_text=issue_text_clean(_issue_value(issue,'key issue'))
            if not issue_text:continue
            exact=[r for r in issues_by_project[project_record_id] if issue_key(r['fields'].get(ISSUE_FIELDS['record']))==issue_key(issue_text)]
            action=_issue_value(issue,'action');owner_raw=_issue_value(issue,'owner');due_raw=_issue_value(issue,'due date')
            severity_raw=_issue_value(issue,'risk')
            owner_ids=owner_names=None;owner_error=None
            if owner_raw:owner_ids,owner_names,owner_error=resolve_people(owner_raw,people)
            due_date=None
            if due_raw:
                due_cell=_issue_cell(issue,'due date') or {'active':due_raw,'raw':due_raw,'type':'s'}
                default_year=int(str(p.get('updated_on'))[:4]) if p.get('updated_on') else None
                due_date,due_error=read_date(due_cell,dt.datetime(1899,12,30),default_year)
                if due_error and due_error!='blank_or_unscheduled':skipped.append({'pid':key,'reason':'issue_due_date_not_understood','value':due_raw,'detail':due_error})
            issue_fields={ISSUE_FIELDS['record']:issue_text,ISSUE_FIELDS['project']:[project_record_id],ISSUE_FIELDS['status']:'Open'}
            if action:issue_fields[ISSUE_FIELDS['action']]=action
            if owner_ids:issue_fields[ISSUE_FIELDS['owners']]=owner_ids
            if due_date:issue_fields[ISSUE_FIELDS['target_date']]=due_date
            severity={'h':'High','m':'Medium','l':'Low'}.get(norm(severity_raw))
            if severity:issue_fields[ISSUE_FIELDS['severity']]=severity
            elif severity_raw:skipped.append({'pid':key,'reason':'issue_severity_not_understood','value':severity_raw})
            if p.get('updated_on'):issue_fields[ISSUE_FIELDS['record_date']]=p['updated_on']
            if owner_error:skipped.append({'pid':key,'reason':'issue_owner_not_unique','value':owner_raw,'detail':owner_error})
            if len(exact)==0:
                changes.append({'op':'create','table':snapshot['issues_table'],'pid':key,'record':None,'field':ISSUE_FIELDS['record'],'field_name':'Issue Record (Manual)','type':'record','old':'','new':issue_fields,'display_new':issue_text,'source_row':issue.get('row')})
            elif len(exact)==1:
                target=exact[0]
                for field_id,new_value in issue_fields.items():
                    if field_id in (ISSUE_FIELDS['record'],ISSUE_FIELDS['project'],ISSUE_FIELDS['status']):continue
                    display_value=', '.join(owner_names or []) if field_id==ISSUE_FIELDS['owners'] else new_value
                    add_update(key,snapshot['issues_table'],target,field_id,new_value,display_value)
            else:skipped.append({'pid':key,'reason':'duplicate_exact_issue_records','issue':issue_text,'count':len(exact)})

        # Every dated red-section item is a Task. Only approved fixed names populate Milestone (Manual).
        task_table_id=snapshot.get('tasks_table')
        milestone_field=schemas.get(task_table_id,{}).get(TASK_FIELDS['milestone'],{})
        milestone_options={norm(x['name']):x['name'] for x in milestone_field.get('options',{}).get('choices',[])}
        for entry in p.get('dated_tasks',[]):
            if not task_table_id:
                skipped.append({'pid':key,'reason':'tasks_table_not_available','task_name':entry.get('task_name')});continue
            task_name=entry['task_name'];milestone=entry.get('milestone')
            if milestone:
                resolved_option=milestone_options.get(norm(milestone))
                if not resolved_option and milestone=='FPO Release':resolved_option=milestone
                if not resolved_option:
                    skipped.append({'pid':key,'reason':'required_milestone_option_missing','milestone':milestone,'header':entry.get('header')});continue
                milestone=resolved_option
            start_date=entry['date'];days=0 if milestone in ('Award','MP Start') else 7
            due_date=(dt.date.fromisoformat(start_date)+dt.timedelta(days=days)).isoformat()
            project_tasks=tasks_by_project[project_record_id]
            candidates=[r for r in project_tasks if norm(r['fields'].get(TASK_FIELDS['name']))==norm(task_name)]
            if not candidates and milestone and norm(task_name)==norm(milestone):
                candidates=[r for r in project_tasks if norm(r['fields'].get(TASK_FIELDS['milestone']))==norm(milestone)]
            default_owners=rec['fields'].get(FIELDS['npi'][0],[])
            if len(candidates)==0:
                fields={TASK_FIELDS['name']:task_name,TASK_FIELDS['project']:[project_record_id],TASK_FIELDS['start']:start_date,TASK_FIELDS['due']:due_date}
                if milestone:fields[TASK_FIELDS['milestone']]=milestone
                if default_owners:fields[TASK_FIELDS['owners']]=default_owners
                if entry.get('green') and default_owners:fields[TASK_FIELDS['completed_by']]=default_owners
                changes.append({'op':'create','table':task_table_id,'pid':key,'record':None,'field':TASK_FIELDS['name'],'field_name':'Task Name (Manual)','type':'record','old':'','new':fields,'display_new':task_name,'source_cell':entry.get('cell')})
            elif len(candidates)==1:
                task=candidates[0]
                add_update(key,task_table_id,task,TASK_FIELDS['start'],start_date,start_date,entry.get('cell'))
                add_update(key,task_table_id,task,TASK_FIELDS['due'],due_date,due_date,entry.get('cell'))
                if milestone and not task['fields'].get(TASK_FIELDS['milestone']):add_update(key,task_table_id,task,TASK_FIELDS['milestone'],milestone,milestone,entry.get('cell'))
                owners=task['fields'].get(TASK_FIELDS['owners'],[]) or default_owners
                if not task['fields'].get(TASK_FIELDS['owners']) and owners:
                    names=[r['fields'].get(PEOPLE_NAME) for r in people if r['id'] in owners]
                    add_update(key,task_table_id,task,TASK_FIELDS['owners'],owners,', '.join(names),entry.get('cell'))
                if entry.get('green') and not task['fields'].get(TASK_FIELDS['completed_by']):
                    if owners:
                        names=[r['fields'].get(PEOPLE_NAME) for r in people if r['id'] in owners]
                        add_update(key,task_table_id,task,TASK_FIELDS['completed_by'],owners,', '.join(names),entry.get('cell'))
                    else:skipped.append({'pid':key,'reason':'green_task_has_no_owner','task_name':task_name,'task':task['id']})
            else:skipped.append({'pid':key,'reason':'duplicate_task_identity','task_name':task_name,'count':len(candidates)})
        for concept,data in p['unmapped'].items():skipped.append({'pid':key,'concept':concept,**data})
        if p.get('sections'):skipped.append({'pid':key,'reason':'additional_source_sections_preserved_for_mapping','sections':p['sections']})
    unique_blockers=[];seen_blockers=set()
    for item in blockers:
        key=(item['concept'],item['field_name'])
        if key not in seen_blockers:seen_blockers.add(key);unique_blockers.append(item)
    return {'kind':'weekly_to_airtable','base':snapshot['base'],'table':snapshot['table'],'tasks_table':snapshot.get('tasks_table'),'issues_table':snapshot.get('issues_table'),'source':parsed['source'],'source_sha256':parsed['sha256'],'changes':changes,'skipped':skipped,'warnings':parsed['warnings'],'blockers':unique_blockers}

def apply_airtable(plan,api,journal,progress=None):
    if plan.get('kind')!='weekly_to_airtable': raise ValueError('Wrong plan type')
    if plan.get('blockers'):raise ValueError('Required Project fields are missing. Create them before execution.')
    if plan['base']!=api.base or plan['table']!=api.table: raise ValueError('Configuration does not match the reviewed preview.')
    if digest(plan['source'])!=plan['source_sha256']: raise ValueError('The Weekly Report changed. Generate a new preview.')
    schema_tables={t['id']:t for t in api.schema()['tables']}
    schemas={tid:{f['id']:f for f in t['fields']} for tid,t in schema_tables.items()}
    touched={ch.get('table',plan['table']) for ch in plan['changes'] if ch.get('op','update')=='update'}
    current={tid:{r['id']:r for r in api.records(tid)} for tid in touched}
    todo=collections.defaultdict(lambda:collections.defaultdict(dict)); backup=[]; creates=collections.defaultdict(list)
    for ch in plan['changes']:
        tid=ch.get('table',plan['table'])
        if ch.get('op')=='create':
            missing=[fid for fid in ch['new'] if fid not in schemas.get(tid,{})]
            if missing:raise ValueError('Create target fields changed after preview: '+', '.join(missing))
            creates[tid].append(ch);continue
        f=schemas.get(tid,{}).get(ch['field'])
        if not f or f['type']!=ch['type']: raise ValueError('A target field changed. Generate a new preview.')
        now=current.get(tid,{}).get(ch['record'],{}).get('fields',{}).get(ch['field'])
        if now==ch['new']: continue
        if now!=ch['old']: raise ValueError(f"{ch['pid']} / {ch['field_name']} was changed after preview. Generate a new preview.")
        todo[tid][ch['record']][ch['field']]=ch['new']; backup.append(current[tid][ch['record']])
    pending=[f'{tid}:{rid}' for tid,rows in todo.items() for rid in rows]
    pending += [f'{tid}:create:{i}' for tid,rows in creates.items() for i,_ in enumerate(rows)]
    result={'before':backup,'confirmed':[],'created':[],'pending':pending,'status':'started'}; save_json(journal,result)
    total=max(1,len(pending));done=0
    try:
        for tid,rows in todo.items():
            items=list(rows.items())
            for i in range(0,len(items),10):
                batch=items[i:i+10]
                api.request(api.base+'/'+tid,'PATCH',{'records':[{'id':rid,'fields':fields} for rid,fields in batch],'typecast':tid==api.tasks})
                for rid,fields in batch:
                    rec=api.request(api.base+'/'+tid+'/'+rid+'?returnFieldsByFieldId=true')
                    if any(rec['fields'].get(f)!=v for f,v in fields.items()): raise RuntimeError('Post-write verification failed: '+rid)
                    key=f'{tid}:{rid}';result['confirmed'].append(key);result['pending'].remove(key);done+=1
                    if progress:progress(done,total)
                save_json(journal,result);time.sleep(.22)
        for tid,rows in creates.items():
            for i in range(0,len(rows),10):
                batch=rows[i:i+10]
                response=api.request(api.base+'/'+tid,'POST',{'records':[{'fields':ch['new']} for ch in batch],'typecast':tid==api.tasks})
                for offset,record in enumerate(response.get('records',[])):
                    original=i+offset;key=f'{tid}:create:{original}'
                    result['created'].append({'table':tid,'record':record['id'],'pid':batch[offset]['pid']})
                    if key in result['pending']:result['pending'].remove(key)
                    done+=1
                    if progress:progress(done,total)
                save_json(journal,result);time.sleep(.22)
    except Exception:
        result['status']='needs_reconciliation';save_json(journal,result);raise
    result['status']='verified';save_json(journal,result)
    return result

# Only current engineering dates and explicit previous revision dates are exported.
# Original TRA / Original MP Ready at KO are deliberately absent.
TRACKER={
 'start':'Eng , OEM Kick Off','tra':'TRA','cut_steel':'Cut Steel','fot':'FOT','eb1':'EB1','eb2':'EB2','eb3':'EB3',
 'transfer_load':'Tooling Transfer Load','transfer_arrival':'Tooling Transfer Arrival','pilot':'Pilot',
 'mpra':'MPRA , ECN','mp':'MP START','previous_mp':'Previous MP Start Date',
 'p1_cad':'P1 CAD DROP','p2_cad':'P2 CAD DROP','p3_cad':'P3 CAD DROP','last_p':'Last P',
 'name':'Project Name , Description','model':'Base Model','skus':'SKUs Kicked Off',
 'type':'Project Type','brand':'Brand',
 'program_code':'Program Code','ale_id':'ALE_ID','launch_year':'Target Launch Year',
 'factory':('Manufacturing Factory','Development Factory'),'country':'Country','status':'Eng Status','sc':'SC Leader',
 'npi':('NPI Project Lead','NPI LEADER'),'npd':('NPD Project Lead','NPD LEADER'),
}
def make_tracker_plan(snapshot,path):
    b=Book(path)
    try:
        sheets=[s for s in b.sheets if norm(s)=='all projects']
        if len(sheets)!=1: raise ValueError('Exactly one ALL PROJECTS sheet is required.')
        sheet=sheets[0]
        try: rows=list(b.tracker_rows(sheet))
        except (zipfile.BadZipFile, ET.ParseError):
            raise ValueError('The All Tracker file is damaged and cannot be written safely. Download a clean copy from SharePoint/OneDrive.') from None
        header=None
        for r,cells in rows[:10]:
            if any(norm(c['raw'])=='project number' for c in cells.values()): header=(r,cells); break
        if header is None: raise ValueError('The Project Number header was not found.')
        bylabel=collections.defaultdict(list)
        for c,v in header[1].items(): bylabel[norm(v['raw'])].append(c)
        if len(bylabel['project number'])!=1: raise ValueError('The Project Number column is not unique.')
        pc=bylabel['project number'][0]; dest=collections.defaultdict(list)
        for r,c in rows:
            if r>header[0] and pid(c.get(pc,{}).get('raw')): dest[pid(c[pc]['raw'])].append((r,c))
        source=collections.defaultdict(list)
        table_schema={t['id']:t for t in snapshot.get('schema',{}).get('tables',[])}
        link_names={}
        for table_id,records in snapshot.get('links',{}).items():
            primary=table_schema.get(table_id,{}).get('primaryFieldId')
            for r in records:
                fields=r.get('fields',{});value=fields.get(primary) if primary else None
                link_names[r['id']]=str(value) if value not in (None,'') else next((str(v) for v in fields.values() if v not in (None,'')),r['id'])
        for rec in snapshot['projects']:
            key=pid(rec['fields'].get(PID_FIELD))
            if key: source[key].append(rec)
        fpo_by_project=collections.defaultdict(list)
        for task in snapshot.get('tasks',[]):
            tf=task.get('fields',{})
            if norm(tf.get(TASK_FIELDS['milestone']))!=norm('FPO Release'):continue
            value=tf.get(TASK_FIELDS['start']) or tf.get(TASK_FIELDS['due'])
            if not value:continue
            for project_record_id in tf.get(TASK_FIELDS['project'],[]):
                fpo_by_project[project_record_id].append(value)
        changes=[]; skipped=[]
        for key,recs in source.items():
            matches=dest.get(key,[])
            if len(recs)!=1 or len(matches)!=1:
                skipped.append({'pid':key,'reason':'project_id_not_unique_or_not_in_tracker','airtable_count':len(recs),'tracker_count':len(matches)}); continue
            rr,cells=matches[0]; fields=recs[0]['fields']
            for concept,label in TRACKER.items():
                spec=snapshot.get('project_specs',{}).get(concept) or SOURCE_FIELDS.get(concept)
                if not spec:
                    skipped.append({'pid':key,'field':str(label),'reason':'airtable_source_field_missing'});continue
                fid,typ=spec; val=fields.get(fid)
                if val is None or val=='': continue
                if typ=='multipleRecordLinks':
                    unresolved=[x for x in val if x not in link_names]
                    if unresolved:skipped.append({'pid':key,'field':label,'reason':'linked_record_name_not_resolved','record_ids':unresolved});continue
                    val='\n'.join(link_names[x] for x in val)
                elif isinstance(val,list):
                    val='\n'.join(str(x.get('name',x) if isinstance(x,dict) else x) for x in val if x not in (None,''))
                elif isinstance(val,dict):val=val.get('name',str(val))
                aliases=(label,) if isinstance(label,str) else label
                cols=[]
                for alias in aliases:
                    if len(bylabel[norm(alias)])==1:cols=bylabel[norm(alias)];label=alias;break
                if len(cols)!=1: skipped.append({'pid':key,'field':label,'reason':'header_not_unique_or_missing'});continue
                col=cols[0]; old=cells.get(col,{'ref':colletter(col)+str(rr),'raw':'','type':None,'style':0,'formula':None})
                if old['formula'] is not None: skipped.append({'pid':key,'cell':old['ref'],'reason':'protected_formula'});continue
                if typ=='date':
                    try: date=dt.date.fromisoformat(val)
                    except (ValueError,TypeError): skipped.append({'pid':key,'field':label,'reason':'invalid_airtable_date'});continue
                    oldval,_=read_date(old,b.epoch); new=(dt.datetime.combine(date,dt.time())-b.epoch).days
                    if oldval==val: continue
                    # Preserve deliberate no-demand/TBC markers, or unreadable multi-date history.
                    if old['raw'].strip() and oldval is None:
                        skipped.append({'pid':key,'cell':old['ref'],'reason':'tracker_date_text_requires_review','old':old['raw'],'proposed':val});continue
                else:
                    new=val
                    if line_norm(old['raw']).strip()==line_norm(val).strip():continue
                changes.append({'pid':key,'cell':old['ref'],'field':label,'old':old['raw'],'new':new,'display_new':val,'style':old['style'],'type':typ})
            # FPO is maintained as a fixed milestone Task, while All Tracker
            # stores it in a dedicated Project-row column.
            fpo_dates=sorted(set(fpo_by_project.get(recs[0]['id'],[])))
            fpo_cols=bylabel[norm('FPO Release Date')]
            if len(fpo_dates)>1:
                skipped.append({'pid':key,'field':'FPO Release Date','reason':'multiple_fpo_milestone_dates','dates':fpo_dates})
            elif len(fpo_dates)==1 and len(fpo_cols)==1:
                val=fpo_dates[0];col=fpo_cols[0]
                old=cells.get(col,{'ref':colletter(col)+str(rr),'raw':'','type':None,'style':0,'formula':None})
                if old['formula'] is not None:skipped.append({'pid':key,'cell':old['ref'],'reason':'protected_formula'})
                else:
                    try:date=dt.date.fromisoformat(val)
                    except (ValueError,TypeError):skipped.append({'pid':key,'field':'FPO Release Date','reason':'invalid_airtable_date'})
                    else:
                        oldval,_=read_date(old,b.epoch);new=(dt.datetime.combine(date,dt.time())-b.epoch).days
                        if oldval!=val:
                            if old['raw'].strip() and oldval is None:skipped.append({'pid':key,'cell':old['ref'],'reason':'tracker_date_text_requires_review','old':old['raw'],'proposed':val})
                            else:changes.append({'pid':key,'cell':old['ref'],'field':'FPO Release Date','old':old['raw'],'new':new,'display_new':val,'style':old['style'],'type':'date'})
            # Append current Issue + Recovery Action to Engineering Remarks without replacing history.
            remark_cols=[]
            for alias in ('Engineering Remarks','Engineering Remark'):
                if len(bylabel[norm(alias)])==1:remark_cols=bylabel[norm(alias)];break
            if remark_cols:
                open_issues=[]
                for issue in snapshot.get('issues',[]):
                    if recs[0]['id'] not in issue.get('fields',{}).get(ISSUE_FIELDS['project'],[]):continue
                    status=issue['fields'].get(ISSUE_FIELDS['status'],'')
                    if norm(status)=='closed':continue
                    title=issue['fields'].get(ISSUE_FIELDS['record'],'').strip();action=issue['fields'].get(ISSUE_FIELDS['action'],'').strip()
                    if title:open_issues.append(f"Issue: {title}"+(f" | Next Action: {action}" if action else ''))
                if open_issues:
                    col=remark_cols[0];old=cells.get(col,{'ref':colletter(col)+str(rr),'raw':'','type':None,'style':0,'formula':None})
                    if old['formula'] is not None:skipped.append({'pid':key,'cell':old['ref'],'reason':'protected_formula'})
                    else:
                        stamp=dt.date.today().isoformat();begin=f'[AutoPM {key} BEGIN]';end=f'[AutoPM {key} END]'
                        prior=re.sub(re.escape(begin)+r'.*?'+re.escape(end),'',line_norm(old['raw']),flags=re.S).strip()
                        block=begin+'\n'+f'Updated {stamp}\n'+'\n'.join(open_issues)+'\n'+end
                        new=(prior+'\n\n'+block).strip() if prior else block
                        if line_norm(old['raw']).strip()!=new:changes.append({'pid':key,'cell':old['ref'],'field':'Engineering Remarks','old':old['raw'],'new':new,'display_new':new,'style':old['style'],'type':'multilineText'})
        return {'kind':'airtable_to_tracker','base':snapshot['base'],'table':snapshot['table'],'source':str(pathlib.Path(path).resolve()),'source_sha256':digest(path),'sheet':sheet,'sheet_part':b.sheets[sheet],'changes':changes,'skipped':skipped,'warnings':['Project Status exports one-way to All Tracker Eng Status. It never changes Airtable Status.','Category, Sub Category, and Date Added are intentionally not exported.','Current Issues and Recovery Actions are appended to Engineering Remarks with a dated AutoPM block. Existing remarks are preserved.']}
    finally:b.close()

def _green_styles(styles_xml,base_style_ids):
    """Return styles.xml plus a map to temporary green-fill cell styles."""
    if not styles_xml:return None,{sid:sid for sid in base_style_ids}
    # Preserve the workbook's namespace prefixes. Excel validates the prefixes
    # named inside mc:Ignorable; allowing ElementTree to rename them to ns1,
    # ns2, ... makes styles.xml invalid even though it is well-formed XML.
    source_text=styles_xml.decode('utf-8','replace')
    namespace_map=dict(re.findall(r'xmlns:([A-Za-z_][\w.-]*)="([^"]+)"',source_text))
    for prefix,uri in namespace_map.items():
        ET.register_namespace(prefix,uri)
    ET.register_namespace('',NS)
    root=ET.fromstring(styles_xml);fills=root.find('m:fills',N);xfs=root.find('m:cellXfs',N)
    if fills is None or xfs is None:return styles_xml,{sid:sid for sid in base_style_ids}
    fill=ET.Element('{'+NS+'}fill');pattern=ET.SubElement(fill,'{'+NS+'}patternFill',{'patternType':'solid'})
    ET.SubElement(pattern,'{'+NS+'}fgColor',{'rgb':'FFC6EFCE'});ET.SubElement(pattern,'{'+NS+'}bgColor',{'indexed':'64'})
    fill_id=len(fills);fills.append(fill);fills.set('count',str(len(fills)))
    style_map={}
    for sid in sorted(set(base_style_ids)):
        if sid<0 or sid>=len(xfs):sid=0
        xf=copy.deepcopy(xfs[sid]);xf.set('fillId',str(fill_id));xf.set('applyFill','1')
        style_map[sid]=len(xfs);xfs.append(xf)
    xfs.set('count',str(len(xfs)))
    rendered=ET.tostring(root,encoding='utf-8',xml_declaration=True)
    # Fail closed if a namespace referenced by mc:Ignorable was lost.
    rendered_text=rendered.decode('utf-8','replace')
    ignorable=re.search(r'(?:mc:Ignorable|\{[^}]+\}Ignorable)="([^"]+)"',rendered_text)
    if ignorable:
        missing=[p for p in ignorable.group(1).split() if not re.search(rf'xmlns:{re.escape(p)}="',rendered_text)]
        if missing:
            declarations=''.join(f' xmlns:{p}="{namespace_map[p]}"' for p in missing if p in namespace_map)
            rendered_text=rendered_text.replace('<styleSheet','<styleSheet'+declarations,1)
            still_missing=[p for p in missing if not re.search(rf'xmlns:{re.escape(p)}="',rendered_text)]
            if still_missing:raise ValueError('Styles namespace preservation failed: '+', '.join(still_missing))
            rendered=rendered_text.encode('utf-8')
    return rendered,style_map

def apply_tracker(plan,output):
    src=pathlib.Path(plan['source']); output=pathlib.Path(output)
    if plan.get('kind')!='airtable_to_tracker': raise ValueError('Wrong plan type')
    if output.resolve()==src.resolve() or output.exists(): raise ValueError('Output must be a new file so the source remains untouched.')
    if digest(src)!=plan['source_sha256']: raise ValueError('All Tracker changed after preview. Generate a new preview.')
    with zipfile.ZipFile(src) as z:
        changes={c['cell']:c for c in plan['changes']}; seen=set()
        styles_xml=z.read('xl/styles.xml') if 'xl/styles.xml' in z.namelist() else None
        new_styles,green_style_map=_green_styles(styles_xml,[c.get('style',0) for c in plan['changes']])
        byrow=collections.defaultdict(dict)
        for ref,ch in changes.items():byrow[int(re.search(r'\d+',ref)[0])][ref]=ch
        def update_row(match):
            text=match.group(0); row=int(re.search(r'\br="(\d+)"',text)[1])
            todo=byrow.get(row,{})
            if not todo:return text
            def render(ch,old=None):
                if old and re.search(r'<(?:\w+:)?f(?:\s|>)',old): raise ValueError('Refusing to overwrite formula '+ch['cell'])
                val=ch['new']; ref=ch['cell']; st=green_style_map.get(ch.get('style',0),ch.get('style',0))
                if ch['type']=='date':return f'<c r="{ref}" s="{st}"><v>{val}</v></c>'
                return f'<c r="{ref}" s="{st}" t="inlineStr"><is><t xml:space="preserve">{escape(str(val))}</t></is></c>'
            def replace_cell(m):
                ref=re.search(r'\br="([A-Z]+\d+)"',m.group(0))[1]
                if ref not in todo:return m.group(0)
                seen.add(ref);return render(todo[ref],m.group(0))
            text=re.sub(r'<c\b[^>]*?(?:/>|>.*?</c>)',replace_cell,text,flags=re.S)
            for ref,ch in todo.items():
                if ref in seen: continue
                new=render(ch); higher=re.search(r'<c\b[^>]*\br="([A-Z]+\d+)"',text)
                insert=None
                for m in re.finditer(r'<c\b[^>]*\br="([A-Z]+\d+)"',text):
                    if colnum(m[1])>colnum(ref):insert=m.start();break
                if insert is None:insert=text.rfind('</row>')
                text=text[:insert]+new+text[insert:];seen.add(ref)
            return text
        wb=z.read('xl/workbook.xml').decode('utf-8')
        calc='<calcPr calcId="0" fullCalcOnLoad="1" forceFullCalc="1"/>'
        wb=re.sub(r'<calcPr\b[^>]*/>',calc,wb) if '<calcPr' in wb else wb.replace('</workbook>',calc+'</workbook>')
        tmp=output.with_suffix(output.suffix+'.partial')
        try:
            with zipfile.ZipFile(tmp,'w') as out:
                for info in z.infolist():
                    if info.filename==plan['sheet_part']:
                        with z.open(info) as source,out.open(info,'w',force_zip64=True) as target:
                            for isrow,segment in xml_segments(source):
                                if isrow:
                                    rr=int(re.search(rb'\br="(\d+)"',segment)[1])
                                    if rr in byrow:
                                        text=segment.decode('utf-8')
                                        segment=re.sub(r'<row\b[^>]*>.*?</row>',update_row,text,flags=re.S).encode('utf-8')
                                        ET.fromstring(segment)
                                target.write(segment)
                        if seen!=set(changes):raise ValueError('Some target cells could not be located. Output stopped.')
                    elif info.filename=='xl/workbook.xml':out.writestr(info,wb.encode())
                    elif info.filename=='xl/styles.xml' and new_styles is not None:out.writestr(info,new_styles)
                    else:
                        with z.open(info) as source, out.open(info,'w',force_zip64=True) as target:
                            for data in iter(lambda:source.read(1024*1024),b''):target.write(data)
            with zipfile.ZipFile(tmp) as check:
                for info in z.infolist():
                    if info.filename not in (plan['sheet_part'],'xl/workbook.xml','xl/styles.xml') and info.CRC!=check.getinfo(info.filename).CRC:
                        raise ValueError('Untouched-content checksum failed: '+info.filename)
            # Verify every target cell after writing, before releasing the output.
            book=Book(tmp)
            actual={v['ref']:v['raw'] for _,row in book.tracker_rows(plan['sheet']) for v in row.values() if v['ref'] in changes}; book.close()
            mismatches=[{'cell':ref,'expected':str(ch['new']),'actual':actual.get(ref)} for ref,ch in changes.items() if line_norm(actual.get(ref))!=line_norm(ch['new'])]
            if mismatches:raise ValueError('Output verification failed: '+json.dumps(mismatches[:10],ensure_ascii=False))
            os.replace(tmp,output)
        finally:
            if tmp.exists():tmp.unlink()
    return str(output)

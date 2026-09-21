"""Exercise exported Excel fill semantics without round-tripping the source file."""
from copy import copy, deepcopy
from datetime import datetime
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile
import xml.etree.ElementTree as ET

import openpyxl

from autopm.tracker import build_tracker_plan, export_tracker, fingerprint
from test_tracker import report_fixture, tracker_fixture


NS = '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}'
GREEN = 'FFC6EFCE'


def styled_tracker(path, *, missing=()):
    tracker_fixture(path)
    with ZipFile(path) as archive:
        parts = {name: archive.read(name) for name in archive.namelist()}
    styles = ET.fromstring(parts['xl/styles.xml'])
    formats = ET.Element(NS + 'numFmts', count='2')
    ET.SubElement(formats, NS + 'numFmt', numFmtId='164', formatCode='#,##0.00;[Red]-#,##0.00')
    ET.SubElement(formats, NS + 'numFmt', numFmtId='165', formatCode='yyyy-mm-dd')
    styles.insert(0, formats)
    font = ET.SubElement(styles.find(NS + 'fonts'), NS + 'font')
    for tag, attrs in [('name', {'val': 'Arial'}), ('sz', {'val': '13'}), ('b', {}),
                       ('i', {}), ('color', {'rgb': 'FF203864'})]:
        ET.SubElement(font, NS + tag, attrs)
    fill = ET.SubElement(styles.find(NS + 'fills'), NS + 'fill')
    pattern = ET.SubElement(fill, NS + 'patternFill', patternType='solid')
    ET.SubElement(pattern, NS + 'fgColor', rgb='FFFFC000')
    border = ET.SubElement(styles.find(NS + 'borders'), NS + 'border')
    for edge in ('left', 'right', 'top', 'bottom'):
        side = ET.SubElement(border, NS + edge, style='thin')
        ET.SubElement(side, NS + 'color', rgb='FF123456')
    xfs = styles.find(NS + 'cellXfs')
    rich = ET.Element(NS + 'xf', numFmtId='164', fontId='1', fillId='3', borderId='1',
                      xfId='0', applyFont='1', applyFill='1', applyBorder='1',
                      applyNumberFormat='1', applyAlignment='1', applyProtection='1',
                      quotePrefix='1', pivotButton='0')
    ET.SubElement(rich, NS + 'alignment', horizontal='center', vertical='top', wrapText='1',
                  indent='1', textRotation='10')
    ET.SubElement(rich, NS + 'protection', locked='0', hidden='1')
    xfs.append(rich)
    custom_date = deepcopy(rich)
    custom_date.set('numFmtId', '165')
    xfs.append(custom_date)
    general = deepcopy(rich)
    general.set('numFmtId', '0')
    xfs.append(general)
    for name in ('fonts', 'fills', 'borders', 'cellXfs'):
        element = styles.find(NS + name)
        element.set('count', str(len(element)))
    sheet = ET.fromstring(parts['xl/worksheets/sheet1.xml'])
    for row in sheet.iter(NS + 'row'):
        for cell in list(row):
            address = cell.get('r')
            if address in missing:
                row.remove(cell)
            elif address in {'A2', 'B2', 'E2', 'F2', 'G2', 'H2'}:
                cell.set('s', '3')
            elif address == 'C2':
                cell.set('s', '4')
            elif address == 'D2':
                cell.set('s', '5')
    parts['xl/styles.xml'] = ET.tostring(styles, encoding='utf-8')
    parts['xl/worksheets/sheet1.xml'] = ET.tostring(sheet, encoding='utf-8')
    with ZipFile(path, 'w') as archive:
        for name, content in parts.items():
            archive.writestr(name, content)


def xml_parts(path):
    with ZipFile(path) as archive:
        styles = ET.fromstring(archive.read('xl/styles.xml'))
        sheet = ET.fromstring(archive.read('xl/worksheets/sheet1.xml'))
    cells = {cell.get('r'): cell for cell in sheet.iter(NS + 'c')}
    return styles, cells


class TrackerHighlightTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.folder = Path(temporary.name)
        self.source = self.folder / 'source.xlsx'
        self.output = self.folder / 'updated.xlsx'
        styled_tracker(self.source)
        self.report = report_fixture()

    def workbook(self, path):
        book = openpyxl.load_workbook(path, read_only=False, data_only=False, keep_links=False)
        self.addCleanup(book.close)
        return book['ALL PROJECTS']

    def assert_green(self, cell):
        self.assertEqual(cell.fill.patternType, 'solid')
        self.assertEqual(cell.fill.fgColor.type, 'rgb')
        self.assertEqual(cell.fill.fgColor.rgb, GREEN)

    def test_changed_cells_green_while_unchanged_values_and_affected_formula_keep_styles(self):
        original_hash = fingerprint(self.source)
        original_styles, original_cells = xml_parts(self.source)
        plan = build_tracker_plan(self.source, [self.report])
        self.assertEqual({change['cell'] for change in plan['changes']}, {'B2', 'C2', 'D2'})
        result = export_tracker(plan, self.output)
        self.assertEqual(result['recalculated_caches'], 1)
        self.assertEqual(fingerprint(self.source), original_hash)
        exported_styles, exported_cells = xml_parts(self.output)
        before, after = self.workbook(self.source), self.workbook(self.output)
        for address in ('B2', 'C2', 'D2'):
            with self.subTest(changed=address):
                self.assert_green(after[address])
        for address in ('A2', 'E2', 'F2', 'G2', 'H2'):
            with self.subTest(unchanged=address):
                self.assertEqual(after[address].value, before[address].value)
                self.assertEqual(after[address].style_id, before[address].style_id)
                self.assertEqual(copy(after[address].fill), copy(before[address].fill))
                if address != 'H2':
                    self.assertEqual(ET.tostring(exported_cells[address]), ET.tostring(original_cells[address]))
        self.assertEqual(after['H2'].value, '=SUM(D2-C2)/7')
        self.assertEqual(original_cells['H2'].get('s'), exported_cells['H2'].get('s'))
        self.assertNotEqual(original_cells['H2'].findtext(NS + 'v'), exported_cells['H2'].findtext(NS + 'v'))
        for tag in ('fonts', 'borders', 'numFmts', 'cellStyleXfs', 'cellStyles'):
            self.assertEqual(ET.tostring(exported_styles.find(NS + tag)), ET.tostring(original_styles.find(NS + tag)))
        original_xfs = list(original_styles.find(NS + 'cellXfs'))
        exported_xfs = list(exported_styles.find(NS + 'cellXfs'))
        self.assertEqual([ET.tostring(xf) for xf in exported_xfs[:len(original_xfs)]],
                         [ET.tostring(xf) for xf in original_xfs])

    def test_green_preserves_font_border_alignment_protection_and_existing_number_formats(self):
        export_tracker(build_tracker_plan(self.source, [self.report]), self.output)
        before, after = self.workbook(self.source), self.workbook(self.output)
        for address in ('B2', 'C2', 'D2'):
            with self.subTest(address=address):
                self.assert_green(after[address])
                for attribute in ('font', 'border', 'alignment', 'protection'):
                    self.assertEqual(copy(getattr(after[address], attribute)), copy(getattr(before[address], attribute)))
                self.assertEqual(after[address].quotePrefix, before[address].quotePrefix)
        self.assertEqual(after['B2'].number_format, '#,##0.00;[Red]-#,##0.00')
        self.assertEqual(after['C2'].number_format, 'yyyy-mm-dd')
        self.assertEqual(after['C2'].value, datetime(2026, 9, 10))
        self.assertTrue(after['C2'].is_date)
        self.assertEqual(before['D2'].number_format, 'General')
        self.assertTrue(after['D2'].is_date)
        self.assertEqual(after['D2'].value, datetime(2026, 9, 20))

    def test_missing_blank_cells_are_created_with_green_fill_and_native_dates(self):
        styled_tracker(self.source, missing={'B2', 'C2'})
        _, original_cells = xml_parts(self.source)
        self.assertNotIn('B2', original_cells)
        self.assertNotIn('C2', original_cells)
        plan = build_tracker_plan(self.source, [self.report])
        for address in ('B2', 'C2'):
            self.assertIsNone(next(change['before'] for change in plan['changes'] if change['cell'] == address))
        export_tracker(plan, self.output)
        sheet = self.workbook(self.output)
        self.assertEqual(sheet['B2'].value, 'New name')
        self.assertEqual(sheet['C2'].value, datetime(2026, 9, 10))
        for address in ('B2', 'C2'):
            self.assert_green(sheet[address])
        self.assertTrue(sheet['C2'].is_date)

    def test_cell_then_row_then_column_style_is_preserved_when_adding_highlight(self):
        cases = [
            ('explicit_cell', '3', '4', '5', False, 3),
            ('explicit_zero', '0', '3', '5', False, 0),
            ('row_style', None, '3', '5', False, 3),
            ('column_style', None, None, '3', False, 3),
            ('new_cell_row', None, '3', '5', True, 3),
            ('new_cell_column', None, None, '3', True, 3),
        ]
        for name, cell_style, row_style, column_style, missing, expected_style in cases:
            with self.subTest(case=name):
                styled_tracker(self.source, missing={'B2'} if missing else ())
                with ZipFile(self.source) as archive:
                    parts = {part: archive.read(part) for part in archive.namelist()}
                sheet = ET.fromstring(parts['xl/worksheets/sheet1.xml'])
                rows = {row.get('r'): row for row in sheet.iter(NS + 'row')}
                if row_style is not None:
                    rows['2'].set('s', row_style)
                    rows['2'].set('customFormat', '1')
                column = ET.Element(NS + 'cols')
                ET.SubElement(column, NS + 'col', min='2', max='2', width='24',
                              customWidth='1', style=column_style)
                sheet.insert(1, column)
                if not missing:
                    cell = next(cell for cell in rows['2'] if cell.get('r') == 'B2')
                    if cell_style is None:
                        cell.attrib.pop('s', None)
                    else:
                        cell.set('s', cell_style)
                parts['xl/worksheets/sheet1.xml'] = ET.tostring(sheet, encoding='utf-8')
                with ZipFile(self.source, 'w') as archive:
                    for part, content in parts.items():
                        archive.writestr(part, content)
                report = deepcopy(self.report)
                report['projects'][0]['fields'] = {'project_name': 'New name'}
                report['projects'][0]['tasks'] = []
                output = self.folder / f'{name}.xlsx'
                export_tracker(build_tracker_plan(self.source, [report]), output)
                original_styles, _ = xml_parts(self.source)
                exported_styles, exported_cells = xml_parts(output)
                original_xf = original_styles.find(NS + 'cellXfs')[expected_style]
                exported_xf = exported_styles.find(NS + 'cellXfs')[int(exported_cells['B2'].get('s'))]
                expected_attributes = {key: value for key, value in original_xf.attrib.items()
                                       if key not in {'fillId', 'applyFill'}}
                actual_attributes = {key: value for key, value in exported_xf.attrib.items()
                                     if key not in {'fillId', 'applyFill'}}
                self.assertEqual(actual_attributes, expected_attributes)
                self.assertEqual([ET.tostring(child) for child in exported_xf],
                                 [ET.tostring(child) for child in original_xf])
                self.assert_green(self.workbook(output)['B2'])

    def test_repeated_exports_reuse_fills_and_styles_without_growth(self):
        previous = self.source
        style_counts = []
        style_ids = []
        for iteration in range(3):
            report = deepcopy(self.report)
            project = report['projects'][0]
            project['report_date'] = f'2026-09-{10 + iteration:02}'
            project['fields'].update(project_name=f'Cloud name {iteration}', status=f'Status {iteration}',
                                     kick_off_date=f'2026-09-{10 + iteration:02}',
                                     mp_start_date=f'2026-09-{20 + iteration:02}')
            project['tasks'][0]['date'] = project['fields']['mp_start_date']
            destination = self.folder / f'copy_{iteration}.xlsx'
            export_tracker(build_tracker_plan(previous, [report]), destination)
            styles, cells = xml_parts(destination)
            fills, xfs = styles.find(NS + 'fills'), styles.find(NS + 'cellXfs')
            self.assertEqual(int(fills.get('count')), len(fills))
            self.assertEqual(int(xfs.get('count')), len(xfs))
            style_counts.append((len(fills), len(xfs)))
            style_ids.append(tuple(cells[address].get('s') for address in ('B2', 'C2', 'D2', 'F2')))
            self.assertEqual(cells['B2'].get('s'), cells['F2'].get('s'))
            for address in ('B2', 'C2', 'D2', 'F2'):
                self.assert_green(self.workbook(destination)[address])
            self.assertFalse(build_tracker_plan(destination, [report])['changes'])
            previous = destination
        self.assertEqual(style_counts, [style_counts[0]] * 3)
        self.assertEqual(style_ids, [style_ids[0]] * 3)


if __name__ == '__main__':
    unittest.main()

// Airtable Automation: input variable programRecordId = triggering Program record ID.
// Deploy once only. Sequential retries are safe; concurrent duplicate runs are not atomic.
const PROGRAMS = 'tbl4XSiYGfBDlq5QP';
const MARKETS = 'tblVXMjT7vWeJwthB';
const PROGRAM_LINK = 'fldkjCFcOei2JeqYN';
const MARKET = 'fldjM7TfaYvPteNFf';
const ORDER = 'fldXL2tSqISHFqtKX';
const KEY = 'fldM2nTtnpPvBRIzT';
const REVERSE_LINK = 'fldnYmBmrPrx5cKTM';
const EXPECTED = ['US', 'CA', 'MX', 'UK', 'EU'];
const { programRecordId } = input.config();
if (!/^rec[A-Za-z0-9]{14}$/.test(programRecordId || '')) {
  throw new Error('A valid programRecordId input is required. No records changed.');
}
const programs = base.getTable(PROGRAMS);
const markets = base.getTable(MARKETS);

async function inspect() {
  const program = await programs.selectRecordAsync(programRecordId);
  if (!program) throw new Error('Program not found. No replacement Program will be created.');
  const ids = (program.getCellValue(REVERSE_LINK) || []).map(r => r.id);
  const rows = ids.length ? (await markets.selectRecordsAsync({
    recordIds: ids, fields: [PROGRAM_LINK, MARKET]
  })).records : [];
  const counts = new Map();
  for (const row of rows) {
    const links = row.getCellValue(PROGRAM_LINK) || [];
    const value = row.getCellValue(MARKET);
    if (links.length !== 1 || links[0].id !== programRecordId) {
      throw new Error(`Invalid Program link on ${row.id}; repair before retrying.`);
    }
    if (!EXPECTED.includes(value)) {
      throw new Error(`Unexpected market on ${row.id}; repair before retrying.`);
    }
    counts.set(value, (counts.get(value) || 0) + 1);
  }
  const duplicates = [...counts].filter(([, count]) => count > 1).map(([name]) => name);
  if (duplicates.length) throw new Error(`Duplicate markets: ${duplicates.join(', ')}. No automatic deletion.`);
  return EXPECTED.filter(name => !counts.has(name));
}

const missing = await inspect();
// Write new-row identity and order only; source dates and existing rows stay intact.
if (missing.length) {
  await markets.createRecordsAsync(missing.map(name => ({ fields: {
    [PROGRAM_LINK]: [{ id: programRecordId }], [MARKET]: name,
    [ORDER]: EXPECTED.indexOf(name) + 1, [KEY]: `${programRecordId}|${name}`
  } })));
}
// A failed/unknown write must be reconciled by re-running inspect, never blindly replayed.
const remaining = await inspect();
if (remaining.length) throw new Error(`Readback incomplete: ${remaining.join(', ')}. Retry this Program only.`);
output.set('programRecordId', programRecordId);
output.set('createdCount', missing.length);
output.set('verifiedMarketCount', EXPECTED.length);
output.set('status', 'verified');

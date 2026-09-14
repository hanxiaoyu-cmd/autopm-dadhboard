const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const source = fs.readFileSync(require('node:path').join(__dirname, 'ensure-program-markets.js'), 'utf8');
const pid = 'rec12345678901234';
function fixture(values = [], options = {}) {
  let rows = values.map((market, i) => ({ id: `r${i}`, market, links: [{id:pid}] }));
  let writes = 0;
  let outputs = {};
  const wrap = r => ({id:r.id,getCellValue:f=>f==='fldjM7TfaYvPteNFf'?r.market:r.links});
  const programs = {selectRecordAsync: async () => options.missing ? null : ({getCellValue:()=>rows.map(r=>({id:r.id}))})};
  const markets = {
    selectRecordsAsync:async()=>({records:rows.map(wrap)}),
    createRecordsAsync:async records=>{
      writes++;
      for(const item of records) {
        assert.deepEqual(Object.keys(item.fields).sort(),['fldjM7TfaYvPteNFf','fldkjCFcOei2JeqYN','fldXL2tSqISHFqtKX','fldM2nTtnpPvBRIzT'].sort());
        assert.equal(item.fields.fldXL2tSqISHFqtKX, ['US','CA','MX','UK','EU'].indexOf(item.fields.fldjM7TfaYvPteNFf)+1);
        assert.equal(item.fields.fldM2nTtnpPvBRIzT, `${pid}|${item.fields.fldjM7TfaYvPteNFf}`);
        rows.push({id:`r${rows.length}`,market:item.fields.fldjM7TfaYvPteNFf,links:item.fields.fldkjCFcOei2JeqYN});
        if(options.failOnce) {options.failOnce=false;throw new Error('Simulated partial write');}
      }
    }
  };
  return {rows, get writes(){return writes;}, get outputs(){return outputs;},run:async()=>{
    outputs={};
    await vm.runInNewContext(`(async()=>{${source}\n})()`,{
      base:{getTable:id=>id==='tbl4XSiYGfBDlq5QP'?programs:markets},
      input:{config:()=>({programRecordId:options.badId?'bad':pid})},
      output:{set:(k,v)=>outputs[k]=v}
    });
  }};
}
(async()=>{
  let f=fixture(); await f.run(); assert.equal(f.rows.length,5);assert.equal(f.outputs.verifiedMarketCount,5);
  await f.run();assert.equal(f.writes,1);assert.equal(f.outputs.createdCount,0);
  f=fixture(['US','EU']);await f.run();assert.equal(f.outputs.createdCount,3);
  f=fixture(['US','US']);await assert.rejects(f.run(),/Duplicate/);assert.equal(f.writes,0);
  f=fixture(['UNKNOWN']);await assert.rejects(f.run(),/Unexpected/);assert.equal(f.writes,0);
  f=fixture([], {missing:true});await assert.rejects(f.run(),/not found/);assert.equal(f.writes,0);
  f=fixture([], {badId:true});await assert.rejects(f.run(),/valid/);assert.equal(f.writes,0);
  f=fixture(['US']);f.rows[0].links.push({id:'another'});await assert.rejects(f.run(),/Invalid Program/);assert.equal(f.writes,0);
  f=fixture([], {failOnce:true});await assert.rejects(f.run(),/partial/);assert.equal(f.rows.length,1);
  await f.run();assert.equal(f.rows.length,5);assert.equal(f.outputs.createdCount,4);
  console.log('PASS: empty, sequential retry, partial set, duplicate, unknown market, missing Program, invalid input, multiple links, partial-write recovery. Offline mock only.');
})().catch(e=>{console.error(e);process.exitCode=1;});

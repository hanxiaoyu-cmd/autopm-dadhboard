import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {randomUUID} from 'node:crypto';
import {applyOperation} from './dist/model.js';
import {expandSample} from './tools/scale-sample.mjs';
const root=path.dirname(fileURLToPath(import.meta.url));
const data=path.resolve(process.env.AUTOPM_DATA_DIR||path.join(root,'data'));
fs.mkdirSync(data,{recursive:true});
const stateFile=path.join(data,'state.json');
if(!fs.existsSync(stateFile))fs.copyFileSync(path.join(root,'data/seed.json'),stateFile);
let state=JSON.parse(fs.readFileSync(stateFile,'utf8'));
if(!process.env.AUTOPM_DATA_DIR && state.sampleExpansion!==1){
 const expanded=expandSample(state);
 fs.copyFileSync(stateFile,path.join(data,'state.before-simplification-20260913.json'));
 fs.writeFileSync(stateFile+'.tmp',JSON.stringify(expanded,null,2));
 fs.renameSync(stateFile+'.tmp',stateFile);state=expanded;
}
const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.svg':'image/svg+xml','.json':'application/json; charset=utf-8'};
const send=(res,code,obj)=>{res.writeHead(code,{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store'});res.end(JSON.stringify(obj));};
const server=http.createServer(async(req,res)=>{
 try{
  const url=new URL(req.url,'http://127.0.0.1');
  if(url.pathname==='/api/state'&&req.method==='GET')return send(res,200,state);
  if(url.pathname==='/api/export'&&req.method==='POST'){
   const origin=req.headers.origin;if(origin&&new URL(origin).host!==req.headers.host)return send(res,403,{error:'Local requests only.'});
   let body='';for await(const chunk of req){body+=chunk;if(body.length>1_000_000)return send(res,413,{error:'Export is too large.'});}
   const input=JSON.parse(body);if(typeof input.content!=='string'||typeof input.name!=='string'||! /^[A-Za-z0-9][A-Za-z0-9_. -]{0,120}\.(csv|txt)$/.test(input.name))return send(res,400,{error:'Choose a CSV or text filename.'});
   const dir=path.join(data,'exports');fs.mkdirSync(dir,{recursive:true});const filename=randomUUID()+'-'+input.name.replaceAll(' ','_');fs.writeFileSync(path.join(dir,filename),input.content,'utf8');
   return send(res,200,{url:'/exports/'+encodeURIComponent(filename),name:input.name});
  }
  if(url.pathname.startsWith('/exports/')&&req.method==='GET'){
   const filename=decodeURIComponent(url.pathname.slice('/exports/'.length));if(!/^[a-z0-9][a-z0-9_.-]*\.(csv|txt)$/i.test(filename))return send(res,404,{error:'File not found.'});
   const file=path.join(data,'exports',filename);if(!fs.existsSync(file))return send(res,404,{error:'File not found.'});
   res.writeHead(200,{'Content-Type':filename.endsWith('.csv')?'text/csv; charset=utf-8':'text/plain; charset=utf-8','Content-Disposition':(url.searchParams.has('preview')?'inline':'attachment')+'; filename="'+filename.slice(37)+'"','X-Content-Type-Options':'nosniff'});return fs.createReadStream(file).pipe(res);
  }
  if(url.pathname==='/api/operation'&&req.method==='POST'){
   const origin=req.headers.origin;if(origin&&new URL(origin).host!==req.headers.host)return send(res,403,{error:'Local requests only.'});
   let body='';for await(const chunk of req){body+=chunk;if(body.length>1_000_000)return send(res,413,{error:'Request is too large.'});}
   const input=JSON.parse(body);if(input.revision!==state.revision)return send(res,409,{error:'This workspace was updated elsewhere. Your form is preserved; reload the current data before retrying.'});
   const result=applyOperation(state,input);const tmp=stateFile+'.tmp';fs.writeFileSync(tmp,JSON.stringify(result.state,null,2));fs.copyFileSync(stateFile,stateFile+'.bak');fs.renameSync(tmp,stateFile);state=result.state;return send(res,200,result);
  }
  if(req.method!=='GET')return send(res,405,{error:'Method not allowed.'});
  const relative=decodeURIComponent(url.pathname)==='/'?'index.html':decodeURIComponent(url.pathname).replace(/^\/+/, '');
  const filename=path.resolve(root,'dist',relative);const publicRoot=path.resolve(root,'dist')+path.sep;
  if(!filename.startsWith(publicRoot)||!fs.existsSync(filename)||!fs.statSync(filename).isFile())return send(res,404,{error:'Not found.'});
  res.writeHead(200,{'Content-Type':types[path.extname(filename)]||'application/octet-stream','Cache-Control':'no-cache','X-Content-Type-Options':'nosniff'});fs.createReadStream(filename).pipe(res);
 }catch(error){send(res,400,{error:error.message||'Unable to save.'});}
});
const port=Number(process.env.PORT||4177);server.listen(port,'127.0.0.1',()=>console.log(`AutoPM ready: http://127.0.0.1:${server.address().port}\nLocal data: ${stateFile}`));

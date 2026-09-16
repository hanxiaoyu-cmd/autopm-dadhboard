import {spawn} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../',import.meta.url));
const url='http://127.0.0.1:4177';
async function ready(){try{const r=await fetch(url+'/api/state',{signal:AbortSignal.timeout(1000)});const s=await r.json();return s.sourceNote?.includes('Airtable')&&Array.isArray(s.projects);}catch{return false;}}
if(await ready()){console.log('AutoPM is already running: '+url);process.exit(0);}
const child=spawn(process.execPath,[fileURLToPath(new URL('../server.mjs',import.meta.url))],{cwd:root,detached:true,stdio:'ignore',windowsHide:true});child.unref();
for(let n=0;n<30;n++){if(await ready()){console.log(`AutoPM ready: ${url}\nServer PID: ${child.pid}`);process.exit(0);}await new Promise(r=>setTimeout(r,200));}
console.error('AutoPM did not start. Check that port 4177 is available.');process.exit(1);

const fs=require('fs'),path=require('path'),http=require('http'),crypto=require('crypto');
const {chromium}=require(require.resolve('playwright',{paths:[process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES]}));
const root=path.resolve(__dirname,'../..'),unit=path.join(root,'grade7/unit-2');
const report={viewports:[],audioFiles:0,errors:[]},assert=(x,s)=>{if(!x)report.errors.push(s);};
const server=http.createServer((req,res)=>{
 let file=path.join(root,decodeURIComponent(req.url.split('?')[0]));if(file.endsWith('/'))file+='index.html';
 try{const data=fs.readFileSync(file);res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.mp3':'audio/mpeg','.json':'application/json','.ttf':'font/ttf'})[path.extname(file)]||'application/octet-stream');res.setHeader('Accept-Ranges','bytes');
 const m=(req.headers.range||'').match(/bytes=(\d+)-(\d*)/);if(m){const start=+m[1],end=m[2]?Math.min(+m[2],data.length-1):data.length-1;res.writeHead(206,{'Content-Range':`bytes ${start}-${end}/${data.length}`,'Content-Length':end-start+1});res.end(data.subarray(start,end+1));}else res.end(data);
 }catch{res.statusCode=404;res.end('Not found');}
});
(async()=>{
 const raw=JSON.parse(fs.readFileSync(path.join(__dirname,'sources/vocabulary-records.json'))),records=JSON.parse(fs.readFileSync(path.join(unit,'vocabulary/entries.json'))),manifest=JSON.parse(fs.readFileSync(path.join(unit,'vocabulary/audio/manifest.json')));
 assert(records.length===165,'165 vocabulary records');
 for(let i=0;i<records.length;i++){
  const r=records[i],orig=raw[i],clip=manifest.files[r.id];
  for(const k of ['id','serial','group','number','en','pos','record_sense_en'])assert(r[k]===orig[k],`Identity changed: ${r.id} ${k}`);
  assert(r.record_sense_he===r.mean_he,`Sense metadata mismatch: ${r.id}`);
  assert(clip.text===r.en.replace(/[.!?]+$/,'')+'. '+r.ex_en,`Audio text mismatch: ${r.id}`);
  const bytes=fs.readFileSync(path.join(unit,'vocabulary',clip.src));
  assert(bytes.length===clip.bytes&&crypto.createHash('sha256').update(bytes).digest('hex')===clip.sha256,`Audio hash mismatch: ${r.id}`);report.audioFiles++;
 }
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}/grade7/unit-2/`;
 const browser=await chromium.launch({headless:true,executablePath:process.env.UNIT2_CHROMIUM,args:['--no-sandbox']});
 for(const [width,height] of [[1366,900],[390,844],[360,640]]){
  const ctx=await browser.newContext({viewport:{width,height},isMobile:width<700});const p=await ctx.newPage();p.on('pageerror',e=>report.errors.push(e.message));
  p.on('response',r=>{if(r.status()>=400)report.errors.push(`${r.status()} ${r.url()}`);});
  for(const file of ['','listening.html','vocabulary/practice.html','vocabulary/full.html','workbook-key.html']){
   await p.goto(base+file);await p.evaluate(()=>document.fonts.ready);assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`Overflow ${file} ${width}`);
  }
  await p.goto(base+'vocabulary/practice.html');
  for(let i=0;i<165;i++){
   const q=await p.evaluate(()=>PRACTICE[contextPractice.state.set*15+contextPractice.state.index]);
   assert(q.id===records[i].id,`Context order ${i}`);
   await p.locator(`[data-choice="${q.correct}"]`).click();await p.locator('#check').click();assert((await p.locator('.feedback').innerText()).startsWith('Correct.'),`Correct feedback ${q.id}`);
   assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`Question overflow ${q.id} ${width}`);
   if(i===4){await p.locator('#writing').fill('The nearby school is open.');await p.reload();await p.locator('#next').click({clickCount:1});for(let j=1;j<4;j++)await p.locator('#next').click();assert(await p.locator('#writing').inputValue()==='The nearby school is open.','Writing persistence');}
   await p.locator('#next').click();
  }
  await p.goto(base+'listening.html');assert(!await p.locator('details').evaluate(e=>e.open),'Transcript starts hidden');
  for(const [i,right] of [0,1,2].entries()){
   await p.locator(`input[name="q${i}"][value="${(right+1)%3}"]`).check();await p.locator(`[data-check="${i}"]`).click();assert((await p.locator(`#feedback${i}`).innerText()).startsWith('Check'),'Wrong answer feedback');
   await p.locator(`input[name="q${i}"][value="${right}"]`).check();await p.locator(`[data-check="${i}"]`).click();assert((await p.locator(`#feedback${i}`).innerText()).startsWith('Correct'),'Correct listening feedback');
  }
  await p.locator('#speed').selectOption('0.5');await p.evaluate(()=>document.querySelector('audio').play());await p.waitForFunction(()=>document.querySelector('audio').currentTime>.15);assert(await p.locator('audio').evaluate(a=>a.playbackRate)===.5,'Listening speed');
  await p.goto(base+'reading/?text=boat');assert(await p.locator('#speed').inputValue()==='0.5','Shared speed');
  await p.goto(base+'vocabulary/full.html');await p.waitForFunction(()=>!document.querySelector('#sound').disabled);
  for(const id of ['g03-48','g05-45','g05-54']){
   await p.evaluate(id=>TeachersDeck.show(TeachersDeck.slides.findIndex(s=>s.type==='word'&&s.word.id===id)),id);await p.locator('#replay').click();await p.waitForFunction(()=>TeachersDeck.audio.currentTime>.1);assert(await p.evaluate(()=>TeachersDeck.audio.error===null),`Playback ${id}`);
   await p.locator('#contents').click();assert(await p.evaluate(()=>TeachersDeck.audio.paused),'Menu stops audio');await p.locator('#menu .close').click();
  }
  if(width===390){await p.goto(base+'vocabulary/practice.html?set=8');await p.screenshot({path:'/tmp/unit2-practice-mobile.png',fullPage:true});}
  report.viewports.push({width,height,contextQuestions:165});await ctx.close();
 }
 await browser.close();server.close();fs.writeFileSync(path.join(__dirname,'activities-qa-report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));if(report.errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exit(1);});

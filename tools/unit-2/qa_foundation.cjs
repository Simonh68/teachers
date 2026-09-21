// Draft QA: no claim of final Read Alone or audio acceptance.
const fs=require('fs'),path=require('path'),http=require('http');
const {chromium}=require(require.resolve('playwright',{paths:[process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES||process.cwd()]}));
const root=path.resolve(__dirname,'../..'),report={viewports:[],errors:[],checks:[]};
const assert=(ok,message)=>{if(!ok)report.errors.push(message);};
const server=http.createServer((req,res)=>{let p=path.join(root,decodeURIComponent(req.url.split('?')[0]));if(p.endsWith('/'))p+='index.html';try{const data=fs.readFileSync(p);res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.jpg':'image/jpeg','.ttf':'font/ttf'})[path.extname(p)]||'application/octet-stream');res.end(data);}catch(e){res.statusCode=404;res.end('Not found');}});
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));
 const base=`http://127.0.0.1:${server.address().port}/grade7/unit-2/`;
 const browser=await chromium.launch({headless:true,...(process.env.UNIT2_CHROMIUM?{executablePath:process.env.UNIT2_CHROMIUM}:{}),args:['--no-sandbox']});
 for(const [width,height] of [[1366,900],[390,844],[360,640]]){
  const ctx=await browser.newContext({viewport:{width,height},hasTouch:true,isMobile:width<700});const p=await ctx.newPage();
  p.on('pageerror',e=>report.errors.push(e.message));p.on('response',r=>{if(r.status()>=400)report.errors.push(`${r.status()} ${r.url()}`);});
  let checked=0;
  for(const name of ['grammar-a','grammar-b']){
   await p.goto(base+name+'/');await p.evaluate(()=>document.fonts.ready);const slides=await p.evaluate(()=>LESSON.slides);
   for(let n=0;n<slides.length;n++){
    if(n)await p.keyboard.press('ArrowRight');
    const measure=await p.evaluate(()=>{const s=document.querySelector('#stage'),a=document.querySelector('.hero');return {overflow:document.documentElement.scrollWidth>innerWidth+1||s.scrollWidth>s.clientWidth+1,rect:a?JSON.stringify([a.offsetLeft,a.offsetTop,a.offsetWidth,a.offsetHeight]):null,text:s.innerText};});
    assert(!measure.overflow,`${name} ${width} slide ${n+1}: horizontal overflow`);
    assert(measure.text.trim().length>5,`${name} empty ${n+1}`);
    if(slides[n].kind==='example'&&!slides[n].reveal){const before=measure.rect;await p.keyboard.press('ArrowRight');const after=await p.locator('.hero').evaluate(a=>JSON.stringify([a.offsetLeft,a.offsetTop,a.offsetWidth,a.offsetHeight]));assert(before===after,`${name} ${width} example ${n+1}: geometry changed`);n++;checked++;}
    checked++;
   }
   const qi=slides.findIndex(s=>s.kind==='quiz'&&!s.reveal);await p.goto(base+name+'/#'+(qi+1));await p.waitForFunction(n=>document.querySelector('#counter').textContent.startsWith(n+' /'),qi+1);const c=p.locator('[data-choice]').first();if(await c.count()){await c.click();await p.keyboard.press('ArrowRight');assert((await p.locator('#stage').innerText()).includes('התשובה הנכונה'),`${name}: no answer feedback`);await p.keyboard.press('ArrowRight');assert((await p.locator('#counter').innerText()).startsWith((qi+3)+' /'),`${name}: answer blocks navigation`);}
  }
  await p.goto(base+'vocabulary/full.html');await p.waitForFunction(()=>window.TeachersDeck);await p.evaluate(()=>document.fonts.ready);
  const vocab=await p.evaluate(()=>{const d=TeachersDeck,errors=[];for(let n=0;n<d.slides.length;n++){d.show(n);const s=document.querySelector('#stage');if(s.scrollWidth>s.clientWidth+1)errors.push(n+1);if(d.slides[n].type==='word'&&!d.slides[n].reveal){const rect=()=>[...s.querySelectorAll('[data-original]')].map(a=>[a.offsetLeft,a.offsetTop,a.offsetWidth,a.offsetHeight]);const before=JSON.stringify(rect());d.show(n+1);if(before!==JSON.stringify(rect()))errors.push('pair '+n);}}return {words:d.words.length,slides:d.slides.length,errors};});
  assert(vocab.words===165,`vocab records ${vocab.words}`);assert(!vocab.errors.length,`vocabulary ${width}: ${vocab.errors}`);checked+=vocab.slides;
  for(const file of ['','main-text.html','companion-stories.html','worksheet.html','teacher.html']){await p.goto(base+file);await p.evaluate(()=>document.fonts.ready);assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`${file} ${width}: page overflow`);}
  if(width===390){
   const cdp=await ctx.newCDPSession(p);async function swipe(x,y,dx,dy){await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x,y}]});for(let n=1;n<=6;n++)await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:x+dx*n/6,y:y+dy*n/6}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});}
   for(const [file,id,next,prev] of [['grammar-a/','#stage','#counter',null],['grammar-b/','#stage','#counter',null],['teacher.html','main','#count',null],['vocabulary/full.html','#stage','#counter',null]]){
    await p.goto(base+file);await p.waitForTimeout(100);if(file.includes('vocabulary'))await p.evaluate(()=>TeachersDeck.show(3));
    const before=await p.locator(next).innerText();const box=await p.locator(id).boundingBox();const x=box.x+box.width*.7,y=box.y+Math.min(120,box.height*.5);
    await swipe(x,y,-100,0);assert(await p.locator(next).innerText()!==before,`${file}: left swipe`);await swipe(x-100,y,100,0);assert(await p.locator(next).innerText()===before,`${file}: right swipe`);
    await p.locator(id).evaluate(e=>e.scrollTop=e.scrollHeight);await swipe(x,y,0,-70);assert(await p.locator(next).innerText()!==before,`${file}: up swipe`);await p.locator(id).evaluate(e=>e.scrollTop=0);await swipe(x,y,0,70);assert(await p.locator(next).innerText()===before,`${file}: down swipe`);
   }
   await p.goto(base+'companion-stories.html');await p.evaluate(async()=>{for(const img of document.images){img.loading='eager';await img.decode();}});assert(await p.locator('img').count()===2,'Two source photographs expected');await p.screenshot({path:'/tmp/unit2-stories-mobile.png',fullPage:true});
  }
  report.viewports.push({width,height,slidesChecked:checked});await ctx.close();
 }
 await browser.close();server.close();report.checks=['all grammar slides','all vocabulary slides and reveal geometry','main pages horizontal overflow','four actual CDP touch directions on each deck','quiz feedback and subsequent keyboard navigation'];
 fs.writeFileSync(path.join(__dirname,'qa-report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report));if(report.errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exit(1)});

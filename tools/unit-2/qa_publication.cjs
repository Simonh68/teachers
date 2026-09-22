// Run against a local server by default; set UNIT2_BASE_URL for the published unit.
const fs=require('fs'),path=require('path'),http=require('http'),crypto=require('crypto');
const {chromium}=require(require.resolve('playwright',{paths:[process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES]}));
const root=path.resolve(__dirname,'../..'),unit=path.join(root,'grade7/unit-2');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const report={base:null,assets:0,viewports:[],readingClipsPlayed:0,clipboardLinks:0,errors:[]};
const assert=(ok,message)=>{if(!ok)report.errors.push(message);};
const server=http.createServer((req,res)=>{let file=path.join(root,decodeURIComponent(req.url.split('?')[0]));if(file.endsWith('/'))file+='index.html';try{const b=fs.readFileSync(file);res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.json':'application/json','.mp3':'audio/mpeg','.jpg':'image/jpeg','.ttf':'font/ttf','.pdf':'application/pdf'})[path.extname(file)]||'application/octet-stream');res.setHeader('Accept-Ranges','bytes');const m=(req.headers.range||'').match(/bytes=(\d+)-(\d*)/);if(m){const a=+m[1],z=m[2]?Math.min(+m[2],b.length-1):b.length-1;res.writeHead(206,{'Content-Range':`bytes ${a}-${z}/${b.length}`});res.end(b.subarray(a,z+1));}else res.end(b);}catch{res.statusCode=404;res.end('Not found');}});
(async()=>{
 let base=process.env.UNIT2_BASE_URL;
 if(!base){await new Promise(r=>server.listen(0,'127.0.0.1',r));base=`http://127.0.0.1:${server.address().port}/grade7/unit-2/`;}
 const proxyUrl=process.env.UNIT2_BASE_URL&&(process.env.HTTPS_PROXY||process.env.https_proxy);
 let proxy;
 if(proxyUrl){const u=new URL(proxyUrl);proxy={server:u.protocol+'//'+u.host,...(u.username?{username:decodeURIComponent(u.username),password:decodeURIComponent(u.password)}:{})};}
 report.base=base;const browser=await chromium.launch({headless:true,executablePath:process.env.UNIT2_CHROMIUM,args:['--no-sandbox'],...(proxy?{proxy}:{})});
 const assetContext=await browser.newContext();
 const assets=process.env.UNIT2_SKIP_MEDIA==='1'?[]:fs.readdirSync(unit,{recursive:true}).filter(f=>/\.(mp3|pdf|jpg)$/.test(f));
 for(let i=0;i<assets.length;i+=8){await Promise.all(assets.slice(i,i+8).map(async f=>{const r=await assetContext.request.get(new URL(f,base).href);assert(r.ok(),`Asset HTTP ${r.status()}: ${f}`);assert(sha(await r.body())===sha(fs.readFileSync(path.join(unit,f))),`Asset mismatch: ${f}`);report.assets++;}));}
 await assetContext.close();
 for(const [width,height] of [[1366,900],[390,844],[360,640]]){
  // The runtime proxy's CA is trusted by API requests; Chromium has a separate trust store.
  const ctx=await browser.newContext({viewport:{width,height},isMobile:width<700,hasTouch:true,ignoreHTTPSErrors:!!proxy,permissions:['clipboard-read','clipboard-write']});const p=await ctx.newPage();p.setDefaultNavigationTimeout(60000);const visit=url=>p.goto(url,{waitUntil:'domcontentloaded'});
  p.on('pageerror',e=>report.errors.push(e.message));p.on('response',r=>{if(r.status()>=400&&r.url().startsWith(new URL(base).origin))report.errors.push(`HTTP ${r.status()} ${r.url()}`);});
  await visit(new URL('../',base).href);assert(await p.locator('a.card').first().getAttribute('href')==='unit-2/','Unit 2 is first on Grade 7 page');
  assert(await p.locator('a[href="unit-1/"]').count()===1,'Unit 1 link retained');await p.locator('a.card').first().click();
  assert(await p.locator('a.home').getAttribute('href')==='../','Unit hub returns to Grade 7');
  const links=await p.locator('.card a').evaluateAll(els=>els.map(e=>e.getAttribute('href')));assert(links.length===10,'Ten unit components');
  for(const f of [...links.filter(f=>!f.endsWith('.pdf')),'workbook-key.html']){
   await visit(new URL(f,base).href);await p.evaluate(()=>document.fonts.ready);
   assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`Overflow: ${f} at ${width}`);
   assert(!/Teacher review edition|טיוטה לעיון/.test(await p.locator('body').innerText()),`Draft label: ${f}`);
  }
  for(const f of ['grammar-a/','grammar-b/']){await visit(new URL(f,base).href);const before=await p.locator('#counter').innerText();await p.keyboard.press('ArrowRight');assert(await p.locator('#counter').innerText()!==before,`Grammar navigation ${f}`);}
  await visit(new URL('companion-stories.html',base).href);await p.evaluate(async()=>{for(const im of document.images){im.loading='eager';await im.decode();}});
  await visit(new URL('reading/?text=snow-day',base).href);
  for(let t=0;t<(width===390?6:1);t++){
   await p.evaluate(t=>{unitReader.chooseText(t);unitReader.setMode('parts');},t);await p.locator('#play').click();
   await p.waitForFunction(()=>{const a=document.querySelector('#audio');return !a.paused&&a.currentTime>unitReader.clip.start+.1;});report.readingClipsPlayed++;
   await p.locator('#menuButton').click();assert(await p.locator('#audio').evaluate(a=>a.paused),'Reading menu pauses audio');await p.locator('#closeMenu').click();
  }
  await visit(new URL('vocabulary/full.html',base).href);await p.waitForFunction(()=>!document.querySelector('#sound').disabled);
  await p.evaluate(()=>TeachersDeck.show(TeachersDeck.slides.findIndex(s=>s.type==='word')));await p.locator('#replay').click();await p.waitForFunction(()=>TeachersDeck.audio.currentTime>.1);
  await p.evaluate(()=>TeachersDeck.show(TeachersDeck.slides.length-1));
  if(width===1366){for(let g=3;g<=5;g++){const url=`https://englishfornoar.co.il/band-ii/groups/group-0${g}.html`;await p.locator(`[data-copy="${url}"]`).click();assert(await p.evaluate(()=>navigator.clipboard.readText())===url,`Clipboard group ${g}`);report.clipboardLinks++;}}
  await visit(base);await p.screenshot({path:`/tmp/unit2-release-${process.env.UNIT2_BASE_URL?'public':'local'}-${width}.png`,fullPage:true});
  report.viewports.push({width,height,components:links.length});await ctx.close();
 }
 await browser.close();server.close();const dest=process.env.UNIT2_REPORT||path.join(__dirname,'release-qa-report.json');fs.writeFileSync(dest,JSON.stringify(report,null,2));console.log(JSON.stringify(report));if(report.errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exit(1);});

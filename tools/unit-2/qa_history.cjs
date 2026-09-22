const fs=require('fs'),path=require('path'),http=require('http'),os=require('os');
const {chromium}=require(require.resolve('playwright',{paths:[process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES]}));
const root=path.resolve(__dirname,'../..'),key='teachers-unit2-meetings-v1';
const assert=(ok,message)=>{if(!ok)throw Error(message);};
const report={viewports:[],checks:[],errors:[]};
const launch={executablePath:process.env.UNIT2_CHROMIUM,headless:true,args:['--no-sandbox']};
const server=http.createServer((req,res)=>{
 let file=path.join(root,decodeURIComponent(req.url.split('?')[0]));if(file.endsWith('/'))file+='index.html';
 try{res.setHeader('Content-Type',({'.html':'text/html','.js':'text/javascript','.css':'text/css','.ttf':'font/ttf'})[path.extname(file)]||'application/octet-stream');res.end(fs.readFileSync(file));}catch{res.statusCode=404;res.end();}
});
const saved=p=>p.evaluate(key=>JSON.parse(localStorage.getItem(key)),key);
async function visit(p,base,id,target){await p.locator(`[data-open-id="${id}"]`).click();await p.waitForURL(base+target);await p.goBack();}
(async()=>{
 await new Promise(r=>server.listen(0,'127.0.0.1',r));const base=`http://127.0.0.1:${server.address().port}/grade7/unit-2/`,browser=await chromium.launch(launch);
 for(const [width,height] of [[1366,900],[390,844],[360,640]]){
  const context=await browser.newContext({viewport:{width,height},isMobile:width<700,hasTouch:true}),p=await context.newPage();p.on('pageerror',e=>report.errors.push(e.message));
  await p.goto(base+'#m3');assert(await p.locator('#reset-history').isDisabled()&&await p.locator('#restore-history').isDisabled(),'Fresh history controls disabled');
  // Existing users have version-1 state without a backup field.
  await p.evaluate(key=>localStorage.setItem(key,JSON.stringify({version:1,opened:{'m3-message':true},completed:{'m3-message':true},ready:{m3:true},lastOpened:'m3-message',expanded:'m3'})),key);await p.reload();
  assert(await p.locator('[data-complete="m3-message"]').isChecked(),'Existing completion preserved on upgrade');
  await visit(p,base,'m3-message','journey-horse.html');await p.evaluate(()=>document.fonts.ready);
  const requests=[],capture=r=>requests.push(r.url());p.on('request',capture);
  await p.locator('#reset-history').click();await p.waitForTimeout(100);p.off('request',capture);assert(!requests.length,'Reset makes no network requests');
  assert(await p.locator('[data-open-status="m3-message"]').isHidden(),'Reset removes Opened badge');assert(await p.locator('[data-open-id="m3-message"]').evaluate(e=>getComputedStyle(e).color)==='rgb(108, 231, 255)','Reset returns tracked link to unvisited colour');
  assert(await p.locator('#last-opened').innerText()==='No activity opened yet.','Reset clears Last opened');assert(await p.locator('[data-complete="m3-message"]').isChecked(),'Reset preserves completion');assert((await saved(p)).ready.m3,'Reset preserves readiness');
  await p.reload();assert(await p.locator('#reset-history').isDisabled()&&await p.locator('#restore-history').isEnabled(),'Reset and backup survive reload');
  await p.locator('#restore-history').focus();await p.keyboard.press('Enter');assert(await p.locator('[data-open-status="m3-message"]').innerText()==='Last opened','Keyboard restore recovers last opened');assert(await p.locator('#restore-history').isDisabled(),'Restore consumes backup');
  await p.locator('#reset-history').click();
  // Preparation shares the same key: visiting it must not discard the backup.
  await p.locator('[data-open-id="unit-prep"]').click();await p.waitForURL(base+'student-preparation.html');await p.locator('[data-ready="m3"]').uncheck();await p.goto(base+'#m3');
  await visit(p,base,'m3-guide','meeting-guide.html#7');
  await p.locator('#reset-history').click();await p.reload();
  assert((await saved(p)).historyBackup.opened['m3-message'],'A second reset keeps earlier cleared history');
  await visit(p,base,'m3-message','journey-horse.html');
  p.on('request',capture);await p.locator('#restore-history').click();await p.waitForTimeout(100);p.off('request',capture);assert(!requests.length,'Restore makes no network requests');
  const restored=await saved(p);assert(restored.opened['m3-guide']&&restored.opened['m3-message']&&restored.opened['unit-prep'],'Restore merges old and new visits');assert(restored.lastOpened==='m3-message','Newer last-opened link retained');assert(restored.completed['m3-message']&&!restored.ready.m3,'Restore keeps completion and latest readiness');
  await p.reload();assert(await p.locator('[data-open-status="m3-guide"]').isVisible(),'Restored history survives reload');
  // Another open tab follows the reset and restore through native storage events.
  const second=await context.newPage();await second.goto(base+'#m3');await p.locator('#reset-history').click();await second.locator('#restore-history').waitFor({state:'visible'});await second.waitForFunction(()=>!document.querySelector('#restore-history').disabled);assert(await second.locator('[data-open-status="m3-message"]').isHidden(),'Other tab sees reset');await second.locator('#restore-history').click();await p.waitForFunction(()=>document.querySelector('[data-open-id="m3-message"]').classList.contains('was-opened'));await second.close();
  await p.evaluate(()=>document.fonts.ready);assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'No horizontal overflow');
  for(const id of ['reset-history','restore-history']){const box=await p.locator('#'+id).boundingBox();assert(box.width>=44&&box.height>=44&&box.x>=0&&box.x+box.width<=width,'Accessible control size and viewport fit');}
  await p.evaluate(()=>scrollTo(0,0));await p.screenshot({path:`/tmp/unit2-history-${width}.png`,fullPage:false});report.viewports.push({width,height,resetRestore:true,networkRequests:requests.length});await context.close();
 }
 const blocked=await browser.newContext();await blocked.addInitScript(key=>{localStorage.setItem(key,JSON.stringify({version:1,opened:{'m1-vocab':true},completed:{'m1-vocab':true},ready:{}}));Storage.prototype.setItem=()=>{throw new DOMException('Blocked','QuotaExceededError');};},key);const bp=await blocked.newPage();await bp.goto(base);await bp.locator('#reset-history').click();await bp.locator('#restore-history').click();assert(await bp.locator('[data-open-status="m1-vocab"]').isVisible(),'Blocked storage: reversible in-memory history');assert(await bp.locator('[data-complete="m1-vocab"]').isChecked(),'Blocked storage: completion preserved');assert((await bp.locator('#save-status').innerText()).includes('Saving is unavailable'),'Blocked storage reported honestly');await blocked.close();
 const clean=await browser.newContext(),cp=await clean.newPage();await cp.goto(base);assert(await cp.locator('#restore-history').isDisabled(),'Backup remains private to browser context');await clean.close();await browser.close();
 const profile=fs.mkdtempSync(path.join(os.tmpdir(),'unit2-history-profile-'));let persistent=await chromium.launchPersistentContext(profile,launch),pp=await persistent.newPage();await pp.goto(base+'#m3');await visit(pp,base,'m3-message','journey-horse.html');await pp.locator('#reset-history').click();await persistent.close();persistent=await chromium.launchPersistentContext(profile,launch);pp=await persistent.newPage();await pp.goto(base+'#m3');await pp.locator('#restore-history').click();assert(await pp.locator('[data-open-status="m3-message"]').isVisible(),'Restore works after browser restart');await persistent.close();fs.rmSync(profile,{recursive:true,force:true});
 report.checks=['legacy state retained','reset and restore, including native-history colour override','completion/readiness independent','merge visits across repeated resets','reload and browser-restart recovery','cross-page and cross-tab persistence','keyboard operation and mobile layout','no reset/restore network requests','blocked-storage fallback','separate-browser isolation'];
 server.close();fs.writeFileSync(path.join(__dirname,'history-qa-report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));if(report.errors.length)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exit(1);});

const { chromium } = require('playwright');
const path=require('path');
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 for(const slug of ['part1-he','part1-en','part2-he','part2-en']){
  const page=await browser.newPage({viewport:{width:1100,height:1500},deviceScaleFactor:1});
  await page.goto('file://'+path.join(__dirname,'worksheet-'+slug+'.html'));
  const fit=await page.locator('.page').evaluateAll(els=>els.map(el=>({height:el.clientHeight,content:el.scrollHeight})));if(fit.length!==2||fit.some(x=>x.content>x.height+2))throw Error('A4 overflow: '+slug+' '+JSON.stringify(fit));
  await page.pdf({path:path.join(__dirname,'worksheet-'+slug+'.pdf'),format:'A4',printBackground:true,preferCSSPageSize:true,margin:{top:'0',right:'0',bottom:'0',left:'0'}});
  await page.close();
 }
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});

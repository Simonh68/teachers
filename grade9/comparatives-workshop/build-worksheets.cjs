const { chromium } = require('playwright');
const path=require('path');
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 for(const slug of ['part1','part2']){
  const page=await browser.newPage({viewport:{width:1100,height:1500},deviceScaleFactor:1});
  await page.goto('file://'+path.join(__dirname,'worksheet-'+slug+'.html'));
  await page.pdf({path:path.join(__dirname,'worksheet-'+slug+'.pdf'),format:'A4',printBackground:true,preferCSSPageSize:true,margin:{top:'0',right:'0',bottom:'0',left:'0'}});
  await page.close();
 }
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});

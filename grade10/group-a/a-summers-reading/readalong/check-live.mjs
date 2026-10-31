import {chromium} from 'playwright';
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const report=[];
for(const part of [1,2,3]){
 const page=await browser.newPage({viewport:{width:1400,height:860},acceptDownloads:false});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 page.on('console',msg=>{if(msg.type()==='error')errors.push(msg.text());});
 const url='https://simonh68.github.io/teachers/grade10/group-a/a-summers-reading/readalong/?part='+part;
 await page.goto(url,{waitUntil:'domcontentloaded',timeout:40000});
 await page.waitForSelector('.card .title',{timeout:17000});
 let title=await page.locator('.card .title').first().innerText();
 if(!title.includes('A Summer'))throw Error('Unexpected intro Part '+part+': '+title);
 const initial=await page.locator('#count').innerText();
 await page.locator('#next').click();
 await page.waitForTimeout(300);
 const newCount=await page.locator('#count').innerText();
 if(initial===newCount)throw Error('Next slide did not move on '+part);
 let images=await page.locator('.visual img').count();
 let next=0;
 for(let i=0;i<90;i++){
  const btn=page.locator('#next');
  const txt=await btn.innerText();
  if(txt.includes('להתחיל להאזין')){next=i;await btn.click();break;}
  await btn.click();
 }
 await page.waitForSelector('.listening #currentText',{timeout:17000});
 const audio=await page.locator('#voice').evaluate(a=>({src:a.src,duration:a.duration,readyState:a.readyState,currentTime:a.currentTime,paused:a.paused}));
 if(!audio.src.includes('part'+part+'.ogg'))throw Error('Wrong audio '+JSON.stringify(audio));
 await page.waitForFunction(()=>document.querySelector('#voice').readyState>=2,{timeout:17000});
 const word=await page.evaluate(()=>!!(window.SUMMER_DATA&&window.SUMMER_DATA.lesson1)); 
 if(!word)throw Error('Vocabulary data absent');
 const timed=await page.evaluate(async p=>{let r=await fetch('../audio/part'+p+'-timed.json');return {ok:r.ok,status:r.status}},part);
 if(!timed.ok)throw Error('Timed transcript not found for part '+part);
 const firstStop=part===1?126.9:part===2?152.7:212.3;
 await page.locator('#voice').evaluate((a,t)=>{a.currentTime=t+.25; a.dispatchEvent(new Event('timeupdate'));},firstStop);
 await page.waitForSelector('#checkpoint:not([hidden]) .quiz',{timeout:14000});
 const questions=await page.locator('#checkpoint .choice').count();
 if(questions<3)throw Error('Checkpoint missing answer choices');
 await page.locator('#checkpoint .choice[data-choice="0"]').click();
 if(await page.locator('#continueQuiz').isDisabled())throw Error('Correct answer did not unlock continue');
 report.push({part,title,slides_to_audio:next+1,images,audio,timed,questions,pageErrors:errors.filter(x=>!x.includes('fonts.googleapis'))});
 await page.close();
}
await browser.close();
for(const r of report) console.log('READALONG_QA',JSON.stringify(r));
if(report.some(r=>r.pageErrors.some(x=>/TypeError|ReferenceError|SyntaxError/.test(x))))process.exit(1);

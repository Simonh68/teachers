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
 let next=0;const checkedPhotos={};const targets={1:['railroad flat','delivery boy','magazine','iron railing','porch','stock clerk'],2:['change booth','shoemaker','stoop','nickel'],3:['softback books','radio','library']}[part];
 for(let i=0;i<90;i++){
  const word=await page.locator('.card .title').first().innerText();
  if(targets.includes(word.toLowerCase())){
    const img=await page.locator('.card .visual img').first().evaluate(async(el)=>{try{await el.decode()}catch(e){}return {src:el.currentSrc||el.src,width:el.naturalWidth,complete:el.complete}});
    if(!img.width)throw Error('Photo not loaded on '+part+' word '+word+': '+JSON.stringify(img));
    checkedPhotos[word.toLowerCase()]=img.src;
  }
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
 await page.locator('#continueQuiz').click();
 await page.waitForSelector('#checkpoint:not([hidden]) .quiz',{timeout:7000});
 await page.locator('#checkpoint .choice[data-choice="0"]').click();
 await page.locator('#continueQuiz').click();
 await page.waitForTimeout(350);
 if(!(await page.locator('#checkpoint').isHidden()))throw Error('Quiz 1 did not resume narration');
 const secondStop=part===1?246.2:part===2?317.8:443.3;
 await page.locator('#voice').evaluate((a,t)=>{a.currentTime=t+.3;a.dispatchEvent(new Event('timeupdate'));},secondStop);
 await page.waitForSelector('#checkpoint:not([hidden]) .quiz',{timeout:9000});
 await page.locator('#checkpoint .choice[data-choice="0"]').click();
 await page.locator('#continueQuiz').click();
 await page.locator('#checkpoint .choice[data-choice="0"]').click();
 await page.locator('#continueQuiz').click();
 await page.waitForTimeout(350);
 if(!(await page.locator('#checkpoint').isHidden()))throw Error('Quiz 2 did not resume narration');
 const missing=targets.filter(w=>!checkedPhotos[w]);
 if(missing.length)throw Error('Vocabulary photo QA missed terms for Part '+part+': '+missing.join(', '));
 const diffPhotos=Object.values(checkedPhotos);if(new Set(diffPhotos).size<diffPhotos.length-1)throw Error('Vocabulary nouns are reusing images: '+JSON.stringify(checkedPhotos));
 report.push({part,title,slides_to_audio:next+1,photosVerified:checkedPhotos,audio,timed,questions,pageErrors:errors.filter(x=>!x.includes('fonts.googleapis'))});
 await page.close();
}
await browser.close();
for(const r of report) console.log('READALONG_QA',JSON.stringify(r));
if(report.some(r=>r.pageErrors.some(x=>/TypeError|ReferenceError|SyntaxError/.test(x))))process.exit(1);

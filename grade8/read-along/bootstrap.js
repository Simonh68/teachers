/* Grade 8 only. Keep the existing unit application for every non-reading view. */
(()=>{'use strict';
const script=document.currentScript,base=new URL('./',script.src),query=new URLSearchParams(location.search);
const view=query.get('view')||'home',legacy=document.getElementById('unit-legacy-app');
const load=(path)=>new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=new URL(path,base).href;s.onload=resolve;s.onerror=()=>reject(Error('Cannot load '+path));document.head.append(s);});
if(!['chunks','sentences'].includes(view)){
 if(!legacy)return;
 const s=document.createElement('script');s.textContent=legacy.textContent;legacy.after(s);
 (async()=>{for(const item of document.querySelectorAll('script[data-legacy-src]'))await new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=item.dataset.legacySrc;s.onload=resolve;s.onerror=reject;item.after(s);});})().catch(console.error);
 return;
}
(async()=>{
 const D=window.UNIT_DATA;if(!D?.story?.length)throw Error('Missing unit reading data');
 const pilot=location.pathname.includes('/unit-1-reading-pilot/');
 document.querySelectorAll('style,link[rel="stylesheet"]').forEach(s=>s.remove());
 const css=document.createElement('link');css.rel='stylesheet';css.href=new URL('reader.css?v=20261005-bilingual1',base).href;const cssReady=new Promise((resolve,reject)=>{css.onload=resolve;css.onerror=()=>reject(Error('Cannot load reader styling'));});document.head.append(css);
 document.body.className='grade8-bilingual';document.body.dataset.readingStandard='grade8-bilingual-v1';
 document.title='Read Along · The Monkey Festival · ח׳2';
 document.body.innerHTML=`<header class="toolbar"><a class="home" href="../" aria-label="חזרה לכיתה ח׳">⌂</a><div class="brand">כיתה ח׳</div><button id="contents" aria-haspopup="dialog">תוכן</button><div class="audio-controls"><button id="play" disabled aria-pressed="false">טוען שמע…</button><button id="replay" disabled aria-label="הקראה מחדש" title="הקראה מחדש">↺</button><label for="speed">מהירות</label><select id="speed" dir="ltr" aria-label="מהירות ההקראה"><option value="0.25">0.25×</option><option value="0.5">0.5×</option><option value="0.75" selected>0.75×</option><option value="1">1×</option><option value="1.25">1.25×</option></select></div></header>
<main id="stage" aria-label="קריאה באנגלית ובעברית"><article class="sheet" id="sheet" role="tabpanel"><div class="meta"><nav id="reading-tabs" class="tabstrip" role="tablist" aria-label="חלקי הסיפור"></nav><span id="step-label" class="step-label"></span></div><div class="text-slot english-slot"><p id="english" class="reading en" lang="en" dir="ltr"></p></div><div class="text-slot hebrew-slot" id="translation-slot" aria-hidden="true"><p id="hebrew" class="reading he" lang="he" dir="rtl"></p></div><p id="hint"></p></article></main>
<footer class="footer" id="footer"><nav class="navigation" aria-label="מעבר שקופיות"><button data-step="-1" aria-label="לשקופית הקודמת">←</button><button data-step="-1" aria-label="לשקופית הקודמת">↑</button><output id="counter" aria-live="polite"></output><button data-step="1" aria-label="לשקופית הבאה">↓</button><button data-step="1" aria-label="לשקופית הבאה">→</button></nav><p id="status" role="status">ההפסקות בשמע בלבד — 1.5 שניות.</p></footer><div class="progress"><div id="progress"></div></div>
<dialog id="reading-menu"><div class="menu-heading"><h2>קריאה · The Monkey Festival</h2><button id="close-menu" aria-label="סגירת התוכן">×</button></div><nav class="menu-modes"><a href="?view=chunks" data-mode="chunks">קריאה בקטעים</a><a href="?view=sentences" data-mode="sentences">משפט בשקף</a><a href="./">מפגשי היחידה</a></nav><div class="jump-row"><button id="start-over">מההתחלה</button><button id="resume-reading">המשך הקריאה</button></div><p class="menu-note">אנגלית תחילה; בשקופית הבאה התרגום נשאר גלוי והמרקר עוקב בשתי השפות. ההקראה באנגלית בלבד.</p><div id="sentence-list"></div></dialog><div id="reading-tip" role="tooltip" hidden></div>`;
 if(pilot){const home=document.querySelector('.home');home.href='./';home.setAttribute('aria-label','חזרה לעותק היחידה');}
 for(const path of ['phrase-data.js?v=20261005-bilingual1','alignment.js?v=20261005-bilingual1','phrase-player.js?v=20261005-bilingual1','reader.js?v=20261005-bilingual1'])await load(path);
 await cssReady;
 await window.initGrade8Bilingual({D,base,view,store:pilot?'teachers-grade8-unit1-reading-pilot-v1':'teachers-grade8-unit1-v1',speedStore:pilot?'teachers-read-alone-pilot-speed-v1':'teachers-read-alone-speed-v1'});
})().catch(e=>{console.error(e);document.body.innerHTML='<main style="padding:25px;font:20px Arial,sans-serif;direction:rtl"><h1>לא ניתן לטעון את הקריאה כרגע.</h1><p>רעננו את העמוד כשהחיבור זמין.</p><a href="./">חזרה למפגשי היחידה</a></main>';});
})();

'use strict';
const D=window.C_SET,$=id=>document.getElementById(id),esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const correct=q=>q.correct_options||[q.correct_option],norm=s=>s.toLowerCase().replace(/[’]/g,"'").replace(/[^a-z0-9 ]/g,' ').replace(/\s+/g,' ').trim();
const answers=D.questions.map(q=>q.options?[]:Array(q.required_answers).fill('')),checked=new Set(),orders=D.questions.map(q=>Object.keys(q.options||{}));
orders.forEach(a=>{for(let i=a.length-1;i>0;i--){let j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}});
let page=0,serial=0,timer=null,active=null,playback=null;
function updatePlaybackButtons(){
 for(const [id,label] of [['paragraphPlay','הפסקה'],['questionPlay','השאלה']]){
  const b=$(id),selected=playback?.button===id;
  b.textContent=selected?(playback.paused?'▶ המשך '+label:'❚❚ השהיה'):'▶ השמעת '+label;
  b.setAttribute('aria-pressed',String(!!selected&&!playback.paused));
 }
}
function stop(){serial++;clearTimeout(timer);timer=null;playback=null;if('speechSynthesis'in window){window.speechSynthesis.cancel();window.speechSynthesis.resume();}document.querySelectorAll('.active').forEach(e=>e.classList.remove('active'));active=null;updatePlaybackButtons();}
function tokenize(text){return text.replace(/\S+/g,m=>`<span class="word">${esc(m)}</span>`);}
function togglePlayback(element,button){
 if(playback?.element!==element){speak(element,button);return;}
 const p=playback;
 if(p.paused){p.paused=false;updatePlaybackButtons();if(p.phase==='gap')p.armGap(p.gapRemaining);else{speechSynthesis.resume();$('status').textContent='ממשיך מאותה נקודה…';}}
 else{p.paused=true;if(p.phase==='gap'){p.gapRemaining=Math.max(0,p.gapDeadline-Date.now());clearTimeout(timer);timer=null;}else speechSynthesis.pause();updatePlaybackButtons();$('status').textContent='הקריאה מושהית — לחצו על המשך.';}
}
function speak(element,button){stop();if(!('speechSynthesis'in window)){$('status').textContent='הדפדפן הזה אינו תומך בהקראה.';return;}
 const id=serial,words=[...element.querySelectorAll('.word')],segments=[];let part=[];
 words.forEach((w,i)=>{part.push(w);if(/[.,;:!?]$/.test(w.textContent)||i===words.length-1){segments.push(part);part=[];}});
 const p=playback={element,button,paused:false,phase:'speech',gapRemaining:0,gapDeadline:0,next:null,armGap:null};updatePlaybackButtons();
 const voices=speechSynthesis.getVoices(),voice=voices.find(v=>v.lang==='en-US')||voices.find(v=>v.lang.startsWith('en'));
 function mark(w){element.querySelectorAll('.word').forEach(x=>x.classList.remove('active'));active=w;w?.classList.add('active');}
 function finish(message){mark(null);playback=null;updatePlaybackButtons();$('status').textContent=message;}
 p.armGap=ms=>{if(id!==serial||p.paused)return;p.phase='gap';p.gapRemaining=ms;p.gapDeadline=Date.now()+ms;$('status').textContent='הפסקה בין מקטעים…';timer=setTimeout(()=>{timer=null;if(id===serial&&!p.paused)run(p.next);},ms);};
 function run(n){if(id!==serial)return;if(n===segments.length){finish('הקריאה הסתיימה.');return;}if(p.paused)return;p.phase='speech';
 const ws=segments[n],text=ws.map(w=>w.textContent).join(' '),u=new SpeechSynthesisUtterance(text);u.lang='en-US';if(voice)u.voice=voice;u.rate=Number($('speed').value);let boundaries=[],pos=0;ws.forEach(w=>{boundaries.push(pos);pos+=w.textContent.length+1;});
 u.onstart=()=>{if(id!==serial)return;ws.forEach(w=>w.classList.add('active'));if(p.paused){speechSynthesis.pause();return;}$('status').textContent='קורא מקטע '+(n+1)+' מתוך '+segments.length;};
 u.onboundary=e=>{if(id!==serial||p.paused||e.name==='sentence')return;let j=0;boundaries.forEach((pos,i)=>{if(pos<=e.charIndex)j=i;});mark(ws[j]);};
 u.onend=()=>{if(id!==serial)return;mark(null);if(n+1===segments.length){finish('הקריאה הסתיימה.');return;}p.next=n+1;p.phase='gap';p.gapRemaining=Number($('gap').value);if(!p.paused)p.armGap(p.gapRemaining);};
 u.onerror=()=>{if(id!==serial)return;finish('הקריאה נעצרה. אפשר ללחוץ שוב על השמעה.');};speechSynthesis.speak(u);}
 run(0);
}
function matchOpen(q,a){const keys=q.answer_key.map(norm),vals=a.map(norm);if(q.required_answers===1)return vals[0]&&(q.acceptable_answer_variants||q.answer_key).map(norm).includes(vals[0]);return vals.every(Boolean)&&keys.every(k=>vals.includes(k));}
function result(i){const q=D.questions[i],a=answers[i];if(q.options){let count=a.filter(k=>correct(q).includes(k)).length;return{ok:a.length===correct(q).length&&count===a.length,units:count,points:count*(q.points/q.scoring_units),complete:a.length===q.required_answers};}return{ok:matchOpen(q,a),units:matchOpen(q,a)?q.scoring_units:0,points:matchOpen(q,a)?q.points:0,pending:!matchOpen(q,a)};}
function keyHTML(q){return q.options?correct(q).map(k=>`<p class="en">${esc(q.options[k])}</p>`).join(''):q.answer_key.map(k=>`<p class="en">${esc(k)}</p>`).join('');}
function paintFeedback(){const q=D.questions[page],r=result(page);$('feedback').innerHTML='';$('whyToggle').hidden=true;$('why').hidden=true;
 if(!checked.has(page))return;
 if(r.ok){$('feedback').innerHTML='<span class="success">✓ נכון, מעולה! 100%</span>';}
 else if(q.options){$('feedback').innerHTML=`<span class="neutral">${q.required_answers===2?r.units+' מתוך 2 הבחירות נכונות':'✗ הבחירה אינה נכונה'}</span>`;$('whyToggle').hidden=!answers[page].some(k=>!correct(q).includes(k));}
 else{$('feedback').innerHTML='<span class="neutral">אפשר להשוות לתשובה במחוון, או לבדוק את הניסוח בסוף המבחן.</span>';}
 if(q.options)document.querySelectorAll('[data-option]').forEach(b=>{const k=b.dataset.option,selected=answers[page].includes(k);b.classList.toggle('good',selected&&correct(q).includes(k));b.classList.toggle('bad',selected&&!correct(q).includes(k));const mark=b.querySelector('.mark');mark.textContent=selected?(correct(q).includes(k)?'✓':'✗'):'○';});
}
function show(n){stop();page=Math.max(0,Math.min(7,n));$('pdfDownload').hidden=page!==0;$('slide').hidden=page===7;$('summary').hidden=page!==7;$('counter').textContent=page===7?'סיכום':'שאלה '+(page+1)+' מתוך 7';$('progress').value=page+1;$('prev').disabled=page===0;$('next').hidden=page>=6;$('finish').hidden=page!==6;$('next').textContent='השאלה הבאה ('+(page+2)+' מתוך 7) ←';if(page===7){renderSummary();return;}
 const q=D.questions[page],ps=q.scope==='whole_text'?D.paragraphs:D.paragraphs.filter(p=>p.id===q.paragraph_id);$('scope').textContent=q.scope==='whole_text'?'כל הטקסט':'פסקה '+['I','II','III','IV'][ps[0].number-1];$('paragraph').innerHTML=ps.map(p=>'<p>'+tokenize(p.text)+'</p>').join('');$('paragraph').classList.remove('concealed');$('textToggle').setAttribute('aria-pressed','true');$('question').innerHTML=tokenize(q.stem);$('instruction').textContent=q.required_answers===2?'יש לתת שתי תשובות.':q.options?'בחרו תשובה אחת.':'כתבו תשובה באנגלית.';
 $('response').innerHTML=q.options?'<div class="choices en">'+orders[page].map(k=>`<button class="choice" data-option="${k}" aria-pressed="${answers[page].includes(k)}"><span class="mark">${answers[page].includes(k)?'●':'○'}</span><span>${esc(q.options[k])}</span></button>`).join('')+'</div>':answers[page].map((v,i)=>`<textarea data-answer="${i}" aria-label="תשובה ${i+1}" placeholder="Your answer ${q.required_answers>1?i+1:''}">${esc(v)}</textarea>`).join('');
 document.querySelectorAll('[data-option]').forEach(b=>b.onclick=()=>{const k=b.dataset.option,a=answers[page];if(q.required_answers===1)answers[page]=[k];else if(a.includes(k))answers[page]=a.filter(x=>x!==k);else if(a.length<q.required_answers)a.push(k);else{$('feedback').textContent='בחרתם שתי תשובות; בטלו אחת כדי לשנות.';return;}checked.delete(page);show(page);});
 document.querySelectorAll('[data-answer]').forEach(t=>t.oninput=()=>{answers[page][Number(t.dataset.answer)]=t.value;checked.delete(page);paintFeedback();});$('key').innerHTML=keyHTML(q);$('key').hidden=true;paintFeedback();$('status').textContent='';}
function renderSummary(keys=false){const units=D.questions.reduce((s,q)=>s+q.points,0),earned=D.questions.reduce((s,q,i)=>s+(checked.has(i)?result(i).points:0),0),pending=D.questions.filter((q,i)=>!q.options&&!result(i).ok).length;
 $('score').textContent=`נקודות שאושרו בהבנת הנקרא: ${earned} מתוך ${units}. `+(pending?`${pending} שאלות פתוחות ממתינות לבדיקה; הציון הכולל ייקבע לאחר בדיקתן.`:`ציון תרגול: ${Math.round(100*earned/units)}%.`);
 $('summaryRows').innerHTML=D.questions.map((q,i)=>`<div class="summaryRow"><b>שאלה ${i+1}</b><p class="en">${esc(q.stem)}</p><p class="en">${esc(q.options?answers[i].map(k=>q.options[k]).join('\n'):answers[i].join('\n'))||'—'}</p><p>${checked.has(i)?result(i).ok?'✓ נכון, מעולה!':q.options?result(i).units+' מתוך '+q.scoring_units+' יחידות נכונות':'בדיקה לפי המחוון בסוף המבחן':'טרם נבדק'}</p><button data-jump="${i}">חזרה לשאלה</button>${keys?'<div class="answer">'+keyHTML(q)+'</div>':''}</div>`).join('');document.querySelectorAll('[data-jump]').forEach(b=>b.onclick=()=>show(Number(b.dataset.jump)));}
function exportText(){return 'Check this Module C reading practice against the supplied rubric. Accept equivalent wording and minor spelling/grammar errors when meaning is clear. Award units separately, do not double-count repeated facts. Reading-only practice. Total '+D.questions.reduce((s,q)=>s+q.points,0)+' points. Give the raw score out of 70 and a normalized practice score out of 100 and concise feedback for each question.\n\n'+D.title+'\n'+D.paragraphs.map(p=>p.number+'. '+p.text).join('\n\n')+'\n\n'+D.questions.map((q,i)=>JSON.stringify({question:i+1,stem:q.stem,options:q.options,student_answer:q.options?answers[i].map(k=>q.options[k]):answers[i],answer_key:q.options?correct(q).map(k=>q.options[k]):q.answer_key,grading:q.grading,units:q.scoring_units,points:q.points,evidence:q.evidence},null,2)).join('\n\n');}
function checkOne(){const q=D.questions[page];if(q.options&&answers[page].length!==q.required_answers){$('feedback').textContent='יש לבחור '+q.required_answers+' תשובות לפני הבדיקה.';return;}if(!q.options&&answers[page].some(a=>!a.trim())){$('feedback').textContent='השלימו את התשובה לפני הבדיקה.';return;}checked.add(page);paintFeedback();}
function checkAll(){D.questions.forEach((q,i)=>{if(q.options?answers[i].length===q.required_answers:answers[i].every(a=>a.trim()))checked.add(i);});renderSummary();}
$('title').textContent=D.title;$('prev').onclick=()=>show(page-1);$('next').onclick=()=>show(page+1);$('finish').onclick=()=>{show(7);checkAll();};$('check').onclick=checkOne;$('checkAll').onclick=checkAll;$('allKeys').onclick=()=>renderSummary(true);$('keyToggle').onclick=()=>{$('key').hidden=!$('key').hidden;};$('whyToggle').onclick=()=>{const q=D.questions[page];$('why').innerHTML=answers[page].filter(k=>!correct(q).includes(k)).map(k=>'<p>'+esc(q.distractors[k]?.error_description_en||q.feedback_en)+'</p>').join('');$('why').hidden=!$('why').hidden;};$('textToggle').onclick=()=>{const hidden=$('paragraph').classList.toggle('concealed');$('textToggle').setAttribute('aria-pressed',String(!hidden));};$('paragraphPlay').onclick=()=>{$('paragraph').classList.remove('concealed');$('textToggle').setAttribute('aria-pressed','true');togglePlayback($('paragraph'),'paragraphPlay');};$('questionPlay').onclick=()=>togglePlayback($('question'),'questionPlay');$('stop').onclick=()=>{stop();$('status').textContent='הקריאה נעצרה.';};$('speed').onchange=stop;$('gap').onchange=stop;
$('copy').onclick=async()=>{const text=exportText();$('export').value=text;try{await navigator.clipboard.writeText(text);$('copyStatus').textContent='כל המבחן והמחוון הועתקו. הדביקו ב־AI לבדיקה כוללת.';}catch(e){$('export').hidden=false;$('export').select();$('copyStatus').textContent='הטקסט מוכן: העתיקו מהתיבה שמתחת.';}};
$('full').onclick=()=>{if(document.fullscreenElement)document.exitFullscreen();else document.documentElement.requestFullscreen?.();};document.addEventListener('keydown',e=>{if(/TEXTAREA|INPUT|SELECT/.test(e.target.tagName))return;if(e.key==='ArrowRight')show(page-1);if(e.key==='ArrowLeft')show(page+1);if(e.key==='Escape')stop();});document.addEventListener('visibilitychange',()=>{if(document.hidden)stop();});window.addEventListener('pagehide',stop);show(0);

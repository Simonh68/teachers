/* Read Alone 1+2: shared prerecorded audio; no browser speech synthesis. */
(() => {
'use strict';
const base = new URL('.', document.currentScript.src);
const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const RATE_KEY = 'teachers-read-alone-speed-v1', POS_KEY = 'teachers-grade9-read-alone-position-v1', DONE_KEY = 'teachers-grade9-read-alone-done-v1';
const rates = [[1,'רגילה'],[.75,'איטית'],[.5,'איטית מאוד — חצי'],[.35,'איטית במיוחד'],[.25,'רבע מהמהירות']];
const readStore = (key, fallback) => { try { const value = localStorage.getItem(key); return value === null ? fallback : JSON.parse(value); } catch (_) { return fallback; } };
const store = (key, value) => { try { localStorage.setItem(key, JSON.stringify(value)); } catch (_) {} };
let speed = Number(readStore(RATE_KEY, .75)); if (!rates.some(r => r[0] === speed)) speed = .75;
let data, timing, clip = null, timer = 0, frame = 0, generation = 0, spoken = -1, mode = 'text', page = 0, sentenceSlide = 0, tipTarget = null, tipPinned = false, touch = null;
let interacted = false; document.addEventListener('pointerdown',()=>interacted=true,{once:true}); document.addEventListener('keydown',()=>interacted=true,{once:true}); let standalone = false, deck = false, loading = true, repeatEnd = null; const tabId = Math.random().toString(36).slice(2); let broadcast; try { broadcast = new BroadcastChannel('teachers-read-alone-audio-v1'); broadcast.onmessage = e => { if(e.data !== tabId) stop(); }; } catch (_) {}
let completed = readStore(DONE_KEY, []); if (!Array.isArray(completed)) completed = [];
completed = new Set(completed.filter(n => Number.isInteger(n) && n >= 0));
const audio = new Audio(); audio.id = 'raAudio'; audio.preload = 'auto'; audio.preservesPitch = true;
function status(text) { const el = $('#raStatus'); if (el) el.textContent = text; }
function clearWord() { $$('.ra-word.ra-spoken').forEach(e => e.classList.remove('ra-spoken')); spoken = -1; }
function hideTip() { if (tipTarget) tipTarget.removeAttribute('aria-describedby'); tipTarget = null; tipPinned = false; const el = $('#raTip'); if (el) el.hidden = true; }
function stop() { generation++; clearTimeout(timer); timer = 0; cancelAnimationFrame(frame); audio.pause(); clearWord(); const b = $('[data-ra-play]'); if (b) b.textContent = '▶ הקראה'; }
function range(ids) { repeatEnd = null; stop(); hideTip(); clip = {ids, start: timing.sentences[ids[0]].start, end: timing.sentences[ids.at(-1)].end, words: ids.flatMap(n => timing.sentences[n].words)}; audio.currentTime = Math.max(0, clip.start - .015); const seek = $('#raSeek'); if (seek) { seek.value = '0'; seek.max = String(clip.end - clip.start); } const next = $('#raNext'); if (next) next.classList.remove('ra-finished'); }
function visibleRoot() { return standalone ? $('#raPanel') : $('.slide.active'); }
function sync() {
 if (!clip) return;
 const seek = $('#raSeek'); if (seek && document.activeElement !== seek) seek.value = String(Math.max(0, audio.currentTime - clip.start));
 if (audio.paused) { clearWord(); return; }
 const word = clip.words.find(w => audio.currentTime >= w.start && audio.currentTime < w.end);
 const next = word ? word.index : -1; if (spoken === next) return; clearWord(); spoken = next;
 if (word) { const el = $(`[data-w="${word.index}"]`, visibleRoot() || document); if (el) { el.classList.add('ra-spoken'); if ($('#raFollow')?.checked) { const p = el.closest('.ra-sentence'); if (p && p.getBoundingClientRect().bottom > $('#raPanel').getBoundingClientRect().bottom) p.scrollIntoView({block:'nearest',behavior:'auto'}); } } }
}
function finished() {
 if (!clip) return; audio.currentTime = clip.end; stop();
 if (standalone && mode === 'text') { completed.add(page); store(DONE_KEY, [...completed]); $(`[data-ra-tab="${page}"]`)?.classList.add('ra-done'); $('#raNext')?.classList.add('ra-finished'); }
 status(standalone && mode === 'text' ? 'סיום הקטע. ממשיכים בלחיצה.' : 'סיום המשפט. המעבר לשקף הבא ידני.');
}
function watch(token) { if (token !== generation || audio.paused) return; if (repeatEnd !== null && audio.currentTime >= repeatEnd + .015) { audio.currentTime = repeatEnd; repeatEnd = null; stop(); status('סיום המשפט. לחצו להמשך הקטע.'); return; } if (clip && audio.currentTime >= clip.end + .015) { finished(); return; } sync(); frame = requestAnimationFrame(() => watch(token)); }
async function play(reset = false) {
 if(reset)repeatEnd=null;
 if (loading || !clip) { status('האודיו נטען. נסו שוב בעוד רגע.'); return; }
 stop(); const token = generation;
 if (document.hidden) return;
 if (reset || audio.currentTime < clip.start - .025 || audio.currentTime >= clip.end - .025) audio.currentTime = Math.max(0, clip.start - .015);
 audio.playbackRate = speed; audio.preservesPitch = true;
 try { broadcast?.postMessage(tabId); await audio.play(); if (token !== generation || document.hidden) { audio.pause(); return; } $('[data-ra-play]').textContent = '❚❚ השהיה'; status(''); watch(token); }
 catch (_) { if (token === generation) status('לחצו על ▶ הקראה להפעלת האודיו.'); }
}
function auto() { if(!interacted)return; const token = generation; timer = setTimeout(() => { if (token === generation && !document.hidden) play(true); }, 2000); }
function showTip(el, pinned = false) {
 hideTip(); tipTarget = el; tipPinned = pinned;
 const tip = $('#raTip'); tip.textContent = el.dataset.he; tip.hidden = false; el.setAttribute('aria-describedby', 'raTip');
 const a = el.getBoundingClientRect(), b = tip.getBoundingClientRect();
 tip.style.left = Math.max(8, Math.min(innerWidth - b.width - 8, a.left + (a.width - b.width) / 2)) + 'px';
 tip.style.top = Math.max(4, a.top - b.height - 9 >= 4 ? a.top - b.height - 9 : Math.min(innerHeight - b.height - 4, a.bottom + 9)) + 'px';
}
function wordHTML(w, interactive) { return `<span class="ra-word${interactive ? ' ra-hit' : ''}" data-w="${w.index}"${interactive ? ` data-he="${esc(w.he)}" tabindex="0" role="button" aria-label="${esc(w.word)} — פירוש"` : ''}>${esc(w.word)}</span>`; }
function sentenceHTML(n, units) {
 const s = data.sentences[n]; let out = '';
 if (units) {
  for (const u of s.units) { const words = s.words.slice(u.first, u.last + 1); out += esc(words[0].prefix) + `<span class="ra-unit ra-hit" data-he="${esc(u.he)}" tabindex="0" role="button" aria-label="${esc(u.en)} — פירוש">` + words.map((w, i) => (i ? esc(w.prefix) : '') + wordHTML(w, false)).join('') + '</span>'; }
 } else out = s.words.map(w => esc(w.prefix) + wordHTML(w, true)).join('');
 return out + esc(s.suffix);
}
function fitReading(){if(!standalone)return;const panel=$('#raPanel'), text=$('#raText');if(!panel||!text)return;let size=mode==='text'?(innerWidth<760?25:36):(innerWidth<760?29:49);text.style.fontSize=size+'px';while(panel.scrollHeight>panel.clientHeight+2&&size>20){size--;text.style.fontSize=size+'px';}} window.addEventListener('resize',fitReading);
function savePosition() { store(POS_KEY, {page, sentenceSlide}); }
function render(autoplay = false) {
 if (!standalone || !data) return;
 stop(); hideTip(); const panel = $('#raPanel'); panel.scrollTop = 0;
 document.body.dataset.mode = mode;
 $$('.ra-mode').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.mode === mode)));
 $('#raTabs').hidden = mode !== 'text'; $('#raFollowLabel').hidden = mode !== 'text';
 let ids;
 if (mode === 'text') {
  page = Math.max(0, Math.min(data.pages.length - 1, page)); ids = data.pages[page];
  $('#raTabs').innerHTML = data.pages.map((_, n) => `<button id="raTab${n}" role="tab" aria-selected="${page === n}" aria-controls="raPanel" tabindex="${page === n ? 0 : -1}" data-ra-tab="${n}" class="${completed.has(n) ? 'ra-done' : ''}">${n + 1}</button>`).join('');
  panel.setAttribute('role','tabpanel'); panel.setAttribute('aria-labelledby', `raTab${page}`);
  panel.innerHTML = `<div id="raText" class="ra-text" dir="ltr" lang="en">${ids.map(n => `<p class="ra-sentence" data-sentence="${n}">${sentenceHTML(n, true)}</p>`).join('')}</div><figure class="ra-figure"><img src="${new URL(data.image, base)}" alt="ספרים בספרייה, בהקשר למכירת הספרים בסיפור" loading="lazy"><figcaption>Community library · הספרייה הקהילתית</figcaption></figure>`;
  $('#raCounter').textContent = `קטע ${page + 1} מתוך ${data.pages.length} · משפטים ${ids[0] + 1}–${ids.at(-1) + 1}`;
  $('#raPrev').disabled = page === 0; $('#raNext').textContent = page === data.pages.length - 1 ? 'לשאלות ההבנה ←' : 'המשך ←';
  $('#raProgress').value = (page + 1) / data.pages.length;
  $('#raReveal').hidden = false; $('#raReveal').textContent = 'תרגום הקטע'; $('#raFullTranslation').textContent = ids.map(n => data.sentences[n].he).join(' '); $('#raFullTranslation').hidden = true;
  $(`[data-ra-tab="${page}"]`).scrollIntoView({block:'nearest',inline:'nearest'});
 } else {
  sentenceSlide = Math.max(0, Math.min(data.sentences.length * 2 - 1, sentenceSlide)); const n = Math.floor(sentenceSlide / 2), reveal = sentenceSlide % 2 === 1; ids = [n];
  panel.setAttribute('role','group'); panel.removeAttribute('aria-labelledby'); panel.setAttribute('aria-label', `משפט ${n + 1}`);
  panel.innerHTML = `<div class="ra-sentence-card"><p id="raText" class="ra-single" lang="en" dir="ltr">${sentenceHTML(n, false)}</p><p class="ra-translation" dir="rtl" lang="he" ${reveal ? '' : 'style="visibility:hidden" aria-hidden="true"'}>${esc(data.sentences[n].he)}</p></div>`;
  $('#raCounter').textContent = `משפט ${n + 1} מתוך ${data.sentences.length} · ${reveal ? 'חשיפת התרגום' : 'אנגלית'} · שקף ${sentenceSlide + 1}/${data.sentences.length * 2}`;
  $('#raPrev').disabled = sentenceSlide === 0; $('#raNext').textContent = sentenceSlide === data.sentences.length * 2 - 1 ? 'לשאלות ההבנה ←' : reveal ? 'למשפט הבא ←' : 'חשיפת תרגום ←';
  $('#raProgress').value = (sentenceSlide + 1) / (data.sentences.length * 2); $('#raReveal').hidden = true; $('#raFullTranslation').hidden = true;
 }
 range(ids); savePosition(); fitReading(); requestAnimationFrame(fitReading); status(mode === 'text' ? 'נגיעה בביטוי מציגה פירוש. ההקראה נעצרת בסוף כל קטע.' : 'נגיעה במילה מציגה פירוש. ההקראה מתחילה לאחר שתי שניות.');
 if (mode === 'sentences') auto(); else if (autoplay) play(true);
}
function next(delta, fromTab = false) {
 if (mode === 'text') { if (page + delta >= data.pages.length) { stop(); location.href = new URL('../practice.html#reading-questions', base); return; } page += delta; render(delta > 0 && !fromTab); }
 else { if (sentenceSlide + delta >= data.sentences.length * 2) { stop(); location.href = new URL('../practice.html#reading-questions', base); return; } sentenceSlide += delta; render(); }
}
function toolbar() { return `<div id="raToolbar" class="ra-toolbar" aria-label="בקרי הקראה"><button type="button" data-ra-play>▶ הקראה</button><button type="button" data-ra-restart title="התחלת הקטע מחדש">↶ מההתחלה</button><button type="button" data-ra-repeat>↺ משפט</button><label class="ra-speed">מהירות <select id="raSpeed" aria-label="מהירות הקראה">${rates.map(([n, label]) => `<option value="${n}" ${n === speed ? 'selected' : ''}>${label}</option>`).join('')}</select></label><input id="raSeek" type="range" min="0" max="1" value="0" step="0.01" aria-label="דילוג בתוך הקטע"><label id="raFollowLabel" class="ra-follow"><input id="raFollow" type="checkbox">מעקב גלילה</label><output id="raStatus" role="status" aria-live="polite"></output></div>`; }
function bind() {
 $('[data-ra-play]').onclick = () => { if (!audio.paused) { stop(); status('מושהה. לחיצה על הקראה ממשיכה מאותה נקודה.'); } else play(); };
 $('[data-ra-restart]').onclick = () => play(true);
 $('[data-ra-repeat]').onclick = () => { if (!clip) return; const id = clip.ids.find(n => audio.currentTime >= timing.sentences[n].start && audio.currentTime <= timing.sentences[n].end + .15) ?? clip.ids.findLast(n => timing.sentences[n].start <= audio.currentTime) ?? clip.ids[0]; repeatEnd = timing.sentences[id].end; audio.currentTime = Math.max(0,timing.sentences[id].start - .015); play(); };
 $('#raSpeed').onchange = e => { speed = Number(e.target.value); audio.playbackRate = speed; store(RATE_KEY, speed); };
 $('#raSeek').oninput = e => { clearTimeout(timer); timer = 0; repeatEnd = null; if (clip) { audio.currentTime = Math.min(clip.end, clip.start + Number(e.target.value)); clearWord(); sync(); } };
 document.addEventListener('click', e => { const hit = e.target.closest('.ra-hit'); if (hit) { e.preventDefault(); showTip(hit,true); } else if (!e.target.closest('#raTip')) hideTip(); });
 document.addEventListener('pointerover', e => { const hit = e.target.closest('.ra-hit'); if (hit && e.pointerType !== 'touch') showTip(hit); });
 document.addEventListener('pointerout', e => { if (!tipPinned && tipTarget && !tipTarget.contains(e.relatedTarget)) hideTip(); });
 document.addEventListener('focusin', e => { if (e.target.matches('.ra-hit')) showTip(e.target); });
 document.addEventListener('keydown', e => { if (e.key === 'Escape') hideTip(); if ((e.key === 'Enter' || e.key === ' ') && e.target.matches('.ra-hit')) { e.preventDefault(); e.stopPropagation(); showTip(e.target,true); } }, true);
 document.addEventListener('scroll', hideTip, true); window.addEventListener('resize', hideTip);
 document.addEventListener('visibilitychange', () => { if (document.hidden) { stop(); hideTip(); } }); window.addEventListener('pagehide', stop);
 document.addEventListener('toggle', e => { if ((e.target.matches('dialog') && e.target.open) || (e.target.matches('details') && e.target.open)) stop(); }, true);
 audio.addEventListener('timeupdate', () => { if (!audio.paused && clip && audio.currentTime >= clip.end + .015) finished(); else sync(); }); audio.addEventListener('pause',clearWord); audio.addEventListener('ended',finished);
 audio.addEventListener('error', () => { stop(); status('טעינת ההקלטה נכשלה. רעננו את הדף או נסו שוב.'); });
 window.addEventListener('storage', e => { if (e.key === RATE_KEY) { const value = Number(readStore(RATE_KEY,.75)); speed = rates.some(r => r[0] === value) ? value : .75; audio.playbackRate = speed; $('#raSpeed').value = String(speed); } });
}
async function init() {
 standalone = !!$('#raApp'); deck = !!document.body.dataset.raDeck; if (!standalone && !deck) return;
 document.body.append(audio); const tip = document.createElement('div'); tip.id = 'raTip'; tip.dir = 'rtl'; tip.lang = 'he'; tip.role = 'tooltip'; tip.hidden = true; document.body.append(tip);
 const host = standalone ? $('#raControls') : document.body.appendChild(Object.assign(document.createElement('div'),{className:'ra-deck-controls'})); host.innerHTML = toolbar(); if (deck) host.hidden = true;
 const meaningDock = standalone ? $('#raMeaningDock') : host.appendChild(Object.assign(document.createElement('div'),{id:'raMeaningDock',dir:'rtl'})); meaningDock.append($('#raTip'));
 bind(); status('טוען טקסט והקלטה…');
 try {
  [data,timing] = await Promise.all(['content.json','audio.json'].map(async name => { const r = await fetch(new URL(name + '?v=20260922-ra1',base)); if (!r.ok) throw new Error(name + ' ' + r.status); return r.json(); }));
  if (data.sentences.length !== timing.sentences.length) throw new Error('audio/text mismatch');
  audio.src = new URL(timing.audio,base); audio.playbackRate = speed; loading = false;
  if (standalone) {
   const saved = readStore(POS_KEY,{}); page = Number.isInteger(saved?.page) ? saved.page : 0; sentenceSlide = Number.isInteger(saved?.sentenceSlide) ? saved.sentenceSlide : 0;
   mode = new URLSearchParams(location.search).get('mode') === 'sentences' ? 'sentences' : 'text';
   const requested = new URLSearchParams(location.search).get('sentence'); if (requested && Number.isInteger(Number(requested))) { sentenceSlide = Math.max(0,(Number(requested)-1)*2); page = Math.max(0,data.pages.findIndex(ids => ids.includes(Number(requested)-1))); }
   $$('.ra-mode').forEach(b => b.onclick = () => { if (mode === b.dataset.mode) return; if (b.dataset.mode === 'sentences') sentenceSlide = data.pages[page][0]*2; else page = Math.max(0,data.pages.findIndex(ids => ids.includes(Math.floor(sentenceSlide/2)))); mode = b.dataset.mode; const url = new URL(location.href); url.searchParams.set('mode',mode); url.searchParams.delete('sentence'); history.replaceState(null,'',url); render(); });
   $('#raPrev').onclick = () => next(-1,true); $('#raNext').onclick = () => next(1);
   $('#raTabs').onclick = e => { const b = e.target.closest('[data-ra-tab]'); if (b) { page = Number(b.dataset.raTab); render(); } };
   $('#raTabs').onkeydown = e => { if (!['ArrowLeft','ArrowRight','Home','End'].includes(e.key)) return; e.preventDefault(); e.stopPropagation(); page = e.key === 'Home' ? 0 : e.key === 'End' ? data.pages.length-1 : Math.max(0,Math.min(data.pages.length-1,page+(e.key==='ArrowRight'?-1:1))); render(); $(`[data-ra-tab="${page}"]`).focus(); };
   $('#raReveal').onclick = () => { const el = $('#raFullTranslation'); el.hidden = !el.hidden; $('#raReveal').textContent = el.hidden ? 'תרגום הקטע' : 'הסתרת התרגום'; };
   document.addEventListener('keydown', e => { if (e.defaultPrevented || e.altKey || e.ctrlKey || e.metaKey || e.target.closest('input,select,textarea,.ra-hit,[role=tab]')) return; if (['ArrowRight','ArrowDown','PageDown'].includes(e.key)) { e.preventDefault(); next(1); } else if (['ArrowLeft','ArrowUp','PageUp'].includes(e.key)) { e.preventDefault(); next(-1,true); } });
   $('#raPanel').addEventListener('touchstart', e => { if (e.touches.length === 1) touch = {x:e.touches[0].clientX,y:e.touches[0].clientY}; },{passive:true});
   $('#raPanel').addEventListener('touchend', e => { if (!touch) return; const t=e.changedTouches[0],dx=t.clientX-touch.x,dy=t.clientY-touch.y; touch=null; if(Math.abs(dx)>55 && Math.abs(dx)>Math.abs(dy)*1.25) next(dx<0?1:-1,true); },{passive:true});
   $('#raPanel').addEventListener('touchcancel',()=>touch=null,{passive:true}); render();
  } else {
   mode = 'sentences';
   const update = () => { stop(); hideTip(); const s = $('.slide.active[data-ra-sentence]'); host.hidden = !s; if (!s) { clip=null; return; } range([Number(s.dataset.raSentence)]); requestAnimationFrame(()=>{document.body.style.setProperty('--ra-toolbar-space',(host.offsetHeight+10)+'px');window.dispatchEvent(new Event('resize'));}); status('הקראה לאחר שתי שניות · נגיעה במילה לפירוש'); auto(); };
   document.addEventListener('teachers:slidechange',update); update();
   document.addEventListener('click',e=>{if(e.target.closest('.section-nav,[data-step],.home'))hideTip();},true);
  }
 } catch (err) { loading = true; stop(); status('לא ניתן לטעון את הקריאה. רעננו את הדף.'); console.error('Read Alone loading:',err); }
}
window.TeachersReadAlone = {stop, setPage(n,m='text'){mode=m;if(m==='text')page=n;else sentenceSlide=n;render();}, get mode(){return mode;}, get page(){return page;}, get sentenceSlide(){return sentenceSlide;}, get audio(){return audio;}, get data(){return data;}, get timing(){return timing;}, get clip(){return clip;}};
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded',init,{once:true}); else init();
})();

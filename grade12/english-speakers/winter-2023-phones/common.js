(() => {
const lang=new URLSearchParams(location.search).get('lang')==='he'?'he':'en';
const t=(en,he)=>lang==='he'?he:en;
const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const exp=(s,cls='')=>`<p class="explain ${cls}" dir="${lang==='he'?'rtl':'ltr'}">${esc(s)}</p>`;
const list=(items,cls='')=>`<ul class="explain ${cls}" dir="${lang==='he'?'rtl':'ltr'}">${items.map(s=>`<li>${esc(s)}</li>`).join('')}</ul>`;
const qtext=q=>lang==='he'?{...q,...window.PHONES_HE[q.n-1]}:q;
const sourceNote=t('This teaching key uses the extended answer key supplied by the teacher (updated January 25). Its official status has not been independently verified. The explanations, exercises and model essay are teaching additions. Deductions below are examples from the supplied key, not an automatic grade.','המפתח הלימודי נשען על מפתח התשובות המורחב שסופק למורה, המעודכן ל־25 בינואר. מעמדו כמסמך רשמי לא אומת בנפרד. ההסברים, התרגילים והחיבור לדוגמה הם תוספות לימודיות. הפחתות הניקוד הן דוגמאות מהמפתח המצורף ואינן ציון אוטומטי.');
function sources(){return exp(sourceNote,'source-note')+`<ul class="source-list" dir="${lang==='he'?'rtl':'ltr'}"><li>${esc(t('Supplied file: Extended AK — Why kids can’t put down phones, W 2023.','הקובץ המצורף: Extended AK — Why kids can’t put down phones, W 2023.'))}</li><li><a target="_blank" rel="noopener" href="${window.PHONES.exam}">${esc(t('Ministry of Education: original Version A paper','משרד החינוך: השאלון המקורי, גרסה א׳'))}</a></li><li><a target="_blank" rel="noopener" href="${window.PHONES.officialKey}">${esc(t('Ministry of Education: answer-key link','משרד החינוך: קישור למפתח התשובות'))}</a> — ${esc(t('the server blocked access during preparation','השרת חסם גישה בזמן ההכנה'))}</li><li><a target="_blank" rel="noopener" href="${window.PHONES.geva}">${esc(t('Yoel Geva: paper with suggested answers','יואל גבע: השאלון עם פתרונות מוצעים'))}</a> (${esc(t('includes answers','כולל תשובות'))})</li><li><a target="_blank" rel="noopener" href="${window.PHONES.highq}">High-Q</a></li></ul>`;}
document.documentElement.lang=lang;
window.PHONE_UI={lang,t,esc,exp,list,qtext,sourceNote,sources};
})();

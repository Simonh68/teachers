/* Original neutral vector scenes. No people, characters, emblems or religious imagery. */
window.TeachersScenes = (() => {
  const wrap = (s) => `<svg viewBox="0 0 1200 700" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">${s}</svg>`;
  const defs = `<defs><linearGradient id="sky" x2="0" y2="1"><stop stop-color="#122851"/><stop offset=".65" stop-color="#6982d8"/><stop offset="1" stop-color="#ffbc84"/></linearGradient><linearGradient id="water" x2="0" y2="1"><stop stop-color="#24e1de"/><stop offset="1" stop-color="#083b6e"/></linearGradient><linearGradient id="sand" x2="0" y2="1"><stop stop-color="#ffdc75"/><stop offset="1" stop-color="#a82b71"/></linearGradient><linearGradient id="light" x2="1" y2="1"><stop stop-color="#67ffd1" stop-opacity="0"/><stop offset=".45" stop-color="#55ffd2" stop-opacity=".8"/><stop offset=".7" stop-color="#ac76ff" stop-opacity=".65"/><stop offset="1" stop-color="#ff6aa7" stop-opacity="0"/></linearGradient><filter id="blur"><feGaussianBlur stdDeviation="12"/></filter></defs>`;
  function stars(n=35) { return Array.from({length:n},(_,i)=>`<circle cx="${35+(i*179)%1130}" cy="${20+(i*71)%260}" r="${i%3===0?2:1}" fill="#fff" opacity="${.35+(i%5)*.12}"/>`).join(''); }
  function landscape(kind,variant=0) {
    if(kind==='desert') return wrap(defs+`<rect width="1200" height="700" fill="url(#sky)"/><circle cx="${810+variant*40}" cy="165" r="83" fill="#ffe88d"/><path d="M0 365 Q270 160 570 370 Q830 150 1200 325 V700 H0Z" fill="#e98d61"/><path d="M0 425 Q190 195 530 410 Q920 260 1200 405 V700 H0Z" fill="url(#sand)"/><path d="M0 495 Q510 270 1200 535 V700 H0Z" fill="#b95281"/><path d="M0 425 Q190 195 530 410" fill="none" stroke="#ffe6a3" stroke-width="4"/><path d="M0 495 Q510 270 1200 535" fill="none" stroke="#f59fc8" stroke-width="3"/>`);
    if(kind==='ocean') return wrap(defs+`<rect width="1200" height="700" fill="#399cda"/><circle cx="990" cy="110" r="65" fill="#ffdb7a"/><path d="M0 170 Q150 110 360 185 T760 170 T1200 175 V700 H0Z" fill="#15cfda"/><path d="M0 240 Q150 180 360 255 T760 240 T1200 245" fill="none" stroke="#bafcef" stroke-width="9"/><path d="M0 340 Q150 260 400 350 T820 325 T1200 340 V700 H0Z" fill="#1676ad"/><path d="M0 340 Q150 260 400 350 T820 325 T1200 340" fill="none" stroke="#67ebf2" stroke-width="8"/><path d="M0 470 Q250 360 540 470 T1200 470 V700 H0Z" fill="#064c85"/><path d="M0 470 Q250 360 540 470 T1200 470" fill="none" stroke="#39b9ce" stroke-width="7"/>`);
    if(kind==='canyon') return wrap(defs+`<rect width="1200" height="700" fill="url(#sky)"/><circle cx="690" cy="160" r="75" fill="#ffd09a"/><path d="M0 180 H190 L270 290 H340 L410 440 L600 650 L790 430 L850 280 H935 L1020 200 H1200 V700 H0Z" fill="#a84880"/><path d="M0 210 H170 L235 350 H345 L480 550 L570 700 H0Z" fill="#e97759"/><path d="M1200 215 H1040 L975 370 H895 L750 540 L620 700 H1200Z" fill="#ba454e"/><path d="M550 700 Q850 610 650 500 Q510 430 750 390 Q850 350 730 315" fill="none" stroke="#4de5eb" stroke-width="26"/><path d="M0 300 H165 M0 340 H202 M0 380 H270 M1020 285 H1200 M996 328 H1200 M956 385 H1200" stroke="#ffb06f" stroke-width="7" opacity=".65"/>`);
    const aurora=kind==='aurora', rainbow=kind==='rainbow';
    return wrap(defs+`<rect width="1200" height="700" fill="${aurora?'#071637':'url(#sky)'}"/>${stars(aurora?70:12)}${aurora?`<g fill="none" stroke="url(#light)" filter="url(#blur)" stroke-width="88"><path d="M30 25 Q190 150 320 70 T630 100 T1170 40"/><path d="M190 0 Q440 270 730 90 T1190 210"/></g>`:`<circle cx="${930-variant*50}" cy="130" r="61" fill="#ffeaa2"/>`}${rainbow?['#ff688d','#ffac60','#ffe38a','#6bedc1','#64d4ff','#b892ff'].map((c,i)=>`<path d="M170 340 A${440-i*11} ${285-i*10} 0 0 1 1050 340" stroke="${c}" stroke-width="12" fill="none" opacity=".85"/>`).join(''):''}<path d="M0 345 L180 110 L280 245 L455 70 L670 315 L850 145 L1030 310 L1200 170 V700 H0Z" fill="#415889"/><path d="M114 195 L180 110 L229 182 L197 169 L182 186 L159 166ZM368 170 L455 70 L533 160 L487 137 L462 157 L441 133 L414 162ZM808 196 L850 145 L905 207 L862 188 L844 209Z" fill="#e4f4ff"/><path d="M0 398 L160 285 L355 383 L635 240 L800 366 L1065 280 L1200 395 V700 H0Z" fill="#146b83"/><path d="M0 475 Q370 355 720 442 T1200 420 V700 H0Z" fill="url(#water)"/><g stroke="#8affec" opacity=".3"><path d="M260 486 H680 M340 512 H870 M190 539 H590 M430 574 H980 M270 610 H660" stroke-width="4"/></g><path d="M0 410 L70 400 L130 500 L85 700 H0ZM1200 385 L1110 420 L1050 535 L1090 700 H1200Z" fill="#06384b"/><g fill="#04283b">${[20,65,110,1100,1150,1190].map((x,i)=>`<path d="M${x} ${290+i%3*25} l-35 105 h20 l-35 78 h100 l-35-78 h20 Z"/>`).join('')}</g>`);
  }
  function diagram(kind,variant=0) {
    let content='';
    if(kind==='circles') {
      content=[{x:375,outer:82,orbit:155,n:6},{x:820,outer:27,orbit:105,n:8}].map(v=>`<g class="context">${Array.from({length:v.n},(_,i)=>{const a=i*2*Math.PI/v.n;return `<circle cx="${v.x+Math.cos(a)*v.orbit}" cy="${225+Math.sin(a)*v.orbit}" r="${v.outer}" fill="#83bce6"/>`;}).join('')}</g><circle cx="${v.x}" cy="225" r="53" fill="#ff9b31" stroke="#fff5c2" stroke-width="3"/><line class="proof" x1="${v.x-53}" y1="225" x2="${v.x+53}" y2="225" stroke="#fff" stroke-width="4"/>`).join('');
    } else if(kind==='colors') {
      content=`<g class="context"><rect x="210" y="68" width="340" height="300" rx="28" fill="#060b2c"/><rect x="680" y="68" width="340" height="300" rx="28" fill="#eaf7ff"/></g><rect x="330" y="160" width="100" height="100" fill="#8585ff"/><rect x="800" y="160" width="100" height="100" fill="#8585ff"/><path class="proof" d="M430 210 H800" stroke="#8585ff" stroke-width="60"/>`;
    } else if(kind==='lines') {
      content=`<g class="context" fill="none" stroke="#7bc5fa" stroke-width="12"><path d="M400 90 L330 145 L400 200 M800 90 L870 145 L800 200 M260 240 L330 295 L260 350 M940 240 L870 295 L940 350"/></g><path d="M330 145 H870 M330 295 H870" stroke="#ffe45f" stroke-width="11"/><path class="proof" d="M330 110 V330 M870 110 V330" stroke="#fc83d5" stroke-dasharray="9 9" stroke-width="4"/>`;
    } else if(kind==='parallel') {
      content=`<g class="context">${Array.from({length:5},(_,r)=>Array.from({length:12},(_,c)=>`<rect x="${145+c*78+(r%2)*35}" y="${70+r*58}" width="78" height="58" fill="${c%2?'#eff5ff':'#183b6c'}"/>`).join('')).join('')}</g>${Array.from({length:6},(_,r)=>`<path d="M145 ${70+r*58} H1080" stroke="#fd658f" stroke-width="4"/>`).join('')}`;
    } else if(kind==='triangles') {
      const special=(variant*3+6)%12;
      content=Array.from({length:12},(_,i)=>{const x=280+i%6*128,y=145+Math.floor(i/6)*140;return `<g transform="translate(${x},${y})"><path d="${i===special?'M-38-32H38L0 38Z':'M0-38L38 32H-38Z'}" fill="${['#59e5ee','#ffc356','#f78bc0'][i%3]}"/><text x="0" y="68" text-anchor="middle" fill="#fff" font-family="Arial" font-size="20">${i+1}</text>${i===special?'<circle class="proof" r="53" fill="none" stroke="#fff" stroke-width="4"/>':''}</g>`;}).join('');
    } else {
      const n=6+variant;
      content=stars(50)+Array.from({length:n},(_,i)=>{const x=225+(i*173)%780,y=110+(i*97)%220;return `<path d="M${x} ${y-23}l7 16 18 2-14 12 4 18-15-9-16 9 4-18-14-12 18-2Z" fill="#ffe460"/>`;}).join('');
    }
    return wrap(`<defs><radialGradient id="bg"><stop stop-color="#214879"/><stop offset="1" stop-color="#0b1833"/></radialGradient></defs><rect width="1200" height="700" fill="url(#bg)"/>${content}`).replace('0 0 1200 700','0 0 1200 420').replace('xMidYMid slice','xMidYMid meet');
  }
  const catalog=[
    ['aurora','Northern lights','Charged particles make gases high in the sky glow.','חלקיקים טעונים גורמים לגזים גבוה בשמיים לזהור.','https://science.nasa.gov/sun/auroras/'],
    ['circles','Look twice','Which orange circle looks bigger?','איזה עיגול כתום נראה גדול יותר?','', 'Both orange circles are the same size.','שני העיגולים הכתומים שווים בגודלם.'],
    ['mountain','A mountain lake','Can you find three shades of blue?','האם תוכלו למצוא שלושה גוונים של כחול?'],
    ['colors','The same color?','Are the two small squares the same color?','האם לשני הריבועים הקטנים יש אותו צבע?','', 'Both squares have exactly the same color.','לשני הריבועים יש בדיוק אותו צבע.'],
    ['canyon','Deep in the valley','Describe this valley in three English words.','תארו את העמק הזה בשלוש מילים באנגלית.'],
    ['rainbow','Colors in the sky','Sunlight can split into colors inside water drops.','אור השמש יכול להתפצל לצבעים בתוך טיפות מים.','https://scijinks.gov/rainbow/'],
    ['parallel','Straight or bent?','Are the pink lines straight or bent?','האם הקווים הוורודים ישרים או כפופים?','', 'All the pink lines are straight.','כל הקווים הוורודים ישרים.'],
    ['stars','A night-sky puzzle','How many yellow stars can you see?','כמה כוכבים צהובים אתם רואים?'],
    ['desert','Dunes at sunset','Name two colors in this landscape.','אמרו שמות של שני צבעים בנוף הזה.'],
    ['triangles','Find the difference','Which triangle points down?','איזה משולש פונה כלפי מטה?'],
    ['ocean','Ocean colors','Describe the sea in three English words.','תארו את הים בשלוש מילים באנגלית.'],
    ['lines','Longer or shorter?','Which yellow line is longer?','איזה קו צהוב ארוך יותר?','', 'Both yellow lines have the same length.','שני הקווים הצהובים שווים באורכם.']
  ];
  function get(n) {
    const variant=Math.floor(n/catalog.length), c=catalog[n%catalog.length];
    const [kind,title,en,he,source='',answer='',answerHe='']=c;
    const out={kind,title,en,he,source,answer,answerHe,svg:['aurora','mountain','canyon','rainbow','desert','ocean'].includes(kind)?landscape(kind,variant):diagram(kind,variant)};
    if(kind==='stars'){out.answer=`There are ${6+variant} yellow stars.`;out.answerHe=`יש ${6+variant} כוכבים צהובים.`;}
    if(kind==='triangles'){const i=(variant*3+6)%12+1;out.answer=`Triangle ${i} points down.`;out.answerHe=`משולש ${i} פונה כלפי מטה.`;}
    return out;
  }
  return {get};
})();

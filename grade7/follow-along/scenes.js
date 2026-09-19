/* Original inline SVG scenes. Every boy wears a cap. No external assets. */
(()=>{
function boy(x,y,shirt,cap,bag,extra=''){
return `<g transform="translate(${x} ${y})"><g class="boy ${extra}">
<path d="M-9 55L-12 93M10 55L14 93" stroke="#263852" stroke-width="13" stroke-linecap="round"/>
<path d="M-18 97h15M8 97h16" stroke="#0a1b30" stroke-width="8" stroke-linecap="round"/>
<rect x="-28" y="19" width="22" height="40" rx="8" fill="${bag}"/>
<path d="M-10 19h22l6 42h-35z" fill="${shirt}"/>
<path d="M-9 25L-21 51" stroke="#dfb68f" stroke-width="8" stroke-linecap="round"/>
<g class="arm"><path d="M11 25L27 46" stroke="#dfb68f" stroke-width="8" stroke-linecap="round"/></g>
<rect x="-4" y="9" width="10" height="14" rx="4" fill="#dca87f"/>
<ellipse cx="0" cy="0" rx="17" ry="20" fill="#e7bd95"/>
<path d="M-18 -5Q-19 -28 2 -27Q20 -25 20 -6Z" fill="${cap}"/>
<path d="M-17 -6h44q4 7-6 8L-17 -1Z" fill="${cap}" stroke="#10273c" stroke-width="2"/>
<circle cx="-5" cy="4" r="1.8" fill="#203347"/><circle cx="8" cy="4" r="1.8" fill="#203347"/>
<path d="M-3 12q5 4 9-1" fill="none" stroke="#9d5d48" stroke-width="2" stroke-linecap="round"/>
</g></g>`;}
const sky='<rect width="360" height="300" rx="20" fill="#183b53"/><circle cx="295" cy="48" r="22" fill="#ffe082"/><g fill="#d9eff1" opacity=".75"><ellipse cx="62" cy="45" rx="37" ry="12"/><ellipse cx="89" cy="41" rx="20" ry="15"/></g>';
const scenes=[
`<svg viewBox="0 0 360 300" role="img" aria-labelledby="sceneTitle"><title id="sceneTitle">דן חובש כובע כחול, בדרך לאוטובוס ולרכבת</title>${sky}<path d="M0 164L92 112l80 50 107-64 81 61v80H0Z" fill="#295c64"/>
<g class="bus"><rect x="176" y="121" width="143" height="66" rx="12" fill="#ecc76a"/><g fill="#183c55"><rect x="186" y="133" width="32" height="24" rx="4"/><rect x="226" y="133" width="32" height="24" rx="4"/><rect x="266" y="133" width="40" height="24" rx="4"/></g><circle cx="202" cy="186" r="11" fill="#10253a"/><circle cx="292" cy="186" r="11" fill="#10253a"/></g>
<path d="M0 200h360v100H0Z" fill="#244653"/><path d="M0 219h360" stroke="#6e96a1" stroke-width="3" stroke-dasharray="20 12" class="road"/>
<path d="M53 97v99" stroke="#aac9cf" stroke-width="5"/><rect x="29" y="78" width="49" height="35" rx="7" fill="#6ee5f7"/><path d="M40 92h26m-22 9h18" stroke="#17374d" stroke-width="4"/>
${boy(111,155,'#68bad5','#356fa0','#4264a4','walking')}<text x="335" y="278" text-anchor="end" fill="#cde9ee" font-size="16">A long way to school</text></svg>`,
`<svg viewBox="0 0 360 300" role="img" aria-labelledby="sceneTitle"><title id="sceneTitle">שני ילדים בכובעים ברכבת; לאחד תיק ירוק. דן חושב על הגשם</title><rect width="360" height="300" rx="20" fill="#17344d"/><rect x="23" y="25" width="314" height="138" rx="16" fill="#a8d5db"/><g class="landscape"><path d="M0 141l70-40 60 33 75-59 82 65 73-30 90 40v25H0Z" fill="#5b9093"/></g><g class="rain" stroke="#54889e" stroke-width="2"><path d="M70 42l-6 15m48 6-6 15m45-36-6 15m59 7-6 15m59-39-6 15m42 11-6 15"/></g><path d="M180 26v134" stroke="#45687d" stroke-width="8"/><rect x="20" y="207" width="320" height="27" rx="7" fill="#335875"/>
${boy(101,132,'#bd897b','#ca8e48','#82b859','sway')}${boy(247,132,'#82a5c9','#8d81b9','#587c91','sway')}
<rect x="35" y="247" width="290" height="37" rx="10" fill="#112a3f"/><text x="180" y="272" text-anchor="middle" fill="#d9fa9c" font-size="17">Two boys. A green bag.</text></svg>`,
`<svg viewBox="0 0 360 300" role="img" aria-labelledby="sceneTitle"><title id="sceneTitle">דן בכובע כחול מנופף לשלום לשני חבריו, שגם הם בכובעים, בכיתה</title><rect width="360" height="300" rx="20" fill="#234a52"/><rect x="148" y="23" width="191" height="104" rx="8" fill="#102d39" stroke="#99a98d" stroke-width="5"/><text x="244" y="66" text-anchor="middle" fill="#ebf4d4" font-size="24">Welcome!</text><text x="244" y="99" text-anchor="middle" fill="#8fd5d8" font-size="18">Grade 7</text><path d="M17 236V44h85v192" fill="#ad8a68" stroke="#ceab84" stroke-width="6"/><circle cx="89" cy="143" r="4" fill="#ffe082"/><path d="M0 239h360v61H0Z" fill="#366062"/>
${boy(74,143,'#68bad5','#356fa0','#4264a4','wave')}${boy(191,143,'#bd897b','#ca8e48','#82b859','sway')}${boy(295,143,'#82a5c9','#8d81b9','#587c91','sway')}
<text x="180" y="281" text-anchor="middle" fill="#e5fac0" font-size="18">Hello!</text></svg>`
];window.READING_SCENES=scenes;
})();

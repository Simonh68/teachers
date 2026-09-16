import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
import {createCanvas,GlobalFonts} from '@napi-rs/canvas';
const BUILD=path.dirname(new URL(import.meta.url).pathname),ROOT=path.dirname(path.dirname(BUILD)),SITE=path.join(ROOT,'grade11/grammar-in-an-essay');
const SKILL='/root/.codex/skills/builtins/presentations';
process.env.RUNTIME_NODE=process.env.CODEX_PRIMARY_RUNTIME_NODE;process.env.RUNTIME_NODE_MODULES=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;process.env.RUNTIME_PYTHON=process.env.CODEX_PRIMARY_RUNTIME_PYTHON;process.env.RUNTIME_BIN_DIR=process.env.CODEX_PRIMARY_RUNTIME+'/dependencies/bin/override';
GlobalFonts.registerFromPath(path.join(SITE,'assets/Nunito.ttf'),'Nunito');
const ctx=createCanvas(10,10).getContext('2d');
const D=JSON.parse(await fs.readFile(path.join(SITE,'lesson.json'),'utf8'));
const P=Presentation.create({slideSize:{width:1280,height:720}});
const C={bg:'#07111F',paper:'#F7F7F2',cyan:'#4EE5FF',lime:'#DFFF5B',amber:'#FFC857',muted:'#A9BDD2',coral:'#FF7163'};
let serial=0;
function tx(slide,text,x,y,w,h,size,color=C.paper,bold=true,align='center',name='text'){
 if(!text)return null;
 const sh=slide.shapes.add({name:`${name}-${++serial}`,geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 sh.text=text;sh.text.style={typeface:/[\u0590-\u05ff]/.test(text)?'Heebo':'Nunito',fontSize:size,bold,color,alignment:align,verticalAlignment:'middle',autoFit:'none',wrap:'square',insets:{left:0,right:0,top:0,bottom:0}};
 return sh;
}
function highlights(sh,terms){for(const t of terms||[])if(sh)sh.text.get(t).fill=C.cyan;}
function gapSentence(slide,s){
 const size=43;ctx.font=`800 ${size}px Nunito`;
 const space=ctx.measureText(' ').width*1.15;
 const bw=Math.max(...s.options.map(t=>ctx.measureText(t).width*1.16))+30;
 const tokens=[...s.before.trim().split(/\s+/).filter(Boolean).map(t=>({t,w:ctx.measureText(t).width*1.16})),{t:s.reveal?s.options[s.correct]:'',w:bw,gap:true},...s.after.trim().split(/\s+/).filter(Boolean).map(t=>({t,w:ctx.measureText(t).width*1.16}))];
 const lines=[[]];let used=0;for(const t of tokens){if(used+t.w+space>1100&&lines.at(-1).length){lines.push([]);used=0;}lines.at(-1).push(t);used+=t.w+space;}
 const y0=174+(155-lines.length*65)/2;
 lines.forEach((line,li)=>{let x=(1280-line.reduce((n,t)=>n+t.w,0)-space*(line.length-1))/2;for(const t of line){if(t.gap){const sh=tx(slide,t.t||' ',x,y0+li*65,t.w,58,size,C.lime,true);slide.shapes.add({name:'gap-line-'+s.n,geometry:'line',position:{left:x,top:y0+li*65+57,width:t.w,height:0},line:{fill:s.reveal?C.lime:C.cyan,width:2}});}else tx(slide,t.t,x-2,y0+li*65,t.w+4,58,size,C.paper,true);x+=t.w+space;}});
}
for(const s of D.slides){
 const sl=P.slides.add();sl.background.fill={type:'gradient',gradientKind:'linear',angleDeg:24,stops:[{offset:0,color:'#102A42'},{offset:65000,color:C.bg},{offset:100000,color:'#161B35'}]};
 const home=tx(sl,'⌂',38,30,44,38,30,C.paper,false);home.text.get('⌂').link={uri:'https://simonh68.github.io/teachers/grade11/five-units/',isExternal:true};
 tx(sl,s.title,95,53,1090,55,28,C.cyan,true,'center','title');
 if(s.tense)tx(sl,s.tense,100,105,1080,30,20,'#FFE35B');
 if(s.kind==='cover'){
  tx(sl,'ברוכים הבאים',80,216,1120,116,86,C.lime);tx(sl,'כיתה י״א · 5 יח״ל',80,356,1120,60,45);tx(sl,s.he,80,445,1120,60,36,C.muted);
 }else if(s.kind==='animation'){
  sl.images.add({blob:new Uint8Array(await fs.readFile(path.join(SITE,'assets',s.asset+'.gif'))),contentType:'image/gif',alt:s.alt,fit:'contain',position:{left:450,top:137,width:380,height:380}});
  tx(sl,s.text,80,540,1120,94,36,C.amber,true);
 }else if(s.kind==='gap'){
  gapSentence(sl,s);
  s.options.forEach((o,i)=>tx(sl,`${String.fromCharCode(65+i)}   ${o}`,90+i*374,378,352,90,33,s.reveal&&i===s.correct?C.lime:C.paper,true));
  tx(sl,s.he,92,514,1096,124,30,C.lime);
 }else if(s.kind==='choice'){
  tx(sl,s.text,90,137,1100,98,40,C.paper,true);
  s.options.forEach((o,i)=>tx(sl,`${String.fromCharCode(65+i)}   ${o}`,95,254+i*88,1090,78,o.length>99?28:31,s.reveal&&i===s.correct?C.lime:C.paper,true,'left'));
  tx(sl,s.he,95,540,1090,109,28,C.lime);
 }else if(s.kind==='essay'){
  let y=133;
  for(const para of s.paragraphs){tx(sl,para,88,y,1104,113,29,C.paper,false,'left');y+=120;}
  tx(sl,s.he,90,623,1100,34,22,C.lime);
 }else if(s.kind==='timer'){
  tx(sl,s.text,90,164,1100,156,45,C.paper,true);
  tx(sl,s.he,100,330,1080,102,31,C.muted,true);
  tx(sl,`${String(Math.floor(s.seconds/60)).padStart(2,'0')}:${String(s.seconds%60).padStart(2,'0')}`,100,456,1080,100,85,C.amber);
  const sh=tx(sl,'שעון פעיל במצגת באתר',100,583,1080,41,24,C.cyan,true);sh.text.get('שעון פעיל במצגת באתר').link={uri:`https://simonh68.github.io/teachers/grade11/grammar-in-an-essay/#slide-${s.n}`,isExternal:true};
 }else if(s.kind==='example'){
  const sh=tx(sl,s.text,85,157,1110,262,s.text.length>160?38:46,C.paper,true);highlights(sh,s.highlights);
  tx(sl,s.he,92,461,1096,169,s.he.length>150?29:33,C.lime,true);
 }else{
  let size=s.text.length>210?36:s.text.length>125?40:46;
  const sh=tx(sl,s.text,85,151,1110,294,size,C.paper,true);highlights(sh,s.highlights);
  tx(sl,s.he,92,475,1096,151,s.he.length>130?30:33,C.muted,true);
 }
 tx(sl,`${s.n} / ${D.slides.length}`,1100,674,120,24,17,C.muted,false);
 let notes=s.note||'';if(s.kind==='animation')notes+='\nOriginal Teachers generated cat illustration, reused for this lesson with new grammar context. Silent GIF, 6 cycles of 1.8 seconds.';if(s.source)notes+='\nSource: '+s.source;if(s.kind==='timer')notes+='\nTimer is interactive in the HTML version. PPTX shows the time allocation and a link to the live timer.';
 sl.speakerNotes.textFrame.setText(notes);
}
const candidate=path.join(BUILD,'candidate.pptx');await(await PresentationFile.exportPptx(P)).save(candidate);
const fixed=path.join(BUILD,'candidate-rtl.pptx');execFileSync(process.env.CODEX_PRIMARY_RUNTIME_PYTHON,[path.join(BUILD,'fix_rtl.py'),candidate,fixed]);
const {finalizePresentation}=await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const final=process.env.ESSAY_FINAL_PPTX||path.join(SITE,'files/grammar-in-an-essay.pptx');
await finalizePresentation({workspaceDir:ROOT,candidatePath:fixed,finalPath:final,pythonExecutable:process.env.CODEX_PRIMARY_RUNTIME_PYTHON,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:D.slides.length,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'user_request',families:['Nunito','Heebo']},verifyArtifactToolImport:true,receiptPath:path.join(BUILD,'validation-'+Date.now()+'.json')});
console.log(final);

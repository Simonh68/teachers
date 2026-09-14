import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {pathToFileURL} from 'node:url';
import {Presentation,PresentationFile} from '@oai/artifact-tool';
process.env.RUNTIME_NODE=process.env.CODEX_PRIMARY_RUNTIME_NODE;
process.env.RUNTIME_NODE_MODULES=process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
process.env.RUNTIME_PYTHON=process.env.CODEX_PRIMARY_RUNTIME_PYTHON;
process.env.RUNTIME_BIN_DIR=process.env.CODEX_PRIMARY_RUNTIME+'/dependencies/bin/override';
const ROOT=path.dirname(new URL(import.meta.url).pathname);
const site=path.resolve(ROOT,'../../grade8/monkey-festival');
const workspace=process.env.LESSON_BUILD_ROOT||ROOT;
const build=path.join(workspace,'pptx-build');
await fs.mkdir(build,{recursive:true});
const data=JSON.parse(await fs.readFile(path.join(site,'lesson.json'),'utf8'));
const P=Presentation.create({slideSize:{width:1280,height:720}});
const C={bg:'#07111F',paper:'#F7F7F2',cyan:'#4EE5FF',lime:'#DFFF5B',amber:'#FFC857',muted:'#A9BDD2'};
const he=t=>/[\u0590-\u05ff]/.test(t);
const boxes=[];
function tx(slide,text,x,y,w,h,size,color=C.paper,bold=false,align='center',name='text'){
  if(!text)return;
  const sh=slide.shapes.add({name,geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  sh.text=text.replace(/\d{1,2}:\d{2}[–-]\d{1,2}:\d{2}/g,m=>'\u200e'+m+'\u200e');
  sh.text.style={typeface:he(text)?'Heebo':'Nunito',fontSize:size,bold,color,alignment:align,verticalAlignment:'middle',autoFit:'none',wrap:'square',insets:{left:0,right:0,top:0,bottom:0}};
  boxes.push({slide:data.slides[P.slides.items.length-1]?.n,text,x,y,w,h,size});
  return sh;
}
for(const s of data.slides){
  const slide=P.slides.add();
  slide.background.fill={type:'gradient',gradientKind:'linear',angleDeg:24,stops:[{offset:0,color:'#102A42'},{offset:65000,color:C.bg},{offset:100000,color:'#161B35'}]};
  if(s.kind==='break'){
    slide.images.add({blob:new Uint8Array(await fs.readFile(path.join(site,'assets',s.asset+'.jpg'))),contentType:'image/jpeg',alt:'Humorous fictional monkey illustration',fit:'contain',position:{left:0,top:0,width:1280,height:720}});
  }else{
    const label=s.label||(s.kind==='reading'?s.title:'כיתה ח׳ · הכנה למבחן');
    tx(slide,label,90,52,1100,34,22,s.kind==='reading'?C.lime:C.cyan,true);
    if(s.tense)tx(slide,s.tense,90,90,1100,28,19,C.amber,true);
    if(s.kind==='cover'){
      tx(slide,s.title,80,228,1120,136,100,C.lime,true);
      tx(slide,s.body,80,398,1120,75,42,C.paper,true);
    }else if(s.kind==='vocab'){
      tx(slide,s.title,80,165,1120,110,s.title.length>16?70:88,C.cyan,true);
      tx(slide,s.body,90,295,1100,104,48,C.paper,true);
      tx(slide,s.meaning,90,430,1100,78,49,C.lime,true);
      tx(slide,s.translation,90,520,1100,94,35,C.paper,true);
    }else if(s.kind==='qa'){
      tx(slide,s.title,88,170,1104,180,s.title.length>74?44:50,C.paper,true);
      tx(slide,s.hint,90,365,1100,40,23,C.cyan,false,he(s.hint??'')?'right':'left');
      tx(slide,s.answer,90,427,1100,184,39,C.lime,true,'left');
    }else if(s.kind==='reading'){
      tx(slide,s.body,90,158,1100,440,s.body.length>310?36:40,C.paper,false,'left');
    }else{
      const titleSize=s.title.length>28?52:64;
      tx(slide,s.title,82,134,1116,116,titleSize,C.lime,true);
      let y=272;
      if(s.body){tx(slide,s.body,85,y,1110,76,38,C.paper,true);y+=85;}
      if(s.sub){tx(slide,s.sub,85,y,1110,60,35,C.cyan,true);y+=68;}
      if(s.items){
        const dated=s.n===3;
        const size=dated?30:(s.items.some(t=>t.length>60)?28:33);
        for(const item of s.items){tx(slide,item,90,y,1100,dated?82:57,size,C.paper,false);y+=dated?92:63;}
      }
      if(s.hint)tx(slide,s.hint,90,Math.max(y+5,545),1100,s.n===3?67:75,s.n===3?24:25,C.muted,false);
      if(s.links){
        const sh=tx(slide,s.links[0].label,90,625,1100,30,22,C.cyan,true);
        if(sh)sh.text.get(s.links[0].label).link={uri:s.links[0].href.startsWith('http')?s.links[0].href:'https://simonh68.github.io/teachers/grade8/monkey-festival/'+s.links[0].href,isExternal:true};
      }
    }
    tx(slide,String(s.n)+' / 70',1120,677,90,20,16,C.muted);
  }
  let notes=s.notes||'';
  if(s.source)notes+='\nSource: '+s.source;
  if(s.kind==='break')notes+='\nOriginal generated illustration for this lesson.';
  slide.speakerNotes.textFrame.setText(notes);
}
const exported=path.join(build,'candidate.pptx');
await (await PresentationFile.exportPptx(P)).save(exported);
const candidate=path.join(build,'candidate-rtl.pptx');
execFileSync(process.env.CODEX_PRIMARY_RUNTIME_PYTHON,[path.join(ROOT,'fix_rtl.py'),exported,candidate]);
await fs.writeFile(path.join(build,'authored-boxes.json'),JSON.stringify(boxes));
const {finalizePresentation}=await import(pathToFileURL('/root/.codex/skills/builtins/presentations/container_tools/artifact_tool_utils.mjs').href);
const FINAL=process.env.FINAL_PPTX||path.join(site,'files/monkey-festival.pptx');
await fs.mkdir(path.dirname(FINAL),{recursive:true});
await finalizePresentation({workspaceDir:workspace,candidatePath:candidate,finalPath:FINAL,pythonExecutable:process.env.CODEX_PRIMARY_RUNTIME_PYTHON,integrityValidatorPath:'/root/.codex/skills/builtins/presentations/container_tools/inspect_presentation_package_integrity.py',layoutValidatorPath:'/root/.codex/skills/builtins/presentations/container_tools/inspect_presentation_layout_geometry.py',layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],explicitTotalSlideCount:70,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[],fontPolicy:{basis:'user_request',families:['Nunito','Heebo']},verifyArtifactToolImport:true,receiptPath:path.join(build,'validation.json')});
console.log(FINAL);

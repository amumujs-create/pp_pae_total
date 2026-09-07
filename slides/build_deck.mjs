import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const SKILL_DIR = '/Users/baghyeongbae/.codex/plugins/cache/openai-primary-runtime/presentations/26.905.11957/skills/presentations';
const workspaceDir = '/Users/baghyeongbae/Desktop/연구/pp_pae_total';
const TMP_DIR = path.join(workspaceDir, '.build_ppt');
const FINAL_PPTX = path.join(workspaceDir, 'output', 'PP_PAE_Assumption_Aware_Extrapolation_v3.pptx');
const RUNTIME_PYTHON = '/Users/baghyeongbae/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';
const { resolvePresentationFont, finalizePresentation } = await import(pathToFileURL(path.join(SKILL_DIR, 'container_tools/artifact_tool_utils.mjs')).href);
const font = resolvePresentationFont({fontFamily:'AppleGothic'});
const P = Presentation.create({slideSize:{width:1280,height:720}});

const C={navy:'#1F2937', blue:'#334E68', teal:'#1F7A8C', orange:'#F4A261', pale:'#F5F7FA', mid:'#9AA5B1', ink:'#101828', gray:'#667085', white:'#FFFFFF', green:'#2D7D46', red:'#C2413B'};
function rect(slide,x,y,w,h,fill='none',line='none',radius=false){
  return slide.shapes.add({geometry:radius?'roundRect':'rect',position:{left:x,top:y,width:w,height:h},fill:fill==='none'?'none':{color:fill},line:line==='none'?{fill:'none',width:0}:{fill:line,width:1}});
}
function text(slide,txt,x,y,w,h,size=20,color=C.ink,bold=false,align='left'){
  const s=slide.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  s.text=txt;
  s.text.style={typeface:font,fontSize:size,color,bold,align,autoFit:'shrinkText'};
  return s;
}
function rule(slide,y=0){ rect(slide,0,y,1280,5,C.navy); }
function footer(slide,n){ text(slide,'Smart Production Systems Lab.   |   Assumption-Aware Extrapolation',72,684,700,18,10,C.gray); text(slide,String(n).padStart(2,'0'),1165,681,45,20,11,C.gray,true,'right'); }
function sectionTitle(slide,no,title,sub=''){
  rule(slide); rect(slide,72,56,6,52,C.navy); text(slide,no,92,50,55,30,20,C.navy,true); text(slide,title,150,49,980,44,31,C.ink,true); if(sub) text(slide,sub,151,98,920,25,14,C.gray); }
function bullet(slide,txt,x,y,w,size=19,color=C.ink){ text(slide,'•',x,y,w?18:18,27,size,C.navy,true); return text(slide,txt,x+24,y,w-24,34,size,color,false); }
function note(slide,txt){ slide.speakerNotes.textFrame.setText(txt); }
function arrow(slide,x,y,w,h,fill=C.navy){ return slide.shapes.add({geometry:'rightArrow',position:{left:x,top:y,width:w,height:h},fill:{color:fill},line:{fill:fill,width:0}}); }
function box(slide,label,sub,x,y,w,h,accent=C.navy){
  rect(slide,x,y,w,h,C.white,accent,true); rect(slide,x,y,8,h,accent,accent,true); text(slide,label,x+24,y+16,w-38,30,21,C.ink,true); if(sub) text(slide,sub,x+24,y+51,w-38,h-58,14,C.gray,false);
}

// 1
{const s=P.slides.add(); s.background.fill=C.white; rule(s); text(s,'Assumption-Aware\nExtrapolation',72,186,700,140,46,C.ink,true); text(s,'PP와 PAE를 연결하는 외삽 연구 프레임워크',76,350,680,34,22,C.blue); rect(s,76,415,88,6,C.orange); text(s,'Smart Production Systems Lab.\n박사과정 연구 프로그램 초안',76,455,380,58,16,C.gray); text(s,'2026',1100,625,100,24,16,C.gray,true,'right'); note(s,'Draft prepared from the PP research documents, PAE planning documents, and the supplied lab seminar formatting references.');}
// 2
{const s=P.slides.add(); s.background.fill=C.white; rule(s); text(s,'INDEX',74,62,250,44,32,C.ink,true); const rows=[['01','문제와 연구 모티베이션'],['02','가정 인지형 외삽 프레임워크'],['03','현재 단계: PP'],['04','후속 단계: PAE와 박사과정 로드맵']]; rows.forEach((r,i)=>{const y=156+i*92;text(s,r[0],120,y,70,28,20,C.navy,true);text(s,r[1],220,y,650,28,23,C.ink);rect(s,220,y+40,760,1,C.mid);}); footer(s,2); note(s,'Structure follows the supplied seminar decks: title, index, numbered sections, and concise diagrams.');}
// 3
{const s=P.slides.add(); s.background.fill=C.white; sectionTitle(s,'01','문제와 연구 모티베이션','RUL·열화·균열·용량 예측에서 외삽이 필요한 이유'); text(s,'배포 환경은 학습 데이터의 끝을 넘어선다',74,150,760,38,26,C.ink,true); const xs=[90,430,770]; const heads=['시간 끝단','새로운 개체·엔진','새 운전 조건·regime']; const subs=['관측한 사이클 이후의 RUL','학습에 없던 unit 또는 machine','support 밖의 상태 조합']; xs.forEach((x,i)=>{rect(s,x,230,250,200,C.pale,'none',true);text(s,heads[i],x+22,258,205,30,20,C.navy,true);text(s,subs[i],x+22,312,205,60,16,C.gray);rect(s,x+22,390,200,4,i===0?C.orange:(i===1?C.teal:C.blue));}); text(s,'평균 점수보다 “어떤 가정으로 미래를 연장했는가”가 외삽의 핵심이다.',75,520,1080,38,24,C.ink,true); footer(s,3); note(s,'Motivation: strict extrapolation is defined by temporal, unit, or condition support shifts.');}
// 4
{const s=P.slides.add(); s.background.fill=C.white; sectionTitle(s,'01','외삽의 핵심 질문','데이터 밖의 함수를 무엇으로 정당화할 것인가'); text(s,'학습 support 밖에서는 데이터만으로 함수가 정해지지 않는다.',74,155,1040,42,28,C.ink,true); rect(s,90,255,450,185,C.pale,'none',true); text(s,'일반 NN',120,282,190,30,22,C.navy,true); text(s,'유연한 residual은 support 밖에서도\n임의의 형태로 연장될 수 있다.',120,335,350,62,18,C.gray); rect(s,735,255,450,185,C.pale,'none',true); text(s,'강한 물리·수식 prior',765,282,300,30,22,C.navy,true); text(s,'식이 틀리거나 regime가 바뀌면\n강한 편향이 생길 수 있다.',765,335,350,62,18,C.gray); arrow(s,574,315,95,55,C.orange); text(s,'연구 목표',448,495,390,32,25,C.ink,true,'center'); text(s,'관측으로 정당화되는 수준의 prior만 사용하고, 근거가 부족하면 축소하거나 보류한다.',185,542,910,36,20,C.blue,false,'center'); footer(s,4); note(s,'Literature framing: the extrapolation problem needs explicit assumptions; strong physics constraints are not automatically reliable under misspecification or regime change.');}
// 5
{const s=P.slides.add(); s.background.fill=C.white; sectionTitle(s,'02','가정 인지형 외삽','Compile → Execute → Assure'); const items=[['Compile','PAE','관측 계약에서\n허용 prior를 결정'],['Execute','PP','약한 prior를\nNN residual과 안전하게 결합'],['Assure','공통 보증','거리·오차·불확실성으로\n예측 또는 보류']]; items.forEach((it,i)=>{const x=95+i*370; rect(s,x,210,300,225,C.white,C.navy,true);rect(s,x,210,300,49,i===0?C.orange:(i===1?C.teal:C.blue),'none',true);text(s,it[0],x+20,220,180,28,22,C.white,true);text(s,it[1],x+22,285,240,28,23,C.ink,true);text(s,it[2],x+22,335,250,64,17,C.gray); if(i<2) arrow(s,x+310,285,44,38,C.mid);}); text(s,'프레임워크의 목표는 범용 식을 찾는 것이 아니라, prior의 강도를 관측 정보와 맞추는 것이다.',92,525,1080,40,23,C.ink,true); footer(s,5); note(s,'Research program overview. PP is the executor for an admissible weak prior; PAE is a future compiler and router.');}
// 6
{const s=P.slides.add(); s.background.fill=C.white; sectionTitle(s,'02','Prior ladder','수식은 가장 강한 prior일 뿐이다'); const data=[['0','구조 지식 없음','prior-off NN + UQ/보류'],['1','경계·범위·이력·거리','PP'],['2','방향·순서·부분 구조','제약형 예측기'],['3','관계식·보존식·동역학','물리/식 residual hybrid']]; data.forEach((r,i)=>{const y=150+i*105;rect(s,90,y,90,78,i===0?C.gray:(i===1?C.teal:(i===2?C.blue:C.orange)),'none',true);text(s,r[0],117,y+20,34,30,24,C.white,true,'center');text(s,r[1],220,y+13,370,30,21,C.ink,true);text(s,r[2],660,y+14,390,30,20,C.blue);rect(s,220,y+57,830,1,C.mid);}); text(s,'PAE의 안전장치: 근거 없는 도메인에서 식을 발명하지 않고 prior-off 경로로 보낸다.',94,590,1060,35,20,C.ink,true); footer(s,6); note(s,'Prior ladder and executor mapping. This is a planned framework contract, not a claim that every executor has been implemented.');}
// 7
{const s=P.slides.add(); s.background.fill=C.white; sectionTitle(s,'02','전체 프레임워크','관측 계약에서 예측과 보류까지'); box(s,'관측 계약','입력, 시간 순서, 경계, 메타데이터,\n알려진 방향·식, deployment shift',82,195,270,122,C.navy); arrow(s,365,235,58,36,C.mid); box(s,'PAE prior compiler','허용 prior를 선택하고\nstrong / weak / off 경로를 결정',435,195,270,122,C.orange); arrow(s,720,235,58,36,C.mid); box(s,'Executor','PP · constrained model ·\nphysics hybrid · prior-off model',790,195,300,122,C.teal); arrow(s,934,340,35,44,C.mid); box(s,'Assurance','support 거리, validation 오차, 불확실성, coverage\n→ predict / report confidence / abstain',420,425,455,116,C.blue); text(s,'현재 구현 범위',95,590,220,24,17,C.gray,true); text(s,'PP executor와 PP-specific geometry·validation 검증',320,590,700,25,18,C.ink); footer(s,7); note(s,'Framework diagram. Assurance is PP-specific today; a cross-executor assurance interface remains a future dissertation objective.');}
// 8
{const s=P.slides.add(); s.background.fill=C.white; sectionTitle(s,'03','현재 단계: PP','첫 번째 독립 논문으로서의 연구 질문'); text(s,'주어진 약한 prior를 NN residual이 외삽 구간에서 망가뜨리지 않게 할 수 있는가?',76,155,1080,42,26,C.ink,true); const a=[['입력 prior','EOL 경계, 양수성, 이력,\n약한 affine tail, support 거리'],['핵심 구조','frozen tail + bounded\ndual-scale history residual'],['출력 검증','pooled R², unit coverage,\nsupport shell, seed robustness']]; a.forEach((it,i)=>{box(s,it[0],it[1],100+i*360,258,300,155,[C.orange,C.teal,C.blue][i]);}); text(s,'PP는 prior를 자동 발견하는 방법이 아니라, 선언된 약한 prior를 안전하게 실행하는 방법이다.',76,540,1080,34,21,C.blue,true); footer(s,8); note(s,'PP paper boundary: fixed admissible weak prior, strict out-of-support RUL extrapolation, support-adaptive bounded residual execution.');}
// 9
{const s=P.slides.add(); s.background.fill=C.white; sectionTitle(s,'03','PP 구조','Affine tail을 보존하며 residual의 외삽 영향 범위를 제어'); text(s,'ŷ = m · softplus( ℓ(z) + cθ(z) )',105,165,1000,46,31,C.ink,true,'center'); box(s,'ℓ(z): frozen affine tail','외삽 방향의 기본 경향을 고정',105,285,300,115,C.orange); arrow(s,422,325,62,34,C.mid); box(s,'cθ(z): history residual','학습 support 안의 세밀한 보정',500,285,300,115,C.teal); arrow(s,817,325,62,34,C.mid); box(s,'m: boundary margin','EOL 경계와 residual envelope를 보존',895,285,300,115,C.blue); text(s,'support에서 멀어질수록 residual은 작은 포화 규모에서 큰 포화 규모로 전환한다.',120,477,1030,32,22,C.ink,true,'center'); text(s,'목적: 내부 구간의 표현력과 외삽 구간의 안정성을 같은 구조 안에서 분리한다.',160,535,960,28,18,C.gray,false,'center'); footer(s,9); note(s,'PP architecture: frozen affine tail, boundary margin, bounded dual-scale residual, and support-adaptive saturation.');}
// 10
{const s=P.slides.add(); s.background.fill=C.white; sectionTitle(s,'03','PP 현재 근거','엄격 외삽에서 평균 성능과 최악 case를 함께 본다'); const vals=[['Sunwoda','0.934'],['RWTH','0.842'],['MICH','0.751']]; vals.forEach((v,i)=>{const x=105+i*350;rect(s,x,202,270,185,C.pale,'none',true);text(s,v[0],x+20,232,230,28,21,C.navy,true,'center');text(s,v[1],x+20,285,230,58,39,[C.teal,C.blue,C.orange][i],true,'center');text(s,'pooled R², 5-seed mean',x+20,350,230,24,13,C.gray,false,'center');}); text(s,'추가 확인',92,457,190,28,20,C.ink,true); bullet(s,'MICH 8개 unit 모두 pooled R² > 0',110,500,480,18); bullet(s,'17,645개 예측에서 boundary/residual bound 위반 0건',620,500,560,18); text(s,'해석: PP는 현 개발 데이터에서 안정적 후보가 되었으며, 논문에서는 고정 후 독립 cohort 검증을 별도 증거로 둔다.',92,593,1080,35,18,C.gray); footer(s,10); note(s,'Source: PP final robust adaptive dual-scale replay results. Values are pooled R² 5-seed means: Sunwoda 0.934, RWTH 0.842, MICH 0.751. Evidence remains retrospective development evidence until independently frozen and tested.');}
// 11
{const s=P.slides.add(); s.background.fill=C.white; sectionTitle(s,'04','후속 단계: PAE','관측 계약 기반 prior compilation과 안전한 prior-off routing'); text(s,'PAE의 질문: 무엇을 알고 있을 때, 어느 정도의 prior를 허용할 수 있는가?',76,155,1100,40,26,C.ink,true); const cols=[['Correct prior','정당한 prior가 있을 때\n성능과 안정성을 높이는가'],['Wrong prior','틀린 prior가 손해를\n만드는지를 보이는가'],['Prior-off / PAE route','근거가 부족하면 약한 경로 또는\nprior-off로 돌아가 손해를 제한하는가']]; cols.forEach((it,i)=>{box(s,it[0],it[1],80+i*385,265,i===2?340:300,165,[C.green,C.red,C.blue][i]);}); text(s,'PAE의 노벨티는 “자동 식 발견”이 아니라, 관측으로 허용되는 prior의 범위를 명시하고 선택 오류를 관리하는 데 있다.',76,560,1100,37,19,C.blue,true); footer(s,11); note(s,'PAE research plan: typed observation contract, admissible-prior compilation, and routing between correct/wrong/off prior conditions.');}
// 12
{const s=P.slides.add(); s.background.fill=C.white; sectionTitle(s,'04','박사과정 연구 로드맵','PP를 출발점으로 prior의 적용 범위와 assurance를 확장'); const steps=[['현재','PP 논문','약한 prior executor\n엄격 RUL 외삽'],['다음','PAE 논문','typed contract와\nprior routing'],['통합','박사논문','compile, execute, assure\n교차 도메인 검증']]; steps.forEach((it,i)=>{const x=100+i*370;rect(s,x,245,280,145,C.white,[C.teal,C.orange,C.blue][i],true);text(s,it[0],x+20,267,100,24,15,C.gray,true);text(s,it[1],x+20,300,220,30,23,C.ink,true);text(s,it[2],x+20,342,230,46,16,C.gray); if(i<2)arrow(s,x+290,300,55,40,C.mid);}); text(s,'각 단계는 독립 논문으로 성립하고, 통합 논문은 prior의 선택부터 안전한 실행과 적용 범위 보고까지 연결한다.',93,500,1090,44,22,C.ink,true,'center'); footer(s,12); note(s,'Dissertation story: PP first, PAE second, integrated assumption-aware extrapolation research program third.');}
// 13
{const s=P.slides.add(); s.background.fill=C.white; rule(s); text(s,'Discussion',72,170,800,60,46,C.ink,true); text(s,'수정이 필요한 지점',76,295,300,30,21,C.navy,true); bullet(s,'PAE의 관측 계약에서 실제로 허용할 prior 범위',95,345,850,20); bullet(s,'PP 논문의 중심 데이터셋과 고정할 외삽 protocol',95,398,850,20); bullet(s,'박사논문에서 추가할 domain과 assurance 실험의 범위',95,451,850,20); text(s,'Thank you',76,590,400,42,30,C.gray); text(s,'Smart Production Systems Lab.',76,642,430,24,15,C.gray); note(s,'Closing discussion slide. Intended for iterative revision of the research story.');}

await fs.mkdir(TMP_DIR,{recursive:true});
const candidatePath=path.join(TMP_DIR,'candidate_pp_pae_v3.pptx');
await (await PresentationFile.exportPptx(P)).save(candidatePath);
const requirements={explicitTotalSlideCount:13,requiredNativeTableOwnerSlides:[],requiredNativeChartOwnerSlides:[]};
const fontPolicy={basis:'design',families:[font]};
const result=await finalizePresentation({
  ...requirements,workspaceDir,candidatePath,finalPath:FINAL_PPTX,pythonExecutable:RUNTIME_PYTHON,
  integrityValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(SKILL_DIR,'container_tools/inspect_presentation_layout_geometry.py'),
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit'],
  requiredNativeTableOwnerSlides:[],fontPolicy,verifyArtifactToolImport:true,
  receiptPath:path.join(TMP_DIR,'validation_pp_pae_v3.json')
});
console.log(JSON.stringify({candidatePath,FINAL_PPTX,result},null,2));

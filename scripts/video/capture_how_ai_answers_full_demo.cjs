// Capture the lesson's two-panel guided demonstration, including its blue shell.
const fs=require('node:fs'),path=require('node:path'),http=require('node:http');
const assert=require('node:assert/strict');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'../..');
const out=path.resolve(root,process.argv[2]||'video-audit/how-ai-answers-layout-v20-2026-11-10');
let html=fs.readFileSync(path.join(root,'previews/how-ai-answers.html'),'utf8');
const before="return E(AnswerBuildScene,{state:ANSWER_BUILD_STATES[step],step:step});";
assert.ok(html.includes(before));
html=html.replace(before,`var state=ANSWER_BUILD_STATES[step];return E(GuidedDemoShell,{
 label:'Build an answer one token at a time',kind:'answer',
 instructions:answerInstruction(state.instruction),
 instructionOptions:ANSWER_BUILD_STATES.map(s=>answerInstruction(s.instruction)),
 beforeInstructions:E(AnswerBuildContext,{state:state}),
 controls:E(GuidedDemoControls,{done:false,actionLabel:step===0?'Start Response':'Continue'})
 },E(AnswerBuildScene,{state:state,step:step,hideContext:true}));`);
html=html.replace('</style>',`\n.capture .guided-demo{width:1080px;margin:0;flex-shrink:0;transform-origin:center}
.capture .answer-build-scene{width:auto}.capture .answer-build-token{animation:none}
</style>`);
const names=['first-prediction','you-selected','name-prediction','spot-selected'];
(async()=>{
 fs.mkdirSync(out,{recursive:true});const server=http.createServer((req,res)=>{res.setHeader('Content-Type','text/html');res.end(html);});
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));let browser;
 try{
  browser=await chromium.launch({channel:'chrome',headless:true});const page=await browser.newPage({viewport:{width:1280,height:720}});
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}/?capture=1&step=0`,{waitUntil:'networkidle'});
  await page.evaluate(()=>document.fonts.ready);
  const height=await page.locator('.guided-demo').evaluate(e=>e.getBoundingClientRect().height);
  const scale=Math.min(1.1,680/height,1200/1080);
  await page.addStyleTag({content:`.capture .guided-demo{transform:scale(${scale})}`});
  const meta={scale,source:'index.html components, via existing lesson preview',states:{}};
  for(let step=0;step<4;step++){
   await page.evaluate(n=>window.setAnswerScene(n),step);
   await page.locator(`.answer-build-scene[data-step="${step}"]`).waitFor();
   const geometry=await page.locator('.guided-demo').evaluate(e=>{
    const rect=n=>{const r=n.getBoundingClientRect();return [r.left,r.top,r.right,r.bottom]};
    return {shell:rect(e),background:getComputedStyle(e).backgroundColor,
     panels:[rect(e.querySelector('.guided-demo-instructions')),rect(e.querySelector('.guided-demo-panel'))],
     rows:[...e.querySelectorAll('.answer-build-option')].map(rect),other:rect(e.querySelector('.answer-build-other')),
     reply:rect(e.querySelector('.answer-build-reply')),
     token:(()=>{const token=e.querySelector('.answer-build-token');if(!token)return null;const range=document.createRange();range.selectNodeContents(token);return rect(range)})()};
   });
   assert.ok(geometry.shell[0]>=0&&geometry.shell[1]>=0&&geometry.shell[2]<=1280&&geometry.shell[3]<=720);
   await page.screenshot({path:path.join(out,`${names[step]}.png`)});meta.states[names[step]]=geometry;
  }
  assert.deepEqual(errors,[]);fs.writeFileSync(path.join(out,'capture.json'),JSON.stringify(meta,null,2));console.log(JSON.stringify(meta));
 }finally{if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(e=>{console.error(e);process.exitCode=1});

// Capture the actual lesson scene; only delivery framing/type scale is adapted.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
const root = path.resolve(__dirname, '../..');
const out = path.join(root, 'video-audit/how-ai-answers-guided-2026-10-06-v12');
(async () => {
  fs.mkdirSync(path.join(out, 'states'), {recursive:true});
  const browser = await chromium.launch({channel:'chrome',headless:true});
  const page = await browser.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1});
  const errors=[]; page.on('pageerror', e=>errors.push(String(e)));
  await page.goto('http://127.0.0.1:8765/previews/how-ai-answers.html?capture=1&step=0');
  await page.waitForFunction(()=>typeof window.setAnswerScene==='function');
  await page.addStyleTag({content:`
    @font-face{font-family:VideoJakarta;src:url('/scripts/video/assets/fonts/PlusJakartaSans-wght.ttf') format('truetype');font-weight:100 900}
    body{margin:0;background:#fff;font-family:VideoJakarta,sans-serif}
    .capture{position:relative;align-items:flex-start;padding-top:148px;box-sizing:border-box}
    .capture .answer-build-scene{width:648px;padding:24px;box-sizing:border-box;transform:scale(1.25);transform-origin:top center;font-family:VideoJakarta,sans-serif}
    .capture .answer-build-option.is-selected{border-width:3.2px;padding:5.8px 11.8px}
    .video-question{position:absolute;left:265px;top:40px;margin:0;font:600 27px/1.5 VideoJakarta,sans-serif;color:#171327}
    .video-question span{display:block;margin-bottom:5px;font-size:16px;font-weight:500;color:#69647a}
  `});
  await page.evaluate(()=>{
    const p=document.createElement('p');p.className='video-question';
    const label=document.createElement('span');label.textContent='Your question';p.append(label,document.createTextNode('What should I name my new dog?'));
    document.querySelector('main').append(p);
  });
  await page.evaluate(()=>document.fonts.ready);
  const metadata=[];
  for(let step=0;step<15;step++){
    await page.evaluate(n=>window.setAnswerScene(n),step);
    await page.waitForFunction(n=>document.querySelector('.answer-build-scene').dataset.step===String(n),step);
    await page.screenshot({path:path.join(out,'states',`state-${step}.png`)});
    metadata.push(await page.evaluate(()=>{
      const scene=document.querySelector('.answer-build-scene');
      const rect=scene.getBoundingClientRect();
      return {step:Number(scene.dataset.step),reply:scene.querySelector('.answer-build-reply > div:last-child').textContent,
        selected:scene.querySelector('.is-selected .answer-build-option-name')?.textContent||null,
        options:ANSWER_BUILD_STATES[Number(scene.dataset.step)].options,
        rect:{x:rect.x,y:rect.y,width:rect.width,height:rect.height},font:document.fonts.check('17px VideoJakarta')};
    }));
  }
  if(errors.length)throw new Error(errors.join('\n'));
  if(metadata.some(m=>!m.font||m.rect.y+m.rect.height>720))throw new Error('Font or frame overflow');
  fs.writeFileSync(path.join(out,'scene-metadata.json'),JSON.stringify(metadata,null,2)+'\n');
  await browser.close();console.log('Captured 15 shared scene states.');
})().catch(e=>{console.error(e);process.exit(1)});

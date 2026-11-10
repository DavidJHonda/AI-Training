// Browser verification of the five-moment lesson, shared shell, and capture surface.
// NODE_PATH=<runtime>/node_modules node scripts/test_how_ai_answers.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
const base = process.env.BASE_URL || 'http://127.0.0.1:8765';
const output = path.resolve(__dirname, '../output/how-ai-answers-guided');
(async () => {
  const browser = await chromium.launch({channel:'chrome',headless:true});
  try {
    const page = await browser.newPage({viewport:{width:1280,height:1100}});
    const errors = [];
    page.on('pageerror', e => { errors.push(e.message); console.error(e.message); });
    await page.route(/script\.google|script\.googleusercontent|\.mp4/,route=>route.abort());
    await page.addInitScript(() => {
      localStorage.setItem('llm-user-name','Preview');
      localStorage.setItem('llm-explorer-progress',JSON.stringify({activeSection:'prediction',visited:['prediction'],completed:[]}));
    });
    await page.goto(base+'/index.html',{waitUntil:'domcontentloaded'});
    await page.getByRole('button',{name:'Read the lesson',exact:true}).click();
    const demo = page.locator('.guided-demo[data-kind="answer"]');
    await demo.waitFor();
    await page.evaluate(() => document.fonts.ready);
    await page.clock.install();
    await page.clock.pauseAt(new Date());
    await page.addStyleTag({content:'.sticky-lesson-bar{visibility:hidden!important}'});
    fs.mkdirSync(output,{recursive:true});
    const reply = () => demo.locator('.answer-build-reply > div:not([aria-hidden])').innerText();
    const next = () => demo.getByRole('button',{name:/^(Start Response|Continue)$/});
    const advance = async () => { await next().focus(); await page.keyboard.press('Enter'); };
    const tick = async ms => { await page.clock.runFor(ms); };
    const selection = () => demo.locator('.answer-build-option.is-selected .answer-build-option-name').allTextContents();
    const chart = () => demo.locator('.answer-build-chart').isVisible();
    for (const width of [1280,540,390,350,320]) {
      await page.setViewportSize({width,height:1100});
      const geometry=[];
      const check = async step => {
        if(step<4) assert.equal(await demo.locator('.answer-build-scene').getAttribute('data-step'),String(step));
        else assert.equal(await demo.locator('.guided-demo-panel').count(),0,'Completed answer removes the bottom white box');
        assert.equal(await demo.evaluate(n => n.scrollWidth <= n.clientWidth && n.getBoundingClientRect().right <= innerWidth),true,`No overflow at ${width}, moment ${step}`);
        geometry.push(await demo.evaluate(n=>{
          const base=n.getBoundingClientRect(), controls=n.querySelector('.guided-demo-controls').getBoundingClientRect(), scene=n.querySelector('.answer-build-scene')?.getBoundingClientRect();
          return {controls:controls.top-base.top,top:scene?scene.top-base.top:null,height:scene?scene.height:0};
        }));
      };
      assert.equal(await reply(),'No tokens yet');
      assert.equal(await next().innerText(),'Start Response');
      assert.equal(await demo.locator('.guided-demo-panel').isVisible(),true,'Replay restores the bottom panel');
      assert.equal(await demo.locator('.answer-build-context').count(),1,'Question and reply appear only once');
      assert.deepEqual(await demo.locator('.answer-build-speaker').allTextContents(),['You','AI’s Answer']);
      assert.equal(await demo.getByText('Reply so far',{exact:true}).count(),0);
      assert.equal(await demo.evaluate(n=>{
        const question=n.querySelector('.answer-build-question').getBoundingClientRect();
        const reply=n.querySelector('.answer-build-reply').getBoundingClientRect();
        const controls=n.querySelector('.guided-demo-controls').getBoundingClientRect();
        const instruction=n.querySelector('.guided-demo-instruction-text').getBoundingClientRect();
        const labels=Array.from(n.querySelectorAll('.answer-build-speaker'),el=>el.getBoundingClientRect());
        return labels[0].right<=question.left && labels[1].right<=reply.left && question.bottom<=reply.top && reply.bottom<=instruction.top && instruction.bottom<=controls.top;
      }),true,'Question, growing reply, explanation, and Continue appear in order');
      assert.equal(await chart(),true);
      assert.deepEqual(await selection(),[]);
      assert.equal(await demo.locator('.answer-build-option').count(),3);
      assert.equal(await demo.locator('.answer-build-other').innerText(),'Other tokens: 59%');
      await check(0);
      await advance();
      assert.equal(await reply(),'You');
      assert.equal(await next().innerText(),'Continue');
      assert.deepEqual(await selection(),['You']);
      await check(1);
      await advance();
      assert.equal(await reply(),'You');
      assert.equal(await chart(),false);
      assert.equal(await next().isDisabled(),true);
      for(const text of ['You could','You could name','You could name him']) {
        await tick(700);
        assert.equal(await reply(),text,'Intermediate tokens appear individually');
      }
      assert.equal(await next().isEnabled(),true);
      await check(2);
      assert.equal(await reply(),'You could name him','Dog names appear as soon as him is added');
      assert.deepEqual(await selection(),[]);
      assert.equal(await chart(),true);
      assert.deepEqual(await demo.locator('.answer-build-option-name').allTextContents(),['Spot','Max','Buddy']);
      assert.equal(await demo.locator('.answer-build-other').innerText(),'Other tokens: 47%');
      await demo.screenshot({path:path.join(output,`${width}-compare.png`)});
      await tick(3000);
      assert.equal(await reply(),'You could name him','Selection waits for Continue');
      assert.deepEqual(await selection(),[]);
      await advance();
      assert.equal(await reply(),'You could name him Spot');
      assert.deepEqual(await selection(),['Spot']);
      assert.equal(await next().isEnabled(),true);
      await check(3);
      await demo.screenshot({path:path.join(output,`${width}-selected.png`)});
      await advance();
      assert.equal(await reply(),'You could name him Spot');
      assert.equal(await chart(),false);
      assert.equal(await demo.locator('.answer-build-end').count(),0);
      await tick(650);
      assert.equal(await reply(),'You could name him Spot.');
      assert.equal(await demo.locator('.answer-build-end').count(),0,'Period alone does not end the response');
      assert.equal(await demo.locator('.guided-demo-panel').isVisible(),true,'Panel stays until the answer is complete');
      await tick(950);
      assert.equal(await demo.locator('.answer-build-end').count(),0,'Completed answer has no End of answer badge');
      assert.equal(await reply(),'You could name him Spot.','Stop token stays outside the reply');
      assert.equal(await demo.getByRole('button',{name:'Replay',exact:true}).isVisible(),true);
      await check(4);
      for(const [index,g] of geometry.entries()) {
        assert.ok(Math.abs(g.controls-geometry[0].controls)<1,`Stable controls at ${width}`);
        if(index<4) assert.ok(Math.abs(g.top-geometry[0].top)<1,`Stable scene top at ${width}`);
        if(index<4) assert.ok(Math.abs(g.height-geometry[0].height)<1,`Stable scene height at ${width}`);
        else assert.ok(g.height<geometry[0].height,`Completed scene removes the empty chart space at ${width}`);
      }
      assert.equal(await demo.getByRole('button',{name:'Replay'}).evaluate(n=>n===document.activeElement),true);
      await demo.screenshot({path:path.join(output,`${width}-complete.png`)});
      await page.keyboard.press('Enter');
      assert.equal(await next().evaluate(n=>n===document.activeElement),true);
      assert.equal(await reply(),'No tokens yet');
    }
    await page.emulateMedia({reducedMotion:'reduce'});
    await advance();
    assert.equal(await demo.locator('.answer-build-token.is-new').evaluate(n=>getComputedStyle(n).animationName),'none');
    await page.addStyleTag({content:'.guided-demo-instruction-text p{font-size:34px!important}'});
    assert.equal(await demo.locator('.guided-demo-instruction-text').evaluate(n=>n.scrollHeight<=n.clientHeight),true);
    await page.goto(base+'/?print=lesson:prediction',{waitUntil:'domcontentloaded'});
    await demo.waitFor();
    assert.equal(await demo.locator('.answer-build-scene').getAttribute('data-step'),'4');
    assert.equal(await demo.getByRole('button').count(),0);
    assert.equal(await demo.locator('.answer-build-print').isVisible(),true);
    await page.goto(base+'/previews/how-ai-answers.html?capture=1&step=3',{waitUntil:'domcontentloaded'});
    await page.locator('.answer-build-scene[data-step="3"]').waitFor();
    assert.equal(await page.locator('button,.guided-demo-instructions').count(),0);
    assert.equal(await page.locator('.answer-build-option.is-selected .answer-build-option-name').innerText(),'Spot');
    await page.evaluate(()=>window.setAnswerScene(4));
    await page.locator('.answer-build-scene[data-step="4"]').waitFor();
    assert.equal(await page.locator('.answer-build-end').innerText(),'End of answer');
    assert.deepEqual(errors,[]);
    console.log('PASS: five moments, sequential tokens, two charts, selection timing, stop token, five widths, stable layout, keyboard, replay, reduced motion, print and capture.');
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});

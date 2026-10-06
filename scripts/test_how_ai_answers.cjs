// Browser verification of the live lesson, shared shell, and capture surface.
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
    page.on('pageerror', e => errors.push(e.message));
    await page.addInitScript(() => {
      localStorage.setItem('llm-user-name','Preview');
      localStorage.setItem('llm-explorer-progress',JSON.stringify({activeSection:'prediction',visited:['prediction'],completed:[]}));
    });
    await page.goto(base);
    const demo = page.locator('.guided-demo[data-kind="answer"]');
    await demo.waitFor();
    await page.evaluate(() => document.fonts.ready);
    await page.addStyleTag({content:'.sticky-lesson-bar{visibility:hidden!important}'});
    fs.mkdirSync(output,{recursive:true});
    assert.equal(await page.locator('img[src*="how-ai-answers-token-by-token"]').count(),0);
    assert.equal(await page.getByText(/Run the Prediction Loop/).count(),1,'Existing practice stays in the lesson');
    const expected = ['', '', 'You', 'You', 'You could', 'You could', 'You could name', 'You could name', 'You could name him', 'You could name him', 'You could name him Spot', 'You could name him Spot', 'You could name him Spot.', 'You could name him Spot.', 'You could name him Spot.'];
    const selections = {2:'You',4:'could',6:'name',8:'him',10:'Spot',12:'.',14:'End of answer'};
    assert.equal(await demo.getByText('These are illustrative chances for the next token, not live model output.',{exact:false}).count(),0);
    for (const width of [1280,540,390,350,320]) {
      await page.setViewportSize({width,height:1100});
      const geometry=[];
      let previousChart;
      for(let step=0;step<expected.length;step++) {
        if(step>0) { await demo.getByRole('button',{name:'See It',exact:true}).focus(); await page.keyboard.press(step%2?'Enter':'Space'); }
        assert.equal(await demo.locator('.answer-build-scene').getAttribute('data-step'),String(step));
        assert.equal((await demo.locator('.answer-build-reply > div:not([aria-hidden])').innerText()),expected[step] || 'No tokens yet');
        assert.equal(await demo.getByRole('button',{name:'Replay',exact:true}).count(),step===14?1:0);
        assert.equal(await demo.locator('.is-selected').count(),selections[step]?1:0,'Only explicit selection states highlight a token');
        const chart=await demo.locator('.answer-build-option').evaluateAll(rows=>rows.map(row=>[row.querySelector('.answer-build-option-name').firstChild.textContent,row.querySelector('.answer-build-percent').textContent]));
        if(selections[step]) {
          assert.equal(await demo.locator('.is-selected .answer-build-option-name').evaluate(n=>n.firstChild.textContent),selections[step]);
          assert.deepEqual(chart,previousChart,'Selection preserves the displayed probabilities');
          assert.equal(await demo.locator('.is-selected').evaluate(n=>getComputedStyle(n).borderTopWidth),'2px');
          if(step<14) assert.equal(await demo.locator('.answer-build-token.is-new').innerText(),selections[step],'The revealed token immediately joins the reply');
          else assert.equal(await demo.locator('.answer-build-token.is-new').count(),0,'End-of-answer is not added to the reply');
        }
        previousChart=chart;
        if(step>0) {
          assert.equal((await demo.locator('.answer-build-percent').allTextContents()).reduce((sum,x)=>sum+parseInt(x),0),100);
        }
        assert.equal(await demo.evaluate(n => n.scrollWidth <= n.clientWidth && n.getBoundingClientRect().right <= innerWidth),true,`No overflow at ${width}, state ${step}`);
        geometry.push(await demo.evaluate(n=>{
          const base=n.getBoundingClientRect(), controls=n.querySelector('.guided-demo-controls').getBoundingClientRect(), scene=n.querySelector('.answer-build-scene').getBoundingClientRect();
          return {controls:controls.top-base.top,top:scene.top-base.top,height:scene.height};
        }));
        if(step===9) {
          assert.equal(await demo.locator('.answer-build-token').filter({hasText:'Spot'}).count(),0,'Name is a candidate before selection');
          await demo.screenshot({path:path.join(output,`${width}-compare.png`),animations:'disabled'});
        }
        if(step===10) await demo.screenshot({path:path.join(output,`${width}-selected.png`),animations:'disabled'});
      }
      for(const g of geometry) {
        assert.ok(Math.abs(g.controls-geometry[0].controls)<1,`Stable controls at ${width}: ${JSON.stringify(geometry)}`);
        assert.ok(Math.abs(g.top-geometry[0].top)<1,`Stable scene top at ${width}`);
        assert.ok(Math.abs(g.height-geometry[0].height)<1,`Stable scene height at ${width}: ${JSON.stringify(geometry)}`);
      }
      assert.equal(await demo.getByRole('button',{name:'Replay'}).evaluate(n=>n===document.activeElement),true,'Final focus moves to Replay');
      await demo.screenshot({path:path.join(output,`${width}-complete.png`)});
      await page.keyboard.press('Enter');
      assert.equal(await demo.getByRole('button',{name:'See It'}).evaluate(n=>n===document.activeElement),true,'Replay focuses first action');
      assert.equal(await demo.locator('.answer-build-scene').getAttribute('data-step'),'0');
    }
    await page.emulateMedia({reducedMotion:'reduce'});
    await demo.getByRole('button',{name:'See It'}).click();
    await demo.getByRole('button',{name:'See It'}).click();
    assert.equal(await demo.locator('.answer-build-token.is-new').evaluate(n=>getComputedStyle(n).animationName),'none');
    // Text zoom should remeasure the instruction reserve instead of cropping it.
    await page.addStyleTag({content:'.guided-demo-instruction-text p{font-size:34px!important}'});
    assert.equal(await demo.locator('.guided-demo-instruction-text').evaluate(n=>n.scrollHeight<=n.clientHeight),true);
    await page.goto(base+'/?print=lesson:prediction');
    await demo.waitFor();
    assert.equal(await demo.locator('.answer-build-scene').getAttribute('data-step'),'14');
    assert.equal(await demo.getByRole('button').count(),0);
    assert.equal(await demo.locator('.answer-build-print').isVisible(),true);
    await page.emulateMedia({media:'print'});
    assert.equal(await demo.isVisible(),true);
    await page.goto(base+'/previews/how-ai-answers.html?capture=1&step=10');
    await page.locator('.answer-build-scene[data-step="10"]').waitFor();
    assert.equal(await page.locator('button,.guided-demo-instructions').count(),0);
    await page.evaluate(()=>window.setAnswerScene(14));
    await page.locator('.answer-build-scene[data-step="14"]').waitFor();
    assert.deepEqual(errors,[]);
    console.log('PASS: lesson reveals, probabilities, delayed answers, stable layout at five widths, keyboard/focus, replay, reduced motion, text zoom, print, capture and no runtime errors.');
  } finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});

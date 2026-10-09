// Browser verification of the Embeddings guided demonstration.
// NODE_PATH=<runtime>/node_modules node scripts/test_embedding_dimension.cjs
const assert = require('node:assert/strict');
const fs = require('node:fs');
const {chromium} = require('playwright');
const base = process.env.BASE_URL || 'http://127.0.0.1:8765';
const output = '/tmp/embedding-dimension-review';
(async () => {
  const browser = await chromium.launch({channel:'chrome', headless:true});
  try {
    const page = await browser.newPage({viewport:{width:1280,height:1100}});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.addInitScript(() => {
      localStorage.setItem('llm-user-name','Preview');
      localStorage.setItem('llm-explorer-progress',JSON.stringify({activeSection:'embeddings',visited:['embeddings'],completed:[]}));
    });
    await page.goto(base);
    const demo = page.locator('.guided-demo[data-kind="embedding-dimension"]');
    await demo.waitFor();
    await page.evaluate(() => document.fonts.ready);
    await page.addStyleTag({content:'.sticky-lesson-bar{visibility:hidden!important}'});
    fs.mkdirSync(output,{recursive:true});
    assert.equal(await page.locator('img[src*="embeddings-new-dimension"],img[src*="embeddings-meaning-row"]').count(),0);
    assert.equal(await page.getByText('Build Your Own Vector',{exact:true}).count(),1);
    for (const width of [1280,768,540,390,320]) {
      await page.setViewportSize({width,height:1100});
      const geometry = [];
      for (let step=0; step<8; step++) {
        if (step) {
          await demo.getByRole('button',{name:'See It',exact:true}).focus();
          await page.keyboard.press(step===1?'Enter':'Space');
        }
        assert.equal(await demo.locator('.embedding-dimension-scene').getAttribute('data-step'),String(step));
        const table = demo.locator('.embedding-dimension-table:visible');
        const snapshot = await table.ariaSnapshot();
        assert.equal(snapshot.includes('Coke'),step>=2,'Coke appears only after the second action');
        assert.equal(snapshot.includes('Coffee'),step>=1,'Coffee appears only after the first action');
        for (const heading of ['Sweet','Bitter','Fizz','Heat','Caffeine','Dark']) assert.ok(snapshot.toLowerCase().includes(heading.toLowerCase()),'Original headings stay visible');
        assert.equal(snapshot.includes('Pepsi'),step>=4,'Pepsi waits until the learner has compared Coke and Coffee');
        assert.equal(snapshot.includes('Citrus'),step>=6,'Citrus heading appears before its values');
        assert.equal(await table.locator('.is-match').count(),step>=5?12:0);
        assert.equal(await table.locator('.is-answer').count(),step===3?3:0);
        const rows = await demo.locator('.embedding-dimension-desktop tbody tr').evaluateAll(nodes => nodes.filter(n=>n.getAttribute('aria-hidden')!=='true').map(n=>[...n.querySelectorAll('td:not(.is-pending)')].map(c=>c.textContent.trim()===""?null:+c.textContent)));
        const expected = [];
        if(step>=1) expected.push([1,9,0,9,8,10]);
        if(step>=2) expected.push([9,1,10,2,3,8]);
        if(step>=4) expected.push([9,1,10,2,3,8]);
        if(step>=6) [0,1,10].forEach((value,i)=>expected[i].push(step===6?null:value));
        assert.equal(await table.getByLabel("Not rated yet",{exact:true}).count(),step===6?3:0,"New Citrus cells wait for another action");
        assert.deepEqual(rows,expected);
        assert.equal(await demo.evaluate(n=>n.scrollWidth<=n.clientWidth && n.getBoundingClientRect().right<=innerWidth),true);
        geometry.push(await demo.evaluate(n=>{
          const top=n.getBoundingClientRect().top, controls=n.querySelector('.guided-demo-controls').getBoundingClientRect(), scene=n.querySelector('.embedding-dimension-scene').getBoundingClientRect();
          return [controls.top-top,scene.top-top,scene.height];
        }));
        await demo.screenshot({path:`${output}/${width}-step-${step}.png`,animations:'disabled'});
      }
      for (const g of geometry) g.forEach((value,i)=>assert.ok(Math.abs(value-geometry[0][i])<1,`Stable layout at ${width}: ${JSON.stringify(geometry)}`));
      assert.equal(await demo.getByRole('button',{name:'Replay'}).evaluate(n=>n===document.activeElement),true);
      await page.keyboard.press('Enter');
      assert.equal(await demo.getByRole('button',{name:'See It'}).evaluate(n=>n===document.activeElement),true);
    }
    await page.emulateMedia({reducedMotion:'reduce'});
    for(let i=0;i<7;i++) await demo.getByRole('button',{name:'See It'}).click();
    assert.equal(await demo.locator('.is-new').first().evaluate(n=>getComputedStyle(n).animationName),'none');
    await page.addStyleTag({content:'.guided-demo-instruction-text p{font-size:34px!important}'});
    assert.equal(await demo.locator('.guided-demo-instruction-text').evaluate(n=>n.scrollHeight<=n.clientHeight),true);
    await page.goto(base+'/?print=lesson:embeddings');
    await demo.waitFor();
    assert.equal(await demo.locator('.embedding-dimension-scene').getAttribute('data-step'),'7');
    assert.equal(await demo.getByRole('button').count(),0);
    await page.emulateMedia({media:'print'});
    assert.equal(await demo.isVisible(),true);
    await page.goto(base+'/previews/embedding-dimension.html?capture=1&step=7');
    await page.locator('.embedding-dimension-scene[data-step="7"]').waitFor();
    assert.equal(await page.locator('button,.guided-demo-instructions').count(),0);
    await page.evaluate(()=>window.setEmbeddingDimensionScene(0));
    await page.locator('.embedding-dimension-scene[data-step="0"]').waitFor();
    assert.deepEqual(errors,[]);
    console.log('PASS: delayed reveals, original values, stable layout at five widths, keyboard, Replay, reduced motion, text zoom, print, capture, and no runtime errors.');
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});

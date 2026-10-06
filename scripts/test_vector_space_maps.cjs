// Browser checks for the actual lesson. Requires Playwright and a local server.
// NODE_PATH=<runtime>/node_modules node scripts/test_vector_space_maps.cjs
// BASE_URL defaults to http://127.0.0.1:8765.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
const base = process.env.BASE_URL || 'http://127.0.0.1:8765';
const output = path.resolve(__dirname, '../output/vector-space-interactions');
(async () => {
  const browser = await chromium.launch({channel:'chrome', headless:true});
  try {
    const page = await browser.newPage({viewport:{width:1280,height:1100}});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.addInitScript(() => {
      localStorage.setItem('llm-user-name', 'Preview');
      localStorage.setItem('llm-explorer-progress', JSON.stringify({activeSection:'vectorspace',visited:['vectorspace'],completed:[]}));
    });
    await page.goto(base);
    await page.locator('.vs-map-demo').first().waitFor();
    await page.addStyleTag({content:'.sticky-lesson-bar{visibility:hidden!important}'});
    fs.mkdirSync(output,{recursive:true});
    const demos = page.locator('.vs-map-demo');
    assert.equal(await demos.count(),2);
    assert.equal(await page.locator('img[src*="vector-space-meaning-map.jpg"]').count(),1);
    for (const [index,steps] of [[0,7],[1,7]]) {
      const demo=demos.nth(index),frame=demo.locator('.vs-map-frame'),next=demo.getByRole('button').first();
      assert.equal(await frame.getAttribute('data-step'),'0');
      assert.equal(await demo.getByRole('button',{name:'Replay',exact:true}).count(),0);
      if(index===0) assert.equal(await demo.locator('svg text').count(),0,'Map starts empty');
      const mapBox=await demo.locator('.vs-map-svg').boundingBox();
      for(let step=1;step<=steps;step++) {
        // Keyboard activation is part of the student path.
        await next.focus();await page.keyboard.press('Enter');
        assert.equal(await frame.getAttribute('data-step'),String(step));
        assert.equal(await demo.getByRole('button',{name:'Replay',exact:true}).count(),step===steps?1:0,'Replay appears only at completion');
        if(index===0 && step<=3) assert.deepEqual(await demo.locator('svg text').allTextContents().then(names=>names.filter(name=>['Dallas','Mountain View','New York City'].includes(name)).sort()),['Dallas','Mountain View','New York City'].slice(0,step).sort(),'Cities appear one at a time');
        if(index===0 && step===1) assert.equal(await demo.locator('svg circle[fill="none"]').count(),0,'Answer waits for a separate reveal');
        if(index===0 && step===5) assert.equal(await demo.locator('svg circle[fill="none"]').count(),1);
        if(index===1) {
          const names=['Coke','Pepsi','Hot coffee','Mystery A','Mystery B'];
          const revealed=names.filter((_,i)=>step>=[1,2,3,4,6][i]);
          assert.deepEqual(await demo.locator('.vs-map-svg g').evaluateAll(groups=>groups.filter(g=>g.querySelectorAll('text').length===2).map(g=>g.querySelector('text').textContent)),revealed);
          assert.equal(await demo.locator('.vs-map-svg circle[fill="none"]').count(),step>=7?2:step>=5?1:0,'Nearest match waits for its reveal');
          assert.equal(await demo.locator('.vs-map-svg g').evaluateAll(groups=>groups.filter(g=>g.querySelectorAll('text').length===2).every(g=>/^\[.*\]$/.test(g.querySelectorAll('text')[1].textContent))),true,'Every drink has a vector under its name');
        }
      }
      assert.equal(await demo.locator('.vs-map-complete').innerText(),'Complete');
      const afterBox=await demo.locator('.vs-map-svg').boundingBox();
      assert.equal(afterBox.width,mapBox.width);assert.equal(afterBox.height,mapBox.height);
      await page.waitForTimeout(1700);
      await demo.screenshot({path:path.join(output,`desktop-${index}-end.png`)});
      await demo.getByRole('button',{name:'Replay',exact:true}).click();
      assert.equal(await frame.getAttribute('data-step'),'0');
    }
    for(const width of [390,350]) {
      await page.setViewportSize({width,height:1000});
      assert.equal(await demos.evaluateAll(nodes=>nodes.every(n=>n.getBoundingClientRect().right<=innerWidth && n.scrollWidth<=n.clientWidth)),true,`Maps fit at ${width}`);
      for(let i=0;i<2;i++) {
        const demo=demos.nth(i),next=demo.getByRole('button').first();
        while(await demo.locator('.vs-map-complete').count()===0)await next.click();
        await demo.screenshot({path:path.join(output,`mobile-${width}-${i}.png`)});
      }
    }
    await page.goto(base+'/?print=lesson:vectorspace');
    await page.locator('.vs-map-demo').first().waitFor();
    assert.deepEqual(await page.locator('.vs-map-frame').evaluateAll(nodes=>nodes.map(n=>n.dataset.step)),['7','7']);
    assert.equal(await page.locator('.vs-map-controls').count(),0);
    await page.emulateMedia({media:'print'});
    assert.equal(await page.locator('.vs-map-demo').first().isVisible(),true);
    assert.deepEqual(errors,[]);
    console.log('PASS: all reveals, keyboard, replay, stable map size, 390/350px layouts, restored illustration, print, and no runtime errors.');
  } finally { await browser.close(); }
})().catch(error=>{console.error(error);process.exitCode=1;});

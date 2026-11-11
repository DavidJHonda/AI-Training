// Fifth phone-readability batch. Run with the same Playwright NODE_PATH as other browser tests.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.BASE_URL || 'http://127.0.0.1:8796';
const lessons = {
  training: ['trainingSetup','trainingPhases','trainingLoop','pretrainingDetails','instructionDetails','preferenceDetails'],
  embeddings: ['studentIdentity','tasteAndAI'],
  vectorspace: ['contextPosition']
};
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const records = [];
  try {
    for (const [id, kinds] of Object.entries(lessons)) {
      const context = await browser.newContext({ viewport: { width: 390, height: 850 }, hasTouch: true, reducedMotion: 'reduce' });
      await context.route(/script\.google|script\.googleusercontent|\.mp4/, r => r.abort());
      await context.addInitScript(id => {
        localStorage.clear(); localStorage.setItem('llm-user-name', 'Phone Review');
        localStorage.setItem('llm-explorer-progress', JSON.stringify({ activeSection: id, visited: [id], completed: [] }));
      }, id);
      const page = await context.newPage(), errors = [];
      page.on('pageerror', e => errors.push(e.message));
      await page.goto(base + '/index.html', { waitUntil: 'networkidle' });
      const toggle = page.locator('.lesson-reading-toggle');
      if (await toggle.count() && await toggle.getAttribute('aria-expanded') === 'false') await toggle.click();
      await page.evaluate(async () => { await document.fonts.ready; for (const image of document.images) { image.loading = 'eager'; await image.decode().catch(() => {}); } });
      assert.deepEqual(await page.locator('[data-phone-reading-board]').evaluateAll(nodes => nodes.map(n => n.dataset.phoneReadingBoard)), kinds);
      for (const [width, height] of [[320, 850], [390, 850], [430, 850], [760, 850], [761, 850], [844, 390], [1024, 1000], [1280, 1000], [1440, 1000]]) {
        await page.setViewportSize({ width, height });
        const mobile = width <= 760 || height <= 500;
        assert.equal(await page.locator('.phone-reading-mobile:visible').count(), mobile ? kinds.length : 0);
        assert.equal(await page.locator('.phone-reading-desktop img:visible').count(), mobile ? 0 : kinds.length);
        if (mobile) {
          const boards = await page.locator('.phone-reading-mobile').evaluateAll(nodes => nodes.map(n => {
            const r = n.getBoundingClientRect();
            return { title: n.querySelector('h3').textContent, kind: n.parentElement.dataset.phoneReadingBoard, x: r.x, y: r.y + scrollY, width: r.width, height: r.height, text: n.innerText,
              tiny: [...n.querySelectorAll('p,li,h4')].filter(e => parseFloat(getComputedStyle(e).fontSize) < (e.tagName === 'H4' ? 20 : 16)).map(e => e.textContent),
              overflow: [...n.querySelectorAll('*')].filter(e => !(e instanceof SVGElement) && e.clientWidth && e.scrollWidth > e.clientWidth + 1).map(e => e.textContent) };
          }));
          for (const board of boards) { assert.deepEqual(board.tiny, []); assert.deepEqual(board.overflow, []); assert.ok(board.x >= 0 && board.x + board.width <= width); }
          const accessibility = await page.locator('#main-content').ariaSnapshot();
          for (const board of boards) {
            assert.equal(accessibility.split('\n').filter(line => line.includes('heading "' + board.title + '" [level=3]')).length, 1, board.title + ' announced once');
          }
          assert.equal(await page.locator('.phone-reading-desktop-source:visible').count(), 0);
          const geometry = await page.evaluate(() => ({ scrollWidth: document.documentElement.scrollWidth, overflow: [...document.querySelectorAll('body *')].filter(e => !(e instanceof SVGElement) && e.children.length === 0 && e.getBoundingClientRect().width && e.getBoundingClientRect().right > innerWidth + 1).map(e => ({ tag: e.tagName, text: e.textContent.slice(0, 100), right: e.getBoundingClientRect().right })) }));
          records.push({ id, width, height, boards, geometry });
        }
      }
      await page.setViewportSize({ width: 390, height: 850 });
      if (id === 'training') {
        assert.deepEqual(await page.locator('[data-phone-reading-board="trainingPhases"] h4').allTextContents(),['1Pretraining','2Instruction Tuning','3Preference Tuning']);
        const loop=await page.locator('[data-phone-reading-board="trainingLoop"] .phone-reading-mobile').innerText();for(const word of ['Guess','Check','Adjust','cloud','jelly','Adjust → Guess','Repeat with more examples. The patterns build.'])assert.ok(loop.includes(word));
        const pre=await page.locator('[data-phone-reading-board="pretrainingDetails"] .phone-reading-mobile').innerText();assert.ok(pre.includes('1,000 lifetimes'));
        assert.equal(await page.locator('[data-phone-reading-board] .phone-reading-mobile').getByText('What Still Needs Work',{exact:true}).count(),3);
      } else if (id === 'embeddings') {
        const idBoard=page.locator('[data-phone-reading-board="studentIdentity"] .phone-reading-mobile');
        assert.equal(await idBoard.locator('.phone-four-chip, .phone-reading-takeaway, .phone-reading-card').count(),0);
        assert.equal(await idBoard.getByRole('img').count(),1);
        assert.equal(await page.locator('.phone-five-comparison').count(),5);
        const activity=page.locator('.embedding-club-activity');
        const clubs=['Lego Club','AI Club','BBQ Club'],dims=['Tech','Build Things','Messy','Tasty','Career Edge'];
        const values=[[3,10,5,0,4],[10,4,1,0,10],[1,3,10,10,1]];
        const lock=activity.getByRole('button',{name:'Hide the names and match'});
        assert.equal(await lock.isDisabled(),true);
        for(const width of [320,390,430,844]) {
          await page.setViewportSize({width,height:width===844?390:850});
          await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
          assert.equal(await activity.getByRole('textbox').count(),15);
          assert.deepEqual(await activity.locator('.embedding-club-dimension:visible').allTextContents(),[...dims,...dims,...dims]);
          const issues=await activity.evaluate(n=>[...n.querySelectorAll('*')].filter(e=>e.clientWidth&&e.scrollWidth>e.clientWidth+1).map(e=>e.tagName));
          assert.deepEqual(issues,[],'Activity fits at '+width);
          const fields=await activity.locator('input').evaluateAll(ns=>ns.map(n=>({font:parseFloat(getComputedStyle(n).fontSize),height:n.getBoundingClientRect().height})));
          for(const field of fields){assert.ok(field.font>=16);assert.ok(field.height>=44);}
        }
        await page.setViewportSize({width:320,height:850});
        const first=activity.getByRole('textbox',{name:'Lego Club, Tech',exact:true});
        await first.fill('99');assert.equal(await first.inputValue(),'10');await first.fill('x');assert.equal(await first.inputValue(),'');
        for(let ci=0;ci<3;ci++)for(let di=0;di<5;di++)await activity.getByRole('textbox',{name:clubs[ci]+', '+dims[di],exact:true}).fill(String(values[ci][di]));
        assert.equal(await lock.isEnabled(),true);await lock.click();
        await page.waitForFunction(()=>document.activeElement.classList.contains('embedding-club-matches'));
        assert.equal(await activity.getByRole('group',{name:'Mystery clubs',exact:true}).count(),1);
        const matches=activity.locator('.scenario-row-body').locator('..');assert.equal(await matches.count(),3);
        const answers=[];
        for(const row of await matches.all()){
          const text=await row.textContent();const ci=values.findIndex(v=>text.includes(dims.map((d,i)=>d+' '+v[i]).join('  ·  ')));
          assert.ok(ci>=0,'Every mystery keeps the exact five scores');answers.push(ci);
        }
        await matches.nth(0).getByRole('button',{name:clubs[(answers[0]+1)%3],exact:true}).click();assert.match(await matches.nth(0).innerText(),/not quite/i);
        for(let i=0;i<3;i++)await matches.nth(i).getByRole('button',{name:clubs[answers[i]],exact:true}).click();
        assert.ok((await activity.innerText()).includes('The numbers carried the meaning.'));
        for(const width of [320,390,430,844]){
          await page.setViewportSize({width,height:width===844?390:850});
          assert.equal(await activity.evaluate(n=>[...n.querySelectorAll('*')].some(e=>e.clientWidth&&e.scrollWidth>e.clientWidth+1)),false,'Completed activity fits at '+width);
        }
        for(const width of [320,390,430,844]) {
          await page.setViewportSize({width,height:width===844?390:850});
          await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
          const demo=page.locator('.guided-demo[data-kind="embedding-dimension"]');
          for(let step=0;step<8;step++) {
            if(step)await demo.getByRole('button',{name:'See It',exact:true}).click();
            await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
            assert.equal(await demo.locator('.embedding-dimension-scene').getAttribute('data-step'),String(step));
            const table=demo.locator('.embedding-dimension-table:visible');assert.equal(await table.count(),1);
            assert.equal(await table.evaluate(n=>n.scrollWidth<=n.clientWidth),true,'Table fits '+width+'px at step '+step+': '+JSON.stringify(await table.evaluate(n=>({width:n.clientWidth,scroll:n.scrollWidth,display:getComputedStyle(n).display}))));
            assert.equal(await table.locator('th').evaluateAll(ns=>ns.every(n=>parseFloat(getComputedStyle(n).fontSize)>=16)),true);
            const accessible=await table.ariaSnapshot();assert.equal(accessible.includes('Coffee'),step>=1,'Coffee at '+width+' step '+step+': '+accessible);assert.equal(accessible.includes('Coke'),step>=2,'Coke at '+width+' step '+step+': '+accessible);assert.equal(accessible.includes('Pepsi'),step>=4,'Pepsi at '+width+' step '+step+': '+accessible);assert.equal(accessible.includes('Citrus'),step>=6,'Citrus at '+width+' step '+step+': '+accessible);
            assert.equal(await table.getByLabel('Not rated yet',{exact:true}).count(),step===6?3:0);
          }
          assert.deepEqual(await demo.locator('.embedding-dimension-mobile tbody tr:last-child td').allTextContents(),['0','1','10']);
          await demo.getByRole('button',{name:'Replay',exact:true}).click();
        }
      } else {
        const contextBoard=page.locator('[data-phone-reading-board="contextPosition"] .phone-reading-mobile');
        assert.equal(await contextBoard.locator('.phone-reading-card').count(),0);
        assert.equal(await contextBoard.getByRole('img').count(),1);
        assert.equal(await contextBoard.locator('.phone-reading-takeaway').innerText(),'IT’s new position reflects its connection to CAT in this sentence.');
        for(const width of [320,390,430,844]) {
          await page.setViewportSize({width,height:width===844?390:850});
          await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
          for(const [i,kind] of ['cities','drinks'].entries()) {
            const demo=page.locator('.vs-map-demo').nth(i);
            for(let step=0;step<8;step++) {
              if(step)await demo.getByRole('button',{name:'See It',exact:true}).click();
            await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
              const phone=demo.locator('.phone-five-map-mobile');assert.equal(await phone.isVisible(),true);assert.equal(await demo.locator('.phone-five-map-desktop').isVisible(),false);
              const rows=phone.locator('.phone-five-map-key li');const expected=step>=6?5:step>=4?4:step>=3?3:step>=2?2:step>=1?1:0;assert.equal(await rows.count(),expected);
              const overflow=await phone.evaluate(n=>n.scrollWidth>n.clientWidth);assert.equal(overflow,false);
              assert.equal(await phone.locator('svg text').count(),expected);
              const pixelSizes=await phone.locator('svg text').evaluateAll(ns=>ns.map(n=>{const r=n.ownerSVGElement.getBoundingClientRect();return +n.getAttribute('font-size')*r.width/720;}));for(const size of pixelSizes)assert.ok(size>=15.9);
              assert.equal(await phone.locator('svg circle[fill="none"]').count(),step>=7?2:step>=5?1:0);
            }
            const copy=await demo.locator('.phone-five-map-key').innerText();assert.ok(copy.includes(kind==='cities'?'32.78° N, 96.80° W':'[9, 1, 10, 2, 3, 8, 1]'));assert.ok(copy.includes(kind==='cities'?'40° N, 76° W':'[2, 8, 0, 8, 7, 9, 0]'));
            await demo.getByRole('button',{name:'Replay',exact:true}).click();
          }
        }
      }
      await page.emulateMedia({ media: 'print' });
      assert.equal(await page.locator('.phone-reading-mobile:visible').count(), 0);
      assert.equal(await page.locator('.phone-reading-desktop img:visible').count(), kinds.length);
      assert.equal(await page.locator('.phone-five-map-mobile:visible').count(),0);
      assert.deepEqual(errors, []);
      await context.close();
    }
    if (process.env.PHONE_WAVE_OUTPUT) { fs.mkdirSync(process.env.PHONE_WAVE_OUTPUT, { recursive: true }); fs.writeFileSync(path.join(process.env.PHONE_WAVE_OUTPUT, 'phone-checks.json'), JSON.stringify(records, null, 2)); }
    console.log('PASS: nine static boards and three live boards; phone widths/landscape/breakpoints, 16px text/20px headings, accessible alternatives, exact copy/values, reveal order, table comparisons, map keys, answer timing, replay, print, and no runtime errors');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });

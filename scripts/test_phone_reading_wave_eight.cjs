// Eighth phone-readability batch. Run with the same Playwright NODE_PATH as other browser tests.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.BASE_URL || 'http://127.0.0.1:8796';
const lessons = {
  faketrap: ['fakeComparison','fakeMotives','fakeChecks'],
  agents: ['agentsDriving','agentsComparison','agentsLoop','agentsRogue'],
  integrity: ['integritySchool','integrityAllowed','integritySharing','integrityPhoto']
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
        await page.waitForTimeout(250);
        const mobile = width <= 760 || height <= 500;
        assert.equal(await page.locator('.phone-reading-mobile:visible').count(), mobile ? kinds.length : 0);
        assert.equal(await page.locator('.phone-reading-desktop img:visible').count(), mobile ? 0 : kinds.length);
        if(!mobile)assert.equal(await page.locator('.phone-reading-mobile svg').count(),0,'Phone artwork stays unmounted on desktop');
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
      await page.waitForTimeout(250);
      if(id==='faketrap') {
        const comparison=page.locator('[data-phone-reading-board="fakeComparison"] .phone-reading-mobile');
        assert.deepEqual(await comparison.locator('h4').allTextContents(),['THE SCENARIO','Does It Look Real?','Where Is It From?']);
        const text=await comparison.innerText();for(const phrase of ['school is closed next week','BEFORE AI','THE AI ERA','CHECKED','MATCHED','SKIPPED','VERDICT','Real.','Unverified.','The source that would know.','Appearance can mislead. The source trail can be checked.'])assert.ok(text.includes(phrase));
        assert.equal(text.split('VERDICT').length-1,2);
        assert.deepEqual(await page.locator('[data-phone-reading-board="fakeMotives"] h4').allTextContents(),['Money','Power','Fame','Cruelty']);
        assert.ok((await page.locator('[data-phone-reading-board="fakeMotives"] .phone-reading-mobile').innerText()).includes('especially at school.'));
        const checks=page.locator('[data-phone-reading-board="fakeChecks"] .phone-reading-mobile');assert.deepEqual(await checks.locator('h4').allTextContents(),['Source','Context','Corroboration']);
        for(const phrase of ['a reason and a way to know?','What important details are missing?','Can an independent source confirm the same event or claim?','Verify somewhere the sender does not control.'])assert.ok((await checks.innerText()).includes(phrase));
        for(const [pair,letter] of [['The Cat','B'],['The Sculpture','A'],['Venice at Night','B']])await page.getByRole('button',{name:pair+', image '+letter+': choose this photograph',exact:true}).click();
        assert.equal(await page.locator('.fake-photo-choice[aria-disabled="true"]').count(),6);assert.equal(await page.locator('.fake-photo-source').count(),3);assert.ok((await page.locator('.fake-photo-takeaway').innerText()).includes('appearance alone isn’t proof'));
      } else if(id==='agents') {
        const driving=await page.locator('[data-phone-reading-board="agentsDriving"] .phone-reading-mobile').innerText();for(const phrase of ['Waze or Google Maps','you still steer, brake, and catch mistakes','You may not catch a mistake until later.'])assert.ok(driving.includes(phrase));
        const comparison=await page.locator('[data-phone-reading-board="agentsComparison"] .phone-reading-mobile').innerText();for(const phrase of ['30 points','Friday’s basketball game','Review all 50 clips','YOU DO','AI DOES','THE AGENT DOES','YOU STILL OWN','final review, and everything posted under your name.'])assert.ok(comparison.includes(phrase));assert.equal(comparison.split('WHAT CHANGES').length-1,2);
        const loop=page.locator('[data-phone-reading-board="agentsLoop"] .phone-reading-mobile');assert.deepEqual(await loop.locator('h4').allTextContents(),['1Goal','2Plan','3Act','4Check']);
        assert.equal(await loop.locator('.phone-eight-flow-arrow').count(),3);assert.equal(await loop.locator('.phone-eight-loop-stage').count(),3);
        const spine=await loop.locator('.phone-eight-loop-stage, .phone-eight-return').evaluateAll(ns=>ns.map(n=>{const r=n.getBoundingClientRect();return {left:r.left,top:r.top,bottom:r.bottom}}));for(let i=1;i<spine.length;i++){assert.ok(Math.abs(spine[i].left-spine[0].left)<1,'Return spine stays aligned');assert.ok(Math.abs(spine[i].top-spine[i-1].bottom)<1,'Return spine stays connected');}
        const back=loop.getByRole('link',{name:'Not done? Go again. Return from Check to step 2, Plan.',exact:true});assert.equal(await back.getAttribute('href'),'#phone-eight-agent-plan');await back.click();assert.equal(await page.evaluate(()=>document.activeElement.textContent),'2Plan');assert.ok(await page.locator('#phone-eight-agent-plan').evaluate(n=>n.getBoundingClientRect().top>=0&&n.getBoundingClientRect().top<200));
        const rogue=await page.locator('[data-phone-reading-board="agentsRogue"] .phone-reading-mobile').innerText();for(const phrase of ['APRIL 2026 · POCKETOS','master key in another file','live database and its backups in nine seconds.','“I violated every principle I was given.”'])assert.ok(rogue.includes(phrase));
        for(const answer of ['Break the goal into steps','Go through all 50','Fix it, then check again','Stop and tell your human','Show your human first'])await page.getByRole('button',{name:answer,exact:true}).click();assert.ok((await page.locator('#main-content').innerText()).includes('Agents do the work; people own the result.'));
      } else {
        assert.deepEqual(await page.locator('[data-phone-reading-board="integritySchool"] h4').allTextContents(),['Acceptable','Follow the Rules','Unacceptable']);
        const school=await page.locator('[data-phone-reading-board="integritySchool"] .phone-reading-mobile').innerText();for(const phrase of ['work you understand and created.','Check the policy and disclose your use.','when the assignment prohibits it.'])assert.ok(school.includes(phrase));
        assert.deepEqual(await page.locator('[data-phone-reading-board="integrityAllowed"] h4').allTextContents(),['1Understand It','2Show Your Process','3Explain AI’s Role']);
        const sharing=await page.locator('[data-phone-reading-board="integritySharing"] .phone-reading-mobile').innerText();for(const phrase of ['Keep it general whenever possible.','Include only what the answer truly needs.','other people’s private information.'])assert.ok(sharing.includes(phrase));
        const photo=page.locator('[data-phone-reading-board="integrityPhoto"] .phone-reading-mobile');assert.deepEqual(await photo.locator('.phone-eight-photo-key li').allTextContents(),['1YOUR NAME','2YOUR SCHOOL AND CLASS','3YOUR LOCKER COMBINATION','4A PRESCRIPTION MEDICATION','5YOUR HOME ADDRESS','6A PRIVATE NOTIFICATION']);
        assert.deepEqual(await photo.locator('.phone-eight-pin').allTextContents(),['1','2','3','4','5','6']);assert.ok(await photo.locator('.phone-eight-pin').evaluateAll(ns=>ns.every(n=>parseFloat(getComputedStyle(n).fontSize)>=16)));
        const tree=await photo.ariaSnapshot();assert.equal(tree.includes('Photographed homework with six numbered privacy exposures.'),true);assert.equal(tree.split('YOUR LOCKER COMBINATION').length-1,1);
        const chunks=page.locator('.redact-chunk[role="button"]');assert.ok(await chunks.count()>10);for(let i=await chunks.count()-1;i>=0;i--)await chunks.nth(i).click();assert.ok((await page.locator('#main-content').innerText()).includes('Privacy becomes a habit.'));assert.equal(await page.getByText('Better Version',{exact:true}).count(),4);
      }
      await page.emulateMedia({ media: 'print' });
      assert.equal(await page.locator('.phone-reading-mobile:visible').count(), 0);
      assert.equal(await page.locator('.phone-reading-desktop img:visible').count(), kinds.length);
      assert.deepEqual(errors, []);
      await context.close();
    }
    if (process.env.PHONE_WAVE_OUTPUT) { fs.mkdirSync(process.env.PHONE_WAVE_OUTPUT, { recursive: true }); fs.writeFileSync(path.join(process.env.PHONE_WAVE_OUTPUT, 'phone-checks.json'), JSON.stringify(records, null, 2)); }
    console.log('PASS: eleven boards; phone, landscape, breakpoints, readable HTML, complete comparisons, exact qualifications, agent return to Plan and focus, six photo-marker relationships, accessible representations, all lesson activities, print and no runtime errors');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });

// Third phone-readability batch. Run with the same Playwright NODE_PATH as other browser tests.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.BASE_URL || 'http://127.0.0.1:8796';
const lessons = {
  flattery: ['flatteryFeedback', 'praiseTraining', 'sycophancyResponse', 'fightFlattery'],
  whatpeoplesay: ['expertBets', 'missedPredictions', 'yourHands'],
  layers: ['horseReads', 'layersNumbers', 'itToCat']
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
      if (id === 'flattery') {
        assert.deepEqual(await page.locator('[data-phone-reading-board="fightFlattery"] .phone-reading-mobile .phone-reading-number').allTextContents(), ['01','02','03']);
        assert.deepEqual(await page.locator('[data-phone-reading-board="praiseTraining"] .phone-reading-mobile h4').allTextContents(), ['People Rank','Praise Can Win','Numbers Move']);
        assert.deepEqual(await page.locator('[data-phone-reading-board="praiseTraining"] .phone-reading-mobile li > .phone-reading-number:first-child').allTextContents(), ['1','2','3']);
        const comparison=await page.locator('[data-phone-reading-board="flatteryFeedback"] .phone-reading-mobile').innerText();
        for (const copy of ['The American Dream is something that many people have thought about over the years.','That praise could fit almost any Gatsby essay.','Your next step is to write a thesis']) assert.ok(comparison.includes(copy));
        const board = page.locator('[data-phone-reading-board="flatteryFeedback"] .phone-reading-mobile');
        assert.equal(await board.locator('h3').textContent(), 'Flattery Trap vs. Useful Feedback');
        assert.deepEqual(await board.locator('h4').allTextContents(), ['Flattery Trap', 'Useful Feedback']);
        assert.equal(await board.locator('.phone-reading-label').count(), 0);
        assert.deepEqual(await board.locator('.phone-reading-fact strong').allTextContents(), ['The Truth', 'The Truth']);
        const response=await page.locator('[data-phone-reading-board="sycophancyResponse"] .phone-reading-mobile').innerText();assert.ok(response.includes('It’s performance art disguised as a gag gift'));
        await page.getByRole('button', { name: 'Mark step 1 complete', exact: true }).click();
        assert.equal(await page.getByRole('button', { name: 'Mark step 1 incomplete', exact: true }).getAttribute('aria-pressed'), 'true');
      } else if (id === 'whatpeoplesay') {
        const pairs=page.locator('[data-phone-reading-board="yourHands"] .phone-three-comparison');assert.equal(await pairs.count(),5);
        assert.deepEqual(await pairs.first().locator('h4').allTextContents(),['Out of Your Hands','In Your Hands']);
        assert.ok((await pairs.first().innerText()).includes('Build real depth in something you care about.'));
        assert.ok((await pairs.last().innerText()).includes('What the next headline predicts'));
        const experts=await page.locator('[data-phone-reading-board="expertBets"] .phone-reading-mobile').innerText();for(const copy of ['Dario Amodei','Geoffrey Hinton','50-100 years into 5-10 years','But Admits','fewer people will die from it.'])assert.ok(experts.includes(copy));
        await page.getByRole('button',{name:'Wrong',exact:true}).first().click();assert.ok(await page.getByText('Wrong, and way undersold.',{exact:false}).first().isVisible());
      } else {
        assert.deepEqual(await page.locator('[data-phone-reading-board="itToCat"] .phone-reading-mobile h4').allTextContents(),['The Sentence','Start','Layer 1','Layer 2','Repeat','Result']);
        assert.deepEqual(await page.locator('[data-phone-reading-board="layersNumbers"] .phone-three-vector').allTextContents(),['[.42, −1.15, …]','[.51, −.87, …]','[.27, −1.21, …]','[.19, −1.12, …]']);
        assert.deepEqual(await page.locator('[data-phone-reading-board="itToCat"] .phone-three-vector').allTextContents(),['[.12, −.34, …]','[.18, −.22, …]','[.25, −.09, …]','[.41, .06, …]']);
        assert.deepEqual(await page.locator('.phone-three-layer p').allTextContents(),['Attention','Transformation']);
        const sentence=await page.locator('[data-phone-reading-board="itToCat"] .phone-reading-note').innerText();assert.ok(sentence.includes('The tired CAT sat on the mat during the May rainstorm. IT soon fell asleep.'));
        assert.deepEqual(await page.locator('[data-phone-reading-board="horseReads"] .phone-reading-mobile h4').allTextContents(),['1First Read','2More Reads','3Meaning Clicks']);
        await page.getByRole('button',{name:'Show Questions',exact:true}).click();
        assert.equal(await page.getByRole('button',{name:'False',exact:true}).count(),7);
        await page.getByRole('button',{name:'False',exact:true}).first().click();
        assert.ok(await page.getByText('Right. No coins, no robot.',{exact:false}).isVisible());
      }
      await page.emulateMedia({ media: 'print' });
      assert.equal(await page.locator('.phone-reading-mobile:visible').count(), 0);
      assert.equal(await page.locator('.phone-reading-desktop img:visible').count(), kinds.length);
      assert.deepEqual(errors, []);
      await context.close();
    }
    if (process.env.PHONE_WAVE_OUTPUT) { fs.mkdirSync(process.env.PHONE_WAVE_OUTPUT, { recursive: true }); fs.writeFileSync(path.join(process.env.PHONE_WAVE_OUTPUT, 'phone-checks.json'), JSON.stringify(records, null, 2)); }
    console.log('PASS: ten boards, phone widths/landscape/breakpoints, 16px text/20px headings, no board clipping, single accessible representation, preserved comparisons, full quotes, exact vectors, connected stages, lesson interactions, print, and runtime errors');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });

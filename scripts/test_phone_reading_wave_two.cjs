// Second phone-readability batch. Run with the same Playwright NODE_PATH as other browser tests.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.BASE_URL || 'http://127.0.0.1:8796';
const lessons = {
  supporttrap: ['supportComparison', 'supportJobs', 'supportDanger'],
  questionsvaluable: ['answersFaster', 'questionValue', 'qualities12', 'qualities34'],
  aitips: ['thoughtPartner', 'learnProfit', 'collegeStart', 'iterate']
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
      if (id === 'supporttrap') {
        const comparison = page.locator('[data-phone-reading-board="supportComparison"] .phone-reading-mobile');
        assert.deepEqual(await comparison.locator('.phone-reading-fact strong').allTextContents(), ['The Truth','The Truth']);
        const danger = await page.locator('[data-phone-reading-board="supportDanger"] .phone-reading-mobile').innerText();
        for (const text of ['Leave the Chat','Do It Now','Tell Anyway','988','911','Safety outranks secrecy.']) assert.ok(danger.includes(text));
        await page.getByRole('button', { name: 'This can stay in the chat.', exact: true }).first().click();
        assert.ok(await page.getByText('This job ends in the chat.', { exact: true }).isVisible());
      } else if (id === 'questionsvaluable') {
        const labels = await page.locator('[data-phone-reading-board="qualities12"] .phone-reading-mobile h4, [data-phone-reading-board="qualities34"] .phone-reading-mobile h4').allTextContents();
        assert.deepEqual(labels, ['Open-Minded','Specific','On Target','Open-Ended']);
        assert.deepEqual(await page.locator('[data-phone-reading-board="answersFaster"] .phone-reading-mobile .phone-reading-fact').allTextContents(), ['Time to AnswerHalf a Saturday','Time to AnswerAn hour or two','Time to AnswerSeconds']);
      } else {
        assert.deepEqual(await page.locator('[data-phone-reading-board="thoughtPartner"] .phone-conversation-role').allTextContents(), ['You','AI','You','AI']);
        assert.deepEqual(await page.locator('[data-phone-reading-board="iterate"] .phone-conversation-role').allTextContents(), ['You','AI','You','AI']);
        assert.deepEqual(await page.locator('.phone-profit-term').allTextContents(), ['$300Sales','$150Costs','$150Profit']);
        assert.deepEqual(await page.locator('.phone-profit-operator').allTextContents(), ['−','=']);
        await page.getByLabel('Enter your idea here', { exact: true }).fill('Organize a study session');
        assert.ok((await page.locator('#main-content').innerText()).includes('I’m considering this idea: Organize a study session'));
      }
      if (id !== 'supporttrap') {
        await page.getByRole('button', { name: 'Mark step 1 complete', exact: true }).click();
        assert.equal(await page.getByRole('button', { name: 'Mark step 1 incomplete', exact: true }).getAttribute('aria-pressed'), 'true');
      }
      await page.emulateMedia({ media: 'print' });
      assert.equal(await page.locator('.phone-reading-mobile:visible').count(), 0);
      assert.equal(await page.locator('.phone-reading-desktop img:visible').count(), kinds.length);
      assert.deepEqual(errors, []);
      await context.close();
    }
    if (process.env.PHONE_WAVE_OUTPUT) { fs.mkdirSync(process.env.PHONE_WAVE_OUTPUT, { recursive: true }); fs.writeFileSync(path.join(process.env.PHONE_WAVE_OUTPUT, 'phone-checks.json'), JSON.stringify(records, null, 2)); }
    console.log('PASS: eleven boards, phone widths/landscape/breakpoints, 16px text/20px headings, no board clipping, single accessible representation, exact roles/values/actions, lesson interactions, print, and runtime errors');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });

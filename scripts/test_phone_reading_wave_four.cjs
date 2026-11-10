// Fourth phone-readability batch. Run with the same Playwright NODE_PATH as other browser tests.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.BASE_URL || 'http://127.0.0.1:8796';
const lessons = {
  tokens: ['tokenExamples','tokenIdentity','tokenSend'],
  aiismath: ['standardProbability','coinPossibilities','coinClue','nextWord'],
  attention: ['contextProblems','earlierReading','transformerReading','contextNumbers','resolvedMeaning','positionOrder']
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
      if (id === 'tokens') {
        const rows=page.locator('[data-phone-reading-board="tokenExamples"] .phone-four-examples > li');assert.equal(await rows.count(),7);
        assert.deepEqual(await rows.first().locator('.phone-four-chip').allTextContents(),['un','belie','vable']);
        assert.deepEqual(await rows.nth(5).locator('.phone-four-chip').allTextContents(),['I','SP ♥','SP AI']);
        assert.deepEqual(await rows.last().locator('.phone-four-chip').allTextContents(),['https','://','www','.quick','book','str','aining','.com']);
        assert.ok((await rows.last().innerText()).includes('8 tokens (even a web address breaks into chunks)'));
        assert.deepEqual(await page.locator('.phone-four-mappings p').allTextContents(),['un↓359','belie↓32898','vable↓24694']);
        assert.ok((await page.locator('[data-phone-reading-board="tokenIdentity"] .phone-reading-mobile').innerText()).includes('The number identifies the token, not its meaning.'));
        await page.getByRole('button',{name:'6',exact:true}).first().click();assert.ok(await page.getByText('Six tokens. Smarter splits into Sm + arter',{exact:false}).isVisible());
      } else if (id === 'aiismath') {
        for (const kind of ['coinPossibilities','coinClue']) {
          const board=page.locator('[data-phone-reading-board="'+kind+'"] .phone-reading-mobile');assert.equal(await board.locator('.phone-four-outcome').count(),4);
          assert.deepEqual(await board.locator('.phone-four-outcome-title').allTextContents(),['Heads + Heads','Heads + Tails','Tails + Heads','Tails + Tails']);
          assert.equal(await board.locator('.is-ruled-out').count(),kind==='coinClue'?2:0);
          assert.ok((await board.innerText()).includes(kind==='coinClue'?'50%':'25%'));
        }
        const next=await page.locator('[data-phone-reading-board="nextWord"] .phone-reading-mobile').innerText();for (const copy of ['Spot','22%','Max','17%','Buddy','14%','remaining 47%'])assert.ok(next.includes(copy));
        await page.getByRole('button',{name:'Higher',exact:false}).first().click();assert.ok(await page.getByText('Guess 2 is…',{exact:false}).isVisible());
      } else {
        assert.deepEqual(await page.locator('[data-phone-reading-board="earlierReading"] .phone-four-chip').allTextContents(),'The tired cat sat on the mat during the May rainstorm. IT soon fell asleep.'.split(' '));
        assert.deepEqual(await page.locator('[data-phone-reading-board="transformerReading"] .phone-four-chip').allTextContents(),'THE TIRED CAT SAT ON THE MAT DURING THE MAY RAINSTORM. IT SOON FELL ASLEEP.'.split(' '));
        assert.equal(await page.locator('.phone-four-word-arrow').count(),14);
        assert.deepEqual(await page.locator('.phone-four-position-stamps p').allTextContents(),['1DOG','2BITES','3MAN']);
        for (const kind of ['contextProblems','resolvedMeaning']) {const words=await page.locator('[data-phone-reading-board="'+kind+'"] .phone-reading-mobile').innerText();for(const copy of ['Please turn on the LIGHT.','The empty suitcase felt LIGHT.','The cat was thirsty, so IT drank the milk.','The milk was fresh, so the cat drank IT.'])assert.ok(words.includes(copy));}
        await page.getByRole('button',{name:'river,',exact:true}).first().click();assert.ok(await page.getByText('Right.',{exact:true}).first().isVisible());
      }
      await page.emulateMedia({ media: 'print' });
      assert.equal(await page.locator('.phone-reading-mobile:visible').count(), 0);
      assert.equal(await page.locator('.phone-reading-desktop img:visible').count(), kinds.length);
      assert.deepEqual(errors, []);
      await context.close();
    }
    if (process.env.PHONE_WAVE_OUTPUT) { fs.mkdirSync(process.env.PHONE_WAVE_OUTPUT, { recursive: true }); fs.writeFileSync(path.join(process.env.PHONE_WAVE_OUTPUT, 'phone-checks.json'), JSON.stringify(records, null, 2)); }
    console.log('PASS: thirteen boards, phone widths/landscape/breakpoints, 16px text/20px headings, no board clipping, single accessible representation, exact token splits/IDs, coin outcomes/odds, context examples, word order, interactions, print, and runtime errors');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });

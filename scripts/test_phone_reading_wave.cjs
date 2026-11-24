// First phone-readability wave: rendering, accessible alternatives, and interactions.
// BASE_URL=http://127.0.0.1:8796 NODE_PATH=<runtime>/node_modules node scripts/test_phone_reading_wave.cjs
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.BASE_URL || 'http://127.0.0.1:8796';
const lessons = {
  welcome: ['toolkit', 'courseWorks', 'coursePath'],
  prompting: ['moves12', 'moves34'],
  critical: ['reactions', 'equation', 'threeQuestions']
};
const criticalHeadings = [
  'heading "What’s your first reaction?" [level=2]',
  'heading "Take it at face value" [level=3]',
  'heading "Question the claim" [level=3]',
  'heading "Behind the Headlines" [level=2]',
  'heading "Critical Thinking Defined" [level=2]',
  'heading "Knowledge Matters" [level=2]',
  'heading "Knowledge" [level=3]',
  'heading "Critical Thinking" [level=3]',
  'heading "What Critical Thinkers Ask" [level=2]',
  'heading "The Question" [level=3]',
  'heading "The Evidence" [level=3]',
  'heading "The Alternatives" [level=3]'
];
const criticalCardQuestions = [
  ['The Question', 'What am I trying to understand or decide?'],
  ['The Evidence', 'What am I basing this on? What am I assuming?'],
  ['The Alternatives', 'What else could explain this? What else could I try?']
];

async function checkCriticalReadingOrder(page, cdp) {
  const snapshot = await page.locator('#critical-reading').ariaSnapshot();
  const lines = snapshot.split('\n').map(line => line.trim().replace(/^- /, ''));
  assert.deepEqual(lines.filter(line => line.startsWith('heading ')), criticalHeadings);
  for (const [card, question] of criticalCardQuestions) {
    const heading = lines.indexOf('heading "' + card + '" [level=3]');
    assert.equal(lines[heading + 1], 'paragraph: ' + question, card + ' must lead into its own question');
  }
  // Chrome exposes the narrow HTML close and wide image caption as static text.
  const { root } = await cdp.send('DOM.getDocument');
  const { nodeId } = await cdp.send('DOM.querySelector', { nodeId: root.nodeId, selector: '#critical-reading' });
  const close = 'AI answers. You decide what to trust.';
  const { nodes } = await cdp.send('Accessibility.queryAXTree', { nodeId, accessibleName: close, role: 'StaticText' });
  assert.equal(nodes.length, 1, 'Closing text must appear once in the expanded lesson');
  assert.ok(lines.findIndex(line => line.includes(close)) > lines.indexOf('paragraph: ' + criticalCardQuestions[2][1]),
    'Closing message must follow the final card');
}

(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const records = [];
  try {
    for (const [id, kinds] of Object.entries(lessons)) {
      const context = await browser.newContext({ viewport: { width: 390, height: 850 }, hasTouch: true, reducedMotion: 'reduce' });
      await context.route(/script\.google|script\.googleusercontent|\.mp4/, r => r.abort());
      await context.addInitScript(id => {
        localStorage.clear();
        localStorage.setItem('llm-user-name', 'Phone Review');
        localStorage.setItem('llm-explorer-progress', JSON.stringify({ activeSection: id, visited: [id], completed: [] }));
      }, id);
      const page = await context.newPage(), errors = [];
      const criticalSession = id === 'critical' ? await context.newCDPSession(page) : null;
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
            return { title: n.querySelector('h3')?.textContent, kind: n.parentElement.dataset.phoneReadingBoard, x: r.x, y: r.y + scrollY, width: r.width, height: r.height, text: n.innerText,
              tiny: [...n.querySelectorAll('p,li,h4')].filter(e => parseFloat(getComputedStyle(e).fontSize) < (e.tagName === 'H4' ? 20 : 16)).map(e => e.textContent),
              overflow: [...n.querySelectorAll('*')].filter(e => !(e instanceof SVGElement) && e.clientWidth && e.scrollWidth > e.clientWidth + 1).map(e => e.textContent) };
          }));
          for (const board of boards) { assert.deepEqual(board.tiny, []); assert.deepEqual(board.overflow, []); assert.ok(board.x >= 0 && board.x + board.width <= width); }
          // Audit the whole lesson too. Pre-existing chrome/activity overflow is
          // reported separately from the eight boards in this bounded wave.
          const pageGeometry = await page.evaluate(() => ({ scrollWidth: document.documentElement.scrollWidth,
            overflow: [...document.querySelectorAll('body *')].filter(e => !(e instanceof SVGElement) && e.children.length === 0 && e.getBoundingClientRect().width && e.getBoundingClientRect().right > innerWidth + 1).map(e => ({ tag: e.tagName, className: String(e.className), text: e.textContent.slice(0, 100), right: e.getBoundingClientRect().right })) }));
          records.push({ id, width, height, boards, pageGeometry });
        }
        const accessibility = await page.locator('#main-content').ariaSnapshot();
        if (mobile) {
          assert.ok(!accessibility.includes('img "What You’ll Need.'), 'Hidden desktop board is absent from the accessibility tree');
          assert.equal(await page.locator('.phone-reading-desktop-source:visible').count(), 0);
        }
        if (criticalSession) {
          await checkCriticalReadingOrder(page, criticalSession);
        } else if (mobile) {
          for (const title of kinds.map(k => ({ toolkit: 'What You’ll Need', courseWorks: 'How the Course Works', coursePath: 'Where This Course Takes You', moves12: 'Four Moves for Better Prompts', moves34: 'Four Moves for Better Prompts, Continued' })[k])) {
            assert.equal(accessibility.split('\n').filter(line => line.includes('heading "' + title + '" [level=3]')).length, 1, title + ' announced once');
          }
        }
      }
      await page.setViewportSize({ width: 390, height: 850 });
      if (id === 'welcome') {
        await page.getByText('Taking the Course as a Group?', { exact: true }).click();
        assert.ok(await page.getByText(/This course works for classes, clubs/).isVisible());
        assert.equal(await page.locator('[data-phone-reading-board="coursePath"] li').count(), 7);
      } else if (id === 'prompting') {
        assert.deepEqual(await page.locator('.phone-reading-mobile .phone-reading-label').allTextContents(), ['Move 1','Include','Weak','Better','Move 2','Include','Weak','Better','Move 3','Include','Weak','Better','Move 4','Include','Weak','Better']);
        const input = page.locator('input[type="number"]').first();
        if (await input.count()) { await input.fill('25'); assert.equal(await input.inputValue(), '25'); }
        const step = page.getByRole('button', { name: 'Mark step 1 complete', exact: true });
        await step.click(); assert.equal(await page.getByRole('button', { name: 'Mark step 1 incomplete', exact: true }).getAttribute('aria-pressed'), 'true');
      } else {
        assert.deepEqual(await page.locator('[data-phone-reading-board="equation"] .phone-reading-mobile [role="img"]').allTextContents(), ['+', '↓']);
        await page.getByRole('button', { name: 'There could be a hidden factor causing both', exact: true }).click();
        assert.ok(await page.getByText('Hot weather is one possible explanation.', { exact: true }).isVisible());
      }
      await page.emulateMedia({ media: 'print' });
      assert.equal(await page.locator('.phone-reading-mobile:visible').count(), 0, 'Phone alternatives never enter print');
      assert.equal(await page.locator('.phone-reading-desktop img:visible').count(), kinds.length, 'Canonical images remain in print');
      assert.deepEqual(errors, []);
      await context.close();
    }
    if (process.env.PHONE_WAVE_OUTPUT) {
      fs.mkdirSync(process.env.PHONE_WAVE_OUTPUT, { recursive: true });
      fs.writeFileSync(path.join(process.env.PHONE_WAVE_OUTPUT, 'phone-checks.json'), JSON.stringify(records, null, 2));
    }
    console.log('PASS: eight boards, portrait/landscape/breakpoints, real text sizes, overflow, single accessible representation, lesson interactions, print, and runtime errors');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exit(1); });

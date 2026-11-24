// Run against scripts/serve-site.py with Playwright on NODE_PATH.
// This checks browser semantics and keyboard operation. Speech needs a screen reader.
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const base = process.env.BASE_URL || 'http://127.0.0.1:8796';
const focused = locator => locator.evaluate(el => el === document.activeElement);

async function mainTree(cdp) {
  const { nodes } = await cdp.send('Accessibility.getFullAXTree');
  const byId = new Map(nodes.map(n => [n.nodeId, n]));
  const main = nodes.find(n => n.role.value === 'main');
  assert.ok(main, 'Main landmark');
  const output = [];
  function visit(node) {
    if (!node.ignored) output.push({ role: node.role.value, name: node.name?.value,
      level: node.properties?.find(p => p.name === 'level')?.value.value });
    for (const child of node.childIds || []) visit(byId.get(child));
  }
  visit(main);
  return output;
}

async function checkGroup(page) {
  const id = new URL(page.url()).pathname.split('/').pop();
  const key = selector => page.locator(selector).press('Enter');
  await page.locator('h1').waitFor();
  assert.match(await page.locator('body').ariaSnapshot(), /heading ".+" \[level=1\]/);
  switch (id) {
    case 'be-the-last-person-standing.html':
      await page.waitForFunction(() => !document.getElementById('choice-a').disabled);
      assert.notEqual(await page.locator('#image-a').getAttribute('alt'), await page.locator('#image-b').getAttribute('alt'));
      await key('#choice-a');
      assert.ok(await focused(page.locator('#next-button')));
      assert.match(await page.locator('#round-announcement').textContent(), /is real/);
      await key('#next-button');
      break;
    case 'one-word-at-a-time.html':
      for (const word of ['books', 'keys']) {
        await page.locator('#word').fill(word);
        await key('#word');
        await key('#next');
      }
      assert.ok(await focused(page.locator('#comparison-title')));
      break;
    case 'where-do-you-stand.html':
      await key('#count-votes');
      for (const input of await page.locator('.position-input').all()) await input.fill('1');
      await key('#show-results');
      assert.ok(await focused(page.locator('#results-title')));
      await key('#next-scenario');
      break;
    case 'whats-missing.html':
      await key('#show-checks');
      await key('#next-button');
      break;
    case 'prompetition.html':
      await key('#show-details');
      assert.equal(await page.locator('#show-details').getAttribute('aria-expanded'), 'true');
      await key('#next');
      break;
    case 'spot-whats-wrong.html':
    case 'make-the-question-better.html':
    case 'what-happened-next.html':
    case 'find-your-match.html':
      await key('#reveal');
      assert.ok(await page.evaluate(() => /^H[1-6]$/.test(document.activeElement.tagName)));
      await key('#next');
      break;
    case 'group-session.html':
      if (await page.locator('#study-subject').count()) {
        await page.locator('#study-subject').fill('Gravity');
        await page.locator('#study-situation').fill('A penguin park');
        assert.match(await page.locator('textarea').inputValue(), /Gravity.*penguin park/s);
      } else {
        assert.ok(await page.locator('.discussion-questions h2').count());
      }
      break;
    default: throw new Error('Add a keyboard check for ' + id);
  }
}

async function checkLinks(main, context, opened) {
  for (const link of await main.locator('a[href*="group-exercises/"]:visible,a[href*=".pdf"]:visible').all()) {
    const url = await link.evaluate(a => a.href);
    if (opened.has(url)) continue;
    const [child] = await Promise.all([context.waitForEvent('page'), link.press('Enter')]);
    try {
      if (/\.pdf(?:\?|$)/.test(url)) {
        await child.waitForURL(url);
        const response = await context.request.head(url);
        assert.equal(response.status(), 200);
        assert.match(response.headers()['content-type'], /pdf/);
        assert.match(await link.getAttribute('aria-label') || await link.innerText(), /pdf/i);
      } else {
        await child.waitForLoadState('domcontentloaded');
        await checkGroup(child);
      }
      opened.add(url);
    } finally { await child.close(); }
  }
}

async function checkActivity(main, id) {
  if (id === 'critical') {
    const questions = main.locator('.activity-quiz--mint');
    assert.equal(await questions.count(), 4);
    for (const [i, answer] of [0, 1, 1, 0].entries()) {
      const question = questions.nth(i);
      const options = question.getByRole('button');
      if (!i) {
        await options.nth(1).press('Enter');
        assert.match(await question.getByRole('status').innerText(), /.+/);
      }
      await options.nth(answer).press('Enter');
      assert.ok(await focused(options.nth(answer)));
      assert.equal(await options.nth(answer).getAttribute('aria-pressed'), 'true');
      assert.match(await question.getByRole('status').innerText(), /.+/);
    }
    assert.ok(await main.getByText('Bring these habits to AI.', {exact:true}).isVisible());
    return 'four claims, feedback and takeaway';
  }
  const steps = main.getByRole('button', {name: /^Mark step \d+ complete$/});
  const count = await steps.count();
  if (count) {
    for (let i = 0; i < count; i++) {
      const step = steps.first();
      await step.press('Space');
    }
    assert.equal(await main.getByRole('button',{name:/^Mark step \d+ incomplete$/}).count(), count);
    return count + ' lab steps';
  }
  const activity = main.locator('.interactive-box');
  if (id === 'reviews') {
    await main.getByRole('radio').first().press('ArrowRight');
    assert.equal(await main.getByRole('radio',{checked:true}).count(),1);
    return 'rating selection';
  }
  if (id === 'whatyoulearned') {
    await main.getByRole('button',{name:'Start the Final'}).press('Enter');
    const option = main.getByRole('radio').first();
    await option.press('Space');
    assert.equal(await option.getAttribute('aria-checked'), 'true');
    return 'final question and answer';
  }
  if (!await activity.count()) return '';
  if (id === 'paceofchange') {
    for (const input of await activity.getByRole('textbox').all()) await input.fill('5');
  }
  const choices = activity.getByRole('button').filter({visible:true});
  if (!await choices.count()) return '';
  const first = activity.locator('button:enabled:visible,[role="button"]:visible').first();
  const name = await first.getAttribute('aria-label') || (await first.innerText()).trim();
  await first.press('Enter');
  return name;
}

async function walkthrough(browser, width) {
  const context = await browser.newContext({ viewport: {width,height:900}, hasTouch:width===390, reducedMotion:'reduce' });
  try {
    await context.route(/script\.google|googleusercontent/, r => r.abort());
    await context.addInitScript(() => localStorage.setItem('llm-user-name','Accessibility Review'));
    const page = await context.newPage(), errors = [], opened = new Set();
    page.setDefaultTimeout(7000);
    page.on('pageerror', e => errors.push(e.message));
    await page.goto(base + '/course', {waitUntil:'domcontentloaded'});
    const main = page.getByRole('main');
    await main.getByRole('heading',{level:1}).waitFor();
    const ids = await page.evaluate(() => SECTION_GROUPS.flatMap(group => group.sections));
    const cdp = await context.newCDPSession(page);
    for (const [i,id] of ids.entries()) {
      try {
        const current = await page.locator('select[aria-label^="Choose a lesson"]').inputValue();
        assert.equal(current, id, 'Next must follow course navigation');
        const toggle = main.locator('.lesson-reading-toggle');
        if (await toggle.count()) {
          await toggle.press('Enter');
          assert.equal(await toggle.getAttribute('aria-expanded'),'true');
          await toggle.press('Space');
          assert.ok(await focused(toggle));
          assert.equal(await toggle.getAttribute('aria-expanded'),'false');
          await toggle.press('Enter');
        }
        const closed = main.locator('details:not([open]) > summary:visible');
        while (await closed.count()) await closed.first().press('Enter');
        const tree = await mainTree(cdp);
        const headings = tree.filter(n=>n.role==='heading');
        assert.equal(headings.filter(n=>n.level===1).length,1);
        for (const n of tree.filter(n=>['button','link','heading','Video','textbox','slider','spinbutton','combobox','checkbox','radio'].includes(n.role)))
          assert.ok(n.name?.trim(), id+' unnamed '+n.role);
        const boards = main.locator('[data-phone-reading-board],[data-answer-board],[data-vary-board]');
        for (const board of await boards.all()) {
          const snapshot = await board.ariaSnapshot();
          assert.match(snapshot,/heading /);
          assert.doesNotMatch(snapshot,/besmarterthanthetool\.com/);
        }
        const close = main.locator('.lesson-closing-board');
        if (await close.count()) {
          const lines = await close.locator('.welcome-opening-board-text p').allTextContents();
          for (const text of lines) assert.equal(tree.filter(n=>n.role==='StaticText' && n.name===text).length,1,'Close: '+text);
          assert.equal(await close.evaluate(el=>!!el.parentElement.querySelector('[data-phone-reading-board]') && !!el.nextElementSibling?.matches('[data-phone-reading-board]')), false);
        }
        const video = main.locator('video:visible').first();
        if (await video.count()) {
          await video.focus();
          await page.keyboard.press('Space');
          await page.waitForFunction(()=>[...document.querySelectorAll('main video')].some(v=>!v.paused && v.readyState>=2));
          await page.keyboard.press('Space');
        }
        await checkLinks(main, context, opened);
        const activity = await checkActivity(main,id);
        const next = main.getByRole('button',{name:/^(Mark as complete Next up:|Next Lesson )/i}).last();
        assert.ok((await next.innerText()).trim().length>12);
        await next.press('Enter');
        await page.waitForFunction(()=>document.activeElement.tagName==='H1');
        assert.deepEqual(errors,[]);
        console.log(width, id, headings.length+' headings', activity);
      } catch (e) { throw new Error(width+' '+id+': '+e.message,{cause:e}); }
    }
    console.log(width, ids.length+' destinations;',opened.size+' unique group/PDF links');
  } finally { await context.close(); }
}

(async()=>{
  const browser=await chromium.launch({channel:'chrome',headless:true});
  console.log('Chrome',browser.version());
  try { for (const width of [1440,390]) await walkthrough(browser,width); }
  finally { await browser.close(); }
})().catch(e=>{console.error(e);process.exitCode=1;});

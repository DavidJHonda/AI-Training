// Browser regression: navigation cannot substitute for passing The Final.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const vm = require('node:vm');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || '/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const nav = vm.runInNewContext(html.slice(html.indexOf('const SECTION_GROUPS ='), html.indexOf('// Opener sections all share')) + '\n({required: REQUIRED_SECTIONS, sections: SECTIONS})');
assert.equal(nav.required.length, 55);
const beforeFinal = Array.from(nav.required, s => s.id).filter(id => id !== 'whatyoulearned');
function attempt(correctCount) {
  let saved;
  const context = {localStorage: {setItem(k,v) { saved = v; }}};
  vm.createContext(context);
  vm.runInContext(html.slice(html.indexOf('const FINAL_BANK ='), html.indexOf('function OpenerFoundationsSection')), context);
  vm.runInContext(`saveFinalAttempt_(FINAL_BANK, Object.fromEntries(FINAL_BANK.map((q,i) => [q.id, i < ${correctCount} ? q.correct : (q.correct + 1) % q.options.length])))`, context);
  return saved;
}
const server = http.createServer((req,res) => {
  const file = path.resolve(root, '.' + new URL(req.url, 'http://localhost').pathname);
  if (!file.startsWith(root + path.sep)) { res.writeHead(404); return res.end(); }
  fs.readFile(file, (error, data) => {
    if (error) { res.writeHead(404); return res.end(); }
    res.setHeader('Content-Type', {'.html':'text/html','.js':'application/javascript','.css':'text/css','.svg':'image/svg+xml'}[path.extname(file)] || 'application/octet-stream');
    res.end(data);
  });
});
(async () => {
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  let browser;
  const errors = [];
  try {
    browser = await chromium.launch({channel:'chrome', headless:true});
    async function student({score, completed=beforeFinal, active='whatyoulearned', answers}={}) {
      const context = await browser.newContext();
      const page = await context.newPage();
      page.on('pageerror', e => errors.push(e.message));
      await page.route(/script\.google|script\.googleusercontent|\.mp4/, r => r.abort());
      await page.addInitScript(({score,completed,active,answers}) => {
        if (localStorage.getItem('test-initialized')) return;
        localStorage.setItem('test-initialized','1');
        localStorage.setItem('llm-user-name','Preview');
        localStorage.setItem('llm-explorer-progress', JSON.stringify({activeSection:active, visited:[active], completed}));
        if (score !== undefined) localStorage.setItem('final-exam', JSON.stringify({bestScore:score, attempts:1}));
        if (answers) localStorage.setItem('final-exam-unfinished:v1', answers);
      }, {score,completed,active,answers});
      await page.goto(`http://127.0.0.1:${server.address().port}/index.html`);
      await page.locator('.course-header [role="progressbar"]').waitFor();
      return {page, context};
    }
    async function progress(page, count) {
      await page.waitForFunction(count => {
        const bar = document.querySelector('.course-header [role="progressbar"]');
        return bar?.getAttribute('aria-valuemax') === '55' && bar.getAttribute('aria-valuenow') === String(count);
      }, count);
      await page.waitForFunction(count => JSON.parse(localStorage.getItem('llm-explorer-progress')).completed.length === count, count);
    }
    // Repair stale Final/review/resource flags without crediting an unpassed exam.
    for (const score of [undefined, 76]) {
      console.log('Checking legacy progress:', score);
      const {page,context} = await student({score, completed:[...beforeFinal,'whatyoulearned','reviews','resources','forgroups']});
      await progress(page,54);
      await page.getByRole('button', {name:/What Do You Think/}).last().click();
      await progress(page,54);
      await page.getByRole('button', {name:/Resources/}).last().click();
      await progress(page,54);
      await page.getByRole('button', {name:/For Groups/}).last().click();
      await progress(page,54);
      await context.close();
    }
    // Existing passes count even when the student opens another lesson first.
    console.log('Checking existing pass');
    const existing = await student({score:80, active:'welcome'});
    await progress(existing.page,55); await existing.context.close();
    // Threshold and failed retake; passing needs no certificate name or Next click.
    for (const [correctCount,priorScore,expected] of [[19,undefined,54],[20,undefined,55],[0,80,55]]) {
      console.log('Checking submitted score:', correctCount*4, 'prior:', priorScore);
      const {page,context} = await student({score:priorScore, answers:attempt(correctCount)});
      await page.getByRole('button',{name:'Continue the Final',exact:true}).click();
      await page.getByRole('button',{name:'Submit the Final',exact:true}).click();
      await page.waitForFunction(() => !!sessionStorage.getItem('final-exam-result:v1'));
      await progress(page,expected);
      assert.equal(await page.evaluate(() => JSON.parse(localStorage.getItem('final-exam')).bestScore), Math.max(priorScore || 0,correctCount*4));
      await page.reload(); await progress(page,expected);
      await context.close();
    }
    assert.deepEqual(errors,[]);
    console.log('PASS: 55 required items; optional pages and Next do not complete The Final; legacy progress, 76% failure, 80% pass, failed retake, and reload verified.');
  } finally {
    if (browser) await browser.close();
    server.closeAllConnections();
    await new Promise(resolve => server.close(resolve));
  }
})().catch(error => { console.error(error); process.exitCode=1; });

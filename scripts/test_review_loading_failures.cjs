// Isolated reproductions: no requests to Google, live rows, or email deliveries.
// Optional source directory permits running the same cases against a before snapshot.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const sourceDir = process.argv[2] || path.join(__dirname, '..');
const observe = process.argv.includes('--observe');
const html = fs.readFileSync(path.join(sourceDir, 'index.html'), 'utf8');
const backend = fs.readFileSync(path.join(sourceDir, 'google-apps-script.gs'), 'utf8');
const headers = ['Submitted At', 'Updated At', 'Review ID', 'Student ID', 'Course Version', 'Usefulness Rating', 'Improvement', 'Testimonial', 'Quote Permission', 'Quote First Name'];

function serverFixture(count = 45) {
  const rows = [headers.slice()];
  for (let i = 0; i < count; i++) rows.push([new Date(1700000000000 + i * 1000), new Date(), 'id-' + i, 'private-student', 'v1', i % 5 + 1, 'private-feedback', 'Review ' + i, 'first_name', 'Student ' + i]);
  const state = {busy: false, lockCalls: 0, lockTimeouts: 0, writes: 0, reads: 0, flushes: 0, afterWrite: null, logs: [], readError: false};
  const sheet = {
    getLastRow: () => rows.length,
    getLastColumn: () => rows[0].length,
    setFrozenRows() {},
    appendRow(row) { rows.push(Array.from(row)); state.writes++; if (state.afterWrite) state.afterWrite(); },
    getRange(row, col, height = 1, width = 1) {
      return {
        getValues() {
          state.reads++;
          if (state.readError && row > 1) throw Error('Spreadsheet unavailable: private-spreadsheet-identifier');
          return rows.slice(row - 1, row - 1 + height).map(r => r.slice(col - 1, col - 1 + width));
        },
        setValues(values) {
          values.forEach((r, i) => r.forEach((value, j) => { rows[row - 1 + i][col - 1 + j] = value; }));
          state.writes++;
          if (state.afterWrite) state.afterWrite();
        },
        createTextFinder(value) {
          return {matchEntireCell() { return this; }, findNext() {
            const offset = rows.slice(row - 1, row - 1 + height).findIndex(r => r[col - 1] === value);
            return offset < 0 ? null : {getRow: () => row + offset};
          }};
        }
      };
    }
  };
  const context = {
    console: {error: (...args) => state.logs.push(args.join(' ')), log() {}},
    Utilities: {DigestAlgorithm: {SHA_256: 'sha256'}, computeDigest: (algorithm, text) => Array.from(crypto.createHash(algorithm).update(text).digest())},
    SpreadsheetApp: {getActiveSpreadsheet: () => ({getSheetByName: () => sheet}), flush() { state.flushes++; }},
    ContentService: {MimeType: {JSON: 'json', TEXT: 'text'}, createTextOutput: text => ({setMimeType: () => text})},
    LockService: {getScriptLock: () => {
      let acquired = false;
      return {waitLock(ms) {
        state.lockCalls++;
        if (state.busy) { state.lockTimeouts++; throw Error('Lock timeout: another process held the lock for ' + ms + ' ms'); }
        state.busy = acquired = true;
      }, releaseLock() { if (acquired) state.busy = acquired = false; }};
    }}
  };
  vm.createContext(context);
  vm.runInContext(backend, context);
  return {
    rows, state,
    get(cursor) { return JSON.parse(context.doGet({parameter: {action: 'public_reviews', ...(cursor ? {cursor} : {})}})); },
    post(overrides = {}) { return context.doPost({postData: {contents: JSON.stringify({eventType: 'review', reviewId: 'test-review', studentId: 'private-student', usefulnessRating: 4, testimonial: 'New review', quotePermission: 'first_name', quoteFirstName: 'Nick', ...overrides})}}); }
  };
}

function feedFixture(server) {
  const slots = [], effects = [], pendingEffects = [], listeners = {}, timers = new Map();
  let now = 0, timerId = 0, cursor = 0, refreshKey = 0, delay = 0, requests = 0;
  const schedule = (fn, ms) => { timers.set(++timerId, {at: now + ms, fn}); return timerId; };
  const context = {
    React: {createElement: (type, props, ...children) => ({type, props: props || {}, children: children.flat(Infinity)})},
    useState(initial) { const i = cursor++; if (!(i in slots)) slots[i] = initial; return [slots[i], value => { slots[i] = value; }]; },
    useRef(initial) { const i = cursor++; return slots[i] || (slots[i] = {current: initial}); },
    useEffect(callback, deps) {
      const i = cursor++;
      if (!effects[i] || effects[i].deps[0] !== deps[0]) pendingEffects.push(() => {
        if (effects[i]) effects[i].cleanup();
        effects[i] = {deps, cleanup: callback()};
      });
    },
    ActivityButton: 'ActivityButton', SIGNUP_ENDPOINT: 'https://isolated.test/exec', AbortController,
    setTimeout: schedule, clearTimeout: id => timers.delete(id),
    setInterval: fn => { listeners.timer = fn; return 0; }, clearInterval() {},
    window: {addEventListener: (name, fn) => { listeners[name] = fn; }, removeEventListener() {}},
    document: {visibilityState: 'visible', addEventListener: (name, fn) => { listeners[name] = fn; }, removeEventListener() {}},
    fetch(url, options) {
      requests++;
      return new Promise((resolve, reject) => {
        const finish = () => {
          options.signal.removeEventListener('abort', abort);
          resolve({ok: true, json: async () => server.get(new URL(url).searchParams.get('cursor'))});
        };
        const id = schedule(finish, delay);
        const abort = () => { timers.delete(id); reject(Error('Request aborted')); };
        options.signal.addEventListener('abort', abort, {once: true});
        if (options.signal.aborted) abort();
      });
    }
  };
  vm.createContext(context);
  vm.runInContext(html.slice(html.indexOf('function StudentReviewsList('), html.indexOf('function ReviewsSection(')), context);
  const flatten = node => [node, ...node.children.flatMap(child => child && typeof child === 'object' ? flatten(child) : [])];
  const render = () => { cursor = 0; const result = flatten(context.StudentReviewsList({refreshKey})); pendingEffects.splice(0).forEach(fn => fn()); return result; };
  const settle = () => new Promise(resolve => setImmediate(resolve));
  return {
    render, listeners,
    setDelay(value) { delay = value; },
    refresh() { refreshKey++; render(); },
    dispose() { effects.filter(Boolean).forEach(e => e.cleanup()); },
    get requests() { return requests; },
    async tick(ms) {
      const end = now + ms;
      await settle();
      for (;;) {
        const next = [...timers].sort((a, b) => a[1].at - b[1].at)[0];
        if (!next || next[1].at > end) break;
        now = next[1].at; timers.delete(next[0]); next[1].fn(); await settle();
      }
      now = end; await settle();
    }
  };
}

async function main() {
  const findings = [];
  const check = async (name, test) => {
    try { const details = await test(); findings.push({case: name, pass: true, ...details}); }
    catch (error) { findings.push({case: name, pass: false, error: error.message}); }
  };
  await check('New submission, edit, and independent return to page', async () => {
    const server = serverFixture(5);
    assert.equal(server.post(), 'review-ok');
    assert.equal(server.get().ratingSummary.total, 6);
    const submittedAt = server.rows.at(-1)[0];
    assert.equal(server.post({usefulnessRating: 1, testimonial: 'Edited review', quoteFirstName: 'Changed name'}), 'review-ok');
    const feed = feedFixture(server); feed.render(); await feed.tick(0);
    assert.equal(feed.render().filter(n => n.type === 'article').length, 6);
    assert.equal(server.get().ratingSummary.total, 6);
    assert.equal(server.rows.at(-1)[0], submittedAt);
    assert.equal(server.get().reviews[0].name, 'Changed name');
    feed.dispose();
  });
  await check('Public read while an unrelated execution holds the write lock', async () => {
    const server = serverFixture(5);
    server.state.busy = true;
    const feed = feedFixture(server); feed.render(); await feed.tick(0);
    const failed = feed.render().some(n => n.props.role === 'alert');
    feed.dispose();
    assert.equal(failed, false, 'Read displayed the loading error; lock timeouts=' + server.state.lockTimeouts);
    assert.equal(server.state.lockCalls, 0, 'A public read should not queue behind writers');
  });
  await check('Edit publishes all changed fields together, including during a read', async () => {
    const server = serverFixture(1);
    let observations = [];
    server.state.afterWrite = () => observations.push(server.get());
    assert.equal(server.post({reviewId: 'id-0', usefulnessRating: 2, testimonial: 'Revised text', quoteFirstName: 'Revised name'}), 'review-ok');
    assert.equal(server.state.writes, 1, 'The edit is split across separate sheet writes');
    assert.equal(server.state.flushes, 1);
    for (const result of observations) {
      assert.equal(result.reviews[0].rating, 2);
      assert.equal(result.reviews[0].text, 'Revised text');
      assert.equal(result.reviews[0].name, 'Revised name');
    }
  });
  await check('Withdrawing publication during an edit never exposes private text', async () => {
    const server = serverFixture(1);
    const observations = [];
    server.state.afterWrite = () => observations.push(server.get());
    assert.equal(server.post({reviewId: 'id-0', testimonial: 'private-revised-review', quotePermission: 'none'}), 'review-ok');
    for (const result of observations) {
      assert.deepEqual(result.reviews, []);
      assert.equal(result.ratingSummary.total, 1);
      assert.ok(!JSON.stringify(result).includes('private-'));
    }
  });
  await check('Writers still serialize; a busy write cannot append a duplicate', async () => {
    const server = serverFixture(5);
    server.state.busy = true;
    assert.equal(server.post(), 'error');
    assert.equal(server.state.writes, 0);
    server.state.busy = false;
    assert.equal(server.post(), 'review-ok');
    assert.equal(server.post(), 'review-ok');
    assert.equal(server.rows.length, 7);
  });
  await check('Read and layout failures expose only safe diagnostic categories', async () => {
    const server = serverFixture();
    server.state.readError = true;
    const result = server.get();
    assert.equal(result.code, 'REVIEWS_READ_FAILED');
    assert.ok(!JSON.stringify(result).includes('private-'));
    server.state.readError = false;
    server.rows[0][6] = 'Wrong column';
    assert.equal(server.get().code, 'REVIEWS_LAYOUT_FAILED');
  });
  await check('Load older pages, then refresh 45 reviews at 8 seconds per page', async () => {
    const server = serverFixture();
    const feed = feedFixture(server); feed.render(); await feed.tick(0);
    for (let i = 0; i < 2; i++) {
      feed.render().find(n => n.children.includes('Load older reviews')).props.onClick(); await feed.tick(0);
    }
    assert.equal(feed.render().filter(n => n.type === 'article').length, 45);
    feed.setDelay(8000); feed.refresh(); await feed.tick(24000);
    const articles = feed.render().filter(n => n.type === 'article').length;
    const failed = feed.render().some(n => n.props.role === 'alert');
    feed.dispose();
    assert.equal(failed, false, 'Three healthy 8-second requests exhaust the shared 20-second timeout');
    assert.equal(articles, 45);
  });
  await check('A genuinely stalled page still times out', async () => {
    const feed = feedFixture(serverFixture()); feed.setDelay(21000); feed.render(); await feed.tick(20000);
    assert.ok(feed.render().some(n => n.props.role === 'alert'));
    feed.dispose();
  });
  await check('Unmount and remount do not publish a cancelled request', async () => {
    const server = serverFixture(5);
    const oldFeed = feedFixture(server); oldFeed.setDelay(8000); oldFeed.render(); oldFeed.dispose(); await oldFeed.tick(8000);
    const newFeed = feedFixture(server); newFeed.render(); await newFeed.tick(0);
    assert.equal(newFeed.render().filter(n => n.type === 'article').length, 5);
    newFeed.dispose();
  });
  await check('1,000 reviews paginate without omissions or private fields', async () => {
    const server = serverFixture(1000);
    let cursor, items = [], pages = 0;
    do {
      const result = server.get(cursor); assert.ok(!result.error);
      items.push(...result.reviews); cursor = result.nextCursor; pages++;
      assert.equal(result.ratingSummary.total, 1000);
    } while (cursor);
    assert.equal(pages, 50); assert.equal(new Set(items.map(r => r.text)).size, 1000);
    assert.ok(!JSON.stringify(items).includes('private-'));
    return {pages, sheetReads: server.state.reads, lockCalls: server.state.lockCalls};
  });
  console.log(JSON.stringify(findings, null, 2));
  if (!observe && findings.some(f => !f.pass)) process.exitCode = 1;
}
main().catch(error => { console.error(error); process.exitCode = 1; });

const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const backend = fs.readFileSync(path.join(root, 'google-apps-script.gs'), 'utf8');
for (const script of html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)) {
  if (script[1].trim()) new vm.Script(script[1]);
}

// In-memory Apps Script services: exercise the actual handler without contacting Google.
class Sheet {
  constructor() { this.rows = []; }
  appendRow(row) { this.rows.push(Array.from(row)); }
  setFrozenRows() {}
  getLastRow() { return this.rows.length; }
  getLastColumn() { return this.rows[0].length; }
  getRange(row, col, height = 1, width = 1) {
    return {
      getValues: () => this.rows.slice(row - 1, row - 1 + height).map(r => r.slice(col - 1, col - 1 + width)),
      setValues: values => values.forEach((r, i) => r.forEach((v, j) => { this.rows[row - 1 + i][col - 1 + j] = v; })),
      createTextFinder: value => ({
        matchEntireCell() { return this; },
        findNext: () => {
          const offset = this.rows.slice(row - 1, row - 1 + height).findIndex(r => r[col - 1] === value);
          return offset < 0 ? null : {getRow: () => row + offset};
        }
      })
    };
  }
}
const enrollment = new Sheet();
const sheets = {Enrollment: enrollment};
const emails = [];
let locked = false;
const server = {
  Utilities: {DigestAlgorithm: {SHA_256: 'sha256'}, computeDigest: (algorithm, text) => Array.from(crypto.createHash(algorithm).update(text).digest())},
  console: {error() {}},
  SpreadsheetApp: {getActiveSpreadsheet: () => ({
    getSheets: () => [enrollment],
    getSheetByName: name => sheets[name],
    insertSheet: name => (sheets[name] = new Sheet())
  })},
  MailApp: {sendEmail: (...args) => emails.push(args)},
  LockService: {getScriptLock: () => ({waitLock() { assert.equal(locked, false); locked = true; }, releaseLock() { locked = false; }})},
  ContentService: {MimeType: {TEXT: 'text'}, createTextOutput: text => ({setMimeType: () => text})}
};
vm.createContext(server);
vm.runInContext(backend, server);
const post = data => server.doPost({postData: {contents: JSON.stringify(data)}});
const base = {eventType: 'review', reviewId: 'new-review', studentId: 'student', usefulnessRating: 4};
assert.equal(post(base), 'review-ok');
const reviews = sheets.Reviews;
assert.deepEqual(reviews.rows[0], ['Submitted At', 'Updated At', 'Review ID', 'Student ID', 'Course Version', 'Usefulness Rating', 'Improvement', 'Testimonial', 'Quote Permission', 'Quote First Name']);
assert.equal(reviews.rows[1].length, 10);
assert.deepEqual(reviews.rows[1].slice(6), ['', '', 'none', '']);
for (const usefulnessRating of [undefined, 0, 6, 2.5, 'bad']) assert.equal(post({...base, usefulnessRating}), 'error');
assert.equal(reviews.rows.length, 2);
const historical = [new Date('2025-01-01'), new Date('2025-01-02'), 'old-review', 'student', 'v1', 3, 'Old feedback', 'Old quote', 'anonymous', ''];
reviews.appendRow(historical);
assert.equal(post({...base, reviewId: 'old-review', usefulnessRating: 5, improvement: 'More practice', testimonial: 'Helpful course', quotePermission: 'first_name', quoteFirstName: 'Pat', confidenceBefore: 1, mostUseful: 'ignored'}), 'review-ok');
assert.equal(reviews.rows.length, 3);
assert.equal(reviews.rows[2][0], historical[0]);
assert.ok(reviews.rows[2][1] > historical[1]);
assert.deepEqual(reviews.rows[2].slice(6), ['More practice', 'Helpful course', 'first_name', 'Pat']);
assert.equal(post({...base, reviewId: 'old-review', testimonial: '', quotePermission: 'first_name'}), 'review-ok');
assert.deepEqual(reviews.rows[2].slice(7), ['', 'none', '']);
assert.equal(post({...base, testimonial: 'Quote', quotePermission: 'first_name'}), 'error');
assert.equal(post({...base, testimonial: 'Quote', quotePermission: 'public'}), 'error');
assert.equal(post({...base, testimonial: '=formula', improvement: '+private', quotePermission: 'anonymous'}), 'review-ok');
assert.deepEqual(reviews.rows[1].slice(6), ["'+private", "'=formula", 'anonymous', '']);
assert.equal(post({...base, reviewId: 'stale-client', confidenceBefore: 4, confidenceAfter: 5, mostUseful: 'Old form', changedBehavior: 'Old form'}), 'review-ok');
assert.equal(reviews.rows[3].length, 10);
assert.deepEqual(reviews.rows[3].slice(6), ['', '', 'none', '']);
// Deploy first, delete the retired columns second: both layouts work during the transition.
const legacy = new Sheet();
legacy.appendRow(reviews.rows[0].slice(0, 6).concat(['Confidence Before', 'Confidence After', 'Most Useful', 'What Changed'], reviews.rows[0].slice(6)));
const legacyRow = [new Date('2025-01-01'), new Date('2025-01-02'), 'legacy-review', 'student', 'v1', 3, 2, 5, 'Lesson one', 'Check sources', 'Old feedback', 'Old quote', 'none', ''];
legacy.appendRow(legacyRow);
sheets.Reviews = legacy;
assert.equal(post({...base, reviewId: 'legacy-review', improvement: 'Before deletion', testimonial: 'Keep this review'}), 'review-ok');
assert.equal(legacy.rows[1][0], legacyRow[0]);
assert.deepEqual(legacy.rows[1].slice(6, 10), legacyRow.slice(6, 10));
assert.equal(legacy.rows[1][10], 'Before deletion');
assert.equal(post({...base, reviewId: 'legacy-new'}), 'review-ok');
assert.equal(legacy.rows[2].length, 14);
assert.deepEqual(legacy.rows[2].slice(6, 10), ['', '', '', '']);
// Simulate deleting the four columns together in Google Sheets.
legacy.rows.forEach(row => row.splice(6, 4));
assert.equal(post({...base, reviewId: 'legacy-review', improvement: 'After deletion', testimonial: 'Keep this review'}), 'review-ok');
assert.equal(legacy.rows.length, 3);
assert.equal(legacy.rows[1].length, 10);
assert.equal(legacy.rows[1][0], legacyRow[0]);
assert.deepEqual(legacy.rows[1].slice(6), ['After deletion', 'Keep this review', 'none', '']);
assert.equal(post({...base, reviewId: 'compact-new'}), 'review-ok');
assert.equal(legacy.rows[3].length, 10);
// A malformed layout must fail before any cells or rows are written.
legacy.rows[0][6] = 'Wrong heading';
const beforeInvalidWrite = JSON.stringify(legacy.rows);
assert.equal(post({...base, reviewId: 'legacy-review'}), 'error');
assert.equal(post({...base, reviewId: 'invalid-new'}), 'error');
assert.equal(JSON.stringify(legacy.rows), beforeInvalidWrite);
sheets.Reviews = reviews;
assert.equal(post({firstName: 'Test', lastName: 'Student', studentId: 'student', email: 'test@example.com'}), 'ok');
assert.equal(enrollment.rows.length, 1);
const completion = {eventType: 'course_completed', completionId: 'completion', studentId: 'student', firstName: 'Test', lastName: 'Student', score: 88};
assert.equal(post(completion), 'completion-ok');
assert.equal(post(completion), 'completion-ok');
assert.equal(sheets['Course Completions'].rows.length, 2);
assert.equal(post({...completion, firstName: 'Corrected'}), 'completion-ok');
assert.equal(sheets['Course Completions'].rows[1][2], 'Corrected');
assert.equal(post({...completion, completionId: 'failed', score: 70}), 'error');
assert.equal(sheets['Course Completions'].rows.length, 2);
assert.equal(emails.length, 3);
assert.equal(locked, false);

// Public endpoint tests use synthetic rows only in memory, never on the course page.
const publicSheet = new Sheet();
publicSheet.appendRow(reviews.rows[0]);
for (let i = 0; i < 45; i++) {
  publicSheet.appendRow([new Date(Date.UTC(2026, 0, i + 1)), new Date('2026-09-01'), 'secret-review-' + i, 'secret-student-' + i, 'private-version', i % 5 + 1, 'private-improvement-' + i, 'Review ' + i, i % 2 ? 'anonymous' : 'first_name', 'Name ' + i]);
}
publicSheet.appendRow([new Date('2026-09-01'), new Date(), 'secret-private', 'student', '', 5, 'private-feedback', 'private-review-text', 'none', 'Private Name']);
publicSheet.appendRow([new Date('2026-09-02'), new Date(), 'secret-empty', 'student', '', 5, '', '   ', 'anonymous', '']);
const getPublic = cursor => JSON.parse(server.doGet({parameter: {action: 'public_reviews', ...(cursor ? {cursor} : {})}}));
sheets.Reviews = publicSheet;
let firstPage = getPublic();
assert.equal(firstPage.reviews.length, 20);
assert.deepEqual(firstPage.ratingSummary, {average: 145 / 47, total: 47});
assert.equal(firstPage.reviews[0].text, 'Review 44');
assert.equal(firstPage.reviews[0].name, 'Name 44');
assert.equal(firstPage.reviews[1].name, 'Anonymous');
let secondPage = getPublic(firstPage.nextCursor);
let thirdPage = getPublic(secondPage.nextCursor);
assert.deepEqual(secondPage.ratingSummary, firstPage.ratingSummary);
assert.deepEqual(thirdPage.ratingSummary, firstPage.ratingSummary);
assert.equal(thirdPage.reviews.length, 5);
assert.equal(thirdPage.nextCursor, null);
const allPublic = firstPage.reviews.concat(secondPage.reviews, thirdPage.reviews);
assert.equal(new Set(allPublic.map(r => r.text)).size, 45);
assert.equal(allPublic.filter(r => r.rating === 1).length, 9);
for (let i = 1; i < allPublic.length; i++) assert.ok(allPublic[i - 1].submittedAt >= allPublic[i].submittedAt);
for (const review of allPublic) assert.deepEqual(Object.keys(review).sort(), ['name', 'rating', 'submittedAt', 'text']);
assert.ok(!/secret|private-|Private Name/.test(JSON.stringify([firstPage, secondPage, thirdPage])));
// Editing an old review changes its contents, but retains its position by Submitted At.
assert.equal(post({...base, reviewId: 'secret-review-0', testimonial: 'Edited oldest', quotePermission: 'anonymous', usefulnessRating: 1}), 'review-ok');
let changedPage = getPublic(firstPage.nextCursor);
assert.equal(changedPage.reset, true);
assert.equal(changedPage.reviews[0].text, 'Review 44');
assert.equal(getPublic(getPublic(changedPage.nextCursor).nextCursor).reviews.at(-1).text, 'Edited oldest');
// Withdrawal invalidates an in-flight cursor and removes the entry, not just its name.
assert.equal(post({...base, reviewId: 'secret-review-44', testimonial: 'Review 44', quotePermission: 'none'}), 'review-ok');
assert.equal(getPublic(changedPage.nextCursor).reset, true);
assert.equal(getPublic().reviews[0].text, 'Review 43');
assert.ok(!getPublic().reviews.some(r => r.text === 'Review 44'));
// Anonymous permission must ignore a stored name; missing approved name falls back safely.
publicSheet.rows[44][9] = 'Do not expose';
assert.equal(getPublic().reviews[0].name, 'Anonymous');
publicSheet.rows[43][9] = '';
assert.equal(getPublic().reviews[1].name, 'Anonymous');
const publicBeforeLegacy = JSON.stringify(getPublic());
publicSheet.rows.forEach((row, i) => row.splice(6, 0, ...(i ? [1, 5, 'retired', 'retired'] : ['Confidence Before', 'Confidence After', 'Most Useful', 'What Changed'])));
assert.equal(JSON.stringify(getPublic()), publicBeforeLegacy);
publicSheet.rows.forEach(row => row.splice(6, 4));
assert.ok(JSON.parse(server.doGet({parameter: {action: 'public_reviews', cursor: 'bad'}})).error);
assert.ok(JSON.parse(server.doGet({parameter: {action: 'private_reviews'}})).error);
const savedSheet = sheets.Reviews;
delete sheets.Reviews;
assert.deepEqual(getPublic().reviews, []);
assert.deepEqual(getPublic().ratingSummary, {average: null, total: 0});
assert.equal(sheets.Reviews, undefined); // A public read doesn't create anything.
const aggregateSheet = new Sheet();
aggregateSheet.appendRow(reviews.rows[0]);
sheets.Reviews = aggregateSheet;
assert.equal(post({...base, reviewId: 'aggregate-public', usefulnessRating: 5, testimonial: 'Public', quotePermission: 'anonymous'}), 'review-ok');
assert.equal(post({...base, reviewId: 'aggregate-private', usefulnessRating: 1, testimonial: 'Private', quotePermission: 'none'}), 'review-ok');
assert.equal(post({...base, reviewId: 'aggregate-rating-only', usefulnessRating: 3}), 'review-ok');
assert.deepEqual(getPublic().ratingSummary, {average: 3, total: 3});
assert.equal(getPublic().reviews.length, 1);
assert.equal(post({...base, reviewId: 'aggregate-rating-only', usefulnessRating: 5}), 'review-ok');
assert.equal(post({...base, reviewId: 'aggregate-rating-only', usefulnessRating: 5}), 'review-ok');
assert.deepEqual(getPublic().ratingSummary, {average: 11 / 3, total: 3});
assert.equal(aggregateSheet.rows.length, 4);
// Invalid spreadsheet cells do not add zeroes or corrupt the average.
for (const rating of ['', 0, 6, 'invalid', 2.5]) aggregateSheet.appendRow([new Date(), new Date(), 'invalid', '', '', rating, '', '', 'none', '']);
assert.deepEqual(getPublic().ratingSummary, {average: 11 / 3, total: 3});
sheets.Reviews = savedSheet;
sheets.Reviews = reviews;

async function testPublicUI() {
  sheets.Reviews = publicSheet;
  const slots = [], effects = [], pending = [], listeners = {};
  let cursor = 0, offline = false, requests = 0;
  let refreshKey = 0;
  const feedSource = html.slice(html.indexOf('function StudentReviewsList('), html.indexOf('function ReviewsSection('));
  const context = {
    React: {createElement: (type, props, ...children) => ({type, props: props || {}, children: children.flat(Infinity)})},
    useState(initial) {
      const i = cursor++;
      if (!(i in slots)) slots[i] = initial;
      return [slots[i], value => { slots[i] = value; }];
    },
    useRef(initial) { const i = cursor++; return slots[i] || (slots[i] = {current: initial}); },
    useEffect(callback, deps) {
      const i = cursor++;
      if (!effects[i] || effects[i].deps[0] !== deps[0]) pending.push(() => {
        if (effects[i]) effects[i].cleanup();
        effects[i] = {deps, cleanup: callback()};
      });
    },
    ActivityButton: 'ActivityButton', SIGNUP_ENDPOINT: 'https://example.test/exec', AbortController,
    setTimeout, clearTimeout,
    setInterval: callback => { listeners.timer = callback; return 1; }, clearInterval() {},
    window: {addEventListener: (name, fn) => { listeners[name] = fn; }, removeEventListener() {}},
    document: {visibilityState: 'visible', addEventListener: (name, fn) => { listeners[name] = fn; }, removeEventListener() {}},
    fetch: async url => {
      requests++;
      if (offline) throw Error('offline');
      const params = Object.fromEntries(new URL(url).searchParams);
      return {ok: true, json: async () => JSON.parse(server.doGet({parameter: params}))};
    }
  };
  vm.createContext(context);
  vm.runInContext(feedSource, context);
  const flatten = node => [node, ...node.children.flatMap(child => child && typeof child === 'object' ? flatten(child) : [])];
  const render = () => {
    cursor = 0;
    const nodes = flatten(context.StudentReviewsList({refreshKey}));
    pending.splice(0).forEach(fn => fn());
    return nodes;
  };
  const settleUI = () => new Promise(resolve => setImmediate(resolve));
  render(); await settleUI();
  let nodes = render();
  assert.equal(nodes.filter(n => n.type === 'article').length, 20);
  assert.ok(nodes.some(n => n.type === 'h2' && n.children[0] === 'Student Reviews'));
  assert.ok(nodes.some(n => n.children.includes('47 ratings')));
  assert.ok(nodes.some(n => n.children.includes(getPublic().ratingSummary.average.toFixed(1) + ' out of 5')));
  assert.ok(nodes.findIndex(n => n.props['aria-label'] === 'Overall course rating') < nodes.findIndex(n => n.props.role === 'region'));
  const scroll = nodes.find(n => n.props.role === 'region');
  assert.equal(scroll.props.style.overflowY, 'auto');
  assert.equal(scroll.props.tabIndex, 0);
  const beforeScroll = requests;
  const event = {currentTarget: {scrollHeight: 1000, scrollTop: 800, clientHeight: 200}};
  scroll.props.onScroll(event); scroll.props.onScroll(event);
  await settleUI();
  assert.equal(requests, beforeScroll + 1);
  assert.equal(render().filter(n => n.type === 'article').length, 40);
  render().find(n => n.children.includes('Load older reviews')).props.onClick();
  await settleUI();
  assert.equal(render().filter(n => n.type === 'article').length, 44);
  assert.ok(!render().some(n => n.children.includes('Load older reviews')));
  // A rating-only edit changes the displayed average without changing either count.
  const averageBefore = getPublic().ratingSummary.average;
  post({...base, reviewId: 'secret-empty', usefulnessRating: 1});
  refreshKey++; render(); await settleUI();
  assert.notEqual(getPublic().ratingSummary.average, averageBefore);
  assert.ok(render().some(n => n.children.includes(getPublic().ratingSummary.average.toFixed(1) + ' out of 5')));
  assert.ok(render().some(n => n.children.includes('47 ratings')));
  assert.equal(render().filter(n => n.type === 'article').length, 44);
  // Refresh loaded pages after an edit: no duplicate entry, no promotion to newest.
  post({...base, reviewId: 'secret-review-0', testimonial: '<b>Literal review text</b>', quotePermission: 'anonymous'});
  refreshKey++; render(); await settleUI();
  nodes = render();
  assert.equal(nodes.filter(n => n.type === 'article').length, 44);
  assert.ok(nodes.some(n => n.type === 'p' && n.children[0] === '<b>Literal review text</b>'));
  assert.ok(!nodes.some(n => n.props.dangerouslySetInnerHTML));
  post({...base, reviewId: 'secret-review-43', testimonial: 'Review 43', quotePermission: 'none'});
  listeners.timer(); await settleUI();
  assert.equal(render().filter(n => n.type === 'article').length, 43);
  assert.ok(!render().some(n => n.children.includes('Review 43')));
  offline = true;
  listeners.focus(); await settleUI();
  assert.equal(render().filter(n => n.type === 'article').length, 0);
  assert.ok(render().some(n => n.props.role === 'alert'));
  offline = false;
  render().find(n => n.children.includes('Try loading reviews again')).props.onClick();
  await settleUI();
  assert.equal(render().filter(n => n.type === 'article').length, 20);
  publicSheet.rows.slice(1).forEach(row => { row[8] = 'none'; });
  listeners.visibilitychange(); await settleUI();
  assert.ok(render().some(n => n.children.includes('No student reviews yet.')));
  assert.ok(render().some(n => n.children.includes('47 ratings')));
  publicSheet.rows.splice(1);
  listeners.timer(); await settleUI();
  assert.ok(render().some(n => n.children.includes('No ratings yet')));
  assert.ok(render().some(n => n.children.includes('0 ratings')));
  post({...base, reviewId: 'only-rating', usefulnessRating: 4});
  listeners.timer(); await settleUI();
  assert.ok(render().some(n => n.children.includes('4.0 out of 5')));
  assert.ok(render().some(n => n.children.includes('1 rating')));
  assert.ok(render().some(n => n.children.includes('No student reviews yet.')));
  effects.filter(Boolean).forEach(effect => effect.cleanup());
  sheets.Reviews = reviews;
}

// Stateful component harness: preserve hook state and local storage across renders.
const storage = new Map([['review-id', 'ui-review']]);
let reviewSequence = 0;
const source = html.slice(html.indexOf('function ReviewsSection('), html.indexOf('function WhatYouLearnedSection('));
function client(profile = {studentId: 'student', firstName: 'Pat'}) {
  const states = [];
  let cursor = 0;
  let failRequest = false;
  let loseResponse = false;
  const requests = [];
  const context = {
    React: {createElement: (type, props, ...children) => ({type, props: props || {}, children: children.flat(Infinity)})},
    getStudentProfile: () => profile,
    useLocalStorage: (key, initial) => [storage.has(key) ? JSON.parse(storage.get(key)) : initial, updater => {
      const previous = storage.has(key) ? JSON.parse(storage.get(key)) : initial;
      storage.set(key, JSON.stringify(updater(previous)));
    }],
    useState: initial => {
      const i = cursor++;
      if (!(i in states)) states[i] = typeof initial === 'function' ? initial() : initial;
      return [states[i], value => { states[i] = typeof value === 'function' ? value(states[i]) : value; }];
    },
    localStorage: {getItem: key => storage.get(key) || null, setItem: (key, value) => storage.set(key, value)},
    crypto: {randomUUID: () => 'ui-review-' + (++reviewSequence)},
    REVIEW_ID_KEY: 'review-id', REVIEW_DRAFT_KEY: 'draft', REVIEW_SUBMITTED_KEY: 'submitted',
    COMPLETION_VERSION: 'v2', SIGNUP_ENDPOINT: 'mock',
    fetch: async (url, options) => {
      const payload = JSON.parse(options.body);
      requests.push(payload);
      if (failRequest) throw Error('Offline');
      const result = post(payload);
      if (loseResponse) throw Error('Response lost after save');
      return {text: async () => result};
    },
    ...Object.fromEntries(['LessonHeader', 'Takeaway', 'StudentReviewsList', 'ActivityButton', 'BodyP', 'InnerCard', 'LessonRule', 'NextLessonGate'].map(name => [name, name]))
  };
  vm.createContext(context);
  vm.runInContext(html.slice(html.indexOf('function getOrCreateReviewId('), html.indexOf('// Typography tokens for static content boxes')), context);
  vm.runInContext(source, context);
  const flatten = node => [node, ...node.children.flatMap(child => child && typeof child === 'object' ? flatten(child) : [])];
  return {
    requests,
    setOffline: value => { failRequest = value; },
    setResponseLost: value => { loseResponse = value; },
    render() { cursor = 0; return flatten(context.ReviewsSection({})); }
  };
}
const node = (ui, predicate) => ui.render().find(predicate);
const click = (ui, label) => node(ui, n => n.type === 'ActivityButton' && n.children.includes(label)).props.onClick();
const field = (ui, id, value) => node(ui, n => n.props.id === id).props.onChange({target: {value}});
const settle = () => new Promise(resolve => setImmediate(resolve));
(async () => {
  let ui = client();
  assert.ok(node(ui, n => n.type === 'StudentReviewsList'));
  assert.equal(ui.render().filter(n => n.type === 'textarea').length, 2);
  assert.equal(ui.render().filter(n => n.props.role === 'radiogroup').length, 1);
  assert.equal(node(ui, n => n.type === 'ActivityButton' && n.children.includes('Submit my review')).props.disabled, true);
  assert.ok(node(ui, n => n.children.includes('Pick a rating')));
  assert.equal(node(ui, n => n.props.id === 'review-testimonial').props.placeholder, 'One or two sentences is plenty.');
  assert.equal(node(ui, n => n.props.id === 'review-improvement').props.placeholder, 'Just for us. We won’t publish it.');
  click(ui, 'Submit my review');
  assert.equal(ui.requests.length, 0);
  assert.match(node(ui, n => n.props.role === 'alert').children[0], /star rating/);
  node(ui, n => n.props['aria-label'] === '4 out of 5').props.onClick();
  assert.equal(node(ui, n => n.type === 'ActivityButton' && n.children.includes('Submit my review')).props.disabled, false);
  assert.equal(node(ui, n => n.props.role === 'status').children[0], '4 out of 5');
  ui = client(); // Reload with the saved draft.
  assert.equal(node(ui, n => n.props['aria-label'] === '4 out of 5').props['aria-checked'], true);
  ui.setOffline(true);
  click(ui, 'Submit my review');
  await settle();
  assert.match(node(ui, n => n.props.role === 'alert').children[0], /still saved/);
  ui.setOffline(false);
  ui.setResponseLost(true);
  click(ui, 'Try again');
  await settle();
  assert.equal(reviews.rows.filter(r => r[2] === 'ui-review').length, 1);
  ui.setResponseLost(false);
  click(ui, 'Try again');
  await settle();
  assert.equal(reviews.rows.filter(r => r[2] === 'ui-review').length, 1);
  assert.ok(ui.requests.every(r => r.reviewId === 'ui-review'));
  assert.equal(storage.get('submitted'), 'ui-review');
  assert.ok(node(ui, n => n.children.includes('Write another review')));
  assert.ok(!node(ui, n => n.children.includes('Edit my review')));
  assert.equal(node(ui, n => n.type === 'StudentReviewsList').props.refreshKey, 1);
  for (const key of ['confidenceBefore', 'confidenceAfter', 'mostUseful', 'changedBehavior']) assert.ok(!(key in ui.requests[0]));
  const originalRow = reviews.rows.find(r => r[2] === 'ui-review').slice();
  const summaryBeforeAnother = getPublic().ratingSummary;
  ui = client(); // The thank-you state survives reload.
  click(ui, 'Write another review');
  const secondId = storage.get('review-id');
  assert.notEqual(secondId, 'ui-review');
  assert.equal(JSON.parse(storage.get('draft')).usefulnessRating, 0);
  assert.equal(node(ui, n => n.props.id === 'review-testimonial').props.value, '');
  assert.equal(node(ui, n => n.props.id === 'review-improvement').props.value, '');
  assert.equal(node(ui, n => n.type === 'ActivityButton' && n.children.includes('Submit my review')).props.disabled, true);
  ui = client(); // Blank form and fresh review ID survive reload too.
  assert.ok(node(ui, n => n.children.includes('Pick a rating')));
  node(ui, n => n.props['aria-label'] === '2 out of 5').props.onClick();
  field(ui, 'review-testimonial', 'Useful practice');
  assert.ok(!node(ui, n => n.props['aria-label'] === 'Quote permission'));
  assert.ok(!node(ui, n => n.props.id === 'review-public-name'));
  const publicationNotice = 'Your review will appear publicly with your first name or nickname. Your suggestions for improvement stay private.';
  assert.equal(node(ui, n => n.props.id === 'review-publication-notice').children[0], publicationNotice);
  assert.ok(ui.render().findIndex(n => n.props.id === 'review-publication-notice') < ui.render().findIndex(n => n.type === 'ActivityButton' && n.children.includes('Submit my review')));
  field(ui, 'review-improvement', 'More examples');
  click(ui, 'Submit my review');
  await settle();
  assert.equal(ui.requests[0].reviewId, secondId);
  const secondRow = reviews.rows.find(r => r[2] === secondId);
  assert.deepEqual(secondRow.slice(6), ['More examples', 'Useful practice', 'first_name', 'Pat']);
  assert.deepEqual(reviews.rows.find(r => r[2] === 'ui-review'), originalRow);
  assert.equal(getPublic().ratingSummary.total, summaryBeforeAnother.total + 1);
  assert.ok(Math.abs(getPublic().ratingSummary.average - (summaryBeforeAnother.average * summaryBeforeAnother.total + 2) / (summaryBeforeAnother.total + 1)) < 1e-10);
  click(ui, 'Write another review');
  assert.equal(node(ui, n => n.props.id === 'review-testimonial').props.value, '');
  assert.equal(node(ui, n => n.props.id === 'review-improvement').props.value, '');
  assert.deepEqual(reviews.rows.find(r => r[2] === secondId).slice(6), ['More examples', 'Useful practice', 'first_name', 'Pat']);
  // Old draft permission values do not override the notice on an explicit submission.
  for (const permission of ['none', 'anonymous']) {
    storage.delete('submitted');
    storage.set('review-id', 'draft-' + permission);
    storage.set('draft', JSON.stringify({usefulnessRating: 4, testimonial: 'Old draft', quotePermission: permission, quoteFirstName: 'Old stored name'}));
    ui = client({studentId: 'student', firstName: 'Nickname'});
    ui.render();
    assert.equal(ui.requests.length, 0);
    click(ui, 'Submit my review');
    await settle();
    assert.deepEqual(reviews.rows.find(r => r[2] === 'draft-' + permission).slice(7), ['Old draft', 'first_name', 'Nickname']);
  }
  // A profile without a saved name can provide a nickname on a new review.
  click(ui, 'Write another review');
  const thirdId = storage.get('review-id');
  ui = client({studentId: 'student'});
  node(ui, n => n.props['aria-label'] === '4 out of 5').props.onClick();
  field(ui, 'review-testimonial', 'Review without a saved name');
  field(ui, 'review-public-name', '');
  click(ui, 'Submit my review');
  assert.equal(ui.requests.length, 0);
  assert.match(node(ui, n => n.props.role === 'alert').children[0], /first name or nickname/);
  field(ui, 'review-public-name', 'Nick');
  click(ui, 'Submit my review');
  await settle();
  assert.equal(reviews.rows.find(r => r[2] === thirdId)[9], 'Nick');
  await testPublicUI();
  console.log('PASS: public field allowlist, all-rating consent filtering, ordering, pagination, edits/withdrawals, feed refresh/retry/scroll, form, drafts, compact/legacy layouts, enrollment, and certificates.');
})().catch(error => { console.error(error); process.exitCode = 1; });

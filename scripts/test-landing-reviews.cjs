// Exercise review loading failures without contacting the public feed.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');

class Element {
  constructor() { this.children = []; this.listeners = {}; this.hidden = false; this.className = ''; }
  set textContent(value) { this.text = value; this.children = []; }
  get textContent() { return this.text || ''; }
  setAttribute() {}
  append(...children) { children.forEach(child => { child.parent = this; this.children.push(child); }); }
  replaceChildren(...children) { this.children = []; this.append(...children); }
  remove() { this.parent.children = this.parent.children.filter(child => child !== this); }
  querySelector(selector) { return this.children.find(child => child.className.split(' ').includes(selector.slice(1))); }
  get classList() { return {add: name => { this.className += ' ' + name; }}; }
  addEventListener(name, callback) { this.listeners[name] = callback; }
}

async function main() {
  const elements = Object.fromEntries(['review-list', 'review-summary', 'review-retry', 'review-more'].map(id => [id, new Element()]));
  const requests = [];
  let fail = true;
  const context = {
    document: {getElementById: id => elements[id], createElement: () => new Element()},
    AbortController, setTimeout, clearTimeout,
    fetch: async url => {
      const cursor = new URL(url).searchParams.get('cursor');
      requests.push(cursor);
      if (fail) throw Error('Temporary connection failure');
      return {ok: true, json: async () => ({reviews: [{text: cursor ? 'Older review' : 'Newest review', rating: 5, name: 'Student'}], nextCursor: cursor ? null : 'page-2', ratingSummary: {total: 2, average: 5}})};
    }
  };
  vm.createContext(context);
  vm.runInContext(fs.readFileSync(path.join(__dirname, '..', 'landing.js'), 'utf8'), context);
  await new Promise(resolve => setImmediate(resolve));
  const list = elements['review-list'], retry = elements['review-retry'], more = elements['review-more'];
  assert.equal(retry.hidden, false, 'An initial failure offers a retry');
  assert.equal(elements['review-summary'].hidden, true);
  fail = false;
  await retry.listeners.click();
  const original = list.querySelector('.review');
  assert.ok(original, 'Initial retry displays a review');
  fail = true;
  await more.listeners.click();
  assert.equal(list.querySelector('.review'), original, 'Pagination failure preserves loaded reviews');
  assert.equal(elements['review-summary'].hidden, false, 'Pagination failure preserves the rating summary');
  assert.equal(retry.hidden, false);
  await retry.listeners.click();
  assert.equal(list.children.filter(child => child.className.includes('review-load-error')).length, 1, 'Repeated failures do not duplicate the error');
  fail = false;
  await retry.listeners.click();
  assert.deepEqual(requests, [null, null, 'page-2', 'page-2', 'page-2'], 'Retry requests the failed page');
  assert.equal(list.children.length, 2, 'Retry adds the older review without duplicating existing reviews');
  assert.equal(list.querySelector('.review-load-error'), undefined);
  assert.equal(more.hidden, true);
  assert.equal(retry.hidden, true);
  console.log('PASS: first-load recovery, retained reviews and rating summary, repeated pagination failures, and cursor-specific retry.');
}
main().catch(error => { console.error(error); process.exitCode = 1; });

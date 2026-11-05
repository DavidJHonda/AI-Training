// Exercise the actual entry script in the document Vercel serves at the root.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.join(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const script = html.match(/<script id="main-entry-route">([\s\S]*?)<\/script>/)[1];
assert.ok(html.indexOf('id="main-entry-route"') < html.indexOf('<body'), 'Route before rendering enrollment');
const config = JSON.parse(fs.readFileSync(path.join(root, 'vercel.json'), 'utf8'));
assert.equal(config.rewrites.find(rule => rule.source === '/' && !rule.has).destination, '/index.html', 'Local root routing must match Vercel filesystem precedence');

for (const [label, url, name, blocked, expected] of [
  ['new visitor', 'https://example.com/', null, false, '/landing.html'],
  ['returning learner', 'https://example.com/', 'Alex', false, '/course'],
  ['blocked storage', 'https://example.com/', null, true, '/landing.html'],
  ['cleared name', 'https://example.com/', '', false, '/landing.html'],
  ['campaign and fragment', 'https://example.com/?utm_source=newsletter#meet-nate-and-luke', null, false, '/landing.html?utm_source=newsletter#meet-nate-and-luke'],
  ['direct course', 'https://example.com/course', 'Alex', false, null],
  ['legacy course bookmark', 'https://example.com/index.html', 'Alex', false, null],
  ['guest sample', 'https://example.com/course/why-learn-ai', null, false, null],
  ['print', 'https://example.com/?print=welcome', 'Alex', false, null],
  ['review', 'https://example.com/?review=closing-boards', null, false, null],
  ['file preview', 'file:///index.html', 'Alex', false, null],
]) {
  const navigations = [];
  const location = new URL(url);
  location.replace = destination => navigations.push(destination);
  const saved = new Map([
    ['llm-user-name', name],
    ['llm-explorer-progress', '{"activeSection":"tokens","completed":["welcome"]}'],
  ]);
  // Only reads are exposed: a storage mutation fails the test.
  vm.runInNewContext(script, {
    location, URLSearchParams,
    localStorage: { getItem(key) { if (blocked) throw Error('Storage blocked'); return saved.get(key); } },
  });
  assert.deepEqual(navigations, expected ? [expected] : [], label);
  console.log('PASS: ' + label);
}
const landing = fs.readFileSync(path.join(root, 'landing.html'), 'utf8');
assert.ok(!landing.includes('location.replace('), 'Explicit introduction stays accessible to returning learners');
assert.ok(html.includes('const introductionUrl = filePreview ? "landing.html" : "/landing.html";'));
console.log('PASS: introduction link has no redirect loop');

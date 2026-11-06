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
  ['LLM sample', 'https://example.com/course/whats-an-llm', null, false, null],
  ['guest sample', 'https://example.com/course/why-learn-ai', null, false, null],
  ['public groups', 'https://example.com/course/for-groups', null, false, null],
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

// Exercise sample selection for hosted URLs, local files, and old bookmarks.
const sampleHelpers = html.slice(html.indexOf('function getSampleSection('), html.indexOf('function BodyP('));
for (const [url, expected] of [
  ['https://example.com/course/whats-an-llm', 'aihistory'],
  ['https://example.com/course/whats-an-llm/?utm_source=test', 'aihistory'],
  ['file:///course/index.html?sample=whats-an-llm', 'aihistory'],
  ['https://example.com/course/why-learn-ai', 'whydeeper'],
  ['file:///course/index.html?sample=why-learn-ai', 'whydeeper'],
  ['https://example.com/course/for-groups', 'forgroups'],
  ['https://example.com/course/for-groups/?utm_source=test', 'forgroups'],
  ['file:///course/index.html?sample=for-groups', 'forgroups'],
  ['https://example.com/course?sample=whats-an-llm', null],
  ['https://example.com/whats-an-llm', null],
  ['https://example.com/course/unknown', null],
]) {
  const actual = vm.runInNewContext(sampleHelpers + '\ngetSampleSection(location)', { URLSearchParams, location: new URL(url) });
  assert.equal(actual, expected, url);
  if (expected && url.startsWith('https:')) {
    const route = new URL(url).pathname.replace(/\/$/, '');
    assert.equal(config.rewrites.find(rule => rule.source === route).destination, '/index.html');
  }
}
console.log('PASS: new sample, old bookmarks, local-file preview, and exact route matching');

// Run the actual LAB with React hook stubs to verify preview state isolation.
const labSource = html.slice(html.indexOf('function ContinueTheStoryLab('), html.indexOf('function ThreeMythsBox('));
for (const sample of [true, false]) {
  const saved = new Map([
    ['llm-lab-story-steps', '{"0":true}'],
    ['llm-explorer-progress', '{"activeSection":"tokens","completed":["welcome"]}'],
  ]);
  const original = new Map(saved);
  const writes = [];
  let initialized = false;
  let state;
  const context = {
    URLSearchParams, LessonContext: {},
    useContext: () => ({ sample }),
    useState(initial) {
      if (!initialized) { state = typeof initial === 'function' ? initial() : initial; initialized = true; }
      return [state, next => { state = next; }];
    },
    localStorage: {
      getItem: key => saved.get(key),
      setItem: (key, value) => { writes.push(key); saved.set(key, value); },
    },
    React: { createElement: (type, props, ...children) => ({ type, props, children }) },
    InteractiveBox: 'box', ActivityCounter: 'counter', LabStepList: 'steps',
  };
  vm.createContext(context);
  vm.runInContext(sampleHelpers + labSource, context);
  const render = () => vm.runInContext('ContinueTheStoryLab({})', context);
  let lab = render();
  let steps = lab.children.find(child => child && child.type === 'steps');
  assert.equal(!!steps.props.checked[0], !sample, 'Only enrolled course reads saved LAB checkmarks');
  steps.props.onToggle(1);
  lab = render();
  steps = lab.children.find(child => child && child.type === 'steps');
  assert.equal(steps.props.checked[1], true, 'Checkbox works in both modes');
  assert.equal(saved.get('llm-explorer-progress'), original.get('llm-explorer-progress'));
  if (sample) {
    assert.deepEqual(saved, original, 'Preview must leave all saved progress untouched');
    assert.deepEqual(writes, []);
    assert.ok(lab.children.some(child => child && child.type === 'p' && child.children.join('').includes('temporary')));
  } else {
    assert.deepEqual(writes, ['llm-lab-story-steps']);
    assert.deepEqual(JSON.parse(saved.get('llm-lab-story-steps')), { 0: true, 1: true });
  }
}
console.log('PASS: preview LAB checkmarks work without reading or overwriting saved course/LAB progress');

const localLinks = new Map([
  ['/course', { href: '/course' }],
  ['/course/whats-an-llm', { href: '/course/whats-an-llm' }],
  ['/course/why-learn-ai', { href: '/course/why-learn-ai' }],
  ['/course/for-groups', { href: '/course/for-groups' }],
]);
vm.runInNewContext(fs.readFileSync(path.join(root, 'start-course.js'), 'utf8'), {
  location: new URL('file:///course/landing.html'),
  localStorage: { getItem: () => null },
  window: { addEventListener() {} },
  document: { querySelectorAll(selector) {
    const route = selector.match(/^a\[href="([^" ]+)"\]$/)?.[1];
    return localLinks.has(route) ? [localLinks.get(route)] : [];
  } },
});
assert.equal(localLinks.get('/course').href, 'index.html');
assert.equal(localLinks.get('/course/whats-an-llm').href, 'index.html?sample=whats-an-llm');
assert.equal(localLinks.get('/course/why-learn-ai').href, 'index.html?sample=why-learn-ai');
assert.equal(localLinks.get('/course/for-groups').href, 'index.html?sample=for-groups');
console.log('PASS: Finder preview rewrites sample, group directory, and course entry links correctly');

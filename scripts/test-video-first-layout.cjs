// Exercise the actual lesson components without starting timers, media, or network requests.
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const root = path.join(__dirname, '..');
function loadCourse(html) {
  const React = {
    Component: class {}, Fragment: 'fragment',
    createElement(type, props, ...children) {
      return { type, props: { ...props, children: children.length === 1 ? children[0] : children } };
    },
    useState: initial => [typeof initial === 'function' ? initial() : initial, () => {}],
    useEffect() {}, useRef: current => ({ current }), useContext: () => ({}),
    createContext: () => ({ Provider: 'provider' }), isValidElement: element => !!element?.type,
    cloneElement(element, props, ...children) {
      return { type: element.type, props: { ...element.props, ...props, ...(children.length ? { children } : {}) } };
    },
  };
  const context = {
    React, ReactDOM: { createRoot: () => ({ render() {} }) }, URLSearchParams,
    Math: Object.assign(Object.create(Math), { random: () => 0.5 }),
    window: { location: { search: '', protocol: 'http:', pathname: '/course' },
      addEventListener() {}, removeEventListener() {}, innerWidth: 1200, matchMedia: () => ({ matches: false }) },
    document: { getElementById: () => null },
    localStorage: { getItem: () => null, setItem() { throw Error('Rendering must not save progress'); } },
    setTimeout() {}, clearTimeout() {}, console,
  };
  vm.createContext(context);
  vm.runInContext(fs.readFileSync(path.join(root, 'group-activities-data.js'), 'utf8'), context);
  const script = html.slice(html.indexOf('const {\n  useState'), html.lastIndexOf('</script>'));
  vm.runInContext(script, context);
  return { context, ...vm.runInContext('({sections: SECTION_COMPONENTS, videos: LESSON_VIDEOS, reading: LessonReading, player: WatchPlayer})', context) };
}
const boundaries = new Set(['LessonHeader', 'WatchOverview', 'WatchPlayer', 'LessonReading', 'InteractiveBox', 'GroupExercise', 'StandaloneGroupExercise', 'NextLessonGate']);
function collect(node, stop = boundaries, output = []) {
  if (node == null || typeof node === 'boolean') return output;
  if (Array.isArray(node)) { node.forEach(child => collect(child, stop, output)); return output; }
  if (typeof node !== 'object') { output.push({ text: String(node) }); return output; }
  if (typeof node.type === 'function') {
    if (stop.has(node.type.name)) { output.push(node); return output; }
    return collect(node.type(node.props), stop, output);
  }
  output.push(node);
  return collect(node.props.children, stop, output);
}
const current = loadCourse(fs.readFileSync(path.join(root, 'index.html'), 'utf8'));
const named = (nodes, name) => nodes.filter(node => node.type?.name === name);
let lessonCount = 0;
for (const [id, lesson] of Object.entries(current.sections)) {
  const nodes = collect(lesson({}));
  const readings = named(nodes, 'LessonReading');
  const hasVideo = !!current.videos[id] && !current.videos[id].comingSoon;
  assert.equal(readings.length, hasVideo ? 1 : 0, id + ': reading disclosure matches actual opening video');
  if (!hasVideo) continue;
  lessonCount++;
  const reading = readings[0];
  assert.equal(reading.props.sectionId, id);
  const contents = collect(reading.props.children);
  for (const name of ['InteractiveBox', 'GroupExercise', 'StandaloneGroupExercise', 'NextLessonGate', 'WatchPlayer', 'WatchOverview']) {
    assert.equal(named(contents, name).length, 0, id + ': ' + name + ' must remain outside collapsed reading');
  }
  const header = named(nodes, 'LessonHeader')[0];
  const headerNodes = collect(header.type(header.props), new Set(['WatchPlayer']));
  const players = named(headerNodes, 'WatchPlayer');
  assert.equal(players.length, 1, id + ': one immediately visible lesson player');
  assert.equal(players[0].props.video.src, current.videos[id].src);
  const nativeVideos = collect(current.player(players[0].props)).filter(node => node.type === 'video');
  assert.equal(nativeVideos.length, 1);
  assert.equal(nativeVideos[0].props.autoPlay, false, id + ': no autoplay');
  assert.equal(nativeVideos[0].props.preload, 'metadata', id + ': no full preloading');
  const closed = collect(current.reading(reading.props), new Set());
  assert.equal(closed.find(node => node.props?.className === 'lesson-reading-content').props.hidden, true);
  assert.equal(closed.find(node => node.type === 'button').props['aria-expanded'], false);
  current.context.window.location.search = '?print=lesson:' + id;
  const printTree = collect(current.reading(reading.props), new Set());
  assert.ok(!printTree.some(node => node.props?.className === 'lesson-reading-content'), id + ': print content has no collapsed wrapper');
  current.context.window.location.search = '';
  const readingIndex = nodes.indexOf(reading);
  assert.ok(nodes.findIndex(node => node.type?.name === 'NextLessonGate') > readingIndex, id + ': navigation stays reachable');
  for (const activity of named(nodes, 'InteractiveBox')) assert.ok(nodes.indexOf(activity) > readingIndex, id + ': practice follows reading');
}
assert.equal(lessonCount, Object.keys(current.videos).length);
console.log('PASS: ' + lessonCount + ' video lessons have a visible paused player, collapsed reading, and accessible activities/navigation.');
console.log('PASS: lessons without opening videos retain expanded content; all reading stays expanded for print exports.');

// Optional migration audit compares the real teaching text/images/activity definitions
// with a pre-change source file, ignoring presentation wrappers and video controls.
if (process.argv[2]) {
  const before = loadCourse(fs.readFileSync(process.argv[2], 'utf8'));
  function signature(course, id) {
    const stop = new Set(['LessonHeader', 'WatchOverview', 'WatchPlayer', 'InteractiveBox', 'GroupExercise', 'StandaloneGroupExercise', 'NextLessonGate']);
    // Unwrap disclosures instead of rendering their label or hidden state.
    function unwrap(node) {
      if (node == null || typeof node !== 'object') return node;
      if (Array.isArray(node)) return node.map(unwrap);
      if (node.type?.name === 'LessonReading') return unwrap(node.props.children);
      if (node.props?.className === 'lesson-video-expanded no-print') return null;
      if (typeof node.type === 'function' && !stop.has(node.type.name)) return unwrap(node.type(node.props));
      return { ...node, props: { ...node.props, children: unwrap(node.props.children) } };
    }
    return collect(unwrap(course.sections[id]({})), stop).flatMap(node => {
      if (node.text != null) return ['text:' + node.text];
      if (node.type === 'img') return ['image:' + node.props.src + ':' + node.props.alt];
      if (['InteractiveBox', 'GroupExercise', 'StandaloneGroupExercise'].includes(node.type?.name)) {
        return ['activity:' + JSON.stringify(node.props, (key, value) => typeof value === 'function' ? value.name : value)];
      }
      return [];
    }).sort();
  }
  for (const id of Object.keys(current.sections)) {
    const actual = signature(current, id), expected = signature(before, id);
    if (JSON.stringify(actual) !== JSON.stringify(expected)) {
      console.log(id, 'added', actual.filter(x => !expected.includes(x)), 'removed', expected.filter(x => !actual.includes(x)));
    }
    assert.deepEqual(actual, expected, id + ': preserve teaching text, images, and activities');
  }
  console.log('PASS: all 57 lesson pages preserve teaching text, images, and activity definitions compared with the pre-migration source.');
}

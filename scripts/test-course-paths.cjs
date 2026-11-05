// Verify the agreed selection against the shared catalog without launching UI.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const catalog = html.slice(html.indexOf('const SECTION_GROUPS ='), html.indexOf('// Opener sections all share'));
const {paths, groups, sections, required, selected, getPath} = vm.runInNewContext(catalog +
  '\n({paths: COURSE_PATHS, groups: SECTION_GROUPS, sections: SECTIONS, required: REQUIRED_SECTIONS, selected: ESSENTIAL_SECTION_IDS, getPath: getCoursePath})');
const plain = value => JSON.parse(JSON.stringify(value));

assert.deepEqual(plain(paths.full.groups), plain(groups));
assert.deepEqual(plain(paths.full.sections), plain(sections));
assert.deepEqual(plain(paths.full.requiredSections), plain(required));
assert.equal(paths.full.sections.length, 57);
assert.equal(paths.full.requiredSections.length, 54);
assert.equal(new Set(selected).size, selected.length, 'No duplicate Essential IDs');
for (const id of selected) assert.ok(sections.some(section => section.id === id), 'Known lesson: ' + id);

assert.deepEqual(Array.from(paths.essentials.sections, section => section.label), [
  'Welcome',
  'What Is AI?', 'AI is Different', 'What’s an LLM?', 'Does AI Think?', 'Does School Matter?', 'Learn with AI',
  'Where AI Works Best', 'Questions Matter', 'Prompting Matters', 'Context Matters', 'Evaluation Matters', 'Beyond the First Answer',
  'How AI Learns',
  'Hallucination', 'Document Trap', 'Flattery Trap', 'Support Trap', 'Fake Trap',
  'Big Downside', 'Big Upside', 'Rise of Agents', 'Work Changes',
  'Critical Thinking', 'Honesty & Privacy',
  'Five Big Ideas'
]);
assert.equal(paths.essentials.requiredSections.length, 26, '24 lessons plus introduction and finish');
assert.deepEqual(Array.from(paths.essentials.groups, group => group.sections.length), [7, 6, 1, 5, 4, 2, 1]);
assert.deepEqual(plain(paths.essentials.groups.flatMap(group => group.sections)), Array.from(paths.essentials.sections, section => section.id));
for (const section of paths.essentials.sections) {
  assert.equal(section, sections.find(item => item.id === section.id), 'Both paths share metadata');
}
for (const id of [undefined, null, '', 'unknown', 'toString', '__proto__']) {
  assert.equal(getPath(id), paths.full, 'Unknown paths default to Full Course');
}
assert.equal(getPath('essentials'), paths.essentials);
assert.equal(getPath('full'), paths.full);
console.log('PASS: full-course compatibility, exact Essential selection and order, shared metadata, and safe path fallback.');

// Run: node scripts/test_quiz_feedback.cjs
// Exercise the actual shared component and its click handlers without a browser.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { test } = require('node:test');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const start = html.indexOf('function QuizBlock(props) {');
const end = html.indexOf('\nfunction ProgressBar(', start);
assert.ok(start >= 0 && end > start);

function mount(options, extraProps = {}) {
  const slots = [], answers = [];
  let cursor = 0, tree;
  const React = {
    createElement(type, props, ...children) {
      return { type, props: props || {}, children: children.flat(Infinity) };
    }
  };
  function useState(initial) {
    const index = cursor++;
    if (!(index in slots)) slots[index] = initial;
    return [slots[index], value => {
      slots[index] = typeof value === 'function' ? value(slots[index]) : value;
    }];
  }
  const QuizBlock = new Function('React', 'useState',
    html.slice(start, end) + '\nreturn QuizBlock;')(React, useState);
  const props = { surface: 'mint', options, onAnswer: (...args) => answers.push(args), ...extraProps };
  function render() {
    cursor = 0;
    tree = QuizBlock(props);
  }
  function nodes(node = tree) {
    return node && typeof node === 'object' ? [node, ...node.children.flatMap(nodes)] : [];
  }
  function text(node) {
    if (node == null || typeof node === 'boolean') return '';
    return typeof node === 'object' ? node.children.map(text).join(' ') : String(node);
  }
  function click(index) {
    nodes().filter(node => node.type === 'button')[index].props.onClick();
    render();
  }
  function feedback() {
    const zone = nodes().find(node => node.props.className === 'choicequiz-feedback');
    return zone ? text(zone) : '';
  }
  render();
  return { click, feedback, answers, nodes };
}

const options = [
  { label: 'Temporary versus permanent jobs?', correct: true, feedback: 'Construction and permanent jobs represent different benefits.' },
  { label: 'How many customers?', correct: false, feedback: 'Customer numbers do not tell you how many local jobs remain.' },
  { label: 'How big is the building?', correct: false, hint: 'Think about staffing.', feedback: 'A large building does not necessarily need a large permanent staff.' }
];

test('first wrong click shows its explanation without completing the question', () => {
  const quiz = mount(options);
  assert.equal(quiz.feedback(), '');
  quiz.click(1);
  assert.ok(quiz.feedback().includes(options[1].feedback));
  assert.ok(!quiz.feedback().includes('Look again at what this option'));
  assert.ok(!quiz.feedback().includes(options[0].feedback));
  assert.deepEqual(quiz.answers, []);
  quiz.click(1);
  assert.ok(quiz.feedback().includes(options[1].feedback));
  assert.deepEqual(quiz.answers, []);
});

test('feedback stays consistent before and after solving, including options with hints', () => {
  const quiz = mount(options);
  quiz.click(2);
  const before = quiz.feedback();
  assert.ok(before.includes(options[2].feedback));
  assert.ok(!before.includes(options[2].hint));
  quiz.click(0);
  assert.ok(quiz.feedback().includes(options[0].feedback));
  assert.deepEqual(quiz.answers, [[0, true]]);
  quiz.click(2);
  assert.equal(quiz.feedback(), before);
  quiz.click(1);
  assert.ok(quiz.feedback().includes(options[1].feedback));
  quiz.click(0);
  assert.deepEqual(quiz.answers, [[0, true]], 'Revisiting answers does not repeat completion');
});

test('hint remains available when a wrong option has no full explanation', () => {
  const quiz = mount([
    options[0],
    { label: 'Hint-only option', correct: false, hint: 'Look for the missing information.' }
  ]);
  quiz.click(1);
  assert.ok(quiz.feedback().includes('Look for the missing information.'));
  assert.deepEqual(quiz.answers, []);
});

test('a question restored as correct can still show wrong-answer feedback', () => {
  const quiz = mount(options, { picked: 0 });
  assert.ok(quiz.feedback().includes(options[0].feedback));
  quiz.click(1);
  assert.ok(quiz.feedback().includes(options[1].feedback));
  assert.deepEqual(quiz.answers, []);
});

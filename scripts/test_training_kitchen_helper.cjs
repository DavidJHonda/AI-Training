// Dependency-free behavior checks for the inline course activity.
// Run: node scripts/test_training_kitchen_helper.cjs
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const { test } = require('node:test');

const html = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
const start = html.indexOf('const KITCHEN_HELPER_ROUNDS =');
const end = html.indexOf('\nfunction TrainingSection(', start);
assert.ok(start >= 0 && end > start);
const source = html.slice(start, end);

// Render the actual component with a minimal hooks host. This tests its state
// and event handlers without a browser, network calls, or replacing its logic.
function mount() {
  const slots = [];
  let cursor = 0, pending = [], tree, completed = 0, focuses = 0;
  function useState(initial) {
    const index = cursor++;
    if (!(index in slots)) slots[index] = initial;
    return [slots[index], value => {
      slots[index] = typeof value === 'function' ? value(slots[index]) : value;
    }];
  }
  function useRef(initial) {
    const index = cursor++;
    if (!(index in slots)) slots[index] = { current: initial };
    return slots[index];
  }
  function useEffect(fn, deps) {
    const index = cursor++;
    const prior = slots[index];
    if (!prior || deps.some((value, i) => !Object.is(value, prior[i]))) pending.push(fn);
    slots[index] = deps;
  }
  const React = {
    useRef,
    createElement(type, props, ...children) {
      if (props && props.ref) props.ref.current = { focus() { focuses++; } };
      return { type, props: props || {}, children: children.flat(Infinity) };
    }
  };
  const exports = new Function('React', 'useState', 'useEffect', 'InteractiveBox', 'InnerCard', 'ActivityButton',
    source + '\nreturn { TrainingKitchenHelper, kitchenHelperProfile, KITCHEN_HELPER_ROUNDS, KITCHEN_HELPER_TESTS };')(
      React, useState, useEffect, 'InteractiveBox', 'InnerCard', 'ActivityButton');
  const props = { onComplete() { completed++; } };
  function render() {
    cursor = 0;
    pending = [];
    tree = exports.TrainingKitchenHelper(props);
    pending.forEach(fn => fn());
    return tree;
  }
  function nodes(node = tree) {
    if (!node || typeof node !== 'object') return [];
    return [node, ...node.children.flatMap(nodes)];
  }
  function text(node = tree) {
    if (node == null || typeof node === 'boolean') return '';
    if (typeof node !== 'object') return String(node);
    return node.children.map(text).join(' ');
  }
  function click(label, options = {}) {
    const button = nodes().find(node => (node.type === 'button' || node.type === 'ActivityButton') &&
      (text(node) === label || node.props['aria-label'] === label));
    assert.ok(button, 'Button exists: ' + label);
    if (!options.force) assert.ok(!button.props.disabled, 'Button is enabled: ' + label);
    button.props.onClick();
    render();
  }
  render();
  return { exports, click, text, nodes, render,
    get tree() { return tree; }, get completed() { return completed; }, get focuses() { return focuses; } };
}

test('inline JavaScript parses and old quiz is removed', () => {
  for (const m of html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
    if (!/\bsrc=|application\/ld\+json/.test(m[1])) new Function(m[2]);
  }
  assert.ok(!html.includes('TrainingWhoTaughtQuiz'));
  assert.ok(!html.includes('Notice what nobody ranked: whether it was true.'));
  assert.ok(html.includes('React.createElement(TrainingKitchenHelper, null)'));
});

test('opening instructions, safe progression, and selectable preferences', () => {
  const app = mount();
  assert.equal(app.tree.props.title, 'Train a Kitchen Helper');
  assert.equal(app.tree.props.instructions.length, 4);
  assert.match(app.tree.props.lead, /During training, people compare an LLM’s answers/);
  assert.match(app.tree.props.lead, /pretend AI called the Kitchen Helper/);
  assert.match(app.text(), /No real AI model is being trained/);
  assert.equal(app.focuses, 0, 'Does not steal focus on mount');
  app.click('Next question', { force: true });
  assert.match(app.text(), /How do I make a cheese sandwich/);
  app.click('Choose A');
  app.click('Choose B');
  assert.equal(app.nodes().filter(n => n.props['aria-pressed'] === true).length, 1);
  app.click('Next question');
  assert.match(app.text(), /How do I make a yogurt parfait/);
  assert.equal(app.focuses, 1);
  assert.equal(app.completed, 0);
});

for (let bits = 0; bits < 8; bits++) {
  const choices = [bits & 1, (bits >> 1) & 1, (bits >> 2) & 1];
  test('choices ' + choices.map(x => 'AB'[x]).join('') + ' drive both answers and an accurate reveal', () => {
    const app = mount();
    // Middle question deliberately reverses the styles.
    const stepCount = Number(choices[0] === 1) + Number(choices[1] === 0) + Number(choices[2] === 1);
    const expectedStyle = stepCount >= 2 ? 'steps' : 'short';
    const expectedCount = Math.max(stepCount, 3 - stepCount);
    choices.forEach((choice, index) => {
      app.click('Choose ' + 'AB'[choice]);
      app.click(index === 2 ? 'Try your helper' : 'Next question');
    });
    const profile = app.exports.kitchenHelperProfile(choices);
    assert.equal(profile.style, expectedStyle);
    assert.equal(profile.count, expectedCount);
    assert.equal(profile.probabilities.short + profile.probabilities.steps, 1);
    assert.match(app.text(), /Your helper is ready/);
    assert.ok(!app.text().includes('See the other style'));
    assert.equal(app.completed, 0);
    // Either test question can be asked first.
    const tests = app.exports.KITCHEN_HELPER_TESTS;
    const order = bits % 2 ? [1, 0] : [0, 1];
    order.forEach((index, position) => {
      app.click('Ask: ' + tests[index].question);
      assert.ok(app.text().includes(tests[index][expectedStyle]));
      assert.equal(app.completed, position === 0 ? 0 : 1);
      if (position === 0) assert.ok(!app.text().includes('See the other style'));
      app.click('Ask: ' + tests[index].question, { force: true });
      assert.equal(app.completed, position === 0 ? 0 : 1, 'Repeated clicks do not complete twice');
    });
    const label = expectedStyle === 'steps' ? 'descriptive answers' : 'brief answers';
    assert.ok(app.text().includes('You chose ' + label + ' in ' + expectedCount + ' of 3 rounds.'));
    const reveal = 'You chose ' + label + ' in ' + expectedCount + ' of 3 rounds.';
    const otherStyle = expectedStyle === 'steps' ? 'short' : 'steps';
    tests.forEach(test => assert.ok(!app.text().includes(test[otherStyle])));
    app.click('See the other style');
    tests.forEach(test => {
      assert.ok(app.text().includes(test[expectedStyle]), 'Original answer stays visible');
      assert.ok(app.text().includes(test[otherStyle]), 'Alternative appears');
    });
    assert.ok(app.text().includes(reveal), 'Comparison does not change preferences');
    assert.equal(app.completed, 1, 'Comparison does not complete twice');
    assert.equal(app.nodes().filter(n => n.props['aria-expanded'] === true).length, 1);
    app.click('Hide the other style');
    tests.forEach(test => assert.ok(!app.text().includes(test[otherStyle])));
    assert.ok(app.text().includes(reveal));
    app.click('See the other style');
    app.render();
    assert.equal(app.completed, 1);
    app.click('Start over');
    assert.match(app.text(), /YOUR CHOICES · 1 OF 3/);
    assert.ok(!app.text().includes('Your feedback shaped the answers'));
    assert.ok(!app.text().includes('THE OTHER STYLE'));
    assert.equal(app.nodes().filter(n => n.props['aria-pressed'] === true).length, 0);
    app.click('Next question', { force: true });
    assert.match(app.text(), /YOUR CHOICES · 1 OF 3/);
  });
}

test('descriptive answers are distinctly longer, and visible labels match the distinction', () => {
  const app = mount();
  const words = text => text.trim().split(/\s+/).length;
  for (const round of app.exports.KITCHEN_HELPER_ROUNDS) {
    const brief = round.options.find(option => option.style === 'short').text;
    const descriptive = round.options.find(option => option.style === 'steps').text;
    assert.ok(words(descriptive) >= words(brief) * 2, round.question);
  }
  for (const question of app.exports.KITCHEN_HELPER_TESTS) {
    assert.ok(words(question.steps) >= words(question.short) * 2, question.question);
  }
  assert.ok(!source.includes('step-by-step answers'));
  assert.ok(!source.includes('short answers'));
});

test('incomplete or invalid choices do not produce a profile', () => {
  const app = mount();
  [[], [0, 1], [0, null, 1], [0, 2, 1]].forEach(choices => {
    assert.equal(app.exports.kitchenHelperProfile(choices), null);
  });
});

test('restart clears the prior preference and can produce the opposite style', () => {
  const app = mount();
  const tests = app.exports.KITCHEN_HELPER_TESTS;
  for (const [choices, style] of [[[0, 1, 0], 'short'], [[1, 0, 1], 'steps']]) {
    choices.forEach((choice, i) => {
      app.click('Choose ' + 'AB'[choice]);
      app.click(i === 2 ? 'Try your helper' : 'Next question');
    });
    tests.forEach(test => app.click('Ask: ' + test.question));
    tests.forEach(test => assert.ok(app.text().includes(test[style])));
    app.click('Start over');
  }
  assert.equal(app.completed, 2);
});

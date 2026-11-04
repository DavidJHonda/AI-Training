// Preview-only scene. The course's shared GuidedDemonstration owns progression.
function GuidedDemoShell(props) {
  var shell = PreviewGuidedDemoShell(props);
  // Keep reading order aligned with the visual order: example, explanation, control.
  if (props.kind === 'training' && props.instructions) {
    return React.cloneElement(shell, null, React.Children.toArray(shell.props.children).reverse());
  }
  return shell;
}

const TRAINING_LOOP_STATES = [
  { instruction: 'The model reads text.' },
  { instruction: 'The model hides a word.' },
  { instruction: 'The model guesses the missing word.' },
  { instruction: 'The training system checks the guess against the original text.' },
  { instruction: 'The training system adjusts the model’s weights to make the original word more likely in this situation.' },
  { instruction: 'The loop repeats with another example. The model keeps the changes from earlier training.' },
  { instruction: [] }
];

function TrainingLoopScene(props) {
  var E = React.createElement, step = props.step;
  var guessed = step >= 3, checked = step >= 4, adjusted = step >= 5;
  function reserved(visible, className, children) {
    return E('div', {key:className,className: className + (visible ? '' : ' training-reserve'),
      'aria-hidden': visible ? undefined : 'true', inert: visible ? undefined : ''}, children);
  }
  function bar(label, width, detail) {
    return E('div', {className:'how-ai-learns-bar-row'},
      E('span', null, label),
      E('span', {className:'how-ai-learns-track', 'aria-hidden':'true'}, E('span', {className:'how-ai-learns-fill', style:{width:width+'%'}})),
      E('span', null, detail));
  }
  return E('div', {className:'how-ai-learns-scene', 'data-training-state':step,
    role:'group', 'aria-label':'A training example, its prediction, and the effect of an adjustment'},
    reserved(step>=1, 'how-ai-learns-text',
      E('p', {className:'how-ai-learns-sentence'}, step<=1 ? 'Peanut butter and jelly.' : 'Peanut butter and _ _ _ _ _')),
    E('div', {className:'how-ai-learns-workspace'},
    E('div', {className:'how-ai-learns-comparison'}, [
      reserved(guessed, 'how-ai-learns-result', [
        E('p', {key:'label',className:'how-ai-learns-label'}, 'Model’s guess'),
        E('p', {key:'word',className:'how-ai-learns-word'+(step===3?' training-new':'')}, 'cloud')]),
      reserved(checked, 'how-ai-learns-result is-checked', [
        E('p', {key:'label',className:'how-ai-learns-label'}, 'Original word'),
        E('p', {key:'word',className:'how-ai-learns-word'+(step===4?' training-new':'')}, 'jelly')])]),
    reserved(adjusted, 'how-ai-learns-effect', [
      E('p',{key:'weights',className:'how-ai-learns-weight-state'}, 'Weights adjusted'),
      E('p',{key:'label',className:'how-ai-learns-label'}, 'Chance of “jelly”'),
      E('div',{key:'bars',className:'how-ai-learns-bars'},
        bar('Before',28,'Less likely'),
        bar('After',44,'More likely')),
      E('p',{key:'note',className:'how-ai-learns-detail'},'Illustrative bars, not measured values.')]))
  );
}
function TrainingLoopDemo() {
  return React.createElement(GuidedDemonstration, {
    label:'The Training Loop', kind:'training', states:TRAINING_LOOP_STATES,
    renderScene:function(state,step,isPrint) {
      return React.createElement(TrainingLoopScene,{step:step,isPrint:isPrint});
    }
  });
}

// Preview-only phase demonstrations. Each state keeps its explanation with its result.
const TRAINING_PHASE_DEMOS = [
  {
    name: 'Pretraining', purpose: 'Learn patterns from large amounts of text and code.',
    contextLabel: 'Training text', context: 'Peanut butter and jelly.',
    states: [
      {title:'Start with text', explanation:'The original text supplies the answer to check against. See what the model predicts when the last word is held back.', outputs:[{label:'The model will see',text:'Peanut butter and ___'}]},
      {title:'Predict', explanation:'Using the words before the blank, the model predicts “cloud.” The prediction comes from its current weights.', outputs:[{label:'Model’s prediction',text:'Peanut butter and cloud'}]},
      {title:'Check', explanation:'The training system compares the prediction with the original word. The example says “jelly.”', outputs:[{label:'Prediction',text:'cloud'},{label:'Original word',text:'jelly'}]},
      {title:'Adjust', explanation:'The training system changes the model’s weights to make “jelly” more likely after these words. Repeating this across many examples builds language patterns.', outputs:[{label:'Prediction',text:'cloud'},{label:'Original word',text:'jelly'}], effect:'“Jelly” becomes more likely in this context.'}
    ]
  },
  {
    name:'Instruction Tuning', purpose:'Learn to follow requests using good example responses.',
    contextLabel:'Request', context:'Explain how to make a sandwich in three steps.',
    states:[
      {title:'Start with a request', explanation:'Training pairs this request with a good example answer. Follow a simplified example of predicting, comparing, and adjusting.', outputs:[{label:'The goal',text:'An answer that follows the three-step request.'}]},
      {title:'Predict', explanation:'The model predicts the response, one token at a time. Here, its response talks about sandwiches but doesn’t give the requested steps.', outputs:[{label:'Model’s response',text:'Sandwiches are a popular lunch.'}]},
      {title:'Check', explanation:'Training compares the model’s predictions with a good example response. This example shows what following the request looks like.', outputs:[{label:'Model’s response',text:'Sandwiches are a popular lunch.'},{label:'Example response',list:['Get two slices of bread.','Add the fillings.','Put the slices together.']}]},
      {title:'Adjust', explanation:'The training system changes the weights to make responses like the example more likely. Many request-and-response pairs teach the model to follow instructions.', outputs:[{label:'Example response',list:['Get two slices of bread.','Add the fillings.','Put the slices together.']}],effect:'Responses that follow the request become more likely.'}
    ]
  },
  {
    name:'Preference Tuning',purpose:'Learn from feedback about which answers are more helpful.',
    contextLabel:'Question',context:'I’ve never made a sandwich. How much peanut butter should I use?',
    states:[
      {title:'Start with a question',explanation:'There can be several answers to the same question. See two possible responses, then the feedback used to guide training.',outputs:[{label:'The goal',text:'An answer a beginner can use.'}]},
      {title:'Predict',explanation:'The model produces possible responses through prediction. Both answer the question, but they give different levels of guidance.',outputs:[{label:'Answer A',text:'Use the appropriate amount.'},{label:'Answer B',text:'Start with a tablespoon and spread it thinly.'}]},
      {title:'Check',explanation:'People compare the answers and prefer B because it gives a beginner a concrete amount. That preference supplies feedback for training.',outputs:[{label:'Answer A',text:'Use the appropriate amount.'},{label:'Answer B · Preferred',text:'Start with a tablespoon and spread it thinly.',preferred:true}]},
      {title:'Adjust',explanation:'Training uses that feedback to change the model’s weights, making answers like B more likely. Better doesn’t always mean longer—it depends on what the person needs.',outputs:[{label:'Answer B · Preferred',text:'Start with a tablespoon and spread it thinly.',preferred:true}],effect:'Helpful responses like B become more likely.'}
    ]
  }
];

function TrainingPhaseState(props) {
  const E=React.createElement, state=props.state;
  return E('div',{className:'phase-state-content'},
    E('h4',null,state.title),
    E('div',{className:'phase-outputs'},state.outputs.map((output,i)=>
      E('div',{key:i,className:'phase-output'+(output.preferred?' is-preferred':'')},
        E('p',{className:'phase-output-label'},output.label),
        output.list ? E('ol',null,output.list.map((item,j)=>E('li',{key:j},item))) : E('p',{className:'phase-output-text'},output.text)))),
    state.effect ? E('p',{className:'phase-effect'},state.effect) : null,
    E('p',{className:'phase-explanation'},state.explanation));
}

function TrainingPhasesDemo() {
  const E=React.createElement;
  const [active,setActive]=useState(0), [steps,setSteps]=useState([0,0,0]);
  const tabs=useRef([]), phase=TRAINING_PHASE_DEMOS[active], step=steps[active];
  const isPrint=new URLSearchParams(window.location.search).has('print');
  function selectPhase(index,focus) {
    setActive(index);
    if(focus && tabs.current[index]) tabs.current[index].focus();
  }
  function changeStep(value) {
    setSteps(previous=>previous.map((old,index)=>index===active?value:old));
  }
  function tabKey(event,index) {
    let next;
    if(event.key==='ArrowRight') next=(index+1)%3;
    if(event.key==='ArrowLeft') next=(index+2)%3;
    if(event.key==='Home') next=0;
    if(event.key==='End') next=2;
    if(next!==undefined){event.preventDefault();selectPhase(next,true);}
  }
  const print=E('div',{className:'phase-print'},TRAINING_PHASE_DEMOS.map((item,i)=>
    E('section',{key:i},E('h3',null,(i+1)+' · '+item.name),E('p',null,item.purpose),
      E('p',null,E('strong',null,item.contextLabel+': '),item.context),
      item.states.slice(1).map((state,j)=>E(TrainingPhaseState,{key:j,state:state})))));
  return E(React.Fragment,null,
    !isPrint ? E('div',{className:'phase-interactive'},
      E('div',{className:'phase-tabs',role:'tablist','aria-label':'Training phases'},
        TRAINING_PHASE_DEMOS.map((item,i)=>E('button',{
          key:i,type:'button',role:'tab',id:'phase-tab-'+i,'aria-selected':active===i,
          'aria-controls':'phase-panel',tabIndex:active===i?0:-1,
          ref:node=>{tabs.current[i]=node;},onClick:()=>selectPhase(i,false),onKeyDown:event=>tabKey(event,i)
        },E('span',{className:'phase-tab-number','aria-hidden':'true'},i+1),
          item.name,steps[i]===3?E('span',{className:'phase-tab-complete','aria-label':'Complete'},' ✓'):null))),
      E('section',{className:'phase-demo-panel',id:'phase-panel',role:'tabpanel','aria-labelledby':'phase-tab-'+active,'data-phase':active,'data-step':step},
        E('h3',null,phase.name),E('p',{className:'phase-purpose'},phase.purpose),
        E('div',{className:'phase-context'},E('span',null,phase.contextLabel),E('p',null,phase.context)),
        E('div',{className:'phase-state-stack'},
          phase.states.map((state,i)=>E('div',{
            key:active+'-'+i,className:i===step?'phase-state-current':'phase-state-measure',
            role:i===step?'status':undefined,'aria-live':i===step?'polite':undefined,
            'aria-atomic':i===step?'true':undefined,'aria-hidden':i===step?undefined:'true',inert:i===step?undefined:''
          },E(TrainingPhaseState,{state:state})))),
        E('div',{className:'phase-actions'},
          E(GuidedDemoControls,{key:active,done:step===3,onAdvance:()=>changeStep(Math.min(step+1,3)),onReplay:()=>changeStep(0)}),
          active<2 ? E('button',{type:'button',className:'phase-next'+(step===3?'':' phase-next-hidden'),
            tabIndex:step===3?0:-1,'aria-hidden':step===3?undefined:'true',disabled:step!==3,
            onClick:()=>selectPhase(active+1,true)},'Next phase →') : null))) : null,
    E('div',{className:isPrint?'phase-print-mode':undefined},print));
}

// Build a lesson preview and deterministic video scene from the same live source.
// node scripts/video/preview_temperature.cjs
// Open /previews/temperature.html; ?capture=1&step=3 shows only the scene.
// window.setTemperatureScene(step) selects any authored state for capture.
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
function section(start, end) {
  const a = html.indexOf(start), b = html.indexOf(end, a);
  if (a < 0 || b < 0) throw new Error('Missing component boundary: ' + start);
  return html.slice(a, b);
}
const css = [...html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)].map(m => m[1]).join('\n');
const scripts = [...html.matchAll(/<script[^>]*src="[^"]*react[^>]*><\/script>/g)].map(m => m[0]).join('\n');
const fonts = [...html.matchAll(/<link[^>]*href="https:\/\/fonts\.[^>]*>/g)].map(m => m[0]).join('\n');
const output = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Next Token · Temperature</title>${fonts}<style>${css}
main{max-width:900px;margin:32px auto;padding:0 16px}h1{font-family:var(--serif);font-size:42px;font-weight:400;margin:0 0 20px;color:var(--ink)}.capture{max-width:none;width:1280px;height:900px;margin:0;padding:0;background:var(--card);display:flex;align-items:center;justify-content:center}.capture .temperature-scene{width:900px}.capture .temperature-bar > span{transition:none}
</style></head><body><main id="preview"></main>${scripts}<script>
var useState=React.useState,useEffect=React.useEffect,useRef=React.useRef;
${section('function BodyP(', '\n// lessonId ->')}
${section('function ActivityButton(', '\nfunction FeedbackPill(')}
${section('function GuidedDemoShell(', 'var VECTOR_MAP_SEQUENCES =')}
${section('var TEMPERATURE_DATA =', 'function InferenceSection(')}
function Preview(){
 var E=React.createElement,params=new URLSearchParams(location.search),capture=params.get('capture')==='1';
 var state=useState(Math.max(0,Math.min(Number(params.get('step'))||0,TEMPERATURE_STATES.length-1))),step=state[0],setStep=state[1];
 useEffect(function(){window.setTemperatureScene=function(n){if(!Number.isInteger(n)||n<0||n>=TEMPERATURE_STATES.length)throw new Error('Invalid temperature state');setStep(n);};},[]);
 if(capture){document.getElementById('preview').className='capture';return E(TemperatureScene,{state:TEMPERATURE_STATES[step],step:step});}
 return E(React.Fragment,null,E('h1',null,'How Temperature Changes the Odds'),E(BodyP,null,'Temperature changes how concentrated or spread out the probabilities are. In chat apps, it’s already set for you behind the scenes. Watch what different settings do to the dog-name choices.'),E(TemperatureDemo));
}
ReactDOM.createRoot(document.getElementById('preview')).render(React.createElement(Preview));
</script></body></html>`;
fs.mkdirSync(path.join(root, 'previews'), {recursive:true});
fs.writeFileSync(path.join(root, 'previews/temperature.html'), output);
console.log('Generated previews/temperature.html from live components.');

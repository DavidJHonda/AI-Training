// Generates a review/capture page from the live lesson's exact components.
// Run: node scripts/video/preview_vector_space.cjs
// Serve repo root; open /previews/vector-space-maps.html.
// ?scene=cities|drinks|context isolates one scene; ?autoplay=1 advances it.
// window.setVectorScene(kind, step) is the deterministic capture interface.
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '../..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const start = html.indexOf('var VECTOR_MAP_SEQUENCES =');
const end = html.indexOf('\nfunction VectorSpaceSection(', start);
if (start < 0 || end < 0) throw new Error('Vector Space component boundaries missing');
const styles = [...html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)].map(m => m[1]).join('\n');
const scripts = [...html.matchAll(/<script[^>]*src="[^"]*react[^>]*><\/script>/g)].map(m => m[0]).join('\n');
const fonts = [...html.matchAll(/<link[^>]*href="https:\/\/fonts\.[^>]*>/g)].map(m => m[0]).join('\n');
const bodyStart = html.indexOf('function BodyP(');
const bodyEnd = html.indexOf('\n// lessonId ->', bodyStart);
if (bodyStart < 0 || bodyEnd < 0) throw new Error('BodyP boundaries missing');
const buttonStart = html.indexOf('function ActivityButton(');
const buttonEnd = html.indexOf('\nfunction FeedbackPill(', buttonStart);
const result = `<!doctype html><html lang="en"><head><base href="../"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vector Space · map sequences</title>${fonts}<style>${styles}
body{margin:0;background:var(--bg);font-family:var(--sans)}main{max-width:900px;margin:32px auto;padding:0 16px}.preview-tools{display:flex;flex-wrap:wrap;gap:12px;align-items:center;margin-bottom:20px}.preview-tools button{font:inherit;padding:10px 18px;border:1px solid var(--rule);border-radius:8px;background:var(--card);cursor:pointer}.capture{max-width:none;margin:0;padding:0;width:1280px;height:720px;background:var(--card);display:flex;align-items:center;justify-content:center}.capture .vs-map-demo{display:flex;flex-direction:column;width:1280px;height:720px;margin:0;border-radius:20px;box-sizing:border-box}.capture .vs-map-panel{flex:1;min-height:0}.capture .vs-map-frame{width:100%;height:100%;box-sizing:border-box}.capture .vs-map-svg{height:100%;width:100%}.capture .vs-map-caption,.capture .vs-map-note{display:none}.capture .vs-map-reveal{animation:none}.capture > img{max-width:100%!important;max-height:100%;width:auto!important;margin:0!important;object-fit:contain}.capture .vs-map-caption{min-height:0;font-size:20px;margin:12px 0}.capture .vs-map-note{font-size:15px}
</style></head><body><main id="preview"></main>${scripts}<script>
var useState=React.useState,useEffect=React.useEffect;
${html.slice(bodyStart, bodyEnd)}
${html.slice(buttonStart, buttonEnd)}
${html.slice(start, end)}
function Preview(){
 var E=React.createElement,params=new URLSearchParams(location.search),single=params.get('scene');
 var initialKind=VECTOR_MAP_SEQUENCES[single]?single:'cities';
 var initialStep=Math.max(0,Math.min(Number(params.get('step'))||0,VECTOR_MAP_SEQUENCES[initialKind].labels.length));
 var state=useState({kind:initialKind,step:initialStep}),value=state[0],set=state[1];
 var playing=useState(params.get('autoplay')==='1'),auto=playing[0],setAuto=playing[1];
 useEffect(function(){window.setVectorScene=function(kind,step){if(!VECTOR_MAP_SEQUENCES[kind]||step<0||step>VECTOR_MAP_SEQUENCES[kind].labels.length)throw new Error('Invalid map state');setAuto(false);set({kind:kind,step:step});};},[]);
 useEffect(function(){if(!auto)return;var id=setTimeout(function(){if(value.step<VECTOR_MAP_SEQUENCES[value.kind].labels.length)set({kind:value.kind,step:value.step+1});else setAuto(false);},3000);return function(){clearTimeout(id);};},[auto,value]);
 if(params.get('capture')==='1'){document.getElementById('preview').className='capture';return value.kind==='context'?E(VectorContextIllustration,null):E(VectorMapBox,{kind:value.kind,label:VECTOR_MAP_SEQUENCES[value.kind].title,quiet:true},E(VectorMapFrame,{kind:value.kind,step:value.step,quiet:true}));}
 var config=VECTOR_MAP_SEQUENCES[value.kind];
 var controls=E(VectorMapControls,{config:config,step:value.step,
 onAdvance:function(){setAuto(false);set({kind:value.kind,step:value.step+1});},
 onReplay:function(){setAuto(false);set({kind:value.kind,step:0});},
 onPlay:function(){set({kind:value.kind,step:0});setAuto(true);}});
 return E(React.Fragment,null,E('div',{className:'preview-tools'},E('a',{href:'../index.html'},'Back to course'),['cities','drinks','context'].map(function(k){return E('button',{key:k,onClick:function(){setAuto(false);set({kind:k,step:0});}},VECTOR_MAP_SEQUENCES[k].title);})),
 config.intro ? E(BodyP,null,config.intro) : null,
 value.kind === 'context' ? E(VectorContextIllustration,null) : E(VectorMapBox,{kind:value.kind,label:config.title,instructions:config.instructions?config.captions[value.step]:null,instructionOptions:config.captions,controls:controls},E(VectorMapFrame,{kind:value.kind,step:value.step})));

}
ReactDOM.createRoot(document.getElementById('preview')).render(React.createElement(Preview));
</script></body></html>`;
fs.mkdirSync(path.join(root, 'previews'), {recursive:true});
fs.writeFileSync(path.join(root, 'previews/vector-space-maps.html'), result);
console.log('Generated previews/vector-space-maps.html from index.html');

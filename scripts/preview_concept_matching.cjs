// Rebuild a review preview directly from the live lesson components.
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
function section(start,end){const a=html.indexOf(start),b=html.indexOf(end,a);if(a<0||b<0)throw Error('Missing source boundary: '+start);return html.slice(a,b);}
const css=[...html.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)].map(m=>m[1]).join('\n');
const scripts=[...html.matchAll(/<script[^>]*src="[^"]*react[^>]*><\/script>/g)].map(m=>m[0]).join('\n');
const fonts=[...html.matchAll(/<link[^>]*href="https:\/\/fonts\.[^>]*>/g)].map(m=>m[0]).join('\n');
const output=`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Understand AI · Match the Concepts</title>${fonts}<style>${css}
main{max-width:980px;margin:32px auto;padding:0 16px}
</style></head><body><main id="preview"></main>${scripts}<script>
var useState=React.useState,useEffect=React.useEffect,useRef=React.useRef;
${section('function BodyP(', '\n// lessonId ->')}
${section('function SectionKicker(', 'function ShowcaseBox(')}
${section('function ActivityInstructions(', 'function GroupExercise(')}
${section('function ActivityButton(', 'function FeedbackPill(')}
${section('var UNDERSTAND_AI_CONCEPTS =', 'function PredictionLoopTryIt(')}
ReactDOM.createRoot(document.getElementById('preview')).render(React.createElement(MatchTermsTryIt));
</script></body></html>`;
fs.writeFileSync(path.join(root,'previews/concept-matching.html'),output);
console.log('Generated previews/concept-matching.html from live components.');

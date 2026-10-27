// Local review only. Reads the course components; writes only the separate preview.
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const source = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
function section(start, end) {
  const a = source.indexOf(start), b = source.indexOf(end, a);
  if (a < 0 || b < 0) throw new Error('Missing component boundary: ' + start);
  return source.slice(a, b);
}
const css = [...source.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/g)].map(m => m[1]).join('\n');
const fonts = [...source.matchAll(/<link[^>]*href="https:\/\/fonts\.[^>]*>/g)].map(m => m[0]).join('\n');
const scripts = [...source.matchAll(/<script[^>]*src="[^"]*react[^>]*><\/script>/g)].map(m => m[0]).join('\n');
const shared = [
  section('function BodyP(', '\n// lessonId ->'),
  section('function SectionKicker(', 'function ShowcaseBox('),
  section('function InnerCard(', 'function ActivityCounter('),
];
// Extract only the components this preview uses; no course routing, storage, or analytics.
const output = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow"><title>Training · Lesson preview</title>
${fonts}<style>${css}
body{margin:0;background:var(--bg);font-family:var(--sans);color:var(--ink)}
.preview-note{background:var(--seeBand);color:var(--seeAccent);padding:12px 20px;text-align:center;font-size:13px;line-height:1.6}
.preview-brand{max-width:960px;margin:28px auto 0;padding:0 28px;font-size:14px;font-weight:800;color:var(--inkMuted)}
main{max-width:960px;margin:20px auto 48px;background:var(--card);border-radius:24px;padding:48px 56px;box-shadow:var(--shadowSoft)}
.lesson-group{font-size:12px;letter-spacing:.12em;font-weight:700;color:var(--inkMuted);text-transform:uppercase;margin:0 0 12px}
h1{font-family:var(--serif);font-size:64px;font-weight:400;line-height:.98;letter-spacing:-.025em;margin:0 0 30px}
.lesson-copy p,.lesson-copy li{font-size:17px;line-height:1.65;color:var(--inkSoft)}
.lesson-copy p{margin:0 0 18px}.lesson-copy h2{font-size:24px;line-height:1.3;margin:40px 0 18px;color:var(--ink)}
.example{background:var(--primaryFaint);padding:24px;border-radius:16px;margin:22px 0}
.example p:last-child,.example ol:last-child{margin-bottom:0}.example .label,.label{font-size:12px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;color:var(--primaryDeep);margin:0 0 12px}
.example .sentence{font-size:25px;line-height:1.4;color:var(--ink);font-weight:600}
.example-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px;margin:22px 0}
.example-grid .example{margin:0}.example.preferred{background:var(--tryBand)}.preferred .label{color:var(--tryAccent)}
.preparation-board{margin:26px 0 22px}.preparation-board img{display:block;width:100%;height:auto;border-radius:12px}.preparation-board figcaption{text-align:right;font-size:13px;margin-top:8px}.preparation-board a{color:var(--primaryDeep)}
.generic-loop{margin:24px 0;padding:24px;background:#eae7fd;border-radius:18px}
.lesson-copy .generic-loop>h2{font-size:30px;margin:0 0 20px}
.loop-stage{background:var(--card);padding:20px;border-radius:12px}
.loop-steps{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px}
.loop-step{--loop-color:#4f2fc4;text-align:center;position:relative;min-width:0}.loop-check{--loop-color:#1652f0}.loop-adjust{--loop-color:#0e8f86}
/* Reuse the original board's illustrations without altering the source asset. */
.loop-art{aspect-ratio:457/257;border-radius:10px;background-image:url('../course-assets/training/training-guess-check-adjust.jpg');background-size:350.1094% 426.07%;background-repeat:no-repeat}
.loop-art-try{background-position:7% 29.9523%}.loop-art-check{background-position:49.9563% 29.9523%}.loop-art-adjust{background-position:93.0009% 29.9523%}
.loop-step:not(:last-child)::after{content:'→';position:absolute;right:-22px;top:48px;color:var(--inkMuted);font-size:20px}
.loop-step h3{font-size:25px;color:var(--loop-color);margin:18px 0 10px}
.loop-step h3 span{display:block;width:30px;height:30px;line-height:30px;border-radius:50%;font-size:16px;background:var(--loop-color);color:#fff;margin:0 auto 12px}
.lesson-copy .loop-step p{font-size:16px;line-height:1.55;margin:0}
.loop-repeat{position:relative;color:#4f2fc4;margin-top:16px;text-align:center;height:55px}
.loop-repeat svg{width:100%;height:55px}.loop-repeat strong{position:absolute;top:0;left:0;right:0;font-size:13px}
@media(max-width:760px){.loop-steps{grid-template-columns:1fr;gap:28px}.loop-step:not(:last-child)::after{display:none}.loop-art{max-width:320px;margin:auto}.loop-repeat svg{display:none}.loop-repeat{height:auto;margin-top:24px}.loop-repeat strong{position:static}}
@media(max-width:540px){.generic-loop{padding:18px 12px}.loop-stage{padding:18px 16px}.lesson-copy .generic-loop>h2{font-size:25px}}
.training-phases{margin:26px 0 36px;padding:24px;background:var(--primaryFaint);border-radius:18px}
.lesson-copy .training-phases>h2{margin:0 0 8px;font-size:30px}
.lesson-copy .phases-intro{margin:0 0 22px}
.phase-tabs{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-bottom:20px}
.phase-tabs button{display:flex;align-items:center;justify-content:center;gap:8px;min-height:56px;padding:12px 8px;border:1px solid var(--rule);border-radius:10px;background:transparent;color:var(--inkSoft);font:600 15px/1.35 var(--sans);cursor:pointer}
.phase-tabs button[aria-selected="true"]{background:var(--primaryDeep);color:#fff;border-color:var(--primaryDeep)}
.phase-tab-number{font-size:12px;opacity:.8}.phase-tab-complete{font-weight:800}
.phase-demo-panel{padding:24px;background:var(--card);border-radius:12px}
.phase-demo-panel h3{margin:0 0 8px;font-size:24px;color:var(--primaryDeep)}
.lesson-copy .phase-purpose{margin:0 0 20px}
.phase-context{border-bottom:1px solid var(--rule);padding-bottom:18px;margin-bottom:20px}
.phase-context>span,.phase-output-label{font-size:12px!important;letter-spacing:.04em;text-transform:uppercase;font-weight:700;color:var(--inkMuted)!important}
.lesson-copy .phase-context p{font-size:21px;line-height:1.45;color:var(--ink);margin:6px 0 0}
.phase-state-stack{display:grid}.phase-state-stack>div{grid-area:1/1}
.phase-state-measure{visibility:hidden;pointer-events:none}
.phase-state-content h4{color:var(--primaryDeep);font-size:20px;margin:0 0 16px}
.phase-outputs{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px}
.phase-output{padding:0 0 12px;border-bottom:2px solid var(--rule)}
.phase-output.is-preferred{border-color:var(--tryAccent)}
.lesson-copy .phase-output-label{margin:0 0 8px}.lesson-copy .phase-output-text{font-size:20px;line-height:1.45;color:var(--ink);margin:0}
.phase-output ol{margin:0;padding-left:23px}.phase-output li{font-size:17px;line-height:1.5}
.lesson-copy .phase-effect{font-weight:700;color:var(--tryAccent);margin:16px 0 0}
.lesson-copy .phase-explanation{margin:18px 0 0;font-size:17px;line-height:1.6}
.phase-actions{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-top:22px}
.phase-actions .guided-demo-controls{padding:0;border:0}
.phase-next{font:700 15px var(--sans);min-height:44px;padding:10px 14px;color:var(--primaryDeep);background:var(--primaryFaint);border:0;border-radius:8px;cursor:pointer}
.phase-next-hidden{visibility:hidden}.phase-tabs button:focus-visible,.phase-next:focus-visible{outline:3px solid var(--primary);outline-offset:3px}
.lesson-copy .phases-note{font-size:15px;line-height:1.6;margin:18px 0 0}
.phase-print{display:none}.phase-print-mode .phase-print{display:block}
.phase-print>section+section{border-top:1px solid var(--rule);margin-top:28px;padding-top:20px}.phase-print .phase-state-content{margin:22px 0}
@media(max-width:620px){.phase-tabs{grid-template-columns:1fr;gap:6px}.phase-tabs button{justify-content:flex-start;min-height:44px}.phase-actions{flex-wrap:wrap}.phase-outputs{grid-template-columns:1fr}}
@media(max-width:540px){.training-phases{padding:18px 12px}.phase-demo-panel{padding:20px 16px}.lesson-copy .training-phases>h2{font-size:25px}}
@media print{.phase-interactive{display:none}.phase-print{display:block}.phase-print .phase-state-content{break-inside:avoid}}
.closing{margin-top:36px;text-align:center;padding:28px 20px;border-radius:16px;background:var(--seeBand)}
.closing p{margin:0;font-size:18px;line-height:1.6}.closing strong{display:block;margin-top:12px;font-size:23px}
.preview-footer{text-align:center;font-size:13px;color:var(--inkMuted);margin-top:28px}
@media(max-width:620px){main{margin:12px 10px 28px;padding:28px 20px;border-radius:18px}.preview-brand{padding:0 22px;margin-top:20px}h1{font-size:52px}.example-grid{grid-template-columns:1fr}.example{padding:20px}.lesson-copy h2{font-size:22px}.interactive-box{padding:20px 16px!important}}
</style></head><body>
<div class="preview-note"><strong>Lesson preview</strong> · Proposed rewrite · The current course is unchanged</div>
<header class="preview-brand">Be Smarter Than the Tool</header>
<main>
<article class="lesson-copy" aria-labelledby="lesson-title">
<p class="lesson-group">Understand AI</p><h1 id="lesson-title">Training</h1>
<p>AI can explain chemistry, write code, and help you improve an essay. How did it learn to do those things?</p>
<p>Think about learning to shoot a basketball. You take a shot, see where it goes, and adjust your next attempt. Practice gives you chances to improve.</p>
<p>AI training also uses repeated attempts and adjustments. But what changes inside an AI model?</p>
<figure class="preparation-board">
<img src="../course-assets/training/training-before-starts.jpg" alt="Before Training Starts. Set Up the System: Engineers design the model and give its internal numbers starting values. Training will adjust those numbers as the model learns. Gather the Data: Teams collect books, websites, conversations, code, images, audio, and video. This becomes the curriculum.">
<figcaption><a href="../course-assets/training/training-before-starts.jpg" target="_blank" rel="noopener">Open board full size</a></figcaption>
</figure>
<p>Those internal numbers are called <strong>weights</strong>. Training changes them through repeated attempts and feedback.</p>
<p>Across the three phases of training, the basic loop stays the same: <strong>Predict. Check. Adjust. Repeat.</strong></p>
<section class="generic-loop" id="training-loop-board" aria-labelledby="training-loop-title">
<h2 id="training-loop-title">The Training Loop</h2>
<div class="loop-stage">
<div class="loop-steps">
<section class="loop-step"><div class="loop-art loop-art-try" aria-hidden="true"></div><h3><span>1</span> Predict</h3><p>The model predicts what comes next, whether it’s completing text or answering a request.</p></section>
<section class="loop-step loop-check"><div class="loop-art loop-art-check" aria-hidden="true"></div><h3><span>2</span> Check</h3><p>The training system evaluates it using an example or feedback.</p></section>
<section class="loop-step loop-adjust"><div class="loop-art loop-art-adjust" aria-hidden="true"></div><h3><span>3</span> Adjust</h3><p>The system changes the model’s weights to improve future predictions.</p></section>
</div>
<div class="loop-repeat"><svg viewBox="0 0 900 60" aria-hidden="true"><path d="M750 5 V45 H150 V5 M140 16 L150 5 L160 16" fill="none" stroke="currentColor" stroke-width="3"/></svg><strong>REPEAT</strong></div>
</div>
</section>
<p>What changes between phases is the examples and feedback used to guide those adjustments. Here’s what that looks like in each phase.</p>
<section class="training-phases" aria-labelledby="training-phases-title">
<h2 id="training-phases-title">Three Phases of Training</h2>
<p class="phases-intro">Follow one example in each phase. Select See It to reveal a change and its explanation together.</p>
<div id="training-phase-demonstrations"></div>
<p class="phases-note">Better doesn’t always mean longer. Feedback can improve answers, but it doesn’t guarantee they’re correct.</p>
</section>
<h2>Training ends. You start chatting.</h2>
<p>During training, the model’s weights change.</p>
<p>During an ordinary chat, the model uses the weights it already has.</p>
<p>If you say, “Make that answer shorter,” it can use your instruction to change its next response. That doesn’t mean it has retrained itself. Your message gives it information to use in this conversation.</p>
</article>
<div id="kitchen-helper"></div>
<div class="lesson-copy"><p>Notice what carries over: you chose answers to some questions, and those preferences shaped the helper’s answers to different questions.</p></div>
<div class="closing"><p>Training shapes future answers through examples and feedback.<strong>Predict. Check. Adjust. Repeat.</strong></p></div>
<footer class="preview-footer">End of lesson preview</footer>
</main>
${scripts}
<script>
var useState=React.useState,useEffect=React.useEffect,useRef=React.useRef;
${shared.join('\n')}
${section('function ActivityInstructions(', 'function GroupExercise(')}
${section('function ActivityButton(', '\nfunction FeedbackPill(')}
${section('function GuidedDemoControls(', 'function GuidedDemonstration(')}
${fs.readFileSync(path.join(root, 'previews/training-phase-demos.js'), 'utf8')}
${section('const KITCHEN_HELPER_ROUNDS =', 'function TrainingSection(')}
ReactDOM.createRoot(document.getElementById('training-phase-demonstrations')).render(React.createElement(TrainingPhasesDemo));
ReactDOM.createRoot(document.getElementById('kitchen-helper')).render(React.createElement(TrainingKitchenHelper));
</script></body></html>`;
fs.writeFileSync(path.join(root, 'previews/training-rewrite.html'), output);
console.log('Created previews/training-rewrite.html');

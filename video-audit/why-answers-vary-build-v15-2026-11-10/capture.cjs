const {chromium}=require('/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const fs=require('fs');
const root='/Users/davidobrien/Developer/AI-Training',out=root+'/video-audit/why-answers-vary-build-v15-2026-11-10';
(async()=>{const b=await chromium.launch({channel:'chrome',headless:true});try{
const p=await b.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1});
await p.goto('file://'+root+'/previews/temperature.html?capture=1&step=0');await p.locator('.temperature-scene').waitFor();await p.evaluate(()=>document.fonts.ready);
await p.addStyleTag({content:`html,body{margin:0;background:#f6f5fb} .capture{width:1280px;height:720px;background:#f6f5fb;display:block;padding:24px 48px;box-sizing:border-box}.capture .temperature-scene{width:1184px;padding:0;box-sizing:border-box}.temperature-reply{font-size:25px;margin:10px 0}.temperature-reply-label{display:none}.temperature-table{border-spacing:0 8px}.temperature-table th,.temperature-table td{font-size:25px;padding:9px 16px;line-height:1.25}.temperature-table thead th{font-size:25px}.temperature-table th:first-child{width:20%}.temperature-bar{height:10px;margin-top:7px}.temperature-pending{top:10px}.temperature-table .is-focus>th::after{display:none}.temperature-table .is-focus>td{border-inline-color:var(--card)}.temperature-table thead th:first-child{color:transparent}h2.video-heading{font-size:36px;font-family:var(--sans);font-weight:800;letter-spacing:-1px;margin:0 0 18px;color:var(--ink)}`});
await p.evaluate(()=>{const h=document.createElement('h2');h.className='video-heading';h.textContent='How Temperature Changes the Odds';document.querySelector('main').prepend(h)});
const rows=[];
for(let step=0;step<4;step++) {await p.evaluate(n=>window.setTemperatureScene(n),step);await p.locator(`[data-step="${step}"]`).waitFor();await p.screenshot({path:out+`/temperature-${step}.png`});rows.push(await p.evaluate(()=>[...document.querySelectorAll('.temperature-table tr')].map(tr=>[...tr.children].map(x=>{let r=x.getBoundingClientRect();return {text:x.innerText,rect:[r.x,r.y,r.width,r.height]}}))))}
fs.writeFileSync(out+'/capture.json',JSON.stringify(rows,null,2));console.log('Captured states');
}finally{await b.close()}})().catch(e=>{console.error(e);process.exit(1)});

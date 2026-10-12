const {chromium} = require('/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const path = require('path');
const fs = require('fs');
(async()=>{
 const browser = await chromium.launch({headless:true,channel:'chrome'});
 const page = await browser.newPage({viewport:{width:1440,height:1000},deviceScaleFactor:2});
 await page.goto('http://127.0.0.1:8765/?print=lesson:vectorspace',{waitUntil:'networkidle'});
 const font=fs.readFileSync(path.resolve('scripts/video/assets/fonts/PlusJakartaSans-wght.ttf')).toString('base64');
 await page.addStyleTag({content:`@font-face{font-family:SentenceCapture;src:url(data:font/ttf;base64,${font});font-weight:100 900}`});
 const label=page.getByText('THE SENTENCE',{exact:true});
 const card=label.locator('..');
 await card.evaluate(el=>{el.style.fontFamily='SentenceCapture, sans-serif';el.style.width='900px';el.style.boxSizing='border-box';el.style.maxWidth='none';});
 await page.evaluate(()=>document.fonts.ready);
 await card.screenshot({path:path.join(__dirname,'lesson-sentence-v20.png')});
 fs.writeFileSync(path.join(__dirname,'sentence-capture-v20.json'),JSON.stringify({url:page.url(),bounds:await card.boundingBox(),html:await card.evaluate(e=>e.outerHTML)},null,2)+'\n');
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});

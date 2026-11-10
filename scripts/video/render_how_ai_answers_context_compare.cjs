// Render the approved EE-COMPARE board at its canonical 1600 px width.
const fs = require('node:fs');
const path = require('node:path');
const {execFileSync} = require('node:child_process');
const {chromium} = require('playwright');
const root = path.resolve(__dirname, '../..');
const source = path.join(__dirname, 'assets/how-ai-answers-same-token-context.html');
const scratch = path.join(root, 'tmp/how-ai-answers-context-compare');
const output = path.join(root, 'course-assets/how-ai-answers/how-ai-answers-same-token-context.jpg');
(async () => {
  fs.mkdirSync(scratch, {recursive:true});
  const browser = await chromium.launch({channel:'chrome',headless:true});
  try {
    const page = await browser.newPage({viewport:{width:1600,height:1000},deviceScaleFactor:1});
    await page.setContent(fs.readFileSync(source,'utf8'));
    await page.addStyleTag({content:'html,body{margin:0;padding:0;}'});
    await page.evaluate(() => document.fonts.ready);
    const board = page.locator('#same-token-context-preview .board');
    const geometry = await board.boundingBox();
    if (geometry.width !== 1600) throw new Error('Unexpected board width');
    const overflow = await board.evaluate(el => [...el.querySelectorAll('*')].some(n => n.scrollWidth > n.clientWidth + 1));
    if (overflow) throw new Error('Board content overflows');
    const png = path.join(scratch,'board.png');
    await board.screenshot({path:png});
    execFileSync(path.join(root,'.video-venv/bin/python'), ['-c',
      'from PIL import Image; import sys; Image.open(sys.argv[1]).convert("RGB").save(sys.argv[2],"JPEG",quality=95,subsampling=0,optimize=True)',
      png,output]);
    console.log(JSON.stringify({output,width:geometry.width,height:Math.ceil(geometry.height)}));
  } finally { await browser.close(); }
})().catch(error => {console.error(error);process.exitCode=1;});

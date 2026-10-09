// Capture the current lesson scene as a Notebook source, without controls or highlights.
// Start the course preview server, then run:
// BASE_URL=http://127.0.0.1:8793 node scripts/video/capture_temperature_board.cjs
const fs = require('node:fs');
const path = require('node:path');
const {execFileSync} = require('node:child_process');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || '/Users/davidobrien/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = path.resolve(__dirname, '../..');
const output = path.join(root, 'gemini-notebook/the-next-token/assets/the-next-token-temperature.jpg');
(async () => {
  execFileSync(process.execPath, [path.join(__dirname, 'preview_temperature.cjs')]);
  const browser = await chromium.launch({channel:'chrome', headless:true});
  try {
    const page = await browser.newPage({viewport:{width:1280,height:900}, deviceScaleFactor:2});
    await page.goto((process.env.BASE_URL || 'http://127.0.0.1:8793') + '/previews/temperature.html?capture=1&step=2');
    const scene = page.locator('.temperature-scene[data-step="2"]');
    await scene.waitFor();
    await page.evaluate(() => document.fonts.ready);
    if (await page.getByRole('button').count() || await scene.locator('.temperature-value:not(.is-pending)').count() !== 18) {
      throw new Error('Expected the complete temperature comparison without controls');
    }
    fs.mkdirSync(path.dirname(output), {recursive:true});
    await scene.screenshot({path:output, type:'jpeg', quality:95, animations:'disabled'});
    console.log(output);
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });

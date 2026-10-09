// Render the approved live component as successive Notebook upload boards.
const fs=require('node:fs'), path=require('node:path');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'../..');
const out=path.join(root,'gemini-notebook/embeddings/assets');
const states=[['headings',0],['coffee',1],['coke',3],['pepsi',4],['citrus-column',6],['citrus-values',7]];
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1});
  await page.goto('http://127.0.0.1:8765/previews/embedding-dimension.html?capture=1');
  await page.locator('.embedding-dimension-scene').waitFor();
  await page.evaluate(()=>document.fonts.ready);
  await page.addStyleTag({content:`html,body{margin:0!important;padding:0!important;background:var(--bg)!important;width:1280px;height:720px;overflow:hidden}main.capture{width:1280px;height:720px;background:var(--bg);box-sizing:border-box;padding:24px}.capture .embedding-dimension-scene{box-sizing:border-box;width:1232px;background:var(--card);border-radius:18px;padding:24px}.embedding-dimension-scale{font-size:22px;margin-bottom:24px}.embedding-dimension-table{border-spacing:0 12px}.embedding-dimension-table th{font-size:18px}.embedding-dimension-table tbody th{font-size:28px}.embedding-dimension-tile{width:72px;height:72px;font-size:38px}.embedding-dimension-table .is-new{animation:none}.embedding-dimension-tile.is-match,.embedding-dimension-tile.is-answer{outline:none}.embedding-dimension-mobile{display:none!important}.embedding-dimension-desktop{display:table!important}`});
  for(const [name,step] of states){
   await page.evaluate(n=>window.setEmbeddingDimensionScene(n),step);
   await page.locator(`.embedding-dimension-scene[data-step="${step}"]`).waitFor();
   const rows=await page.locator('.embedding-dimension-desktop tbody tr').evaluateAll(nodes=>nodes.map(n=>({name:n.querySelector('th').textContent,hidden:n.getAttribute('aria-hidden')==='true'})));
   if(rows.map(r=>r.name).join(',')!=='Coffee,Coke,Pepsi')throw Error('Unexpected row order');
   if(step===1&&rows.filter(r=>!r.hidden).map(r=>r.name).join(',')!=='Coffee')throw Error('First reveal must be Coffee only');
   await page.screenshot({path:path.join(out,`embeddings-ratings-${name}.jpg`),type:'jpeg',quality:96});
  }
  // The same top crop used by the lesson, applied to the existing faceless upload.
  await page.setViewportSize({width:1600,height:1176});
  await page.goto('http://127.0.0.1:8765/gemini-notebook/embeddings/assets/embeddings-student-id-faceless.jpg');
  await page.evaluate(()=>{const img=document.querySelector('img');document.body.replaceChildren(img);Object.assign(document.body.style,{margin:'0',width:'1600px',height:'1176px',overflow:'hidden'});Object.assign(img.style,{display:'block',width:'1600px',height:'1308px',margin:'0',maxWidth:'none',maxHeight:'none'});return img.decode();});
  await page.screenshot({path:path.join(out,'embeddings-student-id-faceless-no-banner.jpg'),type:'jpeg',quality:96});
  console.log('Rendered six stable-order table states and the banner-free faceless illustration.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});

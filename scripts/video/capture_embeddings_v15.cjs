// Capture the live lesson components for the approved Embeddings visual update.
const fs=require('node:fs'),path=require('node:path');
const {chromium}=require('playwright');
const root=path.resolve(__dirname,'../..');
const out=path.join(root,'video-audit/embeddings-build-2026-10-09-v15');
const configs=[
 {id:'headings',state:0},
 {id:'coffee',state:1},
 ...Array.from({length:6},(_,i)=>({id:'coffee-'+i,state:1,rings:[['Coffee',i]]})),
 {id:'two',state:2},
 ...Array.from({length:6},(_,i)=>({id:'coke-'+i,state:2,rings:[['Coke',i]]})),
 {id:'answer',state:3,rings:[['Coke',0],['Coke',1],['Coke',2]]},
 {id:'vector',state:3,rings:[['Coke','six']],label:'A row of numbers like this is called a vector.'},
 {id:'dimension',state:3,rings:[['column',0]],label:'Each position is a dimension.'},
 {id:'value',state:3,rings:[['Coke',0]],label:'The number in that position is its value.'},
 {id:'pepsi',state:4},
 {id:'pepsi-six',state:4,rings:[['Pepsi','six']]},
 {id:'match',state:5,rings:[['Coke','six'],['Pepsi','six']]},
 {id:'citrus-column',state:6},
 {id:'citrus-coffee',state:7,citrusShown:['Coffee'],rings:[['Coffee',6]]},
 {id:'citrus-coke',state:7,citrusShown:['Coffee','Coke'],rings:[['Coke',6]]},
 {id:'citrus-pepsi',state:7,rings:[['Pepsi',6]]},
 {id:'complete',state:7,rings:[['Coke',6],['Pepsi',6]]}
];
(async()=>{
 fs.mkdirSync(path.join(out,'captures'),{recursive:true});
 const browser=await chromium.launch({channel:'chrome',headless:true});
 try{
  const page=await browser.newPage({viewport:{width:1280,height:720},deviceScaleFactor:1});
  await page.goto('http://127.0.0.1:8765/previews/embedding-dimension.html?capture=1');
  await page.locator('.embedding-dimension-scene').waitFor();await page.evaluate(()=>document.fonts.ready);
  await page.addStyleTag({content:`html,body{margin:0!important;padding:0!important;background:var(--bg)!important;width:1280px;height:720px;overflow:hidden}#video-stage{box-sizing:border-box;width:1280px;height:720px;display:flex;align-items:center;justify-content:center;flex-direction:column;padding:24px}.embedding-dimension-scene{box-sizing:border-box;width:1232px;background:var(--card);border-radius:18px;padding:24px}.embedding-dimension-scale{font-size:22px;margin-bottom:24px}.embedding-dimension-table{border-spacing:0 12px}.embedding-dimension-table th{font-size:18px}.embedding-dimension-table tbody th{font-size:28px}.embedding-dimension-tile{width:72px;height:72px;font-size:38px}.embedding-dimension-table .is-new{animation:none}.embedding-dimension-tile.is-match,.embedding-dimension-tile.is-answer{outline:none}.video-label{height:42px;margin:16px 0 0;font-size:27px;font-weight:700;color:var(--primaryDeep)}.video-ring{position:absolute;box-sizing:border-box;border:4px solid var(--primary);border-radius:12px;pointer-events:none}.embedding-dimension-mobile{display:none!important}.embedding-dimension-desktop{display:table!important}`});
  await page.evaluate(()=>{
   window.originalDrinks=JSON.parse(JSON.stringify(EMBEDDING_DIMENSION_DATA.drinks));
   document.body.innerHTML='<div id="video-stage"><div id="video-scene"></div><div class="video-label"></div></div>';
   window.videoRoot=ReactDOM.createRoot(document.getElementById('video-scene'));
  });
  const results=[];
  for(const cfg of configs){
   await page.evaluate(cfg=>{
    document.querySelectorAll('.video-ring').forEach(n=>n.remove());
    const order=cfg.order||['Coffee','Coke','Pepsi'];
    EMBEDDING_DIMENSION_DATA.drinks=order.map(name=>JSON.parse(JSON.stringify(originalDrinks.find(d=>d.name===name))));
    if(cfg.citrusShown) EMBEDDING_DIMENSION_DATA.drinks.forEach(d=>{if(!cfg.citrusShown.includes(d.name))d.values[6]=null;});
    const state={...EMBEDDING_DIMENSION_STATES[cfg.state],answer:false,match:false};
    window.videoRoot.render(React.createElement(EmbeddingDimensionScene,{state,step:cfg.id}));
    document.querySelector('.video-label').textContent=cfg.label||'';
   },cfg);
   await page.locator(`.embedding-dimension-scene[data-step="${cfg.id}"]`).waitFor();
   const geometry=await page.evaluate(cfg=>{
    const table=document.querySelector('.embedding-dimension-desktop');
    const rows={};table.querySelectorAll('tbody tr').forEach(row=>{rows[row.querySelector('th').textContent]=row;});
    const heads=[...table.querySelectorAll('thead th')];
    function rect(nodes,pad=5){const rs=nodes.map(n=>n.getBoundingClientRect());const x=Math.min(...rs.map(r=>r.left))-pad,y=Math.min(...rs.map(r=>r.top))-pad;return {x,y,width:Math.max(...rs.map(r=>r.right))+pad-x,height:Math.max(...rs.map(r=>r.bottom))+pad-y};}
    return (cfg.rings||[]).map(([name,part])=>{
     let nodes;
     if(name==='headers')nodes=heads.slice(1,7);
     else if(name==='column')nodes=[heads[part+1],...['Coke','Coffee'].map(n=>rows[n].querySelectorAll('.embedding-dimension-tile')[part])];
     else if(part==='row')nodes=[rows[name]];
     else if(part==='six')nodes=[...rows[name].querySelectorAll('.embedding-dimension-tile')].slice(0,6);
     else nodes=[rows[name].querySelectorAll('.embedding-dimension-tile')[part]];
     const r=rect(nodes,part==='row'?-1:5),ring=document.createElement('div');ring.className='video-ring';Object.assign(ring.style,{left:r.x+'px',top:r.y+'px',width:r.width+'px',height:r.height+'px'});
     if(typeof part==='number' && name!=='column')ring.style.borderColor=getComputedStyle(nodes[0]).color;
     document.body.appendChild(ring);return r;
    });
   },cfg);
   await page.screenshot({path:path.join(out,'captures',cfg.id+'.png')});results.push({...cfg,geometry});
  }
  await page.goto('http://127.0.0.1:8765/?print=lesson:embeddings');
  await page.locator('.embedding-student-board img').evaluate(img=>img.decode());
  await page.evaluate(()=>{
   const board=document.querySelector('.embedding-student-board').cloneNode(true);
   document.body.replaceChildren(board);
   Object.assign(document.body.style,{margin:'0',width:'1280px',height:'720px',display:'flex',alignItems:'center',justifyContent:'center',background:'var(--bg)'});
   Object.assign(board.style,{width:'925.17px',maxWidth:'none',margin:'0',borderRadius:'12px',flexShrink:'0'});
  });
  await page.screenshot({path:path.join(out,'captures','student-id.png')});
  fs.writeFileSync(path.join(out,'capture-manifest.json'),JSON.stringify({source:'index.html live components',configs:results},null,2));
  console.log('Captured',configs.length,'table states and the banner-free student illustration.');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});

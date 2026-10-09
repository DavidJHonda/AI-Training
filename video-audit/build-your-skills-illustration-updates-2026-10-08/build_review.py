from pathlib import Path
import sys,json,html,subprocess,shutil,re
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent.parent
sys.path.insert(0,str(ROOT/'scripts/video'))
from build_skills_illustrations import SOURCES,paths,FF
OLD=OUT.parent/'build-your-skills-illustration-opportunities-2026-10-08'
e=html.escape
rows=[]
info={
'people-skills':('People Skills','Four matched states show the group’s satisfaction, Maya’s suggestion, the interruption, and her withdrawal. The two quoted lines appear on their spoken cues.','P1-00419.jpg'),
'curious-and-flexible':('Curious and Flexible','The same court shows the familiar passing lane, the defender closing it, and the captain switching to an open teammate. The open receiver highlights on “curious”; the changed pass appears on “flexible.”','P2-00719.jpg'),
'make-your-move':('Make Your Move','A student coordinator checks progress as teammates hand off a box of supplies. A restrained push brings attention to the completed result.','P3-08342.jpg')}
PRE=OUT/'previews';PRE.mkdir(exist_ok=True)
for slug,c in SOURCES.items():
 title,summary,poster=info[slug];src,dst=paths(slug,c)
 clip=PRE/(c['id']+'-after.mp4')
 if not clip.exists():
  start=max(0,c['start']/30-3);duration=min(c['frames']/30,c['end']/30+3)-start
  subprocess.run([FF,'-v','error','-y','-ss',str(start),'-i',str(dst),'-t',str(duration),'-vf','scale=960:540','-c:v','libx264','-threads','2','-preset','fast','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','128k','-movflags','+faststart',str(clip)],check=True)
 def player(label,src,poster):
  return f'<div class="preview-player" data-label="{e(label)}" data-src="{src}"><button class="preview-start" type="button" aria-label="Play {e(label)} current excerpt"><img src="{poster}" alt="{e(label)} preview"><span>▶ Play excerpt</span></button><video hidden aria-label="{e(label)} current excerpt" controls playsinline preload="none" poster="{poster}"></video><p class="preview-status" role="status"></p></div>'
 oldposter=json.loads((OLD/'opportunities.json').read_text())['opportunities'][int(c['id'][1:])-1]['image']
 rows.append(f'''<article id="{c['id']}"><div class="eyebrow">{c['id']} · {title} · {c['start']/30:.2f}–{c['end']/30:.2f} seconds</div><h2>{title}</h2><p>{summary}</p><div class="comparison"><section><h3>Before</h3>{player(title+' before','../'+OLD.name+'/clips/'+c['id']+'.mp4','../'+OLD.name+'/'+oldposter)}</section><section><h3>Updated</h3>{player(title+' updated','previews/'+clip.name,'previews/'+poster)}</section></div><p><a href="../../Prompts/{dst.name}">Full updated video</a> · <a href="{slug}/qa.json">Verification</a> · <a href="{slug}/transitions/">Transition evidence</a> · <a href="{slug}-manifest.json">Edit record</a></p></article>''')
style='''body{margin:0;background:#f4f5fa;color:#262b35;font:17px/1.6 system-ui,sans-serif}main{max-width:1160px;margin:48px auto;padding:0 24px}h1{font-size:40px;line-height:1.15}h2{margin:8px 0}h3{margin:0 0 10px}a{color:#44356c}article{background:white;border:1px solid #dcdee6;border-radius:18px;padding:28px;margin:30px 0}.eyebrow{font-size:13px;text-transform:uppercase;letter-spacing:.06em;color:#5a5470}.comparison{display:grid;grid-template-columns:1fr 1fr;gap:24px}.comparison section{min-width:0}.note{padding:20px;background:#e9e5f3;border-radius:12px}.preview-start{display:block;width:100%;padding:0;border:0;border-radius:8px;overflow:hidden;cursor:pointer;background:#16223c;color:white;text-align:left}.preview-start img{display:block;width:100%;aspect-ratio:16/9;object-fit:contain}.preview-start span{display:block;padding:14px 18px;font-size:16px;font-weight:600}.preview-start:focus-visible{outline:3px solid #8064d9;outline-offset:3px}.preview-player video{display:block;width:100%;aspect-ratio:16/9;background:#16223c}.preview-player [hidden]{display:none!important}.preview-status:empty{display:none}nav{display:flex;gap:22px;margin:24px 0}footer{font-size:14px;color:#626777}@media(max-width:800px){.comparison{grid-template-columns:1fr}h1{font-size:30px}article{padding:20px}}'''
installed=OUT/'local-install.json'
status='Built from the approved three-scene plan. Technical and visual verification in progress.'
if installed.exists():status='Shipped locally · These three updated videos are installed and committed. Queued for the next batch deployment.'
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Build Your Skills — Learning Illustration Updates</title><style>{style}</style></head><body><main><header><div class="eyebrow">Learning Illustration Pass · October 8, 2026</div><h1>Build Your Skills: see the skills in action.</h1><p>Three focused replacements, preserving the existing narration, course boards, duration and closing frames.</p><p class="note">{status}</p><nav><a href="#P1">People Skills</a><a href="#P2">Curious and Flexible</a><a href="#P3">Make Your Move</a></nav></header>{''.join(rows)}<footer><p>Before/after excerpts include surrounding narration. Click Play or Resume; paused previews use still images to avoid the blank-player issue.</p><p>Original AAC packets and decoded audio are checked for exact equality. Unaffected decoded video frames and packets are checked for exact equality. Technical checks do not establish a continuous listening review; no new end-to-end listening pass is claimed.</p><p>New photographic assets use the built-in imagegen tool. <a href="assets/prompts.json">Complete prompts and provenance</a> · <a href="assets/">Saved assets</a> · <a href="REVIEW.md">Production record</a></p></footer></main><script src="preview-player.js"></script></body></html>'''
(OUT/'review.html').write_text(page)
shutil.copyfile(OUT.parent/'build-your-skills-illustration-opportunities-2026-10-08-v2/preview-player.js',OUT/'preview-player.js')
missing=[p for p in re.findall(r'(?:src|href)="([^"#]+)"',page) if not (OUT/p.split('#')[0]).exists()]
print('Missing:',missing)

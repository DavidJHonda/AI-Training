#!/usr/bin/env python3
"""Create the review page for the shortened Embeddings candidate."""
import html,json,re,subprocess
import imageio_ffmpeg
import build_embeddings_v16 as b

def main():
 verify=json.loads((b.OUT/'verification.json').read_text())
 assert verify['output_sha256']==b.sha(b.DST)
 guard=json.loads((b.OUT/'guard/transition-guard.json').read_text());assert guard['pass']
 ff=imageio_ffmpeg.get_ffmpeg_exe()
 for name,start,end in [('coffee-join',57,66),('model-join',198,206.2)]:
  subprocess.run([ff,'-v','error','-y','-ss',str(start),'-i',str(b.DST),'-t',str(end-start),'-vn','-ar','48000','-ac','2',str(b.OUT/(name+'.wav'))],check=True)
 previous=(b.ROOT/'video-audit/embeddings-build-2026-10-09-v15/review.html').read_text()
 style=re.search(r'<style>(.*?)</style>',previous,re.S).group(1)
 moments=[('Start',0),('Shortened Coffee transition',60),('Coffee ratings',76.4),('Add Coke',88.9),('Definitions',103.7),('Add Pepsi',120.62),('Citrus column',135.14),('Citrus values',140.2),('Taste test → AI',161.53),('Shortened model walkthrough',213),('Whole-row takeaway',249.1334),('Word pieces',252.7),('Close',264)]
 buttons=''.join(f'<button data-time="{b.output_frame(b.fr(t))/30:.3f}">{html.escape(label)}</button>' for label,t in moments)
 page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Embeddings v16 · Review</title><style>{style}</style></head><body><main>
<div class="eyebrow">Embeddings · v16</div><h1>A shorter path from ratings to embeddings.</h1><p class="lead">3:47.9 · About 34 seconds shorter than v15 · Review candidate</p>
<video id="video" controls preload="metadata" poster="../embeddings-build-2026-10-09-v15/captures/complete.png"><source src="../../Prompts/embeddings-v16.mp4" type="video/mp4"></video>
<nav class="jumps" aria-label="Jump to a moment">{buttons}</nav>
<section class="card"><h2>The two agreed cuts</h2><p><strong>Before Coffee:</strong> removed the abstract sentence about moving from arbitrary IDs to a grid of scores. The narration now moves from the six characteristics directly into the Coffee example.</p><p><strong>Inside the model:</strong> kept cat → token ID 4719 → matching row, followed by the sentence identifying the complete row as the embedding. Removed the repeated column explanation, decimal values, and definitions. The illustration runs for about 15 seconds.</p><p>The complete labeled illustration remains on the lesson page as a reference. The lesson’s text and interactivity are unchanged.</p><a href="../../Prompts/embeddings-v16.mp4" download>Download v16</a> · <a href="../embeddings-build-2026-10-09-v15/review.html">Previous candidate</a></section>
<div class="columns"><section class="card"><h2>Coffee transition · 1:01.17</h2><p>“…Caffeine, and Dark. You and your friends tasted Coffee…”</p><audio controls preload="none" src="coffee-join.wav"></audio></section><section class="card"><h2>Model transition · 3:22.67</h2><p>“…alongside all the other tokens. The complete continuous row of numbers is the embedding.”</p><audio controls preload="none" src="model-join.wav"></audio></section></div>
<section class="card"><h2>Verification</h2><p>All {verify['frames']:,} frames decoded at 1280 × 720 and 30 fps. {verify['checked_frames']} selected encoded frames matched the expected visuals. Audio alignment passed numerical checks. All {len(guard['boundaries'])} declared transitions passed the automatic frame check.</p><p>Transcription confirms both new joins retain the intended sentences. Direct listening and continuous-motion review remain outstanding. The existing word-piece limitation remains: un / belie / vable appear visually but are not named individually in the narration.</p><details><summary>Evidence</summary><p><a href="build.json">Build and source mapping</a> · <a href="verification.json">Encoded verification</a> · <a href="guard/transition-guard.json">Transition checks</a></p></details></section>
<footer>The installed course video, lesson, source upload, and v15 candidate are unchanged.</footer></main><script>const v=document.getElementById('video');document.querySelectorAll('[data-time]').forEach(b=>b.addEventListener('click',()=>{{document.querySelectorAll('audio').forEach(a=>a.pause());v.currentTime=Number(b.dataset.time);v.play().catch(()=>{{}});}}));document.querySelectorAll('audio').forEach(a=>a.addEventListener('play',()=>{{v.pause();document.querySelectorAll('audio').forEach(other=>{{if(other!==a)other.pause();}});}}));</script></body></html>'''
 (b.OUT/'review.html').write_text(page)
 print(b.OUT/'review.html')
if __name__=='__main__':main()

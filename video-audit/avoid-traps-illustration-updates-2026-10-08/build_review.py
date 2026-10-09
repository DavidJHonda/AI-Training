from pathlib import Path
import subprocess,json,sys,concurrent.futures,re,cv2
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts/video'))
from build_avoid_traps_illustration_updates import OUT,FF,SOURCES
items=[
 ('P1','document-trap','Document Trap','Check the quotation against the original.','The student compares the rulebook with the AI quotation. The original passage is highlighted first; the matching six-foul exception follows. The example is explicitly labeled as a lesson scenario.',3),
 ('P2','support-trap','Support Trap','Turn preparation into action.','The three panels begin with an email draft, rehearsal notes, and a study plan. Sending, talking with a parent, and beginning the work appear as each action is spoken.',5),
 ('P3','fake-trap','Fake Trap','Call the contact you already know.','The phone leaves an urgent voicemail, opens Mom’s saved contact, and places a new call. The interface shows the action without claiming that the message has been verified.',2)
]
def clip(job):
 pid,variant,src,start,duration=job;dest=OUT/f'clips/{pid}-{variant}.mp4'
 if dest.exists():return
 subprocess.run([FF,'-v','error','-ss',str(start),'-i',str(src),'-t',str(duration),'-c:v','libx264','-crf','18','-preset','veryfast','-c:a','aac','-b:a','128k','-movflags','+faststart',str(dest)],check=True)
def time(f):return f'{f//1800}:{(f/30)%60:05.2f}'
jobs=[];sections=[]
for pid,slug,title,heading,desc,state in items:
 cfg=SOURCES[slug];_,a,b=cfg['spans'][0]
 for variant,v in [('before',cfg['source_version']),('after',cfg['version'])]:jobs.append((pid,variant,ROOT/f'Prompts/{slug}-v{v}.mp4',a/30-3,(b-a)/30+6))
 sections.append(f'<section id="{pid}"><p class="eyebrow">{title} · {time(a)}–{time(b)}</p><h2>{heading}</h2><p>{desc}</p><h3>Updated excerpt</h3><video controls playsinline preload="none" poster="previews/{pid}-state-{state}.jpg" src="clips/{pid}-after.mp4"></video><p class="caption">Three seconds of context before and after the insert. Player time is relative to the excerpt.</p><h3>Previous version</h3><video controls playsinline preload="none" poster="previews/{pid}-before-playback.jpg" src="clips/{pid}-before.mp4"></video><p><a href="../../Prompts/{slug}-v{cfg["version"]}.mp4">Full video · {title} v{cfg["version"]}</a> · <a href="{slug}-manifest.json">Edit record</a></p></section>')
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as ex:list(ex.map(clip,jobs))
for pid,slug,title,heading,desc,state in items:
 poster=OUT/f'previews/{pid}-before-playback.jpg'
 capture=cv2.VideoCapture(str(OUT/f'clips/{pid}-before.mp4'))
 capture.set(cv2.CAP_PROP_POS_MSEC,5000);ok,frame=capture.read();capture.release()
 assert ok,f'Cannot extract poster for {pid}'
 assert cv2.imwrite(str(poster),frame)
checks=json.loads((OUT/'verification.json').read_text())
qa=''.join(f'<li>{r["slug"]}: {r["frames"]:,} frames, {r["duration"]:.2f}s; complete decode and identical audio payload verified.</li>' for r in checks)
base=(ROOT/'video-audit/start-smarter-illustration-pilot-2026-10-07/review.html').read_text()
style=re.search(r'<style>(.*?)</style>',base,re.S).group(1)
playback_script="""<script>
document.querySelectorAll('video').forEach(video => {
  video.addEventListener('play', () => {
    document.querySelectorAll('video').forEach(other => {
      if (other !== video) other.pause();
    });
  });
});
</script>"""
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Avoid Traps — illustration updates</title><style>'''+style+'''h3{font-size:17px;margin:24px 0 8px}</style><main><p class="eyebrow">Avoid Traps · Illustration updates · 8 October 2026</p><h1>Make the next step visible.</h1><p class="intro">Three photographic updates in the established <em>Why Learn AI?</em> style: checking a quotation, acting on a plan, and calling a saved contact.</p><p>Approved and shipped locally: Document Trap v4, Support Trap v14, and Fake Trap v11. Commit 2e638b82, queued for batch deployment. <a href="local-install.json">Local release record</a>. The full candidates retain the original audio and runtime. About 31 seconds of supporting imagery changed across three videos. The other six Avoid Traps videos remain as they are.</p><nav><a href="#P1">Check the original</a><a href="#P2">Take the next step</a><a href="#P3">Call a saved contact</a><a href="#checks">Checks & assets</a></nav>'''+''.join(sections)+f'''<section id="checks"><h2>Verification</h2><ul>{qa}</ul><p>Every changed frame was compared against its intended state. Unedited frames were sampled every second and at edit boundaries. Sixteen transition boundaries and the final encoded states were inspected.</p><p>The approved finished source files are reencoded once at CRF 16 for these narrow visual updates. Full candidates copy the original audio without reencoding; browser excerpts use AAC audio. Course boards, their highlights and camera treatments, narration, pauses, and timeline are retained.</p><p>Continuous listening and audiovisual playback assessment by the agent have not been completed. These checks establish technical and frame-level integrity; the owner approved these versions for shipping after review. The course now uses the approved files locally; publication is pending the next batch deployment.</p><p>Existing narration limitations remain: Document Trap contains previously documented claims that overstate how reliably file retrieval and prompting work. Support Trap’s later story and safety language are unchanged. This build does not revise those claims. <a href="../document-trap-repair-2026-09-29-v2/NARRATION-NEEDED.txt">Existing Document Trap narration note</a>.</p><p><a href="verification.json">Verification data</a> · <a href="REVIEW.md">Build record</a> · <a href="../avoid-traps-illustration-opportunities-2026-10-08/review.html">Approved proposal</a></p><h2>Photographic assets</h2><p>Created with the built-in image generation tool: <a href="assets/document.png">rulebook comparison</a>, <a href="assets/support-email.png">email draft</a>, <a href="assets/support-talk-before.png">conversation preparation</a>, <a href="assets/support-talk.png">parent conversation</a>, <a href="assets/support-study-before.png">study preparation</a>, <a href="assets/support-study.png">study underway</a>, and <a href="assets/fake-phone.png">phone scene</a>. Text, highlights, and phone interfaces are rendered separately for precise wording and timing. <a href="assets/prompts.json">Complete generation and edit prompts</a>.</p></section><footer>Document Trap 3:04.167–3:17.667 · Support Trap 1:56.867–2:09.533 · Fake Trap 3:22.267–3:27.233. All changes stay within existing supporting shots.</footer></main></html>'''
html=html.replace('</body>',playback_script+'</body>') if '</body>' in html else html.replace('</html>',playback_script+'</html>')
(OUT/'review.html').write_text(html)
missing=[p for p in re.findall(r'(?:src|href)="([^"#]+)"',html) if not (OUT/p).exists()]
assert not missing,missing
print(OUT/'review.html')

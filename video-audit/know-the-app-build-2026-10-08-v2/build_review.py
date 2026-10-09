from pathlib import Path
import json,shutil
D=Path(__file__).resolve().parent
q=json.loads((D/'qa.json').read_text())
shutil.copyfile(D/'preview/output-00000.jpg',D/'poster.jpg')
(D/'REVIEW.md').write_text(f'''# Know the App — production candidate v2

Built 2026-10-08 from roll 6 using the October 1 edit plan. Review candidate; not installed or shipped.

- Runtime: 4:23.63, 7,909 frames at 30 fps, 1280×720.
- Roll 6 audio is copied unchanged; compressed audio stream hashes match.
- Current canonical Which Model?, How Much Thinking?, and How Much Research? boards, with narration-timed 4 px card highlights.
- Drawn camera examples from roll 4; engine, project-planning and university-comparison drawings from rolls 4 and 5.
- Useful source animation retained. Repaired settled answer labels to say Proposed answer / Review before using, removing claims that the answer has been verified.
- Canonical closing: 48-frame hold, 150-frame push, 26-frame settle.
- Canonical boards and protected source files remain unchanged.

## Validation

Decoded all 7,909 output frames. Automated transition guard passed all 27 declared boundaries. Reviewed contact sheets across the full video, before/at/after frames for every declared join, full-size board previews, label repairs, and final frame. Audio identity: {q['audio_hash']}.

Candidate SHA-256: `{q['sha256']}`.

Continuous audiovisual listening has not been completed. Roll 6's existing narration KEEP review is retained, but the candidate still needs a full listening pass, including the Dallas/College Station example around 3:34–3:39. No new narration correctness or readiness-to-ship certification is claimed.

v1 is superseded by v2's tighter label patches. Build script: `scripts/video/build_know_the_app_v2.py`. Exact timeline and asset hashes: `edit-manifest.json`. QA: `qa.json` and `transitions/`.
''')
(D/'review.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Know the App — video review</title><style>*{box-sizing:border-box}body{margin:0;background:#f5f3ed;color:#222a30;font:16px/1.55 system-ui,sans-serif}main{max-width:1100px;margin:48px auto;padding:0 24px}h1{font-size:42px;line-height:1.1;margin:10px 0 18px}h2{font-size:22px}p{max-width:800px}.eyebrow{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#5b4cb0}.player{background:white;border:1px solid #ddd9d1;border-radius:16px;padding:16px;box-shadow:0 8px 30px #24242b0a}video{display:block;width:100%;aspect-ratio:16/9;background:#eeefe4;border-radius:8px}button,a{color:#423594}button{background:white;border:1px solid #c9c2e2;border-radius:20px;padding:8px 14px;cursor:pointer;font:inherit}.chapters{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:28px}.note{border-left:3px solid #c29941;padding-left:14px;color:#5d5340}small{color:#65646a}@media(max-width:650px){main{margin:24px auto}h1{font-size:32px}.grid{grid-template-columns:1fr}}</style><main><div class="eyebrow">Build Your Skills · Review candidate v2</div><h1>Know the App</h1><p>The new lesson brought into the course’s video style: camera examples, updated teaching boards, and highlights that follow the narration.</p><div class="player"><video id="candidate" controls playsinline preload="none" poster="poster.jpg" src="../../Prompts/know-the-app-v2.mp4"></video><div class="chapters"><button data-time="0">Play from beginning</button><button data-time="55.733">Which Model? · 0:56</button><button data-time="121.767">Thinking · 2:02</button><button data-time="206.067">Research · 3:26</button><button data-time="256.167">Closing · 4:16</button><button id="pause">Pause</button></div><small>4:24 · Roll 6 narration preserved · Candidate only</small></div><div class="grid"><section><h2>What changed</h2><ul><li>Drawn camera, planning, and comparison examples support the spoken teaching.</li><li>All three current course boards replace generated approximations.</li><li>Each card is highlighted as its explanation begins.</li><li>The course closing finishes with the standard slow push.</li></ul></section><section><h2>Checks completed</h2><p>All 7,909 frames decoded. Audio is identical to roll 6. All 27 transition checks passed, and the boards and source files are unchanged.</p><p class="note">Ready for your review. A continuous listening pass is still needed before shipping.</p><p><a href="../../Prompts/know-the-app-v2.mp4">Open full video</a> · <a href="REVIEW.md">Production notes</a> · <a href="edit-manifest.json">Edit record</a></p></section></div></main><script>const v=document.querySelector('video');document.querySelectorAll('[data-time]').forEach(b=>b.addEventListener('click',()=>{v.currentTime=Number(b.dataset.time);v.play().catch(()=>{});}));document.querySelector('#pause').addEventListener('click',()=>v.pause());</script></html>''')

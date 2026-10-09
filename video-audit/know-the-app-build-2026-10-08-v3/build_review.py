from pathlib import Path
import json,shutil
D=Path(__file__).resolve().parent
q=json.loads((D/'qa.json').read_text())
shutil.copyfile(D/'preview/output-00000.jpg',D/'poster.jpg')
(D/'REVIEW.md').write_text(f'''# Know the App — v3 — shipped locally

Built 2026-10-08 from roll 6 using the October 1 edit plan. Shipped locally on 2026-10-08 after owner approval. Queued for batch deployment. Local release commit: 4c56e1e81c57a9b815d9a2b49b330a0c807c92fa. Installed at course-assets/your-choices/your-choices.mp4, cache key 20261008ship3.

- Runtime: 4:23.63, 7,909 frames at 30 fps, 1280×720.
- Roll 6 audio is copied unchanged; compressed audio stream hashes match.
- Current canonical Which Model?, How Much Thinking?, and How Much Research? boards, with narration-timed highlights using the established nominal 4 px renderer.
- Drawn camera, engine and project-planning examples from rolls 4 and 5. New college-physics comparison illustration replaces the property-like maps at 3:47–3:55.
- Useful source animation retained. Repaired settled answer labels to say Proposed answer / Review before using, removing claims that the answer has been verified.
- Banner highlights begin at 1:23.82, 2:39.52 and 4:02.54 and remain through each takeaway.
- Canonical closing: 48-frame hold, 150-frame push, 26-frame settle.
- Canonical boards and protected source files remain unchanged.

## Validation

Decoded all 7,909 output frames. Automated transition guard passed all 27 declared boundaries. Reviewed full-size previews of all three banner states, encoded frames immediately before and at each new highlight, and the new college illustration at its beginning, middle and end. The earlier v2 full-video visual review remains the baseline for unchanged sections. Audio identity: {q['audio_hash']}.

Candidate SHA-256: `{q['sha256']}`.

Editor continuous audiovisual listening was not completed; this limitation was disclosed before the owner reviewed the video, requested revisions, and approved shipping. Roll 6’s narration KEEP review and byte-identical audio are retained. No completed editor listening pass is claimed.

v2 is superseded by v3: three banner highlights and the college-comparison illustration. The generated image is stored in assets/college-physics-comparison.png. Build script: `scripts/video/build_know_the_app_v3.py`. Exact timeline and asset hashes: `edit-manifest.json`. QA: `qa.json` and `transitions/`.
''')
(D/'review.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Know the App — video review</title><style>*{box-sizing:border-box}body{margin:0;background:#f5f3ed;color:#222a30;font:16px/1.55 system-ui,sans-serif}main{max-width:1100px;margin:48px auto;padding:0 24px}h1{font-size:42px;line-height:1.1;margin:10px 0 18px}h2{font-size:22px}p{max-width:800px}.eyebrow{font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#5b4cb0}.player{background:white;border:1px solid #ddd9d1;border-radius:16px;padding:16px;box-shadow:0 8px 30px #24242b0a}video{display:block;width:100%;aspect-ratio:16/9;background:#eeefe4;border-radius:8px}button,a{color:#423594}.chapters a{display:inline-block;text-decoration:none;background:white;border:1px solid #c9c2e2;border-radius:20px;padding:8px 14px;cursor:pointer;font:inherit}.chapters{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0}.grid{display:grid;grid-template-columns:1fr 1fr;gap:28px;margin-top:28px}.note{border-left:3px solid #c29941;padding-left:14px;color:#5d5340}small{color:#65646a}@media(max-width:650px){main{margin:24px auto}h1{font-size:32px}.grid{grid-template-columns:1fr}}</style><main><div class="eyebrow">Build Your Skills · Shipped locally · v3</div><h1>Know the App</h1><p>Updated with all three takeaway-banner highlights and a university physics comparison illustration at 3:47.</p><div class="player"><video id="candidate" controls playsinline preload="none" poster="poster.jpg" src="../../Prompts/know-the-app-v3.mp4"></video><div class="chapters"><a href="../../Prompts/know-the-app-v3.mp4#t=0">Play from beginning</a><a href="../../Prompts/know-the-app-v3.mp4#t=81">Banner 1 · 1:23</a><a href="../../Prompts/know-the-app-v3.mp4#t=158">Banner 2 · 2:39</a><a href="../../Prompts/know-the-app-v3.mp4#t=225">Colleges · 3:47</a><a href="../../Prompts/know-the-app-v3.mp4#t=240">Banner 3 · 4:03</a></div><small>4:24 · Roll 6 narration preserved · Queued for batch deployment</small></div><div class="grid"><section><h2>What changed</h2><ul><li>The first takeaway banner highlights as “Start with the default” is spoken.</li><li>The second banner highlights at “Check the bottom banner.”</li><li>The 3:47 illustration clearly compares Texas A&amp;M and UT Austin physics programs.</li><li>The third banner highlights as “Use deeper research” is spoken.</li></ul></section><section><h2>Checks completed</h2><p>All 7,909 frames decoded. Audio is identical to roll 6. All 27 transition checks passed, and the boards and source files are unchanged.</p><p class="note">Shipped locally after your approval. Queued for batch deployment.</p><p><a href="../../Prompts/know-the-app-v3.mp4">Open full video</a> · <a href="REVIEW.md">Production notes</a> · <a href="edit-manifest.json">Edit record</a></p></section></div></main></html>''')

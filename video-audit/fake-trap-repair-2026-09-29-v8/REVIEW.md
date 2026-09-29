# Fake Trap v8 — narrow visual repair

Status: **visual repair complete; ready for candidate review.** Not installed, committed, or published.

## Authorization and scope

David requested the repaired version after the recommendation to preserve the existing narration and useful animation, add cutaways to the two long boards, and clear the lingering Corroboration highlight. This authorizes the visual-only repair. The previously accepted paraphrases are retained; no narration generation, graft, cut, pause, or duration change is included.

Source: frozen `Prompts/fake-trap-v6-source.mp4`, SHA-256 `8fffe6bdf9de2fc9e8b6736a18b2235f5b54e6992ec8fd1873a3bdd7195ab24e`, the exact file verified live during the evaluation. The raw generations are unavailable. This build therefore uses the finished source, with one final H.264 encode and packet-copied AAC audio. The frozen file protects donor frame references from future installation changes.

Candidate: `Prompts/fake-trap-v8.mp4`. Build script: `scripts/video/build_fake_trap_v8.py`. QA script: `scripts/video/qa_fake_trap_v8.py`. Build log and manifest are in this directory.

## Changes on the output timeline

| Output interval | Change | Source / treatment |
|---|---|---|
| 0:43.90–0:47.90, f1317–1437 | Principal-phone cutaway during “The video is real / that old test fails.” | Frozen source f612–732 (0:20.40–0:24.40), frame-for-frame at original speed. |
| 0:47.90–0:48.633, f1437–1459 | Return to the complete AI-era card, briefly unmarked. | Current canonical comparison JPG, at the existing settled camera position. Avoids bringing back the stale amber Before-AI verdict ring; the existing blue question ring resumes at f1459. |
| 2:38.067–3:09.533, f4742–5686 | Rebuild the compact checks board at its existing scale and timing. | Exact current checks JPG; fixed 4 px renderer strokes. Full opening; Source at f4819; Context at f4988; Corroboration at f5221. |
| 2:47.00–2:52.80, f5010–5184 | Context cutaway: reveal the clip date and the school to test whether the announcement applies. | Frozen source f6060–6234 (3:22.00–3:27.80), frame-for-frame at original speed. Retain the later complete worked example. |
| 3:00.70–3:09.533, f5421–5686 | Clear Corroboration while narration summarizes all three checks. | Unmarked canonical checks board. No banner ring: that sentence is taught later. |

Everything outside f1317–1459 and f4742–5686 uses the original picture. All audio and timing remain unchanged. No illustration generation or course asset edits.

## Board treatment

- **The Same Clip. Two Eras.:** original full opening, dense camera treatment, and owner-approved section rings retained outside the cutaway. New unmarked return keeps the complete active card visible. Two unbroken runs of **17.10 s and 20.00 s**, down from 41.10 s.
- **Why Some Fakes Aren't Friendly:** unchanged four-card walk, **21.57 s**. The review's explicit exception to “about twenty seconds” is preserved; no decorative filler.
- **Check the Source, Not the Pixels:** unchanged compact **9.70 s** span.
- **Move the Test Off the Image:** full-view opening and whole-card Source / Context / Corroboration outlines. Context cutaway splits the board into **8.93 s and 16.73 s** runs, down from 31.47 s. Clear the final ring at the summary onset.
- **Standard close:** unchanged 48-frame hold, 150-frame push to 1.2×, and final settled hold. Still the literal final frame.

The longest board run overall is now the unchanged 21.57-second four-motives walk. Existing detector, emotions, two-jaws, joke, school-verification, callback, victim-support, and safety scenes remain. The two borrowed visual sequences are the only new supporting insertions; they carry the original animation at 1× and no donor audio.

## Verification

- **Frame/time preservation:** independently decoded 9,240 frames, 30 fps, 1280×720, 5:08.00; matches the source exactly.
- **Audio:** packet payload SHA-256 is identical to the source; all 14,439 AAC packet PTS/DTS/duration/size tuples also match. There are no added audio seams or pacing changes.
- **Edited joins:** transition guard passes all 11 declared boundaries. All every-frame boundary strips were visually inspected, including the unmarked comparison return, both cutaways, ring onsets, summary clear, and board exit. No stale frame or unintended image was found.
- **Donor motion:** all 294 donor frames compared against the intended lossless source clips at their exact positions. Mean absolute RGB difference is 2.55/255, maximum 2.70, consistent with the final encode/color conversion; no dropped, reordered, frozen, or retimed donor frames.
- **Untouched picture:** 276 samples outside the changed spans have mean absolute RGB difference 2.46/255, maximum 2.76. The worst pair at f7320 was visually compared: the same illustration/layout/timing, with small RGB round-trip/re-encode bias (mean B/G/R −3.32/−1.47/−3.43). The video is not pixel-lossless. No unrelated content change was identified.
- **Boards:** 82 changed-board samples compared with their expected canonical states. Source, Context, and Corroboration bottom-edge widths each measure **4.0 px in encoded-frame samples**. Full-scale encoded return and summary frames were inspected: active cards complete; summary unmarked.
- **Close:** ten source/candidate samples plus the literal final frame retain the standard close (maximum RGB difference 1.89/255). The original hold/push/settle timing is retained.
- **Protected inputs:** build verified source, installed course video, two board JPGs, and index hash unchanged through encoding. The page/canonical media were not edited by this task.
- **Artifacts:** `verification.json`, `edit-manifest.json`, `qa.log`, `transitions/transition-guard.md`, `encoded-frames/`, and `repair-preview.jpg`.
- **Candidate SHA-256:** `72040bd3ee12a0a1f02695eb6a5c1cc4006c6e16be1e49f8582e20f3b31cbbfd`.
- No whole-file listening or real-time audiovisual playback is claimed. Inspection covered sampled encoded states, every frame around edited boundaries, and frame-for-frame donor correspondence. The audio was preserved and verified without alteration.


## Remaining inherited limitations

This is a narrow repair candidate, not a new whole-file shipping certification. Four generation-prompt verbatim lines remain paraphrased as explicitly accepted for this repair. Unchanged boards retain their historically approved stroke treatment; no unrelated retrofit was performed. The complete audio and every retained animation have not been re-auditioned end to end in this task. The Video Tracker was not accessed or updated.

The ring mask is rasterized at 4× resolution and downsampled before compositing, so `ken_burns_path.ring_px(720)` produces a measured 4 px delivery outline rather than inheriting OpenCV’s inclusive integer-line thickness. The shared renderer is unchanged.

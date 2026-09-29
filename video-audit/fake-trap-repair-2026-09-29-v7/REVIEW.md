# Fake Trap v7 — narrow visual repair

Status: superseded before handoff. Nominal 4 px OpenCV strokes measured 6 px; use v8. Review candidate only; not installed, committed, or published.

## Authorization and scope

David requested the repaired version after the recommendation to preserve the existing narration and useful animation, add cutaways to the two long boards, and clear the lingering Corroboration highlight. This authorizes the visual-only repair. The previously accepted paraphrases are retained; no narration generation, graft, cut, pause, or duration change is included.

Source: frozen `Prompts/fake-trap-v6-source.mp4`, SHA-256 `8fffe6bdf9de2fc9e8b6736a18b2235f5b54e6992ec8fd1873a3bdd7195ab24e`, the exact file verified live during the evaluation. The raw generations are unavailable. This build therefore uses the finished source, with one final H.264 encode and packet-copied AAC audio. The frozen file protects donor frame references from future installation changes.

Candidate: `Prompts/fake-trap-v7.mp4`. Build script: `scripts/video/build_fake_trap_v7.py`. QA script: `scripts/video/qa_fake_trap_v7.py`. Build log and manifest are in this directory.

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

Results will be recorded here after the exact candidate is encoded and checked. Source and canonical asset protection checks are part of the build. No whole-file listening or real-time audiovisual playback is claimed; this repair changes no audio, and packet payload/timing verification is required instead of asserting that unperformed listening occurred.

## Remaining inherited limitations

This is a narrow repair candidate, not a new whole-file shipping certification. Four generation-prompt verbatim lines remain paraphrased as explicitly accepted for this repair. Unchanged boards retain their historically approved stroke treatment; no unrelated retrofit was performed. The complete audio and every retained animation have not been re-auditioned end to end in this task. The Video Tracker was not accessed or updated.

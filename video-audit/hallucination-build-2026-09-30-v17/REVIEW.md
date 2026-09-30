# Hallucination v17 — production candidate

Built `Prompts/hallucination-v17.mp4` from the approved raw `Prompts/hallucination-3.mp4`. Video: 4:38.967, 8,369 frames, 30 fps, 1280×720. The original AAC container tail gives the same 4:39.03 overall duration as the source. This is a review candidate, not an installed or published release.

## Teaching and edit scope

The selected narration remains **KEEP on transcript evidence** under the [three-roll comparison](../hallucination-rerolls-2026-09-30/REVIEW.md). All narration, timing and pauses are unchanged. All 12,017 AAC packets, their timestamps and durations match the selected source exactly. No grafts or new silence.

The three-step overview and both worked examples retain the explicit Check the Match teaching. The Stanford example searches for the original study and ends with an unverified claim. The pizza example finds a real comment, then rejects it as support for cooking advice because the comment is a joke.

## Implemented visuals

| Span | Treatment |
|---|---|
| 0:00–0:49.43 | Exact current Nothing Sounds Wrong board, complete full view; question, answer, reveal and answer outlines follow the narration. |
| 0:54.67–1:02.03 | Corrected the four diagram cards: real university; invented study; invented sample; claimed 18% improvement / invented result. Removed false green verification states while preserving the surrounding diagram and concluding reveal. |
| 1:07.40–1:14.77 | Kept the paper/form-versus-substance animation. Replaced the invented attribution and paper title with an explicitly illustrative heading; removed the extra 18.4% and p-value. |
| 1:14.77–1:57.73 | Exact Why Hallucinations Happen board. Four full-height column outlines follow their spoken explanations. |
| 2:22.47–2:33.83 | Exact illustrated Real Text. Wrong Meaning. board; complete illustration, then the whole takeaway banner. The text-only upload stand-in is gone. |
| 2:43.80–3:25.97 | Exact Check the Claim board; three full-height column outlines, including Check the Match at 3:10.80. |
| 3:28–3:57 | Retained the Stanford worked animation. “Claimed study” replaces “Stanford Meta-Analysis.” The source-search pill is blue while searching, red when not found, then resets with the original transition. |
| 4:28.37–end | Exact canonical close. 48-frame full-view hold, 150-frame smooth push to 1.2×, 120-frame settled tail; final frame is the settled close. |

The certificate drawing, source-document/search comparison, glue/pizza illustration, joke bubbles, source-versus-interpretation diagram and both worked-example animations remain. Engine corner marks were cleaned on retained footage. Course boards use the shared fixed **4 px** post-resize ring renderer; no dives or crop changes. First openings remain unmarked for at least two seconds.

V16 was an internal QA candidate. V17 removes a residual green edge around the source-status pill and rebuilds from the pristine source, not from an encoded candidate.

## Encoded-output checks

- Full FFmpeg decode passed without errors; decoded frame count and frame rate match the source.
- AAC bytes, packet timestamps and packet durations are identical: `SHA256=b5195bf540e1dffbd5dd24d533e2f9537f59370357c61a2a9b977469ad0cba9d`.
- 123 source-scene samples preserve the original imagery outside the declared repair rectangles and corner-mark region.
- 80 encoded preview samples match the intended rendered states, including board openings, ring changes, corrected labels and closing endpoints.
- All 16 declared transition checks passed. Boundary strips and full-resolution encoded repair frames were inspected for stale labels and visual flashes.
- The small RGB shift was reproduced by both FFmpeg and OpenCV decoding. Maximum bias-adjusted preview difference is 1.122/255; this is codec/color-conversion variation rather than a frame alignment error. Raw and adjusted differences are retained in `qa.json`.
- Ring sampling found 13 course-board runs: solid color cores measure 4 px except teal at 5 px after antialiasing/chroma conversion; every outline uses the same shared 4 px renderer setting. The extra gold detection at 1:03–1:07 is the retained certificate artwork, not a course-board ring.
- Source, canonical board JPGs, lesson Markdown and the existing live MP4 hashes are unchanged. The site still references its existing canonical video.

**Unperformed:** end-to-end real-time audiovisual playback and subjective listening. This review uses complete source transcripts, exact audio identity, decoded frames, contact sheets and every-frame transition strips; it does not claim a full listening pass. The external Video Tracker was not accessed or changed.

## Reproduce and inspect

- Build: `.video-venv/bin/python scripts/video/build_hallucination_v17.py --preview`, then the same command without `--preview` (requires unused candidate path).
- Encoded QA: `.video-venv/bin/python scripts/video/qa_hallucination_v17.py`.
- Stroke measurements: `.video-venv/bin/python scripts/video/ring_stroke.py Prompts/hallucination-v17.mp4 video-audit/hallucination-build-2026-09-30-v17/rings --step 1`.
- Exact frame ranges, source/output hashes and protected inputs: `edit-manifest.json`.
- Detailed results: `qa.json`, `encoded-preview/`, `encoded-contact-*.jpg`, `transitions/` and `rings/`.

Source SHA-256: `34768db69bf30e0102db14c8a1e2796567617d7b58733a05711873ce8307ca22`.

Candidate SHA-256: `26be827326779654fa256de92cd59a59966c22f99c9b128700efed0e62d87bd2`.

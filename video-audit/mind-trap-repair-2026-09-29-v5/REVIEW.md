# Mind Trap v5 — approved review build, September 29, 2026

Scope: the user approved all refinements in the live evaluation: the generic-advice label, optional narration tightening, comparison readability, and the ELIZA camera crop. Build only; no local shipping, commit, or deployment is authorized by this request.

Candidate: `Prompts/mind-trap-v5.mp4` — **3:52.13**, 6,964 frames at 30 fps, 1280×720. Encoded-file verification results are below.

## Implemented treatment

| Item | Source time | Candidate time | Result |
|---|---|---|---|
| Comparison board | 0:26.80–1:07.67 | Same | Full unmarked opening, question highlight in full view, then a 0.8-second move beginning at 0:35.13 to a view holding both complete cards. Text is 27.3% larger than the previous full view. All nine highlights retain their original spoken onsets; fixed 4 px delivery outlines. |
| Generic-advice label | Final reveal within 1:14.00–1:16.53 | Same | “Identical Output to Anyone” becomes “Could fit almost anyone.” The original diagram, four-person reveal, arrows, and label fade remain. Only the small caption area changes. |
| Definition reprise | 1:16.53–1:21.67 | Same | Current canonical comparison JPG, unmarked full view, preserved. |
| ELIZA paper scene | 1:21.67–1:45.33 | Same | Existing illustration with a revised continuous camera move from full view toward the paper. The whole exchange stays visible. The reference is the first complete frame of the existing scene; this rebuilds the baked camera motion, with no new image generation. |
| Why AI Feels Like Somebody | 1:52.33–2:46.93 | 1:52.33–2:38.63 | Current canonical board, full-view arrival, whole first card → whole second card → entire takeaway banner. Full view throughout and fixed 4 px outlines. The second-card narration loses only the two redundant sentences below. |
| Standard close | 3:52.43–4:00.43 | 3:44.13–3:52.13 | Preserved picture sequence, both spoken lines, 48-frame hold, 150-frame push, and settled literal final frame. |

The comparison's enlarged view keeps both cards, including photographs, answers, and all three bottom rows, fully inside the frame. It does not crop inside the active card or reflow the asset. The title/question have already been introduced before the move. Both cards fit one uniform camera window, so no unnecessary left/right pan is added.

## Exact narration cut

Remove source frames **4608–4856**, the half-open interval **2:33.600–2:41.900** (8.300 seconds):

> This is a direct psychological reaction to language stimuli. It is a cognitive habit of filling in the blanks when a back-and-forth conversation occurs.

Retained before: “When you receive a conversational response, you automatically begin searching for a persona behind the text.”

Retained after: “So the rule to remember is this, sounding human does not make AI human.”

The join is at candidate **2:33.600**. Both cut boundaries are in quiet gaps, not scene cuts. Source RMS at the flanks is approximately −68 dBFS. The new speech gap is planned at about 0.54 seconds, accounting for the retained natural silence on either side. No silence is added. A 5 ms blend into a shared quiet room-tone segment on each side prevents a discontinuity without touching the neighboring words or changing the planned sample count.

The definition, both explanations, personal-context qualification, movie-versus-college contrast, preparation steps, human involvement, and both closing lines remain. The cut removes restatement, not a teaching point. The previously ambiguous ASR at 0:59 (“calling data patterns”) is unchanged; no unverified word repair was authorized or attempted.

## Sources and reproducibility

- Picture base: stable `video-audit/mind-trap-illustration-sync-2026-09-21/baseline-live-2026-09-21-v3.mp4`, SHA-256 `63c12abcb0235a454894178e457b4e9c5624307f00deebc87e61b3c9bdee3c60`.
- Audio base / protected current video: `course-assets/mind-trap/mind-trap.mp4`, SHA-256 `0b7f49264e5bfbaeb6a3904080c261da08bdc07e711966490f516e7a5c5e3671`.
- Canonical JPGs are loaded directly, including both appearances of the refreshed comparison board. The picture base predates that cast refresh; neither old comparison appearance is retained.
- Original raw rolls 5 and 6 are absent. The stable v3 finished file is the earliest surviving finished source found. This limitation is explicit: the candidate preserves its moving scenes and re-encodes them once, while boards render fresh from JPGs. Audio is decoded from v4, cut once, and encoded to AAC once.
- Build: `.video-venv/bin/python scripts/video/build_mind_trap_v5.py`.
- QA: `.video-venv/bin/python scripts/video/qa_mind_trap_v5.py`.
- Protected hashes, source/output mapping, camera specs, and cut details: `edit-manifest.json`.
- Prepared frame checks: `previews/`, including each highlight, the enlarged cards, caption fade, beginning/middle/end ELIZA camera, and the retained ending.

## Encoded-file verification

- Candidate SHA-256: `ec2084ebb4dc3d8485d59ae79476cf8f450dd2a574288dbbd81b19f73b24312e`.
- Full sequential decode completed: 6,964 frames; presentation timestamps advance uniformly by 1/30 second.
- All 15 declared transition checks passed. Every-frame boundary strips were visually inspected, including the narration cut within the steady second-card view; no stale insert was found.
- All five contact sheets spanning the candidate were visually inspected. Full-resolution encoded frames confirm complete comparison cards, consistent outlines, the corrected caption, the full ELIZA exchange at the end of its camera move, the takeaway banner, and the literal final frame.
- Fresh transcription of the encoded candidate confirms removal of the two sentences, retention of the surrounding explanation, and both closing lines. The measured quiet interval at the new join is 2:33.22–2:33.77 (0.55 seconds).
- Decoded candidate audio correlates 0.999984 with the planned edited PCM. This checks the encoded edit, not perceptual cadence.
- One-second picture samples outside changed ranges match the stable picture source within expected encoding differences (maximum mean absolute RGB difference 2.748/255).
- All protected source, canonical video, board, and lesson hashes remain unchanged.
- Evidence: `qa/summary.json`, `qa/targeted-transcript.json`, `qa/transitions/transition-guard.json`, `qa/sheets/`, and `qa/frames/`. Focused review clips are `qa/narration-join.mp4`, `qa/comparison.mp4`, `qa/label-and-eliza.mp4`, and `qa/closing.mp4`.

## Remaining perceptual review

This is a review candidate. No canonical video or lesson reference is changed. Source files and current boards are hash-protected. Audio listening and uninterrupted end-to-end viewing are not claimed; the candidate and targeted listening clip are supplied for that review. Automated audio comparison and transcription do not certify natural cadence, voice continuity, or absence of perceptual artifacts.

# Support Trap v11 — revised emotional-support board

Approved visual-only update to v9 following the lesson consolidation. Review candidate: `Prompts/support-trap-v11.mp4`, 4:45.50, 8,565 frames at 30 fps, 1280×720. Not installed or published.

The old Use AI to Get Ready for People board is removed. Its introductory narration now accompanies a preparation-to-human-presence diagram and a drawing of a person beyond the screen. The canonical Where AI Fits in Emotional Support board appears during the three-jobs introduction and returns for the preparation and danger explanations. Existing venting, follow-through, door-knocking, and later safety illustrations remain.

## Picture plan and final timeline

| Output interval | Picture / treatment |
|---|---|
| 1:11.53–1:22.53 | Roll 2, frames 2094–2466: preparation leading toward human presence, retimed in source order |
| 1:22.53–1:32.43 | Roll 2, frames 2526–2616: person beyond the screen, retimed in source order |
| 1:32.43–1:42.17 | New canonical board; complete unmarked opening, teal Ordinary Venting outline at 1:38.98 |
| 1:42.17–1:51.37 | Existing venting diagram: frustration becomes calmer words |
| 1:51.37–1:56.87 | New board returns; blue Preparation outline at 1:51.70 |
| 1:56.87–2:09.53 | V9's preparation/follow-through diagram, original timing |
| 2:09.53–2:15.23 | New board returns; red Danger outline at 2:09.92 |
| From 2:15.23 | V9's existing door-knocking illustration and remaining timeline |

The new board is compact and stationary at full view. All three whole-card outlines use the card accent and fixed 4 px delivery stroke. Its 1600×1020 artwork, text, aspect ratio, and banner are unchanged. The first full view lasts approximately 6.53 seconds before the first outline. Later appearances return unmarked until the next explanation starts. The earlier outline ends when its board appearance ends, preventing a carryover on the next return. The spoken banner occurs during the preceding human-connection illustration; no unrelated banner highlight is added later.

The changed interval is [2146,4057); the preparation diagram inside that interval is retained verbatim. The longest new board appearance is 9.73 seconds. Ring bounds in asset coordinates: Ordinary Venting [40,128,525,852], Preparation [557,128,1043,852], Danger [1075,128,1560,852]. Canvas offsets and exact frame states are in `edit-manifest.json` and `leg-jobs.json`.

## Narration and sources

V9's AAC audio is copied without re-encoding, cuts, gain adjustments, new pauses, or timing changes. The existing wording conveys the revised paragraph's meaning, as approved; the new paragraph is not a verbatim recording. The user's preferred continuous live ending and its timing are retained.

Original picture sources are reassembled in one encode using the v9 recipe. V9 supplies audio only. The surviving live donor remains the stable `video-audit/support-trap-build-2026-09-30-v5/donor-3bf1658e.mp4` snapshot. V9 SHA-256: `1f319094ba354c2048d900c8f3c62068b9f43c39971ee378f879588d9320137b`. All raw source hashes and canonical board hashes are checked before rendering. Existing candidates and installed assets are protected from writes.

Build: `.video-venv/bin/python scripts/video/build_support_trap_v11.py`

QA: `.video-venv/bin/python scripts/video/qa_support_trap_v11.py`

## Verification

V10 was an internal rendered check; its two board returns briefly carried the preceding column outline. V11 clears those outlines before each return. Narration, timing, pictures, and all other treatment are identical.

Preview inspection confirms readable complete cards, full-view introduction, correctly positioned highlights, relevant introductory drawings, and retained venting/follow-through illustrations. Final encoded checks are recorded in `qa-results.json`; boundary strips and changed-span samples are in `qa/`.

Full continuous audiovisual playback and listening remain unperformed. This is a narrow visual repair, not a shipping certification. V9's inherited live-story wording difference remains: it says the chatbot encouraged professional help without the lesson's qualifier “sometimes.” No voice graft was introduced to change it.

## Final encoded checks

- All 8,565 frames decode at uniform 30 fps; duration 285.50 seconds.
- All 27 declared transition checks pass. Changed-span samples and entry/exit strips were visually inspected, including the two corrected unmarked board returns.
- Copied AAC hash matches v9 exactly: SHA256=f1ba9a2dbe0748522870422f342fc416286e41259bd19dd39665c82a8beefbb7.
- Unchanged regions sampled every 15 frames differ by at most 0.014450231481481482 mean pixel levels from v9 after the original-source re-encode.
- All protected source, candidate, and installed asset hashes remain unchanged.
- The closing image remains the literal final frame. Full continuous playback/listening remains pending, as stated above.

Candidate SHA-256: c133890cc2a7d14ee8e0d44d4c955c02144c4c6c8da9b0710189040d54974655.

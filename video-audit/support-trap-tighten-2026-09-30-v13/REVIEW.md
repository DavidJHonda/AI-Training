# Support Trap v13 — approved tightening

Approved release: `Prompts/support-trap-v13.mp4`. Duration 4:31.967, 8,159 frames at 30 fps, 1280×720. This implements the owner's three approved changes to v11. Shipped locally September 30, 2026; queued for batch deployment.

## Changes

| V11 interval | V12 treatment |
|---|---|
| 2:08.00–2:09.53, frames [3840,3886) | Hold the last clean preparation-diagram frame, removing the premature native red outline on the third box. Audio unchanged. |
| 2:21.633–2:28.333, frames [4249,4450) | Remove “A chat transitions from a useful tool to a dangerous trap when it replaces action instead of encouraging it.” Join at output 2:21.633. |
| 4:27.900–4:34.733, frames [8037,8242) | Remove “Most of AI literacy is about how to use tools well. Here, using the tool well means knowing when to leave the chat.” Join at output 4:21.200, directly into the canonical close. |

Removed 406 frames / 13.533 seconds. Both narration cuts occur in measured quiet gaps, not inside speech. Quiet endpoints measured approximately −68/−72 dBFS for the first cut and −71/−72 dBFS for the second at frame-scale RMS. Only five milliseconds at either side of each join receive a fade; no pauses or global gain changes are added.

After the first cut, the retained sentence explains that polishing a message wastes time when someone needs immediate help. Its picture is the original urgency drawing, roll 1 frames [4275,4446), retimed to the retained 231-frame span. This removes the discarded tool/trap graphic entirely while preserving the useful drawing. The safety warning, story, safety board, safety inserts, and both closing lines are retained. The closing graphic keeps its original 48-frame prehold, 150-frame push to 1.2×, and 125-frame settled tail through the literal final frame.

## Sources and reproduction

V11: `Prompts/support-trap-v11.mp4`, SHA-256 `c133890cc2a7d14ee8e0d44d4c955c02144c4c6c8da9b0710189040d54974655`.

Picture is assembled in one encode from the original sources and exact current boards using v11's recipe. Audio uses the pristine assembled v9 PCM underlying v11, with only the two approved deletions and quiet-edge fades. Source, board, candidate, and installed asset hashes are protected. Original/output spans, geometry, and provenance are in `edit-manifest.json`.

Build: `.video-venv/bin/python scripts/video/build_support_trap_v13.py`

QA: `.video-venv/bin/python scripts/video/qa_support_trap_v13.py`

V12 was an internal check. V13 moves the held frame earlier to exclude even the initial tiny cap of the native red outline; all narration, timing, and other visuals are identical.

## Verification scope

Final encoded checks are recorded in `qa-results.json`, with transition strips and exact-export join transcripts in `qa/`. Full continuous audiovisual playback and perceptual listening have not been performed; automated and sampled checks do not certify the sound of the new joins. This is a narrow review candidate, not a shipping certification.

The inherited live-story wording difference remains: the narration says the chatbot encouraged professional help without the lesson qualifier “sometimes.” No unrelated narration graft was introduced.

## Final encoded checks

- All 8,159 frames decode at uniform 30 fps; duration 271.967 seconds.
- All 25 declared transition checks pass. The four changed boundaries were visually inspected in the encoded export.
- The held third-column border contains zero red-outline pixels. The preparation emphasis remains intact.
- Retained PCM is sample-identical to the original assembly except for the five-millisecond quiet join edges. Encoded audio correlation: 0.9999868.
- Join transcripts retain the urgency sentence and both exact closing lines, with the approved redundant sentences removed.
- Measured quiet gaps across the new joins: 0.802 seconds at 2:21.24–2:22.04, and 0.611 seconds at 4:20.91–4:21.52. No pause was added.
- All protected files remain unchanged. The closing board is the literal final frame.
- Perceptual listening/full continuous playback remains pending; waveform and transcript checks do not establish an auditory verdict.

Candidate SHA-256: eb1379e4487a1dec1997fa1c7c1cc12734a5d77249f8e8d05b51b5b3bf975536.

## Local shipping — September 30, 2026

Owner instruction: “ship it,” following review of the final candidate. Installed the approved candidate at `course-assets/support-trap/support-trap.mp4`; source, installed, and committed MP4 hashes match. Page cache key: `20260930ship13`. Actual runtime: 4:31.967; the page's whole-minute estimate is 5 min.

Local commit: `2534f605` — Ship Support Trap v13 and revised emotional support board. The commit contains only Support Trap's release, lesson, board source, and matching prep changes. Unrelated working changes remain untouched.

Owner shipping approval is recorded separately from agent checks. The previously disclosed full-playback/perceptual-listening limitation is not represented as a completed agent check. Encoded QA, exact installed hash, staged references, JavaScript parse, and prep sync checks passed.

No push or deployment was performed. Status: shipped locally; queued for batch deployment.

Post-commit cleanup removed 71 regenerable Support Trap scratch files (0.64 GB), preserving candidates, raw rolls, the stable donor, audit records, transcripts, and tracked files.

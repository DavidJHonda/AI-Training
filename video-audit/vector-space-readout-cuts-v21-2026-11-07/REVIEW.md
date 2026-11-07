# Vector Space v21 — three approved number-readout cuts

Candidate: `Prompts/vector-space-v21.mp4`. Review player: `review.html`.
Runtime **3:44.73**, 6,742 frames at 30 fps, 1280×720; **31.70 seconds shorter** than v20.

User approved: “Agree with those 3 cuts. Build it please.” Narrow build only; not installed, committed, or published.

## Changes

| Readout | Removed from v20 (half-open) | New join |
|---|---|---|
| Pepsi | 1:43.600–1:54.200 | 1:43.600 |
| Hot coffee | 2:01.400–2:11.400 | 1:50.800 |
| IT starting and updated numbers | 3:47.700–3:58.800 | 3:27.100 |

Pepsi now moves directly from “Next is Pepsi” to its similarity to Coke. Coffee moves from its introduction to its contrasting scores and neighborhood. The context explanation moves from connecting IT to CAT directly to “It remains a separate token, now near CAT.” The citrus comparison, both city questions, mystery drinks, revised sentence card, and final close remain.

Number-specific context highlights were removed with their narration, including the brief retained edges of those highlights, avoiding a flash before or after the cut. IT and the conclusion retain their original highlights. No new pauses, camera moves, drawings, or narration were added.

## Picture and audio provenance

The immutable v20 candidate and installed video both match SHA-256 `8fe721214ddc4e279db50edcf5762e8bf205111c4398fb9b5a6e65be7459eb47`. Pictures were rebuilt from the existing native v18 source renderer, original roll 8, retained illustration states, and v20 lesson sentence card, with v19/v20's six-frame sentence correction applied. They were not re-encoded from the previously compressed v20 pictures. Narration comes from v20's approved assembled track, cut with the same frame mapping and encoded once to AAC. Quiet joins use 5 ms ramps on each side.

The manifest records source hashes, exact retained spans, boundaries, and provenance. Canonical video, lesson page, source media, boards, and prior candidates remain unchanged.

## Board treatment and supporting scenes

| Board/scene | Treatment | Continuous duration |
|---|---|---|
| Drink map (Soft drinks / Coffee and tea) | Existing fixed full view, drink reveals and answer rings preserved; numbers stay visible | 84.77 s |
| THE SENTENCE | Existing complete static lesson card | 11.53 s |
| How Context Changes IT’s Position | Full view; unmarked explanation followed by IT and conclusion highlights | 18.00 s |

The longest inherited board sequence is the drink map at 84.77 seconds, with its existing progressive reveals. This narrowly approved cut preserves that treatment; no broad illustration redesign was performed. The city map remains 54 seconds. Supporting scenes retained: opening embedding drawing (0:00–0:22.27), nearby-relationships animation (0:22.27–0:31.40), scale/dimensions drawing (2:50.17–3:05.67), and lesson sentence card (3:05.67–3:17.20). No supporting scenes were added or removed except the approved temporal cuts.

## Verification

- Fully decoded all 6,742 frames; duration matches the edit plan.
- Transition guard passed all 44 declared boundaries. Every-frame strips at the three changed joins were visually inspected: no leaked frames or intermediate highlights. IT's retained settled highlight was inspected at full resolution.
- 459 unaffected picture samples compared with corresponding v20 frames: maximum mean pixel difference 0.12845/255 at audit resolution, consistent with encoding variation.
- Retained PCM is identical to v20's decoded track outside the 5 ms seam ramps. Encoded audio correlation to the assembly is 0.9999888, with no clipping.
- Final measured quiet gaps at the joins: Pepsi 0.745 s, coffee 0.498 s, IT 0.629 s. No extra pause duration was inserted.
- Full encoded ASR confirms all three readouts are absent and all adjacent statements, citrus comparison, and closing lines remain complete. See `transcript/vector-space-v21.txt`.
- Protected file hashes remain unchanged.

Direct listening and a full real-time watch have not been performed; automated checks and ASR do not certify subjective cadence. Listening checkpoints are **1:43.6, 1:50.8, and 3:27.1**. The review player has jump buttons and `qa/` contains ten-second join clips. This is a review candidate, not a whole-file shipping certification.

Build: `.video-venv/bin/python video-audit/vector-space-readout-cuts-v21-2026-11-07/build.py` (refuses to overwrite candidate).
Verification: `verify.py`, `qa.json`, `edit-manifest.json`, `transitions/`, and `transcript/`.

Candidate SHA-256: `04603ef7a5687a1f26f5e1b9d6e4dc268fd838145a2072fb82137252452ca0c2`.

## Local shipping — 2026-11-07

Owner approved the reviewed candidate with “ship it.” Installed the exact v21 candidate, updated the video cache key and manifest hash/size, and verified the local HTTP page reference and served video hash. The rounded duration remains “4 min.”

Committed only the release video, manifest record, and one-line lesson reference as `22e0a7369fea3b93a8ae61f9bea901065cef8101`. Unrelated Tokens edits remain untouched. Asset path/reference verification passed; the full hash check reports only the pre-existing Tokens image modification (two mappings), outside this release. Prior direct-listening/full-watch limitations remain recorded; owner acceptance is distinct from those checks.

**Shipped locally; queued for batch deployment.** No push or deployment.

Removed four regenerable audio/canvas intermediates (about 0.07 GB) after the commit. Retained all source rolls, candidates, join clips, build/QA records, screenshots, and transcripts.

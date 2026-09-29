# Where AI Works Best v9 — September 29, 2026

**Built for review:** `Prompts/where-ai-works-best-v9.mp4` — 3:53.900, 7,017 frames, 1280×720 at 30 fps, 22,275,241 bytes.

SHA-256: `6cdac90a1ef219f208cefb9ee070b5280003e47a1ac9aa98c773f1667d4dec4f`.

The user approved this narrow opening repair with “build it please.” The opening now frames essay help as **brainstorming angles for an essay**. The animated card reads **Essay Ideas / Brainstorming**. Other examples, the lesson body, and v8's translation/highlight repairs are retained. At the build handoff, the candidate had not been installed or published. The subsequent local shipping approval and release are recorded below.

## Changed spans

The [approved plan and source hashes](PLAN.md) record exact inputs. Replace roll 3 source 0:03.033–0:04.700 with roll 1 source 1:50.200–1:52.867. The donor appears at output **0:03.033–0:05.700**, followed by the original “plan a schedule, build code, or draw an image.” Gain is +1.1 dB, matching the measured surrounding passage. No synthetic voice or new silence was introduced.

Track the source label's entrance translation and fade from frame 106 through 402, remove the original glyphs, and place the new wording within the existing card. Preserve the document icon, connectors, other cards, and all original animation frames. Hold fully drawn source frame 150 for one additional second while Essay is emphasized. The repaired opening ends at output **0:14.433**; all subsequent v8 content moves later by exactly one second.

The five course boards, their relative highlight timing, and their cameras remain unchanged. Their lossless legs were reused only after checking exact canvas bytes and relative rendering specifications. The finished candidate was assembled from pristine raw rolls, canonical boards, and lossless intermediates. It was not made by re-encoding v8 as its video source.

## Actual candidate checks

- Full sequential decode: **7,017/7,017 frames**.
- Transition guard: **32/32 PASS**, including the new audio joins, label reveal, added emphasis hold, and return to the first course board. Inspected every-frame strips at output frames 91, 106, 151, 171, 181, and 433. No stale frame or abrupt label replacement was observed.
- Inspected the encoded opening contact sheet, full-size settled label, faded label at the opening's last frame, and unchanged final frame. The new text fits inside the card and follows its original opacity and entrance movement. Real-time motion playback was not performed.
- **220 sampled retained visual frames after the opener match v8 exactly**, including the final frame, after the 30-frame offset. The exact sample count is recorded in `qa.json`.
- Assembly PCM matches v8 exactly before the first new fade, through the retained opening suffix away from boundary fades, and throughout everything after the opener. The ending opener room-tone fade differs for 199 samples in its last 5 ms (maximum 9 of 32,768 PCM amplitude units), because the helper's room-tone loop phase follows the changed segment length. This occurs in the quiet gap, with no speech change.
- Encoded audio correlation before the repair is **1.0**, after it **0.9999774**, and against the gain-adjusted donor **0.9999571**. These verify preservation, not subjective audio quality.
- A fresh transcript of the opening clip copied from the actual encode confirms “brainstorm angles for an essay, plan a schedule, build code or draw an image.” It transcribes the introductory auxiliary as “could”; the earlier donor transcription rendered “can.” No claim about that ASR distinction substitutes for listening.
- At −40 dB, the assembled entry gap measures **0:02.855–0:03.333 (0.478 s)**; the exit gap **0:05.678–0:05.862 (0.184 s)**. Both seams are in quiet intervals. No new pause was added.
- All raw rolls, prior v7/v8 candidates, course MP4, lesson Markdown, and six canonical board JPGs retain their pre-build hashes. The course page changed concurrently for **AI Is Different**, triggering the renderer's final whole-page protection assertion after encoding had finished. The matching baseline was found in Git and compared: Where AI Works Best's `whatitdoesbest` entry is identical. This task neither changed nor reverted the page. The manifest records the exception and comparison, rather than claiming the whole page hash was unchanged.
- Corner cleanup: 3,336 cloned frames, 63 inpainted, no declined frames. Changed opener counts were recomputed from the saved v9 mask; the unaffected remainder uses v8's verified counts.

The longest individual board appearance remains **19.0 seconds**, and the longest contiguous sequence of adjacent boards remains **25.867 seconds**. Canonical assets, four-strength teaching sequence, exact-width v8 highlights, and standard 48-frame hold / 150-frame push / settled close remain as documented in the [v8 review](../where-ai-works-best-v8-2026-09-29/REVIEW.md). No full ring scan or full narration reevaluation was repeated for this opening-only repair. The previously accepted omission of “It learned patterns it can apply to new problems” is preserved.

## Listening still needed

**The new joins at 0:03.033 and 0:05.700 have not been heard by ear.** Review the first 16 seconds in `opening-review.mp4`, which was copied from the encoded candidate, for cadence, voice continuity, and any audible splice. Existing v8 listening limitations remain. This is a completed review build, not a whole-file shipping certification.

## Reproduction and evidence

Build: `scripts/video/build_where_ai_works_best_v9.py` (final run used `--render-existing`). Label/animation helper: `scripts/video/where_ai_works_best_v9_opening.py`. Verification: `scripts/video/qa_where_ai_works_best_v9.py`.

Evidence: `edit-manifest.json`, `qa.json`, `qa.log`, `opening-label-tracking.json`, `encoded-opening-sheet.jpg`, `frames/`, `transitions/`, `encoded-transcript/opening-review.txt`, and `opening-silences.txt`.

## Retained supporting scenes (output timeline)

- 0:25.600–0:41.967: Roll 3 drawings: intent/order/flow cards, button test, marked-up draft (break)
- 0:50.233–0:57.333: Roll 3: code monitor + four-strengths map under the bridge
- 1:12.867–1:20.933: G9 roll 1: complete Reshape examples including translate a message
- 1:46.800–1:56.733: Roll 3 drawing: user prompt with essay angles / club names (break)
- 2:18.133–2:30.633: Roll 3 drawings: textbook, scholarship, two articles (break)
- 2:52.867–3:03.400: G6 roll 1: examples, over roll 3's trip/code/colleges/experiment drawings (break)
- 3:09.900–3:28.800: G7 roll 1: vast exposure ... common human formats (roll 3 map, banner covered)
- 3:28.800–3:44.267: Roll 3: This massive exposure ... guarantee ... judgment (rapid draft / human judgment drawings)

## Local release — September 29, 2026

The user subsequently said **“ship it”** after the build response disclosed the listening limitation. Installed the exact approved v9 at `course-assets/where-ai-works-best/where-ai-works-best.mp4`, verified its SHA-256 and full 7,017-frame decode, and changed only the `whatitdoesbest` cache key to `20260929ship1`. Displayed runtime remains “4 min.”

Local commit: `433592b9e2c12b0a10a4ae7f6e6da9abb955e938`. Exactly two release files were committed: the canonical MP4 and its one-line `index.html` reference. The committed video bytes match the approved candidate hash above. Unrelated changes were preserved; audit/build files were not added to the release commit.

**Shipped locally; queued for batch deployment.** No push, deployment, or public-site verification was performed. Owner shipping approval is recorded; agent listening and real-time playback were not performed and are not claimed as passed.

Post-commit cleanup removed 49 regenerable scratch files scoped to the v8/v9 audit folders (board legs, WAVs, padded canvases). Raw rolls, candidates, review clip, manifests, QA results, transcripts, and frame/transition evidence were retained. Shared hardlinks mean logical file sizes are not a physical disk-space measurement.

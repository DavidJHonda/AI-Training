# AI is Different v17 — playlist repair

Built November 2, 2026, from pristine sources under the user's three corrections to v16.

**Candidate:** [ai-is-different-v17.mp4](../../Prompts/ai-is-different-v17.mp4), **4:20.800**, 7,824 frames at 30 fps, 1280×720. Approved and shipped locally on November 2, 2026; queued for batch deployment. See shipping record below.

## Changes

- Show the canonical playlist board at **2:55.367**, on “This graphic shows…,” replacing the digital/physical drawing. Start unmarked, then retain the existing whole-left-section highlight.
- Remove v16 **3:10.733–3:19.100** (frames 5722–5973): the complete spoken three-song/artist/order list. This removes 8.367 seconds. The field explanation now leads directly to “On the right…”. The user's explicit removal supersedes the earlier generation requirement to read every table row; named songs remain where they explain arrows and exclusion on the right.
- Keep the full board visible for “On the right…,” now approximately **3:11.33**, and highlight its AI half. Remove the handwriting close-up cutaway. Keep the board through the visual-cue explanation, until **3:37.200**, when the original training animation resumes.

The continuous 41.833-second board passage follows the user's direct board-reference correction and supersedes the prior optional drawing-break plan. No additional pause or new visual was introduced. All subsequent timing shifts earlier by 8.367 seconds; the established closing motion is preserved.

## Verification

- Entire candidate decodes to the planned 7,824 frames.
- All **17 declared boundaries pass** the transition guard. The changed entry, narration join, board exit, and settled board states were inspected in encoded frames and boundary strips; no stale donor frames were found.
- Edited PCM is **exactly v16 PCM with only frames 5722–5973 removed**. No other audio changes.
- The new encoded join lies in a measured quiet gap at **190.474–191.307s** (0.833s). ASR on the actual encoded join reads: “We have specific columns for song, artist, and play order. On the right, AI works with an unstructured handwritten note.”
- Rules/cooking board assets and render specifications match v16 exactly. Closing specification matches after its timeline shift. Protected hashes are unchanged.
- Listening and continuous audiovisual playback were not performed. The new join at **3:10.733** still needs a listening check; previous v16 listening limitations remain. This limitation was disclosed before the user explicitly authorized shipping; it is not recorded as a passed listening review.

[Playlist context excerpt, output 2:52–3:40](playlist-review.mp4) · [QA measurements](qa.json) · [Edit manifest](edit-manifest.json)

SHA-256: `9e49ef0d6f750588a1ff7f0942914ecafa5c8c4dfa1049d33c7838a8ee10a76f`

Build: `.video-venv/bin/python scripts/video/build_ai_is_different_v17.py`

QA: `.video-venv/bin/python scripts/video/qa_ai_is_different_v17.py`

## Local shipping — November 2, 2026

User approved with “ship it.” Installed v17 at `course-assets/ai-is-different/ai-is-different.mp4`; exact candidate hash confirmed after installation and commit. Local commit: `199b418dc456d9226c9040b59113e5f1dcb93552`. Updated the lesson cache key to `20261102ship1` and the manifest hash, byte size, approval date, and source candidate. Displayed runtime remains 4 min (actual 4:20.800).

Full asset verification passed: 244 retained assets, 515 original path mappings, 263 website references, and 54 finished videos. Only the canonical video and its two release metadata entries were committed. Existing unrelated diff hunks in the shared files were preserved exactly. No push or public deployment was performed. **Shipped locally; queued for batch deployment.**

Removed 20 regenerable scratch files from the v16/v17 audit folders; raw generations, immutable v15 donor, candidates, and review evidence remain. Rebuilding after cleanup requires regenerating the v16 source WAVs first. Listening and continuous playback were not performed by the agent; user shipping approval followed disclosure of that limitation.

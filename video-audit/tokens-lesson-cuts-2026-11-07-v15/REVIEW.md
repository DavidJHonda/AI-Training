# Tokens v15 — November 7 lesson changes

Status: shipped locally; queued for batch deployment. See the release record below.

Authorization: the user approved removing the chat setup/board and repeated cat-board banner, approved the revised opening transition, then explicitly requested updating the video for those changes. This is a narrow repair. Existing complete-card camera treatment is retained and refitted to the shortened image; no new pauses or speed changes.

Candidate: `Prompts/tokens-v15.mp4`, 3:22.133 (6,064 frames at 30 fps, 1280×720). Parent: installed v14, identical to `Prompts/tokens-v14.mp4` (SHA-256 `9e4ca49699e7d68075ebe3ad0bda9d7864073f21990d2f83d5b9a4d7f296f132`).

## Exact changes

All cut times below refer to v14. Half-open intervals were selected in measured PCM troughs, not at visual cuts or transcript timestamps alone.

| Parent interval | Words removed | Output join |
|---|---|---|
| 0:13.667–0:15.800 | “Take a look at this chat interface.” | 0:13.667 |
| 0:18.667–0:39.067 | “Consider this simple chat interaction about Avengers movies.”, the full Avengers exchange, and “You sent and received words.” | 0:16.533 |
| 2:59.167–3:03.067 | “A token ID identifies the token. Meaning comes later.” | 2:36.633 |

The opening retains the existing recording: “The exact same rule applies to AI. How did your words become numbers that AI could work with, and how did AI’s response turn back into words you could read?” The written lesson uses the approved present-tense wording; this edit preserves the original voice and the same two questions rather than synthesizing replacement narration. The removed chat is no longer referenced by an introductory or retrospective sentence.

The surviving AI bridge uses the existing question → AI → reply diagram, continued into the existing question sequence. All other supporting animation mappings remain unchanged, including v13/v14's building-block and reply corrections.

## Affected board plan

| Board | Highlights and camera | Output span | Reason |
|---|---|---|---|
| You Use Words. AI Uses Numbers. | Removed with its narration; surviving bridge uses the existing question diagram. | None | Approved redundant chat cut |
| You See a Word. AI Starts With a Number. | Exact shortened current JPG. Full unmarked opening for 139 frames; teal whole human-card outline, then purple whole AI-card outline; complete-card dives, return through full view between cards and at the end. Fixed 4 px stroke. No banner or banner highlight. | 2:16.167–2:36.633 | Same approved treatment fitted to the new artwork |

The cat asset is 1808×870. Card bounds in image coordinates: left [46,144,841,668]; right [924,144,840,668]. Canvas placement [396,315] in a temporary 2600×1500 stage permits centered cameras. Full camera width 1808; both detail cameras use width 1288. The current JPG is used directly, without reflowing text or modifying the artwork for video.

The examples and Send boards retain their current JPGs and previous treatment. The Send board starts four parent frames later because the last cut ends in a quieter trough; no speech or meaningful visual reveal is lost. Standard close motion is preserved.

## Sources and verification

Rendered from pristine rolls `Prompts/tokens-4.mp4` and `Prompts/tokens-6.mp4`, the retained lossless PCM assembly, and canonical board assets, in one encode. It is not another lossy render of the finished v14. The v14 comparison is used for verification only. Sources, exact frame mapping, asset hashes, and protected files are recorded in `edit-manifest.json`.

Prepared PCM equals v14's lossless assembly with exactly the three listed ranges removed. Total reduction: 26.433 seconds. No added pauses. The 200 ms neighborhoods of the three joins measure -75.35, -72.81, and -77.83 dBFS. These measurements establish quiet edit boundaries; they do not establish audible cadence.

Preview full-view and settled human/AI-card frames inspected. Every cat camera frame checked geometrically to keep the active target fully inside the delivery frame.

Build: `.video-venv/bin/python scripts/video/build_tokens_v15.py`

QA: `.video-venv/bin/python scripts/video/qa_tokens_v15.py --transcribe`


## Encoded candidate results

- Decoded all 6,064 frames at 30 fps and 1280×720. Runtime 3:22.133.
- Inspected the actual encoded opening joins, cat-board entry, and cat-to-Send boundary strips. No remnant chat board or repeated banner appears.
- Transition guard: 17 automatic passes out of 18 boundaries. Its sole flag at frame 4699 is continuous planned pullback motion immediately before the Send cut, not an intermediate scene. The every-frame strip was visually inspected; all 614 encoded cat-board frames match their intended renderer (maximum mean pixel error 2.833/255), independently confirming no stale content. The raw detector flag is retained in the audit.
- Inspected encoded full and complete-card frames, the opening diagram, and the final closing frame. Active cards remain whole; fixed-width outlines follow current card edges.
- 19 samples from untouched spans match the v14 source within mean pixel error <3/255.
- Prepared PCM is exactly the prior lossless assembly with only the three requested cuts. Encoded/reference audio correlation 0.99998369; zero clipped samples. Direct listening remains unperformed.
- Current lesson, source Markdown, canonical JPGs, and installed video match protected hashes.
- Candidate SHA-256: `2eee4b7c2519091fe63c759f9873c93b7bde242161c7875c3121b9bb79ff7433`.

## Transcript check

Full encoded audio was transcribed with local faster-whisper small.en. The opening goes directly from the everyday-computing explanation to the AI bridge and both conversion questions. The cat explanation goes directly from “The number identifies the token, not its meaning” to the Send introduction. No Avengers exchange, chat-interface reference, retrospective “You sent and received words,” or repeated “Meaning comes later” remains. Both closing lines are retained. Transcript and audio-data checks do not substitute for listening; pre-existing ASR ambiguities in token-piece pronunciation remain outside this cut-only scope.

## Review limits

Direct listening and full end-to-end playback with sound have not been performed. New audio joins need listening review; the existing v14 pronunciation and source-animation limitations remain outside this narrow repair. No whole-video KEEP or shipping certification is claimed. Existing longest single board run remains the examples board at 49.733 seconds; the revised cat-plus-Send run is 45.367 seconds. No supporting scenes or pauses were added to address those pre-existing durations.

## Local release — November 7, 2026

The owner explicitly requested “ship it” after reviewing v15 and the disclosed listening limitation. Installed the approved bytes at `course-assets/tokens/tokens.mp4`; updated the lesson cache key to `20261107ship1` and displayed runtime to 3 min. Committed the matching approved lesson cuts, shortened cat board, source materials, and every affected asset-manifest hash/size row. Original migration hashes were preserved.

Local commit: `880a162eed91721f440b65085a9f97bf135d408a`. Installed video hash: `2eee4b7c2519091fe63c759f9873c93b7bde242161c7875c3121b9bb79ff7433`. The installed file matches both the approved candidate and the committed blob. Committed lesson reference verified. `verify-course-assets.py --migration-hashes`, Tokens source sync, inline JavaScript parsing, and whitespace checks passed. Unrelated Vector Space audit work remains untouched. Build and QA scripts and audit records remain local.

No GitHub push or deployment performed. **Shipped locally; queued for batch deployment.** The previously disclosed direct-listening limitations remain recorded; shipping authorization is not a new listening certification.

Post-commit cleanup removed eight regenerable scratch files (about 0.04 GB) from this audit folder only. Review records, transcripts, preview frames, transition strips, the review candidate, and pristine source media remain. Concurrent edits to index.html appeared after the release commit and were left untouched.

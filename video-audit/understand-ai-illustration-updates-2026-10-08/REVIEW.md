# Understand AI illustration updates — 8 October 2026

User approved the three proposed inserts: “I like the ideas. Let's build them.” The process is now a section-by-section illustration improvement pass, not an experiment in style. The initial build was a narrow visual-only update for review. The approved candidates are now shipped locally; queued for batch deployment. See the local release record below.

## Sources and outputs

| Lesson | Verified source | New candidate | Changed frames (end exclusive) | State change |
|---|---|---|---|---|
| Training | Prompts/training-v9.mp4, identical to pre-update course asset | Prompts/training-v10.mp4 | 5222–5429 (174.067–180.967 s) | f5334 / 177.8 s: choose actionable answer |
| Embeddings | Prompts/embeddings-v10.mp4, identical to pre-update course asset | Prompts/embeddings-v12.mp4 | 1475–1930 (49.167–64.333 s) | f1703, 1715, 1743, 1761, 1779, 1807: six dimensions reveal in order |
| AI Is Math | Prompts/ai-is-math-v8.mp4, identical to pre-update course asset | Prompts/ai-is-math-v9.mp4 | 3099–3296 (103.3–109.867 s) | f3216 / 107.2 s: reveal first coin |

Exact sequentially measured source cuts refine the provisional windows in the approved opportunity report. All changes remain within the approved supporting shots. Approximately 28.63 seconds are replaced across the three videos. Full hashes, encoding, and source identities are in the per-lesson manifests. Finished approved files are the available assembly sources; this is one additional high-quality video encode, with original AAC audio copied unchanged.

## Teaching and visual treatment

- Training: two short answers remain visible. The actionable first step becomes selected; the panel says Training Feedback. No claim that ordinary chat immediately updates model weights. This introduces the unchanged preference-tuning board.
- Embeddings: a student records ratings beside Coke and coffee. A separately typeset six-trait strip preserves the lesson order and 0–10 scale. The highlight advances through all six spoken dimensions, revealing Coke scores 9, 1, 10, 2, 3, 8 in order. Previously revealed scores remain visible, so the quick spoken list builds a lasting row. Timings follow the existing word-level transcript: Sweet 56.78, Bitter 57.16, Fizz 58.10, Heat 58.70, Caffeine 59.30, Dark 60.22 seconds, rounded to the nearest 30-fps frame. The original v11 preview is retained; v12 is rebuilt directly from v10 to avoid stacked encoding. This is a human-rating analogy; the existing taste-versus-AI distinction remains intact.
- AI Is Math: matching photographic states show the first lid lifted to reveal heads; the second result stays hidden. No coin is flipped and no second result is revealed. The existing outcome-elimination animation and 25%→50% explanation follow.

Generated assets and complete prompts are retained under assets/. Built-in image_gen was used for all four photographic files, including the matched coin edit. Code renders exact instructional labels and screen content; photographic scenes were not retouched in code.

## Course boards and camera plan

No course board is replaced or retimed. Adjacent boards retain their current canonical appearance, existing highlights, complete-card camera moves, and source durations. The supporting replacements begin and end at the original cuts. In particular:

| Adjacent explanation | Preserved treatment |
|---|---|
| Training: 2 · Instruction Tuning / 3 · Preference Tuning | All source board frames, text, highlighting, and cameras retained |
| Embeddings: Meaning Becomes an Ordered Row of Numbers | Full board appears at its original frame 1930; all subsequent table/quiz/comparison/lookup material retained |
| AI Is Math: the following outcome-elimination diagram and A Clue Changes the Odds | All outcome elimination, calculations, board frames, and camera treatment retained |

No new board-density, pause, or full-view exception is introduced. Previously retained material and owner exceptions outside these shots are unchanged. Longest board runs and unrelated source narration were not re-audited in this narrow build. The earlier source-matched lesson review records remain background evidence, not certification of these new candidates.

## Verification and review limits

Verification results are recorded in verification.json. Complete decode of each candidate must match source counts; copied audio packet hashes must match; every changed frame is compared with its intended rendered state, while unedited frames are sampled each second and at edit boundaries. Transition guard covers entry, state change, and exit for each insert. Encoded settled states and all fourteen current boundary strips are visually inspected before delivery.

No continuous audiovisual review or listening assessment is claimed. Review the three before/after excerpts with sound, especially Training 174.067–180.967 s, Embeddings 49.167–64.333 s, and AI Is Math 103.3–109.867 s, plus their three-second handles. The full candidates preserve audio; excerpt audio is reencoded for preview playback. The Video Tracker was not accessed or edited. These technical checks do not establish full audiovisual shipping certification. The initial build left course assets untouched; installation followed the owner’s explicit shipping approval below.

## Follow-up revision

The user requested highlighting and scores for every dimension as spoken, and approved the other two updates visually. Only Embeddings was rebuilt (v12); Training v10 and AI Is Math v9 remain unchanged. The new Embeddings verification covers its full decode, copied audio, each of seven rendered states, all eight entry/state/exit boundaries, and samples of retained frames. Word-timestamp alignment is automated; listening assessment is not claimed.

## Local release — 8 October 2026

Owner authorized “ship the videos” after reviewing the updates. Installed Training v10, Embeddings v12, and AI Is Math v9, and updated only their lesson cache keys. Candidate, installed, and committed video SHA-256 hashes match. Commit: `39d8d05e98790d82135badb63a85bfe8364b3a65`. Status: **shipped locally; queued for batch deployment**. No push or deployment was performed. Unrelated site changes were preserved. Full installation hashes and references are in `local-install.json`.

Prior complete-decode, audio-payload, frame, and transition verification applies to these exact files. Continuous listening and audiovisual assessment by the agent remain unperformed; owner approval is recorded separately from technical verification.

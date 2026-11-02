# Context Matters: Outside the Window pickup review

Scope: compare the three newly uploaded replacement-narration takes with the approved five-sentence pickup and current page. Full timestamped transcripts are in `transcripts/`. The installed video matches the preparation manifest’s source hash. Listening status throughout: ASR transcript and audio signal review only; the assistant has not auditioned these recordings. Voice identity, naturalness, and seam quality require listening review. This document does not claim a final whole-video KEEP verdict.

## Take 1 — 29.20 seconds — REPAIR

The assignment example and how to share material are RICH at 0:00–0:08.70, in the approved words. The earlier-chat limitation is TAUGHT at 0:09.74–0:12.98; the memory/projects qualification is RICH at 0:14.08–0:18.80. The information check is TAUGHT at 0:21.92–0:25.62. All five required sentences appear according to ASR.

Addition: “So always remember this rule” at 0:19.70–0:21.16. This is unnecessary extra narration. A feasible alternate repair would remove this whole sentence between the preceding “missing details” and the final “Before you ask, check.” No phrase-level graft is needed, but that new internal join has not been auditioned. No teaching error identified in the supplied passage.

## Take 2 — 70.40 seconds — REPAIR; selected donor

The roll first gives an expanded explanation at 0:00–0:44.94, then repeats the exact approved five-sentence narration at 0:45.78–0:66.72. Use only the final passage; reject the duplicate first explanation for this pickup. It is not a better complete roll simply because it covers the topic twice.

The selected passage’s 67 spoken words match the approved wording exactly after case/punctuation normalization. It preserves all essential points and needs no internal cuts. The donor trim is frame 1367 through frame 2015 exclusive (45.5667–67.1667), with both boundaries inside measured silence. Content-only assessment of this extracted passage: all required teaching is present; listening remains unverified.

## Take 3 — 239.20 seconds — REROLL for this pickup; not selected

This roll restarts the subject and supplies a full explanation instead of the requested pickup. The basic local-file distinction is TAUGHT at 1:17.60–2:00.48, and the final information check is TAUGHT at 3:35.66–3:43.00. The earlier-chat section is WRONG in material ways: “you are starting with a blank slate” and “the system resets entirely ignorant” (2:19.70–2:31.74) conflict with the approved memory/projects qualifier. It later acknowledges memory/projects (2:31.74–2:44.82), but describes their operation too categorically.

Other errors/additions: the absolute claim that information must be explicitly pasted or uploaded into that specific active chat (0:44.52–0:57.14) excludes the app tools and carried context taught in this lesson. “That data starvation is exactly what triggers most hallucinations” (1:02.20–1:12.44) is unsupported and outside the approved teaching. The closing claim that useful output depends “entirely” on the data environment (3:49.08–3:55.62) also overstates the lesson. The exact required script is not delivered as one usable passage. No audio from this roll is needed.

## Beat comparison and best-of plan

| Teaching point | Take 1 | Take 2, selected final passage | Take 3 | Choice |
| --- | --- | --- | --- | --- |
| Open assignment is not automatically usable | RICH, 0:00–0:03.90: “Having your assignment open on your laptop doesn’t mean AI can use it.” | RICH, 0:45.78–0:49.00: same exact line | TAUGHT, 1:17.60–1:37.46, expanded local-device explanation | Take 2: exact continuous passage |
| Share material or use app tools | RICH, 0:04.48–0:08.70: “Share the relevant material…” | RICH, 0:49.50–0:53.24: same exact line | TAUGHT, 1:37.78–1:55.54; conflicts with earlier absolute pasted/uploaded restriction | Take 2 |
| Don’t assume every earlier-chat detail is available | TAUGHT, 0:09.74–0:12.98: “And don’t assume…” | TAUGHT, 0:54.14–0:56.92: same exact line | WRONG qualifier, 2:19.70–2:31.74: “blank slate… entirely ignorant” | Take 2 |
| Memory/projects can carry information; supply missing details | RICH, 0:14.08–0:18.80: “Memory and projects can bring information forward…” | RICH, 0:57.64–1:02.58: same exact line | THIN/misleading, 2:31.74–3:07.80: adds categorical summary/compression claims | Take 2 |
| Final information check | TAUGHT, 0:21.92–0:25.62; preceded by added rule sentence | TAUGHT, 1:03.38–1:06.72: “Before you ask, check. Does AI have the information it needs?” | TAUGHT, 3:35.66–3:43.00; then unrelated closing | Take 2 |

Base video: installed `course-assets/context-matters/context-matters.mp4`. One coherent donor passage from take 2 replaces the old four-category explanation; no best-of mixing within the pickup. SOURCE_QA: approved segment agrees with the current page and canonical board. The “And” connective is the approved spoken addition to the second card.

## Board and audio plan

| Board | Highlighting sequence | Camera | On screen / breaks | Reason |
| --- | --- | --- | --- | --- |
| Outside the Window | Complete unmarked board under existing lead-in, then whole left card, whole right card, full takeaway band | Stationary full board, compact at 1280×720; padded house canvas | Source entry 2:50.967 through the inserted takeaway; about 24.63 seconds total | The two-card board remains readable at full view; three distinct teaching beats keep the hold active. |

Use the exact corrected canonical asset, with four-pixel outlines on the complete measured card bounds. This executes the two-card treatment already agreed during preparation. No additional pause is inserted. The source lead-in’s last words are preserved before the new voice. The next source shot and the complete Forgetting Problem and closing are preserved after it.

Source visual entry is frame 5129; exit is frame 6381, verified by sequential frame decoding. Source audio is replaced only from frame 5220 (174.0 seconds, a measured pause) to frame 6381 (212.7 seconds, the visual cut and a measured pause). The outgoing original explanation’s final word ends before the latter boundary; the next spoken question begins afterward. The new passage is gain-matched approximately +4 dB with a limiter applied only to the donor, and five-millisecond seam ramps inside silence. Existing pre/post audio is unchanged in assembled PCM outside those ramps. Expected natural speech gaps at the joins: approximately 0.58 and 0.45 seconds. No extra silence is proposed.

The donor visual is a course-board recreation and is replaced with the canonical board. The other rolls’ pictures are not used. No claim is made that their animations were watched; this is an approved narration pickup under the course board. The unchanged remainder is technically preserved, but has not received a fresh end-to-end listening/watch review here. Candidate remains pending that review and is not installed or marked ready to ship.

## Candidate status

Latest candidate: `Prompts/context-matters-v9.mp4` (3:51.6). V8 was superseded during QA because OpenCV rendered nominal four-pixel outlines as five pixels. V9 uses the exact-width Context Matters renderer. Its narration is identical to the encoded v8 audio, whose final transcription matches all 67 approved words. See `v9/qa.json` and `v9/ring-and-audio-check.json` for final measurements. Listening/watch review remains; no installation or publication.

## Local shipment

Owner authorized “ship it” after receiving v9 and its join preview. Installed exact v9 bytes at the canonical path and committed as `9e2d08372eb51712a80b3a82e481e9b440c7c376`. Local browser and migration-hash asset checks passed; six splice boundaries passed transition guard. Queued for batch deployment; no push or deployment performed. Assistant listening status is unchanged and is not represented as completed. Previous installed source is preserved in the parent Git commit.

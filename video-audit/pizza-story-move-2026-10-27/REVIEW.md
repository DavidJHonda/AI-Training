# Pizza story move — 2026-10-27

Two narrow review candidates implement the owner's request to move the glue-on-pizza story from Hallucination to Does AI Think?. Current page sections, lesson Markdown and October 27 preparation notes establish the destination: after the Chinese Room and learned-pattern explanation, before the three comparisons. No new narration or artwork was generated.

| Candidate | Runtime | Result |
|---|---|---|
| `Prompts/hallucination-v20.mp4` | 3:21.767; 6,053 frames | Removes the story and later pizza application; retains the real-source qualification, checking method, Stanford application and original close. |
| `Prompts/does-ai-think-v15.mp4` | 3:20.333; 6,010 frames | Inserts the story and source-interpretation landing at 1:38.267–2:11.000; retains the original comparisons and close. |

## Source identities and exact edit

Sources are the byte-verified installed Hallucination v19 and Does AI Think? v14. Their paths and SHA-256 hashes, half-open source/output frame ranges, quiet-edge measurements and candidate hashes are in each `edit-manifest.json`. Finished MP4s preserve the previously approved visual edits; each retained span receives one additional encode at H.264 CRF 16. This build does not reconstruct the historical raw-roll assemblies.

Hallucination source cuts:

- 2:04.400–2:43.467: pizza story, diagram and source-interpretation conclusion. The preceding “But AI can also fail by misreading a real source” remains. The next sentence is “This three-step graphic shows how to investigate AI claims.”
- 3:50.233–4:10.700: “Now, we apply the framework to the pizza scenario” through “It must support the claim being made.” The Stanford caveat now leads to the original standard close.

Does AI Think? receives these Hallucination source spans:

- 2:04.400–2:33.267: “When searchers asked Google…” through “The Reddit comment was real. The cooking advice was not.”
- 2:35.900–2:39.767: “The source existed, but the AI interpreted it incorrectly.”

The intervening “This is a different type of error than the fake study” is omitted because the destination lesson has no Stanford study. The next “A real source does not automatically yield a true claim” sentence is also omitted, following the current Does AI Think? landing. Its old 1:38.267–1:46.400 bridge (“Knowing how this predictive mechanism operates…” through “…internal comprehension”) is replaced by the story, consistent with the retired fluent-answer sentence in the October 27 source update.

## Visual and audio treatment

| Board | Highlight and camera | On screen / breaks |
|---|---|---|
| Real Text. Wrong Meaning. | Existing canonical board, original full opening, image outline and takeaway outline; original camera timing. | 1:56.333–2:07.133 in Does AI Think?. Existing pizza/glue and Reddit-joke drawings precede it; the existing source-interpretation animation follows it. |
| Check the Claim | Existing full-board opening and later step walk. | Destination opening held 10 frames earlier inside the quiet lead-in to avoid carrying the old pizza diagram across the cut. |
| When You Think. What AI Does. | Existing full opening, comparison-row highlights, camera and cutaways. | Destination opening held 12 frames earlier inside the quiet lead-in to avoid the retired predictive-text drawing. |

At the start of the moved story, hold the first clean pizza drawing for 15 frames in the quiet lead-in. No other pictures are replaced. Remaining board treatments and both standard closing motions are inherited unchanged. The pizza board is visible for 10.8 seconds; Hallucination's inherited opening chat remains its longest board run at 27.8 seconds. Does AI Think?'s inherited Chinese Room board runs for 25.9 seconds before its existing reply-return cutaway.

All five audio joins fall in measured silence. Five-millisecond edge fades apply only inside those quiet handles. No silence is inserted and no speech is normalized or time-stretched.

## Verification and review limits

Both complete candidates decode at their planned frame counts with uniform 30 fps timestamps. Across 121 encoded frame samples, minimum PSNR against the mapped source pictures is 38.27 dB. Encoded audio agrees with the assembled source audio at 48.67 dB or better signal-to-error ratio, with no timing offset. All five encoded join windows are below −76 dBFS. Source files retain their pinned hashes.

All five new transition guards passed; every resulting boundary strip was visually inspected. The moved canonical pizza illustration was inspected at delivery resolution. No stale-frame island was found at a new join. The complete files were independently transcribed with cached `small.en`; transcripts are retained beside each manifest. Transcript review is separate from listening.

The complete encoded transcripts were read against the current lesson sequence. Hallucination has no pizza, glue or Reddit reference; its real-source qualification joins the checking-method introduction as intended. Does AI Think? contains the entire Google/Reddit story, real-comment/wrong-advice contrast, and interpretation landing, followed by all three comparisons. The orphan reference to the fake study and retired predictive-output bridge are absent. Both closing messages remain complete.

Subjective listening and continuous end-to-end audiovisual playback were not performed. In particular, automatic speech recognition and quiet joins cannot establish whether the narrator change feels natural. Review these output joins (eight-second context MP4s are saved beside each manifest):

- Does AI Think?: **1:38.267**, **2:07.133**, **2:11.000**.
- Hallucination: **2:04.400**, **3:11.167**.

This narrow edit does not constitute a new full production review or a whole-file KEEP verdict. Existing narration, diagrams and visual treatments outside the move are inherited. No course assets, page references, upload materials, external tracker entries, commits or deployment were changed. The candidates are ready for owner listening review, not reported as shipped.

Build: `scripts/video/build_pizza_story_move.py`. Encoded checks: `scripts/video/qa_pizza_story_move.py`. Both refuse to overwrite existing video outputs.

## Local release — 2026-10-27

Owner authorized “Ship both videos.” after disclosure of the listening limitation. Installed Does AI Think? v15 and Hallucination v20 at their canonical course paths. Both installed files and committed blobs match the reviewed candidates. Updated only the two video references/cache keys and the Hallucination runtime label to 3 min, plus the asset hashes and byte counts.

Local commit: `7da33bb6a4e5ff51225e05adf26ae04d7f191c23`. **Shipped locally; queued for batch deployment.** No push or deployment was performed. The other session's lesson-content/preparation edits remain uncommitted and were preserved.

The user's approval is authorization to ship, not evidence that subjective listening occurred. The earlier disclosure remains. Exact hashes and verification are in `shipping-receipt.json`. Build/QA source resolution now uses the retained, byte-identical v14/v19 candidates so future canonical replacements cannot invalidate donor frame references. Historical build manifests retain the original installed-source provenance.

Removed 161,130,240 bytes of this build's regenerable float-audio scratch. Candidates, original source versions, context clips, scripts, transcripts, manifests, QA results and transition images are retained.

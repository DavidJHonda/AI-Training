# Flattery & Engagement: existing-video merge

Scope: user-authorized review candidate from the current installed videos. Preserve all retained teaching, approved board treatments and supporting animations. No new generation, lesson change, installation, commit, or publication. Stable `Prompts/flattery-trap-v13.mp4` and `Prompts/engagement-trap-v15.mp4` match the installed files exactly; hashes are in the build manifest. Original raw rolls were unavailable for the shipped source edits.

## Narration assembly (source time)

| Source | Keep | Purpose |
|---|---|---|
| Flattery v13 | 0:00–4:15.367 | All Flattery teaching through “Ask AI to improve the work, not approve of you.” |
| Engagement v15 | 0:00–1:36.667 | “The engagement trap feels like a helpful conversation that keeps going”; slope example and infinite-scroll choice. |
| Engagement v15 | 2:05.467–2:29.000 | “AI chat interfaces utilize their own invisible version of the missing page break” through “The goal is to turn occasional product use into a daily habit.” |
| Flattery v13 | 4:17.800–4:20.300 | “Look for specifics, not approval.” |
| Engagement v15 | 3:49.200–3:58.267 | “Know what you came for. When you have it, choose what happens next.” and existing final audio tail. |

Expected result: 11,614 frames at 30fps, **6:27.133**, versus 8:23.400 combined. Removed: separate Flattery closing, Raskin regret and lifetime estimate, autoplay/streak discussion, Meta settlement and stopping-points material, and the separate social-media conclusion.

The existing four-second Engagement opening is a spoken substitute for the new unrecorded transition. It provides the antecedent for “This extra help may be useful.” No fabricated speech or word-level reconstruction. This is the one intentional narration difference from the approved merged page's structure.

All cuts fall inside source quiet intervals measured from decoded audio, not Whisper word boundaries. The builder blends only 10ms of each quiet join, without changing the timeline. No new pauses or global level changes. Source active-speech RMS differs by approximately 0.56dB, so no level correction is planned. Voice/cadence continuity requires listening review.

## Board and supporting-picture plan

| Board | Highlights and camera | On-screen / breaks |
|---|---|---|
| Flattery vs. Useful Feedback | Preserve existing full introduction, complete-card framing and timed explanation rings | Preserve source 0:23–1:23. This approximately 60-second worked-example run is an existing approved treatment, retained for this merge rather than shortened or filled with new stills. |
| How the Praise Got Baked In | Preserve three card rings, compact full view | Existing training span, approximately 1:23–1:53; then sycophancy definition drawing. |
| Sycophancy | Current shortened board, one whole-response purple ring, full view | Source 2:13.333–2:23.900; gag-product drawing before, rollback drawing after. |
| Three Ways to Fight the Flattery Trap | Preserve complete-row camera and teal rings, instruction tip, full-view takeaway | Existing board runs up to 19.867s; retain neutral-input, checklist/standard, and rubric-alignment animations between them. |
| One Answer. Two Endings. | Preserve owner's approved question/answer and complete-outcome zoom/pans, existing rings | Source approximately 0:14.77–1:10.7; retains chat-follow-up animation and existing breaks. |
| What Infinite Scroll Removed | Preserve compact two-column rings and takeaway | Source approximately 1:18–1:36.667; Raskin/interface drawing before it, direct return to AI-chat animation after it. |
| Merged closing | Exact current canonical JPG, unmarked on white; 48-frame hold, 150-frame push to 1.2x, settled final hold | Output 6:15.567–6:27.133. Both old closing pictures replaced; complete current wording stays visible. |

Preserve the Engagement chat animation at source 2:05.533–2:15.700, then its engagement-metrics animation through 2:29.000. The audio starts two frames before the chat picture; hold its first frame across those two frames to prevent the preceding phone shot flashing. No new chapter card, board recreation, or decorative illustration.

## Verification and review limits

Inspect the actual encoded candidate: full frame/PTS decode, every retained picture against source at thumbnail resolution, closing frame, encoded audio against planned PCM, source/asset hashes, all declared boundary strips, and a new transcription. Extract review clips around both joins and the closing. No available tool provides perceptual audio listening; automated transcription and waveform checks do not establish voice/cadence quality. Do not label this candidate ready to ship without that review.

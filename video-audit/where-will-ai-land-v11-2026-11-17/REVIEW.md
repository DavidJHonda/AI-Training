# Where Will AI Land? — v11 production candidate

Built from uploaded `Prompts/where-will-ai-land-7.mp4`, not the older edited `-v7.mp4`. User approved the two proposed narration trims and visual cleanup. Paraphrases remain acceptable when they preserve the teaching point.

Candidate: `Prompts/where-will-ai-land-v11.mp4`. Target: 7,829 frames, 30 fps, 1280×720, 260.966667 seconds (4:21).

## Scope

- All narration comes from raw -7. No synthetic narration, donor audio, inserted silence, or level changes.
- Keep the Hanoi bounty story, one-tail assumption, tailless-rat reveal, breeding/repeated-income explanation, rat farms, cancellation, and pile of tails.
- Keep all four examples: Text Messaging, GPS, Cane Toads, Wider Highways. Keep the AI comparison after them, the possibility of unimagined applications/complications, and the curiosity close.
- No lesson, preparation bundle, installed video, shared index, asset manifest, or unrelated working changes modified. This task builds a review candidate; it does not install or publish it.

## Approved narration trims

| Source interval | Removed narration | Output join |
|---|---|---|
| 3:22.100–3:33.167 | “Biological ecosystems and concrete highways are intricate networks. Pulling a single lever to fix a localized issue usually triggers compounding reactions across the entire system.” | 3:22.100 |
| 4:01.400–4:06.500 | “If history is any guide, the actual path of reality will diverge entirely.” | 3:50.333 |

The first join connects “Adding more lanes simply encouraged more people to drive” to “Whether it’s pest control, telecommunications, or traffic management…”. The second connects the Optimists/Worriers forecast comparison to “No researcher, tech CEO, or government regulator knows exactly where this technology is going to land.”

Cuts use quiet source intervals between complete sentences. The exact PCM source samples are concatenated; visual scene boundaries do not alter audio. The optional GPS ranking-sentence trim in the earlier detailed evaluation was not part of the approved two-trim recommendation and is not applied.

The source spinner begins at 4:37.133 and is omitted. The final spoken line remains intact with its source tail before that boundary.

## Visual treatment

- Opening stock photograph replaced by raw -9’s drawn rats/sewer sequence. Its narration is not used.
- Invented colonial charter replaced by raw -9’s generic plan illustration, aligned to its exact scene boundaries (frames 374–507).
- Pile-of-tails scene retained with a 1.45× native camera crop. This emphasizes the tails and excludes the generated desk nameplate.
- Current canonical `where-will-ai-land-plans.jpg` replaces the recreated board and stock toad/highway photographs. It also replaces the misleading banking/GPU image during GPS timing narration.
- Full board appears unmarked for 8.87 seconds before the Text Messaging dive. Complete-card framing retains each illustration, original purpose, and unexpected result. One outline follows the spoken point; the incoming card does not inherit the previous card’s highlight.
- Ring parameter: fixed 4 output pixels at 720p, independent of camera zoom, using the shared renderer. Purple SMS, blue GPS, teal cane toads, amber highways.
- Useful Notebook illustrations remain between board views: phone/conversation drawings, satellites/navigation/deliveries, cane/beetles, Australia map, highway construction/lane animation, comparison collage, AI forecasts and laboratory scenes. Longest continuous canonical-board span: 19.1 seconds.
- Fake historical-entry notebook replaced by the crumpled-plan illustration. No fabricated historical records remain in that shot.
- Engine corner marks removed from retained Notebook frames; canonical graphics have no such marks.
- Current canonical close replaces the recreated close: 48-frame hold, 150-frame eased push to 1.2×, 123-frame settle. The canonical close is the literal final frame.

## Verification

Encoded v11 decoded to exactly 7,829 frames at 30 fps. Full encoded-audio ASR confirms both approved passages are absent and the retained teaching sequence is intact. Audio correlation with the approved PCM edit is 0.9999843; peak is −1.56 dBFS with zero clipped samples. The joins sit within 0.821- and 0.891-second quiet intervals. All 23 every-frame transition strips were inspected. The detector’s only flag is the native SMS-diagram fade at frames 3599/3600, not stale footage. The second narration join visibly skips part of the forecast-line animation; this is repaired in v12. Canonical ring measurements are 4–5 solid pixels under the shared 4-pixel drawing parameter; unrelated gold artwork causes the larger automatic detections. Source and canonical-asset hashes are unchanged.

## Limits

No direct auditory review or continuous motion-with-narration review was performed. Transcripts, waveform measurements, frame counts, and sampled/transition frames do not certify cadence, pronunciation, or the subjective sound of the joins. Audition output 3:22.100 and 3:50.333 before treating this as shipping-certified. Context clips are `join-1.wav` and `join-2.wav`.

The underlying raw -7 wording discussed in the comparison review remains, except for the two authorized trims. This build is not a new fact-check or a claim that every added generalization is ideal.

Build recipe: `scripts/video/build_where_will_ai_land_v11.py`. Exact source/output frame ranges, board states, asset hashes, and replacement provenance are in `edit-manifest.json`.

Superseded by v12 during QA: second narration join skipped part of the animated forecast line. v12 cuts directly to the following roundtable illustration at that join.

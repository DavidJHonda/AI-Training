# Where Will AI Land? — v12 production candidate

Built from uploaded `Prompts/where-will-ai-land-7.mp4`, not the older edited `-v7.mp4`. User approved the two proposed narration trims and visual cleanup. Paraphrases remain acceptable when they preserve the teaching point.

Candidate: `Prompts/where-will-ai-land-v12.mp4`. Target: 7,829 frames, 30 fps, 1280×720, 260.966667 seconds (4:21).

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
- Second narration join cuts directly to the roundtable illustration. This avoids skipping forward inside the animated forecast line; source narration remains unchanged.
- Fake historical-entry notebook replaced by the crumpled-plan illustration. No fabricated historical records remain in that shot.
- Engine corner marks removed from retained Notebook frames; canonical graphics have no such marks.
- Current canonical close replaces the recreated close: 48-frame hold, 150-frame eased push to 1.2×, 123-frame settle. The canonical close is the literal final frame.

## Verification

Encoded candidate checks completed:

- Exactly 7,829 decoded frames at 30 fps; uniform frame timing; runtime 260.966667 seconds.
- Audio matches the approved PCM edit with correlation 0.9999843. Peak −1.56 dBFS; zero clipped samples. The retained pauses around the edits measure 0.821 and 0.891 seconds. No silence was inserted.
- Decoded audio is byte-identical to v11’s verified audio. Its full encoded-audio ASR transcript therefore applies to v12; provenance and hash are saved in `transcript-provenance.json`. Both removed passages are absent, and the story, four examples, AI uncertainty point, and curiosity close remain intact. ASR spelling errors are not treated as proof of mispronunciation.
- All 24 edited boundaries reviewed: 22 every-frame strips are byte-identical to the previously inspected v11 strips; both changed/new strips were inspected directly. The animated chart now cuts cleanly to the roundtable illustration at the second audio join, then to the tablet. No stale intermediate shot was found.
- The automated transition detector retains one false-positive flag for the native SMS-diagram fade at frames 3599/3600. Every-frame inspection shows a continuous fade/scale animation, not inserted stale footage. The automatic report is preserved with a separate manual resolution.
- Full-timeline overview samples inspected. Canonical board and final close inspected at delivery resolution. All 11 selected encoded board/close state images are byte-identical to v11. Its ring measurement report remains applicable: canonical outlines measure 4–5 solid pixels using the shared nominal 4-pixel renderer, with no zoom-dependent thickening. Larger gold detections are illustration details, not added highlight rings.
- Original source files and canonical board/close hashes are unchanged. No source or installed course asset was overwritten.

Candidate is ready for review. Direct listening and continuous playback with narration remain unperformed; see limits below.

## Limits

No direct auditory review or continuous motion-with-narration review was performed. Transcripts, waveform measurements, frame counts, and sampled/transition frames do not certify cadence, pronunciation, or the subjective sound of the joins. Audition output 3:22.100 and 3:50.333 before treating this as shipping-certified. Context clips are `join-1.wav` and `join-2.wav`.

Build recipe: `scripts/video/build_where_will_ai_land_v12.py`. Exact source/output frame ranges, board states, asset hashes, and replacement provenance are in `edit-manifest.json`.

Output SHA-256: `1e0f943aa95d176e35c693b01e89c80d0c2221ff757507c04d096c940c09bff3`.

# Layers — proposed repair, September 28

Recommendation: REPAIR the existing 3:14.700 video. Keep its teaching sequence and explanations. A full sentence reread would improve the IT/CAT example. This is a plan, not build or publication authorization.

Current canonical source: `course-assets/layers/layers.mp4?v=20260923ship1`. SHA-256 `22c403f13e4dcab98aedaf475b91ae6f5af60d1bbb910b8250bcddb2dcdecde5`, 5,841 frames at 30 fps. Fresh sequential decode and canonical board hashes match the retained build-v3 manifest. Reviewed current LayersSection in index.html, current lesson Markdown, prompt, shared video spec and narration rules, full timestamped transcript, canonical boards, retained scene sheet, and fresh full-resolution source frames.

## Teaching

The horse hook and three reads are RICH. The AI-versus-human distinction, layers, attention/transformation, neural-network definition, many-number rows with two displayed values, first/final number pairs, five IT/CAT stages, qualified layer-count scale, benefit/cost tradeoff, and closing lines are TAUGHT. Preserve the established analogy and example values; no new mechanism explanation, illustrative-number disclaimer, lesson rewrite, or unused Why Dozens board is proposed. The AI Brain Break is a separate activity.

The existing IT/CAT walkthrough explains the relationship but never reads the complete sentence. Recommend a full sentence before Start, giving students the context aloud as well as on screen. This is a clarity improvement, not grounds for rerolling otherwise useful narration.

Identified existing donor: `course-assets/vector-space/vector-space.mp4`, approximately **3:21.36–3:25.04**: “The cat sat on the mat during the May rainstorm because it was tired.” Fresh ASR of that actual file confirms the complete sentence; source hash recorded in donor-source.json. Insert after the current “Now let's follow a single word, it, to see how its numbers change in a real sentence” and before “At the start…” around **1:47–1:48**. Keep the existing sentence illustration during the bridge, then show the complete canonical board for the reread, highlight its sentence strip, and move to Start afterward. Approximately four seconds added; final edits require waveform boundaries and voice/level/cadence comparison. Cross-lesson donor voice compatibility and joins are NOT auditioned or certified. If the donor does not fit, report that limitation; do not assemble a new voice word by word or reroll automatically.

## Proposed visual edits

All timestamps below refer to the current source, before the potential reread shifts later timing. Keep original drawings and animation, including the final pronoun/nuance/tradeoff sequence.

| Board / beat | Current continuous exposure | Proposed treatment | Planned break / remaining continuous time |
| --- | --- | --- | --- |
| “The Horse Raced Past the Barn Fell” | 0:05.167–0:45.300; 40.133 s | Full view for sentence and setup, then modest complete-column zooms: First Read ~0:10.08, More Reads ~0:18–0:19.5, Meaning Clicks ~0:29.52. Whole-column outlines include text and illustration; smooth pans; full view for takeaway ~0:42.54. Preview modest zoom to retain entire active column. | No independent horse/barn donor found. Keep the worked example intact; 40.133 s remains one continuous board exposure despite camera motion. Deliberate exception, not filler. |
| How Layers Update the Numbers | 1:04.100–1:42.633; 38.533 s | Compact full view; diagram → Starting Numbers at ~1:21.94 → Final Numbers at ~1:31–1:32 → takeaway ~1:38.56. Keep only the first and final values spoken. Remove near-immediate broad outline: allow the board opening to establish before highlighting. | Reuse the existing line-of-layers drawing from current 0:47.70–1:04.10 around **1:15.30–1:20.30**, returning before “two to track the change” ends and before the starting values. Residual board runs ~11.20 s and 22.33 s. This is an editorial target; verify the entire selected donor picture span during build. |
| How AI Connects ‘IT’ to ‘CAT’ | 1:48.100–2:28.367; 40.267 s | Keep full five-stage progression visible; no dives. Sentence strip only during proposed reading, then one complete stage outline at each spoken onset: Start, Layer 1 ~1:57.14, Layer 2 ~2:02.98, Repeat ~2:10.38, Result ~2:20.06. Remove current simultaneous sentence-strip and Start rings. | Reuse the line-of-layers drawing under **2:10.38–2:18.54**, after a brief Repeat indication if useful; return before Result. Base residual runs ~22.28 s / 9.83 s; full reread adds ~4 s to first run, making it ~26.3 s. No extra silence for the highlight. |
| Depth and tradeoff illustrations | 2:28.367–3:04.000 | KEEP all current animation and qualified scale wording. | Existing non-board break. |
| Canonical close | 3:04.000–3:14.700; 10.700 s | KEEP literal final frame and motion. | Retain closing gap. |

The network drawing is an existing same-lesson picture, inspected freshly at 1:01, with no invented numerical labels. Reuse it only under the general passage-through-layers explanation; the actual number pairs and result must be visible on their own board. Do not substitute the drawing where a student needs a specific value.

Normalize generated outlines to **4 px at 720p**, drawn after camera transforms. Actual sampled published rings are roughly 4–6 px, with the IT/CAT rings visibly heavier. Older widths alone do not justify a reroll. All three canonical board assets match the live lesson. Preserve their wording and artwork.

No added pauses proposed. Keep existing timing except the optional full sentence; expected runtime about 3:19 if that graft works. Measure actual final board durations including all zooms, pans, and holds. Longest planned exposure remains the 40.133-second horse example, openly retained because no suitable independent drawing survives.

## Verification and limitations

Fresh exact source identity, 5,841-frame decode, and board hashes passed. Retained September 27 transition guard passed 16/16 declared boundaries on this exact hash; its every-frame strips were not manually rereviewed for this plan. A repaired candidate needs fresh boundary, source-mapping, framing, ring-width, audio-integrity, and actual-duration checks.

No real-time end-to-end watching/listening, perceptual audio audition, pronunciation check (including the historic I-T issue), donor voice match, phone readability, or public-player playback was performed. ASR supports words and timings only. No original Layers rolls survive in Prompts or video-audit; narration repairs use surviving published files. Existing rendered stills from old rolls do not establish recoverable donor audio or motion. No new published-site byte fetch or Video Tracker access was performed; prior public-byte review is historical evidence, and the current check is of the local canonical published file.

No lesson, board, prompt, MP4, tracker, or publication change made. Only review artifacts and an analysis excerpt were created.

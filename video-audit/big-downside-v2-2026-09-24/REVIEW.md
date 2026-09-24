# Big Downside v2: review candidate (2026-09-24)

Scope: full production pass on `Prompts/big-downside-3.mp4`, with the best-of grafts from rolls 4 and 1. David approved this on 2026-09-24 ("Build it please"). The plan is in `video-audit/big-downside-review-2026-09-24/REVIEW.md`. Board treatment follows the 1b plan in the 2026-09-23 review.
Build: `scripts/video/build_big_downside_v2.py`. Output: `Prompts/big-downside-v2.mp4`, 10149 frames, 5:38.3.
The live video, the lesson, the boards and index.html are unchanged; their hashes were checked after the render.

## Narration (output times)
| Output | Source | Words |
|---|---|---|
| 0:24.67 | roll 1 46.68-54.90 (G3) | "While researchers can trace some internal features, they still cannot fully explain why a model produces one specific answer over another." |
| 0:43.90 | roll 3 cut 35.68-38.33 (G3a) | "Because we cannot trace those internal pathways," removed; the next sentence opens "Fixing an AI is much harder…" |
| 1:06.17 | roll 1 84.87-94.10 (G2) | "These include training the model to be helpful, monitoring the prompts users write, and limiting what the product can do. But no layer catches everything." |
| 1:38.77-2:21.00 | roll 4 102.42-146.95 (G1) | Third idea, "This is called jailbreaking.", the two sign lines word for word, cat-and-mouse, Policy Puppetry with HiddenLayer and the three models. "As highlighted here," (joins at 1:56.93) and "As shown," (2:13.77) trimmed. |
| 3:16.73 | roll 1 240.30-244.70 (G6) | "If you give an AI a goal, it may find a route you never intended." (replaces "career objective") |
| 5:01.27 | roll 1 330.33-339.22 (G5) | "In 2026, over a thousand employees at major AI companies, including the CEO of Anthropic, signed a statement called Pacing the Frontier." |
| 5:10.17 | roll 4 313.40-319.75 (G4) | "They asked the U.S. government to establish an international mechanism to slow automated AI development." |

Donor audio carries +0.9 dB. That's the integrated-loudness difference: rolls 1 and 4 measure -17.2 LUFS, roll 3 measures -16.3. No pauses were added. The gap at each of the 14 joins, measured in the output, is 0.22-0.51 s. A base.en transcript of the output reads the whole lesson through with no clipped or doubled words.

All 13 required lines are now met word for word, apart from roll 3's "breaking boundaries" (missing "the"). All six ideas are numbered.

## Pictures (output times)
| Output | Content |
|---|---|
| 0:24.7-0:33.0 | Roll 1's isolated-feature network under G3 |
| 1:06.2-1:15.4 | Roll 1's Layered Defense rings under G2, then roll 3's unused guardrail-pipeline frames under "This chart shows…" |
| 1:17.8-1:38.8 | The Guardrail Challenge Gets Harder (canonical): three card rings, then the banner. 21.0 s, unbroken |
| 1:38.8-1:51.9 | Roll 4's III/padlock card and safety-monitor diagram |
| 1:51.9-2:02.4 | Why Jailbreaks Keep Appearing (canonical; the illustrated page board, not the faceless upload). Full view, banner ring at "New methods keep surfacing" |
| 2:02.4-2:21.0 | A Jailbreak (canonical): the whole card at "In 2025…", then the quote block |
| 2:41.7-3:05.5 | How the Voice-Clone Scam Works (canonical): full-height column rings. 23.8 s, unbroken |
| 3:21.4-3:28.8 | Roll 4's TEST SANDBOX / JULY 2026 CASE STUDY drawing under the setup sentence |
| 3:28.8-4:01.1 | A Test Became a Real Cyberattack (canonical). Broken at 3:40.1-3:44.7 by roll 1's "1,200 AI Agents Active" sandbox drawing, under "About 1,200 of them…" |
| 4:11.3-4:17.8 | Covers roll 3's 1908 car PHOTOGRAPH with roll 1's AI SAFETY vs CAPABILITY FRONTIER drawing |
| 4:17.8-4:38.2 | Technology First. Safety Later. (canonical): four row rings; the AI row is ringed on "still evolving" |
| 5:01.3-5:10.2 | Roll 1's signed-statement drawing under G5 |
| 5:27.9- | Canonical close; Notebook's close card and outro removed |

Longest board run: 23.8 s (voice clone), then 21.0 s (guardrails). Both are just over the ~20 s rule. No roll drew anything for those steps that doesn't just restate the board, so they run unbroken.

## Checks
- Decoded frames match the plan (10149).
- transition_guard: 30/30 boundaries pass. Contact sheets were inspected (`big-downside-v2/sheets/`); the per-boundary strips were not inspected one by one.
- Corner mark: 4530 frames cloned, 862 inpainted, 0 declined.
- Board rings checked on the state sheets (`build/states-*.jpg`): right card, whole card inside the ring, nothing clipped.

## Kept, David's call
- 3:05.5-3:09.7 hooded figure at monitors (drawn, faceless)
- 4:50-4:59 drawn silhouettes at server racks (red teams); 4:59-5:01 drawn man, head in hands
- 4:38-4:50 "AI OUTPACES REGULATION SPEED" chart (unlabeled 0-160 axis, no claimed figure)
- 3:16.7-3:21.4 the goal diagram under G6 starts partway into roll 3's animation (the picture is aligned so it runs straight into the next shot)

## Not auditioned
Nobody has listened yet. The joins to listen to: 0:24.7, 0:32.9, 0:43.9 ("Fixing an AI…" opening mid-prosody), 1:06.2, 1:15.4, 1:38.8, 1:56.9, 2:13.8, 2:21.0, 3:16.7, 3:21.1, 5:01.3, 5:10.2, 5:16.5, and the close at 5:27.9. Also listen for voice continuity across the three generations, above all through G1 (42 s of roll 4).

## v3 repair (2026-09-24, David: "At 5:10, there's a flash of an old graphic")
Narrow repair. v2 flashed 6 frames (5:10.17-5:10.33) of roll 3's own "Pacing the Frontier" slide under the start of G4. G4's picture started at roll 3 294.78, six frames before roll 3's cut (294.98) to its U.S. Government diagram. v3 starts the picture at 294.98. The diagram's last frame now holds 6 frames longer before "Their warning was explicit."
Output: `Prompts/big-downside-v3.mp4` (build record `build-v3/`), 10149 frames, audio unchanged. Compared frame by frame with v2, it differs only inside 5:10.17-5:12.0 (frames 9305-9360). The only cut left there is the join itself.
Why the guard missed it: the second cut was a soft fade (frame difference 9.1, under the guard's default threshold of 12). v3 passes transition_guard 30/30 at `--cut-threshold 8`. I also rescanned every join in v2 at a threshold of 4: the only other hit, 4:01.1, is the audit-log drawing fading in, not a stale frame.

## Shipped 2026-09-24 (David: "ship it")
`Prompts/big-downside-v3.mp4` installed as `course-assets/big-downside/big-downside.mp4` (sha256 83ecf2e1…, matching build-v3/edit-manifest.json; 338.3 s). Page entry: cache key `20260924ship1`, pill 6 min. The joins listed above were not auditioned by the editor; David approved shipping.

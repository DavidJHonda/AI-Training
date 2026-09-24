# Big Upside v4: review candidate (2026-09-24)

Scope: full production pass on `Prompts/big-upside-6.mp4` (third materials revision), on David's "yes" to the
repair plan in `video-audit/big-upside-review-2026-09-24c/REVIEW.md`, including the optional "breakthrough" cut.
Build: `scripts/video/build_big_upside_v4.py`. Output: `Prompts/big-upside-v4.mp4`, 7719 frames at 30 fps, 4:17.3,
sha256 `75f222783851b0028746bcb4fcf0609b79f26341ffbc8677e1329f68fcb36393`. The live video, lesson, boards,
rolls and index.html are unchanged (hashes verified by the render). Not shipped.

## Narration (output times)

| Output join | Removed from roll 6 | Gap |
|---|---|---|
| 0:34.3 | "We can see its impact on this board, laying out a completely new scale for science. The contrast shows exactly what happened." | 0.62 s |
| 0:39.9 | "Now look at the right side." | 0.82 s |
| 1:02.3 | "His path to a scientific breakthrough actually started with two things you might recognize, chess and video games. This timeline charts his career." | 0.63 s |
| 1:41.6 | "Earning a Nobel Prize, specifically for protein structure prediction ... We see that same dynamic across other medical fields." | 0.50 s |
| 3:29.9 | The pause-the-video passage through "Whatever examples you thought of from our list," | 0.56 s |
| 3:31.6-3:38.4 | "So the next time someone asks you that question, you have a definitive answer ready." replaced by **roll 3's** "So the next time someone asks you, what good does AI do for society? You have an answer ready." (no gain; speech level -16.8 dBFS vs -16.9 after) | 0.52 s in, 0.90 s out |

All 19 verbatim lines remain. A medium.en transcript across every join reads cleanly.

## Pictures (output times)

| Output | Content |
|---|---|
| 0:00-0:30.9 | Notebook: calculator, fifty-year challenge, molecular machines, grid |
| 0:30.9-0:45.9 | **A New Scale for Science** (canonical, compact): Experiments ring, then AlphaFold ring |
| 0:45.9-0:58.5 | Notebook: map, 200,000,000 structures dots, knight card |
| 0:58.5-1:41.6 | **Demis Hassabis timeline** (canonical, compact): arrives at "To answer that, we look to the co-founder of DeepMind"; rows ringed as spoken, banner at "A kid who loved games", then the 2024 Nobel row. Broken 1:21.3-1:25.7 by roll 3's AlphaFold DB drawing (researcher and country counters count up) under "More than 3 million people across over 190 countries" |
| 1:41.6-2:36.9 | **Helping People Stay Healthy** (canonical, compact): card rings as each is named, banner ring |
| 2:36.9-3:29.9 | **Helping People in Everyday Life** (canonical, compact): card rings, banner ring |
| 3:29.9-3:31.6 | Notebook: Documented AI Milestones cards |
| 3:31.6-3:38.7 | Roll 6's "What good does AI do for society?" drawing (from the cut passage) under the grafted question; covers a drawn two-person scene |
| 3:38.7-3:43.8 | Notebook: REAL WORLD IMPACT card |
| 3:43.8-3:54.6 | Covers the Hassabis portrait and a young-man photograph: roll 3's STRATEGIC PLAY chess/simulation cards |
| 3:54.6-3:58.4 | Covers a drawn face: roll 4's attitude/purpose card |
| 3:58.4-4:02.4 | Covers drawn gardeners: roll 4's YOUR UNIQUE SKILLS -> HELPING PEOPLE card |
| 4:02.4-4:06.2 | Covers the Nobel medal photograph: roll 4's drawn Nobel medal card |
| 4:06.2- | Canonical close (standard motion) |

Board runs: protein 15.0 s; timeline 22.8 + 15.9 s; health 55.3 s; everyday 53.0 s. The two example boards are
over the twenty-second guideline. No roll drew anything for the individual cards (every roll showed its own board
render there), and the tall cards gain almost nothing from a dive, so they hold at full view with a ring per card.

## Checks

- Decoded frames 7719, matching the plan. No black interval. The final frame is the canonical close.
- transition_guard: 20/20 boundaries pass.
- Corner mark: 2220 cloned, 307 inpainted, 0 declined.
- Board rings checked on `build/states-*.jpg`. A full-output contact sheet shows no photograph or person.

## Kept, David's call

- Card-naming screen pointers: "Starting on the left with finding cancer.", "Next is the urgent scans column.",
  "Finally, we look at new antibiotics.", "This board outlines...", "This board shows examples...", "Look at the
  reading aloud section.", "In the middle column, we have flood warnings.", "On the far right is targeted spraying."
  They carry the card names and land on each ring.
- "As the banner at the bottom summarizes," (2:25) and "As the board states," (3:25), with no clean pause before
  the banner lines.
- "Every one of those is true." follows "the upside is already reaching people." after a cut (3:29.9); listen for cadence.

## Not auditioned

Nobody has listened. Please check: every join above; the graft at 3:31.6-3:38.4 (voice match with roll 3);
"Hassabis" at 0:58-1:03 (medium.en hears "Hassavis"); "abaucin" at about 2:22 (heard as "abosin").

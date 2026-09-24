# Big Upside v2: review candidate (2026-09-24)

Scope: full production pass on `Prompts/big-upside-1.mp4`, built on David's "Build it" (2026-09-24)
approving the best-of plan in `video-audit/big-upside-review-2026-09-24/REVIEW.md`: five cuts, one graft,
canonical boards, photographs covered, standard close. No pauses added.
Build: `scripts/video/build_big_upside_v2.py`. Output: `Prompts/big-upside-v2.mp4`, 8886 frames at 30 fps,
4:56.2, sha256 `56009641fbfb31f57ec4288e82631b87a2b601db30bc3fae67d50e6f2b508b0c`.
The live video, lesson, boards, both rolls and index.html are unchanged (hashes verified by the render).
Not shipped; not ready to ship until David has listened (see below).

## Narration

All output times are in the candidate.

| Output | Change | Joined gap |
|---|---|---|
| 0:33.0 | Cut source 0:33.00-0:45.60: "Because a protein cannot function ... instruction manual for human biology. This board illustrates the possible shapes." | 0.52 s |
| 0:53.8 | Cut 1:06.40-1:08.10: "Look at the function box." | 0.44 s |
| 1:05.4 | Cut 1:19.70-1:21.63: "Look at the bottom comparison." | 0.62 s |
| 2:39.5 | Cut 2:55.70-2:58.43: "The banner at the bottom summarizes it perfectly." | 0.58 s |
| 3:03.8-3:12.9 | Cut 3:22.80-3:48.63 (roll 1's paraphrased quotation, the "open-source foundation" sentence and "To understand how it does this..."). **Graft**: roll 2 3:05.30-3:14.40, "As Hassabis said, I've dedicated my career to advancing AI because of its unparalleled potential to improve the lives of billions of people." +2.7 dB | 0.42 s in, 0.33 s out |

Gaps measured on the edited audio at -45 dBFS; every join sits inside silence. Speech level around the
graft: -14.4 / -15.3 / -15.5 dBFS (before / graft / after). The graft peaks at -0.28 dBFS with no clipped
samples; the full-scale peaks elsewhere are in roll 1's own audio.

A fresh transcript of the output (`bundle/big-upside-v2/transcript.txt`) reads cleanly across every join
and still carries all eight verbatim lines.

## Pictures (output times)

| Output | Content |
|---|---|
| 0:00-0:33.0 | Notebook: calculator, cell strips, protein jobs, bead chain, key and lock |
| 0:33.0-1:34.6 | **Possible Shapes** (canonical protein board, dense): full view for about 1 s, then a ring and a dive to each complete component as spoken: Same string, Almost endless, One shape, Function, Atoms vs shapes, Protein Facts. Breaks: 0:40.4-0:44.5 live video's scattered folded proteins ("more shapes than atoms"); 0:58.1-1:04.4 live misfolded protein, then a star with a puzzle piece, then the piece fitted (the disease and drug lines); 1:21.0-1:26.3 live bead chain folding ("the sequence determines the folding") |
| 1:34.6-1:48.4 | Notebook: sequence wall, torn-paper fold |
| 1:48.4-1:58.5 | Covers Notebook's state-space card (garbled "~3^N", "~10^80") with roll 1's folded-protein-on-a-book drawing, freed by cut 1 |
| 1:58.5-2:44.1 | **Demis Hassabis timeline** (canonical, compact, still): rows ringed at each year; banner ringed at "A kid who loved games". Breaks: 2:19.7-2:21.8 live server-hall drawing ("founds DeepMind, building an AI lab"); 2:24.8-2:28.6 live blueprint protein ("AlphaFold solves protein folding") |
| 2:44.1-2:53.5 | Notebook: AlphaFold vs lab curves |
| 2:53.5-2:59.5 | Covers the Google DeepMind office photograph (logo) with the live video's UNRESTRICTED ACCESS drawing, under "They gave the answers away, free to everyone." |
| 2:59.5-3:03.8 | Notebook: world map (three million people, 190 countries) |
| 3:03.8-3:12.9 | Live video's world map under the grafted quotation (the Nobel ceremony and portrait photographs left with cut 5) |
| 3:12.9-3:16.0 | Notebook: AI: THE PATTERN ENGINE grid |
| 3:16.0-3:24.5 | Covers "Navigating massive search spaces" (invented "1,420 states", "~1 sample/day", "Configurations ≈ 10^80") with the live video's web of search paths; its last frame holds about 2 s |
| 3:24.5-3:35.6 | Notebook: general-purpose AI engine |
| 3:35.6-3:58.3 | **AI Searches Possibilities Humans Cannot** (canonical, compact): card rings, then the banner |
| 3:58.3-4:15.9 | **AI Turns Patterns into Practical Help** (canonical, compact): card rings, then the banner |
| 4:15.9-4:22.2 | Notebook: head silhouette and question mark |
| 4:22.2-4:28.6 | Notebook: FORCE MULTIPLIER card, frozen at 4:26.4 before the invented "Protein Folding 100x Speed" box draws in |
| 4:28.6-4:40.0 | Notebook: chess knight and controller; held still from 4:34.4 to cover the Hassabis portrait photograph |
| 4:40.0-4:46.5 | Notebook: sunburst; held still from 4:43.0 to cover the Nobel medal photograph |
| 4:46.5-4:56.2 | Canonical close (standard motion). Notebook's close card and black tail removed |

Board runs: protein 7.4 / 13.6 / 16.6 / 8.3 s; timeline 21.1 / 3.0 / 15.5 s; discovery 22.6 s; practical 17.6 s.
Longest unbroken board run: 22.6 s (discovery, no Notebook drawing fits inside it).

All donor drawings come from the live video (sketch style, same as roll 1). Roll 2's pastel 3D renders were
not used. The donor frame numbers bind to the current live file, so a rebuild must happen before the live
file is replaced.

## Checks

- Decoded frames: 8886, matching the plan. No black interval. The literal final frame is the canonical close.
- transition_guard: 31 of 34 boundaries pass. I inspected the three flags frame by frame and all are false
  positives: f1212 and f1334 are the live drawing's own zoom animation, and f1969 is the protein-board
  camera moving to the atoms strip. Strips in `transitions/`. I inspected ten more strips (the covers,
  the graft, the knight and sunburst holds, the close) and they are clean.
- Corner mark: 3010 frames cloned, 1811 inpainted, 0 declined.
- Board rings checked on the state sheets (`build/states-*.jpg`): right component, complete, nothing clipped.
- The first render opened the search-web cover on about 3 s of blank paper. I moved the donor start
  1.3 s later and re-rendered before anyone had viewed it; this record describes the second render.

## Kept, David's call

- 2:44.1-2:53.5 AlphaFold vs lab curves card reads "Structural Alignment: Congruent / Near-Atomic Parity with
  Experimental Data", slightly stronger than the narration's "close to lab methods".
- 3:15.6-3:16.0 the pattern-engine grid starts dissolving toward the invented-figures card for about 12
  frames before the cover cuts in: a faint, illegible ghost of "Manual Search".
- Narration residuals from the evaluation stand: the six cards are not named aloud; abaucin, the Swedish
  trial and solar panels are unspoken; "in a minute" (not "about a minute"); "This graphic shows..." (3:35)
  and "Now see how..." (3:58) remain.

## Not auditioned

Nobody has listened yet. David's ear is needed for:
- the graft at 3:03.8-3:12.9 (voice match across rolls, the name "Hassabis", level)
- the four cut joins: 0:33.0, 0:53.8, 1:05.4, 2:39.5
- "Hassabis" at 1:58.8 and 4:28.1 (the transcriber writes "Hissabis" and "Demisys Abbas")
- "describe seams/scenes" at 4:08.5
- the close

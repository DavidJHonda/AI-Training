# Embrace the Future video board-sync audit

Audit date: 2026-08-29. This is a review manifest. No shipped MP4 was modified.
The first non-destructive pilot is `videos/loudest-voices-v2.mp4`.

The section contains nine videos, 28 teaching boards, and nine standard closes. Board
hashes below identify the exact `lessons/` assets that must appear in the repaired or
rerolled videos. Time ranges describe the current shipped cuts; final visual-only edit
boundaries must snap to the source scene cuts and final highlight changes must snap to
word onsets.

## Executive result

- **Visual repair with source narration preserved:** Opener, Loudest Voices, Data
  Centers.
- **Reroll from the current Markdown, prompt, and exact board bundle:** Pace of Change,
  Big Downside, Big Upside, Rise of Agents, Work Changes, Unexpected Results.
- **Standard closes:** all nine currently contain the correct copy and consistent final
  treatment. Preserve them in visual repairs and require them unchanged in rerolls.
- **Automated pixel audit:** of the 26 page boards that the general audit could match to
  these videos, only the Embrace section map was strongly found (MAD 2.3). The other
  25 were weak matches or absent because the lesson boards were rebuilt after the
  videos shipped. The opener creed and data-center scene art are special non-index
  sources and were reviewed separately.
- **Source-bundle defect:** Big Downside has seven lesson assets, but its prompt says
  six and does not list the separate Policy Puppetry board. Correct the prompt and
  attachment order before rerolling it.

## Highlight color rule

Every state below inherits color from the active component. Editorial cards use their
stored locked accents: purple `#4f2fc4`, blue `#1652f0`, teal `#0e8f86`, green
`#0f7a4a`, amber `#a9760c`, or red `#c41f28`. Neutral board titles use standard video
purple `#6e51ff`. The opener creed is not an Editorial card board; its quote rings use
the creed's own gold accent. Summary states are unmarked unless the narration explicitly
combines cards.

## 1. Opener · `videos/opener-embrace.mp4`

**Action: visual repair; preserve source audio.** The section-map pixels already match
the current lesson. Rebuild its highlight walk and normalize the opening creed states.

| Board | SHA-256 prefix | Current span | Treatment and states |
|---|---:|---:|---|
| `lessons/opener-embrace-1-voices.jpg` | `a43984dfbd19` | 00:08.87–00:33.03 | Compact, full board. Gold rings move to “cure diseases” at 00:12.18, “take your job” at 00:16.64, “boring parts” with the optimistic pair, “hurt society” with the worry pair, then “nobody knows” at 00:27.52. No background wash. |
| `lessons/opener-embrace-2-map.jpg` | `c676013ea8a5` | 02:02.17–02:31.08 | Compact, full board. Begin unmarked; purple row rings at 02:02.10, 02:09.06, and 02:15.30. Return unmarked for the roadmap summary at 02:22.06. |
| `lessons/opener-embrace-3-close.jpg` | `05d23e44c06a` | 02:37.63–02:48.50 | Preserve standard close and source narration. |

## 2. Loudest Voices · `videos/loudest-voices.mp4`

**Action: visual repair; preserve source audio.** The spoken explanation still follows
the revised long board and the four historical calls. Both teaching boards are newer
than the video.

| Board | SHA-256 prefix | Current span | Treatment and states |
|---|---:|---:|---|
| `lessons/loudest-voices-1-three-voices.jpg` | `f9298c68d25e` | 00:47.03–02:56.40 | Dense. Establish the full board, then zoom and pan through each expert's background, Says, and But Admits regions: Dario Amodei purple at 00:47.00, Geoffrey Hinton blue at 01:22.86, Yann LeCun teal at 01:58.84. Pull back unmarked at 02:32.56 for the three admissions and the “bet” conclusion. |
| `lessons/loudest-voices-2-missed-calls.jpg` | `b32412830e72` | 03:01.67–04:17.10 | Dense 2×2 walk. Clifford Stoll purple at 03:04.78; Robert Metcalfe teal at 03:17.04; Steve Ballmer blue at 03:27.86; Henry Ford amber at 03:36.82. Pull back unmarked at 03:47.94 for the pattern. |
| `lessons/loudest-voices-3-close.jpg` | `9f1baf4e5146` | 04:17.10–04:33.10 | Preserve standard close and source narration. |

## 3. Pace of Change · `videos/pace-of-change.mp4`

**Action: reroll.** The current narration still makes claims the final lesson and prompt
deliberately calibrated, including stronger model-release language and an autonomous
self-improvement trajectory. A visual-only repair would preserve those contradictions.

| Board | SHA-256 prefix | Narration beat | Required state colors |
|---|---:|---|---|
| `lessons/pace-of-change-1-three-years.jpg` | `74c3acb70e58` | 2023 versus 2026 | Full board, then row rings in standard purple: Answering, Images, Context Window, Doing. |
| `lessons/pace-of-change-2-accelerants.jpg` | `a4aeec4d93a0` | Why So Fast? | Full board, then Better Training purple, More Compute blue, AI Helps Build AI teal. |
| `lessons/pace-of-change-3-future-research.jpg` | `1d0d5942ec82` | Could AI Improve Itself? | Full board, then Automated AI Research teal and Self-Improving AI purple. Preserve each card's pill/title color. |
| `lessons/pace-of-change-4-future-capability.jpg` | `fe82548b493f` | How Far Can AI Go? | Full board, then AGI blue and ASI red. Return unmarked for “Nobody knows.” |
| `lessons/pace-of-change-5-close.jpg` | `5253ad8cb6a0` | Close | Exact standard close; no highlight. |

## 4. Big Downside · `videos/big-downside.mp4`

**Action: reroll.** The present narration converts conditional future risks into facts,
overstates goal pursuit, and uses older wording that the final review explicitly
replaced. Update the prompt to list all seven sources before the reroll.

| Board | SHA-256 prefix | Narration beat | Required state colors |
|---|---:|---|---|
| `lessons/big-downside-1-worries.jpg` | `ae61e699939d` | Guardrail challenge | Full board, then If AI Changes Itself purple, If AI Matches People blue, If AI Surpasses People red. Keep the narration conditional. |
| `lessons/big-downside-2-jailbreak.jpg` | `0a58d71d7cd2` | Why jailbreaks keep appearing | Full-bleed teaching illustration. Use an amber ring only when naming the opening; otherwise restrained unmarked push. |
| `lessons/big-downside-2b-policy-puppetry.jpg` | `f2553229cc02` | Policy Puppetry example | Compact utility board. Neutral title uses standard purple; the evidence callout inherits the board purple. |
| `lessons/big-downside-3-voice-clone.jpg` | `03a05c1efe0a` | Voice-clone scam | Full board, then Voice Clip purple, Voice Cloned blue, Fake Call red, Call Back teal. |
| `lessons/big-downside-4-goal.jpg` | `5aee0724a6c0` | Controlled OpenAI test | Dense utility board. Establish the full board, then move a standard-purple ring between the setup and conclusion. |
| `lessons/big-downside-5-safety.jpg` | `e275018df264` | Technology First. Safety Later. | Full board, then Cars, Airplanes, Smartphones, and AI rows in spoken order. Use standard purple because this utility timeline does not store separate row accents. |
| `lessons/big-downside-6-close.jpg` | `e698b56b72dc` | Close | Exact standard close; no highlight. |

## 5. Big Upside · `videos/big-upside.mp4`

**Action: reroll.** The existing narration contains the pre-review protein/drug wording,
older AlphaFold usage language, and stronger causal claims than the final lesson allows.

| Board | SHA-256 prefix | Narration beat | Required state colors |
|---|---:|---|---|
| `lessons/big-upside-1-hassabis.jpg` | `ea649f3f90eb` | Hassabis timeline | Establish full board, then walk the seven timeline rows using their stored sequence: purple, blue, teal, green, purple, blue, teal. |
| `lessons/big-upside-2-discovery.jpg` | `5c1139a4e3dd` | Search possibilities | Full board, then New Antibiotics purple, New Materials blue, Cancer Screening teal. |
| `lessons/big-upside-3-help.jpg` | `a107d16249fd` | Practical help | Full board, then Faster Forecasts purple, Flood Warnings blue, Eyes and Ears teal. |
| `lessons/big-upside-4-close.jpg` | `53924441132c` | Close | Exact standard close; no highlight. |

## 6. Rise of Agents · `videos/rise-of-agents.mp4`

**Action: reroll.** The current narration uses the older comparisons, treats stopping as
automatic, and frames the incidents more broadly than the final lesson and prompt.

| Board | SHA-256 prefix | Narration beat | Required state colors |
|---|---:|---|---|
| `lessons/rise-of-agents-1-gps.jpg` | `df4aa68ad92c` | Chatbot versus agent analogy | Full board, then GPS/ChatGPT purple and Self-Driving/Agent blue. |
| `lessons/rise-of-agents-2-highlights.jpg` | `2f451df61829` | Basketball-highlight scenario | Dense long comparison. Begin on the scenario, then complete Ask a Chatbot card purple, complete Hire an Agent card blue, then full unmarked board for ownership. |
| `lessons/rise-of-agents-3-loop.jpg` | `4a2440dff867` | Agent loop | Full board, then Goal purple, Plan blue, Act teal, Check green. Return unmarked while explaining the loop. |
| `lessons/rise-of-agents-4-rogue.jpg` | `423f0702bdb5` | Rogue agents | Full board, then PocketOS purple and Gemini blue. The permission boundary is narration, not a new invented card. |
| `lessons/rise-of-agents-5-close.jpg` | `1fb6c77426ce` | Close | Exact standard close; no highlight. |

## 7. Work Changes · `videos/work-changes.mp4`

**Action: reroll.** The current video is 5:28, uses the earlier boards, and presents the
move toward meaningful work as assured. The final lesson deliberately says AI *can*
move work in that direction.

| Board | SHA-256 prefix | Narration beat | Required state colors |
|---|---:|---|---|
| `lessons/work-changes-1-strengths.jpg` | `3ba1ceb5c023` | Four Shapes of AI Work | Full board, then Transform purple, Generate blue, Compress teal, Reason amber. |
| `lessons/work-changes-2-assignment.jpg` | `dcc5f1d0dfae` | First assignment | Dense long comparison. Begin on the assignment, then complete Before AI card purple, complete With AI card blue, then full unmarked board. |
| `lessons/work-changes-3-concepts.jpg` | `104c75a247a7` | Automate versus augment | Full board, then Automate purple and Augment teal. |
| `lessons/work-changes-4-what-changes.jpg` | `db672e51b2d9` | What Changes for You | Full board, then More Kinds purple, More Productive blue, Meaningful Work teal. |
| `lessons/work-changes-5-close.jpg` | `ad84372ae801` | Close | Exact standard close; no highlight. |

## 8. Data Centers · `videos/data-centers.mp4`

**Action: visual repair; preserve source audio.** The narration remains usable and the
warehouse illustration is current. Replace the rebuilt footprint board and its walk.

| Board | SHA-256 prefix | Current span | Treatment and states |
|---|---:|---:|---|
| `lessons/data-centers-1-data-center.jpg` | `01da9239b6eb` | 00:26.20–00:52.93 | Current scene art. Restrained unmarked push; no arbitrary highlight. |
| `lessons/data-centers-2-footprint.jpg` | `9fa0e91f0d15` | 00:52.93–01:47.00 | Dense 2×2 walk. Establish full board; Electricity purple at 00:56.96, Water blue at 01:02.74, Noise teal at 01:11.22, Permanent Jobs amber at 01:16.04. Return to Electricity purple for the national electricity figures at 01:25.22, then full unmarked at 01:39.14. |
| `lessons/data-centers-3-close.jpg` | `26e32fd0d7d` | 02:20.40–02:27.97 | Preserve standard close and source narration. |

## 9. Unexpected Results · `videos/unexpected-results.mp4`

**Action: reroll.** The current video omits the Hanoi story that now establishes the
lesson's central mechanism. Replacing only the four-card board would leave the revised
learning arc incomplete. The current video also continues narrating after the required
two-line close.

| Board | SHA-256 prefix | Narration beat | Required state colors |
|---|---:|---|---|
| `lessons/unexpected-results-1-plans.jpg` | `eec79422e240` | Four famous plans | Full board, then Text Messaging purple, GPS blue, Cane Toads teal, Wider Highways amber. Return unmarked for the two-positive/two-negative comparison. |
| `lessons/unexpected-results-2-close.jpg` | `201f8332aa3e` | Close | Exact standard close, the two required lines, and literal final frame. No narration follows it. |

## Recommended production order

1. **Visual-repair pilot:** Loudest Voices. It exercises the dense long format, the
   four-card format, zoom/pan, and four inherited colors without touching audio.
2. **Reroll pilot:** Pace of Change. It exercises utility, three-card, two-card, status
   pills, banners, and color-locked highlights.
3. Review both pilots together.
4. Repair Opener and Data Centers.
5. Reroll Big Downside and Big Upside.
6. Reroll Rise of Agents and Work Changes.
7. Reroll Unexpected Results.
8. Run the flash, sentence-integrity, audio-blip, exact-board, highlight-color, and
   standard-close gates across all nine before shipping.

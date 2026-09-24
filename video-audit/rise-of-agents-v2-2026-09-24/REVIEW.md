# Rise of Agents v2: review candidate (2026-09-24)

**Candidate:** `Prompts/rise-of-agents-v2.mp4`, 2:58.4 (5352 frames at 30 fps). Review only. The live
video, lesson, and page are unchanged.

**Build:** `scripts/video/build_rise_of_agents_v2.py`, with the record in `build/edit-manifest.json`.

**Scope:** a full production pass on `Prompts/rise-of-agents-2.mp4`. David approved it on 2026-09-24:
both grafts and cut 1, per `video-audit/rise-of-agents-evaluation-2026-09-24/REVIEW.md`. The
optional "it's autonomous" cut was **not** taken.

## Narration changes

| Change | Source | Output | Seam silences |
|---|---|---|---|
| Graft B (hook), roll 1 0.00-6.10, gain −0.7 dB | "What exactly is an AI agent? To figure that out, let's start with a familiar comparison." | 0:00-0:06.1 | cut inside roll 1's 5.85-6.41 silence; roll 2 opens at 0.21. Joined gap ~0.46 s |
| Graft A (loop), roll 1 118.60-131.25 replaces roll 2 83.80-87.95, gain −0.2 dB | "Not done? Go again. The AI feeds its own evaluation right back into the planning stage to figure out its next move. An agent loops until the goal is met. You set the goal and judge the result." | 1:29.9-1:42.6 | roll 2 83.55-84.02 / 87.72-88.32; roll 1 118.23-118.83 / 131.04-131.57 |
| Cut 1, roll 2 139.25-142.50 | "To prevent this, apply one rule to your workflow." | ~2:33.6 | 138.98-139.56 / 142.28-142.75. Joined gap ~0.6 s |

No pauses were added. Speech levels were measured on active speech before grafting and match within
1 dB.

**Narration verified on the output** (medium.en, `words-medium.txt`): all eight required lines are
spoken, in lesson order.
- "A chatbot answers. An agent acts." @0:06
- "An agent is not a new kind of AI." @0:56
- the loop banner @1:37.6-1:42.2
- the responsibility line @1:43
- "Agents are good, but not perfect." @1:49
- the rule @2:34
- both closing lines @2:48.8 and @2:51.7, with nothing after (4.4 s of clean tail)

"workflow" no longer occurs anywhere. "autonomous" remains once @0:42.7 (cut 2 was not taken).

## Pictures

| Output | Board / picture | Treatment |
|---|---|---|
| 0:00-0:06 | roll 1 AI AGENT drawing (with graft B) | — |
| 0:06-0:24.7 | **A Chatbot Answers. An Agent Acts.** (canonical `rise-of-agents-gps.jpg`; the faceless variant does not ship) | compact, full view; GPS column ring on "Think of a chatbot as a GPS", self-driving column on "An agent is a self-driving car". 18.6 s |
| 0:24.7-0:30.7 | Notebook: dashboard / completed tasks | kept |
| 0:30.7-0:37.4 | **Ask a Chatbot versus Hire an Agent** (canonical) | dense, per-card camera; scenario ring at once in full view (no spoken intro), dive at 2 s; Ask a Chatbot card |
| 0:37.4-0:41.7 | BREAK (8b): roll 1 phone full of clips | under "reviewing clips, trimming, and assembling" |
| 0:41.7-0:56.8 | comparison board resumes | Hire an Agent card through "You still own..."; replaces Notebook's "Human Domain & Authority" restatement. 15.1 s |
| 0:56.8-1:13.6 | Notebook: LLM core / chatbot vs agent diagrams | kept, **flag**: "Autonomous Agent(s)" labels on screen |
| 1:13.6-1:42.9 | **What an Agent Does** (canonical, carries graft A) | compact; Goal, Plan, Act, Check (full height of the shared white box), the go-again loop, then the gold banner on "An agent loops". **29.2 s unbroken: over the 20 s rule.** No roll drew anything for this beat |
| 1:42.9-1:51.7 | Notebook: HUMAN OVERSIGHT REQUIRED | kept |
| 1:51.7-2:00.1 | **Rogue Agents** (canonical) | unmarked under the rogue-agents setup |
| 2:00.1-2:13.4 | Notebook: PocketOS diagram | kept, **flag**: invented "403 PERMISSION DENIED" and "rm -rf /data /backups" labels |
| 2:13.4-2:29.2 | **Rogue Agents** again | replaces Notebook's FATAL ERROR card: PocketOS card ring on "The agent later explained", Gemini card on "In 2025". The PocketOS ring pops 1 frame after the board returns (its second appearance; the full view was shown at 1:51.7) |
| 2:29.2-2:33.9 | Notebook: WARNING goal poorly defined | kept |
| 2:33.9-2:38.5 | roll 1 "Ready to Publish / Review & Approve" drawing | covers the keyboard tail and the "AUTONOMOUS SAFETY POLICY" slide, under the rule |
| 2:38.5-2:48.8 | Notebook: eye key, simple chat vs complex dashboard | kept |
| 2:48.8-end | standard close (canonical `agents` close) | replaces Notebook's close card and the Gemini Notebook outro |

No photographs were found in roll 2 or in the borrowed spans. The course's own GPS board photos are page
assets.

## Checks (Edit Spec 10)

1. The decoded frame count is 5352, which equals the plan. Each leg decoded its span exactly.
2. `transition_guard.py` passed all 17 boundaries (`transitions/`), and I inspected the strips.
   The first frame after each boundary is already the destination.
   - The first render put roll 1's Notebook **close card** under 2:34-2:38, because a frame number
     was wrong (6760 for 3:25.33; the correct frame is 6160). The strip caught it, and I fixed and
     re-rendered. That broken render was deleted; it was never reviewed or shipped.
3. Pauses: none added.
4. Ring state sheets `build/states-*.jpg` were inspected: every ring is on the right card and nothing
   is clipped. The comparison-board dive gains little because the cards are tall (the Edit Spec
   anticipates this). In the dive, the scenario strip shows as a sliver at the top of the frame.
5. Density: GPS, loop, and rogue boards are compact; the comparison board is dense. Every board opens
   at full view.
6. The corner mark was cleaned on 2060 frames (1796 cloned, 264 inpainted), with none declined.
   Protected files were unchanged (hash-checked).

## Not auditioned. David, please listen at these points

- **0:06**: graft B into roll 2's first line (voice continuity across rolls).
- **1:29.9** and **1:42.6**: into and out of graft A.
- **~2:33.6**: the cut 1 join ("...on its own." → "AI should not send...").

## Left undone

- **The 29 s loop board.** No drawing exists for it in either roll.
- **Two flagged Notebook spans kept**: the "Autonomous" diagram labels and the PocketOS diagram's
  invented labels. It's your call whether to cover them.
- **"and it's autonomous" @0:42.7** stays in, because optional cut 2 wasn't approved.
- **The page duration pill** still says "4 min" (`index.html:1160`). It should become "3 min" when this
  ships. Nothing was deployed.

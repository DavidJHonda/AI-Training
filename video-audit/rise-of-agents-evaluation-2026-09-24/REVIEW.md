# Rise of Agents — evaluation of rolls 1 and 2 and the live video (2026-09-24)

These are the first two rolls on the rebuilt kit (2026-09-23 Markdown and prompt). The live
`course-assets/rise-of-agents/rise-of-agents.mp4` (shipped under the old method) was evaluated at the
same time against the same current page.

Grounding: the live `index.html` Rise of Agents section. It matches `lessons/rise-of-agents.md`
point for point, so there's no materials bug.

Files:
- `Prompts/rise-of-agents-1.mp4` (3:53, speech ends 3:52.10, 3.19 s of clean tail)
- `Prompts/rise-of-agents-2.mp4` (2:46, speech ends 2:42.60, 3.39 s of clean tail)
- live `rise-of-agents.mp4` (3:17)

Method: `grade_bundle.py` for each file (base.en transcript, scenes, holds, contact sheets), then
`medium.en` with word timestamps on both rolls (`*/words-medium.txt`) and a −45 dB silence map
(`*/silences.txt`) for every cut and graft point below.

## Teaching points, both rolls and the live video

| # | Lesson point | Roll 1 | Roll 2 | Live | Better |
|---|---|---|---|---|---|
| 1 | "What's an agent?" + start with an analogy | TAUGHT @0:00 "What exactly is an AI agent? To figure that out, let's start with a familiar comparison." | MISSING (opens straight on the line) | MISSING (opens on an invented Stanley Cup scenario) | **1** |
| 2 | "A chatbot answers. An agent acts." | MET @0:06 | MET @0:00 | MISSED @0:31 "A chatbot answers, but an agent acts." | 1 = 2 |
| 3 | GPS is like ChatGPT: turn-by-turn, you still steer, brake, **and catch mistakes** | TAUGHT @0:13, but "catch mistakes" is dropped | TAUGHT @0:03 "Think of a chatbot as a GPS", but "catch mistakes" is dropped | THIN: never says GPS is like ChatGPT; adds an invented "path into a lake" | tie; neither roll has "catch mistakes" |
| 4 | Self-driving is like an agent: steers, brakes, reroutes; **you may not catch a mistake until later** | THIN @0:19. It has the steering, but the mistake clause is **missing**, and that's the point of the analogy | RICH @0:08-0:18 "You may not catch mistakes until later." | THIN: "supervisor" framing @0:34, no mistake clause | **2** |
| 5 | Agents are everywhere because they do the work | TAUGHT @0:26, adds "in the workplace" | RICH @0:18 "...suddenly everywhere. They actually do the work." | MISSING | **2** |
| 6 | Scenario: 30 points, Friday's game, friend's phone video, TikTok | RICH @0:37 (friend, 50 clips, TikTok; no "Friday") | TAUGHT @0:24 (Friday, TikTok; no friend's phone) | TAUGHT (no friend, no Friday) | 1 |
| 7 | Chatbot: you do everything; AI writes the caption; one step, then stops | TAUGHT @0:47 + @1:02 "single isolated task" | TAUGHT @0:28 (drops select plays, when to post, and "then stops") | RICH @0:50-1:08 | live > 1 > 2 |
| 8 | Agent does the whole job; **you still own the goal, final review, everything under your name** | THIN @0:54: "You own the goal". Final review and your name are both dropped | RICH @0:38-0:50 "You still own the goal, the final review, and everything posted under your name." | TAUGHT, "your handle" | **2** |
| 9 | "An agent is not a new kind of AI." | MET @1:14 | MET @0:50 | MISSED @1:37 "Agents are not a new type of AI model." | 1 = 2 |
| 10 | Same kind of LLM as ChatGPT | RICH @1:17 | RICH @0:52 | THIN (ChatGPT not named) | tie |
| 11 | What changes is after you type; chatbot answers and stops; agent plans, uses tools, checks, keeps going | TAUGHT @1:23 "after you hit submit" | RICH @0:57-1:07, the lesson's own sentences (drops "checks") | MISSING | **2** |
| 12 | Goal / Plan / Act / Check with their descriptions | RICH @1:35-1:58, all four, full descriptions incl. "Done or not?" | TAUGHT @1:11-1:23 (Act loses "for the next step"; Check loses "Done, or not?") | TAUGHT, Goal has no description | **1** |
| 13 | "Not done? Go again." + returns to the plan | RICH @1:58-2:06 "feeds its own evaluation right back into the planning stage" | THIN @1:23 "Not done? Go again." (no return to the plan) | TAUGHT "loops back, adjusting the plan" | **1** |
| 14 | Banner: "An agent loops until the goal is met. You set the goal and judge the result." | MET @2:06.32-2:10.98 | **MISSED** @1:25 "It loops until the goal is met." The second sentence is never spoken | MISSED | **1** |
| 15 | Your name on the finished product; evaluating the results still has to happen | THIN @2:17 "it is easy to get complacent" | MISSING (though #8 already carries "under your name") | MISSING | neither |
| 16 | "If an agent creates the TikTok clip and caption, you are responsible for reviewing it and making it better." | MET @2:22 (medium.en confirms "and", not base.en's "in") | MET @1:28 | MISSED | tie |
| 17 | "Agents are good. But not perfect." | MET @2:29 | MET @1:34 | MISSED | tie |
| 18 | Why agents go rogue: they keep acting, with tools and permissions; poorly defined goal or too much access means real damage | TAUGHT @2:32 (drops the chatbot-stops contrast) | RICH @1:37 "Because agents continuously work toward a goal and take action..." | TAUGHT "blast radius" | **2** |
| 19 | April 2026 PocketOS: permissions error, master key, live DB + backups, nine seconds, quotation | RICH @2:39-3:01, but see ERRORS for "committing agent" | RICH @1:45-2:02, quotation verbatim | THIN: "In 2026", no permissions error, no quotation | **2** |
| 20 | 2025 Gemini: files wiped, apology, quotation | TAUGHT @3:01, editorializes "a rather hollow apology" | RICH @2:03-2:13, the lesson's own sentence + quotation | THIN, no year, no quotation | **2** |
| 21 | "AI should not send, spend, submit, delete, or post without you reviewing first." | MET @3:30 | MET @2:22 | MET @2:49 | tie |
| 22 | Rule of thumb: great at automating steps, advanced tools, **start with ChatGPT**, they'll be there | TAUGHT @3:36 ("standard chatbots", not ChatGPT) | TAUGHT @2:28 "Start by getting good at standard ChatGPT." (drops "great at automating steps") | THIN: "it is a valid choice" softens the advice into an option | **2** |
| 23 | Two closing lines, nothing after | MET @3:46.58, @3:49.76 | MET @2:37.40, @2:40.9 | MET @3:09 | tie |

## Per-roll blocks

```text
LESSON: rise-of-agents
CANDIDATE: Prompts/rise-of-agents-1.mp4 (3:53)
VERDICT: REPAIR (donor only; roll 2 is the base)
TEACHING POINTS: see table. Failures are #4 THIN (mistake clause missing), #8 THIN (ownership reduced
  to "the goal"), #15 THIN.
HARD REQUIREMENTS: 8 of 8 MET
  "A chatbot answers. An agent acts." @0:06.46 · "An agent is not a new kind of AI." @1:14.78 ·
  banner @2:06.32-2:10.98 · responsibility line @2:22.16 · "Agents are good, but not perfect." @2:29.46
  (spoken as one phrase, comma cadence) · the rule @3:30.16 · closing lines @3:46.58, @3:49.76
ERRORS: @2:43.30 "A committing agent" (medium.en p=0.16 on "committing", 0.16 s long). The lesson says
  "AI coding agent". It's probably a mumbled "coding", but it **needs one listen**.
  @3:08 "a rather hollow apology" is an editorial judgment the lesson doesn't make.
  @2:55 "When prompted about the failure" is an invented detail. The lesson only says "The agent said".
SOURCE_QA: PASS
ADDITIONS: @2:00 "feeds its own evaluation right back into the planning stage" (accurate; it's the
  best explanation of the go-again arrow in any take).
  Flagged, not welcome: @3:15-3:25 "An agent's greatest strength is its relentless drive to overcome
  obstacles and finish a task. Without strict boundaries, that exact trait makes it dangerous." This
  praises the exact behaviour the prompt bans (working around a block, promising it finishes), and it
  contradicts the Be the Agent activity ("Blocked means report back, not improvise").
REPAIR PLAN: not pursued. Roll 2 is the better base (see the best-of plan). If roll 1 were the base:
  #4 take roll 2 @16.06-18.02 "You may not catch mistakes until later." (0.44 s silence before and
  0.52 s after, under the GPS board); #8 take roll 2 @46.28-50.24 (it sits under Notebook's own
  diagram, not a board); cut @3:15.48-3:25.33 and @2:11.50-2:17.00.
EDITING NOTES: banned words "workflows" @2:11 and "autonomously" @2:50. Formal register ("innovation",
  "actionable", "mistakes happen at scale", "multi-stage"). The loop board holds 43.2 s
  (1:28-2:11). Drawn people (dunking silhouette @0:36, reclining man @2:20, man with phone
  @2:24) break the no-people rule. On-screen "Autonomous AI Agent" @1:08 and "AUTONOMOUS AGENT" @2:32.
  Donor value is high: the AI AGENT opener, the phone of clips, "Video Publishing" checklist,
  error-window monitor, and "Ready to Publish / Review & Approve" drawings.
LISTENING: not listened to. base.en + medium.en word timestamps throughout. Unheard: "committing".
```

```text
LESSON: rise-of-agents
CANDIDATE: Prompts/rise-of-agents-2.mp4 (2:46)
VERDICT: REPAIR (one graft, under the loop board)
TEACHING POINTS: see table. Failures are #14 MISSED (hard requirement), #13 THIN, #1 MISSING (hook), #15
  MISSING (softened by #8).
HARD REQUIREMENTS: 7 of 8 MET
  "A chatbot answers. An agent acts." @0:00 · "An agent is not a new kind of AI." @0:50.76 ·
  banner: MISSED @1:25.44, "It loops until the goal is met." and the second sentence is never spoken ·
  responsibility line @1:28.40 · "Agents are good, but not perfect." @1:34 · the rule @2:22.62 ·
  closing lines @2:37.40, @2:40.9
ERRORS: none factual.
SOURCE_QA: PASS
ADDITIONS: @2:14.46 "You can never expect an agent to safely navigate poorly defined constraints on its
  own." (accurate, harmless)
REPAIR PLAN:
  GRAFT A (required): replace roll 2 @83.94-87.72 ("Not done? Go again. It loops until the goal is
    met.") with roll 1 @118.78-130.98 ("Not done? Go again. The AI feeds its own evaluation right back
    into the planning stage to figure out its next move. An agent loops until the goal is met. You set
    the goal and judge the result."). Seams: roll 2 silence 83.55-84.02 and 87.72-88.32; roll 1 silence
    118.23-118.83 and 131.04-131.57. The whole beat sits between clean silences on both sides, under the
    loop board in both rolls. This fixes #14 and #13 in one move. +8.4 s.
  GRAFT B (optional, recommended): prepend roll 1 @0:00.00-5.85 ("What exactly is an AI agent? To
    figure that out, let's start with a familiar comparison.") over roll 1's own AI AGENT drawing.
    Silence 5.85-6.41 in roll 1. It restores #1. +6.1 s. Needs your ear for voice continuity into roll
    2's first line.
  CUT 1: excise @139.46-142.06 "To prevent this, apply one rule to your workflow." (banned word).
    Silence 138.98-139.56 before and 142.28-142.75 after. −2.6 s.
  CUT 2 (optional, needs ear): "Hire an agent, and it's autonomous." @36.62-38.28. Remove
    37.30-38.55 so it reads "Hire an agent. It reviews, selects...". There's only a 0.18 s gap after
    "agent," with comma intonation, so preview it before committing.
EDITING NOTES: see the edit plan below. No photographs found. On-screen "Autonomous Agents" @0:56 and
  "Autonomous Agent" @1:00-1:07, and "AUTONOMOUS SAFETY POLICY" @2:24. The Notebook PocketOS diagram
  @1:48-1:58 shows an invented shell command ("rm -rf /data /backups") and a "403 PERMISSION DENIED"
  label. It's plausible but not in the lesson, so it's your call. The standard close replaces 2:39, and
  the Notebook outro @2:44 is removed.
LISTENING: not listened to. base.en + medium.en word timestamps; silences measured at every seam.
```

```text
LESSON: rise-of-agents
CANDIDATE: course-assets/rise-of-agents/rise-of-agents.mp4 (3:17, live)
VERDICT: REROLL (superseded by roll 2 + graft)
TEACHING POINTS: see table. MISSING: #1, #5, #11, #15. MISSED verbatim: #2, #9, #14, #16, #17.
  THIN: #3, #4, #10, #19, #20, #22.
HARD REQUIREMENTS: 3 of 8 MET (the rule and the two closing lines).
ERRORS: @0:00 "Game 7 of the Stanley Cup Finals" is invented. @0:16 "a path into a lake" is invented.
  @2:05 "the engine that removes the human from the middle of the workflow, handing over the power to
  execute" runs against "You set the goal and judge the result". @2:24 "In 2026" drops April and the
  permissions error, and neither quotation is spoken.
SOURCE_QA: PASS
ADDITIONS: @3:02 "choosing to deploy an agent means accepting that you are responsible for everything
  the system does" (accurate idea, banned word)
REPAIR PLAN: none. Roll 2 beats it on 14 of 23 points and ties most of the rest.
EDITING NOTES: banned words: workflow ×2, autonomous ×3, deploy. Board furniture: "This graphic shows"
  @0:38, "This diagram illustrates" @1:46, "This board details" @2:20. Its opening car drawings @0:00-0:30
  (phone map, steering wheel, dashboard GPS, foot on brake, cockpit) are the best donor pictures for
  the GPS beat.
LISTENING: not listened to.
```

```text
BEST-OF PLAN: rise-of-agents
BASE: Prompts/rise-of-agents-2.mp4 (it wins the analogy's mistake clause, the full ownership list,
  "what changes is what happens after you type", both rogue cases and their quotations, "ChatGPT" in the
  rule of thumb, and it has the most natural register and a runtime near the pill)
  #14 banner: roll 1 MET @2:06.32 "An agent loops until the goal is met. You set the goal and judge
    the result." | roll 2 MISSED @1:25.44 "It loops until the goal is met." — TAKE roll 1 (under the
    loop board)
  #13 return to the plan: roll 1 RICH @2:00.72 "feeds its own evaluation right back into the planning
    stage" | roll 2 THIN @1:23.94 "Not done? Go again." — TAKE roll 1 (same graft)
  #1 hook: roll 1 TAUGHT @0:00 "What exactly is an AI agent?" | roll 2 MISSING — TAKE roll 1 (head,
    over roll 1's AI AGENT drawing; optional)
  #12 loop descriptions: roll 1 RICH @1:35 | roll 2 TAUGHT @1:11 — not grafted: roll 2 is adequate,
    and a longer graft would run 40+ s on one board
  #6 friend's phone + 50 clips: roll 1 RICH @0:37 | roll 2 TAUGHT @0:24 — not grafted: roll 1's
    beat sits under Notebook's drawings and would add 10 s
GRAFTS: 2 (loop graft under the loop board; head graft over a Notebook drawing at file start)
```

## Proposed edit plan (roll 2 base, provisional pending your approval)

Timings are roll 2 source times. Estimated result: about 2:58 with both grafts and cut 1. The lesson
pill says "4 min" (`index.html:1160`) and should become "3 min" on ship.

| Board | Highlighting sequence | Camera | On screen / breaks | Reason or exception |
|---|---|---|---|---|
| A Chatbot Answers. An Agent Acts. (canonical `rise-of-agents-gps.jpg`; the faceless variant never ships) | title at "A chatbot answers" 0:00; GPS Is Like ChatGPT card 0:03.9; Self-Driving card 0:08.9 | full board; compact | 0:00-0:18.6 (18.6 s, under 20 s). With graft B, roll 1's AI AGENT drawing runs first | — |
| Ask a Chatbot versus Hire an Agent | scenario strip 0:24.7; Ask a Chatbot card 0:28.6; Hire an Agent card 0:36.6, held through "You still own" 0:46.3 | full view, then complete-card dives (dense: card text is small at 1280) | ~0:24.7-0:50.2, 25.5 s. Break: roll 1's phone-of-clips drawing (roll 1 @0:40-0:46) under 0:30-0:34 "reviewing clips, trimming, and assembling", back to the board ~0:35.5 | replaces Notebook's "Human Domain & Authority" re-diagram of the board @0:44-0:50, which restates the board (8b) |
| What an Agent Does | Goal 1:11.08; Plan 1:14.2; Act 1:18.4; Check 1:20.5; "NOT DONE? GO AGAIN." loop at the graft's start; gold banner at the graft's "An agent loops" | full board; compact (matches the four-step-strip calibration) | 1:07.5 to the graft end, ≈28 s. **Flag:** no roll drew anything for this beat, so the ring sequence carries it | over the 20 s rule, with no donor |
| Rogue Agents | PocketOS card 1:45.5; Gemini card 2:03.4 | full board; compact | 1:40-1:48 and 2:04-2:14 (≈18 s), with Notebook's PocketOS diagram and FATAL ERROR drawing between | your call on the diagram's invented shell command |
| Close | standard close | — | replaces 2:37-end | — |

Other picture swaps:
- 2:23-2:28 "AUTONOMOUS SAFETY POLICY" slide goes. Cover it with roll 1's "Ready to Publish / Review &
  Approve" drawing (roll 1 @3:28-3:40), which fits the rule exactly.
- 0:56-1:07 LLM and "Autonomous Agent" diagrams carry the banned word on screen. They're low priority
  and replaceable with roll 1's Chatbot/Agent servers drawing (roll 1 @1:16-1:20).
- The live video's car drawings @0:00-0:30 are available if you'd rather break up the GPS board.

Pauses: none proposed yet. I'll measure the gaps against the assembled cut.

## Recommendation

**Build roll 2 with graft A** (required), and graft B (the hook) if it sounds continuous to you.
Cut "apply one rule to your workflow". Retire the live video: it meets 3 of 8 verbatim lines, invents
the Stanley Cup setup, and never gives either rogue-agent quotation.

Two things need your ear:
1. Roll 1 @2:43 "committing agent". It doesn't matter for the recommended build, because that span isn't
   used.
2. The seam at graft B, and the optional "it's autonomous" cut.

Neither roll speaks "and catch mistakes" in the GPS half, or "they're great at automating steps" in the
rule of thumb. The Markdown and prompt already carry both, so these are generation misses, not
materials bugs. They're minor and don't call for a reroll.

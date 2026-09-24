# Rise of Agents v3: review candidate (2026-09-24)

**Candidate:** `Prompts/rise-of-agents-v3.mp4`, 3:00.0 (5401 frames at 30 fps). Review only. The live
video, v2, the lesson, and the page are unchanged.

**Build:** `scripts/video/build_rise_of_agents_v3.py`, with the record in `build/edit-manifest.json`.

**Scope:** v2 (`video-audit/rise-of-agents-v2-2026-09-24/REVIEW.md`) with David's three notes on it:
1. The live video's intro (live 0:00-0:38) replaces v2's first ~0:30.
2. Highlighting follows the live video: whenever the narration speaks a section inside a card, that
   section is ringed. The non-board drawings stay.
3. The live video's narration for What an Agent Does replaces roll 2's.

## Narration, in order

| Output | Source | Words |
|---|---|---|
| 0:00-0:38.2 | live 0.00-38.20 (+0.4 dB) | Stanley Cup / GPS / "you hit the brakes" / "You are the executor." / self-driving / "A chatbot answers, but an agent acts." / "Your role shifts from being the driver to being the supervisor." |
| 0:38.2-1:24.5 | roll 2 24.45-70.70 | the comparison board, "An agent is not a new kind of AI.", LLM, "We can see how this works in the four-step agent loop." |
| 1:24.5-1:39.1 | live 110.95-125.50 (+0.4 dB) | "It starts by setting a goal. The agent generates a plan, breaking it into steps. It acts, using tools to complete a step, then performs a check. If unsuccessful, it loops back, adjusting the plan until it succeeds." |
| 1:39.1-1:44.3 | roll 1 126.05-131.25 (−0.6 dB) | "An agent loops until the goal is met. You set the goal and judge the result." |
| 1:44.3-end | roll 2 87.95-163.00, with cut 1 | as v2 |

**My choices inside note 3**, which are David's to reverse. Two sentences of the live loop narration are
left out:
- "This diagram illustrates the four-step loop turning intent into a result." It's board-furniture
  narration, and roll 2's intro line stands in.
- "This continuous cycle is the engine that removes the human from the middle of the workflow, handing
  over the power to execute." It contradicts the banner and uses the banned word "workflow".

Roll 1's banner line follows the live narration, because the live video never speaks it and it's a
required line.

**Verified on the output** (medium.en, `words-medium.txt`). Seven of the eight required lines are
spoken:
- "An agent is not a new kind of AI." @1:04.5
- the banner @1:39.3-1:43.9
- the responsibility line @1:44.4
- "Agents are good, but not perfect." @1:50.6
- the rule @2:35.9
- both closing lines @2:50.4 and @2:53.4, with nothing after

"workflow" doesn't occur. "autonomous" occurs twice: the live's "autonomous vehicle" @0:22 and roll 2's
"it's autonomous" @0:50.

### What the live intro gives up (for David's decision, not a blocker)

Against the evaluation's teaching points, swapping in the live intro drops these lines that v2 had:
- **"A chatbot answers. An agent acts."** is spoken as "A chatbot answers, but an agent acts." That's
  a required verbatim line; the board title still shows it, ringed while it's spoken.
- **"You may not catch mistakes until later."** is gone. That's the point of the self-driving half. The
  live comes closest with "If the app suggests a path into a lake, you hit the brakes."
- **"GPS is like ChatGPT"** and **"self-driving is like an agent"** are never said as such.
- **"Agents are suddenly everywhere... they do the work."** is gone.
- **The Stanley Cup Game 7 setup and the lake** aren't in the lesson. The board's photos do show
  hockey jerseys and an arena.

## Highlighting (section-level, after the live video)

| Board | Rings (spoken onset) | Camera |
|---|---|---|
| A Chatbot Answers. An Agent Acts. | title on "A chatbot answers, but an agent acts." @0:31.9, held through "supervisor" | full board; on screen 0:31.7-0:38.2 |
| Ask a Chatbot versus Hire an Agent | THE SCENARIO @0:38.4 · YOU DO @0:42.3 · (break: roll 1 phone of clips @0:45.4-0:47.7) · AI DOES @0:48.2 · THE AGENT DOES @0:50.3 · WHAT CHANGES (agent) @0:56.2 · YOU STILL OWN @1:00.0 | dense: full view with the scenario ring, then per-card dives |
| What an Agent Does | Goal @1:24.9 · Plan @1:26.8 · Act @1:29.9 · Check @1:32.4 · go-again loop @1:34.4 · gold banner @1:39.3 | compact; 1:21.3-1:44.5 (23.3 s, down from v2's 29.2 s) |
| Rogue Agents (first) | unmarked (setup) | compact |
| Rogue Agents (second) | PocketOS quotation @2:14.9 · Gemini card @2:19.5 · Gemini quotation @2:27.6 | compact |

Chatbot WHAT CHANGES isn't ringed because roll 2 never speaks it. The break under "reviewing clips,
trimming, and assembling" is shortened to 2.3 s, so that AI DOES is on screen and ringed when it's said.

## Checks

1. The frame count is 5401, which equals the plan. Each leg decoded its span exactly. Protected files,
   including v2 and the live video, are unchanged (hash-checked).
2. `transition_guard.py` passed all 17 boundaries (`transitions/`), and I inspected the strips.
3. The corner mark was cleaned on 1822 frames (1420 cloned, 402 inpainted), with none declined. The
   live's own frames still carried a faint Gemini Notebook mark; it's cleaned in v3.
4. The ring state sheets `build/states-*.jpg` were inspected. Every section ring sits inside its card,
   on the right section.

## Not auditioned. Listen at these points

- **0:38.2**: live voice into roll 2 ("...supervisor." → "Say you scored 30 points...").
- **1:24.5**: roll 2 into live ("...four-step agent loop." → "It starts by setting a goal.").
- **1:39.1**: live into roll 1 ("...until it succeeds." → "An agent loops...").
- **1:44.3**: roll 1 into roll 2 ("...judge the result." → "If an agent creates...").
- **~2:35**: the cut 1 join.

The live, roll 1 and roll 2 are the same Notebook voice, but they're three separate generations, so
listen for pitch and pace changes at these joins.

## Flags carried from v2

- The "Autonomous Agent" diagram labels @1:04-1:21.
- The PocketOS diagram's invented "403" and "rm -rf" labels @2:01-2:14.
- The page pill still says "4 min" and should become "3 min" on ship.

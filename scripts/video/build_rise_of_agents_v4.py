#!/usr/bin/env python3
"""Rise of Agents v4 review candidate (2026-09-24). Review only; the live video, v2 and v3 are unchanged.

v3 plus the lesson's transition from the analogy to the example (David's note on v3, option 1 approved 2026-09-24):
  roll 2 18.45-24.30  "This distinction is exactly why AI agents are suddenly everywhere. They actually do the work."
                      In inside 18.18-18.70 ("This" 18.72); out inside 24.07-24.64 ("work." ends 24.04). Picture: roll 2's
                      Completed Tasks dashboard drawing from its own cut (559); its 18.45-18.63 frames are a Notebook board
                      render and are not shown.
  roll 1 35.00-36.95  "Let's look at a concrete example." In inside 34.62-35.27, out inside 36.69-37.25. Gain +1.0 dB
                      (the phrase measures -18.0 dBFS against roll 2's -16.6). The dashboard drawing holds its last frame.
Everything else is v3:

v2 (build_rise_of_agents_v2.py) with David's three notes on it (2026-09-24):
  1. The live video's intro (live 0:00-0:38) replaces v2's first ~0:30 (roll 1's hook + roll 2's GPS/everywhere beat).
  2. Board highlighting follows the live video: when the narration speaks a section inside a card, that section is
     ringed (YOU DO, AI DOES, THE AGENT DOES, WHAT CHANGES, YOU STILL OWN; the rogue-agent quotations). Notebook's
     non-board drawings stay.
  3. The live video's narration for What an Agent Does replaces roll 2's.

Narration (medium.en word stamps; silences at -45 dB; LIVE = course-assets/rise-of-agents/rise-of-agents.mp4):
  LIVE 0.00-38.20      Stanley Cup / GPS / self-driving / "A chatbot answers, but an agent acts." / "Your role shifts
                       from being the driver to being the supervisor." Out inside 37.94-38.56. Gain +0.4 dB.
  roll 2 24.45-70.70   comparison board, LLM, "We can see how this works in the four-step agent loop." In inside
                       24.07-24.64 ("Say" 24.68); out inside 70.42-70.96 ("One," 71.08).
  LIVE 110.95-125.50   "It starts by setting a goal. ... If unsuccessful, it loops back, adjusting the plan until it
                       succeeds." In inside 110.82-111.25, out inside 125.26-125.82. Gain +0.4 dB. Two live sentences
                       are left out: "This diagram illustrates the four-step loop turning intent into a result." (board
                       furniture; roll 2's intro line stands in) and "This continuous cycle is the engine that removes the
                       human from the middle of the workflow, handing over the power to execute." (contradicts the
                       banner and uses a banned word).
  roll 1 126.05-131.25 "An agent loops until the goal is met. You set the goal and judge the result." (required banner
                       line; the live never speaks it). In inside 125.93-126.34, out inside 131.04-131.57. Gain -0.6 dB.
  roll 2 87.95-163.00  as v2, with cut 1 (139.25-142.50, "To prevent this, apply one rule to your workflow.").
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, NEUTRAL, PURPLE, BLUE, TEAL, GREEN

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "Prompts"
SRC, R1 = P / "rise-of-agents-2.mp4", P / "rise-of-agents-1.mp4"
A_ = ROOT / "course-assets/rise-of-agents"
LIVE = P / "rise-of-agents-live-pre-v4.mp4"   # the pre-v4 live video (commit 6cccc758), preserved when v4 shipped 2026-09-24
OUT = ROOT / "video-audit/rise-of-agents-v4-2026-09-24/build"
DEST = P / "rise-of-agents-v4.mp4"
GPS, COMPARE, LOOP, ROGUE, CLOSE = (A_ / f"rise-of-agents-{k}.jpg" for k in ("gps", "chatbot-vs-agent", "agent-loop", "rogue", "close"))
LESSON = ROOT / "lessons/rise-of-agents.md"

# Live intro
LIVE_BOARD_IN = 950                     # live 31.67 cut from the cockpit drawing to its GPS board
LIVE_INTRO_END = 1146                   # live 38.20
# Transition: roll 2 "everywhere / do the work" + roll 1 "Let's look at a concrete example."
EVERY_IN, EVERY_OUT = fr(18.45), fr(24.30)   # 554, 729
DASH_IN, DASH_END = 559, 737                 # roll 2 Completed Tasks drawing
EX_A, EX_B = fr(35.00), 1108                 # roll 1 35.00-36.95
# Roll 2 comparison board
CMP_IN, CMP_OUT = 734, 1521             # 24.45 (roll 2 audio resumes) -> 50.70 LLM diagram
CMP_BRK_IN, CMP_BRK_OUT = fr(31.70), fr(34.00)   # under "reviewing clips, trimming, and assembling"
R1_PHONE = 1200                         # R1 40.00-44.73 phone full of clips drawing
# Loop board
LOOP_IN, LOOP_R2_OUT = 2026, fr(70.70)  # 67.53 board in; roll 2's intro line ends 70.42
LIVE_LA, LIVE_LB = 3328, 3765           # live 110.95-125.50
R1A, R1B = 3782, 3938                   # roll 1 126.05-131.25
GB, LOOP_SRC_OUT = 2638, 2648           # roll 2 resumes 87.95 ("If" 88.40); its cut to HUMAN OVERSIGHT at 88.27
ROGUE_A = (2912, 3164)
ROGUE_B = (3562, 4038)
CUT_A, CUT_B = fr(139.25), fr(142.50)
POLICY_OUT = 4413
R1_PUBLISH = 6160                       # R1 3:25.33 Ready to Publish drawing
CLOSE_IN, CLOSE_END = 4721, fr(163.00)

# Leg coordinates
CMP_SHIFT = (CMP_BRK_OUT - CMP_BRK_IN) / FPS
CMP_LEG_END = CMP_BRK_IN + (CMP_OUT - CMP_BRK_OUT)
L_LIVE = LOOP_R2_OUT                             # leg frame where the live loop audio starts
L_R1 = L_LIVE + (LIVE_LB - LIVE_LA)              # leg frame where roll 1's banner line starts
L_RESUME = L_R1 + (R1B - R1A)                    # leg frame where roll 2 resumes
LOOP_LEG_END = L_RESUME + (LOOP_SRC_OUT - GB)
def cmp_leg(t): return t - CMP_SHIFT
def loop_live(t): return (L_LIVE + fr(t) - LIVE_LA) / FPS
def loop_r1(t): return (L_R1 + fr(t) - R1A) / FPS

# Rects in each canonical JPG's own pixels (measured 2026-09-24).
GPS_TITLE = [17, 32, 846, 97]
CMP_SCEN, CMP_CHAT, CMP_AGENT = [41, 112, 1560, 254], [41, 286, 784, 1354], [817, 286, 1560, 1354]
CHAT_YOU_DO, CHAT_AI_DOES = [57, 848, 768, 1032], [57, 1059, 768, 1161]
AGENT_DOES, AGENT_OWN, AGENT_CHANGES = [833, 848, 1544, 1032], [833, 1059, 1544, 1202], [833, 1229, 1544, 1331]
LOOP_COLS = [[40, 127, 420, 763], [420, 127, 800, 763], [800, 127, 1180, 763], [1180, 127, 1561, 763]]
LOOP_ARROW = [592, 614, 1390, 736]
ROGUE_CARDS = [[41, 127, 784, 902], [817, 127, 1560, 902]]
POCKET_QUOTE, GEMINI_QUOTE = [57, 781, 768, 836], [833, 781, 1544, 877]


def T(label, at, rect, color, **kw):
    return dict(label=label, at=at, rects=[rect], color=color, **kw)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[R1, LIVE, GPS, COMPARE, LOOP, ROGUE, CLOSE, LESSON, ROOT / "index.html", P / "rise-of-agents-v2.mp4", P / "rise-of-agents-v3.mp4"])
    b.load_audio([(2.92, 3.48), (9.05, 9.59), (18.18, 18.70), (24.07, 24.64), (36.00, 36.54), (70.42, 70.96), (75.14, 75.64),
                  (87.72, 88.32), (138.98, 139.56), (142.28, 142.75), (156.73, 157.37), (162.63, 166.02)])

    b.graft(LIVE, 0, LIVE_BOARD_IN, "Live intro: Stanley Cup, GPS, steering wheel, brake, the self-driving cockpit (live's own drawings)",
            "live-intro", cover_intro=False, gain_db=0.4)
    b.graft(LIVE, LIVE_BOARD_IN, LIVE_INTRO_END, "Live intro audio under our GPS board: 'A chatbot answers, but an agent acts. Your role shifts...'",
            "live-intro-board", picture_from=0, gain_db=0.4, visual="gps")
    b.keep(EVERY_IN, EVERY_OUT, "Roll 2: 'This distinction is exactly why AI agents are suddenly everywhere. They actually do the work.' over its Completed Tasks drawing",
           video_from=DASH_IN, video_end=DASH_END)
    b.graft(R1, EX_A, EX_B, "Roll 1: 'Let's look at a concrete example.' (Completed Tasks drawing holds)", "r1-example",
            picture_from=DASH_IN + (EVERY_OUT - EVERY_IN), gain_db=1.0, video_end=DASH_END)
    b.keep(CMP_IN, CMP_BRK_IN, "Ask a Chatbot versus Hire an Agent (canonical): scenario, YOU DO", "compare")
    b.keep(CMP_BRK_IN, CMP_BRK_OUT, "BREAK (8b): R1 phone full of clips under 'reviewing clips, trimming, and assembling'",
           video_from=R1_PHONE, video_src=R1, video_end=1342)
    b.keep(CMP_BRK_OUT, CMP_OUT, "Comparison board: AI DOES, THE AGENT DOES, WHAT CHANGES, YOU STILL OWN", "compare", video_from=CMP_BRK_IN)
    b.keep(CMP_OUT, LOOP_IN, "Notebook: LLM core, ChatGPT/agents share it, chatbot stops vs agent loops (flag: 'Autonomous' labels)")
    b.keep(LOOP_IN, LOOP_R2_OUT, "What an Agent Does (canonical): 'We can see how this works in the four-step agent loop.'", "loop")
    b.graft(LIVE, LIVE_LA, LIVE_LB, "Live loop narration under our loop board: goal, plan, act, check, loops back", "live-loop",
            picture_from=L_LIVE, gain_db=0.4, visual="loop")
    b.graft(R1, R1A, R1B, "Roll 1 banner line under our loop board: 'An agent loops until the goal is met. You set the goal and judge the result.'",
            "r1-banner", picture_from=L_R1, gain_db=-0.6, visual="loop")
    b.keep(GB, LOOP_SRC_OUT, "What an Agent Does: banner held into the responsibility line", "loop", video_from=L_RESUME)
    b.keep(LOOP_SRC_OUT, ROGUE_A[0], "Notebook: HUMAN OVERSIGHT REQUIRED (responsibility line, good but not perfect)")
    b.keep(*ROGUE_A, "Rogue Agents (canonical), unmarked under the rogue-agents setup", "rogue-a")
    b.keep(ROGUE_A[1], ROGUE_B[0], "Notebook: PocketOS diagram (flag: invented 403 / rm -rf labels)")
    b.keep(*ROGUE_B, "Rogue Agents (canonical) replaces FATAL ERROR and the board render: PocketOS quotation, Gemini, its quotation", "rogue-b")
    b.keep(ROGUE_B[1], CUT_A, "Notebook: WARNING goal poorly defined")
    b.keep(CUT_B, POLICY_OUT, "R1 Ready to Publish / Review & Approve drawing covers the keyboard tail and the AUTONOMOUS SAFETY POLICY slide, under the rule",
           video_from=R1_PUBLISH, video_src=R1, video_end=6491)
    b.keep(POLICY_OUT, CLOSE_IN, "Notebook: eye key, simple chat vs complex dashboard (rule of thumb)")
    b.mark_close_start()
    b.keep(CLOSE_IN, CLOSE_END, "Canonical close replaces Notebook's close card and outro: the two closing lines")
    b.pause(120, "Settled close hold")
    b.finish_audio()

    b.board("gps", GPS, 0, LIVE_INTRO_END - LIVE_BOARD_IN, "compact", [
        T("Title: 'A chatbot answers, but an agent acts.'", (fr(31.86) - LIVE_BOARD_IN) / FPS, GPS_TITLE, NEUTRAL)], min_open=0)
    b.board("compare", COMPARE, CMP_IN, CMP_LEG_END, "dense", [
        T("The scenario: 'Say you scored 30 points...'", 24.68, CMP_SCEN, PURPLE, cam=CMP_SCEN),
        T("Ask a Chatbot / YOU DO: 'Ask a regular chatbot, and you do the heavy lifting...'", 28.58, CHAT_YOU_DO, PURPLE, cam=CMP_CHAT),
        T("Ask a Chatbot / AI DOES: 'The AI just writes the caption.'", cmp_leg(34.48), CHAT_AI_DOES, PURPLE, cam=CMP_CHAT),
        T("Hire an Agent / THE AGENT DOES: 'Hire an agent... It reviews, selects, builds, captions, and publishes.'", cmp_leg(36.62), AGENT_DOES, BLUE, cam=CMP_AGENT),
        T("Hire an Agent / WHAT CHANGES: 'The agent carries the job all the way through.'", cmp_leg(42.50), AGENT_CHANGES, BLUE, cam=CMP_AGENT),
        T("Hire an Agent / YOU STILL OWN: 'You still own the goal, the final review...'", cmp_leg(46.28), AGENT_OWN, BLUE, cam=CMP_AGENT)],
        min_open=0, per_target_camera=True)
    b.board("loop", LOOP, LOOP_IN, LOOP_LEG_END, "compact", [
        T("1 Goal: 'It starts by setting a goal.'", loop_live(111.34), LOOP_COLS[0], PURPLE),
        T("2 Plan: 'The agent generates a plan...'", loop_live(113.26), LOOP_COLS[1], BLUE),
        T("3 Act: 'It acts, using tools...'", loop_live(116.42), LOOP_COLS[2], TEAL),
        T("4 Check: 'then performs a check.'", loop_live(118.92), LOOP_COLS[3], GREEN),
        T("Not done? Go again: 'If unsuccessful, it loops back...'", loop_live(120.92), LOOP_ARROW, NEUTRAL)],
        banner_at=loop_r1(3790 / FPS))   # roll 1 "An agent loops" 126.32 = frame 3790
    b.board("rogue-a", ROGUE, *ROGUE_A, "compact", [])
    b.board("rogue-b", ROGUE, *ROGUE_B, "compact", [
        T("PocketOS quotation: 'The agent later explained, I violated every principle I was given.'", 118.78, POCKET_QUOTE, PURPLE),
        T("2025 Gemini card: 'In 2025, a Google Gemini agent wiped out...'", 123.36, ROGUE_CARDS[1], BLUE),
        T("Gemini quotation: 'I have failed you completely and catastrophically.'", 131.32, GEMINI_QUOTE, BLUE)], min_open=0)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("agents")
    s = lambda f: round(f / FPS, 2)
    b.manifest({
        "scope_detail": "v3 plus roll 2 'suddenly everywhere / they actually do the work' and roll 1 'Let's look at a concrete example.' between the live intro and the comparison board. v3 was v2 with David's three notes (2026-09-24): the live video's intro replaces v2's opening; section-level rings wherever the narration speaks a section inside a card; the live video's loop narration replaces roll 2's (two live sentences left out, roll 1's banner line kept).",
        "narration": [
            {"source": "live", "seconds": [0.0, s(LIVE_INTRO_END)], "gain_db": 0.4},
            {"source": "roll 2", "seconds": [s(EVERY_IN), s(EVERY_OUT)]},
            {"source": "roll 1", "seconds": [s(EX_A), s(EX_B)], "gain_db": 1.0},
            {"source": "roll 2", "seconds": [s(CMP_IN), s(LOOP_R2_OUT)]},
            {"source": "live", "seconds": [s(LIVE_LA), s(LIVE_LB)], "gain_db": 0.4, "omitted_before": "This diagram illustrates the four-step loop turning intent into a result.",
             "omitted_after": "This continuous cycle is the engine that removes the human from the middle of the workflow, handing over the power to execute."},
            {"source": "roll 1", "seconds": [s(R1A), s(R1B)], "gain_db": -0.6},
            {"source": "roll 2", "seconds": [s(GB), s(CLOSE_END)], "cut": {"seconds": [s(CUT_A), s(CUT_B)], "text": "To prevent this, apply one rule to your workflow."}}],
        "picture_replacements": [
            {"source_frames": [CUT_B, POLICY_OUT], "what": "keyboard tail + 'AUTONOMOUS SAFETY POLICY' slide", "cover": "R1 frames 6160-6298, Ready to Publish / Review & Approve drawing"},
            {"source_frames": [3562, 3699], "what": "Notebook FATAL ERROR card", "cover": "canonical Rogue Agents board (PocketOS quotation)"},
            {"source_frames": [1273, 1521], "what": "Notebook 'Human Domain & Authority' restatement of the comparison board", "cover": "canonical comparison board"}],
        "board_breaks": [{"board": "compare", "source_frames": [CMP_BRK_IN, CMP_BRK_OUT], "drawing": "R1 frames 1200-1269, phone full of clips"}],
        "longest_board_runs_seconds": {"gps": s(LIVE_INTRO_END - LIVE_BOARD_IN), "compare_before_break": s(CMP_BRK_IN - CMP_IN),
                                       "compare_after_break": s(CMP_OUT - CMP_BRK_OUT), "loop": s(LOOP_LEG_END - LOOP_IN),
                                       "rogue_a": s(ROGUE_A[1] - ROGUE_A[0]), "rogue_b": s(ROGUE_B[1] - ROGUE_B[0])},
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:50]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()

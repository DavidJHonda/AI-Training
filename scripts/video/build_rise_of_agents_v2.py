#!/usr/bin/env python3
"""Rise of Agents v2 review candidate from rise-of-agents-2 (2026-09-24). Review only; the live video is unchanged.

Full production pass on roll 2, the second roll on the 2026-09-23 kit. David approved (2026-09-24) the evaluation's
plan in video-audit/rise-of-agents-evaluation-2026-09-24/REVIEW.md: both grafts and cut 1. The optional
"it's autonomous" cut was not taken.

Narration (word stamps from faster-whisper medium.en; silences at -45 dB):
  GRAFT B  head: roll 1 0.00-6.10, "What exactly is an AI agent? To figure that out, let's start with a familiar
           comparison.", with roll 1's own AI AGENT drawing. Out inside roll 1's 5.85-6.41 silence. Roll 2 then
           opens at 0.00 (speech from 0.21). Gain -0.7 dB: roll 1 head speech -16.4 dBFS vs roll 2 opening -17.2.
  GRAFT A  replaces roll 2 83.80-87.95 ("Not done? Go again. It loops until the goal is met.", inside the
           83.55-84.02 / 87.72-88.32 silences) with roll 1 118.60-131.25 ("Not done? Go again. The AI feeds its own
           evaluation right back into the planning stage to figure out its next move. An agent loops until the goal
           is met. You set the goal and judge the result.", inside the 118.23-118.83 / 131.04-131.57 silences).
           Audio only, under our loop board. Gain -0.2 dB (-15.4 vs -15.6).
  CUT 1    roll 2 139.25-142.50: "To prevent this, apply one rule to your workflow." (in 138.98-139.56 and
           142.28-142.75). Joined gap ~0.52 s.
  No pauses added.

Pictures (roll 2 source frames; R1 = rise-of-agents-1; corner mark cleaned on every Notebook frame):
  0-559       A Chatbot Answers. An Agent Acts. (canonical rise-of-agents-gps.jpg; the faceless upload variant never
              ships). Compact; GPS column on "Think of a chatbot as a GPS", self-driving column on "An agent is".
  737-1521    Ask a Chatbot versus Hire an Agent (canonical, dense, per-card camera). Arrives at the scenario (24.57),
              replacing Notebook's render and its "Human Domain & Authority" restatement (42.43-50.70). Broken
              31.30-35.60 by R1's phone full of clips (drawn for the same clips beat) and returning 1.0 s before
              "Hire an agent". One leg; the resume addresses it with video_from.
  2026-2648   What an Agent Does (canonical, compact) carrying graft A: Goal, Plan, Act, Check, the go-again loop,
              then the gold banner on "An agent loops". ~29 s with no break: no roll drew anything for this beat.
  2912-3164   Rogue Agents (canonical) unmarked under the rogue-agents setup.
  3562-4038   Rogue Agents again, replacing Notebook's FATAL ERROR card and its board render: PocketOS card on
              "The agent later explained", Gemini card on "In 2025".
  4275-4413   R1 "Ready to Publish / Review & Approve" drawing covers the keyboard tail and the "AUTONOMOUS SAFETY
              POLICY" slide, under the rule.
  4721-       canonical close in place of Notebook's close card and the Gemini Notebook outro.
Kept and flagged: 0:50-1:07 LLM and "Standard Chatbot / Autonomous Agent" diagrams (banned word on screen);
1:45-1:58 Notebook's PocketOS diagram (invented "403 PERMISSION DENIED" and "rm -rf /data /backups").
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, NEUTRAL, PURPLE, BLUE, TEAL, GREEN

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "Prompts"
SRC, R1 = P / "rise-of-agents-2.mp4", P / "rise-of-agents-1.mp4"
OUT = ROOT / "video-audit/rise-of-agents-v2-2026-09-24/build"
DEST = P / "rise-of-agents-v2.mp4"
A_ = ROOT / "course-assets/rise-of-agents"
GPS, COMPARE, LOOP, ROGUE, CLOSE = (A_ / f"rise-of-agents-{k}.jpg" for k in ("gps", "chatbot-vs-agent", "agent-loop", "rogue", "close"))
LESSON = ROOT / "lessons/rise-of-agents.md"

HEAD_END = fr(6.10)                     # R1 0.00-6.10 (graft B)
GPS_OUT = 559                           # 18.63 roll's cut to the Completed Tasks drawing
CMP_IN, CMP_OUT = 737, 1521             # 24.57 scenario board render -> 50.70 LLM diagram
CMP_BRK_IN, CMP_BRK_OUT = fr(31.30), fr(35.60)
R1_PHONE = 1200                         # R1 40.00-44.73 phone full of clips drawing
LOOP_IN = 2026                          # 67.53
GA, GB = fr(83.80), fr(87.95)           # roll 2 span replaced by graft A
R1A, R1B = fr(118.60), fr(131.25)       # roll 1 donor span
LOOP_SRC_OUT = 2648                     # 88.27 roll's cut to HUMAN OVERSIGHT (its 87.40-88.27 is a board render)
ROGUE_A = (2912, 3164)                  # 97.07-105.47
ROGUE_B = (3562, 4038)                  # 118.73 (FATAL ERROR) -> 134.60 WARNING drawing
CUT_A, CUT_B = fr(139.25), fr(142.50)   # cut 1
POLICY_OUT = 4413                       # 147.10 eye-key drawing
R1_PUBLISH = 6160                       # R1 3:25.33 Ready to Publish drawing
CLOSE_IN, CLOSE_END = 4721, fr(163.00)  # 157.37 Notebook close card; "better." ends 162.60

# Leg coordinates (source-frame units along each leg).
CMP_LEG_END = CMP_BRK_IN + (CMP_OUT - CMP_BRK_OUT)
LOOP_RESUME = GA + (R1B - R1A)
LOOP_LEG_END = LOOP_RESUME + (LOOP_SRC_OUT - GB)
def cmp_leg(t): return t - (CMP_BRK_OUT - CMP_BRK_IN) / FPS          # roll 2 seconds after the break -> leg seconds
def loop_r1(t): return (GA + fr(t) - R1A) / FPS                     # roll 1 seconds inside graft A -> leg seconds

# Card rects in each canonical JPG's own pixels (measured 2026-09-24 from the unmarked assets).
GPS_COLS = [[35, 109, 704, 1078], [704, 109, 1372, 1078]]           # columns sharing one photo strip + white text box
CMP_SCEN, CMP_CHAT, CMP_AGENT = [41, 112, 1560, 254], [41, 286, 784, 1354], [817, 286, 1560, 1354]
LOOP_COLS = [[40, 127, 420, 763], [420, 127, 800, 763], [800, 127, 1180, 763], [1180, 127, 1561, 763]]  # one shared white box
LOOP_ARROW = [592, 614, 1390, 736]
ROGUE_CARDS = [[41, 127, 784, 902], [817, 127, 1560, 902]]


def T(label, at, rect, color, **kw):
    return dict(label=label, at=at, rects=[rect], color=color, **kw)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[R1, GPS, COMPARE, LOOP, ROGUE, CLOSE, LESSON, ROOT / "index.html", A_ / "rise-of-agents.mp4"])
    b.load_audio([(2.92, 3.48), (9.05, 9.59), (18.18, 18.70), (36.00, 36.54), (75.14, 75.64), (77.73, 78.30), (80.63, 81.18),
                  (83.55, 84.02), (87.72, 88.32), (138.98, 139.56), (142.28, 142.75), (156.73, 157.37), (162.63, 166.02)])

    b.graft(R1, 0, HEAD_END, 'Graft B: roll 1 "What exactly is an AI agent? To figure that out, let\'s start with a familiar comparison." over its AI AGENT drawing',
            "r1-head", cover_intro=False, gain_db=-0.7)
    b.keep(0, GPS_OUT, "A Chatbot Answers. An Agent Acts. (canonical): the line, GPS, self-driving, you may not catch mistakes", "gps")
    b.keep(GPS_OUT, CMP_IN, "Notebook: dashboard / completed tasks (agents do the work)")
    b.keep(CMP_IN, CMP_BRK_IN, "Ask a Chatbot versus Hire an Agent (canonical): scenario, Ask a Chatbot", "compare")
    b.keep(CMP_BRK_IN, CMP_BRK_OUT, "BREAK (8b): R1 phone full of clips under 'reviewing clips, trimming, and assembling'",
           video_from=R1_PHONE, video_src=R1, video_end=1342)
    b.keep(CMP_BRK_OUT, CMP_OUT, "Ask a Chatbot versus Hire an Agent: Hire an Agent, you still own (leg frames from the break point)", "compare", video_from=CMP_BRK_IN)
    b.keep(CMP_OUT, LOOP_IN, "Notebook: LLM core, ChatGPT/agents share it, chatbot stops vs agent loops (flag: 'Autonomous' labels)")
    b.keep(LOOP_IN, GA, "What an Agent Does (canonical): intro, Goal, Plan, Act, Check", "loop")
    b.graft(R1, R1A, R1B, 'Graft A: roll 1 "Not done? Go again. ... An agent loops until the goal is met. You set the goal and judge the result." under our loop board',
            "r1-loop", picture_from=GA, gain_db=-0.2, visual="loop")
    b.keep(GB, LOOP_SRC_OUT, "What an Agent Does: banner held into the responsibility line", "loop", video_from=LOOP_RESUME)
    b.keep(LOOP_SRC_OUT, ROGUE_A[0], "Notebook: HUMAN OVERSIGHT REQUIRED (responsibility line, good but not perfect)")
    b.keep(*ROGUE_A, "Rogue Agents (canonical), unmarked under the rogue-agents setup", "rogue-a")
    b.keep(ROGUE_A[1], ROGUE_B[0], "Notebook: PocketOS diagram (flag: invented 403 / rm -rf labels)")
    b.keep(*ROGUE_B, "Rogue Agents (canonical) replaces FATAL ERROR and the board render: PocketOS quotation, Gemini", "rogue-b")
    b.keep(ROGUE_B[1], CUT_A, "Notebook: WARNING goal poorly defined")
    b.keep(CUT_B, POLICY_OUT, "R1 Ready to Publish / Review & Approve drawing covers the keyboard tail and the AUTONOMOUS SAFETY POLICY slide, under the rule",
           video_from=R1_PUBLISH, video_src=R1, video_end=6491)
    b.keep(POLICY_OUT, CLOSE_IN, "Notebook: eye key, simple chat vs complex dashboard (rule of thumb)")
    b.mark_close_start()
    b.keep(CLOSE_IN, CLOSE_END, "Canonical close replaces Notebook's close card and outro: the two closing lines")
    b.pause(120, "Settled close hold")
    b.finish_audio()

    b.board("gps", GPS, 0, GPS_OUT, "compact", [
        T("GPS Is Like ChatGPT: 'Think of a chatbot as a GPS.'", 3.50, GPS_COLS[0], PURPLE),
        T("Self-Driving Is Like an Agent: 'An agent is a self-driving car.'", 9.58, GPS_COLS[1], BLUE)])
    b.board("compare", COMPARE, CMP_IN, CMP_LEG_END, "dense", [
        T("The scenario: 'Say you scored 30 points...'", 24.68, CMP_SCEN, PURPLE, cam=CMP_SCEN),
        T("Ask a Chatbot: 'Ask a regular chatbot...'", 28.58, CMP_CHAT, PURPLE, cam=CMP_CHAT),
        T("Hire an Agent: 'Hire an agent...' through 'You still own...'", cmp_leg(36.62), CMP_AGENT, BLUE, cam=CMP_AGENT)],
        min_open=0, per_target_camera=True)
    b.board("loop", LOOP, LOOP_IN, LOOP_LEG_END, "compact", [
        T("1 Goal", 71.08, LOOP_COLS[0], PURPLE), T("2 Plan", 74.00, LOOP_COLS[1], BLUE),
        T("3 Act", 78.40, LOOP_COLS[2], TEAL), T("4 Check", 81.10, LOOP_COLS[3], GREEN),
        T("Not done? Go again. (graft A)", loop_r1(118.78), LOOP_ARROW, NEUTRAL)],
        banner_at=loop_r1(126.32))
    b.board("rogue-a", ROGUE, *ROGUE_A, "compact", [])
    b.board("rogue-b", ROGUE, *ROGUE_B, "compact", [
        T("April 2026 PocketOS: 'The agent later explained, I violated every principle I was given.'", 118.78, ROGUE_CARDS[0], PURPLE),
        T("2025 Gemini: 'In 2025, a Google Gemini agent...'", 123.36, ROGUE_CARDS[1], BLUE)], min_open=0)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("agents")
    s = lambda f: round(f / FPS, 2)
    b.manifest({
        "scope_detail": "Full production pass on rise-of-agents-2 (David's approval 2026-09-24): graft B (roll 1 hook) at the head, graft A (roll 1 go-again + loop banner) under the loop board, cut 1 (the 'workflow' sentence), canonical boards, one comparison-board break, the safety-policy slide covered, standard close.",
        "narration_changes": {
            "graft_b_head": {"source": str(R1.relative_to(ROOT)), "source_seconds": [0.0, s(HEAD_END)], "gain_db": -0.7,
                             "text": "What exactly is an AI agent? To figure that out, let's start with a familiar comparison."},
            "graft_a_loop": {"replaced_roll2_seconds": [s(GA), s(GB)], "replaced_text": "Not done? Go again. It loops until the goal is met.",
                             "source": str(R1.relative_to(ROOT)), "source_seconds": [s(R1A), s(R1B)], "gain_db": -0.2,
                             "text": "Not done? Go again. The AI feeds its own evaluation right back into the planning stage to figure out its next move. An agent loops until the goal is met. You set the goal and judge the result."},
            "cut_1": {"source_seconds": [s(CUT_A), s(CUT_B)], "text": "To prevent this, apply one rule to your workflow."},
            "not_taken": "optional cut 2 ('and it's autonomous')", "added_teaching_pauses": []},
        "photographs_covered": [],
        "picture_replacements": [
            {"source_frames": [CUT_B, POLICY_OUT], "what": "keyboard tail + 'AUTONOMOUS SAFETY POLICY' slide", "cover": "R1 frames 6160-6298, Ready to Publish / Review & Approve drawing"},
            {"source_frames": [3562, 3699], "what": "Notebook FATAL ERROR card", "cover": "canonical Rogue Agents board (PocketOS quotation)"},
            {"source_frames": [1273, 1521], "what": "Notebook 'Human Domain & Authority' restatement of the comparison board", "cover": "canonical comparison board"}],
        "board_breaks": [{"board": "compare", "source_frames": [CMP_BRK_IN, CMP_BRK_OUT], "drawing": "R1 frames 1200-1329, phone full of clips"}],
        "longest_board_runs_seconds": {"gps": s(GPS_OUT), "compare_before_break": s(CMP_BRK_IN - CMP_IN), "compare_after_break": s(CMP_OUT - CMP_BRK_OUT),
                                       "loop": s(LOOP_LEG_END - LOOP_IN), "rogue_a": s(ROGUE_A[1] - ROGUE_A[0]), "rogue_b": s(ROGUE_B[1] - ROGUE_B[0])},
        "kept_notebook_flags": ["0:50-1:07 source: LLM / 'Autonomous Agents' / 'Standard Chatbot vs Autonomous Agent' diagrams (banned word on screen)",
                                "1:45-1:58 source: PocketOS diagram with invented '403 PERMISSION DENIED' and 'rm -rf /data /backups' labels",
                                "What an Agent Does runs ~29 s unbroken: no roll drew anything for the loop beat"],
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:50]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()

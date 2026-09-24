#!/usr/bin/env python3
"""Big Downside v2 review candidate: roll 3 as the base, with audio from roll 4 and roll 1. Review only.

Plan: video-audit/big-downside-review-2026-09-24/REVIEW.md (BEST-OF PLAN), approved by David 2026-09-24
("Build it please"). Board treatment: the 1b plan in video-audit/big-downside-review-2026-09-23/REVIEW.md.
All grafts G1-G6 are carried, including the optional G5 (Anthropic's CEO) and the conditional G6 ("career").
No added pauses. All times below are SOURCE seconds of the named roll; every join sits in a measured silence
(10 ms RMS < 0.0015) on both sides.

  base   big-downside-3.mp4
  G3     roll 1  46.68-54.90   "While researchers can trace some internal features, ... one specific answer over another."
                               inserted at roll 3 24.65 (after "numerical patterns.")
  G3a    roll 3  35.68-38.33   cut: "Because we cannot trace those internal pathways,"
  G2     roll 1  84.87-94.10   "These include training the model to be helpful, monitoring the prompts users write, and limiting
                               what the product can do. But no layer catches everything."  replaces roll 3 60.60-62.70
  G1     roll 4 102.42-146.95  "Those challenges deal with future models. But the third idea applies right now, jailbreaking. ...
                               ... instead of their safety rules."  replaces roll 3 86.07-125.93, with two trims inside:
                               120.60-122.03 "As highlighted here,"   138.88-139.70 "As shown,"
  G6     roll 1 240.30-244.70  "If you give an AI a goal, it may find a route you never intended."  replaces roll 3 181.65-188.50
  G5     roll 1 330.33-339.22  "In 2026, over a thousand employees ..., including the CEO of Anthropic, signed ... Pacing the Frontier."
                               replaces roll 3 288.62-294.78
  G4     roll 4 313.40-319.75  "They asked the U.S. government to establish an international mechanism to slow automated AI
                               development."  replaces roll 3 294.78-300.20
Donor gain: rolls 1 and 4 measure -17.2 LUFS integrated against roll 3's -16.3, so both carry +0.9 dB.
"""
from pathlib import Path
import argparse, subprocess, sys
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, SPF, NEUTRAL, PURPLE, BLUE, TEAL, RED, readwav, sha, SR

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "Prompts"
SRC, R4, R1 = P / "big-downside-3.mp4", P / "big-downside-4.mp4", P / "big-downside-1.mp4"
OUT = ROOT / "video-audit/big-downside-v2-2026-09-24/build-v3"
DEST = P / "big-downside-v3.mp4"   # v3 (2026-09-24, David): G4 picture starts at roll 3's cut (294.98), not 294.78 - v2 flashed 6 frames of roll 3's Pacing the Frontier slide at 5:10.17
A = ROOT / "course-assets/big-downside"
GUARD, JAIL, PUPP = A / "big-downside-safety-guardrails.jpg", A / "big-downside-jailbreak.jpg", A / "big-downside-policy-puppetry.jpg"
VOICE, GOAL, TIME, CLOSE = A / "big-downside-voice-cloning.jpg", A / "big-downside-goal-test.jpg", A / "big-downside-safety-timeline.jpg", A / "big-downside-close.jpg"
LESSON = ROOT / "lessons/big-downside.md"
GAIN = 0.9

# ---- board rects, image px. Separate white cards: x from the illustration tiles, top 128, bottom = last near-white
# row above the drop shadow (Edit Spec 5). Shared white box (voice clone): full-height columns split midway between tiles.
G_CH, G_MA, G_SU = [41, 128, 524, 691], [558, 128, 1042, 691], [1076, 128, 1559, 691]
G_BANNER = [40, 732, 1560, 820]
J_BANNER = [34, 1014, 1352, 1090]
P_CARD, P_QUOTE = [40, 128, 1560, 468], [64, 328, 1536, 440]
V_COLS = [[40, 127, 420, 711], [420, 127, 800, 711], [800, 127, 1180, 711], [1180, 127, 1560, 711]]
T_CARS, T_AIR, T_PHONE, T_AI = [56, 144, 1544, 273], [56, 289, 1544, 427], [56, 443, 1544, 581], [56, 597, 1544, 726]
GL_A, GL_J, GL_S = [41, 128, 524, 773], [558, 128, 1042, 773], [1076, 128, 1559, 773]
GL_BANNER = [40, 814, 1560, 902]

F = fr


def target(label, at, rects, color):
    return {"label": label, "at": at, "rects": rects if isinstance(rects[0], list) else [rects], "color": color, "radius": 18}


def donor_run(b, src2, key, spans, label):
    """One donor passage cut into several audio spans (trims inside it), each carrying its own picture pieces.
    spans: [(a_in, a_out, [(p_in, p_out, kind, arg), ...]), ...] in donor frames; the pieces tile [a_in, a_out).
    kind 'own': the donor's own frames; 'hold': donor frame `arg` held; 'board': canonical board leg `arg`
    (declared in donor-frame coordinates)."""
    wav = b.out / f"graft-{key}.wav"
    if not wav.exists():
        subprocess.run([b.ff, "-y", "-v", "error", "-i", str(src2), "-vn", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(wav)], check=True)
    a2 = readwav(wav) * (10 ** (GAIN / 20)); r = np.linspace(0, 1, 240)
    for s, e, pieces in spans:
        data = a2[s * SPF:e * SPF].copy(); bed = b.tone(len(data))
        data[:240] = data[:240] * r + bed[:240] * (1 - r); data[-240:] = data[-240:] * (1 - r) + bed[-240:] * r
        assert pieces[0][0] == s and pieces[-1][1] == e and all(p[1] == q[0] for p, q in zip(pieces, pieces[1:])), (key, s, e)
        base = b.cursor
        for p0, p1, kind, arg in pieces:
            row = dict(kind="source", source_start=p0, source_end=p1, start_frame=base + p0 - s, end_frame=base + p1 - s,
                       label=f"{label} [{kind}{'' if arg is None else ' ' + str(arg)}]", graft_audio=str(src2), audio_start=s, audio_end=e)
            if kind == "board":
                row["visual"] = arg
            else:
                row.update(visual="source", video_src=str(src2), video_start=p0 if kind == "own" else arg)
                if kind == "hold": row["video_end"] = arg + 1
            b.rows.append(row)
        b.parts.append(data); b.cursor += e - s
    b.grafts[key] = dict(key=key, source=str(src2), sha256=sha(src2), audio_spans=[[s, e] for s, e, _ in spans], gain_db=GAIN,
                         audio_only=True, picture="per-piece rows (donor drawings via video_src, canonical boards via legs)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare-only", action="store_true")
    args = ap.parse_args()

    b = Build(ROOT, SRC, OUT, DEST, protected=[R4, R1, GUARD, JAIL, PUPP, VOICE, GOAL, TIME, CLOSE, LESSON, ROOT / "index.html",
                                              A / "big-downside.mp4"])
    b.load_audio([(20.18, 20.51), (24.50, 24.87), (35.46, 35.90), (41.55, 42.03), (85.88, 86.27), (90.76, 91.12),
                  (91.95, 92.32), (129.30, 129.69), (181.38, 181.92), (294.68, 294.89), (300.08, 300.35), (302.13, 302.42)])

    # ---------------- timeline (output order)
    b.keep(0, F(24.65), "Roll 3: iPhone hook, 'six ideas', 'The first idea is the black box', learned patterns")
    b.graft(R1, F(46.68), F(54.90), "G3 roll 1: 'While researchers can trace some internal features...' under roll 1's isolated-feature network", "g3", cover_intro=False, gain_db=GAIN)
    b.keep(F(24.65), F(35.68), "Roll 3: the Spot example")
    # G3a: 35.68-38.33 'Because we cannot trace those internal pathways,' cut
    b.keep(F(38.33), F(60.60), "Roll 3: 'Fixing an AI is much harder...', repair manual, second idea, block/redirect/limit")
    b.graft(R1, F(84.87), F(94.10), "G2 roll 1: the three kinds of guardrail + 'But no layer catches everything.' under roll 1's Layered Defense", "g2", cover_intro=False, gain_db=GAIN)
    b.keep(F(62.70), F(65.08), "Roll 3: 'This chart shows the challenge...' over roll 3's unused guardrail-pipeline frames (60.60-62.75)",
           video_from=F(60.60), video_src=SRC, video_end=F(62.75))
    b.keep(F(65.08), F(86.07), "The Guardrail Challenge Gets Harder (canonical): three cards, then the banner", "guardrails")
    donor_run(b, R4, "g1", [
        (F(102.42), F(120.60), [(F(102.42), F(102.60), "hold", F(102.60)),
                                (F(102.60), F(115.60), "own", None),
                                (F(115.60), F(120.60), "board", "jailbreak")]),
        (F(122.03), F(138.88), [(F(122.03), F(127.53), "board", "jailbreak"),
                                (F(127.53), F(138.88), "board", "puppetry")]),
        (F(139.70), F(146.95), [(F(139.70), F(146.95), "board", "puppetry")]),
    ], "G1 roll 4: third idea, jailbreaking, sign lines, cat-and-mouse, Policy Puppetry")
    b.keep(F(125.93), F(146.67), "Roll 3: IV, fourth idea, bad actors, 'This graphic shows a targeted scam in action.'")
    b.keep(F(146.67), F(170.43), "How the Voice-Clone Scam Works (canonical): four steps", "voice")
    b.keep(F(170.43), F(181.65), "Roll 3: 'As AI gets more powerful...', V, fifth idea")
    n6 = F(244.70) - F(240.30)
    b.graft(R1, F(240.30), F(244.70), "G6 roll 1: 'If you give an AI a goal, it may find a route you never intended.' over roll 3's goal diagram", "g6",
            picture_from=F(188.50) - n6, gain_db=GAIN)
    b.keep(F(188.50), F(188.77), "Roll 3: goal diagram, end")
    b.keep(F(188.77), F(196.20), "Roll 3: July 2026 setup over roll 4's TEST SANDBOX / JULY 2026 CASE STUDY drawing", video_from=F(207.30), video_src=R4)
    b.keep(F(196.20), F(207.50), "A Test Became a Real Cyberattack (canonical): Assignment, Agents Joined Forces", "goal")
    b.keep(F(207.50), F(212.10), "Break: roll 1's RESTRICTED SANDBOX / 1,200 AI AGENTS ACTIVE drawing under 'About 1,200 of them...'", video_from=F(246.30), video_src=R1)
    b.keep(F(212.10), F(228.47), "Board 5 again: Attack Spread, then the banner", "goal")
    b.keep(F(228.47), F(238.63), "Roll 3: audit-log drawing under the altered-records line, VI, sixth idea")
    b.keep(F(238.63), F(245.20), "COVERS THE 1908 CAR PHOTOGRAPH: roll 1's AI SAFETY vs CAPABILITY FRONTIER drawing", video_from=F(316.60), video_src=R1, video_end=F(322.70))
    b.keep(F(245.20), F(265.53), "Technology First. Safety Later. (canonical): four rows", "timeline")
    b.keep(F(265.53), F(288.62), "Roll 3: speed chart, red teams, 'But even the industry recognizes the limits of this approach.'")
    b.graft(R1, F(330.33), F(339.22), "G5 roll 1: 'In 2026, ... including the CEO of Anthropic, signed ... Pacing the Frontier.' under roll 1's signed statement", "g5", cover_intro=True, gain_db=GAIN)
    b.graft(R4, F(313.40), F(319.75), "G4 roll 4: 'They asked the U.S. government to establish an international mechanism...' over roll 3's Pacing the Frontier -> U.S. Government diagram", "g4",
            picture_from=F(294.98), video_end=F(300.20), gain_db=GAIN)
    b.keep(F(300.20), F(311.63), "Roll 3: 'Their warning was explicit.' + the quotation")
    b.close(F(311.63), F(318.00))
    b.finish_audio()

    # ---------------- boards
    b.board("guardrails", GUARD, F(65.08), F(86.07), "compact", [
        target("If AI Changes Itself: 'If AI changes itself, guardrails must keep up...'", 68.08, G_CH, PURPLE),
        target("If AI Matches People: 'If AI matches people, it might easily find gaps...'", 72.70, G_MA, BLUE),
        target("If AI Surpasses People: 'And if AI surpasses people...'", 77.18, G_SU, RED),
    ], banner_at=83.68, banner=G_BANNER)
    b.board("jailbreak", JAIL, F(115.60), F(127.53), "compact", [], banner_at=122.20, banner=J_BANNER, push=False)   # roll-4 coordinates; trim inside
    b.board("puppetry", PUPP, F(127.53), F(146.95), "compact", [
        target("Policy Puppetry card: 'In 2025, security firm Hidden Layer reported...'", 130.42, P_CARD, PURPLE),
        target("Quote block: '...prompts that looked like official instructions from AI developers'", 135.26, P_QUOTE, PURPLE),
    ], push=False)   # roll-4 coordinates; trim inside
    b.board("voice", VOICE, F(146.67), F(170.43), "compact", [
        target("Voice Clip: 'Step 1. A scammer pulls a short voice clip...'", 149.84, V_COLS[0], PURPLE),
        target("Voice Cloned: 'Step 2. They use an AI tool to clone that voice...'", 153.64, V_COLS[1], BLUE),
        target("Fake Call: 'Then comes step 3, the fake call.'", 160.12, V_COLS[2], RED),
        target("Call Back: 'The only defense is step 4, hang up...'", 165.44, V_COLS[3], TEAL),
    ])
    b.board("goal", GOAL, F(196.20), F(228.47), "compact", [
        target("Assignment: 'The assignment was strictly defined...'", 199.06, GL_A, PURPLE),
        target("Agents Joined Forces: 'But the agents found a different path. About 1,200...'", 204.24, GL_J, BLUE),
        target("Attack Spread: 'Then the attacks spread. About 700 agents...'", 213.08, GL_S, RED),
    ], banner_at=223.84, banner=GL_BANNER)
    b.board("timeline", TIME, F(245.20), F(265.53), "compact", [
        target("Cars row: 'It took 60 years from mass-market cars in 1908...'", 247.60, T_CARS, PURPLE),
        target("Airplanes row: 'For airplanes, federal flight rules took 23 years.'", 253.20, T_AIR, PURPLE),
        target("Smartphones row: 'Even today, the gap remains. It took 11 years...'", 256.60, T_PHONE, PURPLE),
        target("AI row: 'But for AI, rules are still evolving.'", 262.82, T_AI, PURPLE),
    ])

    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close("bigdownside")
    b.manifest({
        "scope_detail": "Full production pass on roll 3 with best-of grafts from rolls 4 and 1; review only; live unchanged",
        "plan": "video-audit/big-downside-review-2026-09-24/REVIEW.md BEST-OF PLAN (G1-G6, optional G5 and conditional G6 both carried); board treatment from the 2026-09-23 1b plan",
        "grafts_words": {
            "g3": "While researchers can trace some internal features, they still cannot fully explain why a model produces one specific answer over another.",
            "g2": "These include training the model to be helpful, monitoring the prompts users write, and limiting what the product can do. But no layer catches everything.",
            "g1": "Those challenges deal with future models. But the third idea applies right now, jailbreaking. Bad actors deliberately write complex prompts designed specifically to bypass a model's safety monitors. This is called jailbreaking. Defenders must protect many paths. An attacker needs only one opening. [As highlighted here, - cut] New methods keep surfacing, making this an ongoing game of cat and mouse. Here is an example, policy puppetry. In 2025, security firm Hidden Layer reported attackers crafted prompts that looked like official instructions from AI developers. [As shown, - cut] Major models like Claude, ChatGPT, and Gemini followed those fake instructions instead of their safety rules.",
            "g6": "If you give an AI a goal, it may find a route you never intended.",
            "g5": "In 2026, over a thousand employees at major AI companies, including the CEO of Anthropic, signed a statement called Pacing the Frontier.",
            "g4": "They asked the U.S. government to establish an international mechanism to slow automated AI development.",
        },
        "roll3_cuts": {"g3a": [35.68, 38.33], "replaced_by_g2": [60.60, 62.70], "replaced_by_g1": [86.07, 125.93],
                       "replaced_by_g6": [181.65, 188.50], "replaced_by_g5_g4": [288.62, 300.20]},
        "photographs_covered": [{"source_seconds": [238.63, 245.20], "what": "1908 touring car with two people", "cover": "roll 1 316.60-322.70, AI SAFETY vs CAPABILITY FRONTIER drawing"}],
        "donor_drawings": [
            "roll 1 46.68-54.90 isolated-feature network (G3's own picture)", "roll 1 84.87-94.10 Layered Defense rings (G2's own picture)",
            "roll 4 102.60-115.60 III + padlock, adversary/safety-monitor diagram (G1's own picture)",
            "roll 4 207.30-214.73 TEST SANDBOX / JULY 2026 CASE STUDY under the goal-test setup",
            "roll 1 246.30-250.90 RESTRICTED SANDBOX 1,200 AI AGENTS ACTIVE, break inside the goal-test board",
            "roll 1 316.60-322.70 AI SAFETY vs CAPABILITY FRONTIER, photo cover", "roll 1 330.73-339.22 signed statement (G5's own picture)"],
        "kept_notebook_flags": [
            "roll 3 170.43-174.67 hooded figure at monitors (drawn, faceless) under 'As AI gets more powerful...'",
            "roll 3 276.73-285.70 drawn silhouettes at server racks (red teams); 285.70-288.73 drawn man, head in hands",
            "roll 3 4:48-ish 'AI OUTPACES REGULATION SPEED' chart has unlabeled axis numbers (0-160) - no claimed statistic",
        ],
        "breaks": "Goal-test board broken once (roll 1 sandbox drawing). Guardrail board (21.0 s) and voice-clone board (23.8 s) run unbroken: no roll drew anything for those steps that is not a restatement of the board.",
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    print("boundaries:", [(r["start_frame"], r["label"][:60]) for r in b.rows])
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()

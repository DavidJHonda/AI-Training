#!/usr/bin/env python3
"""Work Changes v2 review candidate from work-changes-4 (2026-09-24). Review only.

v2 (David, 2026-09-24, on v1): fix the graphic flash at 0:13 (0.6 s of roll 4's coffee-and-tablet drawing between the
roll 2 graft and the Two Pillars diagram), and highlight Your First Assignment section by section as spoken, the way
the live video does (dense: header, first pass, then you / you start here, result, each with a camera dive). Its
breaks move so every section is on screen while spoken. Narration unchanged from v1.


Roll 4 is the base (video-audit/work-changes-review-2026-09-24/REVIEW.md). David's "yes, build it" 2026-09-24
approved three grafts and three cuts, waiving three near-verbatim lines no roll speaks exactly ("The answer is what
you already know.", the focus line, the learn line). No pauses added.

Narration (roll 4 word stamps, faster-whisper medium.en; silences at -45 dBFS, 50 ms windows):
  GRAFT 1  roll 2 4.00-12.65 "Familiar job titles like entrepreneur, teacher, lawyer, or designer will still exist, but
           the daily reality of those roles is already changing." replaces roll 4 4.00-14.35 (no entrepreneur, "will
           remain exactly the same"). Silences r4 3.75-4.45 / 14.35-15.15, r2 3.65-4.15 / 12.65-13.10. -0.4 dB.
  GRAFT 2  roll 1 200.45-207.20 "In one study, consultants finished certain tasks 25% faster, achieving 40% higher
           quality." replaces roll 4 252.45-258.50 ("One study showed consultants finishing tasks 25% faster with higher
           quality."). Silences r4 252.45-252.95 / 257.60-258.55, r1 200.45-200.65 / 207.20-207.50. Roll 1 runs
           5.1 LU hot (-14.7 vs -19.8 LUFS on these sentences): -5.3 dB.
  GRAFT 3  roll 2 250.30-253.55 "AI can make you productive before it makes you knowledgeable." replaces roll 4
           283.00-287.10 ("The AI can make you highly productive before you are actually knowledgeable."). Silences
           r4 282.95-283.40 / 287.10-287.95, r2 250.30-250.65 / 253.55-253.90. -0.5 dB.
  CUT 1    225.00-226.40 "Look at the bottom banner."
  CUT 2    310.10-319.80 "Because AI is permanently changing how tasks are executed, the sole responsibility for
           building foundational expertise falls entirely on you. Look at this final message."
  END      after "Now it's on you to learn." (323.42): "Thank you." and the end card are dropped.

Pictures: canonical boards at their introductions; drawn people, a chapter card, and two invented charts covered with
people-free drawings from rolls 1-3 (R1/R2/R3), listed in the manifest. Boards over ~20 s broken with drawings where
one exists (rule 8b); Two Ways and What Changes run unbroken for lack of a fitting drawing.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import cv2
from editspec_build import Build, fr, FPS, SPF, NEUTRAL, PURPLE, BLUE, TEAL, AMBER, banner_rect, readwav, writewav

ROOT = Path(__file__).resolve().parents[2]
P = ROOT / "Prompts"
SRC, R1, R2, R3 = (P / f"work-changes-{k}.mp4" for k in (4, 1, 2, 3))
A_ = ROOT / "course-assets/work-changes"
OUT = ROOT / "video-audit/work-changes-v2-2026-09-24/build"
DEST = P / "work-changes-v2.mp4"
STRENGTHS, ASSIGN, TWOWAYS, CHANGES, CLOSE = (A_ / f"work-changes-{k}.jpg" for k in (
    "four-shapes-of-ai-work", "assignment", "automation-and-augmentation", "productivity-and-possibilities", "close"))
LESSON = ROOT / "lessons/work-changes.md"

# Canonical boards, measured 2026-09-24 (image px, xyxy).
S_CARDS = [[41, 128, 784, 676], [817, 128, 1560, 676], [41, 709, 784, 1257], [817, 709, 1560, 1257]]   # 1600x1297
A_QUOTE = [31, 85, 1170, 220]                                                                          # 1203x1308
# Assignment sections, from the text bands (column cards x 31-587 / 613-1170; section rings 16 px inside the card).
B_HEAD, B_PASS, B_THEN, B_RES = [31, 246, 587, 738], [47, 746, 571, 952], [47, 961, 571, 1106], [47, 1145, 571, 1258]
W_HEAD, W_PASS, W_START, W_RES = [613, 246, 1170, 738], [629, 746, 1154, 953], [629, 961, 1154, 1137], [629, 1146, 1154, 1258]
CTX = 110   # camera keeps this much of the neighbouring stage/column either side, like the live video's framing
T_CARDS = [[41, 128, 784, 717], [817, 128, 1560, 717]]                                                 # 1600x885
C_CARDS = [[41, 128, 525, 692], [558, 128, 1043, 692], [1076, 128, 1560, 692]]                         # 1600x732


def target(label, at, rect, color, cam=False, radius=18):
    t = {"label": label, "at": at, "rects": [rect], "color": color, "radius": radius}
    if cam is True: t["cam"] = rect
    elif cam: t["cam"] = cam
    return t


def ctx(r):
    return [r[0] - CTX, r[1], r[2] + CTX, r[3]]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[R1, R2, R3, STRENGTHS, ASSIGN, TWOWAYS, CHANGES, CLOSE, LESSON, ROOT / "index.html"])
    b.load_audio([(3.75, 4.45), (14.35, 15.15), (224.55, 225.0), (225.9, 226.4), (257.6, 258.55), (282.95, 283.4),
                  (287.1, 287.95), (318.0, 318.55), (319.65, 320.1), (323.45, 326.8)])

    # --- opening
    b.keep(0, 120, "COVER (drawn graduate): R2 graduation gown and laptop", video_from=0, video_src=R2, video_end=120)
    b.graft(R2, 120, 380, "GRAFT roll 2: 'Familiar job titles like entrepreneur, teacher, lawyer, or designer will still exist, but the daily reality of those roles is already changing.'",
            "open", cover_intro=False, gain_db=-0.4)
    # roll 4 120-430 (job titles with drawn teacher, lawyer, designer) replaced by graft 1
    b.keep(430, 680, "Notebook: Two Pillars diagram from its first frame ('review two foundational concepts'); v2 drops the 0.6 s coffee-and-tablet flash",
           video_from=450, video_end=680)
    b.keep(680, 768, "COVER (Notebook board render): R1 Targeted AI Integration cards under 'First, AI has specific areas where it thrives.'",
           video_from=579, video_src=R1, video_end=672)
    # --- board 1
    b.keep(768, 1479, "Four AI Strengths at Work (canonical): intro, Reshape, Explore, Find What Matters", "strengths")
    b.keep(1479, 1578, "BREAK: R1 paper stacks around a monitor under 'pulling key ideas and relevant details out of long documents'",
           video_from=1269, video_src=R1, video_end=1413)
    b.keep(1578, 1804, "Four AI Strengths at Work: Work Through Problems", "strengths")
    # --- what sets you apart (chapter card, drawn people, drawn hand, invented chart all covered)
    b.keep(1804, 2115, "COVER (chapter card, drawn office workers): R3 Professional Output Model, identical AI baselines",
           video_from=1575, video_src=R3, video_end=1740)
    b.keep(2115, 2310, "COVER (drawn hand editing): R3 Professional Output Model, human augmentation on top ('The answer is what you already know.')",
           video_from=1740, video_src=R3, video_end=1911)
    b.keep(2310, 2445, "COVER (drawn hand editing): R1 open books ('Your foundational human knowledge...')",
           video_from=1419, video_src=R1, video_end=1503)
    b.keep(2445, 2811, "COVER (invented '85% of timeline' chart): R3 Project Brief, 500 Reviews -> Root Problem -> Propose Fix",
           video_from=1965, video_src=R3, video_end=2208)
    # --- board 2
    b.keep(2811, 3390, "Your First Assignment (canonical): intro, the assignment, Before AI", "assignment")
    b.keep(3390, 3582, "BREAK: R1 review stacks and progress bar under 'You spend days manually reading and organizing those 500 reviews...'",
           video_from=3888, video_src=R1, video_end=4038)
    b.keep(3582, 3939, "Your First Assignment: first pass, then you, the result ('the result is predictable')", "assignment")
    b.keep(3939, 4041, "BREAK: R3 Week 1 findings / Week 2 deep rework under 'The boss adds a page of comments...'",
           video_from=2835, video_src=R3, video_end=3021)
    b.keep(4041, 4194, "Your First Assignment: With AI header", "assignment")
    b.keep(4194, 4353, "BREAK: R2 500 Raw Reviews -> AI Automation -> Structured Data under 'The AI completes that entire first pass in minutes.'",
           video_from=4575, video_src=R2, video_end=4674)
    b.keep(4353, 5096, "Your First Assignment: With AI header, AI does the first pass, you start here, the result", "assignment")
    b.keep(5096, 5847, "Notebook: AI automation / human augmentation diagrams, laptop and desk ('two specific terms')")
    # --- board 3
    b.keep(5847, 6750, "Two Ways AI Changes the Work (canonical): Automate, Augment", "twoways")
    # CUT 1 6750-6792 "Look at the bottom banner."
    b.keep(6792, 6904, "Two Ways AI Changes the Work: banner", "twoways")
    b.keep(6904, 7101, "COVER (drawn professional and robot faces): R2 Deliverable / AI assistant document",
           video_from=5910, video_src=R2, video_end=5997)
    b.keep(7101, 7230, "Notebook: hand signing the project report ('accountability ... on your shoulders')")
    # --- board 4
    b.keep(7230, 7574, "What Changes with AI (canonical): intro, More Kinds, More Productive", "changes")
    b.graft(R1, 6014, 6216, "GRAFT roll 1: 'In one study, consultants finished certain tasks 25% faster, achieving 40% higher quality.'",
            "study", picture_from=7574, visual="changes", gain_db=-5.3)
    # roll 4 7574-7755 (the misstated study line) replaced by graft 2. The graft is 21 frames longer, so the leg runs
    # 21 frames ahead from here: it is built to 7971 and the Meaningful Work ring is placed 21 frames late in leg time.
    b.keep(7755, 7950, "What Changes with AI: Meaningful Work", "changes", video_from=7776)
    # --- the part that matters (drawn people and an invented chart covered)
    b.keep(7950, 8019, "COVER (drawn man in empty room): roll 4's own spreadsheet and red pen ('This leads to a complicated situation.')",
           video_from=8151, video_end=8204)
    b.keep(8019, 8319, "COVER (drawn people): R2 Traditional Entry-Level Tasks (basic research, starter code, simple analysis)",
           video_from=6990, video_src=R2, video_end=7122)   # roll 2 fades to its next scene from 7124
    b.keep(8319, 8490, "COVER (invented Productivity Outpaces Knowledge chart): R2 AI-Driven Autonomous Pipeline ('Now, the AI handles a lot of that initial labor.')",
           video_from=7179, video_src=R2, video_end=7205)
    b.graft(R2, 7509, 7606, "GRAFT roll 2: 'AI can make you productive before it makes you knowledgeable.'",
            "productive", picture_from=8490, video_end=8491, gain_db=-0.5)
    b.rows[-1].update(video_src=str(R1), video_start=6609, video_end=6717)   # picture: R1 Role Anatomy Shift (validating AI output)
    # roll 4 8490-8613 (paraphrased line) replaced by graft 3
    b.keep(8613, 8874, "COVER (invented chart, drawn person with tablet): R1 Role Anatomy Shift, held ('asked to verify and approve...')",
           video_from=6609 + 97, video_src=R1, video_end=6717)
    b.keep(8874, 9008, "Notebook: structural beam check ('required to spot its errors')")
    b.keep(9008, 9303, "COVER (drawn student reading, drawn campus crowd): R1 desk lamp over open books ('relentless learning ... school')",
           video_from=6723, video_src=R1, video_end=6930)
    # CUT 2 9303-9594
    b.mark_close_start()
    b.keep(9594, 9711, "Canonical close replaces Notebook's close card: the two closing lines")
    b.pause(120, "Settled close hold")
    b.finish_audio()
    # keep() fades each row into and out of room tone over 5 ms. Where a picture swap splits one continuous source
    # sentence into two rows, that is a 10 ms dropout inside speech (v1 had ten, up to 12.9k sample units deep).
    # Restore the untouched source samples across every such audio-continuous boundary.
    edited = readwav(OUT / "edited.wav"); restored = []
    for prev, row in zip(b.rows, b.rows[1:]):
        if (prev.get("kind") == row.get("kind") == "source" and prev["source_end"] == row["source_start"]
                and not any(k in r for r in (prev, row) for k in ("graft_audio", "graft_source"))):
            o, so = row["start_frame"] * SPF, row["source_start"] * SPF
            edited[o - 240:o + 240] = b.audio[so - 240:so + 240]; restored.append(row["start_frame"])
    writewav(OUT / "edited.wav", edited)

    b.board("strengths", STRENGTHS, 768, 1804, "dense", [
        target("Reshape Your Material", 33.42, S_CARDS[0], BLUE, cam=True),
        target("Explore Possibilities", 38.92, S_CARDS[1], AMBER, cam=True),
        target("Find What Matters", 47.06, S_CARDS[2], PURPLE, cam=True),
        target("Work Through Problems", 53.78, S_CARDS[3], TEAL, cam=True),
    ])
    b.board("assignment", ASSIGN, 2811, 5096, "dense", [
        target("The assignment", 96.10, A_QUOTE, PURPLE, cam=True),
        target("Before AI", 104.54, B_HEAD, PURPLE, cam=ctx(B_HEAD)),
        target("You do the first pass", 113.08, B_PASS, PURPLE, cam=ctx(B_PASS)),
        target("Then you", 125.06, B_THEN, PURPLE, cam=ctx(B_THEN)),
        target("The result (before)", 129.54, B_RES, PURPLE, cam=ctx(B_RES)),
        target("With AI", 135.68, W_HEAD, AMBER, cam=ctx(W_HEAD)),
        target("AI does the first pass", 149.84, W_PASS, AMBER, cam=ctx(W_PASS)),
        target("You start here", 155.12, W_START, AMBER, cam=ctx(W_START)),
        target("The result (with AI)", 163.68, W_RES, AMBER, cam=ctx(W_RES)),
    ], per_target_camera=True)
    tb = banner_rect(cv2.imread(str(TWOWAYS)))
    b.board("twoways", TWOWAYS, 5847, 6904, "compact", [
        target("Automate", 198.70, T_CARDS[0], PURPLE),
        target("Augment", 208.80, T_CARDS[1], TEAL),
    ], banner_at=226.50, banner=tb, push=False)
    b.board("changes", CHANGES, 7230, 7971, "compact", [
        target("More Kinds", 246.56, C_CARDS[0], PURPLE),
        target("More Productive", 250.42, C_CARDS[1], BLUE),
        target("Meaningful Work", 258.62 + 21 / FPS, C_CARDS[2], TEAL),   # spoken at source 258.62; leg is 21 frames ahead
    ], push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("workchanges")
    s = lambda f: round(f / FPS, 2)
    b.manifest({
        "scope_detail": "Full production pass on work-changes-4 (David's 'yes, build it' 2026-09-24): three audio grafts (roll 2 job titles, roll 1 study line, roll 2 productive line), two cuts plus the tail, canonical boards, covers for drawn people, a chapter card and two invented charts, standard close.",
        "waived_lines": ["It's what you already know. (roll 4: 'The answer is what you already know.')",
                         "AI doesn't just help you work faster. It can help you focus on what's really important. (roll 4 paraphrase)",
                         "You already know what you must do. Learn. And learn more... school. (roll 4 paraphrase)"],
        "narration_changes": {
            "cuts": [{"source_frames": [a, c], "source_seconds": [s(a), s(c)], "text": t} for a, c, t in [
                (120, 430, "While familiar job titles like teacher, lawyer, or designer will remain exactly the same, the daily reality of the tasks you perform in those jobs is actively changing. (replaced by graft 1)"),
                (6750, 6792, "Look at the bottom banner."),
                (7574, 7755, "One study showed consultants finishing tasks 25% faster with higher quality. (replaced by graft 2)"),
                (8490, 8613, "The AI can make you highly productive before you are actually knowledgeable. (replaced by graft 3)"),
                (9303, 9594, "Because AI is permanently changing how tasks are executed, the sole responsibility for building foundational expertise falls entirely on you. Look at this final message."),
                (9711, 9806, "Thank you. (and the end card)")]],
            "grafts": [
                {"source": "Prompts/work-changes-2.mp4", "source_frames": [120, 380], "gain_db": -0.4, "text": "Familiar job titles like entrepreneur, teacher, lawyer, or designer will still exist, but the daily reality of those roles is already changing."},
                {"source": "Prompts/work-changes-1.mp4", "source_frames": [6014, 6216], "gain_db": -5.3, "text": "In one study, consultants finished certain tasks 25% faster, achieving 40% higher quality."},
                {"source": "Prompts/work-changes-2.mp4", "source_frames": [7509, 7606], "gain_db": -0.5, "text": "AI can make you productive before it makes you knowledgeable."}],
            "added_teaching_pauses": []},
        "board_breaks": [
            {"board": "strengths", "source_frames": [1479, 1578], "drawing": "R1 1269-1412 paper stacks around a monitor"},
            {"board": "assignment", "source_frames": [3390, 3582], "drawing": "R1 3888-4037 review stacks and progress bar"},
            {"board": "assignment", "source_frames": [3939, 4041], "drawing": "R3 2835-2936 Week 1 / Week 2 rework"},
            {"board": "assignment", "source_frames": [4194, 4353], "drawing": "R2 4575-4673 500 Raw Reviews -> AI Automation -> Structured Data, held"}],
        "unbroken_boards": {"twoways": "~30 s; no roll drew a people-free automate/augment scene",
                            "changes": "~24 s; no fitting drawing"},
        "audio_continuity_restored_at_output_frames": restored,
        "retained_notebook_art_with_figures": ["Two Pillars diagram (15.0-22.67) has a small portrait icon in its Human Expertise pillar",
                                               "hand signing 'Approved By A. Johnson' project report (236.70-241.0)"],
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()

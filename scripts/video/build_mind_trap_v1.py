#!/usr/bin/env python3
"""Build Mind Trap v1 from mind-trap-6 (2026-09-21 seven-way review: rolls 1-6 and the live video).

Full production pass, review only. Roll 6 carries the whole narration with no cuts; one approved
graft from roll 5 supplies the shared-text-versus-shared-experience sentence the lesson teaches and
roll 6 never speaks. The post-only comparison board walks its two cards and returns for the
definition (killing roll 6's chapter card); the canonical ELIZA board replaces Notebook's render
with card-hugging rings and a banner ring; the live video's ELIZA teletype drawing replaces roll 6's
archival mainframe photograph; standard close. Live video, raw rolls, lesson, and boards unchanged.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, FPS, PURPLE, BLUE, TEAL, AMBER, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/mind-trap-6.mp4"
DONOR = ROOT / "Prompts/mind-trap-5.mp4"
OUT = ROOT / "video-audit/mind-trap-comparison-2026-09-21/build-v1"
DEST = ROOT / "Prompts/mind-trap-v1.mp4"
A = ROOT / "course-assets/mind-trap"
COMPARE, ELIZA, CLOSE = A / "mind-trap-comparison.jpg", A / "mind-trap-eliza.jpg", A / "mind-trap-close.jpg"
LIVE, LESSON = A / "mind-trap.mp4", ROOT / "lessons/mind-trap.md"
OTHER_ROLLS = [ROOT / f"Prompts/mind-trap-{i}.mp4" for i in (1, 2, 3, 4, 5)]

# Roll-6 visual cuts (scenes.txt, frame-checked) and audio boundaries (ffmpeg silencedetect, -40 dB).
CMP_IN, CMP_OUT = 804, 2030      # 0:26.80 cut ("Think about making a significant life choice" 26.86); 1:07.67 cut to the tailored-advice diagram
DEF_IN, DEF_OUT = 2298, 2454     # 1:16.60 cut to the chapter card (never ships); 1:21.80 cut to the mainframe photograph
PHOTO_IN, PHOTO_OUT = 2454, 3160 # the archival photograph, replaced by the live video's ELIZA teletype
ELIZA_IN, ELIZA_OUT = 3374, 5008 # 1:52.47 render in ("Today's chatbots trigger this same illusion" 112.22); held 0.27 s past "human." (166.66) into the pause
GRAFT_IN, GRAFT_OUT = 4434, 4762 # roll 5: 147.80 (its own speech ends 147.75) to 158.73 ("lived alongside you." ends 158.64)
TAIL_IN, TAIL_OUT = 5008, 5023   # the rest of roll 6's post-takeaway pause, under roll 5's picture; 2:47.43 cut to the stakes slider
CLOSE_IN = 6645                  # 3:41.50, inside the quiet 221.38-221.75 before "For decisions that matter." (221.75)
CLOSE_AUDIO_OUT = 6735           # 3:44.50, after "call." (224.36); digital silence to the engine outro at 225.5
LIVE_ELIZA_IN, LIVE_ELIZA_OUT = 2354, 3020   # live video 1:18.47 cut to the ELIZA teletype; 1:40.67 cut to the paper-cut face

# Board geometry, measured from the assets (illustration tile x extent; last near-white row above the drop shadow).
CARD_L, CARD_R = (41, 783), (817, 1559)
CMP_Q = [41, 113, 1559, 238]                                    # the YOU question strip
CMP_CARD = lambda c: [c[0], 271, c[1], 1383]                    # complete card: photo tile top to the last white row
CMP_ROW = lambda c, y0, y1: [c[0] + 16, y0, c[1] - 16, y1]      # a stacked section, 16 px inside the card rails
KNOWS, NOTICES, STAKE = (1027, 1117), (1146, 1237), (1265, 1350)
ELIZA_CARD = lambda c: [c[0], 128, c[1], 675]
ELIZA_BANNER = [40, 716, 1560, 804]

def target(label, at, rect, color, radius=14):
    return {"label": label, "at": at, "rects": [rect], "color": color, "radius": radius}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true"); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, COMPARE, ELIZA, CLOSE, LESSON, *OTHER_ROLLS])
    b.load_audio([(0.00, 0.34), (6.00, 6.32), (12.69, 13.06), (17.58, 17.90), (22.91, 23.30), (26.31, 26.91), (30.79, 31.10),
                  (34.91, 35.29), (38.73, 39.15), (45.74, 46.06), (50.68, 51.05), (58.75, 59.27), (67.30, 67.82), (71.70, 72.08),
                  (76.15, 76.65), (81.14, 81.79), (83.53, 83.91), (89.02, 89.45), (95.37, 95.83), (98.96, 99.30), (104.82, 105.36),
                  (112.00, 112.47), (115.97, 116.31), (121.15, 121.48), (123.86, 124.51), (126.93, 127.38), (134.12, 134.72),
                  (139.07, 139.41), (143.83, 144.51), (147.36, 147.80), (153.22, 153.86), (157.11, 157.53), (161.65, 162.06),
                  (163.74, 164.13), (166.67, 167.42), (172.06, 172.64), (179.47, 179.92), (182.88, 183.38), (193.89, 194.30),
                  (200.82, 201.20), (213.35, 213.84), (221.38, 221.75), (223.05, 223.47)])

    b.keep(0, CMP_IN, "Notebook drawings: computational system vs human cognition, the college decision")
    b.keep(CMP_IN, CMP_OUT, "The Same Question. Different Answers.", "compare")
    b.keep(CMP_OUT, DEF_IN, "Notebook drawings: tailored advice, generic pattern broadcast")
    b.keep(DEF_IN, DEF_OUT, "The Same Question. Different Answers. (held under the definition)", "define")
    b.keep(PHOTO_IN, PHOTO_OUT, "ELIZA teletype drawing borrowed from the live video (replaces the archival photograph)",
           video_from=LIVE_ELIZA_IN, video_src=LIVE, video_end=LIVE_ELIZA_OUT)
    b.keep(PHOTO_OUT, ELIZA_IN, "Notebook drawing: projecting empathy onto a screen")
    b.keep(ELIZA_IN, ELIZA_OUT, "Why AI Feels Like Somebody", "eliza")
    b.graft(DONOR, GRAFT_IN, GRAFT_OUT, "Shared text is not shared experience (roll 5)", "sharedtext")
    b.keep(TAIL_IN, TAIL_OUT, "Roll 6's remaining post-takeaway pause, under roll 5's picture",
           video_from=GRAFT_OUT, video_src=DONOR)
    b.keep(TAIL_OUT, CLOSE_IN, "Notebook drawings: stakes slider, the middle move, prepare vs decide")
    b.mark_close_start()
    b.close(CLOSE_IN, CLOSE_AUDIO_OUT, tail=150)
    b.finish_audio()

    # Board 1 (1600x1424, faces, post-only): compact - every card line reads at full view, and both cards are
    # taller than a 16:9 dive can hold, so the camera stays still and the rings follow the spoken sections.
    b.board("compare", COMPARE, CMP_IN, CMP_OUT, "compact", [
        target("You: Should I choose Michigan or Indiana?", 31.02, CMP_Q, NEUTRAL, radius=18),
        target("Your Mom (whole card)", 35.14, CMP_CARD(CARD_L), BLUE, radius=20),
        target("Mom / Knows: your history", 39.10, CMP_ROW(CARD_L, *KNOWS), BLUE),
        target("Mom / Notices: how you act when you are stuck", 41.02, CMP_ROW(CARD_L, *NOTICES), BLUE),
        target("Mom / Stake: shares the outcome", 45.98, CMP_ROW(CARD_L, *STAKE), BLUE),
        target("The Chatbot (whole card)", 50.74, CMP_CARD(CARD_R), AMBER, radius=20),
        target("Chatbot / Sees: what you typed", 55.94, CMP_ROW(CARD_R, *KNOWS), AMBER),
        target("Chatbot / Matches: common patterns", 59.18, CMP_ROW(CARD_R, *NOTICES), AMBER),
        target("Chatbot / Stake: does not share the outcome", 63.46, CMP_ROW(CARD_R, *STAKE), AMBER),
    ], push=False)

    # The same board, unmarked, returned to under the spoken definition (76.58-81.12) in place of the chapter card.
    b.board("define", COMPARE, DEF_IN, DEF_OUT, "compact", [], push=False)

    # Board 2 (1600x844, two separate rounded cards on the stage): compact, rings hug each card's own edges.
    b.board("eliza", ELIZA, ELIZA_IN, ELIZA_OUT, "compact", [
        target("AI Sounds Like One", 124.94, ELIZA_CARD(CARD_L), PURPLE, radius=22),
        target("Your Brain Looks for a Person", 144.42, ELIZA_CARD(CARD_R), TEAL, radius=22),
    ], banner_at=164.13, banner=ELIZA_BANNER, push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("mindtrap")
    b.manifest({
        "scope_detail": "Full production review candidate from the 2026-09-21 seven-way review (roll 6 base, one approved roll-5 graft); live video, raw rolls, lesson, and boards unchanged.",
        "narration_changes": {
            "graft": "roll 5 147.80-158.73 -> after roll 6's takeaway line; no roll-6 words removed",
            "roll6_pause_split": "the 0.75 s pause after 'Sounding human does not make AI human.' is kept whole, split 0.27 s before the insert (under the board) and 0.50 s after it (under roll 5's picture)",
            "engine_outro_removed_from_frame": CLOSE_AUDIO_OUT,
        },
        "added_teaching_pauses": [],
        "board_render_covered": [
            {"frames": [ELIZA_IN, ELIZA_OUT], "replacement": "canonical Why AI Feels Like Somebody"},
            {"frames": [CLOSE_IN, CLOSE_AUDIO_OUT], "replacement": "standard close"},
        ],
        "post_only_board_inserted": {
            "asset": "course-assets/mind-trap/mind-trap-comparison.jpg",
            "frames": [[CMP_IN, CMP_OUT], [DEF_IN, DEF_OUT]],
            "over": "Notebook's college-decision drawing under the Mom/chatbot comparison, and its 'The Cognitive Illusion' chapter card under the definition",
        },
        "borrowed_picture": {
            "source": str(LIVE.relative_to(ROOT)), "source_frames": [LIVE_ELIZA_IN, LIVE_ELIZA_OUT],
            "output_over": [PHOTO_IN, PHOTO_OUT],
            "reason": "roll 6 ran a black-and-white archival photograph of a 1960s mainframe room, with an identifiable man, for 23.5 s under the ELIZA history",
            "hold": "the donor is 666 frames against 706; its last frame holds for the final 40 (1.33 s) under 'turn the user's own words back into questions'",
        },
        "notebook_interleaves": [],
        "longest_unbroken_board_run_seconds": round((ELIZA_OUT - ELIZA_IN) / FPS, 2),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()

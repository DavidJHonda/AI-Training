#!/usr/bin/env python3
"""Build How AI Answers v1 from roll 4, with four grafts and two cuts (David's approval 2026-09-22).

Roll 4 is the first of five files - rolls 1-4 and the live video - to clear the kit's hard requirements
at once: all eight required verbatim lines, all six percentages spoken at BOTH prediction beats, and
Rank, Pick, Add and Repeat all four named, with "pick" said correctly (roll 2 said "Step two is kick",
which no donor could fix). Roll 3 rewrites both closing lines; roll 1 is 0/8 and builds its explanation
on the prohibited always-highest framing; the live video is 2/8 and speaks none of the six percentages.

Six edits, every boundary measured on the waveform rather than taken off a decoder's word timings:

  A  "But once it understands the prompt" - `understands` is on the kit's banned list. Replaced with
     roll 2's "But then it faces a new problem.", which is the lesson's own sentence.
  B  cut  "This diagram shows four steps before the answer begins." - board furniture.
  C  "In this graphic, the final token is the question mark." - furniture, but it carries teaching, so
     it is replaced rather than cut, with roll 3's clean "In this prompt, the question mark is the final
     token." Donor and hole are both exactly 90 frames, so Board 2's leg stays 1:1 with source seconds.
  D  "To find the very first WORD" - the prompt says token, not word, after the setup. Replaced with
     roll 2's "It uses those numbers from the final token to calculate a probability score for every
     potential next token in its entire vocabulary."
  E  "The AI will select a top scoring token" (leans toward the always-highest claim the prompt forbids)
     AND "This chart breaks down the selection process step by step." (furniture). The two are adjacent
     and share a boundary, so one graft of roll 2's lesson-accurate "The AI selects a token, adds it to
     the growing reply, and then uses that newly expanded context to predict again." removes both.
  F  cut  "Let's look at this diagram to summarize exactly how it builds the answers step by step."

Roll 4 -16.5 LUFS, roll 2 -17.0, roll 3 -17.1 - all within 0.6 LU - with pause floors of -64.4, -65.9
and -67.2 dB, a 2.8 dB spread. This is the cleanest donor set in the series: Embeddings shipped with a
6.4 dB step and Engagement Trap rejected a donor at 17 dB. Boards 1-4 and the close are the canonical
page assets. Live video, rolls, lesson and boards unchanged.
"""
from pathlib import Path
import argparse, json, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, FPS, W, H, PURPLE, BLUE, TEAL, GREEN, AMBER, RED, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/how-ai-answers-4.mp4"      # spine
ROLL2 = ROOT / "Prompts/how-ai-answers-2.mp4"    # edits A, D and E
ROLL3 = ROOT / "Prompts/how-ai-answers-3.mp4"    # edit C
A = ROOT / "course-assets/how-ai-answers"
LIVE = A / "how-ai-answers.mp4"
AUDIT = ROOT / "video-audit/how-ai-answers-stitch-2026-09-22"
OUT = AUDIT / "build"
DEST = ROOT / "Prompts/how-ai-answers-v4.mp4"
BEGINS = A / "how-ai-answers-before-answer-begins.jpg"     # Board 1
WHERE = A / "how-ai-answers-where-answer-begins.jpg"       # Board 2
TOKENBY = A / "how-ai-answers-token-by-token.jpg"          # Board 3
BUILDING = A / "how-ai-answers-building-an-answer.jpg"     # Board 4
LESSON = ROOT / "lessons/how-ai-answers.md"

# ---------------------------------------------------------------- the six edits
# Every in/out point below was checked on the RMS trace of the file being cut, not on Whisper's word
# boundaries. That distinction cost a verbatim line on Embeddings: both silencedetect and Whisper put a
# word 0.15-0.22 s earlier than the waveform did. Quiet window found at each point is given in ms.
EA_IN, EA_OUT = 138, 258        # roll 4 0:04.60 (quiet 4.35-4.92, 570) - 0:08.60 (8.45-8.77, 320)
EA_DIN, EA_DOUT = 152, 215      # roll 2 0:05.05 (4.91-5.22, 310) - 0:07.15 (7.05-7.27, 220)
EB_IN, EB_OUT = 633, 744        # cut, roll 4 0:21.10 (20.84-21.44, 600) - 0:24.80 (24.55-25.06, 510)
EC_IN, EC_OUT = 1209, 1299      # roll 4 0:40.30 (40.07-40.52, 450) - 0:43.30 (43.16-43.47, 310)
EC_DIN, EC_DOUT = 1713, 1803    # roll 3 0:57.10 (56.88-57.39, 510) - 1:00.10 (59.99-60.24, 250)
ED_IN, ED_OUT = 1769, 2101      # roll 4 0:58.97 (58.71-59.21, 500) - 1:10.03 (69.99-70.09, 100)
ED_DIN, ED_DOUT = 2675, 2899    # roll 2 1:29.17 (88.99-89.37, 380) - 1:36.63 (96.59-96.68, 90)
EE_IN, EE_OUT = 2198, 2588      # roll 4 1:13.27 (73.15-73.40, 250) - 1:26.27 (86.16-86.34, 180)
EE_DIN, EE_DOUT = 2973, 3179    # roll 2 1:39.10 (98.93-99.30, 370) - 1:45.97 (105.89-106.04, 150)
EF_IN, EF_OUT = 5703, 5865      # cut, roll 4 3:10.10 (189.99-190.22, 230) - 3:15.50 (195.36-195.65, 300)

# ---------------------------------------------------------------- David's v2 notes, 2026-09-22
# 1. "The live video is better from 0 to 1:22. We can replace the first :51 of the new video with that
#    content." The live's opening carries the SAME canonical Boards 1 and 2, but dives into each step
#    and rings it, instead of holding the board still - which is what makes its small type readable.
#    Taken as a full audio-and-picture graft, so Boards 1 and 2 and edits A, B and C all go with it.
#    OUT-POINT MOVED from David's 1:22 to 1:23.90: at 82.0 the live has only a 70 ms gap, while
#    83.60-84.28 is a 680 ms silence that is also the live's own scene cut, and it keeps the sentence
#    "That single token is the launching pad..." whole while excluding the furniture line after it.
#    (Whisper puts that next line at 83.72; the RMS trace puts it at 84.28. The waveform wins again.)
LIVE_IN, LIVE_OUT = 0, 2517     # live 0:00 - 1:23.90 (quiet 83.60-84.28, 680)
R4_RESUME = 1707                # roll 4 0:56.90 (quiet 56.57-57.00, 430) - where the spine picks up.
                                # MUST be roll 4's own scene cut, not merely a point inside the silence:
                                # 1704 left three frames of roll 4's OWN Board 2 recreation on screen.
                                # It is the same canonical board, so the only visible difference was our
                                # ring vanishing for a tenth of a second. transition_guard caught this
                                # one precisely because the ring state changed; a recreation with no ring
                                # difference would have slipped through, as it did on Support Trap.
GAIN_LIVE = -1.1                # the live is -15.4 LUFS against roll 4's -16.5, so it comes DOWN
# 2. "At 2:14, there's a flash of an old graphic." Confirmed: TWO cuts ten frames apart at output 4020
#    and 4030. transition_guard needs two within six, so it passed this - the same blind spot that let
#    Engagement Trap's nine-frame leak through. Board 3 was held to source 4480 while roll 4's own
#    scene runs to 4490, leaving the last ten frames of its "You could name him Spot" chips on screen
#    for a third of a second. The board now holds to roll 4's own cut, so the flash cannot happen.
# 3. "Delete 3:31 to 3:36. It essentially repeats the closing message." That span is Board 4's banner
#    line. See the note on BD4_OUT below - it is required verbatim line 6.
DEL_LINE6_IN = 6963             # roll 4 3:52.10 (quiet 231.99-232.24, 250), straight into the close

# ---------------------------------------------------------------- board spans, in roll 4 source frames
# Roll 4's own visual cuts: 643 Board 1, 1212 Board 2, 2490 Board 3, 5603 Board 4, 7127 close.
BD1_IN, BD1_OUT = EB_OUT, EC_IN          # 744 - 1209. Opens at the cut-B join; roll 4's own board is
                                         # hidden inside that cut, so there is no earlier frame to take.
BD2_IN, BD2_OUT = EC_IN, 1707            # 1209 - 1707. Starts under graft C, three frames before roll
                                         # 4's own board change at 1212.
BD2_R2 = BD2_IN + (EC_DOUT - EC_DIN)     # leg cursor after the graft (90 frames in, 90 out: 1:1)
BD3_IN, BD3_OUT = EE_OUT, 4490           # 2588 - 4490. Starts where graft E ends, which is where roll 4
                                         # says "Let's look at prediction one on the left."
                                         # EXTENDED past roll 4's own cut at 4353: roll 4 leaves the
                                         # board 0.1 s BEFORE speaking its banner line, "You could name
                                         # him Spot." @2:27.84. v1 held it to 4480 and left ten frames of
                                         # roll 4's own chips drawing flashing on screen (David: "a flash
                                         # of an old graphic"); it now runs to roll 4's own cut at 4490.
BD4_IN, BD4_OUT = 5603, DEL_LINE6_IN     # 3:06.77 - 3:52.10, with cut F inside it. ENDS EARLY on
                                         # David's note 3: everything from 3:52.10 to the close is cut,
                                         # which removes "Inference is the process AI uses to generate an
                                         # answer one token at a time." That is REQUIRED VERBATIM LINE 6
                                         # and Board 4's banner, so the banner ring goes with it.
BD4_LEG = (EF_IN - BD4_IN) + (BD4_OUT - EF_OUT)
BD4_R2 = BD4_IN + (EF_IN - BD4_IN)       # leg cursor after the furniture sentence comes out
CLOSE_IN, CLOSE_AUDIO_OUT = 7118, 7266   # 3:57.27 (quiet 237.20-237.47) - 4:02.20 (242.04-242.69)
GAIN_R2, GAIN_R3 = 0.5, 0.6              # roll 2 -17.0 and roll 3 -17.1 lifted to roll 4's -16.5 LUFS

# ---------------------------------------------------------------- ring rectangles, measured off the art
# Ring colour is measured off each board, never chosen (EDIT-SPEC section 5). Sampling the step titles
# returns #4824c0, #0c48f0, #0c8484 and #0c7848 - the kit's locked purple, blue, teal and green. Banners
# and whole-board points take the neutral video purple.
BD1_S1 = [80, 330, 418, 748]        # 1 Tokens: image, badge, title and its sentence
BD1_S2 = [448, 330, 785, 748]       # 2 Positions
BD1_S3 = [818, 330, 1152, 800]      # 3 Starting Vectors (its sentence runs a line longer)
BD1_S4 = [1185, 330, 1520, 830]     # 4 Through Layers (a line longer again)
BD1_BANNER = [40, 905, 1560, 992]
BD2_QUESTION = [80, 175, 788, 645]  # the token row, "The Question" and its sentence
BD2_FINAL = [818, 175, 1522, 645]   # the ? to FINAL VECTOR panel, "The Final Token" and its sentence
BD2_BANNER = [40, 718, 1560, 812]
BD3_P1 = [80, 322, 600, 762]        # the whole Prediction 1 panel
BD3_P1_ROWS = [104, 528, 578, 726]  # You 18% / A 14% / Great 9%
BD3_P1_PICK = [292, 856, 390, 918]  # the purple "You" chip under Prediction 1
BD3_MIDDLE = [632, 468, 968, 637]   # THREE MORE PREDICTIONS and its three chips. David 2026-09-22:
                                    # blue, "extend a little further down". The chips' ink ends at
                                    # y=623 and the old bottom of 622 cut straight through them. 637
                                    # sits midway between the chips and the blue arrow at y=651, so
                                    # the ring clears the chips without its bottom edge merging into
                                    # the arrow - which it did at 642, both being blue now.
BD3_REPLY = [1040, 392, 1492, 458]  # REPLY SO FAR: You could name him
BD3_HIM = [1386, 393, 1480, 457]    # the teal "him" chip - the new final token
BD3_P5_ROWS = [1022, 528, 1498, 726]  # Spot 22% / Max 17% / Buddy 14%
BD3_P5_PICK = [1203, 856, 1320, 918]  # the teal "Spot" chip under Prediction 5
BD3_BANNER = [40, 995, 1560, 1090]
BD4_RANK = [80, 315, 418, 788]
BD4_PICK = [450, 315, 786, 788]
BD4_ADD = [818, 315, 1152, 788]
BD4_REPEAT = [1185, 315, 1520, 788]
BD4_BANNER = [40, 875, 1560, 962]


def target(label, at, rect, color, radius=16, cam=None):
    d = {"label": label, "at": at, "rects": [rect], "color": color, "radius": radius}
    if cam: d["cam"] = cam
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prepare-only", action="store_true")
    ap.add_argument("--render-existing", action="store_true")
    args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, ROLL2, ROLL3, BEGINS, WHERE, TOKENBY, BUILDING, LESSON])
    b.load_audio([(4.36, 4.92), (10.62, 11.28), (13.69, 14.07), (16.19, 16.82), (20.98, 21.50),
                  (24.69, 25.06), (27.43, 27.75), (29.46, 29.78), (34.91, 35.35), (40.19, 40.53),
                  (50.23, 50.64), (52.38, 52.66), (56.67, 57.01), (58.72, 59.15), (82.76, 83.05),
                  (88.76, 89.08), (102.59, 102.91), (110.70, 111.03), (114.91, 115.20),
                  (117.32, 117.94), (122.96, 123.24), (124.09, 124.66), (129.67, 130.15),
                  (134.40, 134.87), (137.82, 138.14), (141.75, 142.18), (144.71, 145.18),
                  (147.55, 147.91), (149.12, 149.68), (151.72, 152.10), (157.29, 157.74),
                  (166.20, 166.63), (169.37, 169.80), (177.40, 177.80), (179.55, 179.89),
                  (186.40, 186.71), (189.05, 189.37), (195.35, 195.65), (207.01, 207.31),
                  (239.84, 240.12), (242.04, 245.46)])

    # David's note 1: the live video's opening replaces roll 4's, with its own picture AND sound. It
    # carries the same canonical Boards 1 and 2 but dives into each step, which is what makes them
    # readable. Roll 4's Boards 1 and 2 and edits A, B and C are all inside this span and go with it.
    b.graft(LIVE, LIVE_IN, LIVE_OUT,
            "The live video's 0:00-1:23.90 (own picture and sound): the opening, Board 1 dived step by "
            "step, and Board 2 - David 2026-09-22, 'the live video is better from 0 to 1:22'",
            "liveopen", cover_intro=False, gain_db=GAIN_LIVE)
    b.keep(R4_RESUME, ED_IN, "Notebook drawing: the token grid")
    b.graft(ROLL2, ED_DIN, ED_DOUT,
            "'It uses those numbers from the final token to calculate a probability score for every "
            "potential next token in its entire vocabulary.' (roll 2) - replaces roll 4's 'To find the "
            "very first WORD', which the kit forbids after the setup",
            "everytoken", picture_from=ED_IN, gain_db=GAIN_R2)
    b.keep(ED_OUT, EE_IN, "Notebook drawing: 'This triggers a repeating generation loop.'")
    b.graft(ROLL2, EE_DIN, EE_DOUT,
            "'The AI selects a token, adds it to the growing reply, and then uses that newly expanded "
            "context to predict again.' (roll 2) - the lesson's wording, replacing roll 4's 'top scoring "
            "token' lean AND its 'This chart breaks down the selection process' in one move",
            "selectadd", picture_from=EE_IN, gain_db=GAIN_R2)
    b.keep(BD3_IN, BD3_OUT, "The Answer, Token by Token", "bd3")
    b.keep(BD3_OUT, BD4_IN, "Notebook drawings: the finished sentence, the dog")
    b.keep(BD4_IN, EF_IN, "Inference: How AI Builds an Answer", "bd4")
    # cut F: roll 4's "Let's look at this diagram to summarize..." comes out here
    b.keep(EF_OUT, BD4_OUT, "Inference: How AI Builds an Answer", "bd4", video_from=BD4_R2)
    # David's note 3: everything from BD4_OUT to the close is cut - verbatim line 6 and the banner.
    b.mark_close_start()
    b.close(CLOSE_IN, CLOSE_AUDIO_OUT, tail=150)
    b.finish_audio()

    # Boards 1 and 2 are no longer built here: David's note 1 replaces that whole stretch with the
    # live video's own rendering of the same two canonical boards.

    # Board 3 (compact): the longest board in the file at 63 s, so the rings walk it item by item, left
    # panel to right, exactly as roll 4 reads it. Prediction 1's side is purple on the board and
    # Prediction 5's is teal; the middle block belongs to neither, so it takes the neutral purple.
    b.board("bd3", TOKENBY, BD3_IN, BD3_OUT, "compact", [
        target("Prediction 1, the final token", 88.84, list(BD3_P1), PURPLE),
        target("You 18%, A 14%, Great 9%", 95.44, list(BD3_P1_ROWS), PURPLE),
        target("the pick: You", 102.30, list(BD3_P1_PICK), PURPLE, radius=12),
        target("three more predictions", 106.52, list(BD3_MIDDLE), BLUE),   # David 2026-09-22: blue, not neutral
        target("reply so far: You could name him", 117.76, list(BD3_REPLY), TEAL),
        target("him, the new final token", 124.58, list(BD3_HIM), TEAL, radius=12),
        target("Spot 22%, Max 17%, Buddy 14%", 134.42, list(BD3_P5_ROWS), TEAL),
        target("the pick: Spot", 141.72, list(BD3_P5_PICK), TEAL, radius=12),
    ], banner_at=147.84, banner=list(BD3_BANNER), push=False)

    # Board 4 (compact): one ring per step card as it is named. The banner is verbatim line 6. Onsets
    # after the cut are given in the leg's own frame space.
    def bd4(src):
        return (BD4_R2 + (fr(src) - EF_OUT)) / FPS
    b.board("bd4", BUILDING, BD4_IN, BD4_IN + BD4_LEG, "compact", [
        target("1 Rank", bd4(196.04), list(BD4_RANK), PURPLE),
        target("2 Pick", bd4(207.70), list(BD4_PICK), BLUE),
        target("3 Add", bd4(215.06), list(BD4_ADD), TEAL),
        target("4 Repeat", bd4(221.48), list(BD4_REPEAT), GREEN),
    ], push=False)   # no banner ring: its line is the one David cut (see DEL_LINE6_IN)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards:
            b.state_sheet(k)
    # The close board is keyed by the lesson's INTERNAL id, which is `prediction`, not the asset
    # slug. index.html CLOSE_BOARDS carries exactly the two closing lines under that key.
    b.make_close("prediction")
    b.manifest({
        "scope_detail": "Stitched production candidate (David, 2026-09-22): roll 4 spine, four grafts "
                        "(three from roll 2, one from roll 3) and two cuts; live video, rolls, lesson "
                        "and boards unchanged.",
        "narration_changes": {
            "live_open": "David 2026-09-22: roll 4 0:00-0:56.80 replaced by the LIVE video 0:00-1:23.90, "
                         "own picture and sound, -1.1 dB. Supersedes v1's edits A, B and C and both of "
                         "its Board 1 and Board 2 legs, which were inside that span.",
            "line6_cut": "David 2026-09-22: roll 4 3:52.10 to the close removed - 'Inference is the "
                         "process AI uses to generate an answer one token at a time.', REQUIRED VERBATIM "
                         "LINE 6 and Board 4's banner, cut because it repeats the closing message.",
            "flash_fix": "Board 3 now runs to roll 4's own cut at 4490 instead of 4480; v1 left ten "
                         "frames of roll 4's chips drawing flashing at output 2:14.",
            "D_word_for_token": "roll 4 0:58.97-1:10.03 ('To find the very first word...') -> roll 2 "
                                "1:29.17-1:36.63, +0.5 dB",
            "E_framing_and_furniture": "roll 4 1:13.27-1:26.27 ('The AI will select a top scoring "
                                       "token...' plus 'This chart breaks down the selection process "
                                       "step by step.') -> roll 2 1:39.10-1:45.97, +0.5 dB",
            "F_cut": "roll 4 3:10.10-3:15.50 ('Let's look at this diagram to summarize...')",
            "engine_outro_removed_from_frame": CLOSE_AUDIO_OUT,
        },
        "verbatim_lines": {
            "NOTE": "v2 carries five of the eight. Lines 1 and 2 leave with the live-video opening, which "
                    "speaks neither; line 6 is cut on David's note 3. This is a deliberate trade he made "
                    "after watching v1, not a defect of the build.",
            "in_v1_all_eight_from_roll_4": [
                "AI uses the final token's updated numbers to predict what comes next.",
                "AI uses the final token's vector to predict the first token of its answer.",
                "You could name him Spot.",
                "Each added token changes what can fit next.",
                "AI keeps predicting tokens until it produces a special token that signals the answer is finished.",
                "Inference is the process AI uses to generate an answer one token at a time.",
                "Every answer is built one token at a time.",
                "The whole run is called inference.",
            ],
        },
        "audio_floors": {"roll_4": -64.4, "roll_2": -65.9, "roll_3": -67.2, "live": -63.9,
                         "note": "2.8 dB across all three, the cleanest donor set in the series; each "
                                 "graft steps at most 2.8 dB and every one lands under a board or a "
                                 "drawn scene."},
        "added_teaching_pauses": [],
        "board_render_covered": [
            {"frames": [BD3_IN, BD3_OUT], "replacement": "canonical The Answer, Token by Token (held "
                                                         "past roll 4's own cut so its banner line is "
                                                         "spoken while the board is up)"},
            {"frames": [BD4_IN, BD4_IN + BD4_LEG], "replacement": "canonical Inference: How AI Builds an Answer"},
            {"frames": [CLOSE_IN, CLOSE_AUDIO_OUT], "replacement": "standard close"},
        ],
        "notebook_interleaves": [],
        "longest_unbroken_board_run_seconds": round(max(BD3_OUT - BD3_IN, BD4_LEG) / FPS, 2),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build Support Trap v1 from roll 1, with two grafts and one added pause (David, 2026-09-21).

Roll 1 is the only version that speaks both safety-critical lines exactly - the content note ("The next
story discusses suicide.") and the emergency line ("In the U.S., call or text 988 for crisis support.
Call 911 if someone is in immediate danger.") - and it is the most complete on Boards 1 and 3. Two things
it gets wrong or omits are fixed from identified donors:

  blackbox   Roll 1 invents a cause in the account of a real death: "Because she relied on the bot, the
             AI's isolated digital environment ACTIVELY held details...". The prompt forbids inventing
             causes here. The live video's repaired passage (2026-09-19) stays with the lesson's claim and
             invents nothing, so it replaces roll 1's. Audio only; roll 1's own black-box drawing stays on
             screen, capped before its recreation of Board 3.
  leavechat  "Know When to Leave the Chat" - most of the course is about using AI well, here it means
             knowing when to leave - which roll 1 drops entirely. Only roll 2 speaks it. Carried with roll
             2's own drawn scene of a hand leaving a phone.

And one added pause: roll 1 leaves 0.52 s after the content note where the prompt asks for room for a
pause (the live video leaves 4.33 s). 2.5 s of matched room tone is inserted in roll 1's own silence.

Roll 1 -16.92 LUFS / 168.4 Hz, live -17.98 / 170.2, roll 2 -17.59 / 170.2; pause floors -60.6, -63.1 and
-59.0 dB, all within 4 dB, so no noise cliff. Boards 1-3 are the canonical page assets; standard close.
Live video, rolls, lesson and boards unchanged.
"""
from pathlib import Path
import argparse, json, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, FPS, W, H, PURPLE, BLUE, TEAL, AMBER, RED, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/support-trap-1.mp4"        # spine
ROLL2 = ROOT / "Prompts/support-trap-2.mp4"      # "Know When to Leave the Chat"
A = ROOT / "course-assets/support-trap"
LIVE = A / "support-trap.mp4"                    # donor for the black-box passage; also the video replaced
AUDIT = ROOT / "video-audit/support-trap-stitch-2026-09-21"
OUT = AUDIT / "build"
DEST = ROOT / "Prompts/support-trap-v4.mp4"
CMP, ROLE, DANGER = A / "support-trap-comparison.jpg", A / "support-trap-role.jpg", A / "support-trap-danger.jpg"
LESSON = ROOT / "lessons/support-trap.md"

# Every boundary sits inside a measured silence (ffmpeg silencedetect, -40 dB) IN THE FILE BEING CUT, and
# was checked against word-level timings. Contiguous-audio row splits count too: keep() crossfades its own
# row edges into room tone, so a split in running speech punches a hole (Engagement Trap, 2026-09-21).
BD1_IN = 345                     # 0:11.50 (quiet 11.06-11.59), the scenario begins
BD1_OUT = 2148                   # 1:11.60 (quiet 71.34-71.92), Board 2 arrives
BD2_OUT = 2790                   # 1:33.00 (quiet 92.70-93.28); 93.40 fell just outside the silence
BD2_PIC = 2795                   # picture_advance: roll 1 holds its OWN recreation of Board 2 for five
                                 # frames after ours leaves (2790-2794) and cuts at 2795. transition_guard
                                 # did NOT catch this one - its recreation is near-identical to the real
                                 # board, so the cut between them fell under the detector's threshold and
                                 # only a frame-by-frame look found it.
NOTE_AT = 4026                   # 2:14.20 (quiet 133.92-134.47), where roll 1's content note begins
PAUSE_AT, PAUSE_N = 4101, 100    # 2:16.70 (quiet 136.43-136.95), 3.33 s after the content note
# David 2026-09-21: "I do like the way the live video has the content warning at 2:00." The live video
# holds a full-screen CONTENT WARNING card ("Sensitive subject matter regarding self-harm") for 8.4 s
# across the spoken note and the silence, and leads in with "A quick note before we continue." v3 played
# roll 1's exact note over a drawing of an empty chair - restrained, but no visual warning at all, so a
# viewer who needs to look away gets no signal. The card and the lead-in are borrowed; roll 1's wording
# stays, because "The next story discusses suicide." is the lesson's line and the live's is not.
CW_LEAD_IN, CW_LEAD_OUT = 3615, 3677     # live 2:00.50-2:02.57, "A quick note before we continue."
CW_CARD_IN, CW_CARD_END = 3681, 3871     # the card's own frames; it ends at the live's cut at 3871
GA_AT, GA_BACK = 5084, 5608      # 2:49.47 (quiet 169.23-169.72) - 3:06.93 (quiet 186.80-187.08): roll 1's
                                 # "Sophie ultimately died by suicide. Afterward, her mother described
                                 # these AI chats as a black box. Because she relied on the bot..." out.
GA_IN, GA_OUT = 4499, 5061       # live 2:29.97 (quiet 149.56-150.39) - 2:48.70. The out-point stops SHORT
                                 # of the silence's end on purpose: the live video carries ~200 ms of TRUE
                                 # digital silence at 168.76-168.94 (an artifact of its own build), and a
                                 # graft ending inside it punched a 120 ms hole of dead air into the
                                 # output where the room tone should be continuous. Cutting at 168.70
                                 # keeps 0.36 s of the donor's real room tone and lets our bed carry on.
GA_PIC_END = 5624                # roll 1 cuts to its OWN recreation of Board 3 here; the borrowed picture
                                 # stops before it and holds its last clean frame (picture_advance rule)
BD3_IN, BD3_OUT = 5608, 7182     # Board 3 takes the screen as the graft ends; out 3:59.40 (quiet 239.12-239.71)
GB_IN, GB_OUT = 5756, 5961       # roll 2 3:11.87 (quiet 191.54-192.19) - 3:18.70 (quiet 198.55-198.89)
CLOSE_IN, CLOSE_AUDIO_OUT = 7182, 7355   # out 4:05.17: roll 1's last word decays to -72 dB by 245.15 and
                                         # the file goes to digital silence at 245.20, so the tail is kept
                                         # whole and the build supplies room tone after it
GAIN_LIVE, GAIN_R2 = 1.1, 0.7    # both donors are quieter than roll 1

# Ring colour is measured off each board, never chosen (Edit Spec section 5).
# Board 1 (1600x1511): a scenario strip, then two photo-topped cards, then the banner.
BD1_SCENARIO = [42, 114, 1559, 238]        # "THE SCENARIO" label measures #5e45b9 -> PURPLE
BD1_SISTER = [42, 271, 783, 1340]          # "Your Older Sister" measures #3066e3 -> BLUE
BD1_BOT = [817, 271, 1559, 1340]           # "The Chatbot" measures #a87b2e -> AMBER
BD1_BANNER = [41, 1381, 1559, 1468]
# Board 2 (1600x885): two cards, illustration over text; compact - it reads at full view.
BD2_LEFT = [41, 128, 784, 717]             # "What Can Be Real" measures #159289 -> TEAL
BD2_RIGHT = [817, 128, 1560, 717]          # "What Is Missing" measures #c62932 -> RED
BD2_BANNER = [40, 757, 1561, 846]
# Board 3 (1600x901): three separate cards, all three headings measure #c6-#c7 red -> RED.
BD3_CARDS = ([41, 128, 525, 733], [558, 128, 1043, 733], [1076, 128, 1560, 733])
BD3_BANNER = [40, 773, 1561, 862]


def target(label, at, rect, color, radius=20, cam=None):
    d = {"label": label, "at": at, "rects": [rect], "color": color, "radius": radius}
    if cam: d["cam"] = cam
    return d


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true"); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, ROLL2, CMP, ROLE, DANGER, LESSON])
    b.load_audio([(0.00, 0.32), (3.67, 3.90), (5.56, 5.97), (11.06, 11.59), (14.10, 14.42), (15.95, 16.30),
                  (18.82, 19.34), (22.62, 23.02), (23.71, 23.95), (25.34, 25.56), (26.98, 27.47),
                  (28.94, 29.29), (30.70, 30.97), (33.76, 34.07), (35.79, 36.02), (38.55, 39.14),
                  (40.81, 41.13), (43.86, 44.19), (44.82, 45.09), (45.66, 45.87), (47.56, 47.82),
                  (50.24, 50.77), (53.26, 53.47), (55.48, 55.79), (57.92, 58.24), (59.86, 60.28),
                  (64.29, 64.73), (66.34, 66.84), (71.34, 71.92), (74.14, 74.46), (76.31, 76.60),
                  (80.07, 80.70), (81.35, 81.63), (82.49, 83.07), (85.25, 85.45), (87.83, 88.45),
                  (88.94, 89.34), (91.25, 91.46), (92.70, 93.28), (97.36, 97.86), (99.79, 100.14),
                  (103.84, 104.09), (107.53, 108.16), (109.83, 110.16), (113.55, 113.98), (114.98, 115.48),
                  (119.18, 119.53), (122.32, 122.84), (124.53, 125.06), (125.58, 126.19), (131.76, 131.96),
                  (133.92, 134.47), (136.43, 136.95), (143.06, 143.51), (146.82, 147.02), (151.81, 152.34),
                  (157.02, 157.47), (160.15, 160.34), (162.24, 162.66), (164.17, 164.49), (166.27, 166.57),
                  (169.23, 169.72), (171.76, 172.23), (175.77, 176.24), (177.84, 178.03), (186.80, 187.08),
                  (187.31, 187.57), (194.64, 195.05), (195.25, 195.55), (197.34, 197.71), (200.94, 201.21),
                  (201.42, 201.66), (205.04, 205.48), (207.87, 208.27), (208.50, 208.71), (210.41, 210.78),
                  (212.88, 213.35), (215.00, 215.35), (217.12, 217.31), (219.60, 219.99), (220.22, 220.46),
                  (222.16, 222.65), (224.48, 224.90), (226.28, 226.67), (228.87, 229.09), (230.70, 231.06),
                  (231.28, 231.47), (233.74, 234.20), (239.12, 239.71), (241.64, 242.06), (245.10, 248.27)])

    b.keep(0, BD1_IN, "Notebook drawings: AI that sounds patient, caring and understanding")
    b.keep(BD1_IN, BD1_OUT, "Supportive Words versus Support", "bd1")
    b.keep(BD1_OUT, BD2_OUT, "Use AI to Get Ready for People", "bd2")
    b.keep(BD2_OUT, NOTE_AT, "Notebook drawings: the three jobs of an AI interaction",
           video_from=BD2_PIC, video_end=NOTE_AT)
    b.graft(LIVE, CW_LEAD_IN, CW_LEAD_OUT, "'A quick note before we continue.' (live video, over its CONTENT WARNING card)",
            "cwlead", cover_intro=True, gain_db=GAIN_LIVE)
    b.keep(NOTE_AT, PAUSE_AT, "The next story discusses suicide. - roll 1's exact wording, over the live video's CONTENT WARNING card",
           video_src=LIVE, video_from=CW_CARD_IN, video_end=CW_CARD_END)
    b.pause(PAUSE_N, "Room after the content note, with the warning card still held (roll 1 alone leaves 0.52 s)")
    b.keep(PAUSE_AT, GA_AT, "Notebook drawings: Sophie, the persona Harry, and what the chatbot could not do")
    b.graft(LIVE, GA_IN, GA_OUT, "'After Sophie died by suicide, her mother described the chats as a black box…' (the live video's repaired passage, replacing roll 1's invented cause)",
            "blackbox", picture_from=GA_AT, video_end=GA_PIC_END, gain_db=GAIN_LIVE)
    b.keep(BD3_IN, BD3_OUT, "If Someone May Be in Immediate Danger", "bd3")
    b.graft(ROLL2, GB_IN, GB_OUT, "'Most of AI literacy is about how to use tools well. Here, using the tool well means knowing when to leave the chat.' (roll 2, over its own drawn scene)",
            "leavechat", cover_intro=True, gain_db=GAIN_R2)
    b.mark_close_start()
    b.close(CLOSE_IN, CLOSE_AUDIO_OUT, tail=150)
    b.finish_audio()

    # Board 1 (dense): the scenario, then each reply's whole card as it is read, then the banner.
    b.board("bd1", CMP, BD1_IN, BD1_OUT, "dense", [
        dict(target("THE SCENARIO", 16.00, list(BD1_SCENARIO), PURPLE), cam=list(BD1_SCENARIO)),
        dict(target("Your Older Sister", 19.00, list(BD1_SISTER), BLUE), cam=list(BD1_SISTER)),
        dict(target("The Chatbot", 40.81, list(BD1_BOT), AMBER), cam=list(BD1_BOT)),
    ], banner_at=64.60, pullback_at=64.60, banner=BD1_BANNER, per_target_camera=True, lead_camera=True)

    # Board 2 (compact): push=False, because a row boundary sits inside the span.
    b.board("bd2", ROLE, BD1_OUT, BD2_OUT, "compact", [
        target("What Can Be Real", 74.20, list(BD2_LEFT), TEAL, radius=18),
        target("What Is Missing", 80.40, list(BD2_RIGHT), RED, radius=18),
    ], banner_at=89.20, banner=BD2_BANNER, push=False)

    # Board 3 (dense): one leg per action as it is named, then the banner at full view.
    b.board("bd3", DANGER, BD3_IN, BD3_OUT, "dense", [
        dict(target("Leave the Chat", 195.25, list(BD3_CARDS[0]), RED), cam=list(BD3_CARDS[0])),
        dict(target("Do It Now", 210.41, list(BD3_CARDS[1]), RED), cam=list(BD3_CARDS[1])),
        dict(target("Tell Anyway", 222.16, list(BD3_CARDS[2]), RED), cam=list(BD3_CARDS[2])),
    ], banner_at=233.74, pullback_at=233.74, banner=BD3_BANNER, per_target_camera=True, lead_camera=True)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("supporttrap")
    b.manifest({
        "scope_detail": "Stitched production candidate (David, 2026-09-21): roll 1 spine, two grafts and one added pause; live video, rolls, lesson and boards unchanged.",
        "narration_changes": {
            "removed": "roll 1's 2:49.47-3:06.93 ('Sophie ultimately died by suicide. Afterward, her mother described these AI chats as a black box. Because she relied on the bot, the AI's isolated digital environment actively held details...')",
            "graft_blackbox": "live 2:29.97-2:48.90 replaces it; audio only over roll 1's own black-box drawing, +1.1 dB",
            "graft_leavechat": "roll 2 3:11.87-3:18.70 inserted before the closing lines with its own picture, +0.7 dB; no roll 1 words removed",
            "added_pause": f"{PAUSE_N} frames of matched room tone at source {PAUSE_AT}, after the content note",
            "engine_outro_removed_from_frame": CLOSE_AUDIO_OUT,
        },
        "accuracy_requirements": {
            "content_note_verbatim": "roll 1, 2:14.20: 'The next story discusses suicide.'",
            "emergency_line_verbatim": "roll 1, 3:21: 'In the U.S., call or text 988 for crisis support. Call 911 if someone is in immediate danger.'",
            "attribution": "roll 1 names Laura Reiley, 2025, her 29-year-old daughter Sophie Rottenberg",
            "no_invented_cause": "roll 1's causal claim is removed by the blackbox graft; the live passage states only what the lesson states",
            "died_by_suicide_not_euphemised": "the live donor says 'After Sophie died by suicide'",
            "safety_outranks_secrecy": "roll 1, 3:42: 'Safety always outranks secrecy.' (lesson has no 'always')",
        },
        "added_teaching_pauses": [{"source_frame": PAUSE_AT, "frames": PAUSE_N, "why": "room after the content note"}],
        "board_render_covered": [
            {"frames": [BD1_IN, BD1_OUT], "replacement": "canonical Supportive Words versus Support (post-only course board)"},
            {"frames": [BD1_OUT, BD2_OUT], "replacement": "canonical Use AI to Get Ready for People"},
            {"frames": [BD3_IN, BD3_OUT], "replacement": "canonical If Someone May Be in Immediate Danger"},
            {"frames": [CLOSE_IN, CLOSE_AUDIO_OUT], "replacement": "standard close"},
        ],
        "notebook_interleaves": [
            {"source": "support-trap-2.mp4", "frames": [GB_IN, GB_OUT], "use": "roll 2's drawn hand-leaving-a-phone scene under its own leave-the-chat beat"},
        ],
        "longest_unbroken_board_run_seconds": round(max(BD1_OUT - BD1_IN, BD2_OUT - BD1_OUT, BD3_OUT - BD3_IN) / FPS, 2),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()

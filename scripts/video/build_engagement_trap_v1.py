#!/usr/bin/env python3
"""Build Engagement Trap v1 from roll 4 plus three grafts (David's approval 2026-09-21).

The live 2026-09-08 video predates the lesson's whole final section: no Meta settlement, no Board 4,
no scope distinction, and neither closing line spoken. Roll 4 teaches all of it correctly and speaks
both closing lines exactly, so it is the spine. Three grafts close what roll 4 alone compresses:

  answer   the live video's own reading of the AI's reply - the definition, the formula, and all three
           offers - which roll 4 reduces to "The AI answers, then offers an example." The canonical
           Board 1 has that reply on screen, so the narration now reads the bubble the camera is on.
  trapend  roll 2's fuller trap ending (examples, graphs, practice problems, a quiz) carrying the
           lesson's own "All of it was useful. None of it was what you opened the chat to do.",
           which roll 4 drops entirely.
  regret / everywhere
           roll 1's run from Raskin's regret through the half-million estimate and the autoplay,
           streak and one-more-round beat that roll 4 never speaks. Split in two: Board 2 holds
           through the regret and the estimate, then roll 1's own footage (its autoplay countdown,
           its streak-reset panel) carries the everywhere beat under its own narration.

Roll 4 -16.81 LUFS / 173.9 Hz, roll 1 -17.19 / 173.9, roll 2 -15.90 / 177.8, live -15.82 / 183.9.
Boards 1-4 are the canonical page assets; standard close. Live video, rolls, lesson and boards unchanged.
"""
from pathlib import Path
import argparse, json, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, FPS, W, H, PURPLE, BLUE, TEAL, AMBER, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/engagement-trap-4.mp4"     # spine
ROLL1 = ROOT / "Prompts/engagement-trap-1.mp4"   # regret -> half-million -> autoplay/streaks/games
ROLL2 = ROOT / "Prompts/engagement-trap-2.mp4"   # the trap ending and "All of it was useful..."
ROLL3 = ROOT / "Prompts/engagement-trap-3.mp4"   # PICTURE ONLY: its drawn gavel panel covers a stock photo
A = ROOT / "course-assets/engagement-trap"
LIVE = A / "engagement-trap.mp4"                 # donor for the AI's answer; also the video being replaced
AUDIT = ROOT / "video-audit/engagement-trap-stitch-2026-09-21"
OUT = AUDIT / "build"
DEST = ROOT / "Prompts/engagement-trap-v10.mp4"   # v1 leaked frames of roll 4's own panels at two board exits (picture_advance); v2 clipped two word tails
CHAT, SCROLL = A / "engagement-trap-comparison.jpg", A / "engagement-trap-scroll.jpg"
QUIT, POINTS = A / "engagement-trap-stopping-point.jpg", A / "engagement-trap-stopping-points.jpg"
LESSON = ROOT / "lessons/engagement-trap.md"

# Every boundary below sits inside a measured silence (ffmpeg silencedetect, -40 dB / 0.18 s) in the
# roll that owns it, and was checked against word-level timings so no first or last word is clipped.
BD1_IN = 908                     # 0:30.27 (quiet 29.87-30.30), "This comparison chart shows…"
GA_AT, GA_BACK = 1145, 1226      # 0:38.15 (quiet 37.87-38.42) - 0:40.85 (quiet 40.68-41.03): roll 4's
                                 # "The AI answers, then offers an example." comes out.
GA_IN, GA_OUT = 581, 1203        # live 0:19.36 (quiet 19.23-19.49) - 0:40.10 (quiet 39.88-40.31)
GB_AT, GB_BACK = 1416, 1520      # 0:47.20 (quiet 47.10-47.45) - 0:50.65 (quiet 50.48-50.83). Roll 4 keeps
                                 # its own "On the right, you accept." and loses only "Sure. 25 minutes
                                 # later, you're taking a quiz." David 2026-09-21: a bare "Accept..." gave
                                 # no signal that this is the second of two choices. Roll 3 says "On the
                                 # right, the trap." and was tried first, but its pause floor is -48.4 dB
                                 # against roll 4's -65.9 - a 17 dB noise cliff - so the signpost comes
                                 # from roll 4's own room instead.
GB_IN, GB_OUT = 1514, 1860       # roll 2 0:50.47 (dip 50.43-50.50, floor -62.1) - 1:02.00 (quiet 61.76-
                                 # 62.26). Starts at "And 25 minutes later...", after roll 2's own
                                 # "Accept," so the word is not spoken twice.
GD_AT, GD_BACK = 1635, 1763      # 0:54.50 (quiet 54.27-54.73) - 0:58.75 (quiet 58.51-59.00): roll 4's
                                 # "The engagement trap is spending time you never originally budgeted."
GD_IN, GD_OUT = 2541, 2717       # roll 1 1:24.70 (quiet 84.50-84.89) - 1:30.55 (quiet 90.36-90.73):
                                 # "That is the engagement trap. You end up spending time you never
                                 # originally decided to spend." - second person, and closer to the
                                 # lesson's "spending time you never decided to spend".
BD1_OUT = 1983                   # 1:06.10 (quiet 65.89-66.11), Board 2 arrives
# Board 1 carries five audio edits, so its leg cursor is tracked step by step.
BD1_R2 = BD1_IN + (GA_AT - BD1_IN) + (GA_OUT - GA_IN)   # roll 4 resumes after the live graft
BD1_R3 = BD1_R2 + (GB_AT - GA_BACK)                     # the roll 2 trap ending starts here
BD1_R4 = BD1_R3 + (GB_OUT - GB_IN)                      # roll 4 resumes ("Both answered...")
BD1_R5 = BD1_R4 + (GD_AT - GB_BACK)                     # the roll 1 definition starts here
BD1_R6 = BD1_R5 + (GD_OUT - GD_IN)                      # roll 4 resumes ("This design logic...")
BD1_LEG = BD1_R6 - BD1_IN

BD2_IN = 1983
GC_AT, GC_BACK = 2535, 2973      # 1:24.50 (quiet 84.31-84.85) - 1:39.10 (quiet 99.06-99.27): roll 4's
                                 # regret sentence, the half-million estimate and its AI-chat line come out.
GC1_IN, GC1_OUT = 4008, 4368     # roll 1 2:13.60 (quiet 133.22-133.82) - 2:25.60
GC2_IN, GC2_OUT = 4368, 5010     # roll 1 2:25.60 - 2:47.00 (quiet 166.85-167.46), with its own picture
# The junction sits at roll 1's own 2:25.60: its speech runs to 145.25 and resumes at 145.75, so the
# floor is 145.50-145.72. v2 put it at 145.20, taken from roll 4's silence list by mistake, which left
# each graft's 5 ms room-tone crossfade on the decaying tail of "everywhere." (measured, not decoded).
BD2_LEG = GC_AT - BD2_IN

BD3_IN, BD3_OUT = 2973, 3465     # AI Won't Quit for You; out 1:55.50 (quiet 115.14-115.58)
BD4_IN, BD4_OUT = 4802, 5973     # 2:40.08 (quiet 159.90-160.35) - 3:19.10 (quiet 198.63-199.26)
BD3_PIC, BD4_PIC = 3467, 5977   # first clean frame after each board exit (see picture_advance below)
# David 2026-09-21: roll 4 illustrates "harmed children and teens" with a stock PHOTOGRAPH of identifiable
# real teenagers (its own frames 4233-4358). Course rule: no stock photography. Covered picture-only with
# roll 3's drawn gavel-and-binders panel (its frames 4986-5192, sampled 4990-5115). Roll 3's audio is not
# used anywhere - its room is 17 dB noisier - but its drawings are clean.
PHOTO_AT, PHOTO_BACK = 4129, 4356      # source-audio frames either side of the photo, BOTH inside measured
                                       # roll 4 silences (137.52-137.72 and 144.88-145.35). The cover starts
                                       # 3.4 s before the photo because there is no silence any nearer to it:
                                       # a keep() row crossfades its own edges into room tone, so a split in
                                       # running speech punches a notch (v6 measured -10 dB here and -30 dB at
                                       # the close). The picture boundary may sit anywhere; the AUDIO boundary
                                       # may not.
PHOTO_PIC_IN, PHOTO_PIC_OUT = 4233, 4358   # the photo's own picture frames
R3_PIC_IN, R3_PIC_OUT = 4990, 5192     # roll 3's drawn panel; shorter than the row, so its last frame
                                       # holds for the remaining 25 frames (keep()'s documented behaviour)
# David 2026-09-21: roll 4 plays its OWN closing board from frame 6351, so a second, zoomed-out close
# appeared before ours. mark_close_start() is called at that cut instead, which is its documented use:
# the standard close takes the screen exactly where the engine's own close arrives.
RASKIN_PIC = 1772                      # picture_advance, David 2026-09-21 ("a flash of the old version of
                                       # the board at 1:26"): roll 4 holds its OWN recreation of the
                                       # comparison board for 9 frames (1763-1771) before cutting to the
                                       # Aza Raskin panel at 1772. Its panel then runs to 1982; at 1983 it
                                       # cuts to its own scroll-board recreation, which our Board 2
                                       # replaces, so video_end stops the borrowed picture there and holds
                                       # frame 1982 for the row's last 9 frames.
CLOSE_PIC = 6342                       # inside roll 4's 211.14-211.66 silence, 9 frames before its own
                                       # close board arrives at 6351, so ours takes the screen first
CLOSE_IN, CLOSE_AUDIO_OUT = 6438, 6563   # 3:34.60 (quiet 214.47-214.95) - 3:38.77
# The close out-point is measured, not decoded: roll 4's last word still sounds at -35 dB at 218.68 and
# the room-tone floor only arrives at 218.70 (digital silence at 218.85). v2 cut at 218.67 and clipped
# the final decay of "choose what happens next."

GAIN_LIVE, GAIN_R1, GAIN_R2 = -1.0, 0.4, -0.9

# Board 1 (1600x1508): one wide card holding the exchange, two outcome cards below it, then the banner.
# Each rect is the card's or bubble's own measured body, so a ring hugs it (Training Bias v6). Ring colour
# is measured off the artwork, not chosen (Edit Spec section 5): YOU STOP's own accent is #1f58ee -> BLUE
# (v5 ringed it TEAL, which David caught), THE TRAP's is #aa7a14 -> AMBER, and the two chat bubbles sit in
# a card with no locked accent, so they take the neutral video purple #6e51ff.
BD1_YOU, BD1_AI = [607, 253, 1520, 388], [81, 453, 1001, 669]
BD1_STOP, BD1_TRAP = [41, 741, 784, 1340], [817, 741, 1560, 1340]
BD1_BANNER = [40, 1380, 1561, 1469]
# Board 2 (1600x885): two separate cards, illustration over text; compact - it reads at full view.
BD2_LEFT, BD2_RIGHT = [41, 128, 784, 717], [817, 128, 1560, 717]
BD2_BANNER = [40, 757, 1561, 846]
# Board 3 (1387x1134): a photograph in a card with a title and a banner. No rings on the picture
# (Training Bias v6); the camera walks it and the banner rings on its spoken line.
BD3_PHOTO = [34, 109, 1353, 988]
BD3_RIBBON = [330, 270, 800, 970]     # the endless ribbon of conversation cards
BD3_LEVER = [800, 430, 1200, 900]     # the STOP lever and the hourglass
BD3_BANNER = [36, 1020, 1352, 1096]
# Board 4 (1600x860): three separate cards; dense - the body text needs a dive.
BD4_CARDS = ([41, 128, 525, 692], [558, 128, 1043, 692], [1076, 128, 1560, 692])
BD4_BANNER = [40, 732, 1561, 821]


def target(label, at, rect, color, radius=20, cam=None):
    d = {"label": label, "at": at, "rects": [rect], "color": color, "radius": radius}
    if cam: d["cam"] = cam
    return d


def photo_walk_banner(b, key, asset, src_in, leg_frames, moves, photo, banner, banner_at, pullback=30):
    """Camera walk over a photographic board, then a pull-back to the full board with its takeaway
    banner ringed on the line that speaks it. moves: (label, arrive_leg_frame, transit, rect)."""
    asset = Path(asset); canvas_path, cw, ch, ox, oy = b.compose(asset, key)
    n = leg_frames; full = [cw / 2, ch / 2, float(cw)]
    px0, py0, px1, py1 = photo
    def window(r):
        x0, y0, x1, y1 = r; w = max(x1 - x0, (y1 - y0) * W / H) * 1.10; h = w * H / W
        cx = min(max(x0 + ox + (x1 - x0) / 2, ox + px0 + w / 2), ox + px1 - w / 2)
        cy = min(max(y0 + oy + (y1 - y0) / 2, oy + py0 + h / 2), oy + py1 - h / 2)
        return [cx, cy, w]
    first = moves[0][1] - moves[0][2]
    beats = [dict(label="establish", frames=first, **{"from": full}, to=[cw / 2, ch / 2, cw * 0.97])]
    cursor = first
    for i, (label, arrive, transit, r) in enumerate(moves):
        nxt = moves[i + 1][1] - moves[i + 1][2] if i + 1 < len(moves) else banner_at - pullback
        beats += [dict(label=f"to-{label}", frames=transit, to=window(r)),
                  dict(label=f"hold-{label}", frames=nxt - cursor - transit, to=window(r))]
        cursor = nxt
    beats += [dict(label="pull-back", frames=pullback, to=full),
              dict(label="banner-hold", frames=n - banner_at, to=full)]
    assert sum(x["frames"] for x in beats) == n and all(x["frames"] > 0 for x in beats), (key, beats)
    rings = [dict(start=banner_at, end=n, rect=[banner[0] + ox, banner[1] + oy, banner[2] - banner[0], banner[3] - banner[1]],
                  color=NEUTRAL, pad=0, radius=22)]
    (b.out / f"leg-{key}.json").write_text(json.dumps(dict(image=str(canvas_path), fps=FPS, out_w=W, out_h=H,
                                                           upscale=3, beats=beats, rings=rings), indent=1))
    b.boards[key] = dict(key=key, asset=str(asset.relative_to(b.root)), sha256=sha(asset), src_in=src_in,
                         src_out=src_in + n, density="photographic camera walk, banner ringed",
                         full_view_frames=first, canvas_offset=[ox, oy],
                         states=[dict(spoken_onset_source_frame=src_in + banner_at, highlight_target="takeaway banner",
                                      highlight_mode="ring", highlight_color=NEUTRAL, highlight_source="neutral_video_purple")],
                         beats=beats, rings=rings)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true"); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, ROLL1, ROLL2, ROLL3, CHAT, SCROLL, QUIT, POINTS, LESSON])
    b.load_audio([(0.00, 0.26), (4.58, 4.92), (8.21, 8.48), (10.32, 10.51), (11.62, 11.85), (13.11, 13.36),
                  (14.52, 14.78), (16.62, 17.15), (17.89, 18.13), (20.11, 20.47), (22.16, 22.41), (24.00, 24.30),
                  (29.87, 30.30), (33.19, 33.58), (34.22, 34.43), (37.87, 38.42), (39.41, 39.59), (40.68, 41.03),
                  (42.26, 42.54), (43.03, 43.23), (43.93, 44.39), (45.57, 46.01), (47.10, 47.45), (47.96, 48.29),
                  (50.48, 50.83), (52.46, 52.69), (54.27, 54.73), (58.51, 59.06), (65.89, 66.11), (68.21, 68.47),
                  (69.10, 69.29), (70.23, 70.50), (72.52, 72.80), (74.25, 74.65), (75.34, 75.94), (76.49, 76.79),
                  (78.54, 78.93), (80.86, 81.15), (82.76, 82.95), (84.31, 84.85), (89.10, 89.28), (93.68, 94.05),
                  (99.06, 99.27), (101.88, 102.07), (104.58, 104.83), (108.06, 108.36), (115.14, 115.58),
                  (117.77, 118.30), (124.74, 125.11), (128.80, 129.20), (132.76, 133.18), (135.08, 135.29),
                  (137.52, 137.72), (144.88, 145.35), (146.75, 146.95), (150.52, 150.97), (155.98, 156.17),
                  (159.90, 160.35), (164.39, 164.90), (166.82, 167.03), (171.51, 171.78), (174.73, 175.20),
                  (179.55, 179.79), (183.62, 184.15), (186.78, 187.03), (191.74, 192.18), (195.36, 195.76),
                  (198.63, 199.26), (201.70, 201.93), (204.96, 205.41), (211.14, 211.66), (214.47, 214.95),
                  (216.11, 216.59), (217.18, 217.48), (218.67, 221.98)])

    b.keep(0, BD1_IN, "Notebook drawings: the quick question, the clear answer, the three follow-up offers")
    b.keep(BD1_IN, GA_AT, "One Answer. Two Endings.", "bd1")
    b.graft(LIVE, GA_IN, GA_OUT, "The AI's reply: the definition, the formula, and all three offers (live video)",
            "answer", picture_from=GA_AT, visual="bd1", gain_db=GAIN_LIVE)
    b.keep(GA_BACK, GB_AT, "One Answer. Two Endings.", "bd1", video_from=BD1_R2)
    b.graft(ROLL2, GB_IN, GB_OUT, "The trap ending and 'All of the extra material provided was accurate and useful. None of it was what you opened the chat to do.' (roll 2)",
            "trapend", picture_from=BD1_R3, visual="bd1", gain_db=GAIN_R2)
    b.keep(GB_BACK, GD_AT, "One Answer. Two Endings.", "bd1", video_from=BD1_R4)
    b.graft(ROLL1, GD_IN, GD_OUT, "'That is the engagement trap. You end up spending time you never originally decided to spend.' (roll 1)",
            "definition", picture_from=BD1_R5, visual="bd1", gain_db=GAIN_R1)
    # David 2026-09-21: roll 4 draws its own "Aza Raskin / 2006 - BOUNDED (PAGED) vs UNBOUNDED (STREAM)"
    # panel under exactly this narration (its own 0:59-1:06). Board 1 used to hold here, with the
    # narration already past it; roll 4's own picture teaches the beat and ends the board on time.
    b.keep(GD_BACK, BD1_OUT, "Roll 4's Aza Raskin panel: bounded pages against an unbounded stream",
           video_from=RASKIN_PIC, video_end=BD1_OUT)
    b.keep(BD2_IN, GC_AT, "What Infinite Scroll Removed", "bd2")
    # David 2026-09-21: roll 1's own footage here is its infinite-feed phone with a MONTHLY TIME CONSUMED
    # counter animating up to 500,000 Human Lifetimes / Month, landing on the figure as the narration says
    # "half a million". Board 2 used to hold over it. Roll 1 now carries its own picture, and because this
    # graft and `everywhere` are contiguous in roll 1, the join between them disappears entirely.
    b.graft(ROLL1, GC1_IN, GC1_OUT, "Raskin's regret and the half-million counter (roll 1, over its own footage)",
            # cover_intro=True: roll 1 holds its OWN recreation of the scroll board for three frames at
            # 4008 before its scene cuts (transition_guard caught it on v8, the same leak class as v1's
            # Board 4 exit). The graft covers those frames with the first frame after roll 1's own cut.
            "regret", cover_intro=True, gain_db=GAIN_R1)
    b.graft(ROLL1, GC2_IN, GC2_OUT, "Autoplay countdowns, streak counters, one more round (roll 1, over its own footage)",
            "everywhere", cover_intro=False, gain_db=GAIN_R1)
    b.keep(GC_BACK, BD3_OUT, "AI Won't Quit for You", "bd3")
    # picture_advance: roll 4's own "Goal Achieved - Trap Avoided" panels still occupy source 3465-3466
    # as Board 3 leaves, and its own recreation of the stopping-points board occupies 5973-5976 as
    # Board 4 leaves. Both rows start their picture after those frames and hold the last frame rather
    # than running into roll 4's next board render (transition_guard caught both on v1).
    b.keep(BD3_OUT, PHOTO_AT, "Notebook drawings: engagement metrics and the settlement",
           video_from=BD3_PIC, video_end=PHOTO_PIC_IN)
    b.keep(PHOTO_AT, PHOTO_BACK, "Roll 3's drawn gavel panel, covering roll 4's stock photograph of real teenagers",
           video_src=ROLL3, video_from=R3_PIC_IN, video_end=R3_PIC_OUT)
    b.keep(PHOTO_BACK, BD4_IN, "Notebook drawings: the settlement's terms",
           video_from=PHOTO_PIC_OUT, video_end=BD4_IN)
    b.keep(BD4_IN, BD4_OUT, "Putting the Stopping Points Back", "bd4")
    b.keep(BD4_OUT, CLOSE_PIC, "Notebook drawings: social media against AI chat",
           video_from=BD4_PIC, video_end=CLOSE_PIC)
    b.mark_close_start()
    b.keep(CLOSE_PIC, CLOSE_IN, "Standard close takes the screen where roll 4's own close arrives", "close")
    b.close(CLOSE_IN, CLOSE_AUDIO_OUT, tail=150)
    b.finish_audio()

    # Board 1 carries both Board-1 grafts, so every ring onset is given in the leg's own frame space:
    # (BD1_IN + leg_frame) / FPS. The AI bubble rings when the live donor starts reading it, and the
    # trap card rings when roll 2 starts listing what the twenty-five minutes produced.
    b.board("bd1", CHAT, BD1_IN, BD1_IN + BD1_LEG, "dense", [
        dict(target("YOU: the slope question", (BD1_IN + 102) / FPS, list(BD1_YOU), NEUTRAL), cam=list(BD1_YOU)),
        dict(target("AI: the answer and its offers", (BD1_IN + (GA_AT - BD1_IN)) / FPS, list(BD1_AI), NEUTRAL), cam=list(BD1_AI)),
        dict(target("YOU STOP", (BD1_R2 + (fr(41.14) - GA_BACK)) / FPS, list(BD1_STOP), BLUE), cam=list(BD1_STOP)),
        dict(target("THE TRAP", (BD1_R2 + (fr(46.01) - GA_BACK)) / FPS, list(BD1_TRAP), AMBER), cam=list(BD1_TRAP)),
    ], banner_at=(BD1_R4 + (fr(50.82) - GB_BACK)) / FPS,
       pullback_at=(BD1_R4 + (fr(50.82) - GB_BACK)) / FPS,
       banner=BD1_BANNER, per_target_camera=True, lead_camera=True)

    # Board 2 (compact): push=False, because the graft changes the frame count inside the span.
    b.board("bd2", SCROLL, BD2_IN, BD2_IN + BD2_LEG, "compact", [
        target("Before Infinite Scroll", 68.53, list(BD2_LEFT), BLUE, radius=18),
        target("Infinite Scroll", 75.93, list(BD2_RIGHT), AMBER, radius=18),
    ], banner_at=80.93, banner=BD2_BANNER, push=False)

    # Board 3: the course illustration, never uploaded to Notebook. The camera walks the endless
    # ribbon, then the STOP lever and hourglass, then pulls back for the takeaway.
    photo_walk_banner(b, "bd3", QUIT, BD3_IN, BD3_OUT - BD3_IN, [
        ("the-ribbon", 70, 30, BD3_RIBBON),
        ("the-stop-lever", 180, 30, BD3_LEVER),
    ], photo=BD3_PHOTO, banner=BD3_BANNER, banner_at=274)

    # Board 4 (dense): one leg per card as its numbers are spoken, then the banner at full view.
    b.board("bd4", POINTS, BD4_IN, BD4_OUT, "dense", [
        dict(target("Daily Limits", 164.84, list(BD4_CARDS[0]), PURPLE), cam=list(BD4_CARDS[0])),
        dict(target("Prompts to Pause", 171.80, list(BD4_CARDS[1]), BLUE), cam=list(BD4_CARDS[1])),
        dict(target("Nighttime Blocks", 183.92, list(BD4_CARDS[2]), TEAL), cam=list(BD4_CARDS[2])),
    ], banner_at=195.74, pullback_at=195.74, banner=BD4_BANNER, per_target_camera=True, lead_camera=True)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("engagementtrap")
    b.manifest({
        "scope_detail": "Stitched production candidate (David, 2026-09-21): roll 4 spine, three grafts from the live video, roll 2 and roll 1; live video, rolls, lesson and boards unchanged.",
        "narration_changes": {
            "removed": "roll 4's 0:38.15-0:40.85 ('The AI answers, then offers an example.'), 0:45.80-0:50.65 ('On the right, you accept. Sure. 25 minutes later, you're taking a quiz.') and 1:24.50-1:39.10 (its regret sentence, the half-million estimate and its AI-chat line)",
            "graft_answer": "live 0:19.36-0:40.10 replaces roll 4's 0:38.15-0:40.85; audio only over Board 1, -1.0 dB",
            "graft_trapend": "roll 2 0:49.75-1:02.00 replaces roll 4's 0:45.80-0:50.65; audio only over Board 1, -0.9 dB",
            "graft_regret": "roll 1 2:13.60-2:25.20 replaces the first part of roll 4's 1:24.50-1:39.10; audio only over Board 2, +0.4 dB",
            "graft_everywhere": "roll 1 2:25.20-2:47.00 continues it with roll 1's own picture, +0.4 dB",
            "engine_outro_removed_from_frame": CLOSE_AUDIO_OUT,
            "picture_advance": {
                "after_bd3": f"picture resumes at source {BD3_PIC} instead of {BD3_OUT}: roll 4's own 'Goal Achieved - Trap Avoided' panels occupy 3465-3466",
                "after_bd4": f"picture resumes at source {BD4_PIC} instead of {BD4_OUT}: roll 4's own recreation of the stopping-points board occupies 5973-5976",
            },
        },
        "verbatim_lines": {
            "met": ["No thanks. That's all I needed.", "Know what you came for.", "When you have it, choose what happens next."],
            "in_substance": {"Both chats answered the question. Only one ended there.": "roll 4 says 'Both answered the initial question, but only one ended there.'"},
            "still_off": {"The Engagement Trap is spending time you never decided to spend.": "roll 4 says 'never originally budgeted'; roll 1's 'never originally decided to spend' is closer but sits inside a third-person Board 1 run that cannot be spliced into roll 4's second person"},
        },
        "added_teaching_pauses": [],
        "board_render_covered": [
            {"frames": [BD1_IN, BD1_IN + BD1_LEG], "replacement": "canonical One Answer. Two Endings."},
            {"frames": [BD2_IN, BD2_IN + BD2_LEG], "replacement": "canonical What Infinite Scroll Removed"},
            {"frames": [BD3_IN, BD3_OUT], "replacement": "canonical AI Won't Quit for You (post-only course image)"},
            {"frames": [BD4_IN, BD4_OUT], "replacement": "canonical Putting the Stopping Points Back"},
            {"frames": [CLOSE_IN, CLOSE_AUDIO_OUT], "replacement": "standard close"},
        ],
        "notebook_interleaves": [
            {"source": "engagement-trap-1.mp4", "frames": [GC2_IN, GC2_OUT], "use": "roll 1's autoplay countdown and streak-reset panels under its own everywhere beat"},
        ],
        "longest_unbroken_board_run_seconds": round(max(BD1_LEG, BD2_LEG, BD3_OUT - BD3_IN, BD4_OUT - BD4_IN) / FPS, 2),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()

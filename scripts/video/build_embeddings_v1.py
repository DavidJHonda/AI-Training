#!/usr/bin/env python3
"""Build Embeddings v1 from roll 1 with two grafts from roll 2 (David's approval 2026-09-22).

Roll 1 is the only version that lands all eight required verbatim lines, speaks every number the lesson
gives - both drinks' six scores, all four badge numbers, the Citrus trio, and cat's whole row - and keeps
the definition order (vector, then dimension, then value). Roll 2 manages 4 of 8 lines, ends on an
invented summary instead of the two closing lines, and speaks only three of six scores per drink; the
live video is thinner still and never reads cat's row at all. Two gaps in roll 1 have donors in roll 2:

  labels   Roll 1 compresses Board 4's last two comparison rows into one sentence, leaving the taste-test
           side unspoken. Roll 2 says "We explicitly named our traits, like sweet or fizz. An AI has no
           dimension labels at all." Only that much is taken - roll 1's own next sentence, "They simply
           capture patterns in how a token is used in data.", is the lesson's wording and stays, so roll
           2's "complex mathematical patterns" never enters the build.
  neighbours  Roll 1 never names the other tokens. Roll 2 does, and drops roll 1's "master ledger" at the
           same time: "It stores one embedding for every single token, meaning cat sits right alongside
           rows for dog, latte, truck, and bicycle."

Roll 1 -15.28 LUFS, roll 2 -16.66, so roll 2 is lifted 1.4 dB. NOTE THE FLOORS: roll 1's pause floor is
-56.4 dB against roll 2's -62.8, so each graft steps down 6.4 dB into a quieter room and back up on the
way out. That is far short of the 17 dB cliff that disqualified a donor on Engagement Trap, and down-then-
up is the less audible direction, but it is the largest mismatch in an otherwise-viable set; both grafts
are short and land under a board, which is the safer shape. Boards 1-5 are the canonical page assets.
Live video, rolls, lesson and boards unchanged.
"""
from pathlib import Path
import argparse, json, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, FPS, W, H, PURPLE, BLUE, TEAL, AMBER, RED, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/embeddings-1.mp4"          # spine
ROLL2 = ROOT / "Prompts/embeddings-2.mp4"        # Board 4's label rows, and cat's neighbours
A = ROOT / "course-assets/embeddings"
LIVE = A / "embeddings.mp4"
AUDIT = ROOT / "video-audit/embeddings-stitch-2026-09-22"
OUT = AUDIT / "build"
DEST = ROOT / "Prompts/embeddings-v4.mp4"
STUDENT, MEANING = A / "embeddings-student-id.jpg", A / "embeddings-meaning-row.jpg"
NEWDIM, TASTE, MODEL = A / "embeddings-new-dimension.jpg", A / "embeddings-taste-test-to-ai.jpg", A / "embeddings-inside-real-model.jpg"
LESSON = ROOT / "lessons/embeddings.md"

# Every boundary sits inside a measured silence IN THE FILE BEING CUT (ffmpeg silencedetect, -40 dB), and
# was checked against word-level timings. Contiguous-audio row splits count: keep() crossfades its own row
# edges into room tone, so a split in running speech punches a hole. Neither roll carries true digital
# silence anywhere near these points - both only go to digital zero in their own tails.
BD1_IN, BD1_OUT = 551, 1563      # 0:18.37 (quiet 18.16-18.56) - 0:52.10 (quiet 51.90-52.28)
# David 2026-09-22, four cuts. The board stays in full view throughout and the narration stops reading
# aloud what is already legible on screen.
DEL_A_IN, DEL_A_OUT = 711, 1235  # 0:23.70 (quiet 23.50-23.91) - 0:41.18 (quiet 41.00-41.38): removes
                                 # "Look at this illustration of four students... into a shirt pocket." -
                                 # the banned board-furniture line, the four badge numbers and the
                                 # fry-stealer description, all of which the board itself shows.
DEL_B_IN, DEL_B_OUT = 2976, 3288 # 1:39.20 (quiet 99.11-99.48) - 1:49.60 (quiet 109.51-109.72): removes
                                 # coffee's six scores. Extended past David's 1:46 on purpose - "and ten
                                 # for dark. Because we keep the columns aligned," is ONE unbroken run,
                                 # so cutting at 1:46 would have orphaned "and ten for dark." Ending at
                                 # 1:49.60 also drops the "Because we keep the columns aligned" preamble,
                                 # so verbatim line 2 now begins the sentence cleanly.
DEL_C_IN, DEL_C_OUT = 7737, 8295 # 4:17.90 (quiet 257.52-258.36) - 4:36.50 (quiet 276.12-276.86): removes
                                 # "Reading across cat's row, the values start at 0.45 ... at the end."
BD1_LEG = (DEL_A_IN - BD1_IN) + (BD1_OUT - DEL_A_OUT)
BD2_IN, BD2_OUT = 2454, 4340     # 1:21.80 (quiet 81.57-82.00) - 2:24.67 (quiet 144.42-144.89)
BD2_LEG = (DEL_B_IN - BD2_IN) + (BD2_OUT - DEL_B_OUT)
BD2_R2 = BD2_IN + (DEL_B_IN - BD2_IN)                      # leg cursor after coffee's scores come out
BD3_IN, BD3_OUT = 4340, 5261     # Board 3 takes over directly; out 2:55.37 (quiet 175.14-175.60)
BD4_IN = 5448                    # 3:01.60 (quiet 181.41-181.80)
GA_AT, GA_BACK = 6522, 6636      # 3:37.40 (quiet 217.17-217.66) - 3:41.20 (quiet 221.07-221.32): roll 1's
                                 # "And these values don't have human labels, like sweet or fizz." out.
GA_IN, GA_OUT = 4244, 4450       # roll 2 2:21.47 (quiet 141.18-141.72) - 2:28.33 (quiet 148.20-148.45)
BD4_OUT = 6824                   # 3:47.47 (quiet 227.31-227.62), after the banner line
BD5_IN = 6980                    # 3:52.67 (quiet 232.43-232.87). Moved earlier on David's direction:
                                 # roll 1 cuts to its OWN zoomed recreation of the embedding table at
                                 # 6987, so the canonical board now takes the screen seven frames before
                                 # it and opens at full view, which is where he wanted it to start.
GB_AT, GB_BACK = 7323, 7439      # 4:04.10 (quiet 244.00-244.18) - 4:07.97 (quiet 247.71-248.28): roll 1's
                                 # "which acts as a master ledger, storing one embedding for every token."
GB_IN, GB_OUT = 5341, 5574       # roll 2 2:58.03 (quiet 177.89-178.18) - 3:05.80 (quiet 185.55-186.10)
BD5_OUT = 8652                   # 4:48.40 (quiet 287.99-288.79)
BD5_PIC = 8665                   # picture_advance: roll 1 holds its OWN recreation of the embedding-table
                                 # board for 13 frames after ours leaves (8652-8664) and cuts at 8665.
                                 # transition_guard caught this one; the same class has now appeared at a
                                 # board exit in every stitch this week, so it is checked by default.
CLOSE_IN = 9171                  # 5:05.70 (quiet 305.42-306.06)
CLOSE_AUDIO_OUT = 9383           # 5:12.77: roll 1's speech ends 312.48 and the file goes to TRUE digital
                                 # silence at 312.80, so the cut keeps the room tone and stops before zero
GAIN_R2 = 1.4

BD4_LEG = (GA_AT - BD4_IN) + (GA_OUT - GA_IN) + (BD4_OUT - GA_BACK)
BD4_R2 = BD4_IN + (GA_AT - BD4_IN) + (GA_OUT - GA_IN)      # leg cursor when roll 1 resumes
BD5_LEG = (GB_AT - BD5_IN) + (GB_OUT - GB_IN) + (DEL_C_IN - GB_BACK) + (BD5_OUT - DEL_C_OUT)
BD5_R2 = BD5_IN + (GB_AT - BD5_IN) + (GB_OUT - GB_IN)      # after the graft
BD5_R3 = BD5_R2 + (DEL_C_IN - GB_BACK)                     # after the deleted value-reading

# Ring colour is measured off each board, never chosen (Edit Spec section 5). Boards 2 and 3 label their
# rows in plain black - no locked accent - so their rows take the neutral video purple. Board 4's columns
# measure #149288 (teal) and #5334c5 (purple), but its rings run whole rows across both columns, which is
# a whole-board point and therefore also neutral. Board 5's elements carry no accents of their own either,
# so its rings are neutral too - which also keeps them clear of the board's own purple glow and yellow circle.
BD1_PHOTO = [40, 127, 1561, 1150]
BD1_BADGES = [150, 820, 1500, 1100]          # the four badge numbers along the table
BD1_THIEF = [820, 150, 1300, 900]            # the standing student and the fries
BD1_BANNER = [40, 1176, 1561, 1264]
BD2_COKE, BD2_COFFEE = [82, 286, 1519, 457], [82, 476, 1519, 647]
BD2_BANNER = [40, 720, 1561, 809]
# Cell-level rects for Board 2, measured chip by chip (David 2026-09-22): the columns sit at
# SWEET 441-543, BITTER 631-730, FIZZ 818-918, HEAT 1001-1103, CAFFEINE 1189-1291, DARK 1378-1479,
# with Coke's chips on y 320-423 and coffee's on y 512-615.
BD2_COKE_THREE = [95, 300, 935, 440]     # Coke's name plus 9, 1 and 10 - the three the question names
BD2_COKE_FULL = [95, 300, 1495, 440]     # Coke's name and all six values - "the whole row ... is a vector"
BD2_HEADINGS = [420, 222, 1500, 280]     # the six dimension headings - "each individual position"
BD2_ONE_VALUE = [431, 310, 553, 433]     # Coke's SWEET chip - "the specific number placed inside it"
BD3_COKE, BD3_PEPSI, BD3_COFFEE = [82, 286, 1519, 457], [82, 476, 1519, 647], [82, 666, 1519, 837]
BD3_BANNER = [40, 910, 1561, 999]
# Board 3's columns run SWEET 429-535 ... DARK 1228-1333, CITRUS 1389-1492; rows Coke y 322-423,
# Pepsi y 512-615, coffee y 698-802. Pepsi's dark-green Citrus chip measures 1392-1489 x 513-610.
BD3_PEPSI_NAME = [95, 495, 400, 630]     # just the name, as the third drink is introduced
BD3_PEPSI_SIX = [420, 500, 1345, 628]    # Pepsi's first six values only - not the Citrus column
BD3_CITRUS_HEAD = [1380, 198, 1500, 278] # the CITRUS heading and its NEW badge
BD3_PEPSI_CITRUS = [1382, 503, 1499, 620]
BD3_COKE_CITRUS = [1379, 312, 1501, 433]
BD3_COFFEE_CITRUS = [1380, 688, 1502, 812]   # coffee's Citrus 0 - David 2026-09-22, ringed as spoken
BD4_R = ([95, 268, 1530, 345], [95, 370, 1530, 455], [95, 478, 1530, 600])
BD4_LABEL_ROWS = [95, 640, 1530, 815]    # the last two rows under ONE ring, not two (David 2026-09-22)
BD4_BANNER = [40, 901, 1561, 990]
# Board 5, measured: the parchment table body sits at 488-1491 x 419-837, the TOKEN-cat plaque at
# 137-358 x 343-566, and the TOKEN ID plaque at 156-472 x 647-901. David 2026-09-22: ring the items as
# they are spoken and hold the FULL illustration throughout - seeing how the pieces fit together is the
# point of this board, so it no longer dives.
BD5_CATTILE = [137, 343, 358, 566]
BD5_IDTILE = [150, 640, 360, 905]
BD5_TABLEBODY = [488, 419, 1491, 837]        # the other tokens' rows: dog, latte, truck, bicycle, map
BD5_FIRSTTWO = [488, 350, 772, 945]          # the TOKEN ID and TOKEN columns
BD5_DIMHEAD = [772, 350, 1495, 424]          # the d1 ... dn headings
BD5_CATROW = [486, 836, 1482, 943]           # measured from the row's own purple glow
BD5_VALUE = [772, 843, 882, 938]             # the circled 0.45


def bd2(src):
    """Board 2 onset, source seconds -> the leg's own frame space, past the deleted coffee scores."""
    return (BD2_R2 + (fr(src) - DEL_B_OUT)) / FPS


def bd5(src):
    """Board 5 onset, source seconds -> the leg's own frame space, past the deleted value-reading."""
    return (BD5_R3 + (fr(src) - DEL_C_OUT)) / FPS


def target(label, at, rect, color, radius=20, cam=None):
    d = {"label": label, "at": at, "rects": [rect], "color": color, "radius": radius}
    if cam: d["cam"] = cam
    return d


def photo_walk_banner(b, key, asset, src_in, leg_frames, moves, photo, banner, banner_at, pullback=30):
    """Camera walk over a photographic board, then a pull-back to the full board with its banner ringed."""
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


def camera_walk(b, key, asset, src_in, leg_frames, moves, pullback=36):
    """Camera walk with no rings - for a board that ships with its own designed emphasis (Board 5)."""
    asset = Path(asset); canvas_path, cw, ch, ox, oy = b.compose(asset, key)
    n = leg_frames; full = [cw / 2, ch / 2, float(cw)]
    def window(r):
        x0, y0, x1, y1 = r; w = max(x1 - x0, (y1 - y0) * W / H) * 1.12
        return [x0 + ox + (x1 - x0) / 2, y0 + oy + (y1 - y0) / 2, min(w, float(cw))]
    first = moves[0][1] - moves[0][2]
    beats = [dict(label="establish", frames=first, **{"from": full}, to=[cw / 2, ch / 2, cw * 0.98])]
    cursor = first
    for i, (label, arrive, transit, r) in enumerate(moves):
        nxt = moves[i + 1][1] - moves[i + 1][2] if i + 1 < len(moves) else n - pullback
        beats += [dict(label=f"to-{label}", frames=transit, to=window(r)),
                  dict(label=f"hold-{label}", frames=nxt - cursor - transit, to=window(r))]
        cursor = nxt
    beats += [dict(label="pull-back", frames=pullback, to=full)]
    assert sum(x["frames"] for x in beats) == n and all(x["frames"] > 0 for x in beats), (key, beats)
    (b.out / f"leg-{key}.json").write_text(json.dumps(dict(image=str(canvas_path), fps=FPS, out_w=W, out_h=H,
                                                           upscale=3, beats=beats, rings=[]), indent=1))
    b.boards[key] = dict(key=key, asset=str(asset.relative_to(b.root)), sha256=sha(asset), src_in=src_in,
                         src_out=src_in + n, density="camera walk, unringed (board carries its own emphasis)",
                         full_view_frames=first, canvas_offset=[ox, oy], states=[], beats=beats, rings=[])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--prepare-only", action="store_true"); ap.add_argument("--render-existing", action="store_true"); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, ROLL2, STUDENT, MEANING, NEWDIM, TASTE, MODEL, LESSON])
    b.load_audio([(0.00, 0.30), (10.17, 10.60), (18.16, 18.56), (23.40, 23.90), (26.60, 27.10),
                  (35.60, 36.10), (40.70, 41.20), (47.60, 48.10), (51.90, 52.28), (54.90, 55.40),
                  (60.70, 61.20), (65.90, 66.40), (81.57, 82.00), (84.60, 85.10), (94.60, 95.10),
                  (106.60, 107.10), (113.60, 114.10), (121.60, 122.10), (133.60, 134.10),
                  (144.42, 144.89), (148.60, 149.10), (156.60, 157.10), (164.60, 165.10),
                  (175.14, 175.60), (181.41, 181.80), (186.60, 187.10), (200.60, 201.10),
                  (209.60, 210.10), (216.92, 217.54), (220.68, 221.22), (224.08, 224.76),
                  (227.31, 227.62), (229.27, 229.49), (235.46, 235.91), (243.66, 244.18),
                  (247.46, 248.28), (251.06, 251.74), (255.50, 256.00), (263.60, 264.10),
                  (275.60, 276.10), (287.99, 288.79), (296.60, 297.10), (305.42, 306.06),
                  (312.48, 316.00)])

    b.keep(0, BD1_IN, "Notebook drawings: text into tokens, and a token ID that says nothing about meaning")
    b.keep(BD1_IN, DEL_A_IN, "An ID Identifies You. It Doesn't Describe You.", "bd1")
    b.keep(DEL_A_OUT, BD1_OUT, "An ID Identifies You. It Doesn't Describe You.", "bd1",
           video_from=BD1_IN + (DEL_A_IN - BD1_IN))
    b.keep(BD1_OUT, BD2_IN, "Notebook drawings: a token ID is not enough, and the taste test is set up")
    b.keep(BD2_IN, DEL_B_IN, "Meaning Becomes an Ordered Row of Numbers", "bd2")
    b.keep(DEL_B_OUT, BD2_OUT, "Meaning Becomes an Ordered Row of Numbers", "bd2", video_from=BD2_R2)
    b.keep(BD3_IN, BD3_OUT, "One New Dimension Separates Similar Meanings", "bd3")
    b.keep(BD3_OUT, BD4_IN, "Notebook drawing: more dimensions separate similar meanings")
    b.keep(BD4_IN, GA_AT, "From Taste Ratings to AI Embeddings", "bd4")
    b.graft(ROLL2, GA_IN, GA_OUT, "'We explicitly named our traits, like sweet or fizz. An AI has no dimension labels at all.' (roll 2) - Board 4's last two rows, whose taste-test side roll 1 leaves unspoken",
            "labels", picture_from=GA_AT, visual="bd4", gain_db=GAIN_R2)
    b.keep(GA_BACK, BD4_OUT, "From Taste Ratings to AI Embeddings", "bd4", video_from=BD4_R2)
    b.keep(BD4_OUT, BD5_IN, "Notebook drawing: flavour on one side, the structure of language on the other")
    b.keep(BD5_IN, GB_AT, "Inside a Real Model", "bd5")
    b.graft(ROLL2, GB_IN, GB_OUT, "'It stores one embedding for every single token, meaning cat sits right alongside rows for dog, latte, truck, and bicycle.' (roll 2) - names the neighbours roll 1 skips, and drops its 'master ledger'",
            "neighbours", picture_from=GB_AT, visual="bd5", gain_db=GAIN_R2)
    b.keep(GB_BACK, DEL_C_IN, "Inside a Real Model", "bd5", video_from=BD5_R2)
    b.keep(DEL_C_OUT, BD5_OUT, "Inside a Real Model", "bd5", video_from=BD5_R3)
    b.keep(BD5_OUT, CLOSE_IN, "Notebook drawing: unbelievable splits into three pieces, each with its own row",
           video_from=BD5_PIC, video_end=CLOSE_IN)
    b.mark_close_start()
    b.close(CLOSE_IN, CLOSE_AUDIO_OUT, tail=150)
    b.finish_audio()

    # Board 1: a photograph with a banner, held at FULL VIEW for its whole run on David's direction
    # (2026-09-22) - no walk, no dive. The badge walk it used to do has nothing left to walk to anyway:
    # the narration that read the four badge numbers aloud is the first of the deletions. No rings on the
    # picture itself (Training Bias v6); only the takeaway banner rings, as verbatim line 1 is spoken.
    b.board("bd1", STUDENT, BD1_IN, BD1_IN + BD1_LEG, "compact", [
        target("takeaway banner", (BD1_IN + (DEL_A_IN - BD1_IN) + (fr(47.70) - DEL_A_OUT)) / FPS,
               list(BD1_BANNER), NEUTRAL, radius=22),
    ], push=False)

    # Board 2 (compact): each drink's row as its six scores are read, then the banner - which is verbatim
    # line 2, so the ring lands exactly as roll 1 speaks it.
    # The banner is carried as an ordinary target, not banner_at, because the narration keeps teaching
    # the table after the takeaway line and the rings have to keep moving with it.
    b.board("bd2", MEANING, BD2_IN, BD2_OUT, "compact", [
        target("Coke's row", 85.10, list(BD2_COKE), NEUTRAL, radius=18),
        target("Coffee's row", 95.10, list(BD2_COFFEE), NEUTRAL, radius=18),
        # Everything below sits after coffee's scores were cut, so each onset is given in the leg's own
        # frame space. The banner now lands on "Each position always means the same thing." at 109.70,
        # which is where the sentence begins once its "Because we keep the columns aligned," is gone.
        target("takeaway banner", bd2(109.70), list(BD2_BANNER), NEUTRAL, radius=22),
        target("Coke, 9, 1 and 10", bd2(114.20), list(BD2_COKE_THREE), NEUTRAL, radius=18),
        target("Coke and all its values", bd2(123.20), list(BD2_COKE_FULL), NEUTRAL, radius=18),
        target("the dimension headings", bd2(128.30), list(BD2_HEADINGS), NEUTRAL, radius=18),
        target("one value", bd2(131.60), list(BD2_ONE_VALUE), NEUTRAL, radius=14),
        target("the row as a whole", bd2(134.50), list(BD2_COKE_FULL), NEUTRAL, radius=18),
    ], push=False)

    # Board 3 (compact): Coke, then Pepsi matching it, then coffee; the banner is verbatim line 4.
    b.board("bd3", NEWDIM, BD3_IN, BD3_OUT, "compact", [
        target("Pepsi, the third drink", 147.50, list(BD3_PEPSI_NAME), NEUTRAL, radius=18),
        target("Pepsi's first six values", 149.60, list(BD3_PEPSI_SIX), NEUTRAL, radius=18),
        target("the CITRUS heading", 162.00, list(BD3_CITRUS_HEAD), NEUTRAL, radius=16),
        target("Pepsi scores 10 on Citrus", 166.80, list(BD3_PEPSI_CITRUS), NEUTRAL, radius=14),
        target("Coke scores 1", 169.10, list(BD3_COKE_CITRUS), NEUTRAL, radius=14),
        target("Coffee scores 0", 170.60, list(BD3_COFFEE_CITRUS), NEUTRAL, radius=14),
        target("takeaway banner", 172.30, list(BD3_BANNER), NEUTRAL, radius=22),
    ], push=False)

    # Board 4 (dense): one ring per comparison row as the narration walks it. The graft covers rows four
    # and five together, so they ring as one combined point; the banner is verbatim line 6.
    b.board("bd4", TASTE, BD4_IN, BD4_IN + BD4_LEG, "dense", [
        dict(target("What gets a row", 193.10, list(BD4_R[0]), NEUTRAL), cam=list(BD4_R[0])),
        dict(target("Dimensions per row", 201.10, list(BD4_R[1]), NEUTRAL), cam=list(BD4_R[1])),
        dict(target("Values", 207.10, list(BD4_R[2]), NEUTRAL), cam=list(BD4_R[2])),
        dict(target("What they capture and Dimension labels", GA_AT / FPS, list(BD4_LABEL_ROWS), NEUTRAL),
             cam=list(BD4_LABEL_ROWS)),
    ], banner_at=(BD4_R2 + (fr(224.76) - GA_BACK)) / FPS,
       pullback_at=(BD4_R2 + (fr(224.76) - GA_BACK)) / FPS,
       banner=BD4_BANNER, per_target_camera=True, lead_camera=True)

    # Board 5 holds the complete illustration for its whole run - no dive - and rings each item as it is
    # named. Onsets after the graft are given in the leg's own frame space, (BD5_IN + leg) / FPS.
    b.board("bd5", MODEL, BD5_IN, BD5_IN + BD5_LEG, "compact", [
        dict(label="the token and its ID", at=238.60, rects=[list(BD5_CATTILE), list(BD5_IDTILE)],
             color=NEUTRAL, radius=18),
        target("the other tokens' rows", (BD5_IN + (GB_AT - BD5_IN)) / FPS, list(BD5_TABLEBODY), NEUTRAL, radius=16),
        target("the first two columns", (BD5_R2 + (fr(248.18) - GB_BACK)) / FPS, list(BD5_FIRSTTWO), NEUTRAL, radius=16),
        target("the d1 to dn headings", (BD5_R2 + (fr(251.74) - GB_BACK)) / FPS, list(BD5_DIMHEAD), NEUTRAL, radius=16),
        # The ring that used to sit here walked cat's values as they were read aloud; that reading is the
        # third deletion, so the board goes straight from the headings to the parameter sentence.
        target("cat's row", bd5(276.80), list(BD5_CATROW), NEUTRAL, radius=16),
        target("the circled 0.45", bd5(279.80), list(BD5_VALUE), NEUTRAL, radius=12),
        target("the whole row is the embedding", bd5(284.00), list(BD5_CATROW), NEUTRAL, radius=16),
    ], push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("embeddings")
    b.manifest({
        "scope_detail": "Stitched production candidate (David, 2026-09-22): roll 1 spine, two grafts from roll 2; live video, rolls, lesson and boards unchanged.",
        "narration_changes": {
            "removed": "roll 1's 3:37.40-3:41.20 ('And these values don't have human labels, like sweet or fizz.') and 4:04.10-4:07.97 ('which acts as a master ledger, storing one embedding for every token.')",
            "graft_labels": "roll 2 2:21.47-2:28.33 replaces the first; audio only over Board 4, +1.4 dB",
            "graft_neighbours": "roll 2 2:58.03-3:05.80 replaces the second; audio only over Board 5, +1.4 dB",
            "engine_outro_removed_from_frame": CLOSE_AUDIO_OUT,
        },
        "verbatim_lines": {
            "all_eight_from_roll_1": [
                "An ID identifies you. It doesn't describe you.",
                "Each position always means the same thing. The number says how much.",
                "The whole row of numbers is a vector.",
                "Six numbers match. The seventh tells them apart.",
                "That row is called an embedding.",
                "Both use a row of numbers to describe something.",
                "AI uses numbers to work with meaning.",
                "Those numbers help AI recognize similarities and differences.",
            ],
        },
        "audio_floors": {"roll_1": -56.4, "roll_2": -62.8,
                         "note": "roll 1 is the noisier bed; each graft steps down 6.4 dB and back up. Both are short and sit under a board."},
        "added_teaching_pauses": [],
        "board_render_covered": [
            {"frames": [BD1_IN, BD1_OUT], "replacement": "canonical An ID Identifies You (the prompt shipped a faceless variant)"},
            {"frames": [BD2_IN, BD2_OUT], "replacement": "canonical Meaning Becomes an Ordered Row of Numbers"},
            {"frames": [BD3_IN, BD3_OUT], "replacement": "canonical One New Dimension Separates Similar Meanings"},
            {"frames": [BD4_IN, BD4_IN + BD4_LEG], "replacement": "canonical From Taste Ratings to AI Embeddings"},
            {"frames": [BD5_IN, BD5_IN + BD5_LEG], "replacement": "canonical Inside a Real Model"},
            {"frames": [CLOSE_IN, CLOSE_AUDIO_OUT], "replacement": "standard close"},
        ],
        "notebook_interleaves": [],
        "longest_unbroken_board_run_seconds": round(max(BD1_OUT - BD1_IN, BD2_OUT - BD2_IN, BD3_OUT - BD3_IN, BD4_LEG, BD5_LEG) / FPS, 2),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)


if __name__ == "__main__":
    main()

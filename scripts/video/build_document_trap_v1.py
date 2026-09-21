#!/usr/bin/env python3
"""Build Document Trap v1 by stitching document-trap-7, -8 and -3 (David, 2026-09-21).

Ten rolls failed to land the lesson's eleven verbatim lines in one take, so this candidate stops
rerolling and assembles the best take of each beat. Roll 7 is the spine: it carries seven of the
eleven lines verbatim and the lesson's order. Four grafts fill what it misses - roll 3's
"the answer wasn't made up" and "the document trap is thinking uploaded means fully read"; roll 8's
explanations of moves one and two and its "asking only about personal fouls" beat; and roll 3's
six-foul result after the moves are applied. Rolls 7, 8 and 3 sit within 0.2-2.6 dB and 167-186 Hz,
so the voice is continuous.

Boards 1-3 are the canonical page assets; roll 8's own retrieval-strategy footage carries the
applied-moves stretch and the verified six-foul quote. Standard close. Live video, rolls, lesson and
boards unchanged.
"""
from pathlib import Path
import argparse, json, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, sha, FPS, W, H, PURPLE, BLUE, TEAL, AMBER, NEUTRAL

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "Prompts/document-trap-7.mp4"      # spine
ROLL8 = ROOT / "Prompts/document-trap-8.mp4"    # moves 1-2, the one-question beat, the applied-moves footage
ROLL3 = ROOT / "Prompts/document-trap-3.mp4"    # lines 3 and 4, the six-foul result
AUDIT = ROOT / "video-audit/document-trap-stitch-2026-09-21"
OUT = AUDIT / "build-v1"
DEST = ROOT / "Prompts/document-trap-v1.mp4"
A = ROOT / "course-assets/document-trap"
UPLOADED, FLOW, MOVES = A / "document-trap-uploaded.jpg", A / "document-trap-flow.jpg", A / "document-trap-moves.jpg"
LIVE, LESSON = A / "document-trap.mp4", ROOT / "lessons/document-trap.md"

# Every row boundary sits inside a measured silence (ffmpeg silencedetect, -40 dB / 0.18 s) in the
# roll that owns that boundary. Spine frames are roll 7's unless named otherwise.
G1_AT, G1_BACK = 1162, 1360      # 0:38.72 (quiet 38.63-38.82) - 0:45.33 (quiet 45.22-45.44): roll 7's
                                 # "This is an incomplete answer. The document trap occurs when we assume
                                 # uploaded means fully read." comes out; roll 3 says both lines as written.
G1_IN, G1_OUT = 1327, 1688       # roll 3 0:44.23 (quiet 44.06-44.40) - 0:56.27 (quiet 56.15-56.39)
BD1_IN, BD1_OUT = 1162, 1640     # An Incomplete Answer, arriving with the graft and held to its banner line
BD1_LEG = (G1_OUT - G1_IN) + (BD1_OUT - G1_BACK)          # 641 leg frames
BD1_RESUME = BD1_IN + (G1_OUT - G1_IN)                    # leg cursor when roll 7's audio comes back
FLOW_IN, FLOW_OUT = 2065, 2935   # 1:08.83 (its own cut) - 1:37.83 (quiet 97.53-97.89), so the banner line
                                 # and "This is how the rulebook mistake happens" both land on the board
MV1_IN, MV1_AT = 3920, 4087      # 2:10.67 (quiet 130.46-130.90), on "This diagram outlines…" - 2:16.23
G2_BACK = 4192                   # 2:19.73 (quiet 139.55-139.90); roll 7's bare "Start with name the section
                                 # and ask one thing." comes out - it names the moves but explains neither.
G2_IN, G2_OUT = 3672, 3941       # roll 8 2:02.40 (quiet 122.24-122.58) - 2:11.37 (quiet 131.18-131.57)
MV1_OUT = MV1_IN + (MV1_AT - MV1_IN) + (G2_OUT - G2_IN)   # leg end for board leg 1
R8_PIC_IN, R8_PIC_END = 4400, 5268   # roll 8's Targeted Prompt Architecture -> Search Phase, to its own cut
G3_AT = 4550                     # 2:31.67 (quiet 151.49-151.82)
G3_IN, G3_OUT = 4763, 4923       # roll 8 2:38.77 (quiet 158.64-158.89) - 2:44.10 (quiet 163.96-164.22)
MV2_IN, MV2_OUT = 4550, 5038     # moves three and four, named and applied; out 2:47.93 (quiet 167.79-168.06)
G4_IN, G4_OUT = 4851, 5132       # roll 3 2:41.70 (quiet 161.41-161.98) - 2:51.05 (quiet 170.86-171.25)
G4_PIC_IN, G4_PIC_END = 5052, 5268   # roll 8's manual paste -> Extracted Verified Quote -> 6-Foul confirmed
MV3_IN, MV3_OUT = 5038, 5162     # the quotation takeaway on the full board; out 2:52.07 (quiet 171.92-172.24)
TAIL_PIC_IN = 5171               # roll 7's own cut into the real-world documents scene
CLOSE_IN, CLOSE_AUDIO_OUT = 5570, 5862   # 3:05.67 (quiet 185.46-185.89); out 3:15.40, before the engine outro

GAIN_R8, GAIN_R3 = -2.6, 0.2     # roll 8 -15.1, roll 3 -17.9, roll 7 -17.7 LUFS (loudnorm, measured)

# Board 1 (1600x1308): a photograph in a card with a title and a banner. No rings on the picture
# (Training Bias v6); the camera walks it and the banner rings on its spoken line.
BD1_PHOTO = [41, 127, 1560, 1138]
BD1_TRAY = [330, 570, 1040, 950]     # the glowing tray holding the few selected pages
BD1_PAGE = [900, 300, 1270, 720]     # the hand-written page: 5 struck through, 6 circled
BD1_BANNER = [40, 1179, 1560, 1266]
# Board 2 (1600x879): three columns inside one shared white box, so each ring runs the box's full
# height, top edge to bottom edge (Hallucination v10), not just the column's text.
FLOW_BOX_T, FLOW_BOX_B = 127, 711
FLOW_COLS = ([64, FLOW_BOX_T, 396, FLOW_BOX_B], [634, FLOW_BOX_T, 966, FLOW_BOX_B], [1204, FLOW_BOX_T, 1536, FLOW_BOX_B])
FLOW_BANNER = [40, 751, 1560, 839]
# Board 3 (1600x1425): four separate rounded white cards on the stage, so each ring hugs that card's
# own measured edges - the illustration tile's x extent and top, the last near-white row above the
# shadow for the bottom (Training Bias v6 / the Context Window v3 correction).
MV_CARDS = ([41, 128, 783, 675], [817, 128, 1559, 675], [41, 709, 783, 1256], [817, 709, 1559, 1256])

def target(label, at, rect, color, radius=20, cam=None):
    d = {"label": label, "at": at, "rects": [rect], "color": color, "radius": radius}
    if cam: d["cam"] = cam
    return d

def prepare_roll8_leg(b, key, start, end, frames):
    """Write leg-<key>.mkv from roll 8's own frames, corner-cleaned, holding its last frame once the
    scene's own cut is reached, so a roll-3 graft can carry roll 8's picture (Context Window v3's
    prepare_live_leg, extended to a raw roll that still has the engine's corner mark)."""
    import cv2, subprocess
    from gemini_mark import clean_frame, glyph_mask
    leg = b.out / f"leg-{key}.mkv"
    if leg.exists(): return
    mask = glyph_mask()
    p = subprocess.Popen([b.ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0", "-c:v", "ffv1",
                          "-level", "3", str(leg)], stdin=subprocess.PIPE)
    cap = cv2.VideoCapture(str(ROLL8)); i = -1; held = None; written = 0
    while written < frames:
        if i < end - 1:
            ok, im = cap.read(); assert ok, ("roll 8 leg source too short", i)
            i += 1
            if i < start: continue
            assert im.shape[:2] == (H, W), im.shape
            held, _ = clean_frame(im, mask)
        p.stdin.write(held.tobytes()); written += 1
    cap.release(); p.stdin.close(); assert p.wait() == 0

def photo_walk_banner(b, key, asset, src_in, leg_frames, moves, photo, banner, banner_at, pullback=30):
    """Camera walk over a photographic board, then a pull-back to the full board with its takeaway
    banner ringed on the line that speaks it. moves: (label, arrive_leg_frame, transit, rect)."""
    import cv2
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
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, ROLL8, ROLL3, UPLOADED, FLOW, MOVES, LESSON])
    b.load_audio([(5.14, 5.54), (9.74, 10.10), (13.11, 13.53), (16.51, 17.06), (25.10, 25.41), (34.75, 34.98),
                  (38.63, 38.82), (40.77, 41.10), (45.22, 45.44), (51.27, 51.55), (54.49, 54.75), (58.94, 59.41),
                  (61.42, 61.74), (68.34, 68.87), (74.03, 74.35), (79.50, 79.95), (85.17, 85.58), (92.18, 92.59),
                  (95.06, 95.44), (97.53, 97.89), (102.90, 103.30), (106.52, 107.02), (111.81, 112.24),
                  (116.09, 116.52), (121.88, 122.20), (125.87, 126.22), (130.46, 130.90), (136.03, 136.46),
                  (139.55, 139.90), (145.82, 146.21), (148.22, 148.54), (151.49, 151.82), (155.32, 155.60),
                  (160.43, 160.75), (162.05, 162.37), (167.79, 168.06), (171.92, 172.24), (175.16, 175.54),
                  (185.46, 185.89), (190.42, 190.83), (192.96, 193.34), (194.34, 194.66)])

    b.keep(0, G1_AT, "Notebook drawings: the 200-page rulebook, the upload, the question and its five-foul answer, the rulebook audit, five against six")
    b.graft(ROLL3, G1_IN, G1_OUT, "'The answer wasn't made up, it was just incomplete.' … 'The document trap is thinking uploaded means fully read.' (roll 3)",
            "lines34", picture_from=BD1_IN, visual="uploaded", gain_db=GAIN_R3)
    b.keep(G1_BACK, BD1_OUT, "An Incomplete Answer", "uploaded", video_from=BD1_RESUME)
    b.keep(BD1_OUT, FLOW_IN, "Notebook drawings: document storage against the context window, the short file, the long file")
    b.keep(FLOW_IN, FLOW_OUT, "Split, Search, Load", "flow")
    b.keep(FLOW_OUT, MV1_IN, "Notebook boards: the skipped tournament exception, the RAG diagram, complete against incomplete retrieval")
    b.keep(MV1_IN, MV1_AT, "Four Moves for Better Retrieval (the framework)", "moves")
    b.graft(ROLL8, G2_IN, G2_OUT, "Moves one and two, named and explained (roll 8)", "moves12",
            picture_from=MV1_AT, visual="moves", gain_db=GAIN_R8)
    b.keep(G2_BACK, G3_AT, "Roll 8: the targeted prompt, then the search filtered down to the tournament rules",
           video_from=R8_PIC_IN, video_src=ROLL8, video_end=R8_PIC_END)
    b.graft(ROLL8, G3_IN, G3_OUT, "'Asking only about personal fouls keeps the system focused entirely on a single question.' (roll 8, over its own isolated-chunk panel)",
            "askone", cover_intro=False, gain_db=GAIN_R8)
    b.keep(MV2_IN, MV2_OUT, "Four Moves for Better Retrieval (share what matters, ask for the quote)", "moves2")
    prepare_roll8_leg(b, "sixfoul", G4_PIC_IN, G4_PIC_END, G4_OUT - G4_IN)
    b.graft(ROLL3, G4_IN, G4_OUT, "The six-foul result (roll 3, over roll 8's verified-quote panel)", "sixfoul",
            reuse_leg=True, gain_db=GAIN_R3)
    b.keep(MV3_IN, MV3_OUT, "Four Moves for Better Retrieval (the quotation takeaway, full board)", "moves3")
    b.keep(MV3_OUT, CLOSE_IN, "Notebook board: leases, contracts, insurance policies and financial-aid letters",
           video_from=TAIL_PIC_IN, video_end=5577)
    b.mark_close_start()
    b.close(CLOSE_IN, CLOSE_AUDIO_OUT, tail=150)
    b.finish_audio()

    # Board 1 (1600x1308, faces, canonical replacement for the faceless upload the prompt shipped):
    # the camera settles on the tray of selected pages, then on the page where six is circled, then
    # pulls back for the banner line.
    photo_walk_banner(b, "uploaded", UPLOADED, BD1_IN, BD1_LEG, [
        ("selected-pages", 130, 30, BD1_TRAY),
        ("five-and-six", 457, 30, BD1_PAGE),
    ], photo=BD1_PHOTO, banner=BD1_BANNER, banner_at=547)

    # Board 2 (1600x879): compact - every column's text reads at full view on the delivered frame.
    b.board("flow", FLOW, FLOW_IN, FLOW_OUT, "compact", [
        target("Split", 74.38, list(FLOW_COLS[0]), PURPLE, radius=18),
        target("Search", 79.94, list(FLOW_COLS[1]), BLUE, radius=18),
        target("Load", 85.58, list(FLOW_COLS[2]), TEAL, radius=18),
    ], banner_at=92.50, banner=FLOW_BANNER)

    # Board 3 (1600x1425): dense - the card body text needs a dive. Three legs, each opening on the
    # full board, so the roll-8 footage between them never returns to a board already zoomed.
    b.board("moves", MOVES, MV1_IN, MV1_OUT, "dense", [
        dict(target("Name the Section", (MV1_IN + 184) / FPS, list(MV_CARDS[0]), PURPLE), cam=list(MV_CARDS[0])),
        dict(target("Ask One Thing", (MV1_IN + 320) / FPS, list(MV_CARDS[1]), BLUE), cam=list(MV_CARDS[1])),
    ])
    b.board("moves2", MOVES, MV2_IN, MV2_OUT, "dense", [
        dict(target("Share What Matters", 153.96, list(MV_CARDS[2]), TEAL), cam=list(MV_CARDS[2])),
        dict(target("Ask for the Quote", 160.90, list(MV_CARDS[3]), AMBER), cam=list(MV_CARDS[3])),
    ])
    # The quotation takeaway wants the whole board back: full view, unmarked - this board's banner is
    # never spoken, and rule 5 keeps an unspoken target unringed.
    b.board("moves3", MOVES, MV3_IN, MV3_OUT, "compact", [], push=False)

    if not args.render_existing:
        b.render_legs()
        for k in b.boards: b.state_sheet(k)
    b.make_close("documenttrap")
    b.manifest({
        "scope_detail": "Stitched production candidate (David, 2026-09-21) after ten rolls: roll 7 spine, four grafts from rolls 8 and 3; live video, rolls, lesson and boards unchanged.",
        "narration_changes": {
            "removed": "roll 7's 0:38.72-0:45.33 ('This is an incomplete answer. The document trap occurs when we assume uploaded means fully read.') and 2:16.23-2:19.73 ('Start with name the section and ask one thing.')",
            "graft_lines34": "roll 3 0:44.23-0:56.27 replaces roll 7's 0:38.72-0:45.33; audio only over Board 1",
            "graft_moves12": "roll 8 2:02.40-2:11.37 replaces roll 7's 2:16.23-2:19.73; audio only over Board 3, -2.6 dB",
            "graft_askone": "roll 8 2:38.77-2:44.10 inserted at 2:31.67 with its own picture, -2.6 dB; no roll 7 words removed",
            "graft_sixfoul": "roll 3 2:41.70-2:51.05 inserted at 2:47.93 over roll 8's verified-quote panel, +0.2 dB; no roll 7 words removed",
            "engine_outro_removed_from_frame": CLOSE_AUDIO_OUT,
        },
        "verbatim_lines": {
            "from_roll_7": ["How many fouls until I'm out of the game?", "Five fouls and you foul out.",
                            "Search decides which parts reach the answer.",
                            "Look in the tournament section. How many personal fouls are allowed? Quote the rule and any exceptions.",
                            "A quotation is useful because you can check it, not because AI quoted it.",
                            "A missing passage can change the answer.", "Ask for the passage. Then check it."],
            "still_off_by_a_word": {
                "The answer wasn't made up. It was incomplete.": "roll 3 says 'wasn't made up, it was just incomplete' - no roll anywhere drops 'just'",
                "Document Trap is thinking 'uploaded' means 'fully read.'": "roll 3 leads with 'The'",
                "Uploading a file doesn't mean AI has read it all.": "roll 7 says 'the AI'; all ten rolls do",
            },
            "taught_but_not_verbatim": {
                "In this example, the tournament rule allows six fouls.": "no roll speaks this line; roll 3's 'uncover the verified six-foul tournament exception' carries the result, and roll 8's panel shows the confirmed six-foul quote under it",
            },
        },
        "added_teaching_pauses": [],
        "board_render_covered": [
            {"frames": [BD1_IN, BD1_OUT], "replacement": "canonical An Incomplete Answer (the prompt shipped a faceless variant)"},
            {"frames": [FLOW_IN, FLOW_OUT], "replacement": "canonical Split, Search, Load"},
            {"frames": [MV1_IN, MV1_OUT], "replacement": "canonical Four Moves for Better Retrieval (leg 1)"},
            {"frames": [MV2_IN, MV2_OUT], "replacement": "canonical Four Moves for Better Retrieval (leg 2)"},
            {"frames": [MV3_IN, MV3_OUT], "replacement": "canonical Four Moves for Better Retrieval (leg 3, full view)"},
            {"frames": [CLOSE_IN, CLOSE_AUDIO_OUT], "replacement": "standard close"},
        ],
        "notebook_interleaves": [
            {"source": "document-trap-8.mp4", "frames": [R8_PIC_IN, R8_PIC_END], "use": "the targeted prompt and the filtered search under roll 7's applied-moves narration"},
            {"source": "document-trap-8.mp4", "frames": [G3_IN, G3_OUT], "use": "the isolated tournament-rule chunk under its own line"},
            {"source": "document-trap-8.mp4", "frames": [G4_PIC_IN, G4_PIC_END], "use": "the manual paste and the confirmed six-foul quote under the six-foul result"},
        ],
        "longest_unbroken_board_run_seconds": round(max(MV1_OUT - MV1_IN, MV2_OUT - MV2_IN, FLOW_OUT - FLOW_IN, BD1_LEG) / FPS, 2),
    })
    print("Prepared", b.total, f"frames ({b.total / FPS:.2f}s)", flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == "__main__":
    main()

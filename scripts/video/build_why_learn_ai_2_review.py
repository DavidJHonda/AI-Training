#!/usr/bin/env python3
"""Why Learn AI? from the Historical Shift roll under EDIT-SPEC.md (2026-09-13). Review only.

v4 (2026-09-14, beat-by-beat rule): roll 1's Where AI Already Lives walk (40.2-95.3; every row with its job and all its examples,
ending on the banner line) replaces roll 2's compressed version (36.8-70.9) under the board; the five dives and the banner follow
roll 1's onsets; roll 1 lowered 2.24 dB to roll 2's speech level. See the comparison REVIEW.md best-of plan.

Base: Prompts/why-learn-ai-2.mp4 (copy of Prompts/Why_Learn_AI__The_Historical_Shift.mp4, 3:40, REPAIR under
NARRATION-REVIEW). Output: videos/why-learn-ai-v3.mp4 (v2 carried four stock photographs; owner call 2026-09-13: replaced by drawings borrowed from the live video). Audit: video-audit/why-learn-ai-repair-2026-09-13/.
One narration cut (3:23.0-3:31.8 "We are looking at a massive economic… one simple truth", which also removes the engine's
close card). Boards: AI Is the Press (faces; not uploaded; compact, still) over "You face two choices… take your place",
keeping Notebook's scribe drawings before it and its Gutenberg press diagram after; Where AI Already Lives (five cards,
dense, dive per card, banner) from its intro sentence; Why You'll Thrive (three cards, dense, banner) from its intro
sentence. Four pauses at idea boundaries. The roll's four stock photographs (vintage computer, factory engine, old computer,
the White House) are replaced by Notebook drawings borrowed from the LIVE video of this lesson (Layout Ready Macintosh;
gear, bolt, globe; the Winning the Race document), picture only, under the roll's own narration. Corner mark cleaned in render.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, BLUE, TEAL, GREEN, AMBER, RED
from build_honesty_privacy_review import cards

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/why-learn-ai-2.mp4'
LIVE = ROOT / 'videos/why-learn-ai.mp4'   # picture-only borrows: Notebook drawings from the current live video
SRC1 = ROOT / 'Prompts/why-learn-ai-1.mp4'   # roll 1: the richer Where AI Already Lives walk (best-of plan, comparison REVIEW.md, 2026-09-14)
OUT = ROOT / 'video-audit/why-learn-ai-repair-2026-09-13'; DEST = ROOT / 'videos/why-learn-ai-v4.mp4'   # v3 shipped 2026-09-13; v4 = v3 + the roll 1 graft
B = {k: ROOT / f'lessons/why-learn-ai-{k}.jpg' for k in ('1-press', '1-everyday', '2-thrive')}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, SRC1, ROOT / 'lessons/why-learn-ai.md', *B.values()])
    b.load_audio([(13.90, 14.22), (23.86, 24.33), (36.48, 36.85), (40.28, 40.61), (53.84, 54.17), (63.87, 64.46), (70.58, 70.91), (111.60, 112.03),
                  (114.46, 114.94), (123.14, 123.75), (133.27, 133.86), (143.19, 143.55), (150.45, 151.04), (202.21, 203.25), (211.15, 211.94), (216.28, 219.75)])
    PRESS, PRESS_OUT = fr(13.9), 727        # "You face two choices…" through "…take your place." (Notebook's choice cards 578-727 replaced; its press diagram from 727 kept)
    LIVES, LIVES_OUT = 1105, fr(70.9)       # Where AI Already Lives: Notebook's cut 0:36.83; roll 2's audio 36.83-70.9 is REPLACED by roll 1's walk; roll 2 resumes at "The great news" (70.9)
    R1_LIVES = (fr(40.2), fr(95.3))         # roll 1 40.20-95.30: "This board shows where AI is already integrated into your day… long before these conversational chat bots arrived." (troughs -57 / -59 dB)
    R1_LEN = R1_LIVES[1] - R1_LIVES[0]; LIVES_LEG_END = LIVES + R1_LEN
    def r1t(t): return (LIVES + (fr(t) - R1_LIVES[0])) / 30   # roll 1 seconds -> the leg's equivalent roll 2 seconds
    THRIVE, THRIVE_OUT = fr(111.9), 4532    # Why You'll Thrive: from "This chart outlines three reasons you'll thrive" (Notebook cut 1:52.10) to Notebook's anvil cut (2:31.07)
    CUT = (fr(203.0), fr(211.8))           # "We are looking at a massive economic… one simple truth." (engine close card 6271 inside)
    CLOSE_END = fr(217.0)                  # "Learn to run it." ends 216.28
    b.keep(0, PRESS, 'Notebook: scribe, manual copying, 1000x disruption')
    b.keep(PRESS, PRESS_OUT, 'B press: two choices, run it', '1-press'); b.pause(30, 'Pause: into AI is everywhere')
    b.keep(PRESS_OUT, LIVES, 'Notebook: Gutenberg press diagram, AI in your tools')
    b.graft(SRC1, R1_LIVES[0], R1_LIVES[1], 'Roll 1 audio: Where AI Already Lives, all five rows with every example, under our board', 'roll1-lives', picture_from=LIVES, gain_db=-2.24, visual='1-everyday')   # roll 1 -15.8 dBFS vs roll 2 -18.1
    b.pause(30, 'Pause: into you can start now')
    b.keep(LIVES_OUT, 2649, 'Notebook: build skills timeline, drafting tools', video_from=2128, video_end=2649)   # picture starts on Notebook's cut (2128), skipping the one frame of its own board render at 2127 (seen in the v4 seam pairs; v3 carried it too)
    b.keep(2649, 2796, 'Live video: Layout Ready Macintosh drawing (replaces the vintage computer photo)', video_from=4854, video_src=LIVE, video_end=5060)
    b.keep(2796, THRIVE, 'Notebook: magazines, design skill, laptop')
    b.keep(THRIVE, fr(150.8), 'B thrive: intro, three reasons, banner', '2-thrive'); b.pause(30, 'Pause: into this has happened before'); b.keep(fr(150.8), THRIVE_OUT, 'B thrive tail', '2-thrive')
    b.keep(THRIVE_OUT, 4707, 'Notebook: anvil to data center')
    b.keep(4707, 5092, 'Live video: gear, bolt, globe drawing (replaces the engine and old computer photos)', video_from=5520, video_src=LIVE, video_end=5856)   # starts as the gear draws in; the last frame holds 1.6s
    b.keep(5092, 5378, 'Notebook: narrow automation vs general-purpose AI')
    b.keep(5378, 5700, 'Live video: Winning the Race document drawing (replaces the White House photo)', video_from=6078, video_src=LIVE, video_end=6353)
    b.keep(5700, CUT[0], 'Notebook: action plan cards'); b.pause(30, 'Pause: before the closing message')
    b.mark_close_start(); b.close(CUT[1], CLOSE_END); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    c5 = cards(B['1-everyday'], 5); c3 = cards(B['2-thrive'], 3)
    b.board('1-press', B['1-press'], PRESS, PRESS_OUT, 'compact', [], min_open=0, push=False)
    b.board('1-everyday', B['1-everyday'], LIVES, LIVES_LEG_END, 'dense',   # onsets are roll 1's, mapped onto the leg
        [T('Recommends', r1t(44.54), c5[0], PURPLE), T('Navigation', r1t(54.24), c5[1], BLUE), T('Face recognition', r1t(62.14), c5[2], RED), T('Voice assistants', r1t(72.98), c5[3], GREEN), T('Chatbots', r1t(80.04), c5[4], AMBER)],
        banner_at=r1t(89.82), pullback_at=r1t(88.7), min_open=0)
    b.board('2-thrive', B['2-thrive'], THRIVE, THRIVE_OUT, 'dense',
        [T('This is your time', 114.94, c3[0], PURPLE), T("You'll move faster", 123.75, c3[1], BLUE), T('Build good habits early', 133.86, c3[2], TEAL)],
        banner_at=143.55, pullback_at=142.3, min_open=0)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('whydeeper')
    b.manifest({'narration_cuts_source_frames': [[LIVES, LIVES_OUT], list(CUT)], 'roll1_lives_frames': list(R1_LIVES), 'cards_detected': {'1-everyday': c5, '2-thrive': c3}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()

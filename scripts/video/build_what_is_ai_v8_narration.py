#!/usr/bin/env python3
"""What Is AI? v8: roll 1's verbatim definition, comparison and closing lines grafted into the live video.

David, 2026-09-26 ("build the review cut"), approving this plan:
  * Opening definition: keep "Ask the Desk. Ask AI." on screen through the definition and ring its banner;
    this also removes Notebook's timeline drawing with invented dates (live 0:19.5-0:28.6).
  * Definition: roll 1's "AI is software built to do things that used to take a human brain." replaces
    live "That happens because AI is software built to perform tasks that used to require a human brain."
  * Comparison: roll 1's "One helps you find something to watch. The other helps you create a story of your own."
    replaces live "One tool helps you … a completely original story."
  * Closing: roll 1's "Two kinds. One picks, one creates. This course is about the one that creates." replaces
    live "There are two kinds of AI. One picks and one creates. This course is exclusively about the AI that creates."
  * Everything else: the live 20260926ship2 file as shipped (explanation, examples, board walk, cutaways).

Source: the live file frozen in the audit dir (already corner-cleaned, so clean_corner=False; one extra encode
generation). Grafts are audio-only (Build.graft picture_from); every splice sits in measured silence (RMS
profiles and medium.en word onsets in REVIEW.md). Gains match roll 1 to the live speech level around each graft.

Usage:
  .video-venv/bin/python scripts/video/build_what_is_ai_v8_narration.py [--prepare-only]
"""
import argparse, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from editspec_build import Build, fr, sha, CLOSE_TAIL  # noqa: E402

LIVE = ROOT / 'course-assets/what-is-ai/what-is-ai.mp4'
LIVE_SHA = '4500df2e3c5b917115470c95375b226150e0cf8c6b17ed5f17821e899b99b438'   # 20260926ship2 (v7)
ROLL1 = ROOT / 'Prompts/what-is-ai-1.mp4'
OUT = ROOT / 'video-audit/what-is-ai-narration-graft-2026-09-26'
SRC = OUT / 'baseline-20260926ship2-live.mp4'
DEST = ROOT / 'Prompts/what-is-ai-v8.mp4'
DESK = ROOT / 'course-assets/what-is-ai/what-is-ai-ask-the-desk.jpg'

# Live timeline (frames). Desk board arrives on Notebook's cut at 370 (as shipped 2026-09-21).
DESK_IN = 370
DEF_CUT = fr(21.90)            # silence after "…to the Berlin Wall." (ends 21.10)
DEF_RESUME = 859               # 28.63 s, after "…human brain." (ends 28.26) and its breath, before "It can understand" (28.90)
COMP_CUT = fr(158.40)          # silence after "…from your request." (157.74), before "One tool" (158.58); banner ring lands 4757
CLOSE_CUT = 4938               # 164.60 s, silence before "There are two kinds" (164.76); live close card at 4941
# Roll 1 (frames)
R_DEF = (fr(36.10), fr(40.30))       # "AI is software built to do things that used to take a human brain." 36.60-40.02
R_COMP = (fr(156.00), fr(161.20))    # "One helps you find something to watch. The other helps you create a story of your own." 156.18-160.86
R_CLOSE = (fr(164.46), fr(170.27))   # "Two kinds. One picks, one creates. This course is about the one that creates." 164.56-169.88
GAIN_COMP, GAIN_CLOSE = 2.0, 3.5     # roll 1 speech 72.2 / 70.9 dB vs live 74.1-74.3 / 75.0 dB (frame RMS > 300)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    assert sha(LIVE) == LIVE_SHA, 'live file changed since the plan was measured'
    OUT.mkdir(parents=True, exist_ok=True)
    if not SRC.exists(): shutil.copy2(LIVE, SRC)
    assert sha(SRC) == LIVE_SHA
    b = Build(ROOT, SRC, OUT, DEST, protected=[LIVE, ROLL1, DESK])
    b.tall_margin = False   # the desk leg shipped 2026-09-21 edge-to-edge (2044x1150 canvas); keep its framing
    b.load_audio([(21.50, 22.50), (163.70, 164.60)])

    b.keep(0, DEF_CUT, 'Live: hook, desk, ask AI, the list')
    head = b.rows.pop()   # one audio row, two pictures: Notebook to the desk cut, then the desk leg
    b.rows += [dict(head, source_end=DESK_IN, end_frame=DESK_IN, label='Live: hook and desk (Notebook)'),
               dict(head, source_start=DESK_IN, start_frame=DESK_IN, label='Desk board: ask AI, the list', visual='desk')]
    def_pic = DEF_CUT
    b.graft(ROLL1, *R_DEF, 'Roll 1: "AI is software built to do things that used to take a human brain."', 'def', picture_from=def_pic, visual='desk')
    desk_out = def_pic + (R_DEF[1] - R_DEF[0])
    b.keep(DEF_RESUME, COMP_CUT, 'Live: four examples through the Maya/Leo scene and "It generated…"')
    b.graft(ROLL1, *R_COMP, 'Roll 1: "One helps you find something to watch. The other helps you create a story of your own."', 'comp',
            picture_from=COMP_CUT, gain_db=GAIN_COMP)
    comp_pic_end = COMP_CUT + (R_COMP[1] - R_COMP[0])
    b.keep(comp_pic_end, CLOSE_CUT, 'Live: silence under the One Picks banner')
    b.mark_close_start()
    b.graft(ROLL1, *R_CLOSE, 'Roll 1: "Two kinds. One picks, one creates. This course is about the one that creates."', 'close',
            picture_from=CLOSE_CUT, gain_db=GAIN_CLOSE)
    b.pause(CLOSE_TAIL, 'Settled close hold')
    b.finish_audio()

    banner_at = (def_pic + round((36.60 - 36.10) * 30)) / 30   # ring on "AI is…" (roll 1 onset 36.60, 0.50 s into the graft)
    b.board('desk', DESK, DESK_IN, desk_out, 'compact', [], banner_at=banner_at, min_open=0, push=False)
    b.render_legs(); b.state_sheet('desk'); b.make_close('llms')
    m = b.manifest({'build_note': 'Audio-changing build: three roll-1 grafts + desk board extended with banner ring.',
                    'live_sha256': LIVE_SHA, 'banner_at_output_s': banner_at, 'gains_db': {'comp': GAIN_COMP, 'close': GAIN_CLOSE}})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', 'desk', DESK_IN, desk_out, 'banner', banner_at, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    b.render(clean_corner=False); print(DEST)


if __name__ == '__main__':
    main()

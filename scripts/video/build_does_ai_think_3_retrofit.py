#!/usr/bin/env python3
"""Does AI Think? v4: board refresh as a visual-only retrofit of the shipped v3 (2026-09-16). Review only.

The raw rolls (Prompts/does-ai-think-1/2.mp4) no longer exist, so the v3 assembly cannot be re-run from pristine sources; this build
takes the finished v3 (course-assets/does-ai-think/does-ai-think.mp4, 6600 frames) as its source, replaces the two board spans and the
close with new legs, and then muxes v3's original audio stream back in untouched (RETROFIT-PLAYBOOK: visual-only, audio copied).
Boards: The Chinese Room is a NEW asset (1600x1310 with a title and banner; v3 used the bare 1536x1024 illustration) — its four
step-callout rects are the v3 rects mapped through the illustration's placement (scale 0.990/0.988, offset 40,128; the "To anyone
outside" panel measured at both sizes confirms it); When You Think / What AI Does is the same 1600x1556 layout with the URL line (text
rows and separators measured identical), so its five row rects are v3's. Ring onsets are v3's roll-2 onsets shifted onto the output
timeline (B1 −7.7 s, B2 −5.7 s; "Step one" 57.68 / "Step two" 64.20 / "When it comes to meaning" 129.90 / "The outputs might look" 184.58
re-heard on the finished file). Output board spans [1389, 2876) and [3669, 5847), close from 6312 (the v3 cut list). Framing at v3
parity (tall_margin off). Corner cleaning off (v3 is already clean).
"""
from pathlib import Path
import argparse, subprocess, sys, hashlib
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr, PURPLE, GREEN, NEUTRAL
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / 'course-assets/does-ai-think/does-ai-think.mp4'    # the shipped v3, sha256 e71f1b610fc45e59…
OUT = ROOT / 'video-audit/does-ai-think-repair-2026-09-16'
RENDER = OUT / 'v4-render.mp4'                                    # picture + re-encoded audio (discarded)
DEST = ROOT / 'Prompts/does-ai-think-v4.mp4'                      # picture from RENDER + v3's audio stream, copied
B = {'1-chinese-room': ROOT / 'course-assets/does-ai-think/does-ai-think-chinese-room.jpg', '2-side-by-side': ROOT / 'course-assets/does-ai-think/does-ai-think-side-by-side.jpg'}
TOTAL = 6600
B1, B1_OUT = 1389, 2876
B2, B2_OUT = 3669, 5847
CLOSE = 6312

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, LIVE, OUT, RENDER, protected=[*B.values()])
    b.tall_margin = False
    b.load_audio([(25.4, 26.8), (37.3, 38.6), (94.5, 95.7), (121.2, 122.4), (193.2, 194.7), (209.3, 210.5), (216.0, 219.9)])   # v3's own pauses (room tone only; the audio is replaced at mux)
    b.keep(0, B1, 'v3 picture: opening drawings (unchanged)')
    b.keep(B1, B1_OUT, 'B1 The Chinese Room (new asset), four step rings', '1-chinese-room')
    b.keep(B1_OUT, B2, 'v3 picture: symbols and prediction, OUTPUT / COMPREHENSION (unchanged)')
    b.keep(B2, B2_OUT, 'B2 When You Think / What AI Does (URL line), five row rings and the banner', '2-side-by-side')
    b.keep(B2_OUT, CLOSE, 'v3 picture: gears, bubble, x, bulb (unchanged)')
    b.mark_close_start(); b.keep(CLOSE, TOTAL, 'Close (canonical closing JPG)'); b.finish_audio()
    T = lambda label, at, r, c: dict(label=label, at=at, rects=[r], cam=r, color=c, radius=18)
    STEPS = [[60, 158, 466, 410], [60, 415, 466, 627], [60, 637, 466, 850], [60, 859, 466, 1116]]   # v3's [[20,30,430,285],[20,290,430,505],[20,515,430,730],[20,740,430,1000]] mapped into the new board
    ROWS = [[60, 672, 1540, 800], [60, 815, 1540, 942], [60, 958, 1540, 1085], [60, 1102, 1540, 1228], [60, 1245, 1540, 1372]]   # unchanged
    d1, d2 = (B1 - 1620) / 30, (B2 - 3840) / 30   # roll-2 seconds -> output seconds
    b.board('1-chinese-room', B['1-chinese-room'], B1, B1_OUT, 'compact',
        [T('Step 1', 65.19 + d1, STEPS[0], PURPLE), T('Step 2', 71.75 + d1, STEPS[1], PURPLE), T('Step 3', 80.70 + d1, STEPS[2], PURPLE), T('To anyone outside', 88.96 + d1, STEPS[3], NEUTRAL)], min_open=0, push=False)
    b.board('2-side-by-side', B['2-side-by-side'], B2, B2_OUT, 'compact',
        [T('Meaning', 135.64 + d2, ROWS[0], GREEN), T('Experience', 145.70 + d2, ROWS[1], GREEN), T('Word choice', 156.01 + d2, ROWS[2], GREEN), T('Beauty', 165.18 + d2, ROWS[3], GREEN), T('Uncertainty', 176.92 + d2, ROWS[4], GREEN)],
        banner_at=190.31 + d2, min_open=0, push=False)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('doesaithink')
    b.manifest({'retrofit_of': str(LIVE), 'retrofit_of_sha256': hashlib.sha256(LIVE.read_bytes()).hexdigest(), 'audio_note': 'copied from the shipped v3 at mux', 'steps_rects_new_board': STEPS})
    print('Prepared', b.total, f'{b.total / 30:.2f}s', {k: (v['src_in'], v['src_out'], v['full_view_frames']) for k, v in b.boards.items()}, 'close', b.close_start, flush=True)
    if args.prepare_only: return
    if RENDER.exists(): RENDER.unlink()
    b.render(clean_corner=False)
    assert not DEST.exists(), f'{DEST} exists; version-suffix instead of overwriting'
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff, '-v', 'error', '-i', str(RENDER), '-i', str(LIVE), '-map', '0:v:0', '-map', '1:a:0', '-c', 'copy', '-movflags', '+faststart', str(DEST)], check=True)
    print(DEST)

if __name__ == '__main__':
    main()

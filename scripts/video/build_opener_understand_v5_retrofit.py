#!/usr/bin/env python3
"""Understand AI opener v5: add the What Kind of Thing Is AI? board, as a visual-only retrofit of the shipped v4 (2026-09-16). Review only.

David 2026-09-16: "The live video is the base. We need to add the board that appears in the lesson. The rest might be okay as is."
The raw rolls (Prompts/understand-opener-3/4.mp4) no longer exist, so this build takes the finished v4
(course-assets/understand-ai-opener/understand-ai-opener.mp4, 4638 frames) as its picture source, replaces two spans, and muxes v4's
original audio stream back in untouched (RETROFIT-PLAYBOOK: visual-only, audio copied).
1. [0, 352): the What Kind of Thing Is AI? card (course-assets/understand-ai-opener/understand-ai-opener-kind.jpg, 1600x900, compact,
   still) over Notebook's data-center opening still, while the narrator reads the card's four lines; each line ringed in the card's gold
   at its spoken onset ("It's not magic" 0.30, "it's not a person" 1.82, "and it's definitely not normal software" 3.12, "It is entirely
   its own kind of thing" 5.96); the last ring holds under "operating by a completely different set of rules"; out on Notebook's own cut
   to its expert drawing (0:11.73, "Sometimes working with AI…").
2. [4410, 4638): the close, now the canonical closing JPG (make_close_board.py --lesson openerfoundations).
Everything else (the Under the Hood board, the section map with its topic dives, Notebook's drawings, the pauses) is v4's picture.
Corner cleaning off (v4 is already clean).
"""
from pathlib import Path
import argparse, subprocess, sys, hashlib
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / 'course-assets/understand-ai-opener/understand-ai-opener.mp4'   # the shipped v4, sha256 e657b34b984d7ceb…
OUT = ROOT / 'video-audit/understand-ai-opener-repair-2026-09-16'
RENDER = OUT / 'v5-render.mp4'
DEST = ROOT / 'Prompts/understand-ai-opener-v5.mp4'
KIND = ROOT / 'course-assets/understand-ai-opener/understand-ai-opener-kind.jpg'
GOLD = '#eccf6b'   # the creed card's own accent (Work With AI opener precedent)
LINES = [[110, 375, 1489, 423], [110, 424, 1489, 472], [110, 472, 1489, 514], [110, 522, 1489, 571]]   # navy card x 84-1515, y 301-598; white text rows 385-413 / 434-462 / 482-504 / 532-561
TOTAL = 4638
K_OUT = 352      # Notebook's cut 0:11.73 to its expert drawing
CLOSE = 4410     # v4's close start (2:27.00)

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, LIVE, OUT, RENDER, protected=[KIND])
    b.tall_margin = False
    b.load_audio([(29.7, 30.5), (35.6, 36.4), (65.3, 66.1), (80.8, 81.6), (140.1, 140.9), (146.1, 146.9), (151.2, 154.5)])   # v4's own pauses (room tone only; the audio is replaced at mux)
    b.keep(0, K_OUT, 'B0 What Kind of Thing Is AI? card, four line rings', 'kind')
    b.keep(K_OUT, CLOSE, 'v4 picture: Notebook drawings, Under the Hood, section map (unchanged)')
    b.mark_close_start(); b.keep(CLOSE, TOTAL, 'Close (canonical closing JPG)'); b.finish_audio()
    T = lambda label, at, r: dict(label=label, at=at, rects=[r], color=GOLD, radius=18)
    b.board('kind', KIND, 0, K_OUT, 'compact',
        [T("It's not magic.", 0.30, LINES[0]), T('Not a person.', 1.82, LINES[1]), T('Not normal software.', 3.12, LINES[2]), T("It's its own kind of thing.", 5.96, LINES[3])],
        min_open=0, push=False)   # the first line is spoken from frame 0: the ring pops in the full view (Edit Spec rule 3)
    b.render_legs()
    for k in b.boards: b.state_sheet(k)
    b.make_close('openerfoundations')
    b.manifest({'retrofit_of': str(LIVE), 'retrofit_of_sha256': hashlib.sha256(LIVE.read_bytes()).hexdigest(), 'audio_note': 'copied from the shipped v4 at mux', 'kind_lines': LINES})
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

#!/usr/bin/env python3
"""AI Brain Break (Layers TRY IT video) from Prompts/quiz-final.mp4 (2026-09-11). Review only.

Quiz video: no course boards, no standard close (exempt). Edits: a one-second matched-tone pause at each of
the six claim boundaries (each on the roll's own scene cut, inside a measured silence); the Notebook
branding after the last line is cut and the pasta illustration is held for two seconds. No narration
changes. Output: videos/ai-brain-break-v1.mp4. Audit: video-audit/ai-brain-break-2026-09-11/.
"""
from pathlib import Path
import argparse, sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, fr

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/quiz-final.mp4'
OUT = ROOT / 'video-audit/ai-brain-break-2026-09-11'; DEST = ROOT / 'videos/ai-brain-break-v1.mp4'

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    b = Build(ROOT, SRC, OUT, DEST, protected=[ROOT / 'videos/transformers-quiz.mp4', ROOT / 'Prompts/ai-brain-break-source.md'])
    sil = [(20.18, 20.83), (40.79, 41.45), (62.12, 62.80), (108.37, 108.89), (141.80, 142.37), (177.93, 178.60)]
    b.load_audio(sil)
    P = [fr(t) for t in (20.5, 41.1, 62.45, 108.6, 142.1, 178.3)]   # inside each silence, just before the roll's own cut
    END = 6109                                                      # the Notebook branding arrives here; narration ended at 3:23.35
    labels = ['Tokens', 'Training', 'Layers', 'Mind-reading', 'Lemon Pie', 'YellGPT', 'Claude-A-Roni']
    prev = 0
    for i, p in enumerate(P):
        b.keep(prev, p, f'{labels[i]}'); b.pause(30, f'Pause: {labels[i]} to {labels[i + 1]}'); prev = p
    b.keep(prev, END, labels[-1]); b.pause(60, 'Hold the pasta (two seconds), branding cut')
    b.finish_audio(); b.render_legs()
    b.manifest(); print('Prepared', b.total, f'{b.total / 30:.2f}s', flush=True)
    if args.prepare_only: return
    b.render(); print(DEST)

if __name__ == '__main__':
    main()

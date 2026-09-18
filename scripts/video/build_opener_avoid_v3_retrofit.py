#!/usr/bin/env python3
"""Avoid Traps opener v3: the current course boards and the canonical close, as a visual-only retrofit of the shipped file (2026-09-18). Review only.

The shipped file (course-assets/avoid-traps-opener/avoid-traps-opener.mp4, 5070 frames) is the 2026-09-08 patch
(build_opener_avoid_patch.py: cut timeline + four board legs from the plan files in scripts/video/paths/, then the 2026-09-08
illustration sync that placed the read-the-water photo). Its raw roll no longer exists, so this build takes the finished file as
its picture source, re-renders the four legs with the shipped plans (same junction frames, rects, colors, camera pushes) from the
current course-assets files, splices them over the same spans with the shipped script's own renderer and splicer, replaces the
close image with the canonical closing board (make_close_board.py --lesson openerprotect, same hold/push/settle timing), and keeps
the shipped audio stream untouched (-c:a copy). Every Notebook span is the shipped picture.

Since the 2026-09-08 ship: the traps card and the read-the-water photo are byte-identical; the section map has the new title
banner (same 1600x871 dimensions, shipped rects verified on it); the close moves from the archived capture to the canonical JPG.
"""
from pathlib import Path
import argparse, json, hashlib, subprocess, sys
import cv2
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_opener_avoid_patch as P
from make_close_board import close_board_copy

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / 'course-assets/avoid-traps-opener/avoid-traps-opener.mp4'
OUT = ROOT / 'video-audit/avoid-traps-opener-repair-2026-09-18'
DEST = ROOT / 'Prompts/avoid-traps-opener-v4.mp4'
# v4 (owner call 2026-09-18): the opening sentence ("You just spent a section under the hood, observing the mechanics...", 0.00-5.90 s)
# is cut so the lesson stands alone; the file starts in the pause before "The same machinery..." (first word at 6.76 s).
# The cut is a hard trim of the shipped picture and sound at this frame; the audio gets a 10 ms fade-in and is re-encoded (aac 192k).
TRIM = 194   # 6.467 s
FF = P.FFMPEG
D = ROOT / 'course-assets/avoid-traps-opener'
SHIPPED_SHA = '3549352541a05e6af648892a5876a9732b4847b975f0b8cc9dc232a6e445ae23'
PLANS = dict(creed=('opener-avoid-creed-highlights.json', D / 'avoid-traps-opener-traps.jpg'),
             water=('opener-avoid-read-water-current.json', D / 'avoid-traps-opener-read-the-water.jpg'),
             map=('opener-avoid-section-map-current.json', D / 'avoid-traps-opener-section-map.jpg'),
             close=('opener-avoid-close-current.json', None))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True); work = OUT / 'work'; work.mkdir(exist_ok=True)
    assert sha(LIVE) == SHIPPED_SHA, 'live file is not the 2026-09-08 ship'
    assert close_board_copy('openerprotect') == ('When AI fails, nothing looks broken.', 'This section teaches you to read the water.')
    protected = [LIVE, ROOT / 'lessons/opener-avoid.md', D / 'avoid-traps-opener-close.jpg', *(p for _, p in PLANS.values() if p)]
    protected = [p for p in protected if p.exists()]; hashes = {str(p): sha(p) for p in protected}
    if not (OUT / 'close.png').exists():
        subprocess.run([sys.executable, str(ROOT / 'scripts/video/make_close_board.py'), '--lesson', 'openerprotect', '--out', str(OUT / 'close.png')], check=True, stdout=subprocess.DEVNULL)
    ci = cv2.imread(str(OUT / 'close.png')); assert ci.shape[:2] == (2160, 3840), ci.shape
    # the shipped plans, image paths pointed at the current course assets (the plan files keep their shipped junctions/rects/cameras)
    plans = {}
    for key, (name, asset) in PLANS.items():
        cfg = json.loads((ROOT / 'scripts/video/paths' / name).read_text())
        cfg['image'] = str(asset.relative_to(ROOT)) if asset else str(OUT / 'close.png')
        for st in cfg['states']: st['start_frame'] -= TRIM; st['end_frame'] -= TRIM   # shipped junctions on the trimmed timeline
        p = OUT / f'plan-{key}.json'; p.write_text(json.dumps(cfg, indent=2) + '\n'); plans[key] = p
    # the trimmed base: shipped picture and sound from TRIM on (audio re-encoded once, 10 ms fade-in at the new head)
    base = OUT / 'base-trimmed.mp4'; total = P.OUTPUT_FRAMES - TRIM
    if not base.exists():
        subprocess.run([FF, '-y', '-hide_banner', '-loglevel', 'error', '-i', str(LIVE), '-filter_complex',
                        f'[0:v]trim=start_frame={TRIM},settb=1/30,setpts=N/(30*TB),setsar=1,format=yuv420p[v];[0:a]atrim=start={TRIM / 30:.9f},asetpts=PTS-STARTPTS,afade=t=in:st=0:d=0.01[a]',
                        '-map', '[v]', '-map', '[a]', '-r', '30', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(base)], check=True)
        n, fps = P.frame_count(base); assert n == total and abs(fps - 30) < .001, (n, fps)
    P.OUTPUT_FRAMES = total
    # Only the spans whose picture changed are re-rendered: the section map (new title banner) and the close (canonical board).
    # The traps card and the read-the-water photo are byte-identical to the ship-time files, so their shipped picture stays
    # (the water leg was composed by the 2026-09-08 illustration-sync build, not by its plan file here; re-rendering it from the
    # plan would change its framing for no reason).
    # The creed card is unchanged, but the shipped file leaks two frames of Notebook's own pale rendering of it (1403-1404)
    # before the board leg starts at 1405 (transition_guard island, found 2026-09-18). The creed leg re-renders identically
    # from its plan (mean |diff| 0.2 vs the shipped leg), so it is re-rendered with its first state starting at 1403 to cover them.
    cfg = json.loads(plans['creed'].read_text()); cfg['states'][0]['start_frame'] = 1403 - TRIM; plans['creed'].write_text(json.dumps(cfg, indent=2) + '\n')
    SPLICE = ('creed', 'map', 'close')
    walks = [P.render_plan(plans[k], work) for k in SPLICE]
    spans = [dict(key=k, start=w['start'], end=w['end'], labels=w['labels'], junctions=w['junctions']) for k, w in zip(SPLICE, walks)]
    assert [(s['start'], s['end']) for s in spans] == [(1403 - TRIM, 2183 - TRIM), (3620 - TRIM, 4735 - TRIM), (4735 - TRIM, 5070 - TRIM)], spans
    manifest = dict(output=str(DEST), source=str(LIVE), retrofit_of_sha256=SHIPPED_SHA, fps=30, total_frames=P.OUTPUT_FRAMES, trim_frames=TRIM, board_spans=spans,
                    shipped_spans_kept=[dict(key='water', start=3243 - TRIM, end=3410 - TRIM)], island_covered=dict(frames=[1403 - TRIM, 1405 - TRIM], by='creed leg first state'),
                    audio=dict(note='shipped audio from 6.467 s on, 10 ms fade-in, re-encoded aac 192k (audio-changing build: opening sentence cut)', cut=dict(source_seconds=[0, TRIM / 30], text='You just spent a section under the hood, observing the mechanics that make artificial intelligence possible.')),
                    assets={k: dict(path=str(a.relative_to(ROOT)), sha256=sha(a)) for k, (_, a) in PLANS.items() if a},
                    close_asset=dict(path='course-assets/avoid-traps-opener/avoid-traps-opener-close.jpg', sha256=sha(D / 'avoid-traps-opener-close.jpg')),
                    protected_hashes=hashes,
                    scope='Review only; retrofit of the shipped 2026-09-08 file (current course boards + canonical close) with the opening sentence cut; live unchanged')
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared legs', [(s['key'], s['start'], s['end']) for s in spans], 'total', total, flush=True)
    if args.prepare_only: return
    assert not DEST.exists(), f'{DEST} exists; version-suffix instead of overwriting'
    P.OUTPUT = DEST; P.splice_boards(base, walks)
    m = json.load(open(OUT / 'edit-manifest.json')); m['render_sha256'] = sha(DEST); m['protected_files_unchanged'] = {k: sha(k) == v for k, v in hashes.items()}; assert all(m['protected_files_unchanged'].values())
    (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2) + '\n'); print(DEST, flush=True)

if __name__ == '__main__':
    main()

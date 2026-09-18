#!/usr/bin/env python3
"""Hallucination v3: the current course boards and the canonical close, as a visual-only retrofit of the shipped file (2026-09-18). Review only.

The shipped file (course-assets/hallucination/hallucination.mp4, 7018 frames) is the 2026-09-06 reroll build
(build_hallucination_reroll_review.py: four board legs with course-native rings and dives, two audio cuts, one pause, standard close)
plus the 2026-09-08 illustration sync (build_avoid_illustration_sync.py: the Real Text photo board over 3724-3974). Its raw roll
(Prompts/hallucination-reroll.mp4) no longer exists, so this build takes the finished file as its picture source, re-renders the four
board legs with the shipped scripts' own leg makers and renderers (same junctions, rects, accents, cameras and moves) from the current
course-assets JPGs, re-renders the photo board with the sync compositor (banner rect re-detected on the current file), replaces the
close with the canonical closing board (make_close_board.py --lesson hallucination, same 48/150 push), splices every leg over its
shipped output span, and muxes the shipped audio stream back in untouched. Every Notebook span is the shipped picture.

Since the ships: all four boards changed only by the website credit line (same dimensions; every rect verified on the current files);
the Real Text board is the current JPG version of the synced PNG; the close moves from the archived capture to the canonical JPG.
"""
from pathlib import Path
import argparse, json, hashlib, subprocess, sys
import cv2
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_your_choices_reroll_review as common
import build_avoid_illustration_sync as sync
from build_work_changes_hybrid import render_leg
from make_close_board import close_board_copy

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / 'course-assets/hallucination/hallucination.mp4'
OUT = ROOT / 'video-audit/hallucination-repair-2026-09-18'
DEST = ROOT / 'Prompts/hallucination-v3.mp4'
D = ROOT / 'course-assets/hallucination'
SHIPPED_SHA = '0198c0dc16dc880fe4344f31cfd8f0037f95a82d5536c56bb40e29346d98ae88'
TOTAL, CLOSE_OUT = 7018, 6612
at = common.at
# the shipped reroll build's source-frame mapping (two audio cuts, one 30-frame pause after the second)
CUTS = ((2325, 2475), (3327, 3575)); common.CUTS = CUTS; base_mapping = common.output_frame
def mapped(source_frame): return base_mapping(source_frame) + (30 if source_frame >= CUTS[1][1] else 0)
common.output_frame = mapped
CLOSE_START = 6980
P, B, T, A, VP = '#4f2fc4', '#1652f0', '#0e8f86', '#a9760c', '#6e51ff'
CHECK_RECTS = [(70, 175, 500, 718), (585, 175, 1015, 718), (1100, 175, 1530, 718)]   # the shipped complete_step_bounds (v2 manifest)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def legs():
    out = []
    def add(name, asset, points, states):
        leg = common.make_leg(name, asset, tuple(points), tuple(states)); out.append((mapped(points[0]), mapped(points[-1]), leg))
    add('example', D / 'hallucination-example.jpg', (0, at(1), at(9.1), at(34.25), at(45.8), 1908), (
        ('full', None, VP, None, 0), ('your-full-prompt', (605, 203, 1520, 338), VP, None, 0), ('full-ai-bubble', (80, 401, 989, 618), VP, (550, 490, 1180), 24),
        ('full-takeaway', (40, 697, 1560, 786), VP, None, 24), ('example-in-context', None, VP, None, 0)))
    add('why', D / 'hallucination-why-ai-makes-things-up.jpg', (1908, at(69.3), 2475, at(90.5), at(99.6), 3576), (
        ('full', None, VP, None, 0), ('learns-from-text', (56, 164, 362, 794), P, (209, 479, 1200), 24), ('one-token', (452, 164, 756, 794), B, (604, 479, 1200), 24),
        ('keeps-answering', (844, 164, 1150, 794), T, (997, 479, 1200), 24), ('probable-not-true', (1234, 164, 1548, 794), A, (1391, 479, 1200), 24)))
    add('check-claim', D / 'hallucination-check-claim.jpg', (4968, at(169.4), at(187.35), at(205.05), at(222.35), CLOSE_START), (
        ('full', None, VP, None, 0), ('notice-the-claim', CHECK_RECTS[0], P, (285, 446.5, 1050), 24), ('find-the-source', CHECK_RECTS[1], B, (800, 446.5, 1050), 24),
        ('check-the-match', CHECK_RECTS[2], T, (1315, 446.5, 1050), 24), ('three-step-recap', None, VP, None, 24)))
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--prepare-only', action='store_true'); args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True); (OUT / 'states').mkdir(exist_ok=True); work = OUT / 'work'; work.mkdir(exist_ok=True)
    assert sha(LIVE) == SHIPPED_SHA, 'live file is not the 2026-09-08 ship'
    assert close_board_copy('hallucination') == ('Hallucinations sound like every other AI answer.', 'When something doesn’t add up, trace the claim to its source.')
    assets = dict(example=D / 'hallucination-example.jpg', why=D / 'hallucination-why-ai-makes-things-up.jpg', real_text=D / 'hallucination-glue-on-pizza.jpg',
                  check_claim=D / 'hallucination-check-claim.jpg', close=D / 'hallucination-close.jpg')
    protected = [LIVE, ROOT / 'lessons/hallucination.md', *assets.values()]; protected = [p for p in protected if p.exists()]; hashes = {str(p): sha(p) for p in protected}
    renders = []; spans = []
    for a, b, leg in legs():
        path = work / f'{leg.name}.mkv'; print('Rendering', leg.name, a, b, flush=True); render_leg(leg, path); assert common.frame_count(path) == leg.frames == b - a
        cursor = a; states = []
        for st in leg.states:
            states.append(dict(label=st.label, start=cursor, end=cursor + st.frames, rect=st.ring, color=st.color, camera=st.camera, move=st.move_frames)); cursor += st.frames
        renders.append((a, b, path)); spans.append(dict(key=leg.name, start=a, end=b, asset=str(leg.board.relative_to(ROOT)), states=states))
    # the Real Text photo board: the 2026-09-08 sync leg (full illustration 3724-3847, takeaway ring 3847-3974), banner rect re-detected on the current JPG
    rt = dict(asset=str(assets['real_text']), start=3724, end=3974, states=[sync.state(3724, 'full-illustration'), sync.state(3847, 'full-takeaway', sync.gold_bounds(assets['real_text']))], push=0)
    path = work / 'real-text.mkv'; print('Rendering real-text', flush=True); sync.render_leg(rt, path, OUT); assert common.frame_count(path) == 250
    renders.append((3724, 3974, path)); spans.append(dict(key='real-text', start=3724, end=3974, asset=str(assets['real_text'].relative_to(ROOT)), states=rt['states']))
    # canonical close, rendered through the shipped close mover (1600x900 stage, 48-frame hold, 150-frame push to 1.2x)
    if not (OUT / 'close.png').exists():
        subprocess.run([sys.executable, str(ROOT / 'scripts/video/make_close_board.py'), '--lesson', 'hallucination', '--out', str(OUT / 'close.png')], check=True, stdout=subprocess.DEVNULL)
    close_png = work / 'close-1600.png'; cv2.imwrite(str(close_png), cv2.resize(cv2.imread(str(OUT / 'close.png')), (1600, 900), interpolation=cv2.INTER_AREA))
    common.BOARDS['close'] = close_png; close_path = work / 'close.mkv'; common.render_close(close_path, TOTAL - CLOSE_OUT)
    renders.append((CLOSE_OUT, TOTAL, close_path)); spans.append(dict(key='close', start=CLOSE_OUT, end=TOTAL, asset='course-assets/hallucination/hallucination-close.jpg', states=[]))
    renders.sort(key=lambda r: r[0]); assert [(a, b) for a, b, _ in renders] == [(0, 1908), (1908, 3208), (3724, 3974), (4600, 6612), (6612, 7018)], renders
    manifest = dict(output=str(DEST), source=str(LIVE), retrofit_of_sha256=SHIPPED_SHA, fps=30, total_frames=TOTAL, board_spans=spans,
                    assets={k: dict(path=str(p.relative_to(ROOT)), sha256=sha(p)) for k, p in assets.items()}, audio_note='copied from the shipped file at mux (-c:a copy)',
                    protected_hashes=hashes, scope='Review only; visual-only retrofit of the shipped 2026-09-06/08 file (current course boards + canonical close); live unchanged')
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Prepared', [(s['key'], s['start'], s['end']) for s in spans], flush=True)
    if args.prepare_only: return
    assert not DEST.exists(), f'{DEST} exists; version-suffix instead of overwriting'
    graph, vl = [], []; cursor = 0
    cmd = [common.FFMPEG, '-y', '-hide_banner', '-loglevel', 'error', '-i', str(LIVE)]
    for i, (a, b, path) in enumerate(renders, 1):
        if cursor < a: common.source_video(graph, vl, cursor, a)
        common.rendered_video(graph, vl, i, b - a); cursor = b; cmd += ['-i', str(path)]
    assert cursor == TOTAL
    graph.append(''.join(vl) + f'concat=n={len(vl)}:v=1:a=0,format=yuv420p[outv]')
    cmd += ['-filter_complex', ';'.join(graph), '-map', '[outv]', '-map', '0:a:0', '-r', '30', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(DEST)]
    print('Encoding', flush=True); subprocess.run(cmd, check=True)
    assert common.frame_count(DEST) == TOTAL
    m = json.load(open(OUT / 'edit-manifest.json')); m['render_sha256'] = sha(DEST); m['protected_files_unchanged'] = {k: sha(k) == v for k, v in hashes.items()}; assert all(m['protected_files_unchanged'].values())
    (OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2) + '\n'); print(DEST, flush=True)

if __name__ == '__main__':
    main()

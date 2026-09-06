#!/usr/bin/env python3
"""Approved Hallucination reroll repairs, from pristine source; review only."""
from pathlib import Path
import json
import subprocess
import sys
import tempfile

import cv2

import build_your_choices_reroll_review as common
from build_work_changes_hybrid import render_leg

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Prompts/hallucination-reroll.mp4'
OUTPUT = ROOT / 'Prompts/hallucination-reroll-patched-v2.mp4'
LIVE = ROOT / 'videos/hallucination.mp4'
AUDIT = ROOT / 'video-audit/hallucination-reroll-review-2026-09-06-v2'
at = common.at
# Quiet-frame cuts retain complete preceding words and the following onset.
CUTS = ((2325, 2475), (3327, 3575))
common.CUTS = CUTS
base_mapping = common.output_frame
PAUSE_FRAMES = 30


def mapped(source_frame):
    return base_mapping(source_frame) + (PAUSE_FRAMES if source_frame >= CUTS[1][1] else 0)


common.output_frame = mapped
SOURCE_FRAMES = 7476
END = 7386  # First Notebook end-card frame; omit it and everything after it.
CLOSE_START = 6980
P, B, T, A, VP = '#4f2fc4', '#1652f0', '#0e8f86', '#a9760c', '#6e51ff'


def replacements():
    result = []
    def add(name, asset, points, states):
        leg = common.make_leg(name, ROOT / asset, tuple(points), tuple(states))
        result.append((points[0], points[-1], leg))
    # Whole bubbles/banner, not estimated text rectangles.
    add('example', 'illustrations/hallucination-example-v2.jpg',
        (0, at(1), at(9.1), at(34.25), at(45.8), 1908), (
            ('full', None, VP, None, 0),
            ('your-full-prompt', (605,203,1520,338), VP, None, 0),
            ('full-ai-bubble', (80,401,989,618), VP, (550,490,1180), 24),
            ('full-takeaway', (40,697,1560,786), VP, None, 24),
            ('example-in-context', None, VP, None, 0)))
    # Four complete illustrated steps. Keep all text vertically in frame.
    add('why', 'illustrations/hallucination-why-v2.jpg',
        (1908, at(69.3), 2475, at(90.5), at(99.6), 3576), (
            ('full', None, VP, None, 0),
            ('learns-from-text', (56,164,362,794), P, (209,479,1200), 24),
            ('one-token', (452,164,756,794), B, (604,479,1200), 24),
            ('keeps-answering', (844,164,1150,794), T, (997,479,1200), 24),
            ('probable-not-true', (1234,164,1548,794), A, (1391,479,1200), 24)))
    # Native pizza and search scenes stay. Replace the entire Reddit graphic.
    add('real-text', 'illustrations/hallucination-real-text-v3.jpg',
        (4092, at(140.5), 4342), (
            ('full-illustration', None, VP, None, 0),
            ('full-takeaway', (40,1187,1560,1276), VP, None, 0)))
    # Canonical bounds come from board-review-hallucination/geometry.json.
    geometry = json.loads((ROOT/'board-review-hallucination/geometry.json').read_text())
    rects = [tuple(s['complete_step_bounds']) for s in geometry['steps']]
    add('check-claim', 'illustrations/hallucination-check-claim-v1.jpg',
        (4968, at(169.4), at(187.35), at(205.05), at(222.35), CLOSE_START), (
            ('full', None, VP, None, 0),
            ('notice-the-claim', rects[0], P, (285,446.5,1050), 24),
            ('find-the-source', rects[1], B, (800,446.5,1050), 24),
            ('check-the-match', rects[2], T, (1315,446.5,1050), 24),
            ('three-step-recap', None, VP, None, 24)))
    return result


def main():
    if OUTPUT.exists():
        raise SystemExit('Candidate already exists; choose a new versioned filename.')
    AUDIT.mkdir(parents=True, exist_ok=True)
    assert common.frame_count(SOURCE) == SOURCE_FRAMES
    source_hash, live_hash = common.file_md5(SOURCE), common.file_md5(LIVE)
    items = replacements()
    expected = mapped(END)
    boundaries = {mapped(a): 'audio-cut-'+str(i+1) for i,(a,b) in enumerate(CUTS)}
    boundaries[mapped(CUTS[1][1])] = 'end-one-second-pause'
    states = []
    with tempfile.TemporaryDirectory(prefix='hallucination-reroll-', dir='/private/tmp') as folder:
        work = Path(folder)
        renders = []
        for a,b,leg in items:
            path = work / (leg.name+'.mkv')
            print('Rendering', leg.name, flush=True)
            render_leg(leg, path)
            assert common.frame_count(path) == leg.frames
            renders.append((a,b,path,leg.frames))
            if mapped(a) > 0:
                boundaries[mapped(a)] = 'to-'+leg.name
            boundaries[mapped(b)] = 'from-'+leg.name
            cursor = mapped(a)
            for state in leg.states:
                states.append({'name':leg.name+'/'+state.label,
                    'output_frame':cursor+min(state.frames-1,max(30,state.move_frames+5)),
                    'rect':state.ring,'color':state.color,'camera':state.camera,
                    'color_source':'neutral_video_purple' if state.color==VP else 'card_locked_accent'})
                cursor += state.frames
        close = cv2.imread(str(ROOT/'lessons/hallucination-5-close.jpg'))
        close_png = work/'close.png'
        cv2.imwrite(str(close_png), cv2.resize(close,(1600,900),interpolation=cv2.INTER_AREA))
        common.BOARDS['close'] = close_png
        close_video = work/'close.mkv'
        common.render_close(close_video, expected-mapped(CLOSE_START))
        renders.append((CLOSE_START,END,close_video,expected-mapped(CLOSE_START)))
        boundaries[mapped(CLOSE_START)] = 'to-standard-close'
        # Also audit the preserved native illustration -> native search transition.
        boundaries[mapped(3727)] = 'native-pizza-to-search'
        states.extend([{'name':'close/full','output_frame':mapped(CLOSE_START)+20},
                       {'name':'close/settled','output_frame':expected-20}])
        graph, vl, al = [], [], []
        def native(a,b):
            for c,d in CUTS:
                if a < c < b:
                    common.source_video(graph,vl,a,c)
                if c <= a < d or a < c < b:
                    a = min(b,d)
            if b > a:
                common.source_video(graph,vl,a,b)
        cursor = 0
        for i,(a,b,path,n) in enumerate(renders,1):
            native(cursor,a)
            common.rendered_video(graph,vl,i,n)
            cursor = b
        assert cursor == END
        graph.append(''.join(vl)+f'concat=n={len(vl)}:v=1:a=0,format=yuv420p[outv]')
        cursor = 0
        for a,b in CUTS:
            common.source_audio(graph,al,cursor,a)
            if (a,b) == CUTS[1]:
                # Mirror-tile quiet source room tone, not silence or a breath.
                # The current why-board state also gains these same 30 frames.
                graph.extend([
                    '[0:a]atrim=start=119:end=119.15,asetpts=PTS-STARTPTS,'
                    'aresample=44100,aformat=sample_fmts=fltp:channel_layouts=mono,'
                    'asplit=2[rtf][rtr]',
                    '[rtr]areverse[rtrev]',
                    '[rtf][rtrev]concat=n=2:v=0:a=1,aloop=loop=3:size=13230,'
                    'atrim=duration=1,asetpts=PTS-STARTPTS[one_second_pause]'])
                al.append('[one_second_pause]')
            cursor = b
        common.source_audio(graph,al,cursor,END)
        graph.append(''.join(al)+f'concat=n={len(al)}:v=0:a=1[outa]')
        command = [common.FFMPEG,'-y','-hide_banner','-loglevel','error','-i',str(SOURCE)]
        for a,b,path,n in renders:
            command += ['-i',str(path)]
        command += ['-filter_complex',';'.join(graph),'-map','[outv]','-map','[outa]',
            '-r','30','-c:v','libx264','-crf','18','-preset','medium','-pix_fmt','yuv420p',
            '-c:a','aac','-b:a','192k','-movflags','+faststart',str(OUTPUT)]
        print('Encoding review candidate', flush=True)
        subprocess.run(command,check=True)
    assert common.frame_count(OUTPUT) == expected
    assert common.file_md5(SOURCE) == source_hash
    assert common.file_md5(LIVE) == live_hash
    manifest = {'source':str(SOURCE),'source_md5':source_hash,'output':str(OUTPUT),
        'output_frames':expected,'seconds':expected/30,
        'cuts':[{'source_start':a/30,'source_end':b/30,'output_frame':mapped(a)} for a,b in CUTS],
        'pause':{'output_start_frame':mapped(CUTS[1][0]),'frames':PAUSE_FRAMES,
                 'source_room_tone':[119.0,119.15],'visual':'hold current why-board state'},
        'closing_narration':'Original sentence retained per user fallback; no word splice.',
        'replacements':[{'name':leg.name,'source_start':a/30,'source_end':b/30,
            'asset':str(leg.board),'asset_md5':common.file_md5(leg.board)} for a,b,leg in items],
        'states':states,'boundaries':boundaries,'live_video_modified':False,'live_md5':live_hash}
    (AUDIT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    command = [sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(OUTPUT)]
    for f,label in sorted(boundaries.items()):
        command += ['--boundary',f'{f}:{label}']
    command += ['--outdir',str(AUDIT/'transitions')]
    checked = subprocess.run(command)
    if checked.returncode:
        report = json.loads((AUDIT/'transitions/transition-guard.json').read_text())
        failed = [row['frame'] for row in report['boundaries'] if not row['pass']]
        # A continuous 24-frame lateral pan can exceed the cut detector's MAD.
        # Preserve its raw failure report; never silently call it an auto-pass.
        if failed != [mapped(CUTS[0][0])]:
            raise SystemExit('Unexpected transition failure; inspect before handoff.')
        print('Manual strip review required: first-cut continuous pan.', flush=True)
    print(f'Review candidate: {OUTPUT} ({expected/30:.2f}s)',flush=True)


if __name__ == '__main__':
    main()

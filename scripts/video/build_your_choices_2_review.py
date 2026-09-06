#!/usr/bin/env python3
"""Approved Your Choices 2 repair. Review output only; never changes the lesson.

Source narration cuts use quiet frame boundaries, independently from visual
handoffs. After the age-restrictions shot, every frame is course-native: no
Notebook board can leak across an audio edit. Keep the requested model transition.
"""
from pathlib import Path
import json
import subprocess
import sys
import tempfile

import cv2

import build_your_choices_reroll_review as common
from build_work_changes_hybrid import BoardLeg, State, render_leg

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Prompts/your-choices-2.mp4'
OUTPUT = ROOT / 'Prompts/your-choices-2-patched.mp4'
AUDIT = ROOT / 'video-audit/your-choices-2-review/patch'
FPS = 30
at = common.at
CUTS = tuple((at(a), at(b)) for a, b in (
    (29.03, 41.60),   # Complete redundant dashboard passage; resume on visual cut.
    (61.43, 72.37),   # Mandatory-configuration detour and temperature-slider visual.
    (134.23, 151.13), # Processing power / caps / high-cost-default detour.
    (226.37, 235.93), # Only use research/reasoning after default fails.
    (270.63, 276.73), # Student manually changes temperature.
    (306.33, 314.60), # Nonsense / guaranteed vocabulary breadth.
    (330.17, 345.13), # Operator / baseline-quality claim; keep exact close.
))
END = 10666
common.CUTS = CUTS


def mapped(frame):
    return common.output_frame(frame)


def leg(name, board, points, states):
    return common.make_leg(name, board, tuple(at(s) for s in points), states)


def teaching_legs():
    # Keep both comparison cards visible; their highlights guide attention.
    tool = leg('tool', common.BOARDS['tool'],
        (72.37, 79.20, 105.10, 134.23), (
            ('full', None, common.VIDEO_PURPLE, None, 0),
            ('app', common.TOOL_LEFT, common.PURPLE, None, 0),
            ('model', common.TOOL_RIGHT, common.BLUE, None, 0),
        ))
    method = leg('method', common.BOARDS['method'],
        (151.13, 160.65, 196.40, 226.37), (
            ('full', None, common.VIDEO_PURPLE, None, 0),
            ('reasoning', common.METHOD_LEFT, common.TEAL, None, 0),
            ('research', common.METHOD_RIGHT, common.AMBER, None, 0),
        ))
    # Establish the actual lesson board during the temperature introduction.
    # This full-board view continues seamlessly into the walkthrough below.
    intro = leg('temperature-intro', common.BOARDS['temperature'], (235.93, 243.45), (
        ('full', None, common.VIDEO_PURPLE, None, 0),
    ))
    temperature = leg('temperature', common.BOARDS['temperature'],
        (243.45, 249.45, 257.80, 276.73, 295.05, 314.60, 330.17), (
            ('full', None, common.VIDEO_PURPLE, None, 0),
            ('whole-prompt', (80, 167, 1520, 278), common.VIDEO_PURPLE, (800, 240, 1650), 24),
            ('starting-odds', common.STARTING_ODDS, common.VIDEO_PURPLE, (800, 615, 1680), 24),
            ('low-temperature', common.LOW_TEMPERATURE, common.BLUE, (800, 615, 1680), 0),
            ('high-temperature', common.HIGH_TEMPERATURE, common.RED, (800, 615, 1680), 0),
            ('whole-takeaway', common.TEMPERATURE_TAKEAWAY, common.VIDEO_PURPLE, (800, 1048, 1680), 0),
        ))
    return (tool, method, intro, temperature)


def main():
    AUDIT.mkdir(parents=True, exist_ok=True)
    assert common.frame_count(SOURCE) == END
    legs = teaching_legs()
    expected = mapped(END)
    manifest = {
        'source': str(SOURCE), 'output': str(OUTPUT), 'fps': FPS,
        'expected_frames': expected,
        'cuts': [{'source_start': a/FPS, 'source_end': b/FPS,
                  'output_seam': mapped(a)/FPS} for a,b in CUTS],
        'highlights': [{'board': item.name, 'target': state.label,
                        'rect': state.ring, 'highlight_color': state.color,
                        'highlight_source': 'none' if not state.ring else
                            ('neutral_video_purple' if state.color == common.VIDEO_PURPLE else 'card_locked_accent')}
                       for item in legs for state in item.states],
        'notes': ['Keep model transition at source 105.10s.',
                  'Only approved narration cuts; optional evaluation cuts retained.',
                  'Current lesson Temperature board replaces video-only card at output 185.967s; narration and timing unchanged.',
                  'Two-card comparisons retain fixed full-board framing.',
                  'Full card, prompt, column and takeaway boundaries measured on current assets.'],
    }
    (AUDIT / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    with tempfile.TemporaryDirectory(prefix='your-choices-2-', dir='/private/tmp') as directory:
        work = Path(directory)
        paths = []
        for item in legs:
            path = work / (item.name+'.mkv')
            print('Rendering', item.name, item.frames, flush=True)
            render_leg(item, path)
            paths.append(path)
        close = work / 'close.mkv'
        close_frames = mapped(END)-mapped(CUTS[-1][1])
        common.render_close(close, close_frames)
        paths.append(close)
        graph, videos, audio = [], [], []
        common.source_video(graph, videos, 0, CUTS[0][0])
        # The new roll has a faint Gemini Notebook mark in its bottom margin.
        # A restrained aspect-preserving native-shot crop excludes that margin;
        # no inpainting touches illustration content or teaching-board text.
        graph[-1] = graph[-1].replace('setsar=1', 'crop=1220:686:30:0,scale=1280:720,setsar=1')
        common.source_video(graph, videos, CUTS[0][1], CUTS[1][0])
        graph[-1] = graph[-1].replace('setsar=1', 'crop=1220:686:30:0,scale=1280:720,setsar=1')
        for index, item in enumerate(legs, 1):
            common.rendered_video(graph, videos, index, item.frames)
        common.rendered_video(graph, videos, 5, close_frames)
        graph.append(''.join(videos)+f'concat=n={len(videos)}:v=1:a=0,format=yuv420p[outv]')
        cursor = 0
        for start, end in (*CUTS, (END, END)):
            common.source_audio(graph, audio, cursor, start)
            cursor = end
        graph.append(''.join(audio)+f'concat=n={len(audio)}:v=0:a=1[outa]')
        command = [common.FFMPEG, '-y', '-hide_banner', '-loglevel', 'error', '-i', str(SOURCE)]
        for path in paths:
            command.extend(('-i', str(path)))
        command.extend(('-filter_complex', ';'.join(graph), '-map', '[outv]', '-map', '[outa]',
                        '-r', '30', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium',
                        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                        '-movflags', '+faststart', str(OUTPUT)))
        print('Encoding final candidate', flush=True)
        subprocess.run(command, check=True)
    assert common.frame_count(OUTPUT) == expected
    boundaries = {mapped(start): f'cut-{i+1}' for i,(start,end) in enumerate(CUTS)}
    boundaries[mapped(at(243.45))] = 'temperature-intro-to-walkthrough'
    command = [sys.executable, str(ROOT/'scripts/video/transition_guard.py'), str(OUTPUT)]
    for frame, label in sorted(boundaries.items()):
        command.extend(('--boundary', f'{frame}:{label}'))
    command.extend(('--outdir', str(AUDIT/'transitions')))
    subprocess.run(command, check=True)
    print(f'Complete: {OUTPUT}, {expected} frames / {expected/FPS:.2f}s', flush=True)


if __name__ == '__main__':
    main()

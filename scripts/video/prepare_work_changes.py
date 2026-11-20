#!/usr/bin/env python3
"""Build Work Changes narration and the faceless board from current lesson sources.

Run with .video-venv/bin/python, then sync_gemini_notebook.py --lesson work-changes.
The page lesson and finished video are never modified by this preparation step.
"""
from pathlib import Path

from render_navigate_editorial_review import render_first_assignment_long

ROOT = Path(__file__).resolve().parents[2]
SPOKEN_BRIDGE = (
    "Before AI, you read and organized the reviews yourself. "
    "With AI, you get help organizing the feedback and drafting a summary. "
    "You spot-check the results, investigate the problems, and decide what to recommend. "
    "Less time on routine work can mean more time for judgment and decisions."
)
PAGE_BRIDGE = (
    "Before AI, you did all of the work yourself. With AI’s help, the grunt work gets done faster, "
    "giving you more time for higher-value work: understanding what the feedback means and deciding "
    "what to do. The more you know, the better you’ll be at that work."
)


def narration_source():
    lesson = (ROOT / 'lessons/work-changes.md').read_text()
    assert lesson.count('\n## Lab:') == 1, 'Check lesson boundary before preparing narration'
    text = lesson.split('\n## Lab:', 1)[0].rstrip() + '\n'
    assert text.count(PAGE_BRIDGE) == 1, 'Review the approved spoken bridge against revised page copy'
    text = text.replace(PAGE_BRIDGE, '## What Changes\n\n' + SPOKEN_BRIDGE.replace('. ', '.\n\n')
                        + '\n\nThe more you know, the better you’ll be at that work.')
    text = text.replace('../course-assets/work-changes/work-changes-assignment-short.jpg',
                        'work-changes-assignment-faceless.jpg')
    text = text.replace('Here’s the risk: **AI can make you productive before it makes you knowledgeable.**',
                        'Here’s the risk:\n\nAI can make you productive before it makes you knowledgeable.')
    text = text.replace('**Same assignment. Same responsibility. A different way to do the work.**',
                        'Same assignment. Same responsibility. A different way to do the work.')
    # Separate the exact manager quotation from its spoken introduction.
    text = text.replace('Your manager tells you, “', 'Your manager tells you:\n\n“')
    assert text.rstrip().endswith('Now it’s on you to LEARN.')
    assert '100 fictional' not in text and '## Lab:' not in text
    return text


def main():
    output = ROOT / 'lessons/work-changes-video.md'
    output.write_text(narration_source())
    board = render_first_assignment_long(faceless=True)
    target = ROOT / 'gemini-notebook/work-changes/assets/work-changes-assignment-faceless.jpg'
    board.save(target, quality=95, subsampling=0, optimize=True)
    print(f'{output.relative_to(ROOT)}: {len(output.read_text().split())} words')
    print(f'{target.relative_to(ROOT)}: {board.width}x{board.height}')


if __name__ == '__main__':
    main()

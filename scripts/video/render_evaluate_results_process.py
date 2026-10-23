#!/usr/bin/env python3
"""Render the evaluation overview and three simplified stage boards.

Current replacement for the four historical render_evaluate_results_* scripts.
Video camera/ring coordinates must be reviewed before using these layouts in video.
"""
from pathlib import Path
from render_evaluate_results_quick_pass import CARD_COPY as QUICK

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'course-assets/evaluation-matters'
DECIDE = (
    ('What Kind of Task Is It?', 'A factual answer needs accurate information. A draft needs clear writing. A plan needs to work. Check what matters for the task.'),
    ('How Much Is Riding on It?', 'A movie pick is low stakes. A scholarship application or advice about an injury deserves more care. What happens if the answer is wrong?'),
)
DIG = (
    ('Check the Sources', 'Ask for sources, then open them. Does each source support the claim? Is it reliable? For current information, ask AI to search the web.'),
    ('Challenge the Answer', 'Ask, “What’s the strongest argument against this?” or “What important information did you leave out?” Decide whether it changes your view of the answer.'),
    ('Check It Yourself', 'Find another way to check the answer. Recalculate the numbers, test the code, or ask someone who knows the subject.'),
)
STAGES = (
    ('quick-pass', 'Do a Quick Review', tuple(zip(('Read', 'Understand', 'Validate'), QUICK)), None),
    ('dig', 'Take a Closer Look', DIG, 'You decide whether the answer holds up.'),
    ('move', 'Make Your Move', (), 'The tool answers. You evaluate.'),
)


def stage_board(index):
    if index == 0:
        from render_evaluation_quick_review_flow import main
        return main()
    import subprocess
    subprocess.run(['node', str(ROOT / 'scripts/video/render_evaluation_cards.cjs'),
                    '--board', STAGES[index][0]], check=True)


def overview():
    from render_evaluation_flow import main
    main()


if __name__=='__main__':
    overview()
    for i in range(len(STAGES)):
        stage_board(i)

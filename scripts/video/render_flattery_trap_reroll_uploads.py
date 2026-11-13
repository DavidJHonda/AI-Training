#!/usr/bin/env python3
"""Render the Flattery Trap comparison and its text-only upload boards."""
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
from render_avoid_traps_editorial import (ROOT,CompareSide,render_comparison,render_sycophancy_example,render_three_moves,AMBER,BLUE,PURPLE,TEAL)
from render_editorial_full_bleed_batch import Board, render
from course_credit import save_course_image
OUT=ROOT/'gemini-notebook/flattery-trap/assets'

def render_feedback_comparison(art, *, reuse_board_photos=False):
    return render_comparison(
        'Flattery Trap vs. Useful Feedback',
        'You ask AI to evaluate this Great Gatsby essay introduction:\n'
        '“The American Dream is something that many people have thought about over the years. '
        'Some people achieve it and some don’t. In The Great Gatsby, Fitzgerald explores this idea.”',
        (
            CompareSide(
                '', 'Flattery Trap', '“Great start! You’ve clearly identified the central theme. This is a strong foundation.”',
                (('THE TRUTH', 'That praise could fit almost any Gatsby essay. It calls your introduction strong without pointing to a single line that earns the praise.'),), AMBER,
            ),
            CompareSide(
                '', 'Useful Feedback', '“You’ve named your topic: the American Dream. But ‘Fitzgerald explores this idea’ leaves me wondering what you think he shows about it. What does Gatsby’s experience suggest about that dream?”',
                (('THE TRUTH', 'You’ve named your topic, but your reader still needs to know what you think. Your next step is to write a thesis that says what Fitzgerald shows about the American Dream.'),), BLUE,
            ),
        ),
        str(art),
        'Good feedback improves the work. Empty praise only improves the feeling.',
        scenario_label='', reuse_board_photos=reuse_board_photos,
        source_photo_top=383,  # Photo row in the original illustrated board.
    )


def save_comparison_boards(blank_art):
    art = 'course-assets/flattery-engagement/flattery-engagement-feedback-comparison.jpg'
    filename = 'flattery-trap-feedback-comparison.jpg'
    for image, target in (
        (render_feedback_comparison(art, reuse_board_photos=True), ROOT / 'course-assets/flattery-trap' / filename),
        (render_feedback_comparison(blank_art), OUT / 'flattery-trap-feedback-comparison-faceless.jpg'),
    ):
        save_course_image(image, target, quality=95, subsampling=0, optimize=True)


def render_praise_cards(*, illustrated):
    board = Board(
        key='praise-training', title='How AI Learns to Praise',
        cards=(
            ('People Rank', 'Reviewers compare answers and choose the ones they prefer.'),
            ('Praise Can Win', 'Sometimes reviewers choose the answer that offers praise, even when the criticism would be more useful.'),
            ('Numbers Move', 'Training pushes the model toward patterns that earned approval.'),
        ),
        art_sheet='', page_output='', prep_output='', accents=(PURPLE, BLUE, TEAL),
    )
    if illustrated:
        # Recover the three illustrations from the original flow, inside its rounded frames.
        with Image.open(ROOT / 'course-assets/flattery-engagement/flattery-engagement-cycle-of-praise.jpg') as source:
            panels = [source.crop((x + 8, 180, x + 302, 345)) for x in (75, 645, 1215)]
    else:
        panels = [Image.new('RGB', (485, 273), 'white') for _ in board.cards]
    return render(board, art_panels=panels, preserve_art_colors=illustrated, numbers_above_cards=True)


def save_praise_boards():
    for illustrated, target in (
        (True, ROOT / 'course-assets/flattery-trap/flattery-trap-cycle-of-praise.jpg'),
        (False, OUT / 'flattery-trap-cycle-of-praise-faceless.jpg'),
    ):
        save_course_image(render_praise_cards(illustrated=illustrated), target,
                          quality=95, subsampling=0, optimize=True)


def save_response_board():
    image = render_sycophancy_example(title='ChatGPT’s Response', label='')
    save_course_image(image, ROOT / 'course-assets/flattery-trap/flattery-trap-sycophancy.jpg',
                      quality=95, subsampling=0, optimize=True)


def save_feedback_board():
    image = render_three_moves(board_title='How to Get Better Feedback', first_move='Share Your Opinion Last')
    save_course_image(image, ROOT / 'course-assets/flattery-trap/flattery-trap-three-moves.jpg',
                      quality=95, subsampling=0, optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix='flattery-text-boards-') as tmp:
        art = Path(tmp) / 'blank-art.png'
        Image.new('RGB', (1800, 600), 'white').save(art)
        save_comparison_boards(art)
        save_praise_boards()
        save_response_board()
        save_feedback_board()


if __name__ == '__main__':
    main()

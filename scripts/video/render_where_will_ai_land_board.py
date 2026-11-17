"""Build the four-scenario board from the lesson copy and existing course illustrations."""
from pathlib import Path
from PIL import Image
from course_credit import save_course_image
from render_navigate_editorial_batch import Card, CardBoard, PURPLE, AMBER, BLUE, TEAL, render_card_board

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'scripts/video/assets/where-will-ai-land-two-examples'
OUTPUT = ROOT / 'course-assets/where-will-ai-land/where-will-ai-land-plans.jpg'


def main():
    lesson = (ROOT / 'lessons/where-will-ai-land.md').read_text().splitlines()
    title = next(line.split(': ', 1)[1] for line in lesson if line.startswith('### Board 1:'))
    cards = []
    for name in ('Online Shopping', 'Flying Cars', 'Text Messaging', 'Cane Toads'):
        prefix = name + '. '
        body = next(line[len(prefix):] for line in lesson if line.startswith(prefix))
        cards.append(Card(name, body))
    board = CardBoard(key='where-will-ai-land-plans', title=title, cards=tuple(cards),
                      art_sheet='', page_output=str(OUTPUT.relative_to(ROOT)), prep_output='',
                      accents=(PURPLE, AMBER, BLUE, TEAL))
    with Image.open(ROOT / 'course-assets/loudest-voices/loudest-voices-missed-predictions.jpg') as original:
        panels = [original.crop((x, 128, x + 741, 467)).convert('RGB') for x in (42, 817)]
    for filename in ('text-messaging.png', 'cane-toads.png'):
        with Image.open(ASSETS / filename) as source:
            panels.append(source.convert('RGB'))
    image = render_card_board(board, preserved_panels=panels)
    save_course_image(image, OUTPUT, quality=95, subsampling=0, optimize=True)
    print(f'{OUTPUT.name}: {image.width} x {image.height}')


if __name__ == '__main__':
    main()

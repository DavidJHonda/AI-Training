"""Build the four-scenario board from the lesson copy and existing course illustrations."""
from pathlib import Path
from PIL import Image
from course_credit import save_course_image
from render_navigate_editorial_batch import Card, CardBoard, PURPLE, AMBER, BLUE, TEAL, render_card_board

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'scripts/video/assets/where-will-ai-land-two-examples'
OUTPUT = ROOT / 'course-assets/where-will-ai-land/where-will-ai-land-plans.jpg'


def main():
    lesson = (ROOT / 'lessons/where-will-ai-land.md').read_text()
    title = next(line.split(': ', 1)[1] for line in lesson.splitlines() if line.startswith('### Board 1:'))
    paragraphs = lesson.split('\n\n')
    cards = []
    for name in ('Text Messaging', 'GPS', 'Cane Toads', 'Wider Highways'):
        prefix = name + '. '
        position = next(i for i, paragraph in enumerate(paragraphs) if paragraph.startswith(prefix))
        body = paragraphs[position][len(prefix):]
        assert paragraphs[position + 1] == '**Unexpected Result**'
        cards.append(Card(name, body, result=paragraphs[position + 2]))
    board = CardBoard(key='where-will-ai-land-plans', title=title, cards=tuple(cards),
                      art_sheet='', page_output=str(OUTPUT.relative_to(ROOT)), prep_output='',
                      accents=(PURPLE, BLUE, TEAL, AMBER))
    panels = []
    for filename in ('text-messaging.png', 'gps.png', 'cane-toads.png', 'wider-highways.png'):
        with Image.open(ASSETS / filename) as source:
            panels.append(source.convert('RGB'))
    image = render_card_board(board, preserved_panels=panels)
    save_course_image(image, OUTPUT, quality=95, subsampling=0, optimize=True)
    print(f'{OUTPUT.name}: {image.width} x {image.height}')


if __name__ == '__main__':
    main()

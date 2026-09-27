"""People Skills cards using the same exact type/layout renderer as Creative Thinking.

Reuse the approved artwork from immutable source boards; rebuild all lettering
with Plus Jakarta Sans at the canonical 56/40/29 px sizes. Capstone headings may
wrap to preserve approved wording; body baselines stay aligned across cards.
"""
from pathlib import Path
from PIL import Image
from render_editorial_full_bleed_batch import Board, render, PURPLE, BLUE, TEAL, AMBER

ROOT = Path(__file__).resolve().parents[2]
SOURCES = ROOT / 'scripts/video/assets/people-skills-scene'
SPECS = {
    'four-ways': {
        'title': 'Four Ways to Practice',
        'source': 'four-ways-original.jpg',
        'size': (1351, 1164),
        'crops': [(34,108,659,394), (691,108,1317,394), (34,629,659,919), (691,629,1317,919)],
        'accents': (PURPLE, BLUE, TEAL, AMBER),
        'cards': (
            ('Listen to Understand', 'Do not plan your reply while the other person is talking. Ask one genuine follow-up question before offering your opinion.'),
            ('Notice What Isn’t Being Said', 'Pay attention to tone, hesitation, enthusiasm, and changes in behavior. If you’re unsure what a change means, ask.'),
            ('Show People They Matter', 'Remember what they tell you, give specific appreciation, and give people credit when an idea is theirs.'),
            ('Challenge Ideas, Not People', 'Address difficult things directly and calmly. Challenge the idea or behavior without attacking the person.'),
        ),
    },
    'matter-more': {
        'title': 'People Skills Matter More',
        'source': 'matter-more.png',
        'size': (1854, 848),
        'crops': [(48,148,608,464), (647,148,1208,464), (1248,148,1808,464)],
        'accents': (PURPLE, BLUE, TEAL),
        'cards': (
            ('You’ll Stand Out', 'As more people use AI, polished work becomes an expectation. How you work with people helps you stand out.'),
            ('Trust Still Matters', 'People choose teammates and leaders who listen, keep promises, and treat others well.'),
            ('Connection Matters', 'AI can help with the work. People still need to feel heard, understood, and valued.'),
        ),
    },
}


def render_cards(key):
    spec = SPECS[key]
    source = Image.open(SOURCES / spec['source']).convert('RGB')
    if source.size != spec['size']:
        raise ValueError(f'{key}: source size changed; review artwork crop coordinates')
    lesson = (ROOT / 'lessons/people-skills.md').read_text()
    for _, body in spec['cards']:
        if body not in lesson:
            raise ValueError(f'{key}: board copy differs from the lesson: {body}')
    asset = f'course-assets/people-skills/people-skills-{key}.jpg'
    board = Board(key=key, title=spec['title'], cards=spec['cards'],
                  art_sheet='', page_output=asset, prep_output=asset, accents=spec['accents'])
    return render(board, art_panels=[source.crop(box) for box in spec['crops']],
                  wrap_titles=(key == 'matter-more'), preserve_art_colors=True)

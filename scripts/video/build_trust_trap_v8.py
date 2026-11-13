"""Review revisions to the approved Trust Trap v7 assembly."""
from build_trust_trap_v7 import PICTURE, SOUND, SOURCES, PROMPTS, ROOT, build_review

OUT = PROMPTS / 'trust-trap-v8.mp4'
AUDIT = ROOT / 'video-audit/trust-trap-v8-2026-11-13'
sources = {**SOURCES, 'v5': PROMPTS / 'trust-trap-v5.mp4'}

# These source frames hold a single illustration. The older trims included
# neighboring source shots 14–24 frames long inside otherwise valid edit spans.
revised_movies = {
    ('settings', 3.45): ('1', 33.00, 36.00),
    ('generic', 2.85): ('1', 115.00, 121.30),
    ('generic', 8.9): ('1', 91.90, 95.85),
    ('definition', 0): ('2', 105.00, 110.50),
}
picture = []
for beat, offset, kind, *params in PICTURE:
    if beat in ('definition', 'why') and (kind == 'why-board' or beat == 'why'):
        continue
    if (beat, offset) in revised_movies:
        params = revised_movies[beat, offset]
    if beat == 'practical' and offset == 1.3:
        picture.extend([
            ('bridge', 0, 'why-board', 'full'),
            ('why', 0.25, 'why-board', 'language'),
            ('why', 15.39, 'why-board', 'person'),
        ])
        offset = 0
    picture.append((beat, offset, kind, *params))

sound = []
for beat, source, start, end in SOUND:
    if beat == 'why':
        sound.append(('bridge', 'v5', 116.14, 124.07))
    if beat == 'close':
        # Last spoken sound in roll 1 ends at 188.93 seconds.
        end = 189.93
    sound.append((beat, source, start, end))

if __name__ == '__main__':
    build_review(OUT, AUDIT, sound, picture, sources, fixed_boards={'why-board'})

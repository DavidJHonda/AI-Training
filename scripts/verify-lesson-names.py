#!/usr/bin/env python3
"""Check current lesson filenames against the titles in index.html.

Run after retitling a lesson, alongside verify-course-assets.py and the video
prep sync check. Internal lesson IDs remain stable across retitles.
"""
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / 'index.html').read_text()


def registry(name):
    block = re.search(r'const ' + name + r' = \{\n(.*?)\n\};', source, re.S)
    if not block:
        raise ValueError('Cannot find ' + name)
    return dict(re.findall(r'^\s*(\w+): \{(.*?)\},?$', block[1], re.M))


def field(row, name):
    match = re.search(r'\b' + name + r': ("(?:\\.|[^"\\])*")', row)
    return json.loads(match[1]) if match else None


def slug(title):
    title = title.replace('&', ' and ').replace('’', '').replace("'", '')
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')


errors = []
meta = registry('SECTION_META')
videos = registry('LESSON_VIDEOS')
for lesson_id, row in videos.items():
    path = field(row, 'src')
    if not path:
        continue
    path = path.split('?')[0]
    title = field(meta[lesson_id], 'title') or field(meta[lesson_id], 'label')
    # Section openers have a shared display label and a section-specific folder.
    name = Path(path).parent.name if title == 'Opener' else slug(title)
    expected = f'course-assets/{name}/{name}.mp4'
    if path != expected:
        errors.append(f'{title}: expected {expected}, got {path}')
    if not (ROOT / path).is_file():
        errors.append('Missing video: ' + path)
    if title != 'Opener' and not (ROOT / 'lessons' / (name + '.md')).is_file():
        errors.append(f'Missing lesson source: lessons/{name}.md')

prep = json.loads((ROOT / 'gemini-notebook/upload-sets.json').read_text())
for row in prep['lessons'] + prep.get('needs_preparation', []):
    expected = slug(row['title'])
    if row['slug'] != expected:
        errors.append(f"Prep title {row['title']!r}: expected slug {expected}, got {row['slug']}")
    markdown = row.get('markdown')
    if markdown and not Path(markdown).name.startswith('Opener-'):
        if markdown != f'lessons/{expected}.md':
            errors.append(f'Prep source for {expected}: {markdown}')

if errors:
    print('\n'.join(errors))
    sys.exit(1)
print(f'PASS: {len(videos)} lesson video paths and {len(prep["lessons"])} active prep kits use current lesson names.')

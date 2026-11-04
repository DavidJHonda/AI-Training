#!/usr/bin/env python3
"""Check current lesson filenames against the titles in index.html.

Run after retitling a lesson, alongside verify-course-assets.py and the video
prep sync check. Internal lesson IDs remain stable across retitles.
"""
import json
import os
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
    if title == 'Flattery & Engagement':
        return 'flattery-engagement'
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

# Retitles also cover disabled videos, unused rolls, and ignored build artifacts.
# The migration ledger preserves the aliases without requiring obsolete files.
ledger = json.loads((ROOT / 'scripts/video/lesson-filename-migration-2026-11-04.json').read_text())
for lesson in ledger['lessons']:
    current_title = field(meta[lesson['id']], 'title') or field(meta[lesson['id']], 'label')
    if current_title != lesson['title'] or slug(current_title) != lesson['slug']:
        errors.append(f"Retitled lesson registry is stale: {lesson['id']}")
    if not (ROOT / 'lessons' / (lesson['slug'] + '.md')).is_file():
        errors.append(f"Missing lesson source for {current_title}")
    for row in prep['lessons'] + prep.get('needs_preparation', []):
        if row['slug'] == lesson['slug'] and row['title'] != current_title:
            errors.append(f"Prep title differs from the course: {row['title']} / {current_title}")

skip = {'.git', '.video-venv', 'node_modules', '.superpowers', '.claude',
        '__pycache__', '.codex', '.agents'}
for directory, dirs, files in os.walk(ROOT):
    dirs[:] = [name for name in dirs if name not in skip]
    for name in dirs + files:
        if any(alias in name for alias in ledger['aliases']):
            errors.append('Retired asset name recreated: ' + str((Path(directory) / name).relative_to(ROOT)))

if errors:
    print('\n'.join(errors))
    sys.exit(1)
# Include ignored donors and review artifacts from the four-lesson migration.
import subprocess
subprocess.run([sys.executable, str(ROOT / 'scripts/verify-lesson-title-assets.py')], check=True)
subprocess.run([sys.executable, str(ROOT / 'scripts/video/rename_future_section.py'), '--check'], check=True)

print(f'PASS: {len(videos)} lesson video paths and {len(prep["lessons"])} active prep kits use current lesson names; no retired filenames, including unused videos.')

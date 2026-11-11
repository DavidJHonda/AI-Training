"""Read-only media audit; writes CSV/JSON reports beside this script. Never deletes."""
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime, date
from zoneinfo import ZoneInfo
import csv
import fnmatch
import hashlib
import json
import os
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
CUTOFF = date(2026, 11, 4)
ZONE = ZoneInfo('America/Chicago')
MEDIA = {'.mp4', '.mkv', '.mov', '.wav', '.mp3', '.jpg', '.jpeg', '.png', '.npy', '.f32'}
PATTERNS = ('leg-*.mkv', '*.wav', 'canvas-*.png', '*-live.mp4')
TRACKED = set(subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0'))


def write_csv(name, rows, fields):
    with (OUT / name).open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(rows)


def digest(path):
    before = path.stat()
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(4 * 1024 * 1024), b''):
            h.update(chunk)
    after = path.stat()
    return h.hexdigest() if (before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns) else None


rows = []
for area in ('video-audit', 'Prompts', 'course-assets', 'archive', 'tmp'):
    for base, dirs, files in os.walk(ROOT / area, followlinks=False):
        dirs[:] = [d for d in dirs if not (Path(base) / d).is_symlink()]
        for name in files:
            p = Path(base) / name
            if p.suffix.lower() not in MEDIA or p.is_symlink():
                continue
            try:
                s = p.stat()
            except OSError:
                continue
            rel = p.relative_to(ROOT).as_posix()
            parts = Path(rel).parts
            folder = '/'.join(parts[:2]) if len(parts) > 2 else parts[0]
            dates = re.findall(r'20\d\d-\d\d-\d\d', folder)
            folder_date = max(dates, default='')
            modified = datetime.fromtimestamp(s.st_mtime, ZONE)
            recent = bool(folder_date and folder_date >= CUTOFF.isoformat()) or modified.date() >= CUTOFF
            tracked = rel in TRACKED
            standard = area == 'video-audit' and any(fnmatch.fnmatch(name, pat) for pat in PATTERNS)
            if area == 'course-assets':
                category = 'protected_course_asset'
            elif tracked:
                category = 'protected_tracked_file'
            elif recent:
                category = 'hold_recent_work'
            elif standard:
                category = 'older_standard_scratch_review'
            elif area == 'video-audit' and p.suffix.lower() == '.mkv':
                category = 'older_other_lossless_render_review'
            elif area == 'video-audit' and p.suffix.lower() in {'.jpg', '.jpeg', '.png', '.npy', '.f32'}:
                category = 'older_review_evidence_review'
            elif area == 'Prompts':
                category = 'hold_edited_candidate' if re.search(r'-v\d+', p.stem) else 'hold_raw_or_other_source'
            else:
                category = 'hold_other_media'
            review = ROOT / folder / 'REVIEW.md'
            review_text = review.read_text(errors='replace') if review.is_file() else ''
            rows.append(dict(path=rel, bytes=s.st_size, gib=round(s.st_size / 2**30, 6),
                             allocated_bytes=s.st_blocks * 512, category=category,
                             tracked=tracked, recent=recent, folder=folder, folder_date=folder_date,
                             modified_local=modified.isoformat(), standard_cleaner_match=standard,
                             review_path=str(review.relative_to(ROOT)) if review.is_file() else '',
                             shipping_text_present=bool(re.search(r'\b(shipped|installed|committed)\b', review_text, re.I)),
                             sha256='', literal_reference_count=0, literal_reference_examples=''))

# Hash only equal-size video candidates, including canonical copies. A hash is
# evidence of equal bytes, not proof that either pathname can safely be removed.
by_size = defaultdict(list)
for row in rows:
    if Path(row['path']).suffix.lower() in {'.mp4', '.mkv', '.mov'}:
        by_size[row['bytes']].append(row)
duplicates = []
for size, candidates in by_size.items():
    if len(candidates) < 2:
        continue
    by_hash = defaultdict(list)
    for row in candidates:
        try:
            sha = digest(ROOT / row['path'])
        except OSError:
            continue
        if sha:
            row['sha256'] = sha
            by_hash[sha].append(row)
    for sha, group in by_hash.items():
        if len(group) > 1:
            preferred = min(group, key=lambda r: (not r['path'].startswith('course-assets/'), not r['tracked'], r['path']))
            for row in group:
                duplicates.append(dict(row, duplicate_group=sha, preferred_keep=preferred['path'],
                                       possible_redundant_copy=row['path'] != preferred['path']))

# Literal references in local text are clues only. Dynamic paths and external
# sessions are not covered. Both full relative path and unique basenames count.
check = [r for r in rows if r['standard_cleaner_match'] or r['category'] == 'older_other_lossless_render_review' or r['sha256']]
by_basename = defaultdict(list)
for row in check:
    by_basename[Path(row['path']).name].append(row)
tokens = re.compile(r'''(?<![^\s/\\"'`<>\[\]{}(),;:=])[^\s/\\"'`<>\[\]{}(),;:=]+\.(?:mp4|mkv|mov|wav|png)(?![\w.])''', re.I)
text_ext = {'.md', '.txt', '.json', '.py', '.js', '.cjs', '.mjs', '.html', '.sh', '.csv'}
scanned = 0
for base, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in {'.git', '.video-venv', 'node_modules', 'output', 'tmp', '.superpowers'} and not (Path(base)/d).is_symlink()]
    for name in files:
        p = Path(base) / name
        if p.suffix.lower() not in text_ext or p.is_symlink():
            continue
        try:
            if p.stat().st_size > 20 * 2**20:
                continue
            content = p.read_text(errors='replace')
        except OSError:
            continue
        scanned += 1
        rel = p.relative_to(ROOT).as_posix()
        for basename in set(tokens.findall(content)) & by_basename.keys():
            targets = by_basename[basename]
            for row in targets:
                if row['path'] in content or len(targets) == 1:
                    row['literal_reference_count'] += 1
                    examples = row['literal_reference_examples'].split(' | ') if row['literal_reference_examples'] else []
                    if len(examples) < 8:
                        examples.append(rel)
                        row['literal_reference_examples'] = ' | '.join(examples)

fields = list(rows[0])
rows.sort(key=lambda r: (-r['bytes'], r['path']))
write_csv('media-inventory.csv', rows, fields)
scratch = [r for r in rows if r['standard_cleaner_match'] and not r['tracked']]
write_csv('scratch-review.csv', scratch, fields)
first_batch = [r for r in scratch if not r['recent']]
write_csv('first-batch-review.csv', first_batch, fields)
write_csv('other-lossless-review.csv', [r for r in rows if r['category'] == 'older_other_lossless_render_review'], fields)
# Rejoin live reference counts after the scan.
lookup = {r['path']: r for r in rows}
for row in duplicates:
    row.update(lookup[row['path']])
write_csv('exact-duplicate-videos.csv', duplicates, fields + ['duplicate_group', 'preferred_keep', 'possible_redundant_copy'])
groups = defaultdict(lambda: [0, 0])
for row in rows:
    groups[row['category']][0] += 1
    groups[row['category']][1] += row['bytes']
summary = {
    'generated_local': datetime.now(ZONE).isoformat(),
    'root': str(ROOT), 'deletion_performed': False, 'recent_work_cutoff': str(CUTOFF),
    'limitations': [
        'All deletion candidates require review; this script does not delete or certify rebuildability.',
        'Recent work is inferred conservatively from file mtime and audit-folder dates; old does not imply unused.',
        'Reference matches cover literal paths and unique basenames in local text; dynamic paths and external sessions can be missed.',
        'Shipping words are context clues, not verification that a particular build was shipped.',
        'Byte totals are logical size; actual reclaimed space can differ with shared APFS blocks and hard links.',
        'Source and candidate retention decisions have not been made. Workflow tracker status was not checked.'
    ],
    'text_files_scanned': scanned,
    'categories': {k: {'files': v[0], 'logical_gib': round(v[1]/2**30, 3)} for k,v in groups.items()},
    'standard_scratch': {'files': len(scratch), 'logical_gib': round(sum(r['bytes'] for r in scratch)/2**30, 3)},
    'first_batch_review': {'files': len(first_batch), 'logical_gib': round(sum(r['bytes'] for r in first_batch)/2**30, 3)},
    'duplicate_groups': len(set(r['duplicate_group'] for r in duplicates)),
    'redundant_video_logical_gib': round(sum(r['bytes'] for r in duplicates if r['possible_redundant_copy'])/2**30, 3),
}
(OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))

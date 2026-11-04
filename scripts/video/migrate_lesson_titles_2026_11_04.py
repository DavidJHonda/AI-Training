#!/usr/bin/env python3
"""Rename the four approved lessons, including ignored donors and review media.

Default is a read-only plan. --apply records a migration ledger and verifies every
renamed binary's SHA-256. Never overwrite a destination or re-encode media.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
from collections import Counter

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / 'scripts/video/lesson-title-assets-migration-2026-11-04.json'
SKIP = {'.git', '.video-venv', 'node_modules', '.superpowers', '.claude',
        '__pycache__', '.codex', '.agents'}
ALIASES = {
    'next-level-moves': 'beyond-the-first-answer',
    'next_level_moves': 'beyond_the_first_answer',
    'the-next-token': 'why-answers-vary',
    'the_next_token': 'why_answers_vary',
    'finish-smarter-opener': 'five-big-ideas',
    'finish_smarter_opener': 'five_big_ideas',
    'Opener-Finish': 'five-big-ideas',
}
TEXT_EXT = {'.md', '.txt', '.json', '.js', '.cjs', '.mjs', '.html', '.css',
            '.py', '.sh', '.swift', '.csv', '.tsv', '.yaml', '.yml', '.gs',
            '.vtt', '.srt', '.log', '.xml', '.svg'}


def replace_aliases(value):
    for old, new in ALIASES.items():
        value = value.replace(old, new).replace(old.upper(), new.upper())
    return value.replace('five-big-ideas-five-big-ideas', 'five-big-ideas')


def current_path(value):
    """Training is also a concept in other lessons, especially What's an LLM."""
    value = replace_aliases(value)
    if value.startswith('tmp/'):
        value = value.replace('next-token', 'why-answers-vary').replace('next-level-video-review', 'beyond-the-first-answer-video-review')
    parts = value.split('/')
    if any(p.startswith('whats-an-llm') for p in parts):
        return value
    out = []
    for part in parts:
        if not part.startswith(('training-bias', 'training_bias')):
            part = re.sub(r'^training(?=$|[-_.])', 'how-ai-learns', part)
        # Python module imports must follow renamed build/QA scripts.
        part = re.sub(r'^(build|qa|render|capture|preview|test|prepare)_training(?!_bias)(?=_|\.)',
                      r'\1_how_ai_learns', part)
        if part == 'transitions-training':
            part = 'transitions-how-ai-learns'
        out.append(part)
    return '/'.join(out)


def inventory():
    files, directories, links = [], [], []
    for parent, dirs, names in os.walk(ROOT, followlinks=False):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for name in dirs + names:
            p = Path(parent) / name
            rel = p.relative_to(ROOT).as_posix()
            if p.is_symlink():
                links.append(rel)
            elif p.is_dir():
                directories.append(rel)
            else:
                files.append(rel)
    return files, directories, links


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    if LEDGER.exists() and args.apply:
        raise SystemExit('Migration ledger already exists; refusing to apply twice.')
    files, directories, links = inventory()
    mapping = {p: current_path(p) for p in files + links if current_path(p) != p}
    dir_map = {p: current_path(p) for p in directories if current_path(p) != p}
    destinations = list(mapping.values())
    assert len(destinations) == len(set(destinations)), 'Colliding destination paths'
    for old, new in mapping.items():
        assert not os.path.lexists(ROOT / new), f'Destination exists: {new}'
    binary = {p: new for p, new in mapping.items()
              if p not in links and Path(p).suffix.lower() not in TEXT_EXT}
    print(json.dumps({'files_to_move': len(mapping), 'directories_to_move': len(dir_map),
                      'binary_files': len(binary),
                      'binary_gb': round(sum((ROOT / p).stat().st_size for p in binary) / 1e9, 2),
                      'by_root': dict(Counter(p.split('/')[0] for p in mapping)),
                      'raw_videos': {p: n for p, n in mapping.items() if p.startswith('Prompts/')}}, indent=2), flush=True)
    if not args.apply:
        return

    backup = Path('/tmp/ai-training-title-assets-backup-2026-11-04')
    backup.mkdir(exist_ok=True)  # A cancelled preflight may have prepared backups.
    # Stable state is deliberately excluded from filename replacement.
    preserve = re.compile(r'(?:useLocalStorage|localStorage\.(?:getItem|setItem|removeItem))\(\s*([\"\'])(.*?)\1')
    stem_map = {Path(p).stem: Path(n).stem for p, n in mapping.items()
                if p.startswith('scripts/') and Path(p).name != Path(n).name}
    name_map = {Path(p).name: Path(n).name for p, n in mapping.items()
                if Path(p).name != Path(n).name and p.startswith(('course-assets/', 'lessons/', 'packets/'))}
    # Full paths cover basename-preserving moves. Directory paths cover dynamic
    # filenames such as f'Prompts/training-{i}.mp4'.
    substitutions = {**dir_map, **mapping}
    roots = sorted({p.split('/')[0] for p in substitutions})
    path_pattern = re.compile(r'(?<![A-Za-z0-9_-])(?:' + '|'.join(re.escape(k) for k in roots) + r')/[A-Za-z0-9_./-]+')

    def transform(text, context):
        protected = []
        def hold(m):
            protected.append(m[0]); return f'__PRESERVED_STORAGE_{len(protected)-1}__'
        text = preserve.sub(hold, text)
        text = path_pattern.sub(lambda m: substitutions.get(m[0], current_path(m[0])), text)
        text = replace_aliases(text)
        # Standalone board filenames and file stems used by script imports.
        for old, new in name_map.items():
            text = text.replace(old, new)
        for old, new in stem_map.items():
            text = re.sub(r'(?<![\w])' + re.escape(old) + r'(?![\w])', new, text)
        if 'how-ai-learns' in current_path(context) or 'how_ai_learns' in current_path(context):
            text = re.sub(r'(?<=[\"\'])training-(?!bias)', 'how-ai-learns-', text)
        text = text.replace('Prompts/training-', 'Prompts/how-ai-learns-')
        text = text.replace('Prompts/training.', 'Prompts/how-ai-learns.')
        for i, saved in enumerate(protected):
            text = text.replace(f'__PRESERVED_STORAGE_{i}__', saved)
        return text

    # Prepare edits before moving anything. Migration ledgers retain provenance;
    # Vercel sources retain old URLs; the asset manifest retains original names.
    edits = {}
    exclude = {str(Path(__file__).relative_to(ROOT)), 'vercel.json', 'course-assets/manifest.json'}
    for p in files:
        if p in exclude or ('migration' in Path(p).name and p.endswith('.json')):
            continue
        if Path(p).suffix.lower() not in TEXT_EXT:
            continue
        try:
            original = (ROOT / p).read_text()
        except UnicodeError:
            continue
        changed = transform(original, p)
        if changed != original:
            edits[p] = changed
            dest = backup / p
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(original)

    print(f'Prepared {len(edits)} text-reference updates; hashing {len(binary)} binaries.', flush=True)
    hashes = {}
    for i, (p, new) in enumerate(binary.items()):
        hashes[new] = {'sha256': sha(ROOT / p), 'bytes': (ROOT / p).stat().st_size}
        if (i + 1) % 500 == 0:
            print(f'Hashed {i+1}/{len(binary)} binaries', flush=True)
    symlinks = {}
    for p in links:
        target = os.readlink(ROOT / p)
        absolute = os.path.normpath(os.path.join(str((ROOT / p).parent), target))
        try:
            target_rel = Path(absolute).relative_to(ROOT).as_posix()
        except ValueError:
            continue
        new_rel = mapping.get(target_rel, current_path(target_rel))
        if new_rel != target_rel or p in mapping:
            new_link = mapping.get(p, p)
            new_target = str(ROOT / new_rel) if os.path.isabs(target) else os.path.relpath(ROOT / new_rel, (ROOT / new_link).parent)
            symlinks[p] = {'new': new_link, 'old_target': target, 'target': new_target,
                           'resolved_before': (ROOT / p).exists()}

    # Individual file renames allow full destination collision checking first.
    for p, new in mapping.items():
        dest = ROOT / new
        dest.parent.mkdir(parents=True, exist_ok=True)
        (ROOT / p).rename(dest)
    for p, row in symlinks.items():
        link = ROOT / row['new']
        link.unlink()
        link.symlink_to(row['target'])
    for p in sorted(dir_map, key=lambda x: len(x.split('/')), reverse=True):
        (ROOT / p).rmdir()  # Fail if an unaccounted-for file remains.
    for p, changed in edits.items():
        (ROOT / mapping.get(p, p)).write_text(changed)

    manifest_path = ROOT / 'course-assets/manifest.json'
    original = manifest_path.read_text()
    (backup / 'course-assets').mkdir(parents=True, exist_ok=True)
    (backup / 'course-assets/manifest.json').write_text(original)
    manifest = json.loads(original)
    for rows in manifest.values():
        if isinstance(rows, list):
            for row in rows:
                if isinstance(row, dict) and row.get('new') in mapping:
                    old = row['new']
                    row['new'] = mapping[old]
                    if old not in row.setdefault('previous_names', []):
                        row['previous_names'].append(old)
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')

    config = ROOT / 'vercel.json'
    (backup / 'vercel.json').write_text(config.read_text())
    data = json.loads(config.read_text())
    for row in data.get('redirects', []):
        row['destination'] = '/' + mapping.get(row['destination'].lstrip('/'), row['destination'].lstrip('/'))
    known = {r['source'] for r in data['redirects']}
    for old, new in mapping.items():
        if old.startswith(('course-assets/', 'lessons/', 'packets/')) and not Path(old).name.startswith('.') and '/' + old not in known:
            data['redirects'].append({'source': '/' + old, 'destination': '/' + new, 'permanent': True})
    config.write_text(json.dumps(data, indent=2) + '\n')

    report = {'date': '2026-11-04', 'policy': 'Rename files and references; preserve binary bytes, version numbers, stable lesson IDs and browser storage keys. Previous migration ledgers remain historical; resolve their destinations through this ledger.',
              'aliases': ALIASES, 'files': mapping, 'directories': dir_map,
              'binary_integrity': hashes, 'symlinks': symlinks,
              'text_files_updated': [mapping.get(p, p) for p in edits],
              'backup': str(backup)}
    LEDGER.write_text(json.dumps(report, indent=2) + '\n')
    print('Renames complete; checking binary hashes.', flush=True)
    for new, expected in hashes.items():
        assert sha(ROOT / new) == expected['sha256'], f'Binary changed: {new}'
    for row in symlinks.values():
        if row['resolved_before']:
            assert (ROOT / row['new']).exists(), f'Broken symlink: {row["new"]}'
    print(f'PASS: {len(mapping)} files renamed; all {len(binary)} binaries byte-identical; {len(symlinks)} symlinks maintained.', flush=True)


if __name__ == '__main__':
    main()

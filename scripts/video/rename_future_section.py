#!/usr/bin/env python3
"""Migrate the approved Navigate the Future section name and asset filenames.

Use --apply once; --check verifies destinations and detects retired filenames.
Historical transcripts and recorded media retain their original content.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / 'scripts/video/future-section-migration-2026-11-04.json'
SKIP = {'.git', '.video-venv', 'node_modules', '.superpowers', '.claude',
        '__pycache__', '.codex', '.agents'}
TEXT = {'.md', '.txt', '.json', '.js', '.cjs', '.mjs', '.html', '.css', '.py',
        '.sh', '.swift', '.csv', '.tsv', '.yaml', '.yml', '.gs', '.vtt', '.srt', '.log', '.svg'}


def rename(s):
    return s.replace('EMBRACE', 'NAVIGATE').replace('Embrace', 'Navigate').replace('embrace', 'navigate')


def inventory():
    files, dirs = [], []
    for parent, children, names in os.walk(ROOT):
        children[:] = [n for n in children if n not in SKIP]
        for n in children + names:
            p = Path(parent) / n
            rel = p.relative_to(ROOT).as_posix()
            (dirs if p.is_dir() else files).append(rel)
    return files, dirs


def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def check(hashes=False):
    data = json.loads(LEDGER.read_text())
    files, dirs = inventory()
    errors = [f'Retired filename: {p}' for p in files + dirs if rename(p) != p]
    for old, new in data['files'].items():
        if not (ROOT / new).exists():
            errors.append('Missing: ' + new)
    if hashes:
        expected_hashes = dict(data['binary_sha256'])
        expected_hashes.update({p: board['sha256'] for p, board in data.get('regenerated_boards', {}).items()})
        for p, expected in expected_hashes.items():
            if not (ROOT / p).exists() or sha(ROOT / p) != expected:
                errors.append('Unexpected binary change: ' + p)
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f"PASS: Navigate the Future migration: {len(data['files'])} files; no retired filenames."
          + (' Binary hashes verified.' if hashes else ''))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--hashes', action='store_true')
    args = ap.parse_args()
    if args.check:
        return check(args.hashes)
    files, dirs = inventory()
    mapping = {p: rename(p) for p in files if rename(p) != p}
    dm = {p: rename(p) for p in dirs if rename(p) != p}
    assert len(set(mapping.values())) == len(mapping)
    for old, new in mapping.items():
        assert not (ROOT / new).exists(), new
        assert not (ROOT / old).is_symlink(), 'Review symlink explicitly: ' + old
    binary = {p: new for p, new in mapping.items() if Path(p).suffix.lower() not in TEXT}
    print(f'Plan: {len(mapping)} files, {len(dm)} directories, {len(binary)} binaries.', flush=True)
    if not args.apply:
        return
    assert not LEDGER.exists(), 'Migration already applied'
    backup = Path('/tmp/navigate-future-migration-2026-11-04')
    backup.mkdir(exist_ok=False)
    token = re.compile(r'[A-Za-z0-9_./-]*embrace[A-Za-z0-9_./-]*', re.I)
    def paths(text):
        return token.sub(lambda m: rename(m[0]) if any(c in m[0] for c in '/-_.') else m[0], text)
    def titles(text):
        for old, new in [('Embrace the Future', 'Navigate the Future'),
                         ('Embrace the future', 'Navigate the future'),
                         ('EMBRACE THE FUTURE', 'NAVIGATE THE FUTURE')]:
            text = text.replace(old, new)
        return text
    edits = {}
    for p in files:
        if p == str(Path(__file__).relative_to(ROOT)) or p in ('vercel.json', 'course-assets/manifest.json') or 'migration' in Path(p).name:
            continue
        if Path(p).suffix.lower() not in TEXT:
            continue
        try:
            old = (ROOT / p).read_text()
        except UnicodeError:
            continue
        if 'embrace' not in old.lower():
            continue
        new = paths(old)
        if not p.startswith(('video-audit/', 'archive/', 'output/', 'tmp/', 'Prompts/')):
            new = '\n'.join(line if line.startswith('APPROVAL=') else titles(line) for line in new.split('\n'))
        if old != new:
            dest = backup / p; dest.parent.mkdir(parents=True, exist_ok=True); dest.write_text(old)
            edits[p] = new
    hashes = {new: sha(ROOT / old) for old, new in binary.items()}
    for old, new in mapping.items():
        target = ROOT / new; target.parent.mkdir(parents=True, exist_ok=True)
        (ROOT / old).rename(target)
    for old in sorted(dm, key=lambda x: x.count('/'), reverse=True):
        (ROOT / old).rmdir()
    for old, text in edits.items():
        (ROOT / mapping.get(old, old)).write_text(text)

    p = ROOT / 'course-assets/manifest.json'; manifest = json.loads(p.read_text())
    (backup / 'course-assets').mkdir(exist_ok=True); (backup / 'course-assets/manifest.json').write_text(p.read_text())
    for key in ['assets', 'generated_assets', 'video_assets']:
        for row in manifest.get(key, []):
            if row['new'] in mapping:
                old = row['new']; row['new'] = mapping[old]
                row.setdefault('previous_names', []).append(old)
    for key in ['prefixes', 'slug_aliases']:
        for old, dest in list(manifest.get(key, {}).items()):
            manifest[key][old] = rename(dest)
            if rename(old) != old:
                manifest[key][rename(old)] = rename(dest)
    manifest['slug_aliases']['embrace-the-future-opener'] = 'navigate-the-future-opener'
    manifest['slug_aliases']['opener-embrace'] = 'navigate-the-future-opener'
    manifest['filename_cleanup'].append({'date': '2026-11-04', 'reason': 'Rename the section to Navigate the Future.', 'ledger': str(LEDGER.relative_to(ROOT))})
    p.write_text(json.dumps(manifest, indent=2) + '\n')

    p = ROOT / 'vercel.json'; config = json.loads(p.read_text()); (backup / 'vercel.json').write_text(p.read_text())
    for row in config.get('redirects', []):
        row['destination'] = paths(row['destination'])
    known = {r['source'] for r in config['redirects']}
    for old, new in mapping.items():
        if old.startswith(('course-assets/', 'lessons/', 'packets/')) and not Path(old).name.startswith('.') and '/' + old not in known:
            config['redirects'].append({'source': '/' + old, 'destination': '/' + new, 'permanent': True})
    p.write_text(json.dumps(config, indent=2) + '\n')
    LEDGER.write_text(json.dumps({'date': '2026-11-04', 'section': 'Navigate the Future',
        'files': mapping, 'directories': dm, 'binary_sha256': hashes,
        'text_files_updated': [mapping.get(p, p) for p in edits], 'backup': str(backup),
        'policy': 'Current names and paths; preserve stable lesson IDs, historical transcripts, media versions, and donor bytes. Regenerated canonical board hashes are recorded separately.'}, indent=2) + '\n')
    check(True)
    print(f'Updated references in {len(edits)} text files.', flush=True)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Verify the November 4 four-lesson asset migration, including ignored donors.

Use --hashes to verify every renamed binary against its pre-migration SHA-256.
"""
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'lesson_asset_migration', ROOT / 'scripts/video/migrate_lesson_titles_2026_11_04.py')
migration = importlib.util.module_from_spec(spec)
spec.loader.exec_module(migration)
ledger = json.loads(migration.LEDGER.read_text())
errors = []
for old, new in ledger['files'].items():
    if not (ROOT / new).exists() and not (ROOT / new).is_symlink():
        errors.append('Missing renamed asset: ' + new)
    if (ROOT / old).exists() or (ROOT / old).is_symlink():
        errors.append('Retired name recreated: ' + old)
for old in ledger['directories']:
    if (ROOT / old).exists():
        errors.append('Retired directory recreated: ' + old)
files, directories, links = migration.inventory()
for name in files + directories + links:
    if migration.current_path(name) != name:
        errors.append('File or folder still uses a retired lesson name: ' + name)
for row in ledger['symlinks'].values():
    if row['resolved_before'] and not (ROOT / row['new']).exists():
        errors.append('Broken donor symlink: ' + row['new'])
if '--hashes' in sys.argv:
    for name, expected in ledger['binary_integrity'].items():
        path = ROOT / name
        if not path.is_file() or migration.sha(path) != expected['sha256']:
            errors.append('Changed binary bytes: ' + name)
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print(f"PASS: {len(ledger['files'])} renamed files, including ignored donors; no retired lesson filenames or newly broken symlinks.")
if '--hashes' in sys.argv:
    print(f"PASS: all {len(ledger['binary_integrity'])} renamed binaries retain their original SHA-256.")

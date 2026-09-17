#!/usr/bin/env python3
"""Check current canonical asset integrity and current course source references."""
from pathlib import Path
import hashlib
import json
import re
import sys

root = Path(__file__).resolve().parents[1]
m = json.loads((root / 'course-assets/manifest.json').read_text())
errors = []
for row in m['assets']:
    p = root / row['new']
    if not p.is_file():
        errors.append('Missing: ' + row['new'])
    elif '--migration-hashes' in sys.argv and hashlib.sha256(p.read_bytes()).hexdigest() != row['sha256']:
        errors.append('Changed canonical bytes: ' + row['new'])
    if row.get("renamed_from") and (root / row["renamed_from"]).exists():
        errors.append("Attributed filename was recreated: " + row["renamed_from"])
    for previous in row.get("previous_names", []):
        if (root / previous).exists():
            errors.append("Retired filename was recreated: " + previous)
    # A descriptive rename may deliberately reuse this row's old duplicate name.
    # The canonical hash check above still verifies the approved replacement bytes.
    if row.get('consolidated_from') and row['consolidated_from'] != row['new'] and (root / row['consolidated_from']).exists():
        errors.append('Consolidated duplicate was recreated: ' + row['consolidated_from'])
    # A board split from an approved board keeps its source in use.
    if row.get('variant') != 'split-from-approved-board' and (root / row['old']).exists():
        errors.append('Old asset still present: ' + row['old'])
for row in m.get('generated_assets', []):
    p = root / row['new']
    if not p.is_file():
        errors.append('Missing generated asset: ' + row['new'])
    elif '--migration-hashes' in sys.argv and hashlib.sha256(p.read_bytes()).hexdigest() != row['sha256']:
        errors.append('Changed generated asset bytes: ' + row['new'])
for row in m.get('video_assets', []):
    p = root / row['new']
    if not p.is_file():
        errors.append('Missing finished video: ' + row['new'])
    elif '--migration-hashes' in sys.argv and hashlib.sha256(p.read_bytes()).hexdigest() != row['sha256']:
        errors.append('Changed finished video bytes: ' + row['new'])
    if (root / row['old']).exists():
        errors.append('Old video path was recreated: ' + row['old'])
for row in m.get('retired_assets', []):
    if (root / row['new']).exists():
        errors.append('Retired source was recreated: ' + row['new'])
if any(p.is_dir() for p in (root / 'course-assets').rglob('source-illustrations')):
    errors.append('A source-illustrations folder was recreated')
s = (root / 'index.html').read_text()
paths = set(re.findall(r'course-assets/[A-Za-z0-9_./-]+\.(?:jpg|jpeg|png|webp|svg|pdf|mp4)', s))
paths.update('course-assets/training/' + name for name in re.findall(r'board\("([^"\n]+\.jpg)"', s))
for rel in sorted(paths):
    if not (root / rel).is_file():
        errors.append('Missing website asset: ' + rel)
if re.search(r'(?:src|href):\s*["\'](?:lessons|illustrations)/[^"\']+\.(?:jpg|png|pdf)', s):
    errors.append('Website still references an old asset folder')
if re.search(r'[\"\']videos/[^\"\']+\.mp4', s):
    errors.append('Website still references the old videos folder')
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
unique_assets = len({row["new"] for row in m["assets"]})
print(f"PASS: {unique_assets} retained assets, {len(m['assets'])} original path mappings; {len(paths)} current website image/PDF/video references; {len(m.get('video_assets', []))} finished videos.")

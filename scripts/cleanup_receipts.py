"""Recognize completed, narrowly scoped cleanup records during migration checks."""
import hashlib
import json
from pathlib import Path
import re


def verified_cleanup_paths(root, tracked):
    root = Path(root).resolve()
    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def retained(row):
        path = root / row.get('path', '')
        return path.is_file() and sha(path) == row.get('sha256')

    deleted = set()
    plans = list(root.glob('output/storage-cleanup-*/**/verified-deletions.json'))
    plans += list(root.glob('output/storage-cleanup-*/**/scope-plan.json'))
    for receipt in plans:
        cleanup = json.loads(receipt.read_text())
        if not cleanup.get('deletion_performed'):
            continue
        for row in cleanup.get('files', []):
            name = row.get('path', '')
            if name in tracked or not re.fullmatch('[0-9a-f]{64}', row.get('sha256', '')):
                continue
            path = root / name
            if path.resolve().is_relative_to(root / 'video-audit'):
                if path.suffix.lower() in {'.jpg', '.jpeg', '.png'}:
                    deleted.add(name)
                elif (path.suffix.lower() == '.mkv'
                      and row.get('reason') == 'Obsolete silent board cache; preserved image/spec passed render-preview check'
                      and row.get('dependencies') and all(retained(d) for d in row['dependencies'])):
                    deleted.add(name)
            elif (row.get('strict_edit') and re.fullmatch(r'Prompts/[^/]+-v\d+\.mp4', name)
                  and row.get('reason', '').startswith('Superseded by newer hash-verified installed release')):
                keeper = root / row.get('keeper', '')
                if (keeper.is_file() and keeper.resolve().is_relative_to(root / 'course-assets')
                        and sha(keeper) == row.get('successor_sha256')):
                    deleted.add(name)
    for receipt in root.glob('output/storage-cleanup-*/**/audio-deletion-receipt.json'):
        cleanup = json.loads(receipt.read_text())
        name = cleanup.get('path', '')
        path = root / name
        source = root / cleanup.get('retained_candidate', '')
        if (cleanup.get('deletion_performed') and cleanup.get('exact_match')
                and name not in tracked and path.resolve().is_relative_to(root / 'video-audit')
                and path.name == 'encoded.wav'
                and re.fullmatch('[0-9a-f]{64}', cleanup.get('sha256', ''))
                and cleanup['sha256'] == cleanup.get('recreated_sha256')
                and source.is_file() and source.resolve().is_relative_to(root)
                and sha(source) == cleanup.get('retained_candidate_sha256')):
            deleted.add(name)
    return deleted

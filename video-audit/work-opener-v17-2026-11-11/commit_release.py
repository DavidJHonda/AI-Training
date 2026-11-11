"""Commit only the owner-approved installed video and its release metadata."""
from pathlib import Path
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
plan = json.loads((OUT / 'release-plan.json').read_text())


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


assert git('rev-parse', 'HEAD').decode().strip() == plan['base_commit'], 'HEAD changed; reconcile before committing.'
assert not git('diff', '--cached', '--name-only').strip(), 'Preserve existing staged changes.'
video = ROOT / plan['installed_path']
assert hashlib.sha256(video.read_bytes()).hexdigest() == plan['approved_sha256']
subprocess.run(['git', '-C', str(ROOT), 'apply', '--cached', str(OUT / 'release-only.patch')], check=True)
subprocess.run(['git', '-C', str(ROOT), 'add', '--', plan['installed_path']], check=True)
staged = set(git('diff', '--cached', '--name-only').decode().splitlines())
assert staged == set(plan['release_files']), staged
assert hashlib.sha256(git('show', ':index.html')).hexdigest() == plan['expected_index_blob_sha256']
assert hashlib.sha256(git('show', ':course-assets/manifest.json')).hexdigest() == plan['expected_manifest_blob_sha256']
assert hashlib.sha256(git('show', ':' + plan['installed_path'])).hexdigest() == plan['approved_sha256']
subprocess.run(['git', '-C', str(ROOT), 'diff', '--cached', '--check'], check=True)
subprocess.run(['git', '-C', str(ROOT), 'commit', '-m', 'Ship Work With AI opener v17 locally'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
files = git('diff-tree', '--no-commit-id', '--name-only', '-r', commit).decode().splitlines()
assert set(files) == set(plan['release_files']), files
assert hashlib.sha256(git('show', 'HEAD:' + plan['installed_path'])).hexdigest() == plan['approved_sha256']
record = dict(commit=commit, files=files, installed_sha256=plan['approved_sha256'],
              runtime_seconds=plan['duration_seconds'], deployment='queued for batch deployment',
              pushed=False, installed=True, owner_acceptance=plan['user_review_acceptance'])
(OUT / 'local-release.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))

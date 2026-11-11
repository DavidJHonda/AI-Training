from pathlib import Path
import subprocess, hashlib, json
root = Path.cwd()
out = root / 'video-audit/navigate-opener-v13-2026-11-11'
video = 'course-assets/navigate-the-future-opener/navigate-the-future-opener.mp4'
expected_paths = {'index.html', 'course-assets/manifest.json', video}
def git(*args):
    return subprocess.check_output(['git', *args])
assert not git('diff', '--cached', '--name-only').strip(), 'Existing staged changes must be preserved.'
old_index = git('show', 'HEAD:index.html').decode()
old_manifest = git('show', 'HEAD:course-assets/manifest.json').decode()
expected_index = old_index.replace('navigate-the-future-opener.mp4?v=20261104ship11', 'navigate-the-future-opener.mp4?v=20261111ship13')
assert expected_index != old_index
manifest = json.loads(old_manifest)
sha = hashlib.sha256((root / video).read_bytes()).hexdigest()
assert sha == '9a98d0bcc07916ca1b9fe6987b5d49e736565c0af676f6fa29908052258754e2'
for row in manifest['video_assets']:
    if row['new'] == video:
        row.update(sha256=sha, bytes=(root / video).stat().st_size, approved_candidate_version=13)
expected_manifest = json.dumps(manifest, indent=2, ensure_ascii=False) + '\n'
subprocess.run(['git', 'apply', '--cached', '--check', str(out / 'release-only.patch')], check=True)
subprocess.run(['git', 'apply', '--cached', str(out / 'release-only.patch')], check=True)
subprocess.run(['git', 'add', '--', video], check=True)
assert set(git('diff', '--cached', '--name-only').decode().splitlines()) == expected_paths
assert git('show', ':index.html').decode() == expected_index, 'Unrelated page changes staged.'
assert git('show', ':course-assets/manifest.json').decode() == expected_manifest, 'Unrelated manifest changes staged.'
assert hashlib.sha256(git('show', ':' + video)).hexdigest() == sha
subprocess.run(['git', 'diff', '--cached', '--check'], check=True)
subprocess.run(['git', 'diff', '--cached', '--stat'], check=True)
subprocess.run(['git', 'commit', '-m', 'Ship Navigate the Future opener v13 locally'], check=True)
commit = git('rev-parse', 'HEAD').decode().strip()
assert set(git('diff-tree', '--no-commit-id', '--name-only', '-r', commit).decode().splitlines()) == expected_paths
record_path = out / 'local-release.json'
record = json.loads(record_path.read_text())
record.update(local_commit=commit, status='Shipped locally; queued for batch deployment', installed=True)
record_path.write_text(json.dumps(record, indent=2) + '\n')
print('Local release committed:', commit)

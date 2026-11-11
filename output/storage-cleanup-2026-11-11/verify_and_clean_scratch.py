"""Verify an explicit old-scratch allowlist; --delete applies only that saved list.

Donors, all MP4/MOV files, all images and build records are always retained.
No production build modules are imported or executed during dependency analysis.
"""
import argparse
import ast
import csv
import hashlib
import json
import os
import re
import subprocess
from collections import defaultdict, Counter
from datetime import datetime, date
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
ZONE = ZoneInfo('America/Chicago')
CUTOFF = date(2026, 11, 4)
HASH_CACHE = {}


def run(*args):
    return subprocess.check_output(args, cwd=ROOT)


def rel(p):
    return str(Path(p).relative_to(ROOT))


def local(p):
    p = Path(p)
    return p if p.is_absolute() else ROOT / p


def sha(p):
    p = Path(p)
    s = p.stat()
    key = (str(p), s.st_size, s.st_mtime_ns, s.st_ino)
    if key not in HASH_CACHE:
        h = hashlib.sha256()
        with p.open('rb') as f:
            for block in iter(lambda: f.read(4 * 1024 * 1024), b''):
                h.update(block)
        assert p.stat().st_mtime_ns == s.st_mtime_ns, f'File changed during hash: {p}'
        HASH_CACHE[key] = h.hexdigest()
    return HASH_CACHE[key]


def snapshot(p):
    s = p.stat()
    return dict(path=rel(p), bytes=s.st_size, mtime_ns=s.st_mtime_ns, inode=s.st_ino,
                device=s.st_dev, sha256=sha(p))


def csv_write(name, rows, fields):
    with (OUT / name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)


def evaluate(node, env):
    """Small static path evaluator, without eval(), imports, or function execution."""
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.Name):
        return env[node.id]
    if isinstance(node, (ast.List, ast.Tuple)):
        return [evaluate(n, env) for n in node.elts]
    if isinstance(node, ast.Dict):
        return {evaluate(k, env): evaluate(v, env) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.BinOp):
        a, b = evaluate(node.left, env), evaluate(node.right, env)
        if isinstance(node.op, ast.Div):
            return Path(a) / b
        if isinstance(node.op, ast.Add):
            return a + b
    if isinstance(node, ast.Attribute):
        a = evaluate(node.value, env)
        if isinstance(a, Path) and node.attr in {'parent', 'parents', 'name', 'stem', 'suffix'}:
            return getattr(a, node.attr)
    if isinstance(node, ast.Subscript):
        return evaluate(node.value, env)[evaluate(node.slice, env)]
    if isinstance(node, ast.JoinedStr):
        return ''.join(str(evaluate(n.value, env)) if isinstance(n, ast.FormattedValue) else n.value for n in node.values)
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name) and node.func.id in {'Path', 'str'}:
            a = evaluate(node.args[0], env)
            return Path(a) if node.func.id == 'Path' else str(a)
        if isinstance(node.func, ast.Attribute) and node.func.attr == 'resolve':
            return Path(evaluate(node.func.value, env)).resolve()
    raise ValueError('Unknown expression')


def scan_scripts():
    scripts = {}
    for p in (ROOT / 'scripts/video').glob('*.py'):
        text = p.read_text(errors='replace')
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        env = {'ROOT': ROOT, '__file__': str(p)}
        for n in tree.body:
            if isinstance(n, (ast.Assign, ast.AnnAssign)):
                try:
                    value = evaluate(n.value, env)
                    targets = n.targets if isinstance(n, ast.Assign) else [n.target]
                    for target in targets:
                        if isinstance(target, ast.Name):
                            env[target.id] = value
                except (ValueError, KeyError, TypeError, IndexError, AttributeError):
                    pass
        imports = set()
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                imports.update(a.name.split('.')[0] for a in n.names)
            elif isinstance(n, ast.ImportFrom) and n.module:
                imports.add(n.module.split('.')[0])
        resolved_paths = [v for v in env.values() if isinstance(v, Path)]
        for n in ast.walk(tree):
            if isinstance(n, (ast.BinOp, ast.Call, ast.Constant)):
                try:
                    value = evaluate(n, env)
                    if isinstance(value, Path):
                        resolved_paths.append(value)
                    elif isinstance(value, str) and value.startswith(('video-audit/', str(ROOT/'video-audit'))):
                        resolved_paths.append(local(value))
                except (ValueError, KeyError, TypeError, IndexError, AttributeError):
                    pass
        scripts[p] = dict(text=text, env=env, tree=tree, imports=imports, resolved_paths=resolved_paths)
    return scripts


def expected_hashes(obj):
    hashes = {}
    def walk(v):
        if isinstance(v, dict):
            for k, val in v.items():
                if isinstance(val, str) and re.fullmatch('[0-9a-f]{64}', val) and re.search(r'\.(mp4|mov|wav|mkv|jpg|png|jpeg)$', str(k), re.I):
                    hashes[str(local(k))] = val
            for key in ('path', 'source', 'asset', 'donor'):
                p = v.get(key)
                h = v.get('sha256') if key in {'path', 'asset'} else v.get(key + '_sha256')
                if isinstance(p, str) and isinstance(h, str) and re.fullmatch('[0-9a-f]{64}', h):
                    hashes[str(local(p))] = h
            for val in v.values():
                walk(val)
        elif isinstance(v, list):
            for val in v:
                walk(val)
    walk(obj)
    return hashes


def source_paths(obj):
    paths = set()
    source_keys = {'source', 'sources', 'source_files', 'source_hashes', 'donor', 'donors',
                   'donor_files', 'graft_source', 'graft_audio', 'video_src', 'visual_donor',
                   'audio_source', 'source_snapshot', 'snapshot'}
    def strings(v):
        if isinstance(v, str) and re.search(r'\.(mp4|mov|mkv|wav)$', v, re.I):
            paths.add(str(local(v)))
        elif isinstance(v, dict):
            for k, val in v.items():
                strings(k)
                strings(val)
        elif isinstance(v, list):
            for val in v:
                strings(val)
    def walk(v):
        if isinstance(v, dict):
            for k, val in v.items():
                if k in source_keys:
                    strings(val)
                else:
                    walk(val)
        elif isinstance(v, list):
            for val in v:
                walk(val)
    walk(obj)
    return paths


def verify():
    tracked = set(run('git', 'ls-files', '-z').decode().split('\0'))
    rows = []
    for name in ('first-batch-review.csv', 'other-lossless-review.csv'):
        rows.extend(csv.DictReader((OUT / name).open()))
    scripts = scan_scripts()
    # Preserve entire input audit folders used by a different build. This catches
    # dynamically named files under OLD/PREV/REVIEW as well as literal filenames.
    consumers = defaultdict(list)
    producers = defaultdict(list)
    folders = {r['folder'] for r in rows}
    for folder in folders:
        d = ROOT / folder
        for p, data in scripts.items():
            paths = data['resolved_paths']
            owns = any(isinstance(data['env'].get(k), Path) and (data['env'][k] == d or d in data['env'][k].parents) for k in ('OUT', 'AUDIT'))
            if owns:
                producers[folder].append(p)
            elif any(v == d or d in v.parents for v in paths) and any(ext in data['text'] for ext in ('.wav', '.mkv', '.png')) and p.name.startswith('build'):
                consumers[folder].append(rel(p))

    print('Hashing retained videos to resolve original and renamed sources...', flush=True)
    catalog = defaultdict(list)
    protected = []
    for area in ('Prompts', 'course-assets', 'video-audit', 'archive'):
        count = 0
        for base, dirs, files in os.walk(ROOT / area, followlinks=False):
            dirs[:] = [n for n in dirs if not (Path(base)/n).is_symlink()]
            for name in files:
                p = Path(base)/name
                if p.is_symlink() or (p.suffix.lower() not in {'.mp4', '.mov'} and not (p.suffix.lower() == '.mkv' and 'donor' in name.lower())):
                    continue
                record = snapshot(p)
                protected.append(record)
                catalog[record['sha256']].append(p)
                count += 1
        print(f'  {area}: {count} videos recorded', flush=True)
    (OUT/'protected-videos-before.json').write_text(json.dumps(protected, indent=2)+'\n')

    asset_proofs = {}
    def asset_proof(path, expected):
        key = (str(path), expected)
        if key in asset_proofs:
            return asset_proofs[key]
        p = Path(path)
        proof = None
        if p.is_file() and not p.is_symlink() and (not expected or sha(p) == expected):
            proof = dict(kind='retained_file', **snapshot(p))
        elif expected and p.is_relative_to(ROOT):
            history = run('git', 'log', '--all', '--format=%H', '--', rel(p)).decode().splitlines()
            for commit in history:
                result = subprocess.run(['git', 'show', f'{commit}:{rel(p)}'], cwd=ROOT, capture_output=True)
                if result.returncode == 0 and hashlib.sha256(result.stdout).hexdigest() == expected:
                    blob = run('git', 'rev-parse', f'{commit}:{rel(p)}').decode().strip()
                    proof = dict(kind='retained_git_blob', path=rel(p), commit=commit, blob=blob, sha256=expected)
                    break
        asset_proofs[key] = proof
        return proof

    manifest_cache = {}
    def manifest_for(folder):
        if folder not in manifest_cache:
            candidates = [ROOT/folder/'edit-manifest.json', ROOT/folder/'manifest.json']
            manifest_cache[folder] = next(((p, json.loads(p.read_text())) for p in candidates if p.is_file()), (None, {}))
        return manifest_cache[folder]

    verified, held = [], []
    for row in rows:
        p = ROOT / row['path']
        reason = ''
        deps = []
        proof = ''
        manifest_path, m = manifest_for(row['folder'])
        if not p.is_file() or p.is_symlink() or p.resolve() != p:
            reason = 'Missing, symlink, or noncanonical path'
        elif row['path'] in tracked:
            reason = 'Tracked file'
        elif datetime.fromtimestamp(p.stat().st_mtime, ZONE).date() >= CUTOFF:
            reason = 'Recent modification'
        elif 'donor' in p.name.lower():
            reason = 'Donor material retained'
        elif p.suffix.lower() not in {'.wav', '.mkv'}:
            reason = 'Retain images and other inputs/records'
        elif any(t in row['folder'] for t in ('opener', 'how-ai-answers', 'why-answers-vary')):
            reason = 'Lesson family has ongoing recent work; retained conservatively'
        elif consumers[row['folder']]:
            reason = 'Input folder used by another build: ' + ' | '.join(consumers[row['folder']])
        elif not m:
            reason = 'No sufficient build manifest'
        else:
            hashes = expected_hashes(m)
            if p.suffix.lower() == '.mkv':
                # ken_burns_path configs describe a silent render from a still.
                config = p.with_suffix('.json')
                if config.is_file():
                    cfg = json.loads(config.read_text())
                    image = cfg.get('image')
                    if image and cfg.get('beats'):
                        image = local(image)
                        if image.is_file() and not image.is_symlink():
                            deps = [dict(kind='retained_file', **snapshot(config)), dict(kind='retained_file', **snapshot(image)),
                                    dict(kind='retained_file', **snapshot(ROOT/'scripts/video/ken_burns_path.py'))]
                            proof = 'Silent still-image render; exact render config, image, and renderer retained'
                # Historical Hallucination legs contain only board animation.
                if not proof and row['folder'].startswith(('video-audit/hallucination-live-best-of-', 'video-audit/hallucination-repair-')):
                    board = next((b for b in m.get('board_spans', []) if b.get('key') == p.stem), None)
                    if board and 'asset' in board:
                        image = local(board['asset'])
                        ap = asset_proof(image, hashes.get(str(image)))
                        renderer = ROOT/'scripts/video/build_work_changes_hybrid.py'
                        recipe = ROOT/'scripts/video/build_hallucination_v5_review.py' if 'live-best-of' in row['folder'] else ROOT/'scripts/video/build_hallucination_v3_retrofit.py'
                        if ap and renderer.is_file() and recipe.is_file():
                            deps = [ap, dict(kind='retained_file', **snapshot(renderer)), dict(kind='retained_file', **snapshot(recipe))]
                            proof = 'Silent board render; exact image available locally or in Git; timing/states and renderer retained'
                if not proof:
                    reason = 'Cannot establish a complete still-render recipe; may contain unique footage'
            else:
                inputs = source_paths(m)
                # Composite files need their verified source videos, not protected
                # guards such as a live MP4 that was not read by the audio recipe.
                inputs = {v for v in inputs if Path(v).suffix.lower() in {'.mp4', '.mov', '.wav', '.mkv'}}
                unresolved = []
                for value in sorted(inputs):
                    source = Path(value)
                    expected = hashes.get(value)
                    if source.is_file() and not source.is_symlink() and (not expected or sha(source) == expected):
                        deps.append(dict(kind='retained_file', **snapshot(source)))
                    elif expected and catalog.get(expected):
                        source = catalog[expected][0]
                        deps.append(dict(kind='retained_file', original_path=value, **snapshot(source)))
                    else:
                        unresolved.append(value)
                own = producers[row['folder']]
                code = '\n'.join(scripts[s]['text'] for s in own)
                if unresolved:
                    reason = 'Unresolved original source(s): ' + ' | '.join(unresolved)
                elif not inputs:
                    reason = 'No verifiable source video/audio inputs'
                elif not own:
                    reason = 'No retained build script identified'
                elif '.wav' not in code and 'finish_audio(' not in code:
                    reason = 'Audio recipe not identified in producing build script'
                else:
                    # Scripts that reference manual precomputed WAVs without an
                    # extractor can contain unique post-production audio. Hold
                    # that input unless an explicit generator is present.
                    known_generators = ('writewav(', 'write_wav(', 'savewav(', 'wave.open(', 'finish_audio(', 'pcm_s16le', 'pcm_f32le', 'wav(OUT')
                    if not any(k in code for k in known_generators):
                        reason = 'WAV generation not established'
                    else:
                        deps += [dict(kind='retained_file', **snapshot(s)) for s in own]
                        proof = 'Derived build/review audio; original sources verified and generation recipe retained'
            if proof:
                deps.append(dict(kind='retained_file', **snapshot(manifest_path)))
        if proof and not reason:
            verified.append(dict(**snapshot(p), proof=proof, dependencies=deps))
        else:
            held.append(dict(path=row['path'], bytes=row['bytes'], reason=reason or 'Verification incomplete'))

    # Retain every dependency of every approved deletion, including dependencies
    # that the original scratch inventory also proposed removing.
    needed = {d['path'] for r in verified for d in r['dependencies'] if d['kind'] == 'retained_file'}
    final = []
    for r in verified:
        if r['path'] in needed:
            held.append(dict(path=r['path'], bytes=r['bytes'], reason='Retained reconstruction input for another approved scratch file'))
        else:
            final.append(r)
    plan = dict(created_local=datetime.now(ZONE).isoformat(), root=str(ROOT),
                cutoff=str(CUTOFF), deletion_performed=False, files=final)
    (OUT/'verified-deletions.json').write_text(json.dumps(plan, indent=2)+'\n')
    csv_write('verified-deletions.csv', final, ['path', 'bytes', 'sha256', 'proof'])
    csv_write('retained-scratch.csv', held, ['path', 'bytes', 'reason'])
    summary = dict(verified_files=len(final), verified_gib=round(sum(r['bytes'] for r in final)/2**30, 3),
                   retained_files=len(held), retained_gib=round(sum(int(r['bytes']) for r in held)/2**30, 3),
                   reasons=dict(Counter(r['reason'].split(':')[0] for r in held)))
    (OUT/'dependency-verification-summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2), flush=True)


def delete():
    plan = json.loads((OUT/'verified-deletions.json').read_text())
    assert plan['root'] == str(ROOT) and not plan['deletion_performed']
    tracked = set(run('git', 'ls-files', '-z').decode().split('\0'))
    protected = json.loads((OUT/'protected-videos-before.json').read_text())
    print('Rechecking retained videos and reconstruction dependencies before deletion...', flush=True)
    for r in protected:
        p = ROOT/r['path']
        assert p.is_file() and sha(p) == r['sha256'], f'Protected video changed before deletion: {p}'
    dependencies = {json.dumps(d, sort_keys=True): d for r in plan['files'] for d in r['dependencies']}
    for d in dependencies.values():
        if d['kind'] == 'retained_file':
            p = ROOT/d['path']
            assert p.is_file() and not p.is_symlink() and sha(p) == d['sha256'], f'Dependency changed: {p}'
        else:
            data = run('git', 'cat-file', 'blob', d['blob'])
            assert hashlib.sha256(data).hexdigest() == d['sha256']
    for r in plan['files']:
        p = ROOT/r['path']
        assert p.is_relative_to(ROOT/'video-audit') and p.resolve() == p and not p.is_symlink()
        assert r['path'] not in tracked and 'donor' not in p.name.lower() and p.suffix.lower() in {'.mkv', '.wav'}
        assert datetime.fromtimestamp(p.stat().st_mtime, ZONE).date() < CUTOFF
        assert snapshot(p) == {k:r[k] for k in ('path','bytes','mtime_ns','inode','device','sha256')}, f'Scratch changed: {p}'
    before = os.statvfs(ROOT)
    before_free = before.f_bavail * before.f_frsize
    print(f"Preflight passed; removing {len(plan['files'])} individually verified scratch files...", flush=True)
    deleted = []
    journal = OUT/'deletion-log.jsonl'
    assert not journal.exists(), 'Deletion journal already exists; do not repeat a partial deletion blindly'
    with journal.open('x') as log:
        for r in plan['files']:
            p = ROOT/r['path']
            s = p.lstat()
            assert (s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev) == (r['bytes'],r['mtime_ns'],r['inode'],r['device'])
            p.unlink()
            event = dict(path=r['path'], bytes=r['bytes'], sha256=r['sha256'], deleted_local=datetime.now(ZONE).isoformat())
            log.write(json.dumps(event)+'\n')
            log.flush()
            deleted.append(event)
    # Verify all initially recorded videos remain, byte-identical. Active editors
    # can create new videos concurrently; newly added files are outside this set.
    for r in protected:
        p = ROOT/r['path']
        assert p.is_file() and sha(p) == r['sha256'], f'Protected video changed: {p}'
    assert all(not (ROOT/r['path']).exists() for r in deleted)
    after = os.statvfs(ROOT)
    after_free = after.f_bavail * after.f_frsize
    receipt = dict(completed_local=datetime.now(ZONE).isoformat(), deleted_files=len(deleted),
                   deleted_logical_bytes=sum(r['bytes'] for r in deleted),
                   deleted_logical_gib=round(sum(r['bytes'] for r in deleted)/2**30, 3),
                   free_gib_before=round(before_free/2**30, 3), free_gib_after=round(after_free/2**30, 3),
                   measured_free_space_change_gib=round((after_free-before_free)/2**30, 3),
                   protected_videos_verified=len(protected), all_recorded_videos_unchanged=True)
    (OUT/'deletion-receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    plan['deletion_performed'] = True
    (OUT/'verified-deletions.json').write_text(json.dumps(plan, indent=2)+'\n')
    print(json.dumps(receipt, indent=2), flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--delete', action='store_true')
    args = ap.parse_args()
    delete() if args.delete else verify()

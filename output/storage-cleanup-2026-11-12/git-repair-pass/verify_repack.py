"""Verify retained Git objects, refs, reflogs and worktree before releasing backup."""
from pathlib import Path
import hashlib,json,os,subprocess

ROOT=Path('/Users/davidobrien/Developer/AI-Training')
OUT=Path(__file__).resolve().parent
TEMP=Path(json.loads((OUT/'verification-location.json').read_text())['temp_dir'])
before=json.loads((OUT/'before-repack.json').read_text())
def git(*args,**kw):
    return subprocess.check_output(['git',*args],cwd=ROOT,**kw)
objects=set()
indexes=list((ROOT/'.git/objects/pack').glob('*.idx'))
for index in indexes:
    with index.open('rb') as f:
        objects.update(line.split()[1] for line in git('show-index',stdin=f,text=True).splitlines())
for directory in (ROOT/'.git/objects').iterdir():
    if directory.is_dir() and len(directory.name)==2:
        for path in directory.iterdir():
            name=directory.name+path.name
            if path.is_file() and len(name)==40 and all(c in '0123456789abcdef' for c in name):objects.add(name)
missing=sorted(set(before['object_ids'])-objects)
assert not missing,('Missing original objects',missing)
refs=git('for-each-ref','--format=%(refname) %(objectname)',text=True)
def permanent(value):
    return dict(line.split() for line in value.splitlines() if not line.startswith('refs/codex/turn-diffs/'))
assert permanent(refs)==permanent(before['refs']),'Permanent refs changed'
for name,digest in before['controls'].items():
    assert hashlib.sha256((ROOT/'.git'/name).read_bytes()).hexdigest()==digest,('Control file changed',name)
for name,old in before['reflogs'].items():
    data=(ROOT/name).read_bytes()
    assert len(data)>=old['bytes'] and hashlib.sha256(data[:old['bytes']]).hexdigest()==old['sha256'],('Reflog history changed',name)
worktree={}
for base,dirs,names in os.walk(ROOT,followlinks=False):
    dirs[:]=[d for d in dirs if d!='.git' and not (Path(base)/d).is_relative_to(OUT)]
    for name in names:
        path=Path(base)/name
        if path.is_relative_to(OUT):continue
        s=path.lstat();record=[s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev]
        if path.is_symlink():record.append(os.readlink(path))
        worktree[str(path.relative_to(ROOT))]=record
changed=sorted(p for p,v in before['worktree'].items() if worktree.get(p)!=v)
added=sorted(set(worktree)-set(before['worktree']))
removed=sorted(set(before['worktree'])-set(worktree))
assert not removed,('Working files removed',removed)
# Source edits observed during repack are unrelated active work. Never overwrite them.
allowed_concurrent={'index.html','lessons/hallucination.md','scripts/test_phone_reading_wave_six.cjs'}
assert set(changed)<=allowed_concurrent,('Unexpected working file changes',changed)
concurrent={p:dict(before=before['worktree'].get(p),after=worktree[p],sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()) for p in changed+added}
(TEMP/'concurrent-worktree-edits.json').write_text(json.dumps(concurrent,indent=2)+'\n')
roots=set(json.loads((TEMP/'snapshot.json').read_text())['roots'])
roots.update(line.split()[1] for line in refs.splitlines())
roots.add(git('rev-parse','HEAD',text=True).strip())
for path in (ROOT/'.git/logs').rglob('*'):
    if path.is_file():
        for line in path.read_text().splitlines():
            for oid in line.split()[:2]:
                if len(oid)==40 and oid!='0'*40:roots.add(oid)
presence=git('cat-file','--batch-check=%(objectname) %(objecttype)',input=''.join(x+'\n' for x in sorted(roots)),text=True)
assert not any(line.endswith(' missing') for line in presence.splitlines()),'Integrity root missing'
allocated=sum(p.stat().st_blocks*512 for p in (ROOT/'.git').rglob('*') if p.is_file() and not p.is_symlink())
result=dict(original_objects_preserved=len(before['object_ids']),current_objects=len(objects),missing_original_objects=missing,
            permanent_refs_unchanged=True,controls_unchanged=True,reflog_history_preserved=True,
            working_files_unchanged=len(before['worktree'])-len(changed),working_files_removed=removed,
            concurrent_worktree_edits=changed,concurrent_worktree_additions=added,
            git_allocated_bytes=allocated,pack_count=len(indexes),integrity_roots=len(roots))
(TEMP/'after-repack-precheck.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2),flush=True)
with (TEMP/'fsck-after-repack.log').open('w') as log:
    check=subprocess.run(['git','fsck','--full','--no-dangling','--no-reflogs','--no-cache',*sorted(roots)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
result['full_fsck_exit_code']=check.returncode
(TEMP/'after-repack-result.json').write_text(json.dumps(result,indent=2)+'\n')
assert check.returncode==0,'Full integrity check failed; preserve rollback backup'
print('Full post-repack integrity check passed.',flush=True)

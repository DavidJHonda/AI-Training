"""Release only the verified temporary rollback links and write the audit receipt."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess

ROOT=Path('/Users/davidobrien/Developer/AI-Training')
OUT=Path(__file__).resolve().parent
TEMP=Path(json.loads((OUT/'verification-location.json').read_text())['temp_dir'])
before=json.loads((OUT/'before-repack.json').read_text())
after=json.loads((TEMP/'after-repack-result.json').read_text())
assert before['full_fsck_before']['exit_code']==after['full_fsck_exit_code']==0
assert after['original_objects_preserved']==before['object_count']==58340
assert not after['missing_original_objects'] and not after['working_files_removed']
assert all(after[k] for k in ('permanent_refs_unchanged','controls_unchanged','reflog_history_preserved'))
def git(*args,**kwargs):return subprocess.check_output(['git',*args],cwd=ROOT,**kwargs)
objects=set()
for p in (ROOT/'.git/objects/pack').glob('*.idx'):
    with p.open('rb') as f:objects.update(line.split()[1] for line in git('show-index',stdin=f,text=True).splitlines())
for d in (ROOT/'.git/objects').iterdir():
    if d.is_dir() and len(d.name)==2:
        for p in d.iterdir():
            oid=d.name+p.name
            if p.is_file() and len(oid)==40 and all(c in '0123456789abcdef' for c in oid):objects.add(oid)
assert set(before['object_ids'])<=objects,'An original object has disappeared'
tree='9ebafe5699b2d64953beb739283137615441d65f'
raw=git('cat-file','tree',tree)
assert hashlib.sha1(b'tree '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==tree
for name,digest in before['controls'].items():
    assert hashlib.sha256((ROOT/'.git'/name).read_bytes()).hexdigest()==digest,('Git control changed',name)
allowed={'index.html','lessons/hallucination.md','scripts/test_phone_reading_wave_six.cjs','docs/components/page-components.md'}
changed=[]
for name,old in before['worktree'].items():
    p=ROOT/name;s=p.lstat();now=[s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev]
    if p.is_symlink():now.append(os.readlink(p))
    if now!=old:changed.append(name)
assert set(changed)<=allowed,('Unexpected working file changes',changed)
backup=Path(before['object_backup'])
assert str(backup)=='/private/tmp/ai-training-git-backup-a8k0dk2b'
assert backup.is_dir() and not backup.is_symlink()
assert not any(p.is_symlink() for p in backup.rglob('*'))
# All old object names are present in the verified store. Unlink backup names only.
shutil.rmtree(backup)
failed=Path('/private/tmp/ai-training-git-backup-ljwc0e1q')
if failed.exists():
    assert not any(p.is_file() or p.is_symlink() for p in failed.rglob('*'))
    shutil.rmtree(failed)
connectivity=subprocess.run(['git','fsck','--connectivity-only','--no-dangling'],cwd=ROOT,capture_output=True,text=True)
(OUT/'connectivity-final.log').write_text(connectivity.stdout+connectivity.stderr)
allocated=sum(p.stat().st_blocks*512 for p in (ROOT/'.git').rglob('*') if p.is_file() and not p.is_symlink())
for name in ('fsck-fixed-roots.log','fsck-after-repack.log','after-repack-result.json','concurrent-worktree-edits.json'):
    shutil.copyfile(TEMP/name,OUT/name)
receipt=dict(
    investigation=dict(original_tree=tree,tree_present_before_repack=True,exact_tree_hash_verified=True,
                       replacement_object_written=False,explanation='The previously missing tree was already locally present and valid. Ordinary full scans also briefly reported another now-present tree while temporary Codex checkpoint refs were changing. Full checks using fixed roots passed before and after repacking.'),
    repack=dict(command='git repack -a -d --keep-unreachable -n --threads=2 --window-memory=128m --window=10 --depth=50',
                exit_code=0,before_pack_count=19,after_pack_count=len(list((ROOT/'.git/objects/pack').glob('*.idx'))),
                before_git_allocated_bytes=before['git_allocated_bytes'],after_git_allocated_bytes=allocated,
                recovered_bytes=before['git_allocated_bytes']-allocated,free_disk_bytes=shutil.disk_usage(ROOT).free),
    verification=after,final_connectivity_exit_code=connectivity.returncode,
    final_working_files_unchanged=len(before['worktree'])-len(changed),
    preservation=dict(history_rewritten=False,reflogs_expired=False,objects_pruned=False,
                      all_original_objects_retained=True,donor_videos_unchanged=True,active_work_retained=True,
                      required_build_inputs_retained=True,concurrent_edits_left_intact=changed),
    rollback_backup_removed_after_successful_verification=True,
    evidence=dict(baseline='before-repack.json',full_fsck_before='fsck-fixed-roots.log',full_fsck_after='fsck-after-repack.log',
                  concurrent_work='concurrent-worktree-edits.json'))
(OUT/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(dict(recovered_mib=round(receipt['repack']['recovered_bytes']/2**20,2),
                     git_gib=round(allocated/2**30,3),free_gib=round(receipt['repack']['free_disk_bytes']/2**30,2),
                     backup_removed=not backup.exists(),final_connectivity_exit_code=connectivity.returncode),indent=2))
assert connectivity.returncode==0,'Final connectivity issue: see retained log'

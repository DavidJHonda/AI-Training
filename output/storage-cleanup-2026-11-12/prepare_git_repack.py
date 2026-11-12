"""Make a no-data-copy rollback backup and verification baseline for Git repack."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,tempfile

ROOT=Path('/Users/davidobrien/Developer/AI-Training')
OUT=ROOT/'output/storage-cleanup-2026-11-12/git-repair-pass'
location=json.loads((OUT/'verification-location.json').read_text())
TEMP=Path(location['temp_dir'])
checked=json.loads((TEMP/'result.json').read_text())
assert checked['exit_code']==0,'A clean full integrity check is required'
assert subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip()==str(ROOT)
assert not (OUT/'before-repack.json').exists(),'Preserve the existing baseline'

objects=set();files=[]
for index in (ROOT/'.git/objects/pack').glob('*.idx'):
    with index.open('rb') as f:
        result=subprocess.run(['git','show-index'],stdin=f,cwd=ROOT,capture_output=True,text=True,check=True)
    objects.update(line.split()[1] for line in result.stdout.splitlines())
for directory in (ROOT/'.git/objects').iterdir():
    if directory.is_dir() and len(directory.name)==2:
        for path in directory.iterdir():
            name=directory.name+path.name
            if path.is_file() and len(name)==40 and all(c in '0123456789abcdef' for c in name):
                objects.add(name);files.append(path)
files.extend(p for p in (ROOT/'.git/objects/pack').iterdir() if p.is_file())
backup=Path(tempfile.mkdtemp(prefix='ai-training-git-backup-',dir='/private/tmp'))
try:
    for path in files:
        dest=backup/path.relative_to(ROOT/'.git');dest.parent.mkdir(parents=True,exist_ok=True)
        os.link(path,dest)
        assert path.stat().st_ino==dest.stat().st_ino and path.stat().st_dev==dest.stat().st_dev
    for name in ('HEAD','index','shallow','config','packed-refs'):
        path=ROOT/'.git'/name
        if path.is_file():
            dest=backup/'controls'/name;dest.parent.mkdir(exist_ok=True);shutil.copy2(path,dest)
except BaseException:
    shutil.rmtree(backup)
    raise
refs=subprocess.check_output(['git','for-each-ref','--format=%(refname) %(objectname)'],cwd=ROOT,text=True)
logs={str(p.relative_to(ROOT)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in (ROOT/'.git/logs').rglob('*') if p.is_file()}
controls={name:hashlib.sha256((ROOT/'.git'/name).read_bytes()).hexdigest() for name in ('HEAD','index','shallow','config','packed-refs') if (ROOT/'.git'/name).is_file()}
worktree={}
for base,dirs,names in os.walk(ROOT,followlinks=False):
    dirs[:]=[d for d in dirs if d!='.git' and not (Path(base)/d).is_relative_to(OUT)]
    for name in names:
        path=Path(base)/name
        if path.is_relative_to(OUT):continue
        s=path.lstat();record=[s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev]
        if path.is_symlink():record.append(os.readlink(path))
        worktree[str(path.relative_to(ROOT))]=record
allocated=sum(p.stat().st_blocks*512 for p in (ROOT/'.git').rglob('*') if p.is_file() and not p.is_symlink())
fs=os.statvfs(ROOT);free=fs.f_bavail*fs.f_frsize
assert free>allocated+5*2**30,'Insufficient headroom for a verified repack'
state=dict(object_ids=sorted(objects),object_count=len(objects),object_backup=str(backup),backup_files=len(files),refs=refs,reflogs=logs,controls=controls,
           worktree=worktree,git_allocated_bytes=allocated,free_bytes=free,full_fsck_before=checked)
(OUT/'before-repack.json').write_text(json.dumps(state,indent=2)+'\n')
(TEMP/'before-repack.json').write_text(json.dumps(state,indent=2)+'\n')
print(json.dumps(dict(object_count=len(objects),hardlinked_backup_files=len(files),backup=str(backup),working_files=len(worktree),git_gib=round(allocated/2**30,3),free_gib=round(free/2**30,3)),indent=2))

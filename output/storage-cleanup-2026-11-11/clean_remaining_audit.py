"""Inventory audit storage, verify obsolete still renders, deduplicate unused images.

All motion/source/donor clips, active work, source images, and reconstruction
dependencies remain. Default verifies; --delete applies only its saved allowlist.
"""
import argparse,ast,csv,hashlib,importlib.util,json,os,re,subprocess,tempfile
from collections import defaultdict,Counter
from datetime import date,datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE=Path(__file__).resolve().parent
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj);return obj
v=module('scratch_helpers',BASE/'verify_and_clean_scratch.py')
edits=module('edit_helpers',BASE/'clean_edited_videos.py')
ROOT=v.ROOT;OUT=BASE/'audit-cache-pass';OUT.mkdir(exist_ok=True)
ZONE=ZoneInfo('America/Chicago');CUTOFF=date(2026,11,4)
IMAGES={'.jpg','.jpeg','.png'}
KEEP_NAMES=re.compile(r'donor|source|canvas|mask|patch|snapshot|prepared|reference|original|close',re.I)


def storage():
    exts=defaultdict(lambda:[0,0,0]);folders=defaultdict(lambda:[0,0]);seen=set();files=[]
    for base,dirs,names in os.walk(ROOT/'video-audit',followlinks=False):
        dirs[:]=[d for d in dirs if not (Path(base)/d).is_symlink()]
        for name in names:
            p=Path(base)/name
            if p.is_symlink():continue
            s=p.stat();ext=p.suffix.lower() or '<none>';folder=p.relative_to(ROOT).parts[1]
            exts[ext][0]+=1;exts[ext][1]+=s.st_size
            folders[folder][0]+=1;folders[folder][1]+=s.st_blocks*512
            inode=(s.st_dev,s.st_ino)
            if inode not in seen:exts[ext][2]+=s.st_blocks*512;seen.add(inode)
            files.append(dict(path=v.rel(p),bytes=s.st_size))
    return dict(time_local=datetime.now(ZONE).isoformat(),allocated_unique_gib=round(sum(a[2] for a in exts.values())/2**30,3),
                extensions={k:dict(files=a[0],logical_gib=round(a[1]/2**30,3),allocated_unique_gib=round(a[2]/2**30,3)) for k,a in sorted(exts.items(),key=lambda x:-x[1][2])},
                largest_folders=[dict(folder=k,files=a[0],allocated_gib=round(a[1]/2**30,3)) for k,a in sorted(folders.items(),key=lambda x:-x[1][1])[:20]],
                largest_files=sorted(files,key=lambda r:-r['bytes'])[:30])


def save_csv(name,rows,fields):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)


def recent(p):
    dates=re.findall(r'20\d\d-\d\d-\d\d',v.rel(p))
    return bool(dates and max(dates)>=str(CUTOFF)) or datetime.fromtimestamp(p.stat().st_mtime,ZONE).date()>=CUTOFF


def plan():
    assert not (OUT/'deletion-log.jsonl').exists()
    checkpoint=edits.reference_state();tracked=set(v.run('git','ls-files','-z').decode().split('\0'))
    before=storage();(OUT/'remaining-before.json').write_text(json.dumps(before,indent=2)+'\n')
    scripts=v.scan_scripts();active=set()
    for path,data in scripts.items():
        for var in ('OUT','AUDIT'):
            value=data['env'].get(var)
            if isinstance(value,Path) and value.is_relative_to(ROOT/'video-audit'):
                dates=re.findall(r'20\d\d-\d\d-\d\d',str(value))
                if dates and max(dates)>=str(CUTOFF):active.add(path)
        if re.search(r'(?:\.OUT|\bOUT|\bAUDIT)\s*=.*video-audit/[^\n]*2026-11-(?:0[4-9]|[12]\d|30)',data['text']):active.add(path)
    by_module={p.stem:p for p in scripts}
    while True:
        expanded=active|{by_module[name] for p in active for name in scripts[p]['imports'] if name in by_module}
        if expanded==active:break
        active=expanded
    active_prefixes={p for script in active for p in scripts[script]['resolved_paths'] if p!=ROOT/'video-audit' and p.is_relative_to(ROOT/'video-audit')}
    protected=set();read_prefixes=set();protected_video=set()
    for file in (BASE/'verified-deletions.json',BASE/'review-evidence-pass/verified-deletions.json'):
        for r in json.loads(file.read_text())['files']:
            for d in r['dependencies']:
                if d.get('kind')=='retained_file':protected.add(ROOT/d['path'])
    refs=json.loads((BASE/'edited-video-pass/protected-source-references.json').read_text())
    for path,reasons in refs.items():
        if any(reason.startswith(('Source/parent metadata:','Source reservation','Explicit donor','Raw donor','Retained reconstruction')) for reason in reasons):protected_video.add(ROOT/path)
    for script,data in scripts.items():
        for node in ast.walk(data['tree']):
            if not isinstance(node,ast.Call):continue
            name=getattr(node.func,'attr',getattr(node.func,'id',''))
            if name not in {'imread','open','glob','rglob','load','fromfile','read_bytes'}:continue
            if name in {'glob','rglob'} and node.args and isinstance(node.args[0],ast.Constant):
                pattern=node.args[0].value
                if isinstance(pattern,str) and any(ext in pattern for ext in ('.json','.py','.md','.mp4','.mkv','.wav','.npy','.f32')) and not any(ext in pattern for ext in ('.jpg','.jpeg','.png')):continue
            args=node.args if name not in {'glob','rglob','read_bytes'} else [node.func.value]
            for arg in args:
                paths=[]
                for expr in ast.walk(arg):
                    try:
                        value=v.evaluate(expr,data['env'])
                        if isinstance(value,Path) and value.is_relative_to(ROOT/'video-audit'):paths.append(value)
                    except (ValueError,KeyError,TypeError,IndexError,AttributeError):pass
                if paths:
                    prefix=max(paths,key=lambda p:len(p.parts))
                    if prefix!=ROOT/'video-audit':read_prefixes.add(prefix)

    # Keep images referenced as source material by specs and relative links in
    # notes/reports, not just absolute paths in production scripts.
    image_ref=re.compile(r'''video-audit/[^\s"'`<>)(\]}]{1,360}\.(?:jpg|jpeg|png)(?![\w.])''',re.I)
    links=re.compile(r'''(?:!?\[[^\]]*\]\(|(?:src|href)=["'])([^\s)"']+\.(?:jpg|jpeg|png))(?:[?][^\s)"']*)?''',re.I)
    input_keys={'image','asset','path','snapshot','donor','canvas','still','mask','source','source_snapshot'}
    for base,dirs,files in os.walk(ROOT,followlinks=False):
        dirs[:]=[d for d in dirs if d not in {'.git','.video-venv','node_modules','output','tmp','.superpowers'} and not (Path(base)/d).is_symlink()]
        for name in files:
            p=Path(base)/name
            if p.suffix.lower() not in {'.json','.md','.html','.txt','.py','.js','.cjs','.csv'} or p.is_symlink():continue
            try:
                if p.stat().st_size>20*2**20:continue
                text=p.read_text(errors='replace')
            except OSError:continue
            if p.suffix=='.json':
                try:obj=json.loads(text)
                except ValueError:continue
                def walk(value):
                    if isinstance(value,dict):
                        for key,val in value.items():
                            if key in input_keys and isinstance(val,str) and Path(val).suffix.lower() in IMAGES:
                                q=Path(val);q=q if q.is_absolute() else (ROOT/q if '/' in val else p.parent/q)
                                protected.add(Path(os.path.normpath(q)))
                            walk(val)
                    elif isinstance(value,list):
                        for val in value:walk(val)
                walk(obj)
            else:
                protected.update(ROOT/q for q in image_ref.findall(text))
                if p.suffix in {'.md','.html','.txt'}:
                    for target in links.findall(text):
                        if '://' not in target:protected.add(Path(os.path.normpath(p.parent/target)))
                    for target in set(re.findall(r'[\w.-]+\.(?:jpg|jpeg|png)(?![\w.])',text)):
                        q=p.parent/target
                        if q.is_file():protected.add(q)

    ff=subprocess.check_output([str(ROOT/'.video-venv/bin/python'),'-c','import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())'],text=True).strip()
    renderer=ROOT/'scripts/video/ken_burns_path.py';verified=[];held=[];preview_checked=set()
    print('Verifying older still-image render recipes and current-work exclusions...',flush=True)
    def blocked(p):return p in protected or any(q in active_prefixes for q in (p,*p.parents))
    def cfg_inputs(cfg_path,cache_path):
        cfg=json.loads(cfg_path.read_text());image=v.local(cfg.get('image',''))
        if not cfg.get('beats') or not image.is_relative_to(ROOT/'video-audit') or not image.is_file() or image.is_symlink():return None
        if recent(image) or image.stat().st_mtime_ns>cache_path.stat().st_mtime_ns:return None
        if cfg_path not in preview_checked:
            with tempfile.TemporaryDirectory(prefix='audit-render-check-') as tmp:
                result=subprocess.run([str(ROOT/'.video-venv/bin/python'),str(renderer),str(cfg_path),'--preview',tmp],cwd=ROOT,capture_output=True,text=True)
                if result.returncode!=0:return None
            preview_checked.add(cfg_path)
        return [dict(**v.snapshot(q)) for q in (cfg_path,image,renderer)]
    for p in (ROOT/'video-audit').rglob('*.mkv'):
        if p.is_symlink() or not p.is_file() or v.rel(p) in tracked or recent(p) or p in protected_video or blocked(p):continue
        # Only canonical-board/closing caches; keep Notebook scenes and all
        # patched/extracted/donor footage, even if it has no audio track.
        if not re.fullmatch(r'(?:\d+-(?:.*board.*|section-map|close)|state-\d+|board-leg)\.mkv',p.name):continue
        dependencies=[];recipe=[]
        if p.with_suffix('.json').is_file():recipe=[p.with_suffix('.json')]
        elif re.fullmatch(r'state-\d+\.mkv',p.name):
            number=int(re.search(r'\d+',p.stem)[0]);recipe=list(p.parent.glob(f'state-{number}-*.json'))
        elif p.name=='board-leg.mkv' and (p.parent/'concat.txt').is_file():
            recipe=sorted(q for q in p.parent.glob('state-*.json') if re.fullmatch(r'state-\d+-.+\.json',q.name))
            dependencies.append(v.snapshot(p.parent/'concat.txt'))
        if not recipe:continue
        for cfg in recipe:
            deps=cfg_inputs(cfg,p)
            if not deps:break
            dependencies.extend(deps)
        else:
            probe=subprocess.run([ff,'-hide_banner','-i',str(p)],capture_output=True,text=True).stderr
            if 'Video: ffv1' in probe and 'Audio:' not in probe:
                verified.append(dict(**v.snapshot(p),reason='Obsolete silent board cache; preserved image/spec passed render-preview check',dependencies=dependencies))
                protected.update(ROOT/d['path'] for d in dependencies)

    print(f'Verified {len(verified)} still-render caches; finding identical unused image copies...',flush=True)
    by_size=defaultdict(list)
    for base,dirs,files in os.walk(ROOT/'video-audit',followlinks=False):
        dirs[:]=[d for d in dirs if not (Path(base)/d).is_symlink()]
        for name in files:
            p=Path(base)/name
            if p.is_symlink() or p.suffix.lower() not in IMAGES:continue
            by_size[p.stat().st_size].append(p)
    def image_blocked(p):
        return recent(p) or v.rel(p) in tracked or p.stat().st_nlink>1 or blocked(p) or KEEP_NAMES.search(p.name) or any(q in read_prefixes for q in (p,*p.parents))
    duplicate_groups=0
    for size,paths in by_size.items():
        if len(paths)<2 or all(image_blocked(p) for p in paths):continue
        by_hash=defaultdict(list)
        for p in paths:by_hash[v.sha(p)].append(p)
        for sha,peers in by_hash.items():
            if len(peers)<2:continue
            duplicate_groups+=1
            keeper=min(peers,key=lambda p:(not bool(image_blocked(p)),-p.stat().st_mtime_ns,v.rel(p)))
            for p in peers:
                if p==keeper or image_blocked(p):continue
                deps=[v.snapshot(keeper)]
                verified.append(dict(**v.snapshot(p),reason='Exact unused review-image duplicate; identical copy retained',keeper=v.rel(keeper),dependencies=deps))
    needed={d['path'] for r in verified for d in r['dependencies']}
    final=[r for r in verified if r['path'] not in needed]
    assert checkpoint==edits.reference_state(),'Build/reference records changed; reverify before deletion'
    (OUT/'reference-state.json').write_text(json.dumps(checkpoint)+'\n')
    result=dict(created_local=datetime.now(ZONE).isoformat(),deletion_performed=False,files=final)
    (OUT/'verified-deletions.json').write_text(json.dumps(result,indent=2)+'\n')
    save_csv('verified-deletions.csv',final,['path','bytes','sha256','reason','keeper'])
    summary=dict(verified_files=len(final),verified_logical_gib=round(sum(r['bytes'] for r in final)/2**30,3),
                 by_reason={reason:dict(files=sum(r['reason']==reason for r in final),gib=round(sum(r['bytes'] for r in final if r['reason']==reason)/2**30,3)) for reason in set(r['reason'] for r in final)},
                 still_specs_preview_tested=len(preview_checked),duplicate_image_groups=duplicate_groups,active_build_modules_protected=len(active))
    (OUT/'verification-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)


def delete():
    plan=json.loads((OUT/'verified-deletions.json').read_text());assert not plan['deletion_performed'] and not (OUT/'deletion-log.jsonl').exists()
    assert edits.reference_state()==json.loads((OUT/'reference-state.json').read_text()),'References changed; reverify first'
    tracked=set(v.run('git','ls-files','-z').decode().split('\0'));deleted={r['path'] for r in plan['files']}
    dependencies={d['path']:d for r in plan['files'] for d in r['dependencies']}
    print('Rechecking exact deletion identities, images, recipes, and duplicate keepers...',flush=True)
    for name,d in dependencies.items():assert name not in deleted and v.sha(ROOT/name)==d['sha256'],name
    for r in plan['files']:
        p=ROOT/r['path'];assert p.resolve()==p and not p.is_symlink() and p.is_relative_to(ROOT/'video-audit')
        assert p.suffix.lower() in IMAGES|{'.mkv'} and r['path'] not in tracked and not recent(p)
        assert v.snapshot(p)=={k:r[k] for k in ('path','bytes','mtime_ns','inode','device','sha256')}
        if 'keeper' in r:assert v.sha(ROOT/r['keeper'])==r['sha256']
    videos={}
    for area in ('Prompts','course-assets','video-audit','archive'):
        for p in (ROOT/area).rglob('*'):
            if p.suffix.lower() not in {'.mp4','.mov','.mkv'} or p.is_symlink() or not p.is_file() or v.rel(p) in deleted:continue
            s=p.stat();videos[v.rel(p)]=[s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev]
    fs=os.statvfs(ROOT);before=fs.f_bavail*fs.f_frsize;events=[]
    with (OUT/'deletion-log.jsonl').open('x') as log:
        for r in plan['files']:
            p=ROOT/r['path'];s=p.lstat();assert [s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev]==[r[k] for k in ('bytes','mtime_ns','inode','device')]
            p.unlink();event={k:r[k] for k in ('path','bytes','sha256','reason')};event['deleted_local']=datetime.now(ZONE).isoformat()
            log.write(json.dumps(event)+'\n');log.flush();events.append(event)
    changed=[]
    for name,state in videos.items():
        p=ROOT/name;assert p.is_file(),name;s=p.stat()
        if [s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev]!=state:changed.append(name)
    assert all((ROOT/name).is_file() for name in dependencies)
    assert all(not (ROOT/r['path']).exists() for r in events)
    fs=os.statvfs(ROOT);after=fs.f_bavail*fs.f_frsize
    receipt=dict(completed_local=datetime.now(ZONE).isoformat(),deleted_files=len(events),deleted_logical_gib=round(sum(r['bytes'] for r in events)/2**30,3),
                 measured_free_space_change_gib=round((after-before)/2**30,3),free_gib_after=round(after/2**30,3),retained_videos_checked=len(videos),
                 concurrent_video_updates=changed,deleted_by_extension=dict(Counter(Path(r['path']).suffix for r in events)))
    plan['deletion_performed']=True;(OUT/'verified-deletions.json').write_text(json.dumps(plan,indent=2)+'\n')
    (OUT/'deletion-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    after_storage=storage();(OUT/'remaining-after.json').write_text(json.dumps(after_storage,indent=2)+'\n')
    print(json.dumps(receipt,indent=2),flush=True)
    print(json.dumps(dict(remaining_audit_allocated_unique_gib=after_storage['allocated_unique_gib'],extensions=after_storage['extensions'],largest_folders=after_storage['largest_folders'][:6]),indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--delete',action='store_true');args=parser.parse_args()
    delete() if args.delete else plan()

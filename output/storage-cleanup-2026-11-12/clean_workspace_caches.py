"""Conservative cleanup outside video-audit. Never deletes source/video/history.

Targets old untracked UI/PDF-render screenshots, exact duplicate temporary PDFs,
and bytecode whose Python source remains. Keeps original artwork, active work,
all code, audio, build inputs and cleanup records. --delete applies saved plan.
"""
import argparse,ast,csv,hashlib,importlib.util,json,os,re,struct,subprocess
from collections import defaultdict,Counter
from datetime import date,datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE=Path(__file__).resolve().parent;OLD=BASE.parent/'storage-cleanup-2026-11-11'
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
v=module('scratch_helpers',OLD/'verify_and_clean_scratch.py')
edits=module('edit_helpers',OLD/'clean_edited_videos.py')
ROOT=v.ROOT;OUT=BASE/'workspace-pass';OUT.mkdir(exist_ok=True);ZONE=ZoneInfo('America/Chicago');CUTOFF=date(2026,11,4)
GEN=re.compile(r'^(?:current-|live-page-|diff-|searchable-|page(?:[-_.]|$)|frame[-_]|screenshot|overview|preview[-_]|rendered|keepsake|before[-_]|after[-_]|\d{2,})|(?:desktop|mobile|tablet)|[-_](?:375|390|768|1280|1440|1920)(?:[-_.]|$)',re.I)
INPUT_NAME=re.compile(r'donor|source|mask|patch|canvas|prepared|approved|original|reference|close',re.I)


def recent(p):
    dates=re.findall(r'20\d\d-\d\d-\d\d',v.rel(p))
    return bool(dates and max(dates)>=str(CUTOFF)) or datetime.fromtimestamp(p.stat().st_mtime,ZONE).date()>=CUTOFF


def write_csv(name,rows,fields):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)


def reference_state():
    records=edits.reference_state()
    for p in (ROOT/'tmp').rglob('*'):
        if p.is_file() and not p.is_symlink() and p.suffix.lower() in {'.py','.js','.cjs','.mjs','.swift','.sh','.json','.html','.md','.txt','.csv'}:
            s=p.stat();records[v.rel(p)]=[s.st_size,s.st_mtime_ns,s.st_ino]
    return records


def plan():
    assert not (OUT/'cache-deletion-log.jsonl').exists()
    checkpoint=reference_state();tracked=set(v.run('git','ls-files','-z').decode().split('\0'))
    protected=set();prefixes=set();pdfs=defaultdict(list);images=[];bytecode=[];held=[]
    token=re.compile(r'''(?:tmp|output|previews)/[^\s"'`<>)(\]}]{1,350}\.(?:png|jpg|jpeg|pdf|npy|wav|f32)(?![\w.])''',re.I)
    links=re.compile(r'''(?:!?\[[^\]]*\]\(|(?:src|href)=["'])([^\s)"']+\.(?:jpg|jpeg|png|pdf))''',re.I)
    for base,dirs,files in os.walk(ROOT,followlinks=False):
        dirs[:]=[d for d in dirs if d not in {'.git','.video-venv','node_modules','.superpowers'} and not (Path(base)/d).is_symlink() and not (Path(base)/d).name.startswith('storage-cleanup-')]
        for name in files:
            p=Path(base)/name
            if p.is_symlink() or p.suffix.lower() not in {'.json','.py','.js','.cjs','.mjs','.swift','.html','.md','.txt','.csv','.sh'}:continue
            try:
                if p.stat().st_size>20*2**20:continue
                text=p.read_text(errors='replace')
            except OSError:continue
            protected.update(ROOT/q for q in token.findall(text))
            for name in set(re.findall(r'(?<![\w.-])[\w.-]+\.(?:png|jpg|jpeg|pdf)(?![\w.])',text,re.I)):
                q=p.parent/name
                if q.is_file():protected.add(q)
            if p.suffix.lower() in {'.md','.html','.txt'}:
                for q in links.findall(text):
                    if '://' not in q:protected.add(Path(os.path.normpath(p.parent/q)))
            if p.suffix=='.py':
                try:tree=ast.parse(text)
                except SyntaxError:continue
                env={'ROOT':ROOT,'__file__':str(p)}
                for n in tree.body:
                    if isinstance(n,(ast.Assign,ast.AnnAssign)):
                        try:
                            value=v.evaluate(n.value,env)
                            for target in (n.targets if isinstance(n,ast.Assign) else [n.target]):
                                if isinstance(target,ast.Name):env[target.id]=value
                        except (ValueError,KeyError,TypeError,IndexError,AttributeError):pass
                for n in ast.walk(tree):
                    if not isinstance(n,ast.Call):continue
                    fn=getattr(n.func,'attr',getattr(n.func,'id',''))
                    if fn not in {'imread','open','glob','rglob','load','fromfile','PdfReader','read_bytes'}:continue
                    if fn=='open' and len(n.args)>1 and isinstance(n.args[1],ast.Constant) and any(c in str(n.args[1].value) for c in 'wa+'):continue
                    args=n.args if fn not in {'glob','rglob','read_bytes'} else [n.func.value]
                    paths=[]
                    for arg in args:
                        for expr in ast.walk(arg):
                            try:
                                value=v.evaluate(expr,env)
                                if isinstance(value,Path) and any(value.is_relative_to(ROOT/area) for area in ('tmp','output','previews')):paths.append(value)
                            except (ValueError,KeyError,TypeError,IndexError,AttributeError):pass
                    if paths:
                        prefix=max(paths,key=lambda q:len(q.parts))
                        if prefix not in {ROOT/'tmp',ROOT/'output',ROOT/'previews'}:prefixes.add(prefix)
    # PDF matches can be retained anywhere outside the cache scopes.
    for base,dirs,files in os.walk(ROOT,followlinks=False):
        dirs[:]=[d for d in dirs if d not in {'.git','node_modules','.video-venv'} and not (Path(base)/d).is_symlink()]
        for name in files:
            p=Path(base)/name
            if p.is_symlink():continue
            if p.suffix.lower()=='.pdf':pdfs[p.stat().st_size].append(p)
            if p.suffix.lower() in {'.png','.jpg','.jpeg'} and any(p.is_relative_to(ROOT/area) for area in ('tmp','output','previews')):images.append(p)
            if p.suffix=='.pyc' and '__pycache__' in p.parts:
                try:source=Path(importlib.util.source_from_cache(str(p)))
                except ValueError:continue
                if source.is_file() and source.is_relative_to(ROOT):bytecode.append((p,source))
    def eligible(p):
        if v.rel(p) in tracked:return 'Tracked file retained'
        if recent(p):return 'Recent work retained'
        if p in protected or any(q in prefixes for q in (p,*p.parents)):return 'Referenced source/build/review input retained'
        if p.stat().st_nlink>1:return 'Hardlinked source/copy retained'
        if any(re.search(r'(?:imagegen|donor|source|assets|prepared|upload|kit)',part,re.I) for part in p.relative_to(ROOT).parts[:-1]):return 'Original artwork/source/preparation directory retained'
        if 'trust-trap-cut-review-2026-10-27' in p.parts:return 'Approved audio-repair workspace retained'
        if INPUT_NAME.search(p.name):return 'Named source/artwork/approved material retained'
        return ''
    proposed=[]
    # Keep a compact overview in each old screenshot directory.
    overviews={p for p in images if re.match(r'^(?:overview|.*sheet)',p.name,re.I)}
    for p in images:
        reason=eligible(p)
        if not reason and p in overviews:reason='Compact visual summary retained'
        if not reason and not GEN.search(p.name):reason='Not an identified generated UI/PDF screenshot'
        if not reason and not re.search(r'audit|review|preview|render|check|test|inspection|screenshot|release|pdf',str(p.parent),re.I):
            tall=False
            if p.suffix.lower()=='.png':
                with p.open('rb') as f:header=f.read(24)
                if header[:8]==b'\x89PNG\r\n\x1a\n':
                    width,height=struct.unpack('>II',header[16:24]);tall=width in {375,390,414,768,1024,1280,1440,1920} and height>max(900,width)
            if not tall:reason='Source-versus-screenshot role is uncertain'
        if reason:held.append(dict(path=v.rel(p),bytes=p.stat().st_size,reason=reason))
        else:proposed.append(dict(**v.snapshot(p),reason='Old unreferenced generated UI/PDF-render screenshot',dependencies=[]))
    for paths in pdfs.values():
        if len(paths)<2:continue
        matches=defaultdict(list)
        for p in paths:matches[v.sha(p)].append(p)
        for peers in matches.values():
            if len(peers)<2:continue
            keeper=min(peers,key=lambda p:(v.rel(p) not in tracked,p.is_relative_to(ROOT/'tmp'),-p.stat().st_mtime_ns,v.rel(p)))
            for p in peers:
                if p==keeper or not p.is_relative_to(ROOT/'tmp'):continue
                reason=eligible(p)
                if reason:held.append(dict(path=v.rel(p),bytes=p.stat().st_size,reason=reason))
                else:proposed.append(dict(**v.snapshot(p),reason='Exact duplicate temporary PDF; identical PDF retained',keeper=v.rel(keeper),dependencies=[v.snapshot(keeper)]))
    for p,source in bytecode:
        if v.rel(p) in tracked or recent(p):continue
        proposed.append(dict(**v.snapshot(p),reason='Regenerable Python bytecode; original Python source retained',dependencies=[v.snapshot(source)]))
    needed={d['path'] for r in proposed for d in r['dependencies']};proposed=[r for r in proposed if r['path'] not in needed]
    assert checkpoint==reference_state(),'Source/reference records changed; reverify'
    (OUT/'cache-reference-state.json').write_text(json.dumps(checkpoint)+'\n')
    result=dict(created_local=datetime.now(ZONE).isoformat(),deletion_performed=False,files=proposed)
    (OUT/'cache-plan.json').write_text(json.dumps(result,indent=2)+'\n');write_csv('cache-plan.csv',proposed,['path','bytes','sha256','reason','keeper']);write_csv('cache-retained.csv',held,['path','bytes','reason'])
    summary=dict(files=len(proposed),logical_mib=round(sum(r['bytes'] for r in proposed)/2**20,2),by_reason={reason:dict(files=sum(r['reason']==reason for r in proposed),mib=round(sum(r['bytes'] for r in proposed if r['reason']==reason)/2**20,2)) for reason in {r['reason'] for r in proposed}})
    (OUT/'cache-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)


def delete():
    plan=json.loads((OUT/'cache-plan.json').read_text());assert not plan['deletion_performed'] and not (OUT/'cache-deletion-log.jsonl').exists()
    assert reference_state()==json.loads((OUT/'cache-reference-state.json').read_text()),'References changed; reverify'
    tracked=set(v.run('git','ls-files','-z').decode().split('\0'));deps={d['path']:d for r in plan['files'] for d in r['dependencies']}
    for name,d in deps.items():assert v.sha(ROOT/name)==d['sha256'],name
    for r in plan['files']:
        p=ROOT/r['path'];assert p.resolve()==p and not p.is_symlink() and r['path'] not in tracked
        assert p.suffix.lower() in {'.png','.jpg','.jpeg','.pdf','.pyc'} and not recent(p)
        assert v.snapshot(p)=={k:r[k] for k in ('path','bytes','mtime_ns','inode','device','sha256')}
    fs=os.statvfs(ROOT);before=fs.f_bavail*fs.f_frsize;events=[]
    with (OUT/'cache-deletion-log.jsonl').open('x') as log:
        for r in plan['files']:
            p=ROOT/r['path'];s=p.lstat();assert [s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev]==[r[k] for k in ('bytes','mtime_ns','inode','device')]
            p.unlink();event={k:r[k] for k in ('path','bytes','sha256','reason')};event['deleted_local']=datetime.now(ZONE).isoformat();log.write(json.dumps(event)+'\n');log.flush();events.append(event)
    assert all(not (ROOT/r['path']).exists() for r in events)
    assert all((ROOT/name).is_file() for name in deps)
    fs=os.statvfs(ROOT);after=fs.f_bavail*fs.f_frsize
    receipt=dict(completed_local=datetime.now(ZONE).isoformat(),deleted_files=len(events),deleted_logical_mib=round(sum(r['bytes'] for r in events)/2**20,2),measured_free_space_change_mib=round((after-before)/2**20,2),free_gib_after=round(after/2**30,3),
                 deleted_extensions=dict(Counter(Path(r['path']).suffix for r in events)),git_compaction_performed=False,git_integrity_issue='Pre-existing missing tree 9ebafe5699b2d64953beb739283137615441d65f; Git storage left unchanged')
    plan['deletion_performed']=True;(OUT/'cache-plan.json').write_text(json.dumps(plan,indent=2)+'\n');(OUT/'deletion-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--delete',action='store_true');args=p.parse_args();delete() if args.delete else plan()

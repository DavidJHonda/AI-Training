"""Remove only verified duplicate/superseded edits; keep all source roles.

Default produces a dependency-reviewed plan. --delete applies that saved plan.
No source-reference rewrites, Git changes, or production builds are performed.
"""
import argparse
import ast
import csv
import importlib.util
import json
import os
import re
from collections import defaultdict, Counter
from datetime import datetime, date
from pathlib import Path
from zoneinfo import ZoneInfo

BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('scratch_helpers',BASE/'verify_and_clean_scratch.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
ROOT=v.ROOT;ZONE=ZoneInfo('America/Chicago');CUTOFF=date(2026,11,4)
OUT=BASE/'edited-video-pass';OUT.mkdir(exist_ok=True)
EDIT=re.compile(r'(.+)-v(\d+)\.mp4$',re.I)
SOURCE_NAME=re.compile(r'donor|source|snapshot|frozen|original|legacy|raw|reroll|rewind|spine',re.I)
VIDEO_PATH=re.compile(r'''(?:Prompts|video-audit|course-assets|archive)/[^\s"'`<>\[\]{}(),;:!?]{1,350}\.(?:mp4|mov|mkv)(?![\w.])''',re.I)
OUTPUT_NAMES={'DEST','DST','DESTINATION','OUTPUT','OUTPUT_PATH','OUTPUT_FILE','OUTFILE','CANDIDATE','CANDIDATE_PATH','NEW_VIDEO','FINAL'}


def norm(path):
    return Path(os.path.normpath(str(v.local(path))))


def paths_in(value):
    if not isinstance(value,str):return []
    if value.endswith(('.mp4','.mov','.mkv')) and not any(c in value for c in '\n\r'):
        p=norm(value)
        if p.is_relative_to(ROOT) and ' ' not in value:return [p]
    return [norm(s) for s in VIDEO_PATH.findall(value)]


def save_csv(name,rows,fields):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)


def reference_state():
    records={}
    for base,dirs,files in os.walk(ROOT,followlinks=False):
        dirs[:]=[d for d in dirs if d not in {'.git','.video-venv','node_modules','output','tmp','.superpowers'} and not (Path(base)/d).is_symlink()]
        for name in files:
            p=Path(base)/name
            if p.suffix.lower() not in {'.json','.py','.md','.txt','.html','.js','.cjs','.mjs'} or p.is_symlink():continue
            s=p.stat();records[v.rel(p)]=[s.st_size,s.st_mtime_ns,s.st_ino]
    return records


def plan():
    assert not (OUT/'deletion-log.jsonl').exists(),'This pass has already run'
    tracked=set(v.run('git','ls-files','-z').decode().split('\0'))
    initial_references=reference_state()
    previous=BASE/'review-evidence-pass/protected-videos-before.json'
    if (OUT/'inventory.json').exists():previous=OUT/'inventory.json'
    for r in json.loads(previous.read_text()):
        p=ROOT/r['path']
        if not p.is_file() or p.is_symlink():continue
        s=p.stat()
        if (s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev)==(r['bytes'],r['mtime_ns'],r['inode'],r['device']):
            v.HASH_CACHE[(str(p),s.st_size,s.st_mtime_ns,s.st_ino)]=r['sha256']
    print('Inventorying video identities and installed release matches...',flush=True)
    inventory=[];by_hash=defaultdict(list);by_path={};families=defaultdict(list);by_basename=defaultdict(list)
    for area in ('Prompts','course-assets','video-audit','archive'):
        for base,dirs,files in os.walk(ROOT/area,followlinks=False):
            dirs[:]=[d for d in dirs if not (Path(base)/d).is_symlink()]
            for name in files:
                p=Path(base)/name
                if p.is_symlink() or p.suffix.lower() not in {'.mp4','.mov','.mkv'}:continue
                try:r=v.snapshot(p)
                except FileNotFoundError:continue
                m=EDIT.fullmatch(name)
                strict=bool(m and p.parent==ROOT/'Prompts' and not SOURCE_NAME.search(name))
                r.update(area=area,strict_edit=strict,family=m[1] if strict else '',version=int(m[2]) if strict else None)
                inventory.append(r);by_path[str(p)]=r;by_hash[r['sha256']].append(r)
                by_basename[p.name].append(r)
                if strict:families[r['family']].append(r)
    (OUT/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
    reasons=defaultdict(list)
    def protect(path,reason):
        p=norm(path)
        if str(p) in by_path:
            name=by_path[str(p)]['path']
            if reason not in reasons[name]:reasons[name].append(reason)
    def protect_source(path,reason,expected=None,resolve_historical=True):
        p=norm(path)
        if str(p) in by_path:
            protect(p,reason)
            if resolve_historical and expected and by_path[str(p)]['sha256']!=expected:
                for r in by_hash.get(expected,[]):protect(r['path'],reason+' (original source bytes behind replaced path)')
        elif resolve_historical and expected and expected in by_hash:
            # A historical source was renamed. Preserve every surviving match
            # unless its exact path is resolvable without altering provenance.
            for r in by_hash[expected]:protect(r['path'],reason+' (renamed source hash match)')
        elif p.name in by_basename:
            for r in by_basename[p.name]:protect(r['path'],reason+' (relative/renamed source filename)')
    for r in inventory:
        p=ROOT/r['path']
        if r['path'] in tracked:protect(p,'Tracked video')
        if r['area']=='course-assets':protect(p,'Installed/course asset')
        if SOURCE_NAME.search(p.name):protect(p,'Explicit donor/source/snapshot naming')
        if r['area']=='Prompts' and not r['strict_edit']:protect(p,'Raw donor or non-candidate source')
        if r['area']=='archive':protect(p,'Archived source retained')
        dates=re.findall(r'20\d\d-\d\d-\d\d',r['path'])
        if datetime.fromtimestamp(r['mtime_ns']/1e9,ZONE).date()>=CUTOFF or (dates and max(dates)>=str(CUTOFF)):
            protect(p,'Recent video or active audit work')
    for family,rows in families.items():
        for r in sorted(rows,key=lambda r:r['version'],reverse=True)[:2]:protect(r['path'],'Newest two edited versions in family')
        protect(max(rows,key=lambda r:r['mtime_ns'])['path'],'Most recently modified edit in family')

    # Exact identity, rather than a cache-key number, establishes each currently
    # installed edit. Missing/ambiguous matches never justify supersession.
    installed=defaultdict(list)
    for r in inventory:
        if r['area']!='course-assets':continue
        for match in by_hash[r['sha256']]:
            if match['strict_edit']:
                installed[match['family']].append(dict(canonical=r,candidate=match))
    for family,rows in families.items():
        if not installed[family]:
            for r in rows:protect(r['path'],'No hash-verified installed successor for this family')
            continue
        shipped=max(m['candidate']['version'] for m in installed[family])
        for r in rows:
            if r['version']>=shipped:protect(r['path'],'Installed version or newer/unresolved candidate')

    print('Tracing donor, parent-edit, and reconstruction dependencies...',flush=True)
    source_keys={'source','sources','source_files','source_hashes','source_video','source_path','source_snapshot',
                 'donor','donors','donor_files','donor_file','donor_rolls','graft_source','graft_audio','video_src',
                 'visual_donor','audio_source','picture_source','parent','parent_candidate','base','base_source',
                 'original','original_source','reference','snapshot','protected','protected_hashes','input','inputs'}
    json_scanned=0
    for area in ('video-audit','scripts','gemini-notebook','course-assets'):
        for base,dirs,files in os.walk(ROOT/area,followlinks=False):
            dirs[:]=[d for d in dirs if not (Path(base)/d).is_symlink()]
            for name in files:
                if not name.endswith('.json') or 'migration' in name:continue
                p=Path(base)/name
                try:
                    if p.stat().st_size>20*2**20:continue
                    obj=json.loads(p.read_text())
                except (ValueError,OSError):continue
                hashes=v.expected_hashes(obj);json_scanned+=1
                def gather(value,resolve_historical=True):
                    if isinstance(value,str):
                        for q in paths_in(value):protect_source(q,'Source/parent metadata: '+v.rel(p),hashes.get(str(q)),resolve_historical)
                    elif isinstance(value,dict):
                        for key,val in value.items():gather(key,resolve_historical);gather(val,resolve_historical)
                    elif isinstance(value,list):
                        for val in value:gather(val,resolve_historical)
                def walk(value):
                    if isinstance(value,dict):
                        for key,val in value.items():
                            if key.lower() in source_keys or key.lower().startswith(('donor_','source_file','input_')):gather(val,key.lower() not in {'protected','protected_hashes'})
                            else:walk(val)
                    elif isinstance(value,list):
                        for val in value:walk(val)
                walk(obj)

    # Previous cleanup promises to retain these exact paths for reconstruction.
    for path in (BASE/'verified-deletions.json',BASE/'review-evidence-pass/verified-deletions.json'):
        obj=json.loads(path.read_text())
        for r in obj['files']:
            for dep in r['dependencies']:
                if dep.get('kind')=='retained_file':protect(dep['path'],'Retained reconstruction source from previous cleanup')

    # Read code statically. Exclude its own output declaration from input refs;
    # preserve every other mentioned media path, including historical builders.
    scripts=v.scan_scripts()
    for p,data in scripts.items():
        outputs=set()
        for key,value in data['env'].items():
            if (key in OUTPUT_NAMES or key=='OUT') and isinstance(value,(Path,str)):
                for q in paths_in(str(value)):outputs.add(q)
        for node in ast.walk(data['tree']):
            if not isinstance(node,(ast.Assign,ast.AnnAssign)):continue
            targets=node.targets if isinstance(node,ast.Assign) else [node.target]
            if any((isinstance(t,ast.Name) and t.id in OUTPUT_NAMES) or (isinstance(t,ast.Attribute) and t.attr in OUTPUT_NAMES|{'OUT'}) for t in targets):
                for expr in ast.walk(node.value):
                    if isinstance(expr,ast.Constant) and isinstance(expr.value,str):outputs.update(paths_in(expr.value))
        inputs=set()
        for key,value in data['env'].items():
            if key not in OUTPUT_NAMES|{'OUT'} and isinstance(value,(Path,str)):
                inputs.update(paths_in(str(value)))
        for q in data['resolved_paths']:
            if q.suffix.lower() in {'.mp4','.mov','.mkv'} and norm(q) not in outputs:inputs.add(norm(q))
        for node in ast.walk(data['tree']):
            if isinstance(node,ast.Constant) and isinstance(node.value,str):
                for q in paths_in(node.value):
                    if q not in outputs:inputs.add(q)
        for q in inputs:protect(q,'Video input/reference in code: '+v.rel(p))

    # Notes can explicitly reserve an edited video as a future donor. Also
    # preserve direct runtime video references and code outside scripts/video.
    for base,dirs,files in os.walk(ROOT,followlinks=False):
        dirs[:]=[d for d in dirs if d not in {'.git','.video-venv','node_modules','output','tmp','.superpowers'} and not (Path(base)/d).is_symlink()]
        for name in files:
            p=Path(base)/name
            if p.suffix.lower() not in {'.md','.txt','.html','.js','.cjs','.mjs','.py'}:continue
            if p.is_relative_to(ROOT/'scripts/video') and p.suffix=='.py':continue
            try:
                if p.stat().st_size>10*2**20:continue
                text=p.read_text(errors='replace')
            except OSError:continue
            for line in text.splitlines():
                if p.suffix.lower() in {'.md','.txt'} and not re.search(r'donor|source|spine|frozen|snapshot|retain|keep|parent',line,re.I):continue
                for q in paths_in(line):protect(q,'Source reservation/runtime reference: '+v.rel(p))
                if p.suffix.lower() in {'.md','.txt'}:
                    for basename in re.findall(r'''[\w.-]+\.(?:mp4|mov|mkv)(?![\w.])''',line):
                        for r in by_basename.get(basename,[]):protect(r['path'],'Source reservation in notes: '+v.rel(p))

    proposed=[];held=[]
    def priority(r):
        return (r['area']!='course-assets',not bool(reasons[r['path']]),r['path'] not in tracked,-r['mtime_ns'],r['path'])
    # Also consolidate duplicate audit/review outputs. At least one identical
    # copy is explicitly retained, even when none was otherwise protected.
    for rows in by_hash.values():
        if len(rows)>1 and all(not reasons[r['path']] for r in rows):
            keeper=min(rows,key=priority)
            protect(keeper['path'],'Retained identical-video keeper')
    for r in inventory:
        path=r['path'];p=ROOT/path
        if reasons[path]:
            held.append(dict(path=path,bytes=r['bytes'],reasons=' | '.join(reasons[path][:10])))
            continue
        # A versioned Prompts edit can be superseded. Other audit MP4s can be
        # deleted only as exact duplicates of a preserved edited/course video.
        matches=[q for q in by_hash[r['sha256']] if q['path']!=path]
        keepers=[q for q in matches if reasons[q['path']]]
        if p.suffix.lower()=='.mp4' and keepers:
            keeper=min(keepers,key=priority)
            proposed.append(dict(**r,reason='Exact duplicate of a retained video',keeper=keeper['path'],successor_sha256=keeper['sha256']))
        elif r['strict_edit'] and installed[r['family']]:
            successors=[m for m in installed[r['family']] if m['candidate']['version']>r['version']]
            if successors:
                successor=max(successors,key=lambda m:m['candidate']['version'])
                proposed.append(dict(**r,reason='Superseded by newer hash-verified installed release; no source or active-candidate role found',
                                     keeper=successor['canonical']['path'],successor_sha256=successor['canonical']['sha256']))
            else:held.append(dict(path=path,bytes=r['bytes'],reasons='No verified newer installed release'))
        else:
            held.append(dict(path=path,bytes=r['bytes'],reasons='Unclassified/source-like footage; retained'))
    all_deleted={r['path'] for r in proposed}
    assert all(r['keeper'] not in all_deleted for r in proposed)
    result=dict(created_local=datetime.now(ZONE).isoformat(),root=str(ROOT),cutoff=str(CUTOFF),deletion_performed=False,files=proposed)
    assert initial_references==reference_state(),'Reference files changed during verification; rerun before deleting'
    (OUT/'reference-state.json').write_text(json.dumps(initial_references)+'\n')
    (OUT/'verified-deletions.json').write_text(json.dumps(result,indent=2)+'\n')
    save_csv('verified-deletions.csv',proposed,['path','bytes','sha256','reason','keeper','successor_sha256'])
    save_csv('retained-videos.csv',held,['path','bytes','reasons'])
    (OUT/'protected-source-references.json').write_text(json.dumps(dict(reasons),indent=2)+'\n')
    summary=dict(inventoried_videos=len(inventory),verified_files=len(proposed),verified_gib=round(sum(r['bytes'] for r in proposed)/2**30,3),
                 by_reason=dict(Counter(r['reason'] for r in proposed)),retained_videos=len(held),json_records_scanned=json_scanned,
                 families_with_hash_verified_installed_release=sum(bool(m) for m in installed.values()),
                 donor_and_active_policy='Keep raw/non-candidate sources, source-referenced edits, tracked/course videos, recent files, newest two edits per family, and installed-or-newer candidates.')
    (OUT/'verification-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)


def delete():
    plan=json.loads((OUT/'verified-deletions.json').read_text())
    assert not plan['deletion_performed'] and not (OUT/'deletion-log.jsonl').exists()
    assert reference_state()==json.loads((OUT/'reference-state.json').read_text()),'Donor/build references changed; reverify before deleting'
    tracked=set(v.run('git','ls-files','-z').decode().split('\0'))
    inventory=json.loads((OUT/'inventory.json').read_text());before_by_path={r['path']:r for r in inventory}
    refs=json.loads((OUT/'protected-source-references.json').read_text())
    deleted_paths={r['path'] for r in plan['files']}
    print('Rechecking duplicate keepers, installed successors, and exact deletion identities...',flush=True)
    for r in plan['files']:
        p=ROOT/r['path'];keep=ROOT/r['keeper']
        assert p.resolve()==p and not p.is_symlink() and p.suffix.lower()=='.mp4'
        assert p.is_relative_to(ROOT/'Prompts') or p.is_relative_to(ROOT/'video-audit')
        assert r['path'] not in tracked and not refs.get(r['path']) and not SOURCE_NAME.search(p.name)
        assert datetime.fromtimestamp(p.stat().st_mtime,ZONE).date()<CUTOFF
        assert v.snapshot(p)=={k:r[k] for k in ('path','bytes','mtime_ns','inode','device','sha256')}
        assert keep.is_file() and r['keeper'] not in deleted_paths and v.sha(keep)==r['successor_sha256']
        if r['reason'].startswith('Exact duplicate'):
            assert v.sha(keep)==r['sha256']
        else:
            assert r['strict_edit'] and r['family'] and keep.is_relative_to(ROOT/'course-assets')
    protected=[r for r in inventory if r['path'] not in deleted_paths]
    for r in protected:assert (ROOT/r['path']).is_file(),r['path']
    fs=os.statvfs(ROOT);before=fs.f_bavail*fs.f_frsize
    events=[]
    print(f"Removing {len(plan['files'])} verified duplicate/superseded edits...",flush=True)
    with (OUT/'deletion-log.jsonl').open('x') as log:
        for r in plan['files']:
            p=ROOT/r['path'];s=p.lstat()
            assert (s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev)==(r['bytes'],r['mtime_ns'],r['inode'],r['device'])
            p.unlink()
            event={k:r[k] for k in ('path','bytes','sha256','reason','keeper','successor_sha256')}
            event['deleted_local']=datetime.now(ZONE).isoformat();log.write(json.dumps(event)+'\n');log.flush();events.append(event)
    changed=[]
    for r in protected:
        p=ROOT/r['path'];assert p.is_file(),f'Retained video missing: {p}'
        s=p.stat()
        if (s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev)!=(r['bytes'],r['mtime_ns'],r['inode'],r['device']):
            if v.sha(p)!=r['sha256']:changed.append(r['path'])
    assert all(not (ROOT/r['path']).exists() for r in events)
    fs=os.statvfs(ROOT);after=fs.f_bavail*fs.f_frsize
    receipt=dict(completed_local=datetime.now(ZONE).isoformat(),deleted_files=len(events),deleted_logical_gib=round(sum(r['bytes'] for r in events)/2**30,3),
                 measured_free_space_change_gib=round((after-before)/2**30,3),free_gib_after=round(after/2**30,3),
                 retained_videos_verified=len(protected),all_donor_source_and_active_roles_retained=True,
                 concurrent_updates_to_retained_videos=changed,deleted_by_reason=dict(Counter(r['reason'] for r in events)))
    plan['deletion_performed']=True
    (OUT/'verified-deletions.json').write_text(json.dumps(plan,indent=2)+'\n')
    (OUT/'deletion-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--delete',action='store_true');args=p.parse_args()
    delete() if args.delete else plan()

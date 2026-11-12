"""Selectively retire superseded QA captures and unused analysis caches.

Never deletes video, artwork/build inputs, current-release QA, or recent work.
Keeps written records and compact visual summaries of each retired review.
Default verifies an explicit plan; --delete applies only that saved plan.
"""
import argparse,ast,csv,hashlib,importlib.util,json,math,os,re,struct,subprocess,wave
from collections import defaultdict,Counter
from datetime import date,datetime
from pathlib import Path
from zoneinfo import ZoneInfo

BASE=Path(__file__).resolve().parent
OLD=BASE.parent/'storage-cleanup-2026-11-11'
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
v=module('scratch_helpers',OLD/'verify_and_clean_scratch.py')
edits=module('edit_helpers',OLD/'clean_edited_videos.py')
ROOT=v.ROOT;ZONE=ZoneInfo('America/Chicago');OUT=BASE/'selective-evidence-pass';OUT.mkdir(exist_ok=True)
CUTOFF=date(2026,11,4)
IMAGES={'.jpg','.jpeg','.png'}
ALL_EXT=IMAGES|{'.npy','.f32','.wav','.m4a','.mp3'}
KEEP_NAMES=re.compile(r'donor|source|canvas|mask|patch|snapshot|prepared|original|close|reference|approved',re.I)
AUTO_IMAGE=re.compile(r'^(?:boundary-|sheet-|guard-sheet-|encoded-sheet-|preview-sheet-|overview-|contact-|application-contact-|encoded-contact-|frame-|encoded-|output-|preview-|source-|kb\d|transition-|guard-|state[s]?-|f?\d)',re.I)
AUTO_AUDIO=re.compile(r'^(?:join-|encoded|decoded|listen-|preview-|audio-check|verify-|check-|ending-check|narration-repair-review)',re.I)


def recent(p):
    dates=re.findall(r'20\d\d-\d\d-\d\d',v.rel(p))
    return bool(dates and max(dates)>=str(CUTOFF)) or datetime.fromtimestamp(p.stat().st_mtime,ZONE).date()>=CUTOFF


def normalized(path):return Path(os.path.normpath(str(v.local(path))))


def csv_write(name,rows,fields):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)


def output_paths(data):
    paths=set()
    for name,value in data['env'].items():
        if name in edits.OUTPUT_NAMES and isinstance(value,(str,Path)):paths.update(edits.paths_in(str(value)))
    for node in ast.walk(data['tree']):
        if not isinstance(node,(ast.Assign,ast.AnnAssign)):continue
        targets=node.targets if isinstance(node,ast.Assign) else [node.target]
        if any((isinstance(t,ast.Name) and t.id in edits.OUTPUT_NAMES) or (isinstance(t,ast.Attribute) and t.attr in edits.OUTPUT_NAMES) for t in targets):
            for expr in ast.walk(node.value):
                if isinstance(expr,ast.Constant) and isinstance(expr.value,str):paths.update(edits.paths_in(expr.value))
    return {normalized(p) for p in paths}


def plan():
    assert not (OUT/'deletion-log.jsonl').exists()
    checkpoint=edits.reference_state();tracked=set(v.run('git','ls-files','-z').decode().split('\0'))
    old_inv=json.loads((OLD/'edited-video-pass/inventory.json').read_text())
    for r in old_inv:
        p=ROOT/r['path']
        if not p.is_file() or p.is_symlink():continue
        s=p.stat()
        if [s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev]==[r[k] for k in ('bytes','mtime_ns','inode','device')]:v.HASH_CACHE[(str(p),s.st_size,s.st_mtime_ns,s.st_ino)]=r['sha256']
    print('Refreshing video identities, current releases, and active-candidate bindings...',flush=True)
    videos=[];by_path={};families=defaultdict(list);by_hash=defaultdict(list)
    for area in ('Prompts','course-assets','video-audit','archive'):
        for base,dirs,files in os.walk(ROOT/area,followlinks=False):
            dirs[:]=[d for d in dirs if not (Path(base)/d).is_symlink()]
            for name in files:
                p=Path(base)/name
                if p.is_symlink() or p.suffix.lower() not in {'.mp4','.mov','.mkv'}:continue
                r=v.snapshot(p);videos.append(r);by_path[str(p)]=r;by_hash[r['sha256']].append(r)
                match=edits.EDIT.fullmatch(name)
                if p.parent==ROOT/'Prompts' and match and not edits.SOURCE_NAME.search(name):families[match[1]].append(dict(r,version=int(match[2])))
    (OUT/'videos-before.json').write_text(json.dumps(videos,indent=2)+'\n')
    text=(ROOT/'index.html').read_text();block=text.split('const LESSON_VIDEOS = {',1)[1].split('\n};',1)[0]
    current={ROOT/p for p in re.findall(r'course-assets/[^"?]+\.mp4',block)}
    releases={};current_hashes=set();active_videos=set()
    for p in current:
        r=by_path.get(str(p))
        if not r:continue
        current_hashes.add(r['sha256']);active_videos.add(p)
        for family,rows in families.items():
            matches=[row for row in rows if row['sha256']==r['sha256']]
            if matches:releases[family]=dict(canonical=r,version=max(row['version'] for row in matches))
    for family,rows in families.items():
        if family=='flattery-engagement':continue # Explicitly retired merged lesson; briefing.md records its successor.
        active_videos.update(ROOT/r['path'] for r in sorted(rows,key=lambda r:r['version'],reverse=True)[:2])
    active_videos.update(ROOT/r['path'] for r in videos if recent(ROOT/r['path']))
    active_hashes={by_path[str(p)]['sha256'] for p in active_videos if str(p) in by_path}

    scripts=v.scan_scripts();initial={p for p,data in scripts.items() if output_paths(data)&active_videos}
    for p,data in scripts.items():
        if re.search(r'(?:\.OUT|\bOUT|\bAUDIT)\s*=.*video-audit/[^\n]*2026-11-(?:0[4-9]|[12]\d|30)',data['text']):initial.add(p)
    # Include QA of active producers, without treating every old diagnostic that
    # imports a shared renderer as active work.
    active=initial|{p for p,data in scripts.items() if p.name.startswith(('qa_','review_','verify_')) and any(q.stem in data['imports'] for q in initial)}
    modules={p.stem:p for p in scripts}
    while True:
        expanded=active|{modules[name] for p in active for name in scripts[p]['imports'] if name in modules}
        if expanded==active:break
        active=expanded

    input_rules=[];protected=set();linked=set();metadata=defaultdict(list)
    # Preserve actual technical reconstruction inputs. An unused duplicate QA
    # keeper can now itself be retired when its entire review is superseded.
    for file in (OLD/'verified-deletions.json',OLD/'review-evidence-pass/verified-deletions.json',OLD/'audit-cache-pass/verified-deletions.json'):
        obj=json.loads(file.read_text())
        for r in obj['files']:
            if 'duplicate' in r.get('reason','').lower() or 'duplicate' in r.get('proof','').lower():continue
            for d in r['dependencies']:
                if d.get('kind','retained_file')=='retained_file':protected.add(ROOT/d['path'])
    for p,data in scripts.items():
        if not p.name.startswith(('build','fix','repair','soften','mute','cut')) and p not in active:continue
        for node in ast.walk(data['tree']):
            if not isinstance(node,ast.Call):continue
            name=getattr(node.func,'attr',getattr(node.func,'id',''))
            if name not in {'imread','open','glob','rglob','load','fromfile','read_bytes','readwav','loadwav','pcm'}:continue
            if name=='open' and len(node.args)>1 and isinstance(node.args[1],ast.Constant) and any(c in str(node.args[1].value) for c in 'wa+'):continue
            args=node.args if name not in {'glob','rglob','read_bytes'} else [node.func.value]
            hints=' '.join(str(n.value) for arg in args for n in ast.walk(arg) if isinstance(n,ast.Constant) and isinstance(n.value,str))
            explicit={ext for ext in ALL_EXT|{'.json','.mp4','.mkv','.txt','.py'} if ext in hints}
            if explicit and not explicit&ALL_EXT:continue
            allowed=explicit&ALL_EXT if explicit&ALL_EXT else (IMAGES if name=='imread' else ({'.npy'} if name=='load' else ALL_EXT))
            for arg in args:
                found=[]
                for expr in ast.walk(arg):
                    try:
                        value=v.evaluate(expr,data['env'])
                        if isinstance(value,Path) and value!=ROOT/'video-audit' and value.is_relative_to(ROOT/'video-audit'):found.append(value)
                    except (ValueError,KeyError,TypeError,IndexError,AttributeError):pass
                if found:input_rules.append((max(found,key=lambda q:len(q.parts)),allowed,p))

    print('Classifying superseded QA scopes and preserving all specification inputs...',flush=True)
    image_token=re.compile(r'''video-audit/[^\s"'`<>)(\]}]{1,360}\.(?:jpg|jpeg|png)(?![\w.])''',re.I)
    markdown_link=re.compile(r'''(?:!?\[[^\]]*\]\(|(?:src|href)=["'])([^\s)"']+\.(?:jpg|jpeg|png))''',re.I)
    for base,dirs,files in os.walk(ROOT,followlinks=False):
        dirs[:]=[d for d in dirs if d not in {'.git','.video-venv','node_modules','output','tmp','.superpowers'} and not (Path(base)/d).is_symlink()]
        for name in files:
            p=Path(base)/name
            if p.suffix.lower() not in {'.json','.md','.html','.txt'} or p.is_symlink():continue
            try:
                if p.stat().st_size>20*2**20:continue
                content=p.read_text(errors='replace')
            except OSError:continue
            if p.suffix=='.json':
                try:obj=json.loads(content)
                except ValueError:continue
                if isinstance(obj,dict):
                    target=obj.get('candidate') or obj.get('output')
                    if isinstance(target,str) and target.lower().endswith('.mp4') and p.is_relative_to(ROOT/'video-audit'):
                        q=normalized(target);match=edits.EDIT.fullmatch(q.name)
                        if match:metadata[p.parent].append(dict(meta=p,candidate=q,family=match[1],version=int(match[2]),sha256=obj.get('candidate_sha256') or obj.get('output_sha256') or obj.get('render_sha256') or obj.get('sha256')))
                def inputs(value):
                    if isinstance(value,str) and value.lower().endswith(('.jpg','.jpeg','.png','.npy','.f32','.wav')) and '\n' not in value:
                        for q in (normalized(value),Path(os.path.normpath(p.parent/value))):
                            if q.is_relative_to(ROOT/'video-audit') and q.is_file():protected.add(q)
                    elif isinstance(value,dict):
                        for k,val in value.items():inputs(k);inputs(val)
                    elif isinstance(value,list):
                        for val in value:inputs(val)
                inputs(obj)
                protected.update(ROOT/q for q in image_token.findall(content))
            elif p.suffix in {'.md','.html'}:
                for val in markdown_link.findall(content):
                    if '://' not in val:linked.add(Path(os.path.normpath(p.parent/val)))
                linked.update(ROOT/q for q in image_token.findall(content))

    scope_cache={}
    def scope(p):
        for parent in p.parents:
            if parent==ROOT/'video-audit':break
            if parent not in metadata:continue
            if parent in scope_cache:return scope_cache[parent]
            entries=metadata[parent];families_here={m['family'] for m in entries};result=None
            if len(families_here)==1:
                family=next(iter(families_here));m=max(entries,key=lambda row:row['version'])
                any_active=any(row['candidate'] in active_videos or row['sha256'] in active_hashes for row in entries)
                if not any_active and family in releases and m['version']<releases[family]['version']:
                    result=dict(scope=parent,manifest=m['meta'],candidate=m['candidate'],family=family,successor=releases[family]['canonical'],reason='Superseded QA build; newer installed release verified by SHA-256')
                elif not any_active and family=='flattery-engagement' and 'flattery-trap' in releases:
                    result=dict(scope=parent,manifest=m['meta'],candidate=m['candidate'],family=family,successor=releases['flattery-trap']['canonical'],reason='Retired merged Flattery/Engagement QA; standalone Flattery Trap release and archival donors retained')
            scope_cache[parent]=result;return result
        return None

    reader_index=defaultdict(lambda:defaultdict(set))
    for prefix,exts,script in input_rules:
        for ext in exts:reader_index[ext][prefix].add(script)
    def readers(p):
        lookup=reader_index[p.suffix.lower()]
        return {script for prefix in (p,*p.parents) for script in lookup.get(prefix,())}
    candidates=[];held=[];scoped_images=defaultdict(list);all_scope_images=defaultdict(list)
    files=[]
    for base,dirs,names in os.walk(ROOT/'video-audit',followlinks=False):
        dirs[:]=[d for d in dirs if not (Path(base)/d).is_symlink()]
        for name in names:
            p=Path(base)/name
            if p.suffix.lower() in ALL_EXT and not p.is_symlink():files.append(p)
    for p in files:
        reason='';s=p.stat();ext=p.suffix.lower();sc=scope(p)
        if sc and ext in IMAGES:all_scope_images[sc['scope']].append(p)
        if v.rel(p) in tracked:reason='Tracked record'
        elif recent(p):reason='Recent work'
        elif p in protected:reason='Specification or retained technical reconstruction input'
        elif readers(p):reason='Read by a production build or active QA'
        elif ext in IMAGES:
            if p in linked:reason='Linked visual evidence retained with written report'
            elif KEEP_NAMES.search(p.name):reason='Reusable artwork, donor/source still, or named reconstruction image'
            elif not AUTO_IMAGE.search(p.name):reason='Not an identified generated QA capture'
            elif not sc:reason='Current, active, or unverified review scope'
            else:scoped_images[sc['scope']].append((p,sc));continue
        elif p.name=='expected-thumbnails.npy':
            if not sc:reason='Active/current or unresolved thumbnail comparison cache'
            else:
                with p.open('rb') as f:
                    assert f.read(6)==b'\x93NUMPY';version=tuple(f.read(2));n=struct.unpack('<H' if version==(1,0) else '<I',f.read(2 if version==(1,0) else 4))[0];header=ast.literal_eval(f.read(n).decode('latin1').strip());offset=f.tell()
                shape=header.get('shape',());dtype=header.get('descr')
                if dtype not in {'|u1','<u1'} or len(shape)!=4 or shape[-1]!=3 or offset+math.prod(shape)!=s.st_size:reason='Not a verified generated thumbnail array'
                else:candidates.append((p,sc,'Unused generated visual-QA thumbnail cache',dict(npy_shape=list(shape),npy_dtype=dtype)));continue
        elif ext=='.wav' and AUTO_AUDIO.search(p.name) and not KEEP_NAMES.search(p.name) and sc:
            # Listening/check clips are obsolete QA outputs, not uncompressed
            # production masters; all build and active-QA reads were excluded.
            try:
                with wave.open(str(p)) as w:details=dict(channels=w.getnchannels(),rate=w.getframerate(),sample_width=w.getsampwidth(),frames=w.getnframes())
                candidates.append((p,sc,'Superseded listening/encoded-audio diagnostic',details));continue
            except wave.Error:reason='Unsupported/uncertain audio encoding'
        else:reason='Retain master audio, frame maps, and unclassified analysis inputs'
        held.append(dict(path=v.rel(p),bytes=s.st_size,reason=reason))

    # Keep two compact overview/contact/state sheets per retired review scope.
    # When no aggregate survives, keep first/last captures as visual sentinels.
    summaries=[]
    for owner,rows in scoped_images.items():
        existing=[p for p in all_scope_images[owner] if re.search(r'contact|sheet|overview|summary|states',p.name,re.I) and not recent(p)]
        aggregate=sorted(existing,key=lambda p:(len(p.relative_to(owner).parts),p.name))
        keep=set(aggregate[:2]) if aggregate else {rows[0][0],rows[-1][0]}
        summaries.extend(v.rel(p) for p in keep)
        for p,sc in rows:
            if p in keep:held.append(dict(path=v.rel(p),bytes=p.stat().st_size,reason='Compact summary of superseded review retained'))
            else:candidates.append((p,sc,'Superseded generated QA capture; compact summary and written records retained',{}))

    print(f'Classified {len(candidates)} expendable QA artifacts; checksumming and saving the exact plan...',flush=True)
    verified=[]
    for p,sc,reason,details in candidates:
        deps=[v.snapshot(sc['manifest']),sc['successor']]
        if sc['family']=='flattery-engagement':deps.append(v.snapshot(ROOT/'briefing.md'))
        verified.append(dict(**v.snapshot(p),reason=reason,scope=v.rel(sc['scope']),successor=sc['successor']['path'],details=details,dependencies=deps))
    assert checkpoint==edits.reference_state(),'Build/reference files changed; reverify before deleting'
    (OUT/'reference-state.json').write_text(json.dumps(checkpoint)+'\n')
    result=dict(created_local=datetime.now(ZONE).isoformat(),deletion_performed=False,files=verified)
    (OUT/'verified-deletions.json').write_text(json.dumps(result,indent=2)+'\n')
    csv_write('verified-deletions.csv',verified,['path','bytes','sha256','reason','scope','successor'])
    csv_write('retained-evidence.csv',held,['path','bytes','reason'])
    (OUT/'retained-review-summaries.json').write_text(json.dumps(sorted(set(summaries)),indent=2)+'\n')
    summary=dict(verified_files=len(verified),verified_gib=round(sum(r['bytes'] for r in verified)/2**30,3),by_extension={ext:dict(files=sum(Path(r['path']).suffix==ext for r in verified),gib=round(sum(r['bytes'] for r in verified if Path(r['path']).suffix==ext)/2**30,3)) for ext in sorted(ALL_EXT)},
                 retained_visual_summaries=len(set(summaries)),retained_files=len(held),retained_reasons=dict(Counter(r['reason'] for r in held)),active_modules_checked=len(active),videos_protected=len(videos))
    (OUT/'verification-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)


def delete():
    plan=json.loads((OUT/'verified-deletions.json').read_text());assert not plan['deletion_performed'] and not (OUT/'deletion-log.jsonl').exists()
    assert edits.reference_state()==json.loads((OUT/'reference-state.json').read_text()),'Build/reference files changed; reverify'
    tracked=set(v.run('git','ls-files','-z').decode().split('\0'));deps={d['path']:d for r in plan['files'] for d in r['dependencies']}
    print('Rechecking installed successors, source records, and exact deletion identities...',flush=True)
    for name,d in deps.items():assert v.sha(ROOT/name)==d['sha256'],name
    for r in plan['files']:
        p=ROOT/r['path'];assert p.resolve()==p and p.is_relative_to(ROOT/'video-audit') and not p.is_symlink()
        assert p.suffix.lower() in IMAGES|{'.npy','.wav'} and r['path'] not in tracked and not recent(p)
        assert v.snapshot(p)=={k:r[k] for k in ('path','bytes','mtime_ns','inode','device','sha256')}
    videos=json.loads((OUT/'videos-before.json').read_text());states={}
    for r in videos:
        p=ROOT/r['path'];assert p.is_file(),r['path'];s=p.stat();states[r['path']]=[s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev]
    fs=os.statvfs(ROOT);before=fs.f_bavail*fs.f_frsize;events=[]
    print(f"Removing {len(plan['files'])} superseded QA/analysis artifacts...",flush=True)
    with (OUT/'deletion-log.jsonl').open('x') as log:
        for r in plan['files']:
            p=ROOT/r['path'];s=p.lstat();assert [s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev]==[r[k] for k in ('bytes','mtime_ns','inode','device')]
            p.unlink();event={k:r[k] for k in ('path','bytes','sha256','reason','scope','successor')};event['deleted_local']=datetime.now(ZONE).isoformat();log.write(json.dumps(event)+'\n');log.flush();events.append(event)
    changed=[]
    for name,state in states.items():
        p=ROOT/name;assert p.is_file(),name;s=p.stat()
        if [s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev]!=state:changed.append(name)
    assert all((ROOT/name).is_file() for name in deps)
    assert all((ROOT/name).is_file() for name in json.loads((OUT/'retained-review-summaries.json').read_text()))
    assert all(not (ROOT/r['path']).exists() for r in events)
    fs=os.statvfs(ROOT);after=fs.f_bavail*fs.f_frsize
    receipt=dict(completed_local=datetime.now(ZONE).isoformat(),deleted_files=len(events),deleted_logical_gib=round(sum(r['bytes'] for r in events)/2**30,3),measured_free_space_change_gib=round((after-before)/2**30,3),free_gib_after=round(after/2**30,3),
                 protected_videos_verified=len(videos),all_videos_retained=True,concurrent_video_updates=changed,deleted_extensions=dict(Counter(Path(r['path']).suffix for r in events)),written_records_and_current_release_QA_retained=True)
    plan['deletion_performed']=True;(OUT/'verified-deletions.json').write_text(json.dumps(plan,indent=2)+'\n');(OUT/'deletion-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--delete',action='store_true');args=parser.parse_args();delete() if args.delete else plan()

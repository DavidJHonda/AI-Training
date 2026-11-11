"""Conservative review-cache cleanup. Default verifies; --delete uses saved plan.

Never deletes video, WAV, source artwork, contact sheets, transition strips,
small frame-map arrays, tracked files, recent work, or prior reconstruction inputs.
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

BASE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('scratch_helpers', BASE/'verify_and_clean_scratch.py')
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
ROOT, ZONE = v.ROOT, ZoneInfo('America/Chicago')
OUT = BASE/'review-evidence-pass'
OUT.mkdir(exist_ok=True)
CUTOFF = date(2026, 11, 4)
IMAGE_EXT = {'.jpg', '.jpeg', '.png'}
ARRAY_EXT = {'.npy', '.f32'}
FRAME = re.compile(r'^(?:(?:f|frame[-_]?|encoded[-_]?|output[-_]?|preview[-_]?)\d+|\d{3,})(?:[._-].*)?\.(?:jpg|jpeg|png)$', re.I)
FRAME_DIRS = {'preview','previews','frames','encoded','encoded-frames','encoded-preview','encoded-qa','qa','candidate-frames','review-frames'}
PROTECTED_WORDS = re.compile(r'donor|canvas|mask|patch|asset|prepared|sheet|contact|boundary|transition|close|source|before|original', re.I)


def save_csv(name, rows, fields):
    with (OUT/name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)


def known_video_catalog():
    prior_catalog = OUT/'protected-videos-before.json'
    previous = json.loads((prior_catalog if prior_catalog.exists() else BASE/'protected-videos-before.json').read_text())
    # Reuse prior verified hashes only when size, nanosecond mtime, inode and
    # device still match. New/changed videos get fresh SHA-256 values.
    for r in previous:
        p = ROOT/r['path']
        if p.is_file():
            s = p.stat()
            if (s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev)==(r['bytes'],r['mtime_ns'],r['inode'],r['device']):
                v.HASH_CACHE[(str(p),s.st_size,s.st_mtime_ns,s.st_ino)] = r['sha256']
    catalog = defaultdict(list)
    protected = []
    for area in ('Prompts','course-assets','video-audit','archive'):
        for base,dirs,files in os.walk(ROOT/area, followlinks=False):
            dirs[:] = [n for n in dirs if not (Path(base)/n).is_symlink()]
            for n in files:
                p = Path(base)/n
                if p.is_symlink() or p.suffix.lower() not in {'.mp4','.mov','.mkv'}:
                    continue
                record = v.snapshot(p)
                protected.append(record)
                catalog[record['sha256']].append(p)
    return catalog, protected


def plan():
    assert not (OUT/'deletion-log.jsonl').exists(), 'This pass has already run'
    tracked = set(v.run('git','ls-files','-z').decode().split('\0'))
    earlier = json.loads((BASE/'verified-deletions.json').read_text())
    prior_inputs = {d['path'] for r in earlier['files'] for d in r['dependencies'] if d['kind']=='retained_file'}
    scripts = v.scan_scripts()
    print('Checking video originals, cached-frame inputs, and build references...', flush=True)
    catalog, protected_videos = known_video_catalog()
    (OUT/'protected-videos-before.json').write_text(json.dumps(protected_videos,indent=2)+'\n')

    # A producer may set its own OUT or an imported renderer's base.OUT.
    def owns(data, folder):
        d = ROOT/folder
        return any(isinstance(data['env'].get(k),Path) and (data['env'][k]==d or d in data['env'][k].parents) for k in ('OUT','AUDIT')) or bool(re.search(r'\.OUT\s*=.*'+re.escape(folder),data['text']))

    # Protect prefixes used by image reads/globs, including dynamic filenames.
    read_prefixes = set()
    for p,data in scripts.items():
        if not p.name.startswith('build'):
            continue
        for node in ast.walk(data['tree']):
            if not isinstance(node,ast.Call):
                continue
            fn = getattr(node.func,'attr',getattr(node.func,'id',''))
            if fn not in {'imread','open','glob','rglob'}:
                continue
            args = node.args if fn not in {'glob','rglob'} else [node.func.value]
            for arg in args:
                found = []
                for expr in ast.walk(arg):
                    try:
                        value = v.evaluate(expr,data['env'])
                        if isinstance(value,Path) and value.is_relative_to(ROOT/'video-audit'):
                            found.append(value)
                    except (ValueError,KeyError,TypeError,IndexError,AttributeError):
                        pass
                if found:
                    read_prefixes.add(max(found,key=lambda q:len(q.parts)))

    # Protect images and arrays explicitly named as inputs by JSON specs. Output
    # review lists do not make a frame an input; image/path/asset fields do.
    json_inputs = set()
    metadata = defaultdict(list)
    input_keys = {'image','asset','path','snapshot','donor','canvas','still','mask','audio_source','picture_source','source','source_snapshot'}
    def gather(obj):
        if isinstance(obj,dict):
            for k,val in obj.items():
                if k in input_keys and isinstance(val,str) and '/' in val and Path(val).suffix.lower() in IMAGE_EXT|ARRAY_EXT:
                    q = v.local(val)
                    if q.is_relative_to(ROOT):
                        json_inputs.add(str(q.relative_to(ROOT)))
                gather(val)
        elif isinstance(obj,list):
            for val in obj:
                gather(val)
    for base,dirs,files in os.walk(ROOT/'video-audit',followlinks=False):
        for n in files:
            if not n.endswith('.json'):
                continue
            p = Path(base)/n
            try:
                if p.stat().st_size>20*2**20:
                    continue
                obj = json.loads(p.read_text())
            except (ValueError,OSError):
                continue
            gather(obj)
            if n in {'edit-manifest.json','manifest.json'} and isinstance(obj,dict):
                folder = '/'.join(p.relative_to(ROOT).parts[:2])
                metadata[folder].append((p,obj))

    source_cache = {}
    def media_proof(folder, encoded_only):
        key = (folder,encoded_only)
        if key in source_cache:
            return source_cache[key]
        answer = None
        for meta,obj in sorted(metadata[folder],key=lambda pair:len(pair[0].parts)):
            hashes = v.expected_hashes(obj)
            deps = []
            if encoded_only:
                path = obj.get('candidate') or obj.get('output')
                expected = obj.get('candidate_sha256') or obj.get('output_sha256') or obj.get('render_sha256') or obj.get('sha256')
                inputs = {str(v.local(path)):expected} if isinstance(path,str) and isinstance(expected,str) and re.fullmatch('[0-9a-f]{64}',expected) else {}
            else:
                inputs = {name:hashes.get(name) for name in v.source_paths(obj) if Path(name).suffix.lower() in {'.mp4','.mov','.mkv'}}
            if not inputs or not all(inputs.values()):
                continue
            for name,expected in inputs.items():
                matches = catalog.get(expected,[])
                if not matches:
                    break
                deps.append(dict(kind='retained_file',original_path=name,**v.snapshot(matches[0])))
            else:
                deps.append(dict(kind='retained_file',**v.snapshot(meta)))
                answer = deps
                break
        source_cache[key] = answer
        return answer

    approved,held = [],[]
    for base,dirs,files in os.walk(ROOT/'video-audit',followlinks=False):
        dirs[:] = [n for n in dirs if not (Path(base)/n).is_symlink()]
        for n in files:
            p = Path(base)/n
            ext = p.suffix.lower()
            if ext not in IMAGE_EXT|ARRAY_EXT or p.is_symlink():
                continue
            name = str(p.relative_to(ROOT));parts = Path(name).parts;folder='/'.join(parts[:2]);s=p.stat()
            dates = re.findall(r'20\d\d-\d\d-\d\d',parts[1]);reason='';proof='';deps=[]
            if name in tracked:
                reason='Tracked record'
            elif not dates or max(dates)>=str(CUTOFF) or datetime.fromtimestamp(s.st_mtime,ZONE).date()>=CUTOFF:
                reason='Recent work or undated provenance'
            elif any(k in folder for k in ('opener','how-ai-answers','why-answers-vary')):
                reason='Lesson family with ongoing work'
            elif name in prior_inputs or name in json_inputs:
                reason='Retained reconstruction/specification input'
            elif any(q in read_prefixes for q in (p,*p.parents)):
                reason='Image read/glob dependency in build code'
            elif ext in IMAGE_EXT:
                if PROTECTED_WORDS.search(n) or not FRAME.fullmatch(n):
                    reason='Retain summary evidence, artwork, and named stills'
                elif not (set(parts[2:-1]) & FRAME_DIRS or re.match(r'^(?:frame|encoded|output|preview|f)\d',n.replace('-',''),re.I)):
                    reason='Not a recognized review frame-dump location'
                else:
                    encoded = any(part.startswith('encoded') for part in parts[2:-1]) or n.startswith(('encoded-','output-'))
                    deps = media_proof(folder,True)
                    if deps and not encoded:
                        originals = media_proof(folder,False)
                        deps = deps + originals if originals else None
                    if deps:
                        proof='Unreferenced numbered review frame; original video bytes and metadata retained'
                    else:
                        reason='Cannot verify original video for this frame dump'
            else:
                if s.st_size<2*2**20:
                    reason='Retain small frame maps and diagnostic records'
                else:
                    owners = [(q,data) for q,data in scripts.items() if q.name.startswith('build') and owns(data,folder)]
                    consumers=[]
                    for q,data in scripts.items():
                        if not q.name.startswith('build') or owns(data,folder):
                            continue
                        if any(value==p or (value==ROOT/folder or ROOT/folder in value.parents) for value in data['resolved_paths']):
                            consumers.append(str(q.relative_to(ROOT)))
                    code='\n'.join(data['text'] for q,data in owners)
                    # Expected render thumbnails require the original board asset
                    # versions too; retain these for a separate rebuild-aware pass.
                    if n=='expected-thumbnails.npy':
                        reason='Retain expected render thumbnails for historical visual comparisons'
                    elif consumers:
                        reason='Analysis/audio folder used by another build: '+' | '.join(consumers)
                    elif not owners or not any(k in code for k in ('np.save','tofile(','write_bytes(','f32le')):
                        reason='Array/audio generation recipe not established'
                    else:
                        deps=media_proof(folder,False)
                        if deps:
                            deps += [dict(kind='retained_file',**v.snapshot(q)) for q,data in owners]
                            proof='Derived audio cache; original video bytes and generation recipe retained'
                        else:
                            reason='Original audio source not verified'
            if proof and not reason:
                approved.append(dict(path=name,bytes=s.st_size,mtime_ns=s.st_mtime_ns,inode=s.st_ino,
                                     device=s.st_dev,proof=proof,dependencies=deps))
            else:
                held.append(dict(path=name,bytes=s.st_size,reason=reason or 'Incomplete verification'))
    needed={d['path'] for r in approved for d in r['dependencies']}
    final=[]
    for r in approved:
        if r['path'] in needed:
            held.append(dict(path=r['path'],bytes=r['bytes'],reason='Retained input for another approved cache'))
        else:
            final.append(r)
    print(f'Classified {len(final)} removable caches; checksumming the exact list...',flush=True)
    for r in final:
        actual=v.snapshot(ROOT/r['path'])
        assert all(actual[k]==r[k] for k in ('path','bytes','mtime_ns','inode','device'))
        r['sha256']=actual['sha256']
    result=dict(created_local=datetime.now(ZONE).isoformat(),files=final,deletion_performed=False)
    (OUT/'verified-deletions.json').write_text(json.dumps(result,indent=2)+'\n')
    save_csv('verified-deletions.csv',final,['path','bytes','sha256','proof'])
    save_csv('retained-evidence.csv',held,['path','bytes','reason'])
    summary=dict(verified_files=len(final),verified_gib=round(sum(r['bytes'] for r in final)/2**30,3),
                 by_extension={ext:dict(files=sum(Path(r['path']).suffix==ext for r in final),gib=round(sum(r['bytes'] for r in final if Path(r['path']).suffix==ext)/2**30,3)) for ext in sorted(IMAGE_EXT|ARRAY_EXT)},
                 retained_files=len(held),retained_gib=round(sum(r['bytes'] for r in held)/2**30,3),
                 retained_reasons=dict(Counter(r['reason'].split(':')[0] for r in held)),protected_videos=len(protected_videos))
    (OUT/'verification-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2),flush=True)


def delete():
    plan=json.loads((OUT/'verified-deletions.json').read_text())
    assert not plan['deletion_performed'] and not (OUT/'deletion-log.jsonl').exists()
    tracked=set(v.run('git','ls-files','-z').decode().split('\0'))
    deps={d['path']:d for r in plan['files'] for d in r['dependencies']}
    print('Checking the exact deletion list and retained source dependencies...',flush=True)
    for name,d in deps.items():
        assert v.sha(ROOT/name)==d['sha256'],f'Source changed: {name}'
    for r in plan['files']:
        p=ROOT/r['path']
        assert p.resolve()==p and p.is_relative_to(ROOT/'video-audit') and not p.is_symlink()
        assert p.suffix.lower() in IMAGE_EXT|ARRAY_EXT and r['path'] not in tracked
        assert v.snapshot(p)=={k:r[k] for k in ('path','bytes','mtime_ns','inode','device','sha256')}
    protected=json.loads((OUT/'protected-videos-before.json').read_text())
    video_stats={r['path']:((ROOT/r['path']).stat().st_size,(ROOT/r['path']).stat().st_mtime_ns,(ROOT/r['path']).stat().st_ino) for r in protected}
    # All video extensions are outside the allowlist. Record active updates
    # separately; other course edits can continue during this cleanup.
    fs=os.statvfs(ROOT);before=fs.f_bavail*fs.f_frsize
    deleted=[]
    print(f"Removing {len(plan['files'])} verified review caches...",flush=True)
    with (OUT/'deletion-log.jsonl').open('x') as log:
        for r in plan['files']:
            p=ROOT/r['path'];s=p.lstat()
            assert (s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev)==(r['bytes'],r['mtime_ns'],r['inode'],r['device'])
            p.unlink()
            event={k:r[k] for k in ('path','bytes','sha256')};event['deleted_local']=datetime.now(ZONE).isoformat()
            log.write(json.dumps(event)+'\n');log.flush();deleted.append(event)
    changed=[]
    for name,old in video_stats.items():
        p=ROOT/name;assert p.is_file(),f'Video missing: {name}'
        s=p.stat()
        if (s.st_size,s.st_mtime_ns,s.st_ino)!=old:
            changed.append(name)
    assert all(not (ROOT/r['path']).exists() for r in deleted)
    assert all((ROOT/name).is_file() for name in deps)
    fs=os.statvfs(ROOT);after=fs.f_bavail*fs.f_frsize
    receipt=dict(completed_local=datetime.now(ZONE).isoformat(),deleted_files=len(deleted),
                 deleted_logical_gib=round(sum(r['bytes'] for r in deleted)/2**30,3),
                 measured_free_space_change_gib=round((after-before)/2**30,3),free_gib_after=round(after/2**30,3),
                 all_videos_retained=True,protected_videos=len(protected),concurrent_video_updates=changed,
                 deleted_extensions=dict(Counter(Path(r['path']).suffix for r in deleted)))
    plan['deletion_performed']=True
    (OUT/'verified-deletions.json').write_text(json.dumps(plan,indent=2)+'\n')
    (OUT/'deletion-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--delete',action='store_true');args=parser.parse_args()
    delete() if args.delete else plan()

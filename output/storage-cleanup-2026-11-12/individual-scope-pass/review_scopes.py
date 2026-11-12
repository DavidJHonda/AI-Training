"""Review specific superseded audit scopes; delete only a checksummed allowlist.

No video, audio master, artwork, manifest, code, or Git object can be deleted.
Migration inventories describe historical outputs; real source/spec reads still
protect files. Notes, reconstruction promises, and compact review sheets remain.
"""
from pathlib import Path
from collections import defaultdict,Counter
from datetime import datetime,date
from zoneinfo import ZoneInfo
import ast,csv,hashlib,importlib.util,json,os,re,subprocess,sys
sys.dont_write_bytecode=True
ROOT=Path('/Users/davidobrien/Developer/AI-Training')
OUT=Path(__file__).resolve().parent
OLD=ROOT/'output/storage-cleanup-2026-11-11'
spec=importlib.util.spec_from_file_location('helpers',OLD/'verify_and_clean_scratch.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
SCOPES={
 'flattery-engagement-feedback-comparison-2026-09-21':('flattery-trap',6),
 'why-answers-vary-build-2026-09-28-v13':('why-answers-vary',13),
 'how-ai-answers-guided-2026-10-06-v12':('how-ai-answers',12),
 'tokens-build-2026-10-04-v12':('tokens',12),
 'layers-repair-2026-09-28-v7':('layers',7),
 'transformer-repair-2026-09-27-v11':('transformer',11),
 'does-ai-think-combined-v12-2026-10-24':('does-ai-think',12),
 'pace-of-change-build-2026-11-03-v11':('pace-of-change',11),
 'your-home-base-zoom-cut-2026-09-29-v8':('your-home-base',8),
}
def run(*args):return subprocess.check_output(args,cwd=ROOT)
def snap(p):return v.snapshot(p)
def recent(p):
 dates=re.findall(r'20\d\d-\d\d-\d\d',str(p))
 return (dates and max(dates)>='2026-11-04') or datetime.fromtimestamp(p.stat().st_mtime,ZoneInfo('America/Chicago')).date()>=date(2026,11,4)
def state():
 result={}
 for base,dirs,files in os.walk(ROOT):
  dirs[:]=[d for d in dirs if d!='.git' and not (Path(base)/d).is_relative_to(OUT)]
  for n in files:
   p=Path(base)/n
   if p.is_relative_to(OUT):continue
   s=p.lstat();record=[s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev]
   if p.is_symlink():record.append(os.readlink(p))
   result[v.rel(p)]=record
 return result
def git_state():
 return dict(refs=run('git','for-each-ref','--format=%(refname) %(objectname)').decode(),
             controls={n:v.sha(ROOT/'.git'/n) for n in ('HEAD','index','shallow','config','packed-refs') if (ROOT/'.git'/n).is_file()})
def plan():
 assert not (OUT/'scope-deletion-receipt.json').exists()
 tracked=set(run('git','ls-files','-z').decode().split('\0'))
 catalog=json.loads((ROOT/'output/storage-cleanup-2026-11-12/selective-evidence-pass/videos-before.json').read_text())
 byhash=defaultdict(list)
 for a in catalog:byhash[a['sha256']].append(a)
 releases={};dependencies={}
 runtime=(ROOT/'index.html').read_text().split('const LESSON_VIDEOS = {',1)[1].split('\n};',1)[0]
 for scope,(family,old_version) in SCOPES.items():
  canonical=ROOT/f'course-assets/{family}/{family}.mp4'
  assert v.rel(canonical) in runtime
  identity=snap(canonical);matches=[]
  for a in byhash[identity['sha256']]:
   p=ROOT/a['path'];m=re.fullmatch(re.escape(family)+r'-v(\d+)\.mp4',p.name)
   if p.parent==ROOT/'Prompts' and m and p.is_file() and v.sha(p)==identity['sha256']:matches.append((int(m[1]),p))
  assert matches and max(x[0] for x in matches)>old_version,(scope,'No verified successor')
  releases[scope]=dict(canonical=identity,matched_edit=snap(max(matches)[1]),installed_version=max(x[0] for x in matches),old_version=old_version)
  dependencies[identity['path']]=identity
  dependencies[releases[scope]['matched_edit']['path']]=releases[scope]['matched_edit']
 # Preserve every promised reconstruction input and keeper from earlier cleanup.
 protected=set();reasons=defaultdict(set)
 def protect(p,why):
  p=Path(os.path.normpath(str(p)))
  if p.is_relative_to(ROOT/'video-audit'):protected.add(p);reasons[p].add(why)
 for p in (ROOT/'output').glob('storage-cleanup-*/**/verified-deletions.json'):
  for row in json.loads(p.read_text()).get('files',[]):
   for d in row.get('dependencies',[]):
    if d.get('kind','retained_file')=='retained_file' and 'path' in d:protect(ROOT/d['path'],'Previous retained reconstruction dependency')
 # Real specifications and reports protect explicit inputs. Migration receipts
 # are historical listings, not image recipes; retain the receipts themselves.
 ignored_inventories=[]
 for base,dirs,names in os.walk(ROOT):
  dirs[:]=[d for d in dirs if d not in {'.git','.video-venv','node_modules','output','tmp','.superpowers'}]
  for name in names:
   p=Path(base)/name
   if p.is_symlink() or p.suffix.lower() not in {'.json','.md','.html','.txt'}:continue
   if p.suffix=='.json' and ('migration' in name.lower() or name=='inventory.json'):
    ignored_inventories.append(v.rel(p));continue
   if p.stat().st_size>20*2**20:continue
   text=p.read_text(errors='replace')
   if p.suffix=='.json':
    try:obj=json.loads(text)
    except ValueError:continue
    def walk(value):
     if isinstance(value,str) and value.lower().endswith(('.jpg','.jpeg','.png')) and '\n' not in value:
      for q in (v.local(value),p.parent/value):protect(q,'Explicit image in '+v.rel(p))
     elif isinstance(value,dict):
      for k,val in value.items():walk(k);walk(val)
     elif isinstance(value,list):
      for val in value:walk(val)
    walk(obj)
   else:
    for target in re.findall(r'''(?:!?\[[^\]]*\]\(|(?:src|href)=["'])([^\s)"']+\.(?:jpg|jpeg|png))''',text,re.I):
     if '://' not in target:protect(p.parent/target,'Linked written evidence')
    for target in re.findall(r'''video-audit/[^\s"'`<>)(\]}]{1,360}\.(?:jpg|jpeg|png)(?![\w.])''',text,re.I):protect(ROOT/target,'Named image in written record')
    for target in set(re.findall(r'(?<![\w.-])[\w.-]+\.(?:jpg|jpeg|png)(?![\w.])',text,re.I)):
     if (p.parent/target).is_file():protect(p.parent/target,'Named adjacent image in written record')
 # Static read/glob prefixes protect dynamically named renderer inputs.
 rules=[];code_names=set();scripts=v.scan_scripts()
 for script,data in scripts.items():
  code_names.update(re.findall(r'(?<![\w.-])([\w.-]+\.(?:jpg|jpeg|png))(?![\w.])',data['text'],re.I))
  for node in ast.walk(data['tree']):
   if not isinstance(node,ast.Call):continue
   fn=getattr(node.func,'attr',getattr(node.func,'id',''))
   if fn not in {'imread','open','glob','rglob','load','fromfile','read_bytes','read_text'}:continue
   if fn=='open' and len(node.args)>1 and isinstance(node.args[1],ast.Constant) and any(c in str(node.args[1].value) for c in 'wa+'):continue
   args=node.args if fn not in {'glob','rglob','read_bytes','read_text'} else [node.func.value]
   if fn in {'glob','rglob'} and node.args and isinstance(node.args[0],ast.Constant):
    pattern=node.args[0].value
    if isinstance(pattern,str) and Path(pattern).suffix and Path(pattern).suffix.lower() not in {'.jpg','.jpeg','.png'}:continue
   paths=[]
   for arg in args:
    for expr in ast.walk(arg):
     try:
      val=v.evaluate(expr,data['env'])
      if isinstance(val,Path) and val.is_relative_to(ROOT/'video-audit'):paths.append(val)
     except (ValueError,KeyError,TypeError,IndexError,AttributeError):pass
   if paths:
    prefix=max(paths,key=lambda q:len(q.parts))
    # Manually reviewed: the font-sync readers use CONFIG[item]['spec'] JSON
    # paths, not arbitrary images. The cleaner enumerates deletion patterns.
    # A partially resolved ROOT/video-audit must not mean every JPG is input.
    if prefix==ROOT/'video-audit' and script.name in {'build_board_font_sync.py','build_board_font_sync_round2.py','clean_video_audit.py'}:continue
    rules.append((prefix,v.rel(script)))
 candidates=[];held=[];summaries=[]
 for scope in SCOPES:
  folder=ROOT/'video-audit'/scope
  images=[p for p in folder.rglob('*.jpg') if p.is_file() and not p.is_symlink()]
  # Retain all aggregate/contact sheets and first/last capture per output directory.
  dirs=defaultdict(list)
  for p in images:dirs[p.parent].append(p)
  sentinels=set()
  for owner,peers in dirs.items():
   peers=sorted(peers);sentinels.update([peers[0],peers[-1]])
  summaries.extend(v.rel(p) for p in sentinels)
  for p in images:
   rel=p.relative_to(folder);why=''
   generated=(any(x in {'preview','encoded','states','return-check'} for x in rel.parts[:-1]) or bool(re.fullmatch(r'state-.+\.jpg',p.name)))
   if not generated:why='Not a selected generated individual capture'
   elif v.rel(p) in tracked:why='Tracked record'
   elif recent(p):why='Recent work'
   elif p.stat().st_nlink>1:why='Hardlinked copy retained'
   elif re.search(r'donor|source|canvas|mask|patch|prepared|original|close|reference|approved',str(rel),re.I):why='Named source/artwork/reconstruction material'
   elif re.search(r'sheet|overview|contact|summary|states-',p.name,re.I) or p in sentinels:why='Compact visual summary/sentinel retained'
   elif p in protected:why='; '.join(sorted(reasons[p]))
   elif p.name in code_names:why='Image filename explicitly mentioned by code'
   else:
    readers=[s for prefix,s in rules if prefix in (p,*p.parents)]
    if readers:why='Static image read/glob: '+'; '.join(sorted(set(readers)))
   if why:held.append(dict(path=v.rel(p),bytes=p.stat().st_size,reason=why))
   else:candidates.append(dict(**snap(p),scope=scope,reason='Untracked superseded generated individual QA capture; source/spec inputs and compact summaries retained'))
 for scope in SCOPES:
  for p in (ROOT/'video-audit'/scope).rglob('*'):
   if p.is_file() and p.suffix in {'.json','.md','.txt','.py'} and 'migration' not in p.name:dependencies[v.rel(p)]=snap(p)
 result=dict(deletion_performed=False,files=candidates,dependencies=list(dependencies.values()),releases=releases,
             ignored_historical_inventory_records=ignored_inventories,retained_visual_sentinels=sorted(set(summaries)))
 (OUT/'scope-plan.json').write_text(json.dumps(result,indent=2)+'\n')
 with (OUT/'scope-retained.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['path','bytes','reason']);w.writeheader();w.writerows(held)
 (OUT/'worktree-before.json').write_text(json.dumps(state())+'\n')
 (OUT/'git-before.json').write_text(json.dumps(git_state(),indent=2)+'\n')
 summary=dict(verified_files=len(candidates),verified_mib=round(sum(a['bytes'] for a in candidates)/2**20,3),
              by_scope={s:dict(files=sum(a['scope']==s for a in candidates),mib=round(sum(a['bytes'] for a in candidates if a['scope']==s)/2**20,3),installed_version=releases[s]['installed_version']) for s in SCOPES},
              retained_images=len(held),retained_reasons=dict(Counter(a['reason'].split(';')[0] for a in held)))
 (OUT/'scope-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)
def delete():
 plan=json.loads((OUT/'scope-plan.json').read_text());assert not plan['deletion_performed'] and not (OUT/'scope-deletion-receipt.json').exists()
 tracked=set(run('git','ls-files','-z').decode().split('\0'));before=json.loads((OUT/'worktree-before.json').read_text());gs=json.loads((OUT/'git-before.json').read_text());events=[]
 for d in plan['dependencies']:assert v.sha(ROOT/d['path'])==d['sha256'],d['path']
 for a in plan['files']:
  p=ROOT/a['path'];assert p.resolve()==p and not p.is_symlink() and p.suffix=='.jpg' and a['path'] not in tracked and not recent(p)
  assert snap(p)=={k:a[k] for k in ('path','bytes','mtime_ns','inode','device','sha256')}
 current=state();assert all(current.get(a['path'])==before[a['path']] for a in plan['files'])
 with (OUT/'scope-deletion-log.jsonl').open('x') as log:
  for a in plan['files']:
   (ROOT/a['path']).unlink();log.write(json.dumps(a)+'\n');log.flush();events.append(a)
 for d in plan['dependencies']:assert v.sha(ROOT/d['path'])==d['sha256'],d['path']
 after=state();deleted={a['path'] for a in events};unexpected_removed=sorted(set(before)-set(after)-deleted);assert not unexpected_removed
 changes=sorted(p for p in before if p in after and before[p]!=after[p])
 videos=[p for p in before if Path(p).suffix.lower() in {'.mp4','.mov','.mkv'}]
 assert all(after.get(p)==before[p] for p in videos),'A retained video changed'
 end=git_state();assert end['controls']==gs['controls'],'Git control files changed'
 normal=lambda s:dict(line.split() for line in s.splitlines() if not line.startswith('refs/codex/turn-diffs/'))
 assert normal(end['refs'])==normal(gs['refs']),'Permanent Git refs changed'
 result=dict(deleted_files=len(events),deleted_mib=round(sum(a['bytes'] for a in events)/2**20,3),retained_videos_unchanged=len(videos),
             retained_dependency_files_rechecked=len(plan['dependencies']),unexpected_removed_files=unexpected_removed,
             concurrent_worktree_updates=changes,permanent_git_refs_and_controls_unchanged=True,by_scope=dict(Counter(a['scope'] for a in events)))
 plan['deletion_performed']=True;(OUT/'scope-plan.json').write_text(json.dumps(plan,indent=2)+'\n');(OUT/'scope-deletion-receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
 delete() if '--delete' in sys.argv else plan()

"""Check the 116 age-flagged donors, then remove only dependency-free files.

Keeps tracked videos, reconstruction promises, source/parent references by path
and hash, code inputs, recent copies, and specific possible future-use passages.
No Git mutations or build modules are executed. Default saves a reviewed plan.
"""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from collections import defaultdict,Counter
import hashlib,importlib.util,json,os,re,subprocess,sys
sys.dont_write_bytecode=True
ROOT=Path('/Users/davidobrien/Developer/AI-Training')
BASE=Path(__file__).resolve().parent
OUT=BASE/'eligible-cleanup-pass';OUT.mkdir(exist_ok=True)
OLD=ROOT/'output/storage-cleanup-2026-11-11'
spec=importlib.util.spec_from_file_location('scratch_helpers',OLD/'verify_and_clean_scratch.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
CUTOFF=datetime(2026,10,13,tzinfo=ZoneInfo('America/Chicago')).timestamp()
SOURCE_KEYS={'source','sources','source_files','source_hashes','source_video','source_path','source_snapshot',
 'donor','donors','donor_files','donor_file','donor_rolls','graft_source','graft_audio','video_src','visual_donor',
 'audio_source','picture_source','parent','parent_candidate','base','base_source','original','original_source',
 'reference','snapshot','protected','protected_hashes','input','inputs','lossless_audio_source'}
TEXT_EXT={'.json','.py','.js','.cjs','.mjs','.sh','.swift','.md','.txt','.html','.csv'}
CODE_EXT={'.py','.js','.cjs','.mjs','.sh','.swift'}
def run(*args):return subprocess.check_output(args,cwd=ROOT)
def reference_files():
 found={}
 for base,dirs,names in os.walk(ROOT):
  dirs[:]=[d for d in dirs if d not in {'.git','.video-venv','node_modules','output','.aws','.codex','.agents'} and not (Path(base)/d).is_symlink()]
  for name in names:
   p=Path(base)/name
   if not p.is_symlink() and p.suffix.lower() in TEXT_EXT:
    s=p.stat()
    if s.st_size<=20*2**20:found[v.rel(p)]=[s.st_size,s.st_mtime_ns,s.st_ino]
 return found
def worktree():
 found={}
 for base,dirs,names in os.walk(ROOT):
  dirs[:]=[d for d in dirs if d!='.git' and not (Path(base)/d).is_relative_to(OUT)]
  for name in names:
   p=Path(base)/name
   if p.is_relative_to(OUT):continue
   s=p.lstat();record=[s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev]
   if p.is_symlink():record.append(os.readlink(p))
   found[v.rel(p)]=record
 return found
def git_state():
 ids=set()
 for idx in (ROOT/'.git/objects/pack').glob('*.idx'):
  with idx.open('rb') as f:
   result=subprocess.check_output(['git','show-index'],cwd=ROOT,stdin=f,text=True)
  ids.update(line.split()[1] for line in result.splitlines())
 for d in (ROOT/'.git/objects').iterdir():
  if d.is_dir() and len(d.name)==2:
   ids.update(d.name+p.name for p in d.iterdir() if p.is_file() and re.fullmatch('[0-9a-f]{38}',p.name))
 return dict(object_ids=sorted(ids),refs=run('git','for-each-ref','--format=%(refname) %(objectname)').decode(),
  controls={n:v.sha(ROOT/'.git'/n) for n in ('HEAD','index','shallow','config','packed-refs') if (ROOT/'.git'/n).is_file()},
  reflogs={v.rel(p):dict(bytes=p.stat().st_size,sha256=v.sha(p)) for p in (ROOT/'.git/logs').rglob('*') if p.is_file()})
def plan():
 assert not (OUT/'deletion-receipt.json').exists()
 tracked=set(run('git','ls-files','-z').decode().split('\0'))
 old_refs=json.loads((OLD/'edited-video-pass/protected-source-references.json').read_text())
 flagged=[a for a in json.loads((BASE/'date-inventory.json').read_text())['videos'] if a['modified_before_30_day_cutoff']]
 rows=[];reasons=defaultdict(list);by_name={};by_hash=defaultdict(list)
 def keep(name,kind,evidence):
  item=dict(kind=kind,evidence=evidence)
  if item not in reasons[name]:reasons[name].append(item)
 for a in flagged:
  p=ROOT/a['path'];s=p.lstat();row=v.snapshot(p);rows.append(row);by_name[p.name]=a['path'];by_hash[row['sha256']].append(a['path'])
  if a['path'] in tracked:keep(a['path'],'Tracked file','Keep working copies of tracked source videos; Git history unchanged')
  if s.st_mtime>=CUTOFF or s.st_birthtime>=CUTOFF:keep(a['path'],'Recent file/copy','Current modification or birth time is within 30 days')
  if p.is_symlink() or s.st_nlink>1:keep(a['path'],'Linked source','Symlink or hardlinked source retained')
  # Carry forward established technical roles, excluding the old blanket policy
  # that every raw donor must be kept regardless of use.
  for why in old_refs.get(a['path'],[]):
   if why.startswith(('Source/parent metadata:','Video input/reference in code:','Retained reconstruction source','Source reservation/runtime reference:','Source reservation in notes:')):
    keep(a['path'],'Established source/reconstruction/reservation role',why)
 promises=[]
 for p in (ROOT/'output').glob('storage-cleanup-*/**/verified-deletions.json'):
  for row in json.loads(p.read_text()).get('files',[]):
   for d in row.get('dependencies',[]):
    if d.get('kind','retained_file')=='retained_file' and d.get('path') in {a['path'] for a in rows}:
     keep(d['path'],'Required reconstruction input','Previous cleanup retained this exact input: '+v.rel(p));promises.append(v.snapshot(p));break
 refs_before=reference_files();source_records=0;code_records=0;ordinary_mentions=defaultdict(list)
 for rel,record in refs_before.items():
  p=ROOT/rel;text=p.read_text(errors='replace');ext=p.suffix.lower()
  hits=[(base,name) for base,name in by_name.items() if base in text or name in text]
  if ext in CODE_EXT:
   code_records+=1
   # References in migration/rename tools are catalogs, not build input reads.
   if not re.search(r'migrat|rename|clean_video_audit',p.name,re.I):
    for base,name in hits:keep(name,'Current code reference',rel)
  elif ext=='.json' and not re.search(r'migrat|inventory',p.name,re.I):
   try:obj=json.loads(text)
   except ValueError:continue
   source_records+=1
   def gather(value,context):
    if isinstance(value,str):
     for base,name in by_name.items():
      if base in value or name in value:keep(name,'Source/input metadata',rel+' '+context)
     if re.fullmatch('[0-9a-f]{64}',value):
      for name in by_hash.get(value,[]):keep(name,'Source/input hash identity',rel+' '+context)
    elif isinstance(value,dict):
     for k,val in value.items():gather(k,context);gather(val,context)
    elif isinstance(value,list):
     for val in value:gather(val,context)
   def walk(value,context=''):
    if isinstance(value,dict):
     for key,val in value.items():
      if key.lower() in SOURCE_KEYS or key.lower().startswith(('donor_','source_file','input_')):gather(val,context+'/'+key)
      else:walk(val,context+'/'+key)
    elif isinstance(value,list):
     for i,val in enumerate(value):walk(val,context+'/'+str(i))
   walk(obj)
  for base,name in hits:
   if ext in {'.md','.txt','.csv','.html'}:ordinary_mentions[name].append(rel)
 # The two unused-roll graphics reviews contain specific named possible future
 # cutaways. Retain these uncertain options rather than infer their cancellation.
 manual_reservations={
  'Prompts/what-is-ai-2.mp4':('video-audit/what-is-ai-donor-graphics-2026-09-26/REVIEW.md','R2 Home Theater / Workstation, right half only'),
  'Prompts/people-skills-2.mp4':('video-audit/people-skills-engagement-2026-09-26/REVIEW.md','Optional, not planned: a cutaway'),
 }
 evidence=[]
 for name,(rel,needle) in manual_reservations.items():
  assert needle in (ROOT/rel).read_text();keep(name,'Specific possible future-use passage retained conservatively',rel+' — '+needle);evidence.append(v.snapshot(ROOT/rel))
 # Manually reviewed the process-roll comparison and every Evaluation Matters
 # producer. The old v8 implementation uses rolls 1–4; current v10–v12 use
 # rolls 1–3 plus the pinned installed donor. No producer reads rolls 5 or 6.
 # The October 23 prep supersedes the September process-roll donor suggestions.
 manual_evidence=[
  'video-audit/evaluation-matters-process-rolls-2026-09-27/process-board-comparison.csv',
  'scripts/video/kits/WORK-WITH-AI-VIDEO-KITS.md','gemini-notebook/evaluation-matters/DONOR.json',
  *[v.rel(p) for p in (ROOT/'scripts/video').glob('build_evaluation_matters*.py')],
 ]
 evidence.extend(v.snapshot(ROOT/rel) for rel in manual_evidence)
 assert refs_before==reference_files(),'Reference files changed during review; re-run the plan'
 eligible=[dict(a,reason='Older than 30 days; no source/input code or metadata reference by filename or SHA-256, prior reconstruction promise, or current future-use reservation found') for a in rows if not reasons[a['path']]]
 # Final scope-specific review is intentionally narrow: unknown additional
 # candidates must be reviewed rather than accidentally admitted by a parser.
 assert {a['path'] for a in eligible}<={'Prompts/evaluation-matters-5.mp4','Prompts/evaluation-matters-6.mp4'},'Additional candidate requires manual review'
 result=dict(deletion_performed=False,cutoff='2026-10-13',reviewed=rows,files=eligible,
  retained=[dict(path=a['path'],bytes=a['bytes'],reasons=reasons[a['path']]) for a in rows if reasons[a['path']]],
  ordinary_review_mentions=dict(ordinary_mentions),source_records_checked=source_records,code_records_checked=code_records,
  manual_evidence=evidence,reconstruction_promise_records=promises)
 (OUT/'plan.json').write_text(json.dumps(result,indent=2)+'\n');(OUT/'reference-state.json').write_text(json.dumps(refs_before)+'\n')
 summary=dict(reviewed_donors=len(rows),verified_deletions=len(eligible),verified_mib=round(sum(a['bytes'] for a in eligible)/2**20,3),
  retained_donors=len(rows)-len(eligible),retained_reason_counts=dict(Counter(x['kind'] for a in result['retained'] for x in a['reasons'])),
  source_records_checked=source_records,code_records_checked=code_records,candidate_paths=[a['path'] for a in eligible])
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2),flush=True)
def delete():
 p=json.loads((OUT/'plan.json').read_text());assert not p['deletion_performed'] and not (OUT/'deletion-receipt.json').exists()
 assert reference_files()==json.loads((OUT/'reference-state.json').read_text()),'References changed: re-run review'
 for d in p['manual_evidence']+p['reconstruction_promise_records']:assert v.sha(ROOT/d['path'])==d['sha256'],d['path']
 tracked=set(run('git','ls-files','-z').decode().split('\0'))
 for a in p['files']:
  q=ROOT/a['path'];s=q.lstat();assert q.resolve()==q and not q.is_symlink() and q.is_relative_to(ROOT/'Prompts') and s.st_nlink==1
  assert a['path'] not in tracked and s.st_mtime<CUTOFF and s.st_birthtime<CUTOFF
  assert v.snapshot(q)=={k:a[k] for k in ('path','bytes','mtime_ns','inode','device','sha256')}
 before=worktree();gs=git_state();assert reference_files()==json.loads((OUT/'reference-state.json').read_text()),'References changed before deletion'
 (OUT/'worktree-before.json').write_text(json.dumps(before)+'\n');(OUT/'git-before.json').write_text(json.dumps(gs)+'\n')
 events=[]
 with (OUT/'deletion-log.jsonl').open('x') as log:
  for a in p['files']:
   q=ROOT/a['path'];assert v.snapshot(q)=={k:a[k] for k in ('path','bytes','mtime_ns','inode','device','sha256')}
   q.unlink();events.append(a);log.write(json.dumps(a)+'\n');log.flush()
 after=worktree();deleted={a['path'] for a in events};missing=set(before)-set(after)-deleted;assert not missing,missing
 changed=[n for n in before if n in after and before[n]!=after[n]]
 remaining_video=[n for n in before if Path(n).suffix.lower() in {'.mp4','.mov','.mkv'} and n not in deleted]
 assert all(n in after for n in remaining_video)
 for d in p['manual_evidence']+p['reconstruction_promise_records']:assert v.sha(ROOT/d['path'])==d['sha256'],d['path']
 end=git_state();assert set(gs['object_ids'])<=set(end['object_ids']),'An original Git object is absent'
 normal=lambda s:dict(line.split() for line in s.splitlines() if not line.startswith('refs/codex/turn-diffs/'))
 assert gs['controls']==end['controls'] and normal(gs['refs'])==normal(end['refs']),'Git control files or permanent refs changed'
 for name,old in gs['reflogs'].items():
  data=(ROOT/name).read_bytes();assert len(data)>=old['bytes'] and hashlib.sha256(data[:old['bytes']]).hexdigest()==old['sha256']
 check=subprocess.run(['git','fsck','--connectivity-only','--no-dangling'],cwd=ROOT,capture_output=True,text=True)
 (OUT/'git-connectivity.log').write_text(check.stdout+check.stderr)
 receipt=dict(reviewed_older_donors=len(p['reviewed']),deleted_files=len(events),deleted_mib=round(sum(a['bytes'] for a in events)/2**20,3),deleted_paths=sorted(deleted),
  retained_older_donors=len(p['retained']),retained_videos_present=len(remaining_video),retained_videos_unchanged=sum(before[n]==after[n] for n in remaining_video),
  concurrent_worktree_updates=changed,unexpected_removed_files=sorted(missing),original_git_objects_retained=len(gs['object_ids']),
  permanent_refs_and_git_controls_unchanged=True,reflog_history_preserved=True,git_connectivity_exit_code=check.returncode,git_history_rewritten=False)
 p['deletion_performed']=True;(OUT/'plan.json').write_text(json.dumps(p,indent=2)+'\n');(OUT/'deletion-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2),flush=True)
 assert check.returncode==0,'Inspect Git connectivity log'
if __name__=='__main__':delete() if '--delete' in sys.argv else plan()

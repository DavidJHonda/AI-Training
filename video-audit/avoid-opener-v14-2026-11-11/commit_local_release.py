from pathlib import Path
import hashlib,json,re,subprocess
root=Path.cwd(); audit=root/'video-audit/avoid-opener-v14-2026-11-11'
record=json.loads((audit/'local-install.json').read_text())
run=lambda *args,**kw:subprocess.run(args,cwd=root,check=True,**kw)
head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
assert head==(audit/'release-head.txt').read_text().strip(),'HEAD changed; regenerate the release patch before staging.'
assert subprocess.run(['git','diff','--cached','--quiet'],cwd=root).returncode==0,'Existing staged work must remain untouched.'
patch=str(audit/'release-only.patch')
run('git','apply','--cached','--check',patch)
run('git','apply','--cached',patch)
asset='course-assets/avoid-traps-opener/avoid-traps-opener.mp4'
run('git','add','--',asset)
expected={asset,'index.html','course-assets/manifest.json'}
staged=set(subprocess.check_output(['git','diff','--cached','--name-only'],text=True).splitlines())
assert staged==expected,(staged,expected)
before=subprocess.check_output(['git','show',head+':index.html'],text=True)
after=subprocess.check_output(['git','show',':index.html'],text=True)
assert after==before.replace(record['old_line']+'\n',record['new_line']+'\n')
before_manifest=json.loads(subprocess.check_output(['git','show',head+':course-assets/manifest.json'],text=True))
after_manifest=json.loads(subprocess.check_output(['git','show',':course-assets/manifest.json'],text=True))
row=next(x for x in before_manifest['video_assets'] if x['new']==asset)
row.update(sha256=record['sha256'],bytes=record['bytes'],approved_candidate_version=14)
assert before_manifest==after_manifest,'Unexpected manifest changes were staged.'
assert hashlib.sha256(subprocess.check_output(['git','show',':'+asset])).hexdigest()==record['sha256']
run('git','diff','--cached','--check')
result=run('git','commit','-m','Ship Avoid Traps opener v14 locally',capture_output=True,text=True)
print(result.stdout.strip())
match=re.search(r'^\[[^\n]+ ([0-9a-f]{7,40})\]',result.stdout,re.M);assert match,result.stdout
commit=subprocess.check_output(['git','rev-parse',match.group(1)],text=True).strip()
files=set(subprocess.check_output(['git','diff-tree','--no-commit-id','--name-only','-r',commit],text=True).splitlines());assert files==expected,files
assert hashlib.sha256(subprocess.check_output(['git','show',commit+':'+asset])).hexdigest()==record['sha256']
record.update(local_commit=commit,committed_files=sorted(files),publication_status='Shipped locally; queued for batch deployment',course_assets_migration_hash_verification='PASS',agent_direct_listening=False,user_review_approval=True)
(audit/'local-install.json').write_text(json.dumps(record,indent=2)+'\n')
print('Verified local commit',commit)

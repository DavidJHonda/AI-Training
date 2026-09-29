from pathlib import Path
import subprocess,hashlib,json
out=Path(__file__).parent
paths=['course-assets/how-ai-answers/how-ai-answers.mp4','course-assets/manifest.json','index.html']
def git(*args):return subprocess.check_output(['git',*args])
assert not git('diff','--cached','--name-only'),'Other staged work appeared; stop without modifying it'
assert git('diff','--','index.html','course-assets/manifest.json')==out.joinpath('release-text.patch').read_bytes(),'Shared release files changed; inspect before committing'
assert hashlib.sha256(Path(paths[0]).read_bytes()).hexdigest()=='e38783730880f2a64d578670a8715e1a2c7b05881e2dc19fd3b27273ff286ce4'
subprocess.run(['git','add','--',*paths],check=True)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(paths)
assert git('diff','--cached','--','index.html','course-assets/manifest.json')==out.joinpath('release-text.patch').read_bytes()
subprocess.run(['git','commit','-m','Ship approved How AI Answers v11 locally'],check=True)
commit=git('rev-parse','HEAD').decode().strip()
assert set(git('diff-tree','--no-commit-id','--name-only','-r',commit).decode().splitlines())==set(paths)
assert hashlib.sha256(git('show',commit+':'+paths[0])).hexdigest()=='e38783730880f2a64d578670a8715e1a2c7b05881e2dc19fd3b27273ff286ce4'
r=json.loads(out.joinpath('shipping-receipt.json').read_text());r.update(commit=commit,status='shipped locally; queued for batch deployment')
out.joinpath('shipping-receipt.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))

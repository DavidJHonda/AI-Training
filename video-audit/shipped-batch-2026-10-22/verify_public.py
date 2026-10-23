from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,re,hashlib,urllib.request,datetime,subprocess
ROOT=Path.cwd();OUT=ROOT/'video-audit/shipped-batch-2026-10-22';BASE='https://besmarterthanthetool.com/'
ids=['openerrealworld','whatpeoplesay','llms','whydeeper','choosemodel','whybother','modelselection']
local=(ROOT/'index.html').read_text();rows=[]
for key in ids:
 m=re.search(r'^  '+key+r': \{ src: "([^"]+)", duration: "([^"]+)"',local,re.M);assert m,key
 rows.append(dict(id=key,src=m[1],runtime=m[2]))
req=urllib.request.Request(BASE+'index.html?release=1a7b15d1',headers={'Cache-Control':'no-cache'})
with urllib.request.urlopen(req,timeout=30) as r:public=r.read().decode();pageurl=r.url
report=dict(checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),page_url=pageurl,index_matches=public==local,references=[],assets=[])
for row in rows:
 m=re.search(r'^  '+row['id']+r': \{ src: "([^"]+)", duration: "([^"]+)"',public,re.M)
 row['matches']=bool(m and m[1]==row['src'] and m[2]==row['runtime']);report['references'].append(row)
if not all(row['matches'] for row in rows):
 report['status']='deployment pending: public references differ';(OUT/'public-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));raise SystemExit(2)
assets=[r['src'] for r in rows]+['course-assets/loudest-voices/loudest-voices-experts.jpg?v=20261022twoexperts']
def verify(src):
 localpath=ROOT/src.split('?')[0];expected=hashlib.sha256(localpath.read_bytes()).hexdigest();h=hashlib.sha256();size=0
 with urllib.request.urlopen(BASE+src,timeout=45) as r:
  status=r.status
  while True:
   block=r.read(1024*1024)
   if not block:break
   size+=len(block);h.update(block)
 result=dict(src=src,status=status,bytes=size,sha256=h.hexdigest(),expected_sha256=expected,matches=h.hexdigest()==expected)
 print(src,result['matches'],size,flush=True);return result
with ThreadPoolExecutor(max_workers=3) as pool:report['assets']=list(pool.map(verify,assets))
report['status']='verified live' if report['index_matches'] and all(x['matches'] for x in report['assets']) else 'verification mismatch'
(OUT/'public-verification.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],flush=True)
assert report['status']=='verified live'

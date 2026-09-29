from pathlib import Path
import urllib.request,hashlib,json,re,datetime
base='https://besmarterthanthetool.com/'
out=Path(__file__).parent
page=urllib.request.urlopen(base,timeout=30).read().decode()
line=re.search(r'faketrap:\s*\{ src: "([^"]+\.mp4[^\"]*)"[^\n]+',page).group(0)
ref=re.search(r'src: "([^"]+)"',line).group(1)
def section(s): return s.split('function SyntheticMediaSection(props)',1)[1].split('// ── The Final',1)[0]
(out/'public-lesson-source.txt').write_text(section(page))
refs=[ref]+list(dict.fromkeys(re.findall(r'course-assets/fake-trap/[^"\s]+\.jpg(?:\?[^"\s]*)?',page)))
rows=[]
for ref in refs:
 h=hashlib.sha256(); n=0
 with urllib.request.urlopen(base+ref,timeout=40) as r:
  while True:
   data=r.read(1024*1024)
   if not data: break
   h.update(data); n+=len(data)
 p=Path(ref.split('?')[0]); local=hashlib.sha256(p.read_bytes()).hexdigest()
 rows.append(dict(url=base+ref,bytes=n,sha256=h.hexdigest(),local_sha256=local,match=h.hexdigest()==local))
result=dict(checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),page_reference=line,assets=rows,lesson_section_matches_local=section(page)==section(Path('index.html').read_text()))
(out/'public-verification.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))

import urllib.request,hashlib,json,re,pathlib
out=pathlib.Path(__file__).parent
base='https://besmarterthanthetool.com/'
page=urllib.request.urlopen(base,timeout=45).read()
out.joinpath('public-index.html').write_bytes(page)
html=page.decode(); src=re.search(r'prediction: \{ src: "([^"]+\.mp4[^\"]*)"',html).group(1)
h=hashlib.sha256(); size=0
with urllib.request.urlopen(base+src,timeout=60) as r:
 headers=dict(r.headers)
 while chunk:=r.read(1024*1024): h.update(chunk); size+=len(chunk)
local=pathlib.Path('course-assets/how-ai-answers/how-ai-answers.mp4')
record={'url':base+src,'sha256':h.hexdigest(),'bytes':size,'headers':headers,'local_sha256':hashlib.sha256(local.read_bytes()).hexdigest()}
parts=[]
for name in ['DogRecapStrip','LastTokenBridgeBoard','AnswerBuildStrip','PredictionSection']:
 pat=r'function '+name+r'\([^\n]*\{.*?\n\}'
 live=re.search(pat,html,re.S).group(); loc=re.search(pat,pathlib.Path('index.html').read_text(),re.S).group()
 record[name+'_matches_local']=live==loc; parts.append(live)
out.joinpath('live-lesson-source.txt').write_text('\n'.join(parts))
out.joinpath('public-verification.json').write_text(json.dumps(record,indent=2))
print(json.dumps(record,indent=2))

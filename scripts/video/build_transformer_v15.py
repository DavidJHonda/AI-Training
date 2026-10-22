#!/usr/bin/env python3
"""User-requested highlight-only repair of v14. Audio stream copied exactly.

Reassembles from the same retained v12 visuals and canonical boards to avoid
another finished-video generation. No lesson, installation or publication edits.
"""
from pathlib import Path
import copy,json,subprocess
import cv2
from editspec_build import Build,Reader,sha
from build_embeddings_v7 import Renderer
import build_transformer_v14 as prior
ROOT=Path(__file__).resolve().parents[2]
OLD=ROOT/'video-audit/transformer-build-v14-2026-10-22'
OUT=ROOT/'video-audit/transformer-build-v15-2026-10-22'
SOURCE=ROOT/'Prompts/transformer-v14.mp4';DEST=ROOT/'Prompts/transformer-v15.mp4'

def main():
 assert not DEST.exists(),'Never overwrite a candidate'
 old=json.loads((OLD/'edit-manifest.json').read_text());assert sha(SOURCE)==old['candidate_sha256']
 assert all(sha(Path(p))==h for p,h in old['protected'].items())
 OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
 specs=copy.deepcopy(old['specs']);meta=copy.deepcopy(old['boards'])
 ctx=specs['context'];bylabel={r['label']:r for r in ctx['rings']}
 bylabel['cat sentence']['end']=bylabel['cat answer']['end']
 bylabel['milk sentence']['end']=bylabel['milk answer']['end']
 ctx['rings']=[r for r in ctx['rings'] if r['label'] not in ['cat answer','milk answer']]
 specs['earlier']['rings']=[r for r in specs['earlier']['rings'] if r['label']!='IT refers to CAT']
 b=Build(ROOT,prior.VIS,OUT,DEST);renderers={}
 for key,spec in specs.items():
  asset=ROOT/meta[key]['asset'];assert sha(asset)==meta[key]['sha256']
  canvas,cw,ch,ox,oy=b.compose(asset,key);assert [ox,oy]==meta[key]['canvas_offset'];spec['image']=str(canvas)
  (OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2)+'\n');renderers[key]=Renderer(spec)
 mapping=[]
 for row in old['timeline']:
  assert len(mapping)==row['start_frame']
  mapping.extend(range(row['source_start'],row['source_end']) if row['kind']=='retained' else [-1]*(row['end_frame']-row['start_frame']))
 assert len(mapping)==7163
 prior.OUT=OUT;prior.DEST=DEST
 repaired,paper_manifest=prior.paper()
 mapped=[None]*7163
 for key,v in meta.items():
  for n in range(v['start_frame'],v['end_frame']):mapped[n]=(key,n-v['start_frame'])
 for n in range(1107,1222):mapped[n]=None
 samples=[]
 for n in [1222,1254,1255,1260,1281,1282,1293,1379,1380,1395,1412,1413,2099,2100,2160,2213,2214]:
  key,local=mapped[n];im,_,geo=renderers[key].at(local);p=OUT/'preview'/f'{n:05d}.png';cv2.imwrite(str(p),im);samples.append(dict(frame=n,path=str(p),key=key,rings=geo))
 manifest=copy.deepcopy(old);manifest.update(candidate=str(DEST),audio_source=str(SOURCE),audio_source_sha256=sha(SOURCE),specs=specs,prepared_states=samples,paper_tracking=paper_manifest,approval='User requested full sentence-section highlights throughout the spoken pronoun examples at :42–:47, and no highlight on the unspoken We know IT sentence around 1:09.',scope='Highlight-only repair. No audio, camera, scene, duration or lesson change.',changed_frame_ranges=[[1255,1282],[1380,1413],[2100,2214]],boundaries=[1255,1282,1380,1413,2100,2214],status='prepared')
 manifest.pop('candidate_sha256',None)
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 ff=prior.ff;cmd=[ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(SOURCE),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE);rd=Reader(prior.VIS);ins=Reader(prior.VIS)
 for n,f in enumerate(mapping):
  if 1107<=n<1222:im=ins.at(1171+n-1107)
  elif mapped[n]:key,local=mapped[n];im=renderers[key].at(local)[0]
  elif 1497<=n<1735:im=repaired[n-1497]
  else:assert f>=0;im=rd.at(f)
  proc.stdin.write(im.tobytes())
  if n%1000==999:print(f'Rendered {n+1}/7163',flush=True)
 proc.stdin.close();assert proc.wait()==0;rd.c.release();ins.c.release()
 assert sha(SOURCE)==manifest['audio_source_sha256'];assert all(sha(Path(p))==h for p,h in old['protected'].items())
 manifest.update(status='built for review',candidate_sha256=sha(DEST),encode_command=cmd)
 (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(DEST,flush=True)
if __name__=='__main__':main()

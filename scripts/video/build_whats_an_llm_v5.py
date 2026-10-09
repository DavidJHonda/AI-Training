#!/usr/bin/env python3
"""Final Notebook restoration, with cleaned original crossfade into branching."""
import json
import build_whats_an_llm_v4 as prior
base=prior.base
base.OUT=base.ROOT/'video-audit/whats-an-llm-build-2026-10-09-v5'
base.DEST=base.ROOT/'Prompts/whats-an-llm-v5.mp4'
prepare_prior=base.prepare
frame_prior=base.frame

def prepare():
 b,boards,m=prepare_prior()
 m['retiming']['growing_branch_seam']='At original 138.30 s, cut over the 1.2 s overlapping source crossfade to clean branch animation at 139.50 s, retiming its remainder to the existing close boundary. Audio is unchanged.'
 m['boundaries'] += [dict(frame=4271,label='Clean Notebook branch transition')]
 m['boundaries']=sorted(m['boundaries'],key=lambda x:x['frame'])
 (base.OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 return b,boards,m

def frame(f,r,b,boards,reader,close,counts):
 if r['visual']!='growing':return frame_prior(f,r,b,boards,reader,close,counts)
 t=(f-122)/30
 if t>=138.3:
  t=139.5+(t-138.3)*(142.7-139.5)/(142.7-138.3)
  im=prior.get_source('growing',2,round(t*30))
  prior.paper(im,(473,94,828,128),930)
  im=prior.label(im,(650,111),'Different possible answers',color='#7b2630',size=23)
 else:
  im=prior.get_source('growing',2,round(t*30))
  prior.paper(im,(250,248,435,281),455);im=prior.label(im,(345,265),'Words so far',size=22)
  prior.paper(im,(792,220,1090,254),1110);im=prior.label(im,(946,238),'Predict the next word',color='#7b2630',size=23)
  if t>=133.6:prior.paper(im,(844,343,1050,378),1080)
 im,how=base.clean_frame(im,prior.MASK);counts[how]=counts.get(how,0)+1
 return im
base.prepare=prepare;base.frame=frame
if __name__=='__main__':base.render()

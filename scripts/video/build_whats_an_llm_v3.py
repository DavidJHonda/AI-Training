#!/usr/bin/env python3
"""Final review build from pristine rolls; remove the retained animation's percentage label."""
import json
import numpy as np
from build_creative_thinking_v8 import BoardRenderer
import build_whats_an_llm_v2 as base
base.OUT=base.ROOT/'video-audit/whats-an-llm-build-2026-10-09-v3'
base.DEST=base.ROOT/'Prompts/whats-an-llm-v3.mp4'
prepare_base=base.prepare
frame_base=base.frame

def prepare():
 b,boards,m=prepare_base()
 # Refine card switches against the assembled word-timed transcript.
 changes={'familiar':{0:52.68},'loop':{0:114.24,1:119.12,2:121.74,3:125.52}}
 for key,onsets in changes.items():
  p=base.OUT/f'leg-{key}.json';s=json.loads(p.read_text());start=m['boards'][key]['src_in']
  for i,t in onsets.items():
   f=round(t*30);s['rings'][i]['start']=f-start;m['boards'][key]['states'][i]['spoken_onset_source_frame']=f
   if i:s['rings'][i-1]['end']=f-start
  m['boards'][key]['full_view_frames']=s['rings'][0]['start']
  p.write_text(json.dumps(s,indent=2)+'\n');m['boards'][key]['rings']=s['rings'];b.boards[key]['rings']=s['rings'];boards[key]=BoardRenderer(p)
 m['visual_patch']={'source_roll':2,'source_frames':[1675,1788],'output_frames':[1730,1843],'box':[855,540,1055,568],'method':'Same-frame adjacent horizontal background clone, feathered; remove only the probability sublabel. Keep the original reveal, drawings, jelly labels and final answer.'}
 (base.OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
 return b,boards,m

def frame(f,r,b,boards,reader,close,counts):
 im=frame_base(f,r,b,boards,reader,close,counts)
 if 1730<=f<1843:
  x0,y0,x1,y1=855,540,1055,568
  donor=np.repeat(np.median(im[y0:y1,1070:1100],axis=1)[:,None,:],x1-x0,axis=1)
  alpha=np.ones((y1-y0,x1-x0),float);ramp=np.linspace(0,1,4)
  alpha[:4]*=ramp[:,None];alpha[-4:]*=ramp[::-1,None];alpha[:,:4]*=ramp;alpha[:,-4:]*=ramp[::-1]
  im[y0:y1,x0:x1]=np.rint(im[y0:y1,x0:x1]*(1-alpha[:,:,None])+donor*alpha[:,:,None]).astype(np.uint8)
 return im
base.prepare=prepare;base.frame=frame
if __name__=='__main__':base.render('--preview' in base.sys.argv)

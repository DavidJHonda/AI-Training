#!/usr/bin/env python3
"""Final candidate: correct the full bounds of the retained branch drawing's footer."""
import shutil
import numpy as np
import build_the_next_token_v1 as base
OLD=base.OUT
base.OUT=base.ROOT/'video-audit/the-next-token-build-2026-10-09-v2'
base.DEST=base.ROOT/'Prompts/the-next-token-v2.mp4'
original=base.Film.repair_source
def repair(self,im,kind,sf):
 if kind=='branch':
  x0,y0,x1,y1=250,525,1030,622
  donor=im[30:127,x0:x1].astype(float);target=im[y0:y1,x0:x1].astype(float)
  alpha=np.ones((y1-y0,x1-x0),float)
  for j in range(10):
   alpha[j,:]*=j/10;alpha[-1-j,:]*=j/10;alpha[:,j]*=j/10;alpha[:,-1-j]*=j/10
  im[y0:y1,x0:x1]=(donor*alpha[:,:,None]+target*(1-alpha[:,:,None])).astype(np.uint8)
  return im
 return original(self,im,kind,sf)
base.Film.repair_source=repair
if __name__=='__main__':
 base.OUT.mkdir(exist_ok=True)
 for name in ['roll-1.wav','roll-3.wav',*[f'temperature-{i}.png' for i in range(4)]]:
  if not (base.OUT/name).exists():shutil.copy2(OLD/name,base.OUT/name)
 base.main()

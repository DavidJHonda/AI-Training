#!/usr/bin/env python3
"""v13 lesson update plus repair of the inherited old-board dissolve."""
import cv2
import build_embeddings_v13 as base
from build_embeddings_v10 import animation
base.DEST=base.ROOT/'Prompts/embeddings-v14.mp4'
# Re-render the first ten mystery-animation frames from its existing source code.
# v12 blends these with the retired table; begin on the animation itself instead.
for frame in range(2589,2599):
 name=f'mystery-{frame}'
 cv2.imwrite(str(base.OUT/'captures'/f'{name}.png'),animation(frame/30,'mystery'))
 base.STATES.append((frame,frame+1,name))
base.STATES.sort()
if __name__=='__main__':base.main()

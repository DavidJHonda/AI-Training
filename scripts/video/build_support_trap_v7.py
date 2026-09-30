#!/usr/bin/env python3
"""Final Support Trap combination: remove a one-frame ring blink before lunch insert."""
import build_support_trap_v5 as b
b.OUT=b.ROOT/'video-audit/support-trap-build-2026-09-30-v7'
b.DEST=b.ROOT/'Prompts/support-trap-v7.mp4'
b.AUDIO_COPY_SOURCE=b.ROOT/'Prompts/support-trap-v6.mp4'
for r in b.VIS:
    if r['label']=='Urgency: real help now':r['video_start']=b.fr(142.5)
    if r['label']=='Comparison board' and r['end_frame']==880:r['end_frame']=878
    if r['label']=='Sister makes room at lunch':r['start_frame']=878
# Move the picture cut two frames earlier, before the next section ring; audio untouched.
if __name__=='__main__':b.main()

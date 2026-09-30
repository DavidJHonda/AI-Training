#!/usr/bin/env python3
"""Check the delivered frames, audio identity, timing and visual edit boundaries."""
import json,sys,subprocess
from itertools import zip_longest
import av,cv2,numpy as np
from PIL import Image,ImageDraw
import build_curious_flexible_v6 as b

def main():
 cv2.setNumThreads(2)
 out=b.OUT/'qa';out.mkdir(exist_ok=True)
 preview=out/'frames';preview.mkdir(exist_ok=True)
 boundaries=sorted(b.BOUNDARIES)
 wants={f for a,c,_ in b.CHANGED for f in [a-1,a,a+15,(a+c)//2,c-1,c]}
 wants|={1671,1710,2015,2070,2372,2430,2706,2770,3135,3210,3662,3700,4072,4120,4411,4470,4811,4900,5181,5270,6073,6121,6271,6375}
 wants|={5569,5580,5595,5600,5605,5640,5700,5760,5820,5880,5940,6000,6060}
 source=av.open(str(b.SRC)); dest=av.open(str(b.DEST))
 for c in [source,dest]:c.streams.video[0].codec_context.thread_count=2
 checks=[];samples=[];count=0;last=None
 for n,(sf,df) in enumerate(zip_longest(source.decode(video=0),dest.decode(video=0))):
  assert sf is not None and df is not None, "Source/output decoded lengths differ"
  assert (df.width,df.height)==(1280,720)
  assert abs(float(df.pts*df.time_base)-n/30)<.0001
  if n%30==0 or n in wants:
   src=sf.to_ndarray(format='yuv420p');dst=df.to_ndarray(format='yuv420p')
   changed=any(a<=n<c for a,c,_ in b.CHANGED)
   if not changed:
    yerr=abs(src[:720].astype('int16')-dst[:720].astype('int16'))
    checks.append(dict(frame=n,mean_luma_error=float(yerr.mean()),p99_luma_error=float(np.percentile(yerr,99))))
   if n in wants or n%120==0:
    im=df.to_ndarray(format='bgr24')
    if n in wants:cv2.imwrite(str(preview/f'{n:06}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,95])
    if n%120==0:samples.append((n,im))
  last=df;count+=1
 assert count==b.N,count
 assert b.audio_hash(b.SRC)==b.audio_hash(b.DEST)
 assert b.audio_hash(b.SRC,True)==b.audio_hash(b.DEST,True)
 assert max(x['mean_luma_error'] for x in checks)<2.0
 for k in range(0,len(samples),12):
  items=samples[k:k+12];sheet=Image.new('RGB',(1440,1080),'white');d=ImageDraw.Draw(sheet)
  for j,(n,im) in enumerate(items):
   x=(j%3)*480;y=(j//3)*270
   img=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB)).resize((480,270))
   sheet.paste(img,(x,y));d.rectangle((x,y,x+98,y+28),fill='white');d.text((x+7,y+3),f'{n/30//60:.0f}:{n/30%60:05.2f}',font=b.ft(21,True),fill='#b31b26')
  sheet.save(out/f'sheet-{k//12:02}.jpg',quality=92)
 m=dict(decoded_frames=count,expected_frames=b.N,fps=30,duration=count/30,dimensions=[1280,720],frame_timestamps_exact=True,audio_packets_identical=True,decoded_audio_identical=True,unchanged_region_samples=len(checks),unchanged_max_mean_luma_error=max(x['mean_luma_error'] for x in checks),unchanged_frame_checks=checks,source_still_matches=b.sha(b.SRC)==b.EXPECTED,manual_review='Pending inspection of contact sheets, final frames and transition strips; not listened by ear.')
 (out/'verification.json').write_text(json.dumps(m,indent=2)+'\n')
 print(json.dumps({k:v for k,v in m.items() if k!='unchanged_frame_checks'},indent=2))
 args=[sys.executable,str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST)]
 for n,label in b.BOUNDARIES.items():args+=['--boundary',f'{n}:{label}']
 subprocess.run(args+['--handle','8','--outdir',str(out/'transitions')],check=True)
if __name__=='__main__':main()

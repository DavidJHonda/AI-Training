#!/usr/bin/env python3
"""Run the same final-file checks and confirm narration is bit-for-bit inherited."""
import json,subprocess,hashlib
import imageio_ffmpeg
import cv2,numpy as np
import qa_tokens_v12 as qa
from build_tokens_v13 import OUT,DEST,BASE

qa.OUT=OUT
qa.DEST=DEST
# Two lossy generations: retain the 3-level budget per generation and also
# compare every sampled board directly with the already-verified parent.
qa.BOARD_MAE_LIMIT=6
qa.main()
ff=imageio_ffmpeg.get_ffmpeg_exe()
def audio_hash(path):
 return hashlib.sha256(subprocess.check_output([ff,'-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])).hexdigest()
original=audio_hash(BASE);final=audio_hash(DEST)
assert original==final
p=OUT/'encoded-check/results.json';m=json.loads(p.read_text())
caps=[cv2.VideoCapture(str(p)) for p in [BASE,DEST]]
for row in m['board_checks']:
 images=[]
 for cap in caps:
  cap.set(cv2.CAP_PROP_POS_FRAMES,row['frame']);ok,im=cap.read();assert ok;images.append(im)
 err=float(np.abs(images[0].astype(np.int16)-images[1].astype(np.int16)).mean())
 assert err<3,(row['frame'],err)
 row['parent_encoded_pixel_mae']=err
for cap in caps:cap.release()
m['audio']['aac_payload_sha256']=final
m['audio']['identical_to_v12']=True
p.write_text(json.dumps(m,indent=2)+'\n')
print('AAC payload identical:',final)

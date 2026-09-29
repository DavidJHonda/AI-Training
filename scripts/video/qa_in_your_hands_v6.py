#!/usr/bin/env python3
"""Check encoded v6 against preview frames, source spans, and all declared seams."""
import json, subprocess, sys
from pathlib import Path
import cv2
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/in-your-hands-build-2026-09-29-v6'
M=json.loads((OUT/'edit-manifest.json').read_text())
candidate=Path(M['candidate']); source=Path(M['source'])
expected={int(p.stem):p for p in (OUT/'preview').glob('*.jpg')}
c=cv2.VideoCapture(str(candidate)); s=cv2.VideoCapture(str(source)); i=0; rows=[]; retained=[]
while True:
    ok,f=c.read()
    if not ok:break
    ok,base=s.read();assert ok
    if i in expected:
        e=cv2.imread(str(expected[i]));mae=float(np.abs(f.astype(float)-e).mean())
        rows.append({'frame':i,'mean_absolute_pixel_error_vs_preview':round(mae,4)})
        assert mae<4,(i,mae,'Unexpected frame content')
    if (i<1059 or i>=5046) and i%30==0:
        mae=float(np.abs(f.astype(float)-base).mean());retained.append({'frame':i,'mae':round(mae,4)})
        assert mae<4,(i,mae,'Retained content changed')
    i+=1
assert i==5508,i
assert len(rows)==len(expected)
assert M['audio_packets_identical']
c.release();s.release()
args=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(candidate),'--outdir',str(OUT/'transitions')]
for b in M['boundaries']:args.extend(['--boundary',f"{b['frame']}:{b['label']}"])
r=subprocess.run(args)
result={'decoded_frames':i,'preview_samples':len(rows),'max_preview_error':max(x['mean_absolute_pixel_error_vs_preview'] for x in rows),
        'retained_samples':len(retained),'max_retained_error':max(x['mae'] for x in retained),
        'audio_packets_identical':True,'transition_guard_exit':r.returncode,'preview_checks':rows,'retained_checks':retained}
(OUT/'qa.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if not isinstance(v,list)},indent=2))

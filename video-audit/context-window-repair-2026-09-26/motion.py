import cv2, numpy as np, sys
src=sys.argv[1]; a=int(sys.argv[2]); b=int(sys.argv[3])
cap=cv2.VideoCapture(src); i=-1; prev=None; out=[]
while i<b:
    ok,im=cap.read(); i+=1
    if i<a: continue
    g=cv2.cvtColor(cv2.resize(im,(320,180)),cv2.COLOR_BGR2GRAY).astype(int)
    if prev is not None: out.append((i, abs(g-prev).mean()))
    prev=g
line=[]
for f,d in out: line.append(f"{f}:{d:.2f}")
print(' '.join(line))

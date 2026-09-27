import cv2, sys
src, out = sys.argv[1], sys.argv[2]; fs = sorted(int(x) for x in sys.argv[3:])
cap = cv2.VideoCapture(src); i=-1
for f in fs:
    while i < f:
        ok, im = cap.read(); i += 1
    cv2.imwrite(f"{out}/f{f:05d}.png", im)

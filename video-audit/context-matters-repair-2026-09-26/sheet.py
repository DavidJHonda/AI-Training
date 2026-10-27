import cv2, numpy as np, sys
src, out, a, b, step = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5])
cols = int(sys.argv[6]) if len(sys.argv) > 6 else 6
cap = cv2.VideoCapture(src); fps = cap.get(cv2.CAP_PROP_FPS)
f0, f1 = int(round(a*fps)), int(round(b*fps))
cap.set(cv2.CAP_PROP_POS_FRAMES, max(0, f0-60)); i = max(0, f0-60)
# sequential decode from a seek point well before; verify with pos
i = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
tiles = []
while i < f1:
    ok, im = cap.read()
    if not ok: break
    if i >= f0 and (i - f0) % step == 0:
        t = cv2.resize(im, (384, 216))
        cv2.putText(t, f"{i/fps:.2f} f{i}", (4, 20), cv2.FONT_HERSHEY_SIMPLEX, .6, (0,0,0), 3)
        cv2.putText(t, f"{i/fps:.2f} f{i}", (4, 20), cv2.FONT_HERSHEY_SIMPLEX, .6, (0,255,255), 1)
        tiles.append(t)
    i += 1
while len(tiles) % cols: tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[k:k+cols]) for k in range(0, len(tiles), cols)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 80]); print(out, len(tiles))

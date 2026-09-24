import sys, cv2, numpy as np
src, t0, t1, step, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
want = [round(t*30) for t in np.arange(t0, t1 + 1e-6, step)]
cap = cv2.VideoCapture(src); i = -1; cells = []
while want:
    ok, im = cap.read()
    if not ok: break
    i += 1
    if i == want[0]:
        c = cv2.resize(im, (384, 216)); cv2.putText(c, f"{i/30:.2f} f{i}", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 0, 255), 2); cells.append(c); want.pop(0)
while len(cells) % 4: cells.append(np.zeros_like(cells[0]))
cv2.imwrite(out, cv2.vconcat([cv2.hconcat(cells[k:k+4]) for k in range(0, len(cells), 4)]), [cv2.IMWRITE_JPEG_QUALITY, 80])

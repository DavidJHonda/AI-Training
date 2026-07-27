"""NotebookLM corner-mark detector, v2 -- POLARITY INVARIANT.

v1 matched a high-passed ROI with TM_CCOEFF_NORMED against a template taken from
a dark scene. The mark is light-on-dark there and dark-on-light elsewhere, so the
high-pass signal flips sign and correlation collapsed: it scored art-of-prompting
0.019 while the mark is plainly visible at full res. Matching on GRADIENT
MAGNITUDE removes the sign, so the same template works on either background.

Validated on: ai-is-math (dark bg, positive), art-of-prompting (pale bg, positive),
layers f900 (negative).
"""
import glob, os, sys
import cv2
import numpy as np

REPO = "/Users/davidobrien/Documents/GitHub/AI-Training"
ROI = (1130, 680, 1275, 715)
THRESH = 0.45
STEP_FR = 45          # 1.5s at 30fps


def gradmag(g):
    g = cv2.GaussianBlur(g.astype("float32"), (0, 0), 0.8)
    gx = cv2.Sobel(g, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(g, cv2.CV_32F, 0, 1, ksize=3)
    m = cv2.magnitude(gx, gy)
    return m - m.mean()


def roi(f):
    x0, y0, x1, y1 = ROI
    return gradmag(cv2.cvtColor(f[y0:y1, x0:x1], cv2.COLOR_BGR2GRAY))


def grab(path, n):
    cap = cv2.VideoCapture(path); i = 0
    while True:
        ok, f = cap.read()
        if not ok: return None
        if i == n: return f
        i += 1


def score(f, tpl):
    r = roi(f)
    if r.shape != tpl.shape: return 0.0
    return float(cv2.matchTemplate(r, tpl, cv2.TM_CCOEFF_NORMED).max())


def build():
    return roi(grab(os.path.join(REPO, "videos/ai-is-math.mp4"), 900))


def scan(path, tpl):
    cap = cv2.VideoCapture(path); i = 0; hit = 0; tot = 0; mx = 0.0; first = None
    while True:
        ok, f = cap.read()
        if not ok: break
        if i % STEP_FR == 0:
            s = score(f, tpl); tot += 1; mx = max(mx, s)
            if s >= THRESH:
                hit += 1
                if first is None: first = i / 30.0
        i += 1
    return hit, tot, mx, first


if __name__ == "__main__":
    tpl = build()
    if sys.argv[1:2] == ["--validate"]:
        for label, slug, fr in [("POS dark  ai-is-math f1200", "ai-is-math", 1200),
                                ("POS pale  art-of-prompting f1220", "art-of-prompting", 1220),
                                ("NEG       layers f900", "layers", 900),
                                ("NEG       welcome f600", "welcome", 600)]:
            f = grab(os.path.join(REPO, "videos/%s.mp4" % slug), fr)
            print("%-36s %.3f" % (label, score(f, tpl)))
        sys.exit()
    rows = []
    for p in sorted(glob.glob(os.path.join(REPO, "videos/*.mp4"))):
        h, t, mx, first = scan(p, tpl)
        rows.append((h / t if t else 0, mx, h, t, first, os.path.basename(p)[:-4]))
    rows.sort(key=lambda r: -r[0])
    print("%-24s %6s %6s %12s  %s" % ("video", "frac", "max", "frames", "first seen"))
    for frac, mx, h, t, first, slug in rows:
        fs = "-" if first is None else "%d:%05.2f" % (int(first) // 60, first % 60)
        print("%-24s %5.0f%% %6.3f %6d/%-5d %s" % (slug, frac * 100, mx, h, t, fs))

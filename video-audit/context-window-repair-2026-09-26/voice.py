"""Per-span voice metrics: median F0 (Hz), F0 at the span's last voiced 250 ms (terminal contour),
voiced loudness (dBFS), spectral centroid (Hz), floor (10th percentile 10 ms RMS dB)."""
import numpy as np, wave, sys
def load(p):
    w = wave.open(p); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)/32768; return a, w.getframerate()
def f0_track(x, sr, hop=0.01, win=0.04):
    out=[]; n=int(win*sr); h=int(hop*sr)
    for i in range(0, len(x)-n, h):
        f = x[i:i+n]*np.hanning(n); e = np.sqrt(np.mean(f*f))
        if e < 10**(-38/20): out.append(np.nan); continue
        ac = np.correlate(f, f, 'full')[n-1:]; lo, hi = int(sr/320), int(sr/75)
        k = lo + np.argmax(ac[lo:hi]); out.append(sr/k if ac[k] > 0.45*ac[0] else np.nan)
    return np.array(out)
def metrics(a, sr, s, e):
    x = a[int(s*sr):int(e*sr)]; t = f0_track(x, sr); v = t[~np.isnan(t)]
    idx = np.where(~np.isnan(t))[0]
    tail = t[idx[-25:]] if len(idx) else np.array([np.nan])
    head = t[idx[:25]] if len(idx) else np.array([np.nan])
    hop=int(.01*sr); r = np.array([np.sqrt(np.mean(x[i:i+hop]**2))+1e-9 for i in range(0,len(x)-hop,hop)]); db=20*np.log10(r)
    voiced = db[db > np.percentile(db, 60)]
    X = np.abs(np.fft.rfft(x*np.hanning(len(x)))); fr = np.fft.rfftfreq(len(x), 1/sr); c = float((X*fr).sum()/X.sum())
    return dict(f0_med=float(np.nanmedian(v)) if len(v) else None, f0_head=float(np.nanmedian(head)), f0_tail=float(np.nanmedian(tail)),
                loud=float(np.mean(voiced)), centroid=c, floor=float(np.percentile(db,10)))
if __name__ == '__main__':
    a, sr = load(sys.argv[1])
    for spec in sys.argv[2:]:
        name, s, e = spec.split(':'); m = metrics(a, sr, float(s), float(e))
        print(f"{name:28s} {float(s):7.2f}-{float(e):7.2f} f0 {m['f0_med']:.0f} head {m['f0_head']:.0f} tail {m['f0_tail']:.0f}  loud {m['loud']:.1f} dB  centroid {m['centroid']:.0f}  floor {m['floor']:.1f}")

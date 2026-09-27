import numpy as np, wave, sys
def load(p):
    w = wave.open(p); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)/32768; return a, w.getframerate()
a, sr = load(sys.argv[1]); hop = sr//100
db = np.array([20*np.log10(np.sqrt(np.mean(a[i:i+hop]**2))+1e-9) for i in range(0, len(a)-hop, hop)])
np.save(sys.argv[2], db)
thr = float(sys.argv[3]) if len(sys.argv)>3 else -40
q = db < thr; i = 0; out=[]
while i < len(q):
    if q[i]:
        j=i
        while j<len(q) and q[j]: j+=1
        if j-i >= 10: out.append((i/100, j/100, float(db[i:j].min()), float(np.median(db[i:j]))))
        i=j
    else: i+=1
for s,e,mn,md in out: print(f"{s:7.2f}-{e:7.2f} ({e-s:4.2f}s) min {mn:6.1f} med {md:6.1f}")

import sys, wave, numpy as np
n=sys.argv[1]; _w=wave.open(f'video-audit/training-reroll-review-2026-09-27/training-{n}/audio.wav'); sr=_w.getframerate(); x=np.frombuffer(_w.readframes(_w.getnframes()),dtype=np.int16)/32768.0
w=int(sr*0.01); r=np.sqrt(np.convolve(x**2,np.ones(w)/w,'same'))[::w]; db=20*np.log10(r+1e-9)
for rng in sys.argv[2:]:
    a,b=map(float,rng.split('-')); q=db[int(a*100):int(b*100)]<-35; runs=[];s=None
    for i,v in enumerate(q):
        if v and s is None:s=i
        if not v and s is not None:
            if i-s>=15:runs.append(f"{(a*100+s)/100:.2f}-{(a*100+i)/100:.2f}")
            s=None
    if s is not None: runs.append(f"{(a*100+s)/100:.2f}-end")
    print(f"R{n} {rng} quiet>=150ms:", " ".join(runs))

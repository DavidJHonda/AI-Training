import wave, numpy as np
D='video-audit/training-reroll-review-2026-09-27'
def load(n):
    w=wave.open(f'{D}/training-{n}/audio.wav'); return np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768, w.getframerate()
A={n:load(n)[0] for n in (1,2,3)}; SR=48000
def seg(n,a,b): return A[n][int(a*SR):int(b*SR)]
def speech_db(n,a,b):
    x=seg(n,a,b); w=480; r=np.sqrt(np.convolve(x**2,np.ones(w)/w,'same'))[::w]; r=r[r>10**(-35/20)]
    return 20*np.log10(np.sqrt(np.mean(r**2)))
for n,a,b in [(3,0,60),(3,100,250),(1,0,60),(1,100,117),(2,155,178),(2,300,311.3)]:
    print(f'roll {n} {a}-{b} speech RMS {speech_db(n,a,b):.1f} dBFS')
def join(parts,name,gain=None):
    out=[]; F=int(0.005*SR)
    for i,(n,a,b) in enumerate(parts):
        x=seg(n,a,b).copy()
        if gain and n in gain: x*=10**(gain[n]/20)
        x[:F]*=np.linspace(0,1,F); x[-F:]*=np.linspace(1,0,F); out.append(x)
    y=np.concatenate(out); w=wave.open(f'{D}/audition/{name}.wav','wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(y,-1,1)*32767).astype(np.int16).tobytes()); print(name, f'{len(y)/SR:.1f}s')
g={}
d=speech_db(3,0,60)-speech_db(1,0,60); g={1:d}; print('roll1 gain to match roll3', round(d,2))
join([(3,16.0,23.30),(1,20.10,26.0)],'A1-roll3-ready-to-use__roll1-two-things',g)
join([(1,55.0,60.90),(3,59.50,66.0)],'A2-roll1-through-feedback__roll3-across-all-three',g)
join([(3,116.0,123.45),(3,139.30,146.5)],'B-pretraining-quote-cut__sport__in-this-guide')
join([(3,109.9,115.60),(1,114.10,117.90),(3,116.0,120.0)],'C-optional-roll1-write-and-explain-ideas',g)
join([(3,245.0,256.1)],'D-roll3-close-as-is')
d2=speech_db(3,100,250)-speech_db(2,300,311.3)
join([(3,241.0,246.9),(2,305.60,313.5)],'D-alt-roll2-close',{2:d2})

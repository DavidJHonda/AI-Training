import sys, av, numpy as np
src=sys.argv[1]; c=av.open(src); s=c.streams.audio[0]
rs=av.AudioResampler(format='flt',layout='mono',rate=16000)
buf=[]
for fr in c.decode(s):
    for r in rs.resample(fr): buf.append(r.to_ndarray().ravel())
x=np.concatenate(buf); win=160
e=20*np.log10(np.sqrt((x[:len(x)//win*win].reshape(-1,win)**2).mean(1))+1e-9)
q=e< -45; t=0; out=[]
i=0
while i<len(q):
    if q[i]:
        j=i
        while j<len(q) and q[j]: j+=1
        if (j-i)*0.01>=0.15: out.append((i*0.01,j*0.01))
        i=j
    else: i+=1
for a,b in out: print(f"{a:7.2f} {b:7.2f} {b-a:.2f}")

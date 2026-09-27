import numpy as np, sys
from cuts import A, db, cuts
def env(r):
    x=A[r]; n=len(x)//480
    return np.array([db(x[i*480:(i+1)*480]) for i in range(n)])
E={r:env(r) for r in A}
def gap(r,a,b,thr=32):
    e=E[r]; i0,i1=int((a-0.15)*100),int((b+0.15)*100)
    q=e[i0:i1]<thr; runs=[];s=None
    for k,v in enumerate(q):
        if v and s is None: s=k
        if (not v or k==len(q)-1) and s is not None: runs.append((s,k)); s=None
    s,k=max(runs,key=lambda t:t[1]-t[0]); gs,ge=(i0+s)/100,(i0+k)/100
    c=(gs+ge)/2; f=round(c*30)
    return round(gs,2),round(ge,2),f,round(f/30,3)
if __name__=='__main__':
    for c in cuts: print(c, gap(*c))

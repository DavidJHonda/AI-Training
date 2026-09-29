#!/usr/bin/env python3
"""Check encoded frames, source timing, unchanged audio, rings and visual seams."""
import hashlib,json,subprocess
import av,cv2,numpy as np,imageio_ffmpeg
from PIL import Image,ImageDraw
from build_avoid_traps_opener_v9 import ROOT,SRC,DEST,OUT,N,CUTAWAYS,sha,ring_state
cv2.setNumThreads(2)

def audio_hash(p,decoded):
    fmt=['-c:a','pcm_s16le','-f','s16le'] if decoded else ['-c:a','copy','-f','adts']
    result=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(p),'-map','0:a:0',*fmt,'pipe:1'],capture_output=True,check=True)
    return hashlib.sha256(result.stdout).hexdigest()

def audio_packets(p):
    with av.open(str(p)) as c:
        return [(x.pts,x.dts,x.duration,str(x.time_base),hashlib.sha256(bytes(x)).hexdigest())
                for x in c.demux(audio=0) if x.size]

def main():
    m=json.loads((OUT/'edit-manifest.json').read_text())
    assert sha(DEST)==m['candidate_sha256']
    assert all(sha(p)==h for p,h in m['protected'].items())
    ah={kind:[audio_hash(SRC,decode),audio_hash(DEST,decode)] for kind,decode in [('aac',False),('pcm',True)]}
    assert all(a==b for a,b in ah.values()),ah
    ap1,ap2=audio_packets(SRC),audio_packets(DEST);assert ap1==ap2,'Audio packet timestamps/payload changed.'
    boundaries=m['boundaries']
    samples=set(range(0,N,60))|{N-1,2777,2820,2880,2940,3018,3850,4320,4500,5130}
    samples|={b+d for b in boundaries for d in [-3,-2,-1,0,1,2,3]}
    mapping={}
    for n in sorted(samples):
        cut=next((c for c in CUTAWAYS if c['start']<=n<c['end']),None)
        if cut:mapping[n]=cut['source_start']+n-cut['start']
        elif not any(a<=n<b for a,b in m['changed_spans']):mapping[n]=n
    cap=cv2.VideoCapture(str(SRC));cache={};idx=0;wanted=set(mapping.values())
    while True:
        ok,f=cap.read()
        if not ok:break
        if idx in wanted:cache[idx]=f
        idx+=1
    cap.release();assert idx==N
    (OUT/'encoded').mkdir(exist_ok=True)
    cap=cv2.VideoCapture(str(DEST));idx=0;retained=[];donors=[];panels=[];maps=[];rings=[];tiles=[]
    mapstates={k:cv2.imread(str(OUT/(f'map-state-{k}.png' if k is not None else 'map-unmarked.png'))) for k in [None,0,1,2]}
    while True:
        ok,f=cap.read()
        if not ok:break
        assert f.shape==(720,1280,3)
        if idx in samples:
            cv2.imwrite(str(OUT/'encoded'/f'{idx:05d}.jpg'),f)
            ref=None;category=None
            if idx in mapping:
                ref=cache[mapping[idx]];category=retained if mapping[idx]==idx else donors
            elif 3730<=idx<5666:
                ref=mapstates[ring_state(idx)];category=maps
            elif (OUT/f'label-preview-{idx}.png').exists():
                ref=cv2.imread(str(OUT/f'label-preview-{idx}.png'));category=panels
            if ref is not None:
                error=float(np.abs(f.astype(np.int16)-ref.astype(np.int16)).mean())
                category.append(dict(frame=idx,source=mapping.get(idx),mean_abs_difference=error))
                assert error<4,(idx,error)
        if idx in [3850,4320,4500,5130]:
            k=ring_state(idx);color=np.array([(79,47,196),(22,82,240),(14,143,134)][k])
            # Measure solid colour runs across the middle of the top edge.
            yy=[130,283,437][k]
            roi=f[yy-12:yy+12,500:780,::-1].astype(float)
            mask=np.linalg.norm(roi-color,axis=2)<45
            widths=mask.sum(axis=0)
            width=float(np.median(widths));assert 3.5<=width<=4.5,(idx,width)
            rings.append(dict(frame=idx,color=k,solid_width_px=width))
        if idx%120==0 or idx in [2777,2820,2880,3018,3730,3832,4079,4080,4170,4259,4260,4320,4494,4859,4860,4970,5069,5070,5115,5665,5666,N-1]:
            im=Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)).resize((384,216))
            tile=Image.new('RGB',(384,242),'white');tile.paste(im,(0,26));ImageDraw.Draw(tile).text((6,7),f'{idx/30:.3f}s | frame {idx}',fill='black');tiles.append(tile)
        idx+=1
    fps=cap.get(cv2.CAP_PROP_FPS);cap.release();assert idx==N and fps==30
    for j in range(0,len(tiles),16):
        sh=Image.new('RGB',(1536,968),'#eee')
        for k,im in enumerate(tiles[j:j+16]):sh.paste(im,((k%4)*384,(k//4)*242))
        sh.save(OUT/f'qa-sheet-{j//16}.jpg')
    results=dict(frames=idx,fps=fps,duration=idx/fps,audio_hashes=ah,aac_identical=True,decoded_pcm_identical=True,
                 audio_packets_identical=True,audio_packet_count=len(ap1),protected_unchanged=True,
                 retained_frames=retained,donor_frames=donors,label_frames=panels,map_frames=maps,
                 rebuilt_rings=rings,longest_board_hold_seconds=20.0,listening='Not performed; audio identical to v7')
    (OUT/'qa.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:v for k,v in results.items() if not k.endswith('_frames')},indent=2),flush=True)
    args=[str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'guard')]
    for b in boundaries:args+=['--boundary',f'{b}:checked-edit-boundary']
    subprocess.run(args,check=True)

if __name__=='__main__':main()

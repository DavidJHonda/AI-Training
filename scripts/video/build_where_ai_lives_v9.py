"""Build the November three-roll Where AI Lives review edit from original media."""
from bisect import bisect_right
from pathlib import Path
import json
import subprocess

import cv2
import numpy as np

from editspec_build import Build, FPS, H, W, Reader, fr, sha
from gemini_mark import clean_frame, glyph_mask
from ken_burns_path import draw_ring, hex_bgr, ring_px, smoothstep

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / 'video-audit/where-ai-lives-build-2026-11-19-v9'
REVIEW = ROOT / 'video-audit/where-ai-lives-rolls-1-3-2026-11-19'
RAW = {n: ROOT / f'Prompts/where-ai-lives-{n}.mp4' for n in (1, 2, 3)}
DEST = ROOT / 'Prompts/where-ai-lives-v9.mp4'
ASSETS = {name: ROOT / f'course-assets/where-ai-lives/where-ai-lives-{name}.jpg'
          for name in ('math', 'physical-footprint', 'data-center', 'close')}
# All dialogue boundaries land inside the measured inter-sentence gaps.
PARTS = [
    (3, 0, 173.27, 'Opening through parallel GPU work', 0),
    (2, 155.00, 161.40, 'Largest facilities', 0.3),
    (3, 181.37, 190.87, 'Person in the server hall', 0),
    (1, 154.80, 163.23, 'Cabinets and stacked servers', 0.4),
    (3, 191.17, 219.27, 'From the facility to electricity and bills', 0),
    (2, 220.73, 236.47, 'Water and evaporation', 0.7),
    (3, 231.07, 271.93, 'Noise, jobs and company responses', 0),
    (3, 280.73, 292.40, 'Two perspectives on the same data center', 0),
]
MATH = [(40,118,525,722), (557,118,1043,722), (1075,118,1560,722)]
NEIGHBORS = [(40,127,784,758), (816,127,1560,758), (40,790,784,1421), (816,790,1560,1421)]
COLORS = {'math': ['1652f0','4f2fc4','0e8f86'],
          'physical-footprint': ['4f2fc4','1652f0','0e8f86','a9760c']}


def prepare():
    for r in json.loads((REVIEW/'sources.json').read_text()):
        assert sha(ROOT/r['path']) == r['sha256']
    b = Build(ROOT, RAW[3], AUDIT, DEST, [RAW[1], RAW[2], *ASSETS.values()])
    b.load_audio([(190.58,191.48), (280.32,281.05)])
    for roll, start, end, label, gain in PARTS:
        if roll == 3:
            b.keep(fr(start),fr(end),label)
        else:
            b.graft(RAW[roll],fr(start),fr(end),label,label,picture_from=fr(start),gain_db=gain)
    # The phone/fan pairing precedes the canonical closing board.
    b.close_start = b.rows[-1]['start_frame'] + fr(3.35)
    b.pause(fr(2.5),'Closing hold')
    b.finish_audio()
    b.make_close('computecost')
    return b


class Picture:
    def __init__(self,b):
        self.b = b
        self.starts = [r['start_frame'] for r in b.rows]
        self.readers = {}
        self.mask = glyph_mask()
        self.cards = {}
        for name in COLORS:
            path,cw,ch,ox,oy = b.compose(ASSETS[name],name)
            self.cards[name] = (cv2.imread(str(path)), np.array([cw/2,ch/2,cw]), ox,oy)
        hall = cv2.imread(str(ASSETS['data-center']))
        height,width = hall.shape[:2]
        scaled_width = round(width*H/height)
        self.hall = np.full((H,W,3),245,np.uint8)
        left = (W-scaled_width)//2
        self.hall[:,left:left+scaled_width] = cv2.resize(hall,(scaled_width,H),interpolation=cv2.INTER_AREA)
        self.cache_key,self.cache_frame = None,None

    def native(self,n,t):
        target = fr(t)
        reader = self.readers.get(n)
        if not reader or target < reader.n:
            if reader:
                reader.c.release()
            reader = self.readers[n] = Reader(RAW[n])
        return clean_frame(reader.at(target),self.mask)[0]

    def board(self,name,card=-1,age=2):
        image,full,ox,oy = self.cards[name]
        rects = MATH if name=='math' else NEIGHBORS
        def view(idx):
            if idx<0 or name=='math':
                return full
            x,y,r,z=rects[idx]
            return np.array([ox+(x+r)/2,oy+(y+z)/2,self.b.fit_w(r-x,z-y)])
        progress = smoothstep(min(1,max(0,age/1.4)))
        camera = view(card-1)*(1-progress)+view(card)*progress if card>=0 else full
        key = (name,card,*camera)
        if key==self.cache_key:
            return self.cache_frame
        cx,cy,width = camera
        scale=W/width
        left,top=cx-width/2,cy-H/(2*scale)
        transform=np.float32([[1/scale,0,left],[0,1/scale,top]])
        frame=cv2.warpAffine(image,transform,(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REPLICATE)
        if card>=0:
            x,y,r,z=rects[card]
            draw_ring(frame,(x+ox-left)*scale,(y+oy-top)*scale,(r+ox-left)*scale,(z+oy-top)*scale,
                      hex_bgr(COLORS[name][card]),14*scale,ring_px(H))
        self.cache_key,self.cache_frame=key,frame
        return frame

    def scene(self,f):
        idx=bisect_right(self.starts,f)-1
        age=(f-self.starts[idx])/FPS
        if f>=self.b.close_start:
            t=f-self.b.close_start
            zoom=1+.2*smoothstep(min(1,max(0,(t-48)/150)))
            im=self.b.close_img
            h,w=im.shape[:2]
            width=w/zoom
            mat=np.float32([[width/W,0,(w-width)/2],[0,width/W,(h-width*H/W)/2]])
            return cv2.warpAffine(im,mat,(W,H),flags=cv2.WARP_INVERSE_MAP|cv2.INTER_CUBIC),'closing board'
        roll,start,_,label,_=PARTS[idx]
        s=fr(start)/FPS+age
        if idx==0:
            if 117.3<=s<139.4:
                card=bisect_right([120.4,124.35,131.43],s)-1
                return self.board('math',card),f'math panel {card+1}'
            if s>=166.4:
                return self.native(2,142.9+(s-166.4)*1.22),'GPU and parallel work'
        if idx==1:
            return self.native(1,134.9+age),'facility and football fields'
        if idx in (2,3):
            return self.hall,'server hall'
        if idx==4:
            if s<191.64:
                return self.hall,'server hall'
            if 197.75<=s<203.5:
                return self.native(2,190.8+age-(197.75-fr(start)/FPS)),'houses and the facility'
            if s>=203.5:
                return self.board('physical-footprint',0 if s>=206.6 else -1,s-206.6),'electricity' if s>=206.6 else 'neighbors overview'
        if idx==5:
            return self.board('physical-footprint',1,age),'water'
        if idx==6:
            if s<242.65:
                if 238.2<=s<241.9:
                    return self.native(2,195.47+s-238.2),'a neighbor looking out'
                return self.board('physical-footprint',2,age),'noise'
            if s<253.233333:
                return self.board('physical-footprint',3,s-242.65),'permanent jobs'
        if idx==7:
            return self.native(3,285.0+age),'phone and fan'
        return self.native(roll,s),label


def encode(b,pictures,details):
    temp=b.out/'render.tmp.mp4'
    boundaries={r['start_frame']:r['label'] for r in b.rows[1:]}
    cmd=[b.ff,'-y','-loglevel','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30',
         '-i','pipe:0','-i',str(b.out/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264',
         '-vf','scale=out_range=full:out_color_matrix=bt709:flags=accurate_rnd+full_chroma_int',
         '-color_range','pc','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709',
         '-preset','fast','-crf','18','-threads','4','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
         '-movflags','+faststart',str(temp)]
    previous=None
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as proc:
        for f in range(b.total):
            frame,label=pictures.scene(f)
            if f and label!=previous:
                boundaries[f]=label
                print(f'{f/FPS:.2f}s {label}',flush=True)
            previous=label
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        if proc.wait():
            raise RuntimeError('Video encoding failed')
    for reader in pictures.readers.values():
        reader.c.release()
    assert all(sha(p)==h for p,h in b.hashes.items())
    manifest=b.manifest(dict(**details,render_sha256=sha(temp)))
    manifest['boundaries']=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())]
    (b.out/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    temp.rename(b.dest)
    print(b.dest,b.total/FPS)


def main():
    if DEST.exists():
        raise SystemExit(f'Candidate already exists: {DEST}')
    cv2.setNumThreads(2)
    b=prepare()
    encode(b,Picture(b),dict(parts=PARTS))


if __name__=='__main__':
    main()

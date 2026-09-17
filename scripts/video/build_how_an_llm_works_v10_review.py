#!/usr/bin/env python3
"""Approved two-part repair; streaming, single-encode, review-only candidate.

Frames are half-open. Visual and audio timelines are independent: visual cuts do
not introduce audio fades. Only five actual audio joins receive 5ms tone ramps.
"""
from pathlib import Path
import argparse
import json
import subprocess

import cv2
import numpy as np

from editspec_build import (Build, Reader, fr, sha, readwav, writewav, rms,
                            banner_rect, PURPLE, BLUE, TEAL, GREEN, NEUTRAL)
from ken_burns_path import resolve, smoothstep, window, rings_for, draw_ring
from gemini_mark import clean_frame, glyph_mask

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/how-an-llm-works-repair-2026-09-17-v10'
DEST = ROOT / 'Prompts/how-an-llm-works-v10.mp4'
SOURCES = {n: ROOT/'Prompts'/f'how-the-model-{n}.mp4'
           for n in ('learns-1', 'learns-2', 'answers-1', 'answers-2')}
ASSETS = {k: ROOT/'course-assets/how-an-llm-works'/f'how-an-llm-works-{suffix}.jpg'
          for k, suffix in [('llm','llm'), ('training','training'), ('patterns','patterns'),
                            ('odds','same-word-different-odds'),
                            ('prediction','one-word-at-a-time'), ('close','close')]}
PART2 = 5196
CLOSE = 11200
TOTAL = CLOSE + 48 + 150 + 90
SR, SPF = 48000, 1600


def L(t):
    f = fr(t)
    return f + (135 if f >= 527 else 0)


def A(t):
    f = fr(t)
    return PART2 + f + (255 if f >= 1452 else 0)


def cards(path, count):
    im = cv2.imread(str(path)); bg = im[10, 10].astype(int)
    _, _, st, _ = cv2.connectedComponentsWithStats((im.min(axis=2)>246).astype(np.uint8), 4)
    panels = sorted([(int(x),int(y),int(x+w-1),int(y+h-1)) for x,y,w,h,a in st[1:]
                     if w>250 and h>150])
    assert len(panels)==count, (path, panels)
    result=[]
    for x0,_,x1,y1 in panels:
        d=(abs(im[:,x0:x1].astype(int)-bg).sum(axis=2)>40).mean(axis=1)
        yy=np.where(d>.6)[0]; yy=yy[yy>100]
        result.append([x0,int(yy.min()),x1,y1])
    return result


def target(label, frame, rect, color, cam=None):
    return dict(label=label, at=frame/30, rects=[rect], color=color, cam=cam or rect)


def update_spec(b, key, fn):
    p=OUT/f'leg-{key}.json'; spec=json.loads(p.read_text()); fn(spec)
    p.write_text(json.dumps(spec,indent=2))
    b.boards[key]['rings']=spec['rings']; b.boards[key]['beats']=spec['beats']


def ring(b, key, start, end, rect, color=NEUTRAL):
    ox,oy=b.boards[key]['canvas_offset']; base=b.boards[key]['src_in']
    return dict(start=start-base,end=end-base,rect=[rect[0]+ox,rect[1]+oy,
                rect[2]-rect[0],rect[3]-rect[1]],color=color,pad=0,radius=14)


def prepare():
    protected=[*list(SOURCES.values())[1:], ROOT/'index.html',
               *[ROOT/'lessons'/n for n in ('how-an-llm-works.md',
                 'how-an-llm-works-part-1.md','how-an-llm-works-part-2.md')],
               *ASSETS.values()]
    live=ROOT/'course-assets/how-an-llm-works/how-an-llm-works.mp4'
    if live.exists(): protected.append(live)
    b=Build(ROOT,SOURCES['learns-1'],OUT,DEST,protected=protected)
    b.tall_margin=False
    b.total=b.cursor=TOTAL; b.close_start=CLOSE
    lc=cards(ASSETS['llm'],3); pc=cards(ASSETS['patterns'],2)
    b.board('llm',ASSETS['llm'],254,L(42.1666667),'compact',[
        target('Large',L(17.88),lc[0],BLUE),
        target('Language',L(25.74),lc[1],TEAL),
        target('Model',L(33.30),lc[2],PURPLE)],push=False)
    def llm_rings(spec):
        spec['rings'][-1]['end']=L(38.4)-254
        spec['rings'].insert(0,ring(b,'llm',fr(14.12),527,
                         banner_rect(cv2.imread(str(ASSETS['llm'])))))
    update_spec(b,'llm',llm_rings)
    steps=[[60,168,400,665],[440,168,780,665],[820,168,1160,665],[1200,168,1540,665]]
    b.board('training',ASSETS['training'],L(47.6),L(97),'compact',[
        target('Read',L(51.48),steps[0],PURPLE),
        target('Guess',L(58.24),steps[1],BLUE),
        target('Check',L(74.38),steps[2],TEAL),
        target('Adjust',L(82.72),steps[3],GREEN)],push=False)
    b.board('training-summary',ASSETS['training'],L(106),L(115.1333333),
            'compact',[],push=False)
    b.board('patterns',ASSETS['patterns'],L(115.1333333),L(162.3),'compact',[
        target('One Familiar Pattern',L(120.14),pc[0],PURPLE),
        target('Patterns Are Everywhere',L(129.62),pc[1],TEAL)],push=False)
    update_spec(b,'patterns',lambda s:s['rings'][-1].update(end=L(138.18)-L(115.1333333)))
    b.board('odds-intro',ASSETS['odds'],PART2,A(12.8),'compact',[],push=False)
    odds=[[40,142,779,783],[820,142,1559,783]]
    prompts=[[79,169,741,334],[859,169,1520,334]]
    tables=[[62,367,756,754],[842,367,1536,754]]
    b.board('odds',ASSETS['odds'],A(26.2),A(108.3333333),'dense',[
        target('Left card',A(32.8),odds[0],PURPLE,odds[0]),
        target('Left prompt',A(35.78),prompts[0],PURPLE,odds[0]),
        target('Left probability table',A(38.08),tables[0],PURPLE,odds[0]),
        target('Right card',A(67.9),odds[1],TEAL,odds[1]),
        target('Right prompt',A(70.0),prompts[1],TEAL,odds[1]),
        target('Right probability table',A(73.1),tables[1],TEAL,odds[1])],
        pullback_at=A(84.96)/30,push=False)
    def odds_rings(spec):
        br=banner_rect(cv2.imread(str(ASSETS['odds'])))
        spec['rings'][2]['end']=A(64.26)-A(26.2)
        spec['rings'] += [ring(b,'odds',A(84.96),A(88.16),br),
                          ring(b,'odds',A(94.1),A(100.8),odds[0],PURPLE),
                          ring(b,'odds',A(94.1),A(100.8),odds[1],TEAL),
                          ring(b,'odds',A(100.8),A(108.3333333),br)]
        # Pan in the new-context introduction, before the right card is named.
        # Pull back before the takeaway so its edge-to-edge ring is never cropped.
        full=spec['beats'][0]['from']; left=spec['beats'][1]['to']
        right=next(v['to'] for v in spec['beats'] if v['label']=='to-Right card')
        start=A(26.2)
        spec['beats']=[dict(label='full-view',frames=A(32.8)-start,**{'from':full},to=full),
                       dict(label='to-left',frames=24,to=left),
                       dict(label='left-hold',frames=A(64.26)-A(32.8)-24,to=left),
                       dict(label='to-right',frames=24,to=right),
                       dict(label='right-hold',frames=A(84.96)-A(64.26)-24-30,to=right),
                       dict(label='pullback',frames=30,to=full),
                       dict(label='comparison',frames=A(108.3333333)-A(84.96),to=full)]
    update_spec(b,'odds',odds_rings)
    pred=[[40,158,486,455],[577,158,1023,455],[1114,158,1559,455]]
    b.board('prediction',ASSETS['prediction'],A(119.6),A(157.8666667),'compact',[
        target('First panel / jelly',A(122.64),pred[0],PURPLE),
        target('Second panel / for',A(131.84),pred[1],PURPLE),
        target('Third panel / lunch',A(142.72),pred[2],PURPLE)],
        banner_at=A(151.12)/30,push=False)
    b.make_close('aihistory')

    def row(end,label,visual,source=None,start=None,limit=None):
        begin=b.rows[-1]['end_frame'] if b.rows else 0
        r=dict(start_frame=begin,end_frame=end,label=label,visual=visual,kind='visual')
        if source:
            r.update(video_src=str(SOURCES[source]),video_start=start,
                     video_end=limit if limit is not None else start+end-begin)
        b.rows.append(r)
    row(254,'Peanut butter opening','source','learns-1',0)
    row(L(42.1666667),'Canonical LLM','llm')
    # Begin on an established loop, not the white first animation frame.
    row(L(47.6),'Training loop introduction','source','learns-1',1290,1522)
    row(L(97),'Read guess check adjust','training')
    row(L(106),'Training repetition drawing','source','learns-1',1290,1522)
    row(L(115.1333333),'Training summary','training-summary')
    row(L(162.3),'Learned patterns','patterns')
    row(PART2,'Learning to answering handoff','source','learns-2',5310,5443)
    row(A(12.8),'Answering introduction','odds-intro')
    row(A(17.04),'Incremental pieces','source','answers-1',570,711)
    # Stop before fabricated token IDs begin fading in.
    row(A(26.2),'Whole words and word fragments','source','answers-1',720,856)
    row(A(108.3333333),'Continuous context probability comparison','odds')
    row(A(119.6),'Prediction loop introduction and phone analogy','source','answers-2',4800,5139)
    row(A(157.8666667),'Predict choose update example','prediction')
    # Skip blank first animation frames; freeze before the thought label.
    row(A(177.1666667),'Repeated prediction loop','source','answers-2',4800,5251)
    row(CLOSE,'Training versus answering drawings','source','answers-2',5315,5749)
    row(TOTAL,'Canonical standard close','close')
    assert b.rows[-1]['end_frame']==TOTAL
    return b


class BoardRenderer:
    def __init__(self,path):
        self.spec=json.loads(path.read_text()); im=cv2.imread(self.spec['image'])
        self.ih,self.iw=im.shape[:2]; self.big=cv2.resize(im,(self.iw*3,self.ih*3),interpolation=cv2.INTER_LANCZOS4)
        self.beats=resolve(self.spec,16/9,1280,3); self.rings=rings_for(self.spec)
        self.lastkey=None; self.last=None

    def at(self,f):
        cur=0
        for label,n,a,z in self.beats:
            if f<cur+n:break
            cur+=n
        else:raise AssertionError(f)
        q=smoothstep((f-cur)/(n-1)) if n>1 else 1
        cam=tuple(a[j]+(z[j]-a[j])*q for j in range(3))
        active=tuple(i for i,r in enumerate(self.rings) if r[0]<=f<r[1])
        cachekey=(cam,active)
        if cachekey==self.lastkey:return self.last
        x,y,w,h=window(*cam,16/9,self.iw,self.ih)
        xx,yy,ww,hh=[round(v*3) for v in (x,y,w,h)]
        im=cv2.resize(self.big[yy:yy+hh,xx:xx+ww],(1280,720),interpolation=cv2.INTER_AREA)
        scale=1280/w
        for i in active:
            _,_,(rx,ry,rw,rh),col,pad,radius=self.rings[i]
            coords=((rx-pad-x)*scale-2.5,(ry-pad-y)*scale-2.5,
                    (rx+rw+pad-x)*scale+2.5,(ry+rh+pad-y)*scale+2.5)
            assert min(coords[:2])>=0 and coords[2]<1280 and coords[3]<720, (f,coords)
            draw_ring(im,*coords,col,radius*scale+2.5)
        self.lastkey,self.last=cachekey,im
        return im


def audio(b):
    arrays={}
    levels={n:float(json.loads((OUT/f'{n}-loudness.json').read_text())['input_i']) for n in SOURCES}
    # Align all voices to the quietest roll, then reserve headroom, never boost.
    gains={n:min(levels.values())-v for n,v in levels.items()}
    for n,p in SOURCES.items():
        wav=OUT/f'{n}.wav'
        if not wav.exists():subprocess.run([b.ff,'-y','-v','error','-i',str(p),'-vn','-ac','1','-ar',str(SR),str(wav)],check=True)
        arrays[n]=readwav(wav)*10**(gains[n]/20)
    spans=[('learns-1',0,527),('learns-2',590,725),('learns-1',527,5061),
           ('answers-2',0,1452),('answers-1',1820,2075),('answers-2',1452,5945)]
    parts=[]; timeline=[]; pos=0
    for n,s,e in spans:
        part=arrays[n][s*SPF:e*SPF].copy(); assert len(part)==(e-s)*SPF
        timeline.append(dict(source=str(SOURCES[n]),source_in=s,source_out=e,
                             start_frame=pos,end_frame=pos+e-s,gain_db=gains[n]))
        parts.append(part); pos+=e-s
    master=np.concatenate(parts)
    # A small, authentic low-level piece of the final pause, mirrored for continuity.
    seed=arrays['answers-2'][round(198.0*SR):round(198.1*SR)].copy(); seed-=seed.mean()
    tone=np.r_[seed,seed[::-1]]
    master=np.r_[master,np.resize(tone,(TOTAL-pos)*SPF)]
    joins=[r['start_frame'] for r in timeline[1:]]+[pos]
    ramp=np.linspace(0,1,240)
    for f in joins:
        at=f*SPF
        bed=np.resize(tone,480)
        master[at-240:at]=master[at-240:at]*(1-ramp)+bed[:240]*ramp
        master[at:at+240]=master[at:at+240]*ramp+bed[240:]*(1-ramp)
    peak=float(abs(master).max()); head=min(1,32767*10**(-2.5/20)/peak)
    master*=head
    writewav(OUT/'edited.wav',master)
    b.tone_meta=dict(sample_rate=SR,source_integrated_lufs=levels,relative_gains_db=gains,
                    final_headroom_gain_db=20*np.log10(head),peak_dbfs=20*np.log10(abs(master).max()/32767),
                    room_tone_source='answers-2 198.000–198.100',room_tone_rms=rms(seed)*head,
                    splice_ramp_ms=5,added_teaching_pauses=0,final_settle_fill_frames=TOTAL-pos,
                    timeline=timeline,join_frames=joins,
                    preservation='Uncut retained speech; constant per-roll gain; ramps only at actual audio joins.')
    b.grafts={'full-term':dict(source=str(SOURCES['learns-2']),source_frames=[590,725],output_frames=[527,662],audio_only=True),
              'illustrative-values':dict(source=str(SOURCES['answers-1']),source_frames=[1820,2075],output_frames=[6648,6903],audio_only=True)}


def previews(b):
    for key,board in b.boards.items():
        render=BoardRenderer(OUT/f'leg-{key}.json'); n=board['src_out']-board['src_in']
        want={0,n-1}
        want.update(min(n-1,r['start']+26) for r in board['rings'])
        out=OUT/'preview'/key; out.mkdir(exist_ok=True)
        cells=[]
        for f in sorted(want):
            im=render.at(f); cv2.imwrite(str(out/f'f{f:05d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,95])
            cell=cv2.resize(im,(640,360));cv2.putText(cell,f'{key} f{f}',(8,25),cv2.FONT_HERSHEY_SIMPLEX,.65,(0,0,200),2);cells.append(cell)
        if len(cells)%2:cells.append(np.zeros_like(cells[0]))
        cv2.imwrite(str(OUT/'preview'/f'{key}.jpg'),cv2.vconcat([cv2.hconcat(cells[i:i+2]) for i in range(0,len(cells),2)]))


def render(b, copy_audio_from=None):
    assert not DEST.exists(), f'Never overwrite a candidate: {DEST}'
    counts=dict(clone=0,inpaint=0,declined=[]); mask=glyph_mask()
    p=subprocess.Popen([b.ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
                        '-i',str(copy_audio_from or OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','medium',
                        '-pix_fmt','yuv420p',*(['-c:a','copy'] if copy_audio_from else ['-c:a','aac','-b:a','192k']),
                        '-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for row in b.rows:
        visual=row['visual']; start,end=row['start_frame'],row['end_frame']
        if visual=='source': reader=Reader(row['video_src']); last_idx=-1; last_im=None
        elif visual!='close': renderer=BoardRenderer(OUT/f'leg-{visual}.json')
        print(f'render {start/30:.2f}–{end/30:.2f}: {row["label"]}',flush=True)
        for f in range(start,end):
            if visual=='source':
                idx=min(row['video_start']+f-start,row['video_end']-1)
                if idx!=last_idx:
                    im,method=clean_frame(reader.at(idx),mask);last_im=im;last_idx=idx
                else:im=last_im
                if method:counts[method]+=1
                else:counts['declined'].append(f)
            elif visual=='close':
                ci=b.close_img;h,w=ci.shape[:2]
                q=np.clip((f-CLOSE-48)/149,0,1);z=1+.2*smoothstep(q);ww=w/z;hh=ww*9/16
                im=cv2.warpAffine(ci,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),
                                  (1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
            else:im=renderer.at(f-b.boards[visual]['src_in'])
            p.stdin.write(im.tobytes())
        if visual=='source':reader.c.release()
    p.stdin.close();assert p.wait()==0
    m=json.loads((OUT/'edit-manifest.json').read_text())
    m.update(render_sha256=sha(DEST),corner_mark=counts,
             protected_files_unchanged={p:sha(p)==h for p,h in b.hashes.items()})
    assert all(m['protected_files_unchanged'].values())
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
    print('Completed',DEST,TOTAL,'frames',flush=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    b=prepare();audio(b);previews(b)
    b.manifest(dict(scope_detail='Approved two-part narration repair, current canonical boards; review only.',
                    long_board_exception='Continuous probability comparison kept as approved; exact longest board run 90.6333s. Same approved loop drawing supports the prediction introduction before the next board.',
                    timing_coordinate_system='Board src_in/src_out and spoken_onset_source_frame are OUTPUT frames for this build.',
                    original_audio_join_frames=b.tone_meta['join_frames'],
                    helper_sha256=sha(ROOT/'scripts/video/editspec_build.py'),
                    literal_listening_performed=False))
    if not args.prepare_only:render(b)


if __name__=='__main__':main()

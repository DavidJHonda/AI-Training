#!/usr/bin/env python3
"""Approved v9: roll 5 + invitation from 7, established live graphics, current boards.

Build approval: 2026-10-26, following people-skills-rerolls-2026-10-26/REVIEW.md.
Source video and artwork remain untouched; candidate is versioned and not installed.
"""
from pathlib import Path
import argparse, json, subprocess, sys
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from editspec_build import Build, Reader, fr, sha, FPS, W, H, SR, SPF, PURPLE, BLUE, TEAL, AMBER, NEUTRAL
from ken_burns_path import resolve, rings_for, window, smoothstep, draw_ring, ring_px

OUT = ROOT / 'video-audit/people-skills-build-v9-2026-10-26'
SRC = ROOT / 'Prompts/people-skills-5.mp4'
DONOR = ROOT / 'Prompts/people-skills-7.mp4'
LIVE = ROOT / 'course-assets/people-skills/people-skills.mp4'
DEST = ROOT / 'Prompts/people-skills-v9.mp4'
A = ROOT / 'course-assets/people-skills'
PHOTOS = ROOT / 'video-audit/build-your-skills-illustration-updates-2026-10-08/assets'
FONT = ROOT / 'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
PHOTO_NAMES = ['people_start', 'people_suggest', 'people_interrupt', 'people_quiet']

class BoardPicture:
    """Use the house camera/ring math directly; cache settled states losslessly."""
    def __init__(self, spec):
        self.spec = spec
        self.image = cv2.imread(spec['image'])
        self.ih, self.iw = self.image.shape[:2]
        self.up = spec.get('upscale', 3)
        self.big = cv2.resize(self.image, (self.iw*self.up, self.ih*self.up), interpolation=cv2.INTER_LANCZOS4)
        self.beats = resolve(spec, W/H, W, self.up)
        self.rings = rings_for(spec)
        self.cache = {}
    def draw(self, f):
        at = 0
        for label,n,a,b in self.beats:
            if at <= f < at+n:
                t = smoothstep((f-at)/(n-1)) if n>1 else 1
                cam = [a[j]+(b[j]-a[j])*t for j in range(3)]
                break
            at += n
        else: raise ValueError(('board frame out of range', f, at))
        active = tuple(i for i,r in enumerate(self.rings) if r[0]<=f<r[1])
        key = tuple(round(x,8) for x in cam)+active
        if key in self.cache: return self.cache[key].copy()
        x,y,ww,hh = window(*cam, W/H, self.iw, self.ih)
        X,Y,CW,CH = [round(v*self.up) for v in (x,y,ww,hh)]
        crop = self.big[Y:Y+CH,X:X+CW]
        im = cv2.resize(crop,(W,H),interpolation=cv2.INTER_AREA if CW>W else cv2.INTER_LANCZOS4)
        scale = W/ww
        for i in active:
            _,_,(rx,ry,rw,rh),color,pad,radius = self.rings[i]
            half=ring_px(H)/2
            draw_ring(im,(rx-pad-x)*scale-half,(ry-pad-y)*scale-half,
                      (rx+rw+pad-x)*scale+half,(ry+rh+pad-y)*scale+half,
                      color,radius*scale+half,ring_px(H))
        # Cache only static states; transitions remain frame-accurate, without large storage.
        if a == b: self.cache[key] = im.copy()
        return im

class Picture:
    def __init__(self,m):
        self.m=m
        self.boards={k:BoardPicture(json.loads((OUT/f'leg-{k}.json').read_text())) for k in m['boards']}
        self.photos={name:ImageOps.fit(Image.open(PHOTOS/(name+'.png')).convert('RGB'),(W,H),method=Image.Resampling.LANCZOS) for name in PHOTO_NAMES}
        self.font=ImageFont.truetype(str(FONT),32)
        self.live=Reader(LIVE)
        self.close=cv2.imread(str(OUT/'close.png'))
        self.last=None
    def draw(self,row,f):
        k=f-row['start_frame']; n=row['end_frame']-row['start_frame']
        kind=row.get('visual','pause')
        if f>=self.m['close']['start_frame']:
            c=self.m['close']; q=np.clip((f-c['start_frame']-c['prehold'])/(c['push']-1),0,1)
            z=1+.2*q*q*(3-2*q);h,w=self.close.shape[:2];ww=w/z;hh=ww*H/W
            im=cv2.warpAffine(self.close,np.float32([[ww/W,0,(w-ww)/2],[0,hh/H,(h-hh)/2]]),(W,H),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
        elif row['kind']=='room_tone':
            assert self.last is not None
            im=self.last.copy()
        elif kind in self.boards:
            at=row.get('video_start',row['source_start'])+k-self.m['boards'][kind]['src_in']
            im=self.boards[kind].draw(at)
        elif kind=='live':
            a,b=row['live_frames']
            idx=a+round(k*(b-a-1)/max(n-1,1))
            im=self.live.at(idx)
        elif kind.startswith('photo:'):
            name=kind.split(':',1)[1]; pic=self.photos[name]
            z=1+.025*k/max(n-1,1);cw,ch=W/z,H/z;x=(W-cw)*.7;y=(H-ch)*.35
            pic=pic.crop((x,y,x+cw,y+ch)).resize((W,H),Image.Resampling.LANCZOS)
            sf=row['source_start']+k
            if name=='people_interrupt' and sf>=fr(10.94):
                d=ImageDraw.Draw(pic);d.rounded_rectangle((42,572,705,685),radius=15,fill='#f8f6ed')
                d.text((64,580),'“We are done.”',font=self.font,fill='#203335')
                if sf>=fr(11.82):d.text((64,630),'“No more suggestions.”',font=self.font,fill='#203335')
            im=cv2.cvtColor(np.array(pic),cv2.COLOR_RGB2BGR)
        else:raise ValueError(kind)
        self.last=im.copy()
        return im

def prepare():
    assert not DEST.exists(),f'{DEST} already exists; do not overwrite review candidates'
    OUT.mkdir(parents=True,exist_ok=True)
    protected=[DONOR,LIVE,*A.glob('*.jpg'),*(PHOTOS/(name+'.png') for name in PHOTO_NAMES),ROOT/'lessons/people-skills.md']
    b=Build(ROOT,SRC,OUT,DEST,protected=protected)
    b.load_audio([(23.90,24.25),(30.95,31.35),(77.75,78.20),(88.50,88.90),(150.85,151.55)])
    def keep(a,z,label,visual,**extra):
        b.keep(fr(a),fr(z),label,visual);b.rows[-1].update(extra)
    keep(0,3.13,'Finished history project','photo:people_start')
    keep(3.13,8,'Maya suggests a change','photo:people_suggest')
    keep(8,13.2,'Interruption with retimed dialogue','photo:people_interrupt')
    keep(13.2,21.77,'Maya goes quiet; she seems hurt','photo:people_quiet')
    keep(21.77,23.97,'What would you say? Establish Your Next Move','nm',video_start=fr(34.70))
    b.graft(DONOR,fr(36.90),fr(45.43),'Roll 7 invitation and acknowledgment','invitation',
            picture_from=fr(36.90),gain_db=-.75,visual='nm')
    keep(31.13,42.7,'Maya identifies the third-example error','live',live_frames=[fr(35.70),fr(40.53)])
    keep(42.7,50.2,'Hear her even if unused; bridge beyond the project','photo:people_suggest')
    keep(50.2,65.74,'Future: Stand Out and Trust title','mm')
    keep(65.74,70.4,'Trust: live team scene','live',live_frames=[fr(40.53),fr(47.83)])
    keep(70.4,77.93,'Future: Connection','mm')
    # Approved removal: repeated professional-differentiator summary, 77.93–88.67.
    keep(88.67,104.76,'Starting today; Listen and Notice title','fw')
    keep(104.76,113.5,'Notice cues and ask: retained live diagram','live',live_frames=[fr(66.3666667),fr(74.7666667)])
    keep(113.5,124.72,'Show people they matter; Challenge title','fw')
    keep(124.72,129.4,'Calm concern and solution: retained live diagram','live',live_frames=[fr(87.90),fr(94.7666667)])
    keep(129.4,133.03,'Challenge: the full new worked example','fw')
    # Approved removal: abstract summary and repeated scenario setup, 133.03–146.63.
    keep(146.63,151.2,'Give Maya credit: learner question','photo:people_suggest')
    b.pause(65,'Maya question: add 2.167 seconds for 3.0 seconds total thinking time')
    # Approved removal: added drafting/data sentence, 151.20–157.37.
    b.make_close('peopleskills')
    b.close(fr(157.37),fr(165.80),tail=120)
    b.finish_audio()
    b.board('nm',A/'people-skills-why-people-matter.jpg',fr(34.70),fr(45.43),'compact',
            [dict(label='invitation bubble',at=38.78,rects=[[587,187,1083,378]],color=NEUTRAL,radius=22)],
            banner_at=42.66,banner=[34,1073,1566,1160],push=False)
    mm=[[40,127,526,733],[557,127,1043,733],[1075,127,1560,733]]
    b.board('mm',A/'people-skills-matter-more.jpg',fr(50.2),fr(77.93),'compact',
            [dict(label=label,at=at,rects=[r],color=color) for label,at,r,color in zip(
                ['You’ll Stand Out','Trust Still Matters','Connection Matters'],[53.98,63.60,71.10],mm,[PURPLE,BLUE,TEAL])],push=False)
    fw=[[40,127,784,759],[816,127,1560,759],[40,790,784,1422],[816,790,1560,1422]]
    targets=[dict(label=label,at=at,rects=[r],cam=r,color=color) for label,at,r,color in zip(
        ['Listen to Understand','Notice What Isn’t Being Said','Show People They Matter','Challenge Ideas, Not People'],
        [93.70,103.08,114.04,121.98],fw,[PURPLE,BLUE,TEAL,AMBER])]
    targets[2]['camera_at']=113.5
    b.board('fw',A/'people-skills-four-ways.jpg',fr(88.67),fr(133.03),'dense',targets,lead_camera=True)
    m=b.manifest(dict(
        approval='User approved roll 5, short roll 7 passage, maximum reuse of live graphics, and the proposed edits/pause on 2026-10-26.',
        scope_detail='Approved review candidate; no installation, commit, or publication.',
        source_audio_loudness=dict(base_lufs=-20.28,donor_lufs=-19.53,donor_gain_db=-.75),
        removed_source_seconds=[[23.97,31.13],[77.93,88.67],[133.03,146.63],[151.2,157.37]],
        visual_reuse='All visuals use existing live-video artwork/footage, current canonical boards, or the standard close; no new-roll scene footage.',
        thinking_pause=dict(source_question_end_detected=150.722834,source_close_onset_detected=157.728594,added_frames=65,target_total_seconds=3.0),
        direct_listening_performed=False,continuous_playback_performed=False))
    # Record every visual change, audio edit, highlight onset, and caption reveal on OUTPUT time.
    boundaries={r['start_frame']:r['label'] for r in b.rows[1:]}
    for row in b.rows:
        key=row.get('visual')
        if key in b.boards:
            sf=row.get('video_start',row['source_start']);end=sf+row['end_frame']-row['start_frame']
            for state in b.boards[key]['states']:
                t=state['spoken_onset_source_frame']
                if sf<=t<end:boundaries[row['start_frame']+t-sf]='Highlight: '+state['highlight_target']
    for t in [10.94,11.82]:boundaries[fr(t)]='Interruption caption'
    m['declared_boundaries']=[dict(frame=k,label=v) for k,v in sorted(boundaries.items())]
    m['longest_unbroken_content_board_seconds']=max((r['end_frame']-r['start_frame'])/FPS for r in b.rows if r.get('visual') in b.boards)
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    print(f'Prepared {b.total} frames, {b.total/FPS:.3f}s; {len(b.rows)} timeline rows',flush=True)
    return m

def previews(m):
    d=OUT/'preview';d.mkdir(exist_ok=True)
    wanted={0,m['total_frames']-1}
    wanted.update(range(0,m['total_frames'],120))
    for x in m['declared_boundaries']:
        wanted.update([max(0,x['frame']-1),min(m['total_frames']-1,x['frame']+25)])
    pic=Picture(m);ri=0
    for f in range(m['total_frames']):
        while f>=m['timeline'][ri]['end_frame']:ri+=1
        # Render sequentially for live Reader and pause holds.
        im=pic.draw(m['timeline'][ri],f)
        if f in wanted:cv2.imwrite(str(d/f'f{f:05d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,94])
    print('Rendered source-plan preview frames',flush=True)

def render(m):
    assert not DEST.exists(),DEST
    from imageio_ffmpeg import get_ffmpeg_exe
    ff=get_ffmpeg_exe();pic=Picture(m);ri=0
    with (OUT/'encode.log').open('w') as log:
        p=subprocess.Popen([ff,'-v','warning','-f','rawvideo','-pix_fmt','bgr24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0',
            '-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-threads','4','-crf','18','-preset','medium',
            '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE,stderr=log)
        for f in range(m['total_frames']):
            while f>=m['timeline'][ri]['end_frame']:ri+=1
            p.stdin.write(pic.draw(m['timeline'][ri],f).tobytes())
            if f%900==0:print(f'Rendering {f}/{m["total_frames"]} frames',flush=True)
        p.stdin.close();assert p.wait()==0,'ffmpeg render failed'
    m['render_sha256']=sha(DEST)
    m['protected_files_unchanged']={k:sha(k)==v for k,v in m['protected_hashes'].items()}
    assert all(m['protected_files_unchanged'].values())
    m['status']='Built review candidate; encoded QA pending'
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    print('BUILT',DEST,flush=True)

if __name__=='__main__':
    cv2.setNumThreads(2)
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');ap.add_argument('--render-prepared',action='store_true');ap.add_argument('--preview',action='store_true');args=ap.parse_args()
    m=json.loads((OUT/'edit-manifest.json').read_text()) if args.render_prepared else prepare()
    if args.preview:previews(m)
    if not args.prepare_only:render(m)

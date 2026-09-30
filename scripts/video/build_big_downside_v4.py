#!/usr/bin/env python3
"""Approved narrow repair of the verified September 24 live render.

Raw rolls no longer exist locally. Recover the exact committed finished source
to /private/tmp; assert its hash. Remove the callback's overclaim and replace
the off-topic historical introduction. Never install or publish this candidate.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, Reader, readwav, writewav, sha, SR, SPF
from ken_burns_path import draw_ring, ring_px, hex_bgr

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/big-downside-repair-2026-09-30-v4'
DEST = ROOT / 'Prompts/big-downside-v4.mp4'
SRC = Path('/private/tmp/big-downside-83ecf2e1-source.mp4')
EXPECTED = '83ecf2e1a9de491260981d6048ce792657a478cfcfe6be13ad71d4314fc902d4'
SOURCE_REV = 'a81bf97a'
LIVE = ROOT / 'course-assets/big-downside/big-downside.mp4'
BOARD = ROOT / 'course-assets/big-downside/big-downside-voice-cloning.jpg'
HISTORY = ROOT / 'scripts/video/assets/big-downside-history-2026-09-30/technology-history.png'
N = 10149
CUT_A, CUT_B = 5414, 5444  # Picture frame deletion. Audio split independently at low-energy boundaries.
AUDIO_A, AUDIO_B = 180.430, 181.430
DROP = CUT_B-CUT_A
TOTAL = N-DROP
VOICE_A, VOICE_B = 4852, 5565-DROP
HISTORY_A, HISTORY_B = 7538-DROP, 7735-DROP
COLS = [[40,127,420,711],[420,127,800,711],[800,127,1180,711],[1180,127,1560,711]]
ONSETS = [4947,5061,5256,CUT_A]
COLORS = ['#4f2fc4','#1652f0','#c41f28','#0e8f86']


def prepare():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'preview').mkdir(exist_ok=True)
    if not SRC.exists():
        with SRC.open('wb') as f:
            subprocess.run(['git','show',SOURCE_REV+':course-assets/big-downside/big-downside.mp4'],cwd=ROOT,stdout=f,check=True)
    assert sha(SRC)==EXPECTED and sha(LIVE)==EXPECTED
    b=Build(ROOT,SRC,OUT,DEST,protected=[LIVE,BOARD,HISTORY])
    if not (OUT/'source.wav').exists():
        subprocess.run([b.ff,'-v','error','-y','-i',str(SRC),'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',str(OUT/'source.wav')],check=True)
    a=readwav(OUT/'source.wav')[:N*SPF]
    ia,ib=round(AUDIO_A*SR),round(AUDIO_B*SR)
    left,right=a[:ia].copy(),a[ib:].copy()
    # Ramps affect only 5ms either side of this one edit. Visual boundaries never fade audio.
    room=a[round(180.35*SR):round(180.40*SR)]
    bed=np.resize(room,240); ramp=np.linspace(0,1,240)
    left[-240:]=left[-240:]*(1-ramp)+bed*ramp
    right[:240]=right[:240]*ramp+bed*(1-ramp)
    edited=np.r_[left,right]
    assert len(edited)==TOTAL*SPF
    writewav(OUT/'edited.wav',edited)
    writewav(OUT/'callback-after.wav',edited[174*SR:187*SR])
    canvas,cw,ch,ox,oy=b.compose(BOARD,'voice')
    board=cv2.resize(cv2.imread(str(canvas)),(1280,720),interpolation=cv2.INTER_AREA)
    # Source image itself is untouched. The typography is a separate video overlay.
    history=cv2.resize(cv2.imread(str(HISTORY)),(1280,720),interpolation=cv2.INTER_AREA)
    overlays=[]
    font=ImageFont.truetype(str(ROOT/'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'),42)
    for text,y in [('New technology arrives.',40),('Safeguards follow.',96)]:
        layer=Image.new('RGBA',(1280,720),(0,0,0,0)); d=ImageDraw.Draw(layer)
        bbox=d.textbbox((0,0),text,font=font); x=(1280-(bbox[2]-bbox[0]))//2
        d.text((x,y),text,font=font,fill=(27,33,83,255))
        arr=np.array(layer);overlays.append((cv2.cvtColor(arr[:,:,:3],cv2.COLOR_RGB2BGR),arr[:,:,3:4].astype(float)/255))
    return b,a,edited,board,(cw,ch,ox,oy),history,overlays


def draw_board(base,f,geom):
    im=base.copy();cw,ch,ox,oy=geom
    active=next((i for i in reversed(range(4)) if f>=ONSETS[i]),None)
    if active is not None:
        x0,y0,x1,y1=COLS[active]; sx,sy=1280/cw,720/ch; half=ring_px(720)/2
        draw_ring(im,(x0+ox)*sx-half,(y0+oy)*sy-half,(x1+ox)*sx+half,(y1+oy)*sy+half,hex_bgr(COLORS[active]),18*sx+half,ring_px(720))
    return im


def draw_history(base,f,overlays):
    im=base.copy();k=f-HISTORY_A
    for i,(rgb,alpha) in enumerate(overlays):
        opacity=np.clip((k-(0 if i==0 else 62))/12,0,1)
        blend=alpha*opacity
        im=np.clip(im*(1-blend)+rgb*blend,0,255).astype(np.uint8)
    return im


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    b,a,edited,board,geom,history,overlays=prepare()
    protected={str(p):sha(p) for p in [LIVE,BOARD,HISTORY]}
    boundaries=[dict(frame=VOICE_A,label='canonical voice board'),dict(frame=CUT_A,label='callback audio deletion and Call Back ring'),dict(frame=VOICE_B,label='resume original supporting scene'),dict(frame=HISTORY_A,label='historical technology insert'),dict(frame=HISTORY_B,label='resume canonical safety timeline')]
    manifest=dict(output=str(DEST),source=str(SRC),source_git_revision=SOURCE_REV,source_sha256=EXPECTED,source_limitation='Only finished render survives locally; source recovered from Git, one additional video/AAC encode.',approval='User: Make the repairs please. Continues evaluation plan; no shipping approval.',fps=30,total_frames=TOTAL,duration=TOTAL/30,boundaries=boundaries,source_video_spans=[[0,CUT_A],[CUT_B,N]],audio=dict(cut_seconds=[AUDIO_A,AUDIO_B],removed_words='The only defense is',retained_words='Step four. Hang up and call the person back on the real number.',crossfade_ms=5,sample_rate=SR,added_pauses=False,other_PCM_unchanged=True),voice_board=dict(asset=str(BOARD),source_span=[4852,5565],output_span=[VOICE_A,VOICE_B],highlight_onsets=ONSETS,ring_px=4,full_view=True),history=dict(asset=str(HISTORY),sha256=sha(HISTORY),source_span=[7538,7735],output_span=[HISTORY_A,HISTORY_B],tool='Built-in image_gen',overlay=['New technology arrives.','Safeguards follow.']),close=dict(output_start_frame=9838-DROP,unchanged_source_frames=True),remaining='Missing historical dates, tested-model scope, goal-line article and pacing qualification have no available donor audio. Listening and full motion sign-off remain unperformed.')
    for f in [VOICE_A,4947+15,5061+15,5256+15,CUT_A+15,VOICE_B-1]:cv2.imwrite(str(OUT/'preview'/f'{f:06d}.jpg'),draw_board(board,f,geom))
    for f in [HISTORY_A,HISTORY_A+30,HISTORY_A+90,HISTORY_B-1]:cv2.imwrite(str(OUT/'preview'/f'{f:06d}.jpg'),draw_history(history,f,overlays))
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    if args.prepare_only:return
    assert not DEST.exists(),'Use a new candidate version; never overwrite.'
    proc=subprocess.Popen([b.ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','medium','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    reader=Reader(SRC)
    for f in range(TOTAL):
        sf=f if f<CUT_A else f+DROP
        source=reader.at(sf)
        if VOICE_A<=f<VOICE_B:im=draw_board(board,f,geom)
        elif HISTORY_A<=f<HISTORY_B:im=draw_history(history,f,overlays)
        else:im=source
        proc.stdin.write(im.tobytes())
        if f%900==0:print('Rendered',f,'/',TOTAL,flush=True)
    reader.c.release();proc.stdin.close();assert proc.wait()==0
    manifest.update(render_sha256=sha(DEST),protected_files_unchanged={p:sha(p)==h for p,h in protected.items()})
    assert all(manifest['protected_files_unchanged'].values())
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('COMPLETE',DEST,TOTAL/30,flush=True)


if __name__=='__main__':main()

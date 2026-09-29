#!/usr/bin/env python3
"""Approved visual-only repair; copy v7 audio and preserve its output timeline."""
from pathlib import Path
import argparse, json, subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
from editspec_build import Build, sha
from build_embeddings_v7 import Renderer

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT/'course-assets/embeddings/embeddings.mp4'
DEST = ROOT/'Prompts/embeddings-v8.mp4'
OUT = ROOT/'video-audit/embeddings-repair-2026-09-29-v8'
OLD = ROOT/'video-audit/embeddings-repair-2026-09-27-v7'
EXPECTED = '14d9ba4b66ee5a698eaa5845e7ec08b931d5de33f93a5d798c92a486637dca94'
FRAMES = 7997
TASTE = (1475,1930)
DIAGRAM = (4116,4303)
BOARD = (4303,5771)
cv2.setNumThreads(2)

def diagram(im):
    """Repair only the two static ribbon labels; retain lower animated scene."""
    ans=im.copy()
    # Remove sixth-value circles and their overlapped glyphs; leave ribbon
    # texture and the existing shared-dimension yellow line outside the mask.
    for rect,xy in [((770,106,859,168),(787,123)),((771,210,862,268),(787,228))]:
        x0,y0,x1,y1=rect
        patch=ans[y0:y1,x0:x1].copy()
        mask=(patch.max(axis=2)<125).astype(np.uint8)*255
        mask=cv2.dilate(mask,np.ones((3,3),np.uint8))
        repaired=cv2.inpaint(patch,mask,4,cv2.INPAINT_TELEA)
        ans[y0:y1,x0:x1]=repaired
        # Reconstruct only the small original numeric label hidden by the circle.
        pil=Image.fromarray(cv2.cvtColor(ans,cv2.COLOR_BGR2RGB))
        draw=ImageDraw.Draw(pil)
        font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',27)
        draw.text(xy,'0.55,',font=font,fill=(24,29,24),anchor='lt')
        ans=cv2.cvtColor(np.asarray(pil),cv2.COLOR_RGB2BGR)
    # Seventh coordinates, not the matching sixth coordinates, separate rows.
    cv2.ellipse(ans,(909,136),(45,22),-2,0,360,(24,29,24),3,cv2.LINE_AA)
    cv2.ellipse(ans,(909,244),(47,23),0,0,360,(24,29,24),3,cv2.LINE_AA)
    return ans

def taste(im):
    # Extra label stays in this otherwise empty paper corner for the scene.
    # Clone neighboring paper at the same height, preserving its texture.
    ans=im.copy()
    ans[661:713,1175:1275]=im[661:713,1070:1170]
    return ans

def setup():
    assert sha(SRC)==EXPECTED
    OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
    b=Build(ROOT,SRC,OUT,DEST)
    meta=json.loads((OLD/'edit-manifest.json').read_text())
    asset=ROOT/meta['boards']['bd4']['asset']
    assert sha(asset)==meta['boards']['bd4']['sha256']
    canvas,cw,ch,ox,oy=b.compose(asset,'comparison')
    assert [ox,oy]==meta['boards']['bd4']['canvas_offset']
    spec=json.loads((OLD/'leg-bd4.json').read_text());spec['image']=str(canvas)
    full=[cw/2,ch/2,float(cw)]
    closer=[cw/2,ch/2,cw*.96]
    spec['beats']=[dict(label='complete-board restrained push',frames=900,**{'from':full,'to':closer}),
                   dict(label='complete-board hold',frames=BOARD[1]-BOARD[0]-900,to=closer)]
    # Full canonical asset remains inside even the tightest crop.
    assert (cw*.96*9/16)>=cv2.imread(str(asset)).shape[0]
    (OUT/'comparison-spec.json').write_text(json.dumps(spec,indent=2)+'\n')
    return Renderer(spec),meta

def changed(i):
    return any(a<=i<b for a,b in [TASTE,DIAGRAM,BOARD])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    renderer,old=setup()
    protected=[SRC,ROOT/'lessons/embeddings.md',*sorted((ROOT/'course-assets/embeddings').glob('*.jpg'))]
    hashes={str(p):sha(p) for p in protected}
    wanted={1470,1500,1620,1929,4116,4128,4140,4152,4176,4200,4302,4303,
            4400,4648,4888,5068,5377,5583,5700,5770,7635,7996}
    ff=imageio_ffmpeg.get_ffmpeg_exe();proc=None
    if not args.prepare_only:
        assert not DEST.exists(),'Never overwrite a review candidate'
        proc=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
            '-i',str(SRC),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16',
            '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    cap=cv2.VideoCapture(str(SRC));i=0
    while True:
        ok,im=cap.read()
        if not ok:break
        if TASTE[0]<=i<TASTE[1]:im=taste(im)
        elif DIAGRAM[0]<=i<DIAGRAM[1]:im=diagram(im)
        elif BOARD[0]<=i<BOARD[1]:im=renderer.at(i-BOARD[0])[0]
        if i in wanted:cv2.imwrite(str(OUT/'preview'/f'{i:05d}.jpg'),im)
        if proc:proc.stdin.write(im.tobytes())
        i+=1
        if i%1500==0:print('Frames',i,flush=True)
    cap.release();assert i==FRAMES
    if proc:proc.stdin.close();assert proc.wait()==0
    assert all(sha(Path(p))==h for p,h in hashes.items())
    manifest=dict(source=str(SRC),source_sha256=EXPECTED,candidate=str(DEST),frames=i,fps=30,
      duration=i/30,scope='User approved build of reviewed targeted visual repairs. No narration or timing changes. Not shipping.',
      changed_spans=[dict(start=a,end=b) for a,b in [TASTE,DIAGRAM,BOARD]],
      boundaries=sorted(set([*old['boundaries'],*TASTE,*DIAGRAM,*BOARD])),
      source_limitation='Finished v7 is the source; raw embeddings-1/2 rolls are absent. Comparison board rendered from canonical JPG.',
      audio='Original AAC stream copied with -c:a copy; no new audio joins.',protected=hashes,
      unperformed='Continuous perceptual audio/motion review; existing audio joins remain unverified.',
      optional_cutaways='Not included: review identified no approved concrete donor or new scene.')
    if proc:manifest['render_sha256']=sha(DEST)
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Prepared' if args.prepare_only else DEST,flush=True)

if __name__=='__main__':main()

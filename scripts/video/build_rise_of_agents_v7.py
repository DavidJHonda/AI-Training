#!/usr/bin/env python3
"""Update Rogue Agents artwork and remove the universal review rule in one source encode."""
import json, subprocess
import cv2, numpy as np
from PIL import Image, ImageDraw
import build_rise_of_agents_v6 as base
from render_rise_of_agents_rogue import QUOTE
from render_embrace_editorial_batch import FRAME

ROOT,SRC,BOARD,FF,FPS,RATE,N,EXPECTED = (getattr(base,k) for k in ('ROOT','SRC','BOARD','FF','FPS','RATE','N','EXPECTED'))
sha,wav=base.sha,base.wav
OUT=ROOT/'video-audit/rise-of-agents-repair-2026-09-30-v7'
DEST=ROOT/'Prompts/rise-of-agents-v7.mp4'
CUTS=[(4414,4749),(4901,5088)]
TOTAL=N-sum(z-a for a,z in CUTS)

def removed(f):return any(a<=f<z for a,z in CUTS)
def output_frame(f):return f-sum(max(0,min(f,z)-a) for a,z in CUTS if f>a)

def board_frames():
    im=cv2.imread(str(BOARD));h,w=im.shape[:2]
    scale=min(1240/w,680/h);bw,bh=round(w*scale),round(h*scale)
    ox,oy=(1280-bw)//2,(720-bh)//2
    rgb=Image.new('RGB',(1280,720),FRAME)
    canvas=cv2.cvtColor(np.array(rgb),cv2.COLOR_RGB2BGR)
    canvas[oy:oy+bh,ox:ox+bw]=cv2.resize(im,(bw,bh),interpolation=cv2.INTER_AREA)
    ring=Image.fromarray(cv2.cvtColor(canvas,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(ring)
    rect=tuple(round(v*scale+(ox if i%2==0 else oy)) for i,v in enumerate(QUOTE))
    d.rounded_rectangle(rect,radius=11,outline='#6e51ff',width=4)
    return canvas,cv2.cvtColor(np.asarray(ring),cv2.COLOR_RGB2BGR),dict(density='compact',scale=scale,offset=[ox,oy],size=[bw,bh],quote_rect=rect,stroke_px=4,ring_color='#6e51ff',camera='Full board, no crop or zoom; quote banner ring at spoken onset.')

def main():
    cv2.setNumThreads(2)
    assert sha(SRC)==EXPECTED
    assert not DEST.exists(),'Never overwrite a review candidate'
    OUT.mkdir(parents=True,exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
    protected={str(p):sha(p) for p in [SRC,BOARD,ROOT/'index.html',ROOT/'lessons/rise-of-agents.md']}
    pcm=subprocess.check_output([FF,'-v','error','-i',str(SRC),'-vn','-ac','1','-ar',str(RATE),'-f','s16le','-'])
    a=np.frombuffer(pcm,dtype='<i2').astype(np.float64)[:N*1600]
    parts=[];start=0
    for lo,hi in CUTS:parts.append(a[start*1600:lo*1600]);start=hi
    parts.append(a[start*1600:]);edited=np.concatenate(parts)
    joins=[output_frame(lo) for lo,hi in CUTS]
    for j in joins:
        p=j*1600;edited[p-96:p+96]=np.linspace(edited[p-96],edited[p+95],192)
        wav(OUT/f'join-{j}-context.wav',edited[(j-100)*1600:(j+140)*1600])
    assert len(edited)==TOTAL*1600
    wav(OUT/'edited.wav',edited)
    board,ring,geom=board_frames()
    # Remove all review-rule imagery, including its visual lead and tail in the
    # retained silence. Hold the preceding warning and introduce the next scene.
    c=cv2.VideoCapture(str(SRC));c.set(cv2.CAP_PROP_POS_FRAMES,5095);ok,next_scene=c.read();c.release();assert ok
    decode=subprocess.Popen([FF,'-v','error','-threads','2','-i',str(SRC),'-an','-f','rawvideo','-pix_fmt','bgr24','pipe:1'],stdout=subprocess.PIPE)
    temp=OUT/'rendering.mp4';assert not temp.exists()
    encode=subprocess.Popen([FF,'-v','warning','-f','rawvideo','-pixel_format','bgr24','-video_size','1280x720','-framerate','30','-i','pipe:0','-i',str(OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-threads','2','-preset','fast','-crf','16','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(temp)],stdin=subprocess.PIPE)
    count=0;warning=None
    wants={3633,3800,3885,4110,4160,4283,4300,4413,4749,4759,4898,4899,4900,5088,5094,5095,5633}
    for f in range(N):
        buf=decode.stdout.read(1280*720*3);assert len(buf)==1280*720*3
        if removed(f):continue
        frame=np.frombuffer(buf,np.uint8).reshape(720,1280,3)
        if f==4898:warning=frame.copy()
        if 3633<=f<3885:frame=board
        elif 3885<=f<4283:frame=base.patch_scene(frame,f)
        elif 4283<=f<4759:frame=ring if f>=4286 else board
        elif 4899<=f<4901:frame=warning
        elif 5088<=f<5095:frame=next_scene
        if f in wants:cv2.imwrite(str(OUT/'preview'/f'source-{f:06d}-output-{count:06d}.jpg'),frame)
        encode.stdin.write(frame.tobytes());count+=1
        if f%900==0:print(f'Rendered source {f/30:.0f}s',flush=True)
    decode.stdout.close();assert decode.wait()==0
    encode.stdin.close();assert encode.wait()==0 and count==TOTAL
    assert all(sha(p)==h for p,h in protected.items()),'Source or lesson changed during build'
    temp.rename(DEST)
    boundaries=[3633,3885,4283,joins[0],output_frame(4759),joins[1],output_frame(5095)]
    m=dict(candidate=str(DEST),candidate_sha256=sha(DEST),source=str(SRC),source_sha256=EXPECTED,
        source_limitation='Only finished v4 survives; decoded once and final H264 encoded once at CRF16. Earlier repair candidates are not chained.',
        approval='User requested removal of the review-first line from lesson and video, plus redesigned Rogue Agents board.',fps=30,total_frames=TOTAL,duration=TOTAL/30,
        cuts=[dict(source_frames=[lo,hi],source_seconds=[lo/30,hi/30],output_join_frame=output_frame(lo),reason=reason) for (lo,hi),reason in zip(CUTS,['Previously approved withdrawal of Gemini story','Remove AI should not send, spend, submit, delete, or post without you reviewing first.'])],
        picture_changes=[dict(source_frames=[3633,3885],kind='compact canonical board'),dict(source_frames=[3885,4283],kind='previous label corrections preserving animation'),dict(source_frames=[4283,4759],kind='compact board with quote banner ring, excluding removed interval'),dict(source_frames=[4899,5095],kind='remove review-rule illustrations; bridge retained quiet edges')],
        boundary_frames=boundaries,boundary_labels=['compact board in','PocketOS animation','quote banner board','Gemini removal join','goal warning','advanced tools join','advanced tools motion resumes'],board=geom,board_sha256=sha(BOARD),
        audio=dict(rate=RATE,channels=1,join_smoothing_ms=4,added_pauses=False,gain_changes=False,listening='Not directly auditioned; join context supplied'),protected_hashes=protected,
        scope='Review candidate; canonical MP4 and lesson video reference unchanged. Lesson text, current board and prep sources updated.')
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    print('COMPLETE',DEST,TOTAL/30,flush=True)

if __name__=='__main__':main()

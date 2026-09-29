#!/usr/bin/env python3
"""Remove the approved repeated explanation; highlight the returning takeaway immediately."""
from pathlib import Path
import json,subprocess,wave,hashlib
import cv2,numpy as np,imageio_ffmpeg
from editspec_build import Build,Reader,sha
from build_embeddings_v7 import Renderer
from gemini_mark import clean_frame,glyph_mask
from build_what_is_ai_v9 import history,movie,label_erase,text

ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'Prompts/what-is-ai-5.mp4'
PREV=ROOT/'video-audit/what-is-ai-build-2026-09-29-v10'
OUT=ROOT/'video-audit/what-is-ai-build-2026-09-29-v11'
DEST=ROOT/'Prompts/what-is-ai-v11.mp4'
CUT=(630,1440)
KEEP=[(0,630),(1440,5477)]
FRAMES=[f for a,b in KEEP for f in range(a,b)]
SR=44100
SPF=1470

def main():
    assert not DEST.exists(),'Never overwrite an existing candidate'
    OUT.mkdir(exist_ok=True);(OUT/'preview').mkdir(exist_ok=True)
    old=json.loads((PREV/'edit-manifest.json').read_text())
    assert sha(SRC)==old['source_sha256']
    b=Build(ROOT,SRC,OUT,DEST)
    renderers={};specs={}
    for key,meta in old['boards'].items():
        asset=ROOT/meta['asset'];assert sha(asset)==meta['sha256']
        canvas,_,_,ox,oy=b.compose(asset,key);assert [ox,oy]==meta['canvas_offset']
        spec=json.loads((PREV/f'leg-{key}.json').read_text());spec['image']=str(canvas)
        if key=='desk':
            # The definition is now this board's first appearance. No stale list ring.
            spec['rings']=[spec['rings'][-1]]
        if key=='picks-summary':spec['rings'][0]['start']=0
        (OUT/f'leg-{key}.json').write_text(json.dumps(spec,indent=2)+'\n')
        renderers[key]=Renderer(spec);specs[key]=spec
    close=json.loads((PREV/'leg-close.json').read_text())
    renderers['close']=Renderer(close);specs['close']=close
    intervals=old['board_intervals']
    starts={k:v['src_in'] for k,v in old['boards'].items()};starts['close']=5138
    tracking={f:boxes[0][0]-544 for f,boxes in json.loads((PREV/'movie-tracking.json').read_text())}
    keyboard=cv2.resize(cv2.imread(str(PREV/'assets/keyboard-clean.png')),(1280,720),interpolation=cv2.INTER_AREA)
    mask=glyph_mask();corner={'clone':0,'inpaint':0,'declined':[]}
    def visual(sf,im):
        for a,z,key in intervals:
            if a<=sf<z:return renderers[key].at(sf-starts[key])[0]
        if 1928<=sf<2094:
            scale=1+.025*(sf-1928)/165
            return cv2.warpAffine(keyboard,np.float32([[scale,0,640*(1-scale)],[0,scale,360*(1-scale)]]),(1280,720),flags=cv2.INTER_CUBIC)
        if 1752<=sf<1928:im=history(im,sf)
        if 2955<=sf<3075:label_erase(im,(440,553,400,40),(440,615))
        if 3250<=sf<3480:
            label_erase(im,(220,43,850,43),(220,0))
            im=text(im,'Examples of Generative AI',(640,66),29,(28,50,67),True)
        if 4061<=sf<4374:im=movie(im,sf,tracking)
        im,how=clean_frame(im,mask)
        if how:corner[how]+=1
        else:corner['declined'].append(sf)
        return im
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    wav=OUT/'source-native.wav'
    subprocess.run([ff,'-v','error','-i',str(SRC),'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',str(wav)],check=True)
    with wave.open(str(wav)) as w:audio=np.frombuffer(w.readframes(w.getnframes()),np.int16)
    needed=5477*SPF
    # AAC can end a fraction of a frame before the last picture; pad only its silent tail.
    audio=np.pad(audio,(0,max(0,needed-len(audio))))[:needed]
    edited=np.concatenate([audio[a*SPF:z*SPF] for a,z in KEEP])
    edited_wav=OUT/'edited.wav'
    with wave.open(str(edited_wav),'wb') as w:
        w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR);w.writeframes(edited.tobytes())
    inverse={sf:n for n,sf in enumerate(FRAMES)}
    boundaries=sorted({630}|{inverse[f] for f in old['boundaries'] if f in inverse})
    wanted=set(range(0,len(FRAMES),120))|{len(FRAMES)-1,4181,4182,4180,4240}
    wanted|={n for t in boundaries for n in (t-1,t,t+1)}
    wanted|={inverse[f] for f in old['preview_frames'] if f in inverse}
    wanted={f for f in wanted if 0<=f<len(FRAMES)}
    protected={str(p):sha(p) for p in [SRC,ROOT/'Prompts/what-is-ai-v10.mp4',ROOT/'course-assets/what-is-ai/what-is-ai.mp4',
       *sorted((ROOT/'course-assets/what-is-ai').glob('*.jpg'))]}
    p=subprocess.Popen([ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
      '-i',str(edited_wav),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast','-crf','16','-threads','4',
      '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar',str(SR),'-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    rd=Reader(SRC)
    for n,sf in enumerate(FRAMES):
        im=visual(sf,rd.at(sf))
        if n in wanted:cv2.imwrite(str(OUT/'preview'/f'{n:05d}.jpg'),im)
        p.stdin.write(im.tobytes())
        if n%1000==999:print(f'Rendered {n+1}/{len(FRAMES)}',flush=True)
    p.stdin.close();assert p.wait()==0;rd.c.release()
    assert all(sha(Path(path))==h for path,h in protected.items())
    edge=CUT[0]*SPF;resume=CUT[1]*SPF
    rms=lambda a:20*np.log10(max(float(np.sqrt(np.mean(a.astype(float)**2)))/32768,1e-10))
    manifest=dict(candidate=str(DEST),candidate_sha256=sha(DEST),source=str(SRC),source_sha256=sha(SRC),
      scope='Narrow approved narration cut and immediate returning takeaway highlight; all other v10 treatment preserved.',
      approval='User removes repetition around :22–:48 and requests highlight when board appears at old 2:46.',
      cut_source_frames=list(CUT),cut_source_seconds=[21,48],keep_source_frames=KEEP,source_frame_mapping=FRAMES,
      frames=len(FRAMES),fps=30,duration=len(FRAMES)/30,removed_seconds=27,
      audio_sample_rate=SR,audio_pcm_sha256=hashlib.sha256(edited.tobytes()).hexdigest(),
      audio_join=dict(output_seconds=21,source_silences=[[20.56805,21.461973],[47.322404,48.356009]],
        left_rms_db=rms(audio[edge-441:edge]),right_rms_db=rms(audio[resume:resume+441]),
        edge_jump_pcm=int(audio[resume])-int(audio[edge-1]),added_pause=0,processing='Exact PCM concatenation in existing silence; no fades, no added pause; AAC re-encoded at original 44.1 kHz mono.'),
      boards=old['boards'],board_intervals_source=intervals,highlight_change=dict(board='One Picks. One Creates.',
        source_frame=4991,output_frame=inverse[4991],output_seconds=inverse[4991]/30,ring_start_local=0,
        reason='Explicit owner instruction overrides unmarked opening on this returning board.'),
      definition_board=dict(output_start=21,unmarked_until=48.38-27,reason='Cut removes original introduction. Preserve full board and first spoken definition onset; remove former list ring.'),
      boundaries=boundaries,preview_frames=sorted(wanted),protected=protected,corner_cleanup=corner,
      reused_assets=str(PREV/'assets'),listening='Not directly auditioned; mathematical splice and silence checks only. Owner playback review required before publication.')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Built',DEST,flush=True)

if __name__=='__main__':main()

#!/usr/bin/env python3
"""Approved redundancy cuts and premature native-outline repair."""
import copy,json,subprocess
import cv2,numpy as np
import build_support_trap_v11 as prior
b=prior.b
b.OUT=b.ROOT/'video-audit/support-trap-tighten-2026-09-30-v12'
b.DEST=b.ROOT/'Prompts/support-trap-v12.mp4'
BASE=b.ROOT/'Prompts/support-trap-v11.mp4'
BASE_SHA='c133890cc2a7d14ee8e0d44d4c955c02144c4c6c8da9b0710189040d54974655'
PCM=b.ROOT/'video-audit/support-trap-hybrid-2026-09-30-v9/edited.wav'
CUTS=[(4249,4450),(8037,8242)]
KEEP=[(0,4249),(4450,8037),(8242,8565)]
HOLD_A,HOLD_B=3864,3886
TOTAL=8565-sum(z-a for a,z in CUTS)

def mapped(f):return f-sum(max(0,min(f,z)-a) for a,z in CUTS if f>a)
def original(f):
    cursor=0
    for a,z in KEEP:
        if f<cursor+z-a:return a+f-cursor
        cursor+=z-a
    raise ValueError(f)

def setup():
    build,rows=prior.setup()
    # Remove the discarded tool/trap scene. Keep the relevant urgency drawing
    # throughout its retained narration, without importing the scene's old fade.
    old=next(r for r in rows if r['start_frame']==4249)
    rows.remove(old)
    rows.append(dict(start_frame=4450,end_frame=4681,kind='native',key='1',video_start=4275,video_end=4446,retime=True,clean=True,label='Retained urgency: no time to polish a message'))
    rows.sort(key=lambda r:r['start_frame'])
    final=[]
    for r in rows:
        for a,z in KEEP:
            left,right=max(a,r['start_frame']),min(z,r['end_frame'])
            if right>left:
                v=copy.deepcopy(r);v.update(original_start_frame=left,original_end_frame=right,start_frame=mapped(left),end_frame=mapped(right))
                final.append(v)
    assert final[0]['start_frame']==0 and final[-1]['end_frame']==TOTAL
    assert all(a['end_frame']==z['start_frame'] for a,z in zip(final,final[1:]))
    return build,rows,final

def main():
    assert not b.DEST.exists(),'Never overwrite a candidate'
    b.OUT.mkdir(exist_ok=True);(b.OUT/'preview').mkdir(exist_ok=True)
    assert b.sha(BASE)==BASE_SHA
    for key,src in b.SOURCES.items():assert b.sha(src)==b.EXPECTED[key]
    protected={str(p):b.sha(p) for p in [BASE,PCM,*b.SOURCES.values(),*list((b.ROOT/'course-assets/support-trap').glob('*.jpg')),b.ROOT/'course-assets/support-trap/support-trap.mp4']}
    build,rows,final=setup();boards={k:b.BoardRender(k,v) for k,v in build.boards.items()}
    source=b.wavread(PCM);assert len(source)==8565*b.SPF
    audio=np.concatenate([source[a*b.SPF:z*b.SPF] for a,z in KEEP])
    # Five milliseconds only at each quiet join edge; no added silence or gain.
    for a,z in CUTS:
        seam=mapped(a)*b.SPF;ramp=np.linspace(0,1,240)
        audio[seam-240:seam]*=1-ramp;audio[seam:seam+240]*=ramp
    assert len(audio)==TOTAL*b.SPF;b.wavwrite(b.OUT/'edited.wav',audio)
    prep=next(r for r in rows if r['start_frame']==3506)
    rr=b.Reader(b.SOURCES['2'])
    hold,_=b.render_frame(prep,HOLD_A,boards,rr,None,build.close_img);rr.cap.release()
    cv2.imwrite(str(b.OUT/'outline-hold.png'),hold)
    boundaries={r['start_frame']:r['label'] for r in final[1:]}
    boundaries.update({HOLD_A:'Hold last clean preparation graphic',mapped(CUTS[0][0]):'Cut repeated tool-versus-trap sentence',mapped(CUTS[1][0]):'Safety takeaway directly to canonical close'})
    wants={f for r in final for f in [r['start_frame'],r['end_frame']-1,(r['start_frame']+r['end_frame'])//2]}
    wants|={f for boundary in boundaries for f in [boundary-1,boundary,boundary+5,boundary+12] if 0<=f<TOTAL}
    manifest=dict(output=str(b.DEST),approval='User: Build it please, following approval of the two redundancy cuts and removal of the premature third-box highlight.',
        base=str(BASE),base_sha256=BASE_SHA,fps=30,total_frames=TOTAL,duration=TOTAL/30,source_hashes=b.EXPECTED,
        original_visual_timeline=rows,visual_timeline=final,original_timeline_boards=build.boards,
        cuts=[dict(original_start_frame=a,original_end_frame=z,output_join_frame=mapped(a),removed_frames=z-a) for a,z in CUTS],
        retained_original_intervals=KEEP,outline_hold=dict(original_start_frame=HOLD_A,original_end_frame=HOLD_B,hold_original_frame=HOLD_A),
        boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],
        audio=dict(source_PCM=str(PCM),source_sha256=b.sha(PCM),sample_rate=48000,quiet_edge_fade_ms=5,added_pauses=False,global_normalization=False),
        close=dict(original_start_frame=b.CLOSE_START,start_frame=mapped(b.CLOSE_START),prehold=48,push=150,endpoint=1.2,settle=125),
        inherited_wording_note='Live story retains encouraged professional help without the lesson qualifier sometimes.',scope='Review candidate only; not installed or published.')
    proc=subprocess.Popen([b.FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-i',str(b.OUT/'edited.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','medium','-threads','2','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(b.DEST)],stdin=subprocess.PIPE)
    readers={};written=0
    for r in rows:
        intervals=[(max(a,r['start_frame']),min(z,r['end_frame'])) for a,z in KEEP if min(z,r['end_frame'])>max(a,r['start_frame'])]
        if not intervals:continue
        reader=None
        if r['kind']=='native':
            reader=readers.get(r['key'])
            if reader is None or reader.n>r['video_start']:
                if reader:reader.cap.release()
                reader=b.Reader(b.SOURCES[r['key']]);readers[r['key']]=reader
        still=cv2.imread(r['asset']) if r['kind']=='image' else None
        for a,z in intervals:
            for f in range(a,z):
                im=hold if HOLD_A<=f<HOLD_B else b.render_frame(r,f,boards,reader,still,build.close_img)[0]
                output=mapped(f)
                if output in wants:cv2.imwrite(str(b.OUT/'preview'/f'{output:06d}.jpg'),im)
                proc.stdin.write(im.tobytes());written+=1
        print('Render: '+r['label'],flush=True)
    for reader in readers.values():reader.cap.release()
    proc.stdin.close();assert proc.wait()==0 and written==TOTAL
    manifest.update(render_sha256=b.sha(b.DEST),encoded_input_frames=written,protected_files_unchanged={p:b.sha(p)==h for p,h in protected.items()})
    assert all(manifest['protected_files_unchanged'].values())
    (b.OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('COMPLETE',b.DEST,TOTAL/30,flush=True)

if __name__=='__main__':main()

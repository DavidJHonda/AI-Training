#!/usr/bin/env python3
"""Approved v11 graphics insert; pristine visuals, identical delivery AAC.

Only output frames [4367,5004) change. Short donor animations are retimed and
then held before their unwanted next states; no narration or timing edits.
"""
import argparse
import json
import subprocess
import cv2
import numpy as np
import build_how_an_llm_works_v10_review as base
from editspec_build import Reader, sha, PURPLE
from gemini_mark import clean_frame, glyph_mask

ROOT=base.ROOT
PREVIOUS=ROOT/'Prompts/how-an-llm-works-v11.mp4'
OLD=ROOT/'video-audit/how-an-llm-works-repair-2026-09-17-v11'
OUT=ROOT/'video-audit/how-an-llm-works-repair-2026-09-17-v12'
DEST=ROOT/'Prompts/how-an-llm-works-v12.mp4'
START,SWITCH,END=4367,4675,5004
DONORS=[
    dict(start_frame=START,end_frame=SWITCH,label='Broader learned structures: problem-solving drawing',
         kind='visual',visual='source',video_src=str(ROOT/'Prompts/how-an-llm-works-reroll-2.mp4'),
         video_start=2840,video_end=2890,video_rate=.25),
    dict(start_frame=SWITCH,end_frame=END,label='Patterns form during training: internal numbers drawing',
         kind='visual',visual='source',video_src=str(base.SOURCES['learns-2']),
         video_start=4950,video_end=5089,video_rate=.5),
]


class Drawing:
    """Sequentially decode/clean unique frames; linearly retime without optical AI."""
    def __init__(self,row,mask):
        self.row=row;self.frames=[];self.methods=[]
        reader=Reader(row['video_src'])
        for f in range(row['video_start'],row['video_end']):
            im,method=clean_frame(reader.at(f),mask)
            assert im.shape==(720,1280,3)
            self.frames.append(im);self.methods.append(method)
        reader.c.release()
    def at(self,f):
        pos=min(f*self.row['video_rate'],len(self.frames)-1)
        lo=int(pos);hi=min(lo+1,len(self.frames)-1);q=pos-lo
        return (self.frames[lo] if not q else
                cv2.addWeighted(self.frames[lo],1-q,self.frames[hi],q,0))


def prepare():
    old=json.loads((OLD/'edit-manifest.json').read_text())
    assert sha(PREVIOUS)==old['render_sha256']
    # index.html has advanced since v11; current lesson and referenced JPGs were
    # reread for this repair. Pin today's page without undoing other task edits.
    for path,digest in old['protected_hashes'].items():
        if path!=str(ROOT/'index.html'):assert sha(path)==digest,path
    base.OUT=OUT;base.DEST=DEST
    b=base.prepare()
    for p in [PREVIOUS,*[r['video_src'] for r in DONORS]]:b.hashes[str(p)]=sha(p)
    b.tone_meta=dict(old['audio'],delivery='AAC stream copied bit-for-bit from v11; no audio edits')
    b.grafts=old['grafts']
    # Carry forward v11's exact row-only jelly treatment.
    def jelly(spec):
        start,end=base.A(94.1),base.A(100.8)
        chosen=[r for r in spec['rings'] if r['start']==start-b.boards['odds']['src_in']]
        assert len(chosen)==2
        for r,rect in zip(chosen,[[62,368,756,445],[842,671,1536,754]]):
            r.update(base.ring(b,'odds',start,end,rect,PURPLE))
    base.update_spec(b,'odds',jelly)
    b.boards['odds']['comparison_highlights']=old['boards']['odds']['comparison_highlights']
    # Preserve all board specs; shorten only this board's visible timeline leg.
    i=next(i for i,r in enumerate(b.rows) if r['visual']=='patterns')
    original=dict(b.rows[i]);assert original['end_frame']==END
    b.rows[i:i+1]=[dict(original,end_frame=START),*[dict(r) for r in DONORS]]
    assert all(a['end_frame']==z['start_frame'] for a,z in zip(b.rows,b.rows[1:]))
    for key,board in b.boards.items():
        for field in ('asset','sha256','rings','beats'):
            assert board.get(field)==old['boards'][key].get(field),(key,field)
    # Every unaffected visual row is byte-for-byte the same planned treatment.
    expected=[r for r in old['timeline'] if r['visual']!='patterns']
    actual=[r for r in b.rows if r['visual']!='patterns' and r not in DONORS]
    assert actual==expected
    base.previews(b)
    b.manifest(dict(scope_detail='Approved narrow visual repair: two selected Notebook drawings replace the long patterns-board hold; narration, timing and v11 jelly highlights unchanged.',
                    previous_candidate=str(PREVIOUS),previous_sha256=sha(PREVIOUS),
                    changed_output_frames=[[START,END]],changed_output_seconds=[[START/30,END/30]],
                    drawing_inserts=DONORS,
                    page_changed_since_previous=sha(ROOT/'index.html')!=old['protected_hashes'][str(ROOT/'index.html')],
                    retiming='Linear adjacent-frame blending at the video_rate recorded on each drawing row; endpoint holds; no looping or added camera movement.',
                    long_board_exception=old['long_board_exception'],
                    timing_coordinate_system=old['timing_coordinate_system'],
                    literal_listening_performed=False))
    return b


def render(b,preview_only=False):
    mask=glyph_mask(); drawings={r['start_frame']:Drawing(r,mask) for r in DONORS}
    folder=OUT/'drawing-previews';folder.mkdir(exist_ok=True)
    for r in DONORS:
        d=drawings[r['start_frame']];cells=[]
        for f in sorted(set([0,r['end_frame']-r['start_frame']-1,*range(30,r['end_frame']-r['start_frame'],30)])):
            im=d.at(f);outf=r['start_frame']+f
            cv2.imwrite(str(folder/f'f{outf:05d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,96])
            cell=cv2.resize(im,(480,270));cv2.putText(cell,f'{outf/30:.3f}s f{outf}',(8,25),cv2.FONT_HERSHEY_SIMPLEX,.65,(0,0,200),2);cells.append(cell)
        while len(cells)%3:cells.append(np.zeros_like(cells[0]))
        cv2.imwrite(str(folder/f'sheet-{r["start_frame"]}.jpg'),cv2.vconcat([cv2.hconcat(cells[i:i+3]) for i in range(0,len(cells),3)]))
    if preview_only:return
    assert not DEST.exists(),f'Never overwrite {DEST}'
    counts=dict(clone=0,inpaint=0,declined=[])
    p=subprocess.Popen([b.ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
                        '-i',str(PREVIOUS),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','medium',
                        '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for row in b.rows:
        visual=row['visual'];start,end=row['start_frame'],row['end_frame'];drawing=drawings.get(start)
        if visual=='source' and not drawing:reader=Reader(row['video_src']);last_idx=-1;last_im=None
        elif visual not in ('source','close'):renderer=base.BoardRenderer(OUT/f'leg-{visual}.json')
        print(f'render {start/30:.2f}–{end/30:.2f}: {row["label"]}',flush=True)
        for f in range(start,end):
            if drawing:im=drawing.at(f-start)
            elif visual=='source':
                idx=min(row['video_start']+f-start,row['video_end']-1)
                if idx!=last_idx:im,method=clean_frame(reader.at(idx),mask);last_im=im;last_idx=idx
                else:im=last_im
                if method:counts[method]+=1
                else:counts['declined'].append(f)
            elif visual=='close':
                ci=b.close_img;h,w=ci.shape[:2]
                q=np.clip((f-base.CLOSE-48)/149,0,1);z=1+.2*base.smoothstep(q);ww=w/z;hh=ww*9/16
                im=cv2.warpAffine(ci,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),
                                  (1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
            else:im=renderer.at(f-b.boards[visual]['src_in'])
            p.stdin.write(im.tobytes())
        if visual=='source' and not drawing:reader.c.release()
    p.stdin.close();assert p.wait()==0
    m=json.loads((OUT/'edit-manifest.json').read_text())
    m.update(render_sha256=sha(DEST),corner_mark=counts,
             drawing_corner_cleaning={str(k):dict(clone=d.methods.count('clone'),inpaint=d.methods.count('inpaint'),
                                                  declined=[i+d.row['video_start'] for i,v in enumerate(d.methods) if v is None]) for k,d in drawings.items()},
             protected_files_unchanged={p:sha(p)==h for p,h in b.hashes.items()})
    assert all(m['protected_files_unchanged'].values())
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
    print('Completed',DEST,base.TOTAL,'frames',flush=True)


def verify(b):
    def ahash(p):return subprocess.check_output([b.ff,'-v','error','-i',str(p),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-'],text=True).strip()
    hashes={p.name:ahash(p) for p in (PREVIOUS,DEST)};assert len(set(hashes.values()))==1
    cap=cv2.VideoCapture(str(DEST));count=0;cells=[]
    meta=dict(fps=cap.get(cv2.CAP_PROP_FPS),width=cap.get(cv2.CAP_PROP_FRAME_WIDTH),height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    want={base.TOTAL-1,8304,*range(START,END,30)}
    for f in [START,SWITCH,END]:want.update([f-1,f,f+1])
    qa=OUT/'encoded-checks';qa.mkdir(exist_ok=True)
    while True:
        ok,im=cap.read()
        if not ok:break
        if count in want:
            cv2.imwrite(str(qa/f'f{count:05d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,96])
            if START<=count<END and (count-START)%30==0:
                cell=cv2.resize(im,(480,270));cv2.putText(cell,f'{count/30:.3f}s f{count}',(8,25),cv2.FONT_HERSHEY_SIMPLEX,.65,(0,0,200),2);cells.append(cell)
        count+=1
    cap.release();assert count==base.TOTAL;assert meta==dict(fps=30.,width=1280.,height=720.)
    for i in range(0,len(cells),9):
        chunk=cells[i:i+9]
        while len(chunk)%3:chunk.append(np.zeros_like(cells[0]))
        cv2.imwrite(str(qa/f'sheet-{i//9}.jpg'),cv2.vconcat([cv2.hconcat(chunk[k:k+3]) for k in range(0,len(chunk),3)]))
    (qa/'verification.json').write_text(json.dumps(dict(decoded_frames=count,metadata=meta,audio_hashes=hashes,audio_bitstream_identical=True),indent=2))
    subprocess.run([str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),
                    '--outdir',str(OUT/'transitions'),'--boundary',f'{START}:board-to-problem-solving',
                    '--boundary',f'{SWITCH}:problem-solving-to-internal-numbers',
                    '--boundary',f'{END}:internal-numbers-to-handoff'],check=True)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');ap.add_argument('--verify-only',action='store_true');args=ap.parse_args()
    if args.verify_only:
        import imageio_ffmpeg
        from types import SimpleNamespace
        verify(SimpleNamespace(ff=imageio_ffmpeg.get_ffmpeg_exe()));return
    b=prepare();render(b,args.prepare_only)
    if not args.prepare_only:verify(b)

if __name__=='__main__':main()

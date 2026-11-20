#!/usr/bin/env python3
"""Two approved sentence cuts, banner zoom, and two photographic inserts.

Rebuilds from raw roll 3 and original assets, retaining v9's other treatments.
"""
from pathlib import Path
import argparse
import json
import subprocess
import wave

import av
import cv2
import numpy as np

import build_work_changes_v9 as base
from make_close_board import compose_canonical_for_video

ROOT = base.ROOT
OUT = ROOT/'video-audit/work-changes-v10-2026-11-20'
DEST = ROOT/'Prompts/work-changes-v10.mp4'
ASSETS = ROOT/'scripts/video/assets/work-changes-cutaways-2026-11-20'
TRAIN = ASSETS/'learning-through-reviews.png'
SCHOOL = ASSETS/'school-practice.png'
FPS, SR, SPF = 30, 48000, 1600
CUTS = [(1215, 1504), (7613, 7788)]
ROWS = [(0,1215),(1504,7613),(7788,8051)]
TOTAL = sum(b-a for a,b in ROWS)
TRAIN_IN, TRAIN_OUT = 5676, 5957


def output_frame(n):
    if any(a <= n < b for a,b in CUTS):
        return None
    return n-sum(b-a for a,b in CUTS if b <= n)


class Edit(base.Edit):
    def __init__(self):
        self.assignment = base.Board(base.ASSIGN)
        self.concepts = base.Board(base.CONCEPTS)
        self.check = cv2.imread(str(base.CHECK))
        self.training = cv2.imread(str(TRAIN))
        self.school_image = cv2.imread(str(SCHOOL))
        OUT.mkdir(parents=True,exist_ok=True)
        compose_canonical_for_video(base.CLOSE,OUT/'close-canvas.png','#ffffff')
        self.close = cv2.imread(str(OUT/'close-canvas.png'))

    def assignment_frame(self,n):
        if n < base.fr(129.76):
            return super().assignment_frame(n)
        a=self.assignment
        camera=base.lerp(a.fit(base.RIGHT),a.fit(base.BANNER),n-base.fr(129.76),36)
        cx,cy,width=camera; height=width*base.H/base.W
        cx=np.clip(cx,width/2,a.cw-width/2)
        cy=np.clip(cy,height/2,a.ch-height/2)
        camera=np.array([cx,cy,width])
        rect=base.BANNER
        bounds=[rect[0]+a.ox,rect[1]+a.oy,rect[2]+a.ox,rect[3]+a.oy]
        if min(bounds[0]-(cx-width/2),bounds[1]-(cy-height/2),
               cx+width/2-bounds[2],cy+height/2-bounds[3]) < 10:
            rect=None
        return a.render(camera,rect,base.GENERAL),'assignment-banner-zoom'

    def frame(self,source_frame,n):
        if TRAIN_IN <= n < TRAIN_OUT:
            return base.image_push(self.training,(n-TRAIN_IN)/(TRAIN_OUT-TRAIN_IN),.03),'learning-through-reviews-photo'
        if base.SCHOOL_IN <= n < base.CLOSE_IN:
            return base.image_push(self.school_image,(n-base.SCHOOL_IN)/(CUTS[1][0]-base.SCHOOL_IN),.02),'school-practice-photo'
        return super().frame(source_frame,n)


def prepare_audio():
    wav=OUT/'source.wav'
    if not wav.exists():
        subprocess.run([base.FF,'-v','error','-y','-i',str(base.SOURCE),'-vn','-ac','2','-ar',str(SR),
                        '-c:a','pcm_s16le',str(wav)],check=True)
    with wave.open(str(wav)) as reader:
        assert reader.getframerate()==SR and reader.getnchannels()==2
        samples=np.frombuffer(reader.readframes(reader.getnframes()),np.int16).reshape(-1,2)
    edited=np.concatenate([samples[a*SPF:b*SPF] for a,b in ROWS])
    assert len(edited)==TOTAL*SPF
    with wave.open(str(OUT/'edited.wav'),'wb') as writer:
        writer.setnchannels(2);writer.setsampwidth(2);writer.setframerate(SR);writer.writeframes(edited.tobytes())
    joins=[]
    for cut_a,cut_b in CUTS:
        boundary=cut_a-sum(b-a for a,b in CUTS if b<=cut_a)
        left=samples[cut_a*SPF-960:cut_a*SPF].astype(float)/32768
        right=samples[cut_b*SPF:cut_b*SPF+960].astype(float)/32768
        joins.append(dict(source_cut_frames=[cut_a,cut_b],source_cut_seconds=[cut_a/FPS,cut_b/FPS],
            output_frame=boundary,output_seconds=boundary/FPS,
            before_20ms_rms_db=float(20*np.log10(max(np.sqrt(np.mean(left*left)),1e-10))),
            after_20ms_rms_db=float(20*np.log10(max(np.sqrt(np.mean(right*right)),1e-10))),
            sample_jump_per_channel=(samples[cut_b*SPF].astype(int)-samples[cut_a*SPF-1].astype(int)).tolist()))
    (OUT/'audio-joins.json').write_text(json.dumps(joins,indent=2)+'\n')
    return joins


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');args=parser.parse_args()
    cv2.setNumThreads(2)
    edit=Edit();(OUT/'preview').mkdir(exist_ok=True)
    protected={str(p.relative_to(ROOT)):base.sha(p) for p in [base.SOURCE,ROOT/'Prompts/work-changes-v9.mp4',
        base.ASSIGN,base.CONCEPTS,base.CLOSE,base.CHECK,TRAIN,SCHOOL,ROOT/'index.html',
        ROOT/'course-assets/work-changes/work-changes.mp4']}
    wanted={1200,1214,1504,1510,3893,3908,3929,3960,4080,4155,5676,5745,5880,5956,7451,7515,7612,7788,7950,8050}
    if not args.preview:
        assert not DEST.exists(),'Never overwrite an existing review candidate'
        joins=prepare_audio()
        encoder=subprocess.Popen([base.FF,'-v','error','-f','rawvideo','-pix_fmt','yuv420p',
            '-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),
            '-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','17','-preset','fast','-threads','4',
            '-profile:v','high','-level:v','3.1','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
            '-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    spans=[];current=None;written=0
    with av.open(str(base.SOURCE)) as container:
        container.streams.video[0].codec_context.thread_count=2
        for frame in container.decode(video=0):
            n=round(frame.time*FPS);o=output_frame(n)
            if o is None:continue
            assert o==written;written+=1
            if args.preview and n not in wanted:continue
            im,label=edit.frame(frame,n)
            raw=frame.to_ndarray(format='yuv420p') if im is None else av.VideoFrame.from_ndarray(im,format='bgr24').to_ndarray(format='yuv420p')
            if not args.preview:
                encoder.stdin.write(raw.tobytes())
                if current is None or label!=current['label'] or n in [b for a,b in CUTS]:
                    if current:current['output_end_frame']=o;spans.append(current)
                    current=dict(output_start_frame=o,source_start_frame=n,label=label)
                if written%900==0:print(f'Rendered {written}/{TOTAL}',flush=True)
            if n in wanted:
                if im is None:im=frame.to_ndarray(format='bgr24')
                cv2.imwrite(str(OUT/'preview'/f'{o:06d}-source-{n:06d}-{label}.jpg'),im)
    assert written==TOTAL
    if args.preview:print('Preview complete');return
    encoder.stdin.close();assert encoder.wait()==0
    current['output_end_frame']=TOTAL;spans.append(current)
    assert all(base.sha(ROOT/p)==h for p,h in protected.items())
    manifest=dict(candidate=str(DEST.relative_to(ROOT)),candidate_sha256=base.sha(DEST),
        approval='User requested two content cuts, banner zoom, and photographic training-ground and school illustrations.',
        scope='Narrow revision of v9, rebuilt from raw version 3 and original assets.',
        frames=TOTAL,fps=FPS,duration=TOTAL/FPS,source_frame_rows=ROWS,cuts=CUTS,
        audio='Two complete-sentence cuts in measured quiet gaps. Retained stereo PCM unchanged before one AAC encode. No added pauses, fades, gain changes, or grafts.',
        audio_joins=joins,protected_sources=protected,visual_spans=spans,
        illustration_prompts=str((ASSETS/'generation-record.json').relative_to(ROOT)),
        status='Review candidate, not installed or published.',
        listening='No perceptual listening certified; source words and quiet cut boundaries verified by ASR and waveform.')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('COMPLETE',DEST,TOTAL/FPS,flush=True)


if __name__=='__main__':main()

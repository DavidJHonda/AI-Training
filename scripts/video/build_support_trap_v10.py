#!/usr/bin/env python3
"""Visual-only lesson-board update, assembled from v9's original sources."""
import argparse, copy, json, subprocess
import cv2
import build_support_trap_v9 as prior
b = prior.b
b.OUT = b.ROOT / 'video-audit/support-trap-board-update-2026-09-30-v10'
b.DEST = b.ROOT / 'Prompts/support-trap-v10.mp4'
BASE = b.ROOT / 'Prompts/support-trap-v9.mp4'
BASE_SHA = '1f319094ba354c2048d900c8f3c62068b9f43c39971ee378f879588d9320137b'
START, END = 2146, 4057

def setup():
    build, original = prior.setup()
    def target(label, at, rect, color):
        return dict(label=label, at=at, rects=[rect], color=color, cam=rect)
    build.board('jobs', b.ROOT/'course-assets/support-trap/support-trap-jobs.jpg',
                2773, END, 'compact', [
                    target('Ordinary Venting', 98.98, [40,128,525,852], '#0e8f86'),
                    target('Preparation', 111.70, [557,128,1043,852], '#1652f0'),
                    target('Danger', 129.92, [1075,128,1560,852], '#c41f28'),
                ], push=False)
    del build.boards['role']
    changed = [
        dict(start_frame=START,end_frame=2476,kind='native',key='2',video_start=2094,video_end=2466,retime=True,clean=True,label='AI preparation leads toward human presence'),
        dict(start_frame=2476,end_frame=2773,kind='native',key='2',video_start=2526,video_end=2616,retime=True,clean=True,label='A person beyond the screen: preparation does not replace people'),
        dict(start_frame=2773,end_frame=3065,kind='board',board='jobs',label='Current emotional-support board: overview and ordinary venting'),
        dict(start_frame=3065,end_frame=3341,kind='native',key='1',video_start=2779,video_end=3055,retime=False,clean=True,label='Retained venting diagram: frustration becomes calmer words'),
        dict(start_frame=3341,end_frame=3506,kind='board',board='jobs',label='Current emotional-support board: preparation'),
    ]
    # Retain v9's follow-through diagram, then replace its redundant danger chart.
    changed += [copy.deepcopy(r) for r in original if r['start_frame']==3506]
    changed += [dict(start_frame=3886,end_frame=END,kind='board',board='jobs',label='Current emotional-support board: danger')]
    rows = [copy.deepcopy(r) for r in original if r['end_frame']<=START] + changed
    rows += [copy.deepcopy(r) for r in original if r['start_frame']>=END]
    assert rows[0]['start_frame']==0 and rows[-1]['end_frame']==prior.TOTAL
    assert all(a['end_frame']==z['start_frame'] for a,z in zip(rows,rows[1:]))
    return build, rows

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
    b.OUT.mkdir(exist_ok=True);(b.OUT/'preview').mkdir(exist_ok=True)
    assert b.sha(BASE)==BASE_SHA
    for key,src in b.SOURCES.items():assert b.sha(src)==b.EXPECTED[key]
    protected={str(p):b.sha(p) for p in [BASE,*b.SOURCES.values(),*list((b.ROOT/'course-assets/support-trap').glob('*.jpg')),b.ROOT/'course-assets/support-trap/support-trap.mp4']}
    build,rows=setup();boards={k:b.BoardRender(k,v) for k,v in build.boards.items()}
    # The old ending and all untouched visuals use the same original-source recipe.
    flashrow=next(r for r in rows if r['start_frame']==prior.repair.FLASH_A)
    rr=b.Reader(b.SOURCES['1'])
    hold,_=b.clean_frame(rr.at(flashrow['video_start']+prior.repair.FLASH_B-prior.repair.FLASH_A),b.MASK)
    rr.cap.release()
    boundaries={r['start_frame']:r['label'] for r in rows[1:]}
    boundaries.update({prior.repair.QUOTE:'Spoken AI response highlight',prior.repair.FLASH_B:'Resume settled tool-versus-trap graphic'})
    wants={f for r in rows for f in [r['start_frame'],r['start_frame']+15,r['end_frame']-1,(r['start_frame']+r['end_frame'])//2]}
    wants.update(s['spoken_onset_source_frame']+15 for s in build.boards['jobs']['states'])
    manifest=dict(output=str(b.DEST),approval='User: Agree. Build it please. Approved visual edit following lesson consolidation.',
                  fps=30,total_frames=prior.TOTAL,duration=prior.TOTAL/30,base=str(BASE),base_sha256=BASE_SHA,
                  source_hashes=b.EXPECTED,visual_timeline=rows,boards=build.boards,
                  changed_interval=[START,END],boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],
                  audio=dict(source=str(BASE),mode='AAC stream copy; no timing, gain, narration, or pause changes'),
                  scope='Review candidate only; not installed or published. Exact new paragraph is represented in meaning by existing narration.',
                  inherited_wording_note='Live ending retains encouraged her to seek professional help without the lesson qualifier sometimes.',
                  close=dict(start_frame=b.CLOSE_START,prehold=48,push=150,endpoint=1.2,settle=prior.TOTAL-b.CLOSE_START-198))
    proc=None
    if not args.preview:
        assert not b.DEST.exists(),'Never overwrite a candidate'
        proc=subprocess.Popen([b.FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
            '-i',str(BASE),'-map','0:v','-map','1:a','-c:v','libx264','-crf','18','-preset','medium','-threads','2',
            '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(b.DEST)],stdin=subprocess.PIPE)
    readers={};written=0
    for r in rows:
        reader=None
        if r['kind']=='native':
            reader=readers.get(r['key'])
            if reader is None or reader.n>r['video_start']:
                if reader:reader.cap.release()
                reader=b.Reader(b.SOURCES[r['key']]);readers[r['key']]=reader
        still=cv2.imread(r['asset']) if r['kind']=='image' else None
        for f in range(r['start_frame'],r['end_frame']):
            if args.preview and f not in wants:continue
            im=hold if prior.repair.FLASH_A<=f<prior.repair.FLASH_B else b.render_frame(r,f,boards,reader,still,build.close_img)[0]
            if f in wants:cv2.imwrite(str(b.OUT/'preview'/f'{f:06d}.jpg'),im)
            if proc:proc.stdin.write(im.tobytes());written+=1
        print(('Preview' if args.preview else 'Render')+': '+r['label'],flush=True)
    for reader in readers.values():reader.cap.release()
    if proc:
        proc.stdin.close();assert proc.wait()==0 and written==prior.TOTAL
        manifest.update(render_sha256=b.sha(b.DEST),encoded_input_frames=written,
            protected_files_unchanged={p:b.sha(p)==h for p,h in protected.items()})
        assert all(manifest['protected_files_unchanged'].values())
    (b.OUT/('preview-manifest.json' if args.preview else 'edit-manifest.json')).write_text(json.dumps(manifest,indent=2)+'\n')
    print('COMPLETE',b.DEST,flush=True)

if __name__=='__main__':main()

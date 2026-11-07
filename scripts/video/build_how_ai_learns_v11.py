#!/usr/bin/env python3
"""Phase-focused repair: current boards, four narration cuts, neutral feedback UI.

User authorized the on-page simplification and requested this video build.
Review candidate only. Retain the opening analogy, shared-loop illustration,
unaffected narration/pictures, and the existing standard close.
"""
from pathlib import Path
import argparse, json, subprocess
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from editspec_build import Build, fr, sha, PURPLE, BLUE, GREEN

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'Prompts/how-ai-learns-v10.mp4'
LIVE = ROOT / 'course-assets/how-ai-learns/how-ai-learns.mp4'
DEST = ROOT / 'Prompts/how-ai-learns-v11.mp4'
OUT = ROOT / 'video-audit/how-ai-learns-phase-focus-v11-2026-11-07'
ASSETS = ROOT / 'course-assets/how-ai-learns'
FEEDBACK = ROOT / 'video-audit/understand-ai-illustration-updates-2026-10-08/assets/how-ai-learns.png'
FONT = ROOT / 'scripts/video/assets/fonts/PlusJakartaSans-wght.ttf'
EXPECTED = '8e4cf9a1d123b2534045adbe5c3515e24e9133e427f262b9372803897ac8d796'
CUTS = [(1455, 1605, 'Overview basketball question'),
        (3609, 3908, 'Pretraining sample-answer introduction and answer'),
        (4733, 5037, 'Instruction-tuning sample-answer introduction and answer'),
        (5910, 6425, 'Preference-tuning polished-answer introduction and answer')]
VISUALS = [(1350, 1926, 'phases'), (3165, 3609, 'pre'),
           (4320, 5222, 'inst'), (5222, 5429, 'feedback'), (5429, 6640, 'pref')]
BOARD_FILES = dict(phases='three-phases', pre='pretraining', inst='instruction-tuning', pref='preference-tuning')

def mapped(f):
    assert not any(a < f < z for a,z,_ in CUTS), f
    return f - sum(z-a for a,z,_ in CUTS if z <= f)

def feedback_scene(selected):
    """Retain the approved photograph and perspective; revise its code-drawn UI."""
    base = np.array(Image.open(FEEDBACK).convert('RGB'))
    ui = Image.new('RGB', (900,540), '#f5f8f6'); d = ImageDraw.Draw(ui)
    def text(x,y,s,size,color='#203335'):
        d.text((x,y),s,font=ImageFont.truetype(str(FONT),size),fill=color)
    text(32,15,'TRAINING FEEDBACK',30,'#137d77')
    text(32,65,'Which response helps more?',42)
    for y,label,active in [(146,'Response A',False),(303,'Response B',selected)]:
        d.rounded_rectangle((25,y,875,y+137),radius=15,fill='#e3f0e9' if active else 'white',outline='#137d77' if active else '#aebdb6',width=6 if active else 2)
        text(47,y+38,label,43)
    text(34,476,'Selected: more helpful' if selected else 'Compare the answers.',36,'#137d77' if selected else '#526568')
    corners=np.float32([(772,128),(1486,143),(1465,595),(743,547)])
    transform=cv2.getPerspectiveTransform(np.float32([(0,0),(899,0),(899,539),(0,539)]),corners)
    warped=cv2.warpPerspective(np.array(ui),transform,(base.shape[1],base.shape[0]),flags=cv2.INTER_CUBIC)
    alpha=cv2.warpPerspective(np.full((540,900),255,np.uint8),transform,(base.shape[1],base.shape[0])).astype(float)[:,:,None]/255
    im=Image.fromarray(np.uint8(np.clip(warped*alpha+base*(1-alpha),0,255))).resize((1280,720),Image.Resampling.LANCZOS)
    return cv2.cvtColor(np.asarray(im),cv2.COLOR_RGB2BGR)

def prepare():
    assert sha(SRC)==EXPECTED
    b=Build(ROOT,SRC,OUT,DEST,protected=[LIVE, ROOT/'lessons/how-ai-learns.md', FEEDBACK,
        *[ASSETS/f'how-ai-learns-{suffix}.jpg' for suffix in BOARD_FILES.values()]])
    b.load_audio([(48.2,48.65),(119.95,120.65),(167.5,168.2),(196.6,197.4)])
    pos=0
    for a,z,label in CUTS:
        b.keep(pos,a,'Retained narration before '+label)
        pos=z
    b.keep(pos,7382,'Retained ending and standard close')
    b.finish_audio()
    audio_rows=list(b.rows)
    b.rows=[]
    # Split pictures independently of audio; unchanged scene edges are not new audio edits.
    edges=sorted({v for a,z,k in VISUALS for v in (a,z)})
    for r in audio_rows:
        boundaries=[r['source_start']]+[v for v in edges if r['source_start']<v<r['source_end']]+[r['source_end']]
        for a,z in zip(boundaries,boundaries[1:]):
            key=next((k for s,e,k in VISUALS if s<=a and z<=e),'source')
            row=dict(kind='source',source_start=a,source_end=z,start_frame=mapped(a),end_frame=mapped(z),visual=key,label=key+' / retained source '+str(a)+'–'+str(z))
            if key!='source':row['video_start']=mapped(a)
            b.rows.append(row)
    def target(label,t,rect,color):
        return dict(label=label,at=mapped(fr(t))/30,rects=[rect],color=color,radius=14)
    cfg={
        'phases': [target('Pretraining',53.90,[40,112,530,398],PURPLE),
                   target('Instruction Tuning',56.30,[555,112,1045,398],BLUE),
                   target('Preference Tuning',60.54,[1070,112,1560,398],GREEN)],
        'pre': [target('What Pretraining Builds',108.72,[74,165,1526,467],PURPLE)],
        'inst': [target('Learn to Follow Instructions',147.24,[74,165,1526,412],BLUE),
                 target('What Still Needs Work',168.32,[74,444,1526,609],BLUE)],
        'pref': [target('Learn from Feedback',182.88,[74,165,1526,412],GREEN),
                 target('What Still Needs Work',214.48,[74,444,1526,609],GREEN)],
    }
    for a,z,key in VISUALS:
        if key=='feedback':continue
        b.board(key,ASSETS/f'how-ai-learns-{BOARD_FILES[key]}.jpg',mapped(a),mapped(z),'compact',cfg[key],push=False,min_open=57 if key=='pref' else 60)
    # Keep the six unchanged source scene cuts in the QA boundary list as well.
    old=json.loads((ROOT/'video-audit/how-ai-learns-v9-2026-09-27/edit-manifest.json').read_text())
    boundaries={r['start_frame']:r['label'] for r in b.rows[1:]}
    for r in old['timeline'][1:]:
        f=r['start_frame']
        if not any(a<=f<z for a,z,_ in CUTS):boundaries.setdefault(mapped(f),r['label'])
    m=b.manifest()
    m.update(dict(scope='Authorized narrow video repair; review candidate only.',cuts=[dict(source_start=a,source_end=z,label=l,output_join=mapped(a)) for a,z,l in CUTS],
        boundaries=[dict(frame=f,label=l) for f,l in sorted(boundaries.items())],
        source_limitation='Uses the stable finished v10 candidate for retained pictures/audio; one additional video encode. Changed boards and feedback UI rendered from their original assets.',
        close='Existing standard closing picture, narration, and final hold retained from v10.',
        feedback=dict(source=str(FEEDBACK),source_frames=[5222,5429],selection_source_frame=5334,change='Basketball prompt and sample answers replaced with neutral response labels.'),
        pauses='No added pauses. Four excisions at measured quiet frame boundaries; 5 ms source/room-tone edge fades.'))
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
    return b,m

def main():
    cv2.setNumThreads(2)
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    b,m=prepare()
    # Inspect board keyframes before rendering lossless legs.
    for key in b.boards:
        (OUT/'preview'/key).mkdir(parents=True,exist_ok=True)
        subprocess.run([str(b.py),str(b.kb),str(OUT/f'leg-{key}.json'),'--preview',str(OUT/'preview'/key)],check=True)
    scenes=[feedback_scene(False),feedback_scene(True)]
    for i,im in enumerate(scenes):cv2.imwrite(str(OUT/f'feedback-{i}.jpg'),im)
    print('Prepared',b.total,'frames;',b.total/30,'seconds',flush=True)
    if args.prepare_only:return
    b.render_legs()
    for key in b.boards:b.state_sheet(key)
    # A supporting illustration uses the same leg reader as boards, but is not a course board.
    s,e=mapped(5222),mapped(5429)
    proc=subprocess.Popen([b.ff,'-y','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0','-c:v','ffv1','-level','3',str(OUT/'leg-feedback.mkv')],stdin=subprocess.PIPE)
    for f in range(5222,5429):proc.stdin.write(scenes[int(f>=5334)].tobytes())
    proc.stdin.close();assert proc.wait()==0
    b.boards['feedback']=dict(src_in=s,src_out=e)
    b.render(clean_corner=False)
    print('BUILT',DEST,flush=True)

if __name__=='__main__':main()

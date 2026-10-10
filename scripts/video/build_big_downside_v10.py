#!/usr/bin/env python3
"""Requested overview labels and matching illustrated laptop section introductions."""
from pathlib import Path
import copy,json,subprocess,sys
import cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
from editspec_build import Reader,sha,fr
from build_big_downside_v8 import ROOT,FF,PREV,source_frame
from build_big_downside_v7 import lesson_signature
from build_creative_thinking_v8 import BoardRenderer
from gemini_mark import clean_frame,glyph_mask
from ken_burns_path import smoothstep

OUT=ROOT/'video-audit/big-downside-build-2026-10-10-v10'
PRIOR=ROOT/'video-audit/big-downside-build-2026-10-10-v9'
BASE=ROOT/'Prompts/big-downside-v9.mp4'
DEST=ROOT/'Prompts/big-downside-v10.mp4'
TITLES=['Hard to Understand and Control','People Can Misuse AI','AI Can Take the Wrong Route']

def prepare():
    old=json.loads((PRIOR/'edit-manifest.json').read_text());assert sha(BASE)==old['render_sha256']
    for p,h in old['protected_hashes'].items():
        if p!=str(ROOT/'index.html'):assert sha(p)==h,p
    (OUT/'preview').mkdir(exist_ok=True)
    inserts=[dict(start_frame=fr(11.6),end_frame=fr(15.2),label='Correctly named three-idea overview',
        visual='overview',kind='overview',video_source=str(ROOT/'Prompts/big-downside-1.mp4'),
        video_start=fr(16.8),video_end=fr(22.5333333),anchors=None)]
    for i,a,z in [(1,15.2,20.4333333),(2,77.8,84.1666667),(3,148.5333333,153.7333333)]:
        inserts.append(dict(start_frame=fr(a),end_frame=fr(z),label=f'Section {i}: {TITLES[i-1]}',
            visual=f'section-{i}',kind='section_title',image=str(OUT/'assets'/f'section-{i}.png')))
    cuts=sorted({0,old['total_frames'],*[r['start_frame'] for r in old['timeline']],
        *[r['end_frame'] for r in old['timeline']],*[r['start_frame'] for r in inserts],*[r['end_frame'] for r in inserts]})
    timeline=[]
    for a,z in zip(cuts,cuts[1:]):
        override=next((r for r in inserts if r['start_frame']<=a<r['end_frame']),None)
        r=copy.deepcopy(override or next(r for r in old['timeline'] if r['start_frame']<=a<r['end_frame']))
        if override:r.update(map_start=override['start_frame'],map_end=override['end_frame'])
        r.update(start_frame=a,end_frame=z);timeline.append(r)
    m=copy.deepcopy(old)
    m.update(output=str(DEST),base=str(BASE),base_sha256=sha(BASE),timeline=timeline,
        prior_visual_inserts=old['inserts'],inserts=inserts,
        audio='Exact AAC stream copied from v9. No audio or duration change.',
        scope='User requested corrected overview names and three matching illustrated student/laptop section introductions. Review build only.',
        protected_hashes={p:sha(p) for p in [*old['protected_hashes'],str(BASE),*[r['image'] for r in inserts if 'image' in r]]},
        lesson_scope_sha256=lesson_signature((ROOT/'index.html').read_text()),
        overview_labels=TITLES,section_assets={str(i):str(OUT/'assets'/f'section-{i}.png') for i in [1,2,3]})
    for k in ['render_sha256','corner_mark','protected_files_unchanged']:m.pop(k,None)
    labels={b['frame']:b['label'] for b in old['boundaries']}
    for r in inserts:labels[r['start_frame']]='Enter '+r['label'];labels[r['end_frame']]='Exit '+r['label']
    m['boundaries']=[dict(frame=f,label=label) for f,label in sorted(labels.items())]
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2));return m

FONT=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',28)
NUM=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf',26)
def overview_labels(im,f):
    # These are video caption replacements over the donor's existing label panels.
    # They replace both old headings and old subtitles, preserving its animated arrows.
    pil=Image.fromarray(cv2.cvtColor(im,cv2.COLOR_BGR2RGB));d=ImageDraw.Draw(pil)
    lines=[['Hard to Understand','and Control'],['People Can','Misuse AI'],['AI Can Take','the Wrong Route']]
    for i,y in enumerate([122,303,483]):
        color=[(184,62,50),(49,104,136),(153,76,42)][i]
        # Opaque panels cover the donor labels on every frame; only our text builds.
        d.rounded_rectangle((751,y,1190,y+115),radius=17,fill=(246,244,229),outline=(147,146,128),width=2)
        if f-fr(11.6)<[0,9,18][i]:continue
        d.rounded_rectangle((767,y+16,773,y+99),radius=3,fill=color)
        d.rounded_rectangle((789,y+33,837,y+81),radius=10,outline=color,width=2)
        d.text((813,y+57),str(i+1),font=NUM,fill=color,anchor='mm')
        for j,line in enumerate(lines[i]):d.text((855,y+22+j*35),line,font=FONT,fill=(28,36,38))
    return cv2.cvtColor(np.array(pil),cv2.COLOR_RGB2BGR)

def render(m,preview=False):
    cv2.setNumThreads(2)
    boards={k:BoardRenderer(PREV/f'leg-{k}.json') for k in m['boards']}
    pictures={f'section-{i}':cv2.resize(cv2.imread(m['section_assets'][str(i)]),(1280,720),interpolation=cv2.INTER_AREA) for i in [1,2,3]}
    close=cv2.imread(str(PREV/'close.png'));mask=glyph_mask();readers={};counts={}
    process=None
    if not preview:
        assert not DEST.exists(),'Never overwrite a review candidate'
        process=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30',
            '-i','pipe:0','-i',str(BASE),'-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','fast',
            '-crf','18','-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for r in m['timeline']:
        key=r['visual'];frames=range(r['start_frame'],r['end_frame'])
        if preview:
            if r['kind'] not in ['overview','section_title']:continue
            frames=sorted({r['start_frame'],r['end_frame']-1,*range(r['start_frame'],r['end_frame'],12)})
        for f in frames:
            if key in pictures:im=pictures[key].copy()
            elif key in boards:im=boards[key].frame(f-m['boards'][key]['src_in'])
            elif key=='close':
                q=np.clip((f-m['close']['start_frame']-48)/149,0,1);z=1+.2*smoothstep(q)
                h,w=close.shape[:2];ww=w/z;hh=ww*9/16
                im=cv2.warpAffine(close,np.float32([[ww/1280,0,(w-ww)/2],[0,hh/720,(h-hh)/2]]),
                    (1280,720),flags=cv2.INTER_CUBIC|cv2.WARP_INVERSE_MAP)
            else:
                path=r['video_source'];vf=source_frame(r,f);rd=readers.get(path)
                if rd is None or rd.n>vf:
                    if rd:rd.c.release()
                    rd=Reader(path);readers[path]=rd
                im,how=clean_frame(rd.at(vf),mask);counts[str(how)]=counts.get(str(how),0)+1
                if key=='overview':im=overview_labels(im,f)
            if preview or f in (r['start_frame'],r['end_frame']-1) or (r['kind'] in ['overview','section_title'] and f%15==0):
                cv2.imwrite(str(OUT/'preview'/f'{f:06}.jpg'),im)
            if process:process.stdin.write(im.tobytes())
        print(f"{r['end_frame']}/{m['total_frames']} {r['label']}",flush=True)
    for rd in readers.values():rd.c.release()
    if preview:return
    process.stdin.close();assert process.wait()==0
    m.update(render_sha256=sha(DEST),corner_mark=counts,
        protected_files_unchanged={p:sha(p)==h for p,h in m['protected_hashes'].items()},
        lesson_scope_unchanged=lesson_signature((ROOT/'index.html').read_text())==m['lesson_scope_sha256'])
    (OUT/'edit-manifest.json').write_text(json.dumps(m,indent=2))
    assert all(v for p,v in m['protected_files_unchanged'].items() if p!=str(ROOT/'index.html'))
    assert m['lesson_scope_unchanged'];print('COMPLETE',DEST,flush=True)

if __name__=='__main__':render(prepare(),'--preview' in sys.argv)

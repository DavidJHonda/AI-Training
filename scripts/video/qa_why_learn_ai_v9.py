#!/usr/bin/env python3
"""Decode and inspect the exact review candidate; no claim of audio audition."""
from pathlib import Path
import json,re,subprocess,sys
import cv2,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
from editspec_build import readwav,sha
from build_why_learn_ai_v9 import OUT,DEST,ROOT,AUDIT,BOARDS,SR
import imageio_ffmpeg

def main():
    m=json.loads((OUT/'edit-manifest.json').read_text());ff=imageio_ffmpeg.get_ffmpeg_exe()
    boundaries={r['start']:r['label'] for r in m['visual_timeline'][1:]}
    for row in m['timeline']:
        if row.get('graft_audio'):
            boundaries.setdefault(row['start_frame'],row['label']+' audio in')
            boundaries.setdefault(row['end_frame'],row['label']+' audio out')
    cmd=[sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),'--outdir',str(OUT/'guard')]
    for f,l in sorted(boundaries.items()):cmd+=['--boundary',f'{f}:{l}']
    p=subprocess.run(cmd,capture_output=True,text=True)
    (OUT/'guard.log').write_text(p.stdout+p.stderr)
    guard=json.loads((OUT/'guard/transition-guard.json').read_text())
    assert guard['decoded_frames']==m['total_frames']
    qa=OUT/'qa';qa.mkdir(exist_ok=True)
    wants=set(range(0,m['total_frames'],180))|{m['total_frames']-1}
    for f in boundaries:wants|={f-1,f}
    for key,b in m['boards'].items():
        wants.add(b['src_in'])
        for ring in b['rings']:wants.add(b['src_in']+ring['start']+30)
    cap=cv2.VideoCapture(str(DEST));i=0;tiles=[];pairs=[];dimensions=[]
    while True:
        ok,im=cap.read()
        if not ok:break
        if i in wants:
            cv2.imwrite(str(qa/f'frame-{i:06}.jpg'),im)
            small=cv2.resize(im,(384,216));small=cv2.copyMakeBorder(small,24,0,0,0,cv2.BORDER_CONSTANT,value=(255,255,255))
            cv2.putText(small,f'{i/30:.2f}s / f{i}',(5,17),cv2.FONT_HERSHEY_SIMPLEX,.45,(0,0,0),1)
            if i%180==0 or i==m['total_frames']-1:tiles.append(small)
            if i in boundaries or i+1 in boundaries:pairs.append(small)
        if i==0:dimensions=list(im.shape[:2][::-1]);fps=cap.get(cv2.CAP_PROP_FPS)
        i+=1
    cap.release();assert i==m['total_frames']
    for name,items in [('overview',tiles),('boundary-pairs',pairs)]:
        for k in range(0,len(items),20):
            group=items[k:k+20]
            while len(group)%4:group.append(np.full_like(group[0],255))
            cv2.imwrite(str(qa/f'{name}-{k//20}.jpg'),cv2.vconcat([cv2.hconcat(group[n:n+4]) for n in range(0,len(group),4)]))
    subprocess.run([ff,'-y','-v','error','-i',str(DEST),'-vn','-ac','1','-ar',str(SR),'-c:a','pcm_s16le',str(OUT/'encoded.wav')],check=True)
    original=readwav(OUT/'edited.wav');encoded=readwav(OUT/'encoded.wav');n=min(len(original),len(encoded))
    correlation=float(np.corrcoef(original[:n],encoded[:n])[0,1])
    sil=subprocess.run([ff,'-v','info','-i',str(DEST),'-af','silencedetect=noise=-35dB:d=0.12','-f','null','-'],capture_output=True,text=True)
    (OUT/'encoded-silences.txt').write_text(sil.stderr)
    gaps=[];s=None
    for line in sil.stderr.splitlines():
        hit=re.search(r'silence_start: ([\d.]+)',line)
        if hit:s=float(hit[1])
        hit=re.search(r'silence_end: ([\d.]+)',line)
        if hit and s is not None:gaps.append([s,float(hit[1])]);s=None
    joins=[]
    for row in m['timeline']:
        if not row.get('graft_audio'):continue
        for edge in ['start_frame','end_frame']:
            t=row[edge]/30
            matching=[g for g in gaps if g[0]-.08<=t<=g[1]+.08]
            joins.append(dict(time=t,label=row['label']+' '+edge,silence_windows=matching))
        key=row['label'].split(': ')[-1]
        a=max(0,row['start_frame']/30-4);d=(row['end_frame']-row['start_frame'])/30+8
        subprocess.run([ff,'-y','-v','error','-ss',str(a),'-i',str(DEST),'-t',str(d),'-vn','-c:a','libmp3lame','-b:a','160k',str(OUT/f'final-join-{key}.mp3')],check=True)
    transcript=json.loads((OUT/'edited-transcript.json').read_text()) if (OUT/'edited-transcript.json').exists() else None
    norm=lambda s:' '.join(re.findall(r"[a-z0-9]+",s.lower().replace('’',"'")))
    prompt=(ROOT/'gemini-notebook/why-learn-ai/PROMPT.txt').read_text().split('TEACH THE COMPLETE LESSON')[0]
    required=re.findall('“([^”]+)”',prompt)
    words=norm(' '.join(s['text'] for s in transcript['segments'])) if transcript else ''
    checks={line:norm(line) in words for line in required}
    report=dict(candidate=str(DEST),sha256=sha(DEST),decoded_frames=i,duration=i/30,fps=fps,dimensions=dimensions,
                transition_guard_pass=guard['pass'],source_protection=m['protected_files_unchanged'],audio_correlation=correlation,
                audio_clipped_samples=int(np.sum(abs(original)>=32767)),join_silences=joins,
                required_lines_in_automated_transcript=checks,added_midvideo_pauses=0,
                longest_continuous_board_seconds=max((r['end']-r['start'])/30 for r in m['visual_timeline'] if r['kind']=='board'),
                direct_listening_completed=False,continuous_motion_viewing_completed=False,
                manual_frame_review_completed=False)
    (OUT/'checks.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()

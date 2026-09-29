#!/usr/bin/env python3
"""Encoded-file verification for the approved v14 repair."""
from pathlib import Path
import json
import re
import subprocess
import wave

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/hallucination-v14-2026-09-29'
FF=imageio_ffmpeg.get_ffmpeg_exe()


def samples(path, frames):
    expr='+'.join(f'eq(n,{n})' for n in sorted(set(frames)))
    raw=subprocess.check_output([FF,'-v','error','-threads','2','-i',str(path),
        '-vf',f"select='{expr}',scale=320:180",'-fps_mode','vfr',
        '-pix_fmt','rgb24','-f','rawvideo','-'])
    arr=np.frombuffer(raw,dtype=np.uint8).reshape(-1,180,320,3)
    assert len(arr)==len(set(frames)),(len(arr),len(set(frames)))
    return dict(zip(sorted(set(frames)),arr))


def main():
    m=json.loads((OUT/'edit-manifest.json').read_text()); dest=Path(m['candidate'])
    result=subprocess.run([FF,'-v','error','-threads','2','-i',str(dest),
                           '-progress','pipe:1','-f','null','-'],capture_output=True,text=True,check=True)
    assert not result.stderr.strip(),result.stderr
    decoded=int(re.findall(r'^frame=(\d+)$',result.stdout,re.M)[-1])
    assert decoded==m['total_frames'],decoded
    print('Full decode:',decoded,'frames',flush=True)
    frames=sorted(set(list(range(0,decoded,30))+[decoded-1]+[r['start_frame'] for r in m['timeline']]))
    got=samples(dest,frames)
    expected={}
    for n in frames:
        row=next(r for r in m['timeline'] if r['start_frame']<=n<r['end_frame'])
        va,vb=row['source_video']; length=row['end_frame']-row['start_frame']
        if length==vb-va: expected[n]=va+n-row['start_frame']
        elif vb-va==1: expected[n]=va
    original=samples(Path(m['source']),list(expected.values()))
    differences=[dict(output_frame=n,source_frame=s,
                      mean_absolute_difference=float(np.abs(got[n].astype(float)-original[s]).mean()))
                 for n,s in expected.items()]
    maximum=max(r['mean_absolute_difference'] for r in differences)
    assert maximum<3,maximum
    # Check decoded AAC against the exact approved PCM edit at every sample.
    pcm=subprocess.check_output([FF,'-v','error','-i',str(dest),'-vn','-ac','1','-ar','48000','-f','s16le','-'])
    actual=np.frombuffer(pcm,dtype='<i2').astype(float)
    with wave.open(str(OUT/'edited.wav')) as w:
        reference=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(float)
    assert len(actual)>=len(reference)
    actual=actual[:len(reference)]
    noise=float(np.sum((actual-reference)**2)); energy=float(np.sum(reference**2))
    snr=10*np.log10(energy/noise)
    assert snr>25,snr
    joins=[]
    for n in m['audio_join_output_frames']:
        s=n*1600; window=actual[s-240:s+240]/32768
        joins.append(dict(output_frame=n,time=n/30,
                          local_peak_dbfs=float(20*np.log10(max(np.max(np.abs(window)),1e-9))),
                          maximum_sample_step=float(np.max(np.abs(np.diff(window))))))
    # A readable overview plus the literal final decoded frame.
    sheet_frames=list(range(0,decoded,120))+[decoded-1]
    for sheet in range((len(sheet_frames)+11)//12):
        canvas=Image.new('RGB',(960,800),'white');draw=ImageDraw.Draw(canvas)
        for k,n in enumerate(sheet_frames[sheet*12:(sheet+1)*12]):
            x=(k%3)*320;y=(k//3)*200
            canvas.paste(Image.fromarray(got[n]),(x,y+20))
            draw.text((x+6,y+3),f'{int(n/30)//60}:{n/30%60:05.2f}  f{n}',fill='black')
        canvas.save(OUT/f'candidate-sheet-{sheet:02}.jpg',quality=90)
    Image.fromarray(got[decoded-1]).save(OUT/'final-frame.jpg')
    report=dict(decoded_frames=decoded,duration=decoded/30,
                comparison_samples=len(differences),maximum_visual_mean_absolute_difference=maximum,
                audio_comparison_snr_db=float(snr),audio_samples=len(reference),joins=joins,
                final_frame_source=expected[decoded-1],
                check_claim_longest_remaining_run_seconds=19.2666666667,
                whole_video_longest_board_run_seconds=(3490-2153)/30,
                listening='not auditioned; ASR and signal checks do not certify subjective sound')
    (OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    (OUT/'visual-comparison.json').write_text(json.dumps(differences,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)


if __name__=='__main__': main()

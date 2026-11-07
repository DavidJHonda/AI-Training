#!/usr/bin/env python3
"""Check encoded phase-focused candidate against the edit and canonical legs."""
import json,subprocess,wave
import av,cv2,numpy as np
from PIL import Image,ImageDraw,ImageFont
import build_how_ai_learns_v11 as b
from editspec_build import Reader,sha,readwav

def main():
    cv2.setNumThreads(2)
    m=json.loads((b.OUT/'edit-manifest.json').read_text());out=b.OUT/'encoded';out.mkdir(exist_ok=True)
    source=Reader(b.SRC);legs={k:Reader(b.OUT/f'leg-{k}.mkv') for k in m['boards']};legs['feedback']=Reader(b.OUT/'leg-feedback.mkv')
    samples=set(range(0,m['total_frames'],90))|{m['total_frames']-1}
    for edge in m['boundaries']:samples.update(range(edge['frame']-2,edge['frame']+3))
    for key,board in m['boards'].items():
        samples.add(board['src_in'])
        samples.update(board['src_in']+r['start']+26 for r in board['rings'])
    pts=[];errors=[];count=0
    with av.open(str(b.DEST)) as container:
        assert container.streams.video[0].average_rate==30
        for f,frame in enumerate(container.decode(video=0)):
            im=frame.to_ndarray(format='bgr24');assert im.shape==(720,1280,3)
            if f in samples:
                row=next(r for r in m['timeline'] if r['start_frame']<=f<r['end_frame'])
                key=row['visual']
                if key=='source':ref=source.at(row['source_start']+f-row['start_frame'])
                else:
                    start=b.mapped(5222) if key=='feedback' else m['boards'][key]['src_in']
                    ref=legs[key].at(f-start)
                mae=float(np.abs(cv2.resize(im,(320,180)).astype(float)-cv2.resize(ref,(320,180)).astype(float)).mean())
                errors.append(dict(frame=f,visual=key,mae=mae));assert mae<3,(f,key,mae)
                cv2.imwrite(str(out/f'frame-{f:05d}.jpg'),im)
            pts.append(float(frame.pts*frame.time_base));count+=1
    assert count==6114 and abs(pts[-1]-(count-1)/30)<1e-6
    assert np.max(np.abs(np.diff(pts)-1/30))<1e-6
    import imageio_ffmpeg
    ff=imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff,'-y','-v','error','-i',str(b.DEST),'-vn','-ac','1','-ar','48000','-c:a','pcm_s16le',str(b.OUT/'encoded.wav')],check=True)
    expected=readwav(b.OUT/'edited.wav');encoded=readwav(b.OUT/'encoded.wav')[:len(expected)]
    assert len(encoded)==len(expected)
    correlation=float(np.corrcoef(expected,encoded)[0,1]);assert correlation>.999
    joins=[]
    for cut in m['cuts']:
        n=cut['output_join']*1600;radius=240
        db=lambda a:float(20*np.log10(max(np.sqrt(np.mean(a*a)),.001)/32768))
        joins.append(dict(frame=cut['output_join'],seconds=cut['output_join']/30,edge_rms_dbfs=db(encoded[n-radius:n+radius]),label=cut['label']))
        assert joins[-1]['edge_rms_dbfs']<-45
    assert all(sha(p)==digest for p,digest in m['protected_hashes'].items())
    font=ImageFont.truetype(str(b.FONT),16)
    overview=sorted(f for f in samples if f%90==0 or f==m['total_frames']-1)
    changed=sorted({board['src_in'] for board in m['boards'].values()}|{board['src_in']+r['start']+26 for board in m['boards'].values() for r in board['rings']}|{b.mapped(5222)+30,b.mapped(5334)+30})
    # Feedback snapshots may not be in the routine sample set.
    c=cv2.VideoCapture(str(b.DEST))
    for f in changed:
        if not (out/f'frame-{f:05d}.jpg').exists():
            c.set(cv2.CAP_PROP_POS_FRAMES,f);ok,im=c.read();assert ok;cv2.imwrite(str(out/f'frame-{f:05d}.jpg'),im)
    c.release()
    for name,frames in [('overview',overview),('changed',changed)]:
        for page in range((len(frames)+15)//16):
            sheet=Image.new('RGB',(1280,800),'white');draw=ImageDraw.Draw(sheet)
            for j,f in enumerate(frames[page*16:page*16+16]):
                x=j%4*320;y=j//4*200;sheet.paste(Image.open(out/f'frame-{f:05d}.jpg').resize((320,180)),(x,y));draw.text((x+5,y+181),f'{f/30:.2f}s / f{f}',font=font,fill='black')
            sheet.save(b.OUT/f'encoded-{name}-{page}.jpg')
    args=[str(b.ROOT/'.video-venv/bin/python'),str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST),'--outdir',str(b.OUT/'transitions')]
    for edge in m['boundaries']:args.extend(['--boundary',str(edge['frame'])+':'+edge['label']])
    subprocess.run(args,check=True)
    result=dict(frames=count,duration=count/30,removed_seconds=(7382-count)/30,fps=30,continuous_video_timestamps=True,
                expected_picture_max_mae=max(e['mae'] for e in errors),expected_picture_sample_count=len(errors),
                encoded_audio_correlation=correlation,joins=joins,protected_files_unchanged=True,
                limitation='No continuous audiovisual listening. Encoded frame inspection, waveform/correlation checks, and fresh speech transcription are separate checks; human listen-through remains pending.')
    (b.OUT/'qa.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()

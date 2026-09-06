"""Final-output inspection assets: every highlight and every audio splice."""
import json
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw
import build_hallucination_review as build
from audio_gap_review import decode_audio, dbfs, write_wav


def main():
    qa=build.AUDIT/'qa'
    qa.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((build.AUDIT/'manifest.json').read_text())
    requests={s['output_frame']:s['name'].replace('/','-') for s in manifest['states']}
    requests[manifest['output_frames']-1]='literal-final-frame'
    cap=cv2.VideoCapture(str(build.OUTPUT))
    images=[]
    count=0
    while True:
        ok,frame=cap.read()
        if not ok: break
        if count in requests:
            name=requests[count]
            cv2.imwrite(str(qa/(name+'.png')),frame)
            images.append((count,name,Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))))
        count+=1
    cap.release()
    assert count==manifest['output_frames']
    for offset in range(0,len(images),4):
        group=images[offset:offset+4]
        sheet=Image.new('RGB',(1280,390*((len(group)+1)//2)),'white')
        draw=ImageDraw.Draw(sheet)
        for i,(f,name,im) in enumerate(group):
            x=(i%2)*640;y=(i//2)*390
            draw.text((x+8,y+6),f'{f/30:.2f}s {name}',fill='black')
            sheet.paste(im.resize((640,360)),(x,y+27))
        sheet.save(qa/f'states-{offset//4:02}.jpg')
    audio=decode_audio(build.OUTPUT)
    clips=[];seams=[]
    for i,cut in enumerate(manifest['cuts'],1):
        time=cut['output_frame']/30
        center=round(time*44100)
        clip=audio[center-round(3*44100):center+round(4*44100)]
        write_wav(qa/f'audio-cut-{i}.wav',clip)
        clips.extend((clip,np.zeros(11025,dtype=np.float32)))
        seams.append({'cut':i,'output_time':time,
            'seam_20ms_dbfs':dbfs(audio[center-441:center+441]),
            'sample_step':float(abs(audio[center]-audio[center-1]))})
    write_wav(qa/'all-cut-boundaries.wav',np.concatenate(clips))
    (qa/'audio-seams.json').write_text(json.dumps(seams,indent=2)+'\n')
    print(json.dumps({'frames':count,'seconds':count/30,'seams':seams},indent=2))


if __name__=='__main__': main()

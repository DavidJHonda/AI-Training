"""Build visual inspection sheets from this candidate's actual decoded frames."""
from pathlib import Path
import json
import cv2
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[2]
AUDIT=ROOT/'video-audit/make-your-move-2-review'
OUT=AUDIT/'qa-current'
OUT.mkdir(exist_ok=True)
manifest=json.loads((AUDIT/'edit-manifest.json').read_text())
for directory in ('transitions-current','motion-review'):
    report=json.loads((AUDIT/directory/'transition-guard.json').read_text())
    for offset in range(0,len(report['boundaries']),4):
        group=report['boundaries'][offset:offset+4]
        sheet=Image.new('RGB',(1600,480*len(group)), 'white')
        draw=ImageDraw.Draw(sheet)
        for row,boundary in enumerate(group):
            path=AUDIT/directory/boundary['strip']
            img=Image.open(path).convert('RGB')
            img.thumbnail((1600,450))
            sheet.paste(img,(0,row*480+28))
            draw.text((8,row*480+8),f"{boundary['frame']} {boundary['label']}",fill='black')
        sheet.save(OUT/f'{directory}-{offset//4:02}.jpg')

# Verify entire moves, not just the ±12 frames near their starting boundary.
def mapped(f):
    return f-sum(max(0,min(f,b)-a) for a,b in manifest['source_frame_cuts'])
requests={}
for state in manifest['states']:
    if state['move']:
        for step in (0,7,15,23,30):
            requests[mapped(state['start']+step)]=(state['label'],step)
cap=cv2.VideoCapture(str(ROOT/manifest['output']))
frames={}
for n in range(manifest['output_frames']):
    ok,frame=cap.read()
    assert ok
    if n in requests:
        frames[requests[n]]=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
cap.release()
moving=[s for s in manifest['states'] if s['move']]
for offset in range(0,len(moving),3):
    group=moving[offset:offset+3]
    sheet=Image.new('RGB',(1600,210*len(group)),'white')
    draw=ImageDraw.Draw(sheet)
    for row,state in enumerate(group):
        draw.text((8,row*210+5),state['label'],fill='black')
        for col,step in enumerate((0,7,15,23,30)):
            sheet.paste(frames[(state['label'],step)].resize((320,180)),(col*320,row*210+25))
    sheet.save(OUT/f'complete-moves-{offset//3:02}.jpg')

# Settled highlights at reviewable size, pulled from renderer final state.
states=[s for s in manifest['states'] if s['rect']]
for offset in range(0,len(states),6):
    group=states[offset:offset+6]
    sheet=Image.new('RGB',(1920,570*((len(group)+1)//2)),'white')
    draw=ImageDraw.Draw(sheet)
    for i,state in enumerate(group):
        x=(i%2)*960;y=(i//2)*570
        draw.text((x+8,y+5),state['label'],fill='black')
        img=Image.open(AUDIT/'highlight-previews'/f"{state['label']}.jpg")
        sheet.paste(img.resize((960,540)),(x,y+25))
    sheet.save(OUT/f'highlights-{offset//6:02}.jpg')
print(OUT)

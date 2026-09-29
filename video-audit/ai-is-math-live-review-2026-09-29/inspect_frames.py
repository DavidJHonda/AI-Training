from pathlib import Path
import cv2,json
from PIL import Image,ImageDraw
out=Path(__file__).parent; (out/'details').mkdir(exist_ok=True)
times=[44.54,46.6,54.5,61.14,63.2,71,78,82,118.3,120.3,128,133,136,148.4,150,152,154,155,156,158,160,162,163.3,165.4,168.5,174,180,187,190,193,196,198.14,200,204,206.1]
frames={round(t*30):t for t in times}
cap=cv2.VideoCapture('course-assets/ai-is-math/ai-is-math.mp4'); i=0
while True:
 ok,frame=cap.read()
 if not ok:break
 if i in frames: cv2.imwrite(str(out/'details'/f'{frames[i]:07.2f}.jpg'),frame)
 i+=1
cap.release()
(out/'decode.json').write_text(json.dumps({'frames':i,'fps':30,'duration':i/30},indent=2))
paths=[p for p in sorted((out/'details').glob('*.jpg')) if 148<=float(p.stem)<=163]
sheet=Image.new('RGB',(1280,384*((len(paths)+1)//2)), 'white'); d=ImageDraw.Draw(sheet)
for n,p in enumerate(paths):
 x=n%2*640;y=n//2*384; im=Image.open(p); im.thumbnail((640,360));sheet.paste(im,(x,y+24));d.text((x+5,y+4),p.stem,fill='black')
sheet.save(out/'bridge-sequence.jpg')
print(i,'frames decoded')

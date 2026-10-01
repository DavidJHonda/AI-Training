from pathlib import Path
import sys
from PIL import Image,ImageDraw
root=Path('/Users/davidobrien/Developer/AI-Training')
sys.path.insert(0,str(root/'scripts/video'))
from editorial_typography import draw_inner_title
for rel,old,new in [('scripts/video/render_editorial_full_bleed_batch.py','"Create and Solve Problems"','"Create and Solve"'),('index.html','Create and solve problems','Create and solve'),('lessons/make-your-move.md','Create and solve problems:','Create and solve:')]:
 p=root/rel;s=p.read_text();assert old in s;p.write_text(s.replace(old,new))
p=root/'course-assets/make-your-move/make-your-move-skills.jpg'
im=Image.open(p).convert('RGB');d=ImageDraw.Draw(im)
d.rectangle((64,1114,748,1179),fill='white')
draw_inner_title(d,(74,1121),'Create and Solve',fill='#0e8f86')
im.save(p,quality=95,subsampling=0,optimize=True)

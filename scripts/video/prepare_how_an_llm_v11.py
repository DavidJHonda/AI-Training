"""Inspect narrowly selected existing drawing donors, without changing sources."""
from pathlib import Path
import cv2
import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'video-audit/how-an-llm-works-repair-2026-09-17-v11/source-checks'

def main():
    for name,seconds in [('how-the-model-learns-2',range(150,171)),
                         ('how-an-llm-works-reroll-2',range(93,103))]:
        path=ROOT/'Prompts'/f'{name}.mp4'
        if not path.exists():
            print('Missing:',path,flush=True);continue
        dest=OUT/name;dest.mkdir(parents=True,exist_ok=True)
        want={round(t*30) for t in seconds};cells=[]
        c=cv2.VideoCapture(str(path))
        for f in range(max(want)+1):
            ok,im=c.read();assert ok
            if f not in want:continue
            cv2.imwrite(str(dest/f'f{f:05d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,96])
            cell=cv2.resize(im,(480,270));cv2.putText(cell,f'{f/30:.2f}s f{f}',(8,25),cv2.FONT_HERSHEY_SIMPLEX,.65,(0,0,200),2);cells.append(cell)
        c.release()
        for i in range(0,len(cells),9):
            chunk=cells[i:i+9]
            while len(chunk)%3:chunk.append(np.zeros_like(cells[0]))
            cv2.imwrite(str(dest/f'sheet-{i//9}.jpg'),cv2.vconcat([cv2.hconcat(chunk[k:k+3]) for k in range(0,len(chunk),3)]))
        print('Inspected',name,flush=True)

if __name__=='__main__':main()

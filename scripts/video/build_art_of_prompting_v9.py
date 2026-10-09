#!/usr/bin/env python3
"""Approved narrow v8 visual repair. Copy audio; preserve timeline and motion."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/art-of-prompting-build-2026-09-29-v9'
SOURCE = ROOT / 'Prompts/art-of-prompting-v8.mp4'
DEST = ROOT / 'Prompts/art-of-prompting-v9.mp4'
SHA = '9805eddcd0e97de5a683c2751034e3a7c44a81d13d91a11e1543b1eda6414ad6'
SPANS = [(3447, 3730), (4304, 4489), (6467, 6936)]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TrackedRepair:
    def __init__(self, reference, boxes):
        self.reference = reference
        self.orb = cv2.ORB_create(nfeatures=2000)
        self.kp, self.des = self.orb.detectAndCompute(reference, None)
        gray = cv2.cvtColor(reference, cv2.COLOR_BGR2GRAY)
        region = np.zeros(gray.shape, np.uint8)
        for x, y, w, h in boxes:
            region[y:y+h, x:x+w] = 255
        self.mask = cv2.dilate(((gray < 150) & (region > 0)).astype(np.uint8)*255,
                               np.ones((3, 3), np.uint8))
        self.min_inliers = 99999

    def apply(self, frame, clone_paper=False):
        kp, des = self.orb.detectAndCompute(frame, None)
        matches = cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(self.des, des, k=2)
        good = [m for m,n in matches if m.distance < .72*n.distance]
        assert len(good) >= 30, len(good)
        src = np.float32([self.kp[m.queryIdx].pt for m in good])
        dst = np.float32([kp[m.trainIdx].pt for m in good])
        matrix, inliers = cv2.findHomography(src, dst, cv2.RANSAC, 2.0)
        n = int(inliers.sum())
        assert n >= 25, n
        self.min_inliers = min(self.min_inliers, n)
        mask = cv2.warpPerspective(self.mask, matrix, (1280,720), flags=cv2.INTER_NEAREST)
        if clone_paper:
            # Long narrow cursor: nearby same-frame paper preserves grain and
            # avoids the pale streak produced by diffusion across its length.
            donor = cv2.warpAffine(frame, np.float32([[1,0,-45],[0,1,0]]), (1280,720))
            alpha = cv2.GaussianBlur(cv2.dilate(mask,np.ones((3,3),np.uint8)),(5,5),.8)[:,:,None]/255
            clean = np.rint(frame*(1-alpha)+donor*alpha).astype(np.uint8)
        else:
            clean = cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)
        return clean, matrix


def overlay_layer(header=False):
    up = 3
    im = Image.new('RGBA', (1280*up,720*up))
    d = ImageDraw.Draw(im)
    if header:
        font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 20*up)
        d.text((255*up,245*up), 'WEAK PROMPT', font=font, fill=(76,65,64,255))
    else:
        font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 40*up)
        for y, line in [(312,'Write a caption for our lacrosse'),(369,'championship photo.')]:
            d.text((255*up,y*up),line,font=font,fill=(35,39,40,255))
    arr = np.array(im.resize((1280,720), Image.Resampling.LANCZOS))
    return arr[:,:,[2,1,0,3]]


def composite(frame, layer, matrix, opacity=1):
    warped = cv2.warpPerspective(layer, matrix, (1280,720), flags=cv2.INTER_LINEAR)
    alpha = warped[:,:,3:4].astype(np.float32)/255*opacity
    return np.rint(frame*(1-alpha)+warped[:,:,:3]*alpha).astype(np.uint8)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--preview',action='store_true');args=ap.parse_args()
    assert sha(SOURCE)==SHA
    assert args.preview or not DEST.exists(), 'Never overwrite a review candidate'
    OUT.mkdir(exist_ok=True,parents=True)
    doc = TrackedRepair(cv2.imread(str(OUT/'source-3590.png')),
                        [(653,284,79,81),(654,475,79,80),(1200,270,77,88)])
    paper = TrackedRepair(cv2.imread(str(OUT/'source-4395.png')),[(216,211,28,89)])
    header, text = overlay_layer(True), overlay_layer(False)
    close = cv2.imread(str(OUT/'close-canvas.png'))
    cap=cv2.VideoCapture(str(SOURCE))
    if not args.preview:
        ff=imageio_ffmpeg.get_ffmpeg_exe()
        proc=subprocess.Popen([ff,'-v','error','-n','-f','rawvideo','-pix_fmt','bgr24',
            '-s','1280x720','-r','30','-i','pipe:0','-i',str(SOURCE),'-map','0:v:0','-map','1:a:0',
            '-c:v','libx264','-crf','16','-preset','medium','-threads','4','-pix_fmt','yuv420p',
            '-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    targets={3447,3590,3729,4304,4391,4395,4403,4488,6467,6514,6664,6935}
    i=0
    while True:
        ok, frame=cap.read()
        if not ok:break
        if args.preview and i not in targets:
            i+=1;continue
        if 3447<=i<3730:
            frame,_=doc.apply(frame)
        elif 4304<=i<4489:
            frame,matrix=paper.apply(frame,clone_paper=True)
            frame=composite(frame,header,matrix)
            # Sentence begins about 2:26.4; lead-in already has its label.
            if i>=4392:
                frame=composite(frame,text,matrix,min(1,(i-4392+1)/6))
        elif 6467<=i<6936:
            j=i-6467
            t=max(0,min(1,(j-48)/149))
            z=1+.2*t*t*(3-2*t)
            width=3840/z; height=2160/z
            x=(3840-width)/2; y=(2160-height)/2
            # Subpixel camera mapping from the untouched canonical canvas.
            m=np.float32([[1280/width,0,-x*1280/width],[0,720/height,-y*720/height]])
            frame=cv2.warpAffine(close,m,(1280,720),flags=cv2.INTER_LANCZOS4)
        if i in targets:
            cv2.imwrite(str(OUT/f'{"preview" if args.preview else "render"}-{i}.jpg'),frame)
        if not args.preview:proc.stdin.write(frame.tobytes())
        i+=1
    cap.release()
    assert i==6936,i
    if not args.preview:
        proc.stdin.close();assert proc.wait()==0
        record={'source':str(SOURCE),'source_sha256':SHA,'candidate':str(DEST),
                'candidate_sha256':sha(DEST),'frames':i,'fps':30,'duration':i/30,
                'changed_spans':SPANS,'audio':'copied AAC stream; no audio edits',
                'document_min_tracking_inliers':doc.min_inliers,'paper_min_tracking_inliers':paper.min_inliers,
                'close_asset_sha256':sha(ROOT/'course-assets/prompting-matters/prompting-matters-close.jpg'),
                'source_limitation':'Only finished v8 used; one additional picture encode at CRF16. Raw rolls unavailable.'}
        (OUT/'manifest.json').write_text(json.dumps(record,indent=2)+'\n')
        print(json.dumps(record,indent=2))


if __name__=='__main__':main()

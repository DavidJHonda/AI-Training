#!/usr/bin/env python3
"""Render Big Upside's concise protein comparison using canonical course typography.

The text-free art was created with the built-in image generator. Prompt:
One compact conceptual folded protein, classic scientific ribbon cartoon with
alpha helices, beta sheets and connecting loops; soft 3D violet/teal/blue render
on white; square, centered, generous margins. No people, DNA helix, atoms, text,
labels, frame or logos. Not a claimed specific molecule.

Sources: https://www.ebi.ac.uk/about/news/perspectives/alphafold-using-open-data-and-ai-to-discover-the-3d-protein-universe/
https://www.ebi.ac.uk/about/news/technology-and-innovation/alphafold-200-million/

Run with --art for the first build. Later builds reuse the finished board's art
panel, so no additional source illustration needs to live in course-assets.
"""
from pathlib import Path
import argparse
from PIL import Image, ImageDraw, ImageOps
from editorial_typography import ROOT, draw_board_title, draw_inner_title, face
from editorial_takeaway import draw_takeaway_band
from course_credit import save_course_image

OUTPUT = ROOT/'course-assets/big-upside/big-upside-protein.jpg'
ART_BOX = (76, 138, 354, 416)
TITLE = 'A New Scale for Science'
SHAPE = 'A protein’s shape helps determine what it does.'
TAKEAWAY = 'Shared freely to help scientists study disease and develop medicines.'

def render(art=None):
    if art:
        with Image.open(art) as src:
            protein = ImageOps.contain(src.convert('RGB'), (278,278), Image.Resampling.LANCZOS)
    else:
        with Image.open(OUTPUT) as src:
            if src.size != (1600,930):
                raise ValueError('First build requires --art; current board is not the simplified layout.')
            protein = src.crop(ART_BOX).convert('RGB')
    image = Image.new('RGB',(1600,930),'white')
    d=ImageDraw.Draw(image)
    d.rounded_rectangle((0,0,1599,929),radius=22,fill='#eae7fd')
    draw_board_title(d,TITLE)
    d.rounded_rectangle((40,127,1560,428),radius=14,fill='white')
    image.paste(protein,(76,138))
    for y,line in [(207,'A protein’s shape helps determine'),(261,'what it does.')]:
        d.text((412,y),line,font=face('bold',40),fill='#0e0a1f',anchor='la')
    for x,label,number,lines,color in [
        (40,'Experiments','About 200,000',['protein structures determined','through decades of experiments.'],'#4f2fc4'),
        (820,'AlphaFold','Over 200 million',['protein structures predicted','and shared free.'],'#1652f0')]:
        d.rounded_rectangle((x,460,x+740,762),radius=14,fill='white')
        draw_inner_title(d,(x+34,486),label,fill=color)
        f=face('bold',64)
        assert d.textlength(number,font=f)<672
        d.text((x+34,547),number,font=f,fill=color,anchor='la')
        for i,line in enumerate(lines):
            assert d.textlength(line,font=face('medium',29))<672
            d.text((x+34,646+i*41),line,font=face('medium',29),fill='#3a3550',anchor='la')
    draw_takeaway_band(image,top=802,left=40,right=1560,text=TAKEAWAY,font=face('medium',32))
    return image

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--art',type=Path)
    parser.add_argument('--output',type=Path,default=OUTPUT)
    args=parser.parse_args()
    image=render(args.art)
    save_course_image(image,args.output,quality=95,subsampling=0,optimize=True)
    print(args.output)

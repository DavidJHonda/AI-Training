"""Render one RGB frame of the date-free model release cutaway at 30 fps."""
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
S = 2
INK = '#242137'
FONT = Path(__file__).resolve().parents[1] / 'fonts' / 'PlusJakartaSans-wght.ttf'
PALETTES = [
    ('#e6dedf', '#a8474e', '#f3dada'),
    ('#dedeea', '#625291', '#e8e4fc'),
    ('#d4e5dc', '#2d7369', '#e0f2e8'),
]


@lru_cache(None)
def font(size, weight):
    face = ImageFont.truetype(str(FONT), size * S)
    face.set_variation_by_axes([weight])
    return face


def box(x, y, r, b):
    return tuple(round(v * S) for v in (x, y, r, b))


def points(coords):
    return [(round(x * S), round(y * S)) for x, y in coords]


def centered(draw, x, y, text, size, weight=600, fill=INK):
    draw.text(points([(x, y)])[0], text, font=font(size, weight),
              anchor='mm', fill=fill)


def trace(draw, coords, color, width):
    draw.line(points(coords), fill=color, width=width*S, joint='curve')


@lru_cache(None)
def tile(index):
    # A printed circuit package, with a different circuit pattern for each release.
    pale, accent, light = PALETTES[index]
    im = Image.new('RGBA', (272*S, 277*S))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box(8, 9, 269, 272), radius=17*S, fill=INK)
    d.rounded_rectangle(box(1, 1, 262, 264), radius=17*S, fill=pale, outline=INK, width=3*S)
    for x in range(16, 251, 7):
        for y in range(17, 185, 7):
            if x+y<105 or x+y>370:
                d.ellipse(box(x,y,x+1.3,y+1.3),fill=accent)
    cx, cy = 131, 104
    for k in range(-36, 37, 12):
        for side in (-1, 1):
            trace(d, [(cx+k,cy+side*46),(cx+k,cy+side*59)], INK, 4)
            trace(d, [(cx+side*46,cy+k),(cx+side*59,cy+k)], INK, 4)
    d.rounded_rectangle(box(cx-46,cy-46,cx+46,cy+46),radius=9*S,fill=accent,outline=INK,width=3*S)
    d.rounded_rectangle(box(cx-33,cy-33,cx+33,cy+33),radius=5*S,outline=light,width=2*S)
    paths = [
        [[(-20,-14),(-6,-14),(6,0),(20,0)],[(-20,14),(-5,14),(5,4)]],
        [[(-20,14),(-9,14),(-9,-12),(12,-12)],[(2,15),(2,1),(20,1)]],
        [[(-20,6),(-10,6),(4,-8),(19,-8)],[(-16,-13),(-7,-13),(6,11),(20,11)]],
    ]
    for path in paths[index]:
        trace(d,[(cx+x,cy+y) for x,y in path],light,3)
        for x,y in (path[0],path[-1]):
            d.ellipse(box(cx+x-3,cy+y-3,cx+x+3,cy+y+3),fill=light)
    trace(d,[(19,190),(244,190)],INK,2)
    centered(d,131,226,'Released',31,730)
    return im


@lru_cache(None)
def paper():
    rng = np.random.default_rng(13)
    grain = rng.normal(0, 1.6, (H, W, 1))
    bg = Image.fromarray(np.clip(np.array([243,239,228])+grain,0,255).astype('uint8'))
    im = bg.convert('RGBA').resize((W*S,H*S),Image.Resampling.BILINEAR)
    d=ImageDraw.Draw(im)
    centered(d,640,156,'New models, months apart',64,770)
    return im


def frame(n):
    im = paper().copy()
    for i,(x,start) in enumerate(zip((108,508,908),(0,37,75))):
        if n < start:
            break
        t = min(1, (n-start+1)/12) if i else 1
        ease = 1-(1-t)**3
        if i:
            d=ImageDraw.Draw(im)
            left=x-99; tip=left+round(69*ease); y=385
            trace(d,[(left,y),(tip,y)],INK,4)
            if t>0.45:
                trace(d,[(tip-10,y-8),(tip,y),(tip-10,y+8)],INK,4)
        card=tile(i)
        if ease<1:
            card=card.copy()
            card.putalpha(card.getchannel('A').point(lambda a: round(a*ease)))
        im.alpha_composite(card,(x*S, round((278+22*(1-ease))*S)))
    return im.convert('RGB').resize((W,H),Image.Resampling.LANCZOS)

#!/usr/bin/env python3
"""Draw a text-only upload stand-in; canonical artwork is never modified."""
from pathlib import Path
from PIL import Image, ImageDraw
from editorial_typography import face

ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT / 'gemini-notebook/hallucination/assets/hallucination-glue-on-pizza-faceless.jpg'


def centered(draw, text, x, y, width, size, color, weight='bold'):
    font = face(weight, size)
    assert draw.textlength(text, font=font) <= width, text
    draw.text((x + (width-draw.textlength(text, font=font))/2, y), text, font=font, fill=color)


def main():
    with Image.open(ROOT/'course-assets/hallucination/hallucination-glue-on-pizza.jpg') as canonical:
        size = canonical.size
    assert size == (1387, 1134), 'Recheck layout if canonical dimensions change'
    image = Image.new('RGB', size, '#eae7fd')
    draw = ImageDraw.Draw(image)
    draw.text((34, 28), 'Real Text. Wrong Meaning.', font=face('bold', 52), fill='#141025')
    draw.rounded_rectangle((34, 127, 1353, 985), 18, fill='white')
    cards = [(76,'Real joke','#4f2fc4'), (528,'AI misreads it','#1652f0'), (980,'Wrong advice','#0e8f86')]
    for x,title,color in cards:
        draw.rounded_rectangle((x,400,x+331,652),18,fill='#f3f1fc')
        centered(draw,title,x,499,331,32,color)
    for x in (427,879):
        draw.line((x,526,x+77,526),fill='#625d75',width=6)
        draw.polygon([(x+77,526),(x+61,515),(x+61,537)],fill='#625d75')
    draw.rounded_rectangle((34,1018,1353,1095),16,fill='#ffe4a2')
    centered(draw,'The Reddit comment was real. The cooking advice was not.',
             50,1036,1287,30,'#141025','medium')
    DEST.parent.mkdir(parents=True,exist_ok=True)
    image.save(DEST,quality=95,subsampling=0)
    print(f'{DEST}: {size[0]}x{size[1]}')


if __name__ == '__main__': main()

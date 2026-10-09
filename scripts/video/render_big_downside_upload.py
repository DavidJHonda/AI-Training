#!/usr/bin/env python3
"""Render the text-only jailbreak upload; the canonical illustration stays intact."""
from PIL import Image, ImageDraw
from editorial_typography import ROOT, face

SOURCE = ROOT / 'course-assets/big-downside/big-downside-jailbreak.jpg'
OUTPUT = ROOT / 'gemini-notebook/big-downside/assets/big-downside-jailbreak-faceless.jpg'


def render():
    with Image.open(SOURCE) as source:
        width, height = source.size
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, width-1, height-1), radius=22, fill='#eae7fd')
    title = 'Why Jailbreaks Keep Appearing'
    draw.text((34, 26), title, font=face('bold', 48), fill='#0e0a1f')
    draw.text((width/2, 154), 'Guardrails', font=face('bold', 30), fill='#625c7a', anchor='mt')
    panels = [
        ((64, 230, width-64, 505), ['Defenders must protect', 'many paths.'], '#4f2fc4'),
        ((64, 555, width-64, 830), ['An attacker needs only', 'one opening.'], '#1652f0'),
    ]
    for box, lines, color in panels:
        draw.rounded_rectangle(box, radius=18, fill='white')
        top = (box[1]+box[3])/2 - 64
        for i, line in enumerate(lines):
            draw.text((width/2, top+i*68), line, font=face('bold', 50), fill=color, anchor='mt')
    draw.rounded_rectangle((34, height-119, width-34, height-42), radius=14, fill='#ffe69b')
    takeaway = 'New methods keep surfacing, making this an ongoing game of cat-and-mouse.'
    font=face('medium', 29)
    assert draw.textlength(takeaway, font=font) < width-110
    draw.text((width/2, height-83), takeaway, font=font, fill='#0e0a1f', anchor='mm')
    draw.text((width-34,height-12),'besmarterthanthetool.com',font=face('medium',18),fill='#625c7a',anchor='rd')
    return image


if __name__ == '__main__':
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    render().save(OUTPUT, 'JPEG', quality=95, subsampling=0, optimize=True, progressive=True)
    print(OUTPUT)

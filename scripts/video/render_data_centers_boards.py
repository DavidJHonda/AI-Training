#!/usr/bin/env python3
"""Canonical Data Centers EE-3FB demand board."""
from pathlib import Path
from PIL import Image, ImageDraw
from editorial_typography import face, draw_board_title, draw_inner_title
from editorial_takeaway import draw_takeaway_band
from render_editorial_full_bleed_batch import Board, render
from course_credit import save_course_image
ROOT=Path(__file__).resolve().parents[2]
FRAME='#eae7fd'; INK='#0e0a1f'; BODY='#3a3550'; PURPLE='#4f2fc4'; BLUE='#1652f0'; TEAL='#0e8f86'

def demand():
    return render(Board(key='data-centers-demand',title='Meeting the Demand',cards=(
        ('More Power','Companies are arranging additional electricity supplies for their data centers.'),
        ('Better Cooling','Some cooling designs reuse water, reducing how much new water they need.'),
        ('More Efficient Chips','Better chips can do more work with each unit of electricity.'),
    ),art_sheet='scripts/video/assets/editorial-full-bleed/data-centers-demand/art-sheet.png',page_output='course-assets/data-centers/data-centers-meeting-demand.jpg',prep_output='course-assets/data-centers/data-centers-meeting-demand.jpg',accents=(PURPLE,BLUE,TEAL),takeaway='More power meets demand. Better efficiency reduces the resources needed per task.'))

if __name__=='__main__':
    for name,im in [('meeting-demand',demand())]:
        ImageDraw.Draw(im).text((1560,im.height-10),'besmarterthanthetool.com',font=face('medium',20),fill='#625c7a',anchor='rd')
        path=ROOT/f'course-assets/data-centers/data-centers-{name}.jpg'
        save_course_image(im,path,'JPEG',quality=95,subsampling=0,optimize=True)
        print(f'{path}: {im.size}')

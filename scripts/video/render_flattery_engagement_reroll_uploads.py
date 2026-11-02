#!/usr/bin/env python3
"""Render text-only upload boards from their native layout and original copy.

No canonical bitmap is edited. Blank art sheets let the existing board renderer
preserve text, geometry, dimensions and diagram relationships without faces.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
from render_avoid_traps_editorial import (ROOT,CompareSide,render_comparison,Card,FlowBoard,
 render_flow_board_with_title_size,AMBER,BLUE,PURPLE,TEAL)
from course_credit import save_course_image
OUT=ROOT/'gemini-notebook/flattery-engagement/assets'

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 with TemporaryDirectory(prefix='flattery-text-boards-') as tmp:
  art=Path(tmp)/'blank-art.png';Image.new('RGB',(1800,600),'white').save(art)
  comparison=render_comparison('Flattery vs. Useful Feedback',
   'You ask AI to evaluate this Great Gatsby essay introduction:\n“The American Dream is something that many people have thought about over the years. Some people achieve it and some don’t. In The Great Gatsby, Fitzgerald explores this idea.”',
   (CompareSide('THE TRAP','Flattery','“Great start! You’ve clearly identified the central theme. This is a strong foundation.”',
    (('PRAISED','The work without pointing to evidence.'),('COULD FIT','Almost any Gatsby essay.'),('RESULT','False praise for a weak essay intro.')),AMBER),
    CompareSide('WHAT YOU NEED','Useful Feedback','“Right topic, but this needs work. The opening is filler, and you still need a thesis.”',
    (('PRAISED','The topic and nothing more.'),('NAMED','The missing thesis.'),('RESULT','A specific next move.')),BLUE)),str(art),
   'Good feedback improves the work. Empty praise only improves the feeling.')
  flow=render_flow_board_with_title_size(FlowBoard('praise-flow','How the Praise Got Baked In',
   (Card('People Rank','Reviewers compare answers and choose the ones they prefer.'),
    Card('Agreement Can Win','Positive, confident, agreeable answers can feel better in the moment.'),
    Card('Numbers Move','Training pushes the model toward patterns that earned approval.')),
   str(art),'','',(PURPLE,BLUE,TEAL)),31)
  for im,name,size in [(comparison,'flattery-engagement-feedback-comparison-faceless.jpg',(1600,1582)),(flow,'flattery-engagement-cycle-of-praise-faceless.jpg',(1600,751))]:
   assert im.size==size,(name,im.size,size)
   save_course_image(im,OUT/name,quality=95,subsampling=0,optimize=True)
   print(name,im.size)
if __name__=='__main__':main()

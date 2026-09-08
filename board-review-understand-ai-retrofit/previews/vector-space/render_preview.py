"""Frame the illustrated preview using the course's standard board helpers."""
import importlib.util
import sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
spec = importlib.util.spec_from_file_location('board_renderer', ROOT / 'scripts/video/render_understand_ai_retrofit_review.py')
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
art = Image.open(HERE / 'context-journey-art-v2.png').convert('RGB')
art_width = 1520
art_height = round(art.height * art_width / art.width)
stage_top = 127
banner_top = stage_top + art_height + m.TAKEAWAY_GAP
height = banner_top + m.TAKEAWAY_HEIGHT + m.TAKEAWAY_BOTTOM_PADDING
canvas = Image.new('RGB', (m.WIDTH, height), m.FRAME)
draw = ImageDraw.Draw(canvas)
m.draw_board_title(draw, 'How Context Changes IT’s Position')
art = art.resize((art_width, art_height), Image.Resampling.LANCZOS)
canvas.paste(art, (40, stage_top), m.rounded_mask(art.size, 14))
m.draw_takeaway_band(canvas, top=banner_top, left=40, right=1560,
    text='IT’s new position reflects its connection to CAT in this sentence.',
    font=m.face('medium', m.TAKEAWAY_TEXT_SIZE))
m.save(canvas, HERE / 'context-journey-standard-preview.jpg')

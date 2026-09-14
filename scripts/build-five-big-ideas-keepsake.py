#!/usr/bin/env python3
"""Build the downloadable Five Big Ideas keepsake image and PDF."""

from pathlib import Path
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import Color, HexColor
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "illustrations" / "five-big-ideas-keepsake-art-clean.png"
PNG = ROOT / "illustrations" / "five-big-ideas-keepsake.png"
PDF = ROOT / "lessons" / "five-big-ideas-keepsake.pdf"

NAVY = "#17367f"
GOLD = "#f4bd32"
INK = "#0d0820"
CREAM = "#fffaf0"
MUTED = "#4b4862"

TITLE = "Five Big Ideas to Take With You"
CLOSING = "Now you’re smarter than the tool."
IDEAS = [
    "AI predicts. It doesn’t think.",
    "Fluent isn’t the same as true.",
    "The more you know, the more it gives.",
    "You make the call.",
    "The better AI gets, the more you matter.",
]

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def fit_art(width: int, height: int) -> Image.Image:
    art = Image.open(ART).convert("RGB")
    scale = max(width / art.width, height / art.height)
    resized = art.resize((round(art.width * scale), round(art.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int):
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = word if not current else current + " " + word
        if draw.textbbox((0, 0), candidate, font=font)[2] <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_panel(draw, box, number, text, font):
    x, y, w, h = box
    draw.rounded_rectangle((x, y, x + w, y + h), radius=28, fill=(255, 250, 240, 238), outline=(244, 189, 50, 225), width=3)
    badge_r = 34
    badge_x, badge_y = x + 30 + badge_r, y + h // 2
    draw.ellipse((badge_x - badge_r, badge_y - badge_r, badge_x + badge_r, badge_y + badge_r), fill=GOLD)
    number_font = ImageFont.truetype(FONT_BOLD, 28)
    number_box = draw.textbbox((0, 0), str(number), font=number_font)
    draw.text((badge_x - (number_box[2] - number_box[0]) / 2, badge_y - (number_box[3] - number_box[1]) / 2 - 2), str(number), fill=NAVY, font=number_font)
    lines = wrap(draw, text, font, w - 145)
    line_height = font.size * 1.25
    start_y = y + (h - len(lines) * line_height) / 2
    for i, line in enumerate(lines):
        draw.text((x + 110, start_y + i * line_height), line, fill=INK, font=font)


def build_png():
    width, height = 1600, 2400
    poster = Image.new("RGB", (width, height), NAVY)
    poster.paste(fit_art(width, 2080), (0, 220))
    draw = ImageDraw.Draw(poster, "RGBA")
    title_font = ImageFont.truetype(FONT_BOLD, 72)
    idea_font = ImageFont.truetype(FONT_BOLD, 48)
    idea_font_compact = ImageFont.truetype(FONT_BOLD, 44)
    closing_font = ImageFont.truetype(FONT_BOLD, 43)

    draw.rectangle((0, 0, width, 220), fill=NAVY)
    draw.text((80, 68), TITLE, fill="white", font=title_font)

    panels = [
        (1000, 260, 540, 210),
        (55, 590, 650, 200),
        (960, 940, 580, 205),
        (55, 1320, 610, 200),
        (80, 2110, 1440, 160),
    ]
    for i, (box, text) in enumerate(zip(panels, IDEAS), 1):
        draw_panel(draw, box, i, text, idea_font_compact if i == 3 else idea_font)

    draw.rectangle((0, 2300, width, height), fill=NAVY)
    closing_box = draw.textbbox((0, 0), CLOSING, font=closing_font)
    closing_width = closing_box[2] - closing_box[0]
    draw.text(((width - closing_width) / 2, 2322), CLOSING, fill=GOLD, font=closing_font)
    poster.save(PNG, "PNG", optimize=True)


def pdf_wrap(c, text, font_name, font_size, max_width):
    words, lines, current = text.split(), [], ""
    for word in words:
        candidate = word if not current else current + " " + word
        if pdfmetrics.stringWidth(candidate, font_name, font_size) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def pdf_number_badge(number):
    """Rasterize the decorative number so PDF reading order stays with the idea text."""
    badge = Image.new("RGBA", (88, 88), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)
    draw.ellipse((0, 0, 87, 87), fill=GOLD)
    font = ImageFont.truetype(FONT_BOLD, 36)
    box = draw.textbbox((0, 0), str(number), font=font)
    draw.text(((88 - (box[2] - box[0])) / 2, (88 - (box[3] - box[1])) / 2 - 4), str(number), fill=NAVY, font=font)
    stream = BytesIO()
    badge.save(stream, "PNG")
    stream.seek(0)
    return ImageReader(stream)


def build_pdf():
    pdfmetrics.registerFont(TTFont("PosterSans", FONT_REGULAR))
    pdfmetrics.registerFont(TTFont("PosterSansBold", FONT_BOLD))
    page_w, page_h = letter
    c = canvas.Canvas(str(PDF), pagesize=letter, pageCompression=1)
    c.setTitle(TITLE)

    c.setFillColor(HexColor(NAVY))
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    art_y, art_h = 38, 682
    c.drawImage(ImageReader(str(ART)), 0, art_y, width=page_w, height=art_h, preserveAspectRatio=False, mask="auto")
    c.setFillColor(HexColor(NAVY))
    c.rect(0, 720, page_w, 72, fill=1, stroke=0)
    c.setFont("PosterSansBold", 23)
    c.setFillColorRGB(1, 1, 1)
    c.drawString(28, 744, TITLE)

    # Coordinates mirror the downloadable image, converted into the PDF's art area.
    panels = [
        (405, 628, 185, 70),
        (20, 511, 250, 70),
        (400, 389, 190, 74),
        (20, 282, 260, 70),
        (30, 50, 552, 64),
    ]
    for i, ((x, y, w, h), text) in enumerate(zip(panels, IDEAS), 1):
        c.setFillColor(Color(1, 0.98, 0.94, alpha=0.94))
        c.setStrokeColor(HexColor(GOLD))
        c.roundRect(x, y, w, h, 10, fill=1, stroke=1)
        c.drawImage(pdf_number_badge(i), x + 9, y + h / 2 - 11, width=22, height=22, mask="auto")
        font_size = 11 if i in (1, 3) else (13 if i < 5 else 15)
        lines = pdf_wrap(c, text, "PosterSansBold", font_size, w - 54)
        c.setFillColor(HexColor(INK))
        c.setFont("PosterSansBold", font_size)
        line_height = font_size * 1.22
        text_y = y + h / 2 + (len(lines) - 1) * line_height / 2 - 4
        for line in lines:
            c.drawString(x + 38, text_y, line)
            text_y -= line_height

    c.setFillColor(HexColor(NAVY))
    c.rect(0, 0, page_w, 38, fill=1, stroke=0)
    c.setFillColor(HexColor(GOLD))
    c.setFont("PosterSansBold", 16)
    c.drawCentredString(page_w / 2, 14, CLOSING)
    c.showPage()
    c.save()


if __name__ == "__main__":
    build_png()
    build_pdf()
    print(PNG)
    print(PDF)

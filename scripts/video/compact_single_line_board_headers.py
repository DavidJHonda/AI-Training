#!/usr/bin/env python3
"""Normalize legacy one-line board headers to the compact 132 px standard.

The pass is deliberately conservative: it touches only 1600x900 board images with
an older white body panel beginning at y=172 and exactly one title-ink band no more
than 50 px tall. Wrapped titles, sequence-marker headers, contact sheets, previews,
and non-board artwork are skipped. Re-running the script is safe because compact
boards no longer match the y=172 body-panel test.
"""

from argparse import ArgumentParser
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
LAVENDER = (238, 234, 255)
WHITE = (255, 255, 255)
ROOTS = (
    ROOT / "board-review-first-four/alternatives",
    ROOT / "board-review-first-four/current-selected",
    ROOT / "board-review-first-four/standardized/start-smarter",
    ROOT / "illustrations",
    ROOT / "lessons",
)


def is_near_white(pixel):
    return min(pixel) > 244


def find_body_top(image):
    for y in range(90, 220):
        hits = sum(
            1 for x in range(60, 1540, 4)
            if is_near_white(image.getpixel((x, y)))
        )
        if hits > 300:
            return y
    return None


def title_spans(image, body_top):
    active_rows = []
    for y in range(max(1, body_top - 3)):
        hits = 0
        for x in range(50, 1550, 2):
            pixel = image.getpixel((x, y))
            if max(pixel) < 205 and sum(pixel) < 540:
                hits += 1
        if hits >= 2:
            active_rows.append(y)

    runs = []
    for y in active_rows:
        if not runs or y > runs[-1][-1] + 3:
            runs.append([y])
        else:
            runs[-1].append(y)
    return [(run[0], run[-1]) for run in runs if run[-1] - run[0] >= 3]


def title_bounds(image, span):
    y0, y1 = span
    points = []
    for y in range(max(0, y0 - 4), min(172, y1 + 5)):
        for x in range(40, 1560):
            r, g, b = image.getpixel((x, y))
            if max(r, g, b) < 205 and r + g + b < 540:
                points.append((x, y))
    if not points:
        return None
    return (
        max(0, min(x for x, _ in points) - 5),
        max(0, min(y for _, y in points) - 5),
        min(1600, max(x for x, _ in points) + 6),
        min(172, max(y for _, y in points) + 6),
    )


def title_mask(crop):
    mask = Image.new("L", crop.size, 0)
    source = crop.load()
    alpha = mask.load()
    for y in range(crop.height):
        for x in range(crop.width):
            r, g, b = source[x, y]
            distance = abs(r - LAVENDER[0]) + abs(g - LAVENDER[1]) + abs(b - LAVENDER[2])
            alpha[x, y] = 0 if distance < 24 else min(255, (distance - 24) * 8)
    return mask


def body_bottom(image):
    if is_near_white(image.getpixel((100, 850))):
        return 860
    if is_near_white(image.getpixel((100, 725))):
        return 736
    return None


def eligible(path):
    name = path.name.lower()
    return (
        path.suffix.lower() in {".jpg", ".png"}
        and not any(token in name for token in ("contact-sheet", "preview", "photo-base"))
    )


def compact(path, apply=False):
    try:
        image = Image.open(path).convert("RGB")
    except Exception:
        return False, "unreadable"
    if image.size != (1600, 900):
        return False, "not-1600x900"
    corner = image.getpixel((10, 10))
    if sum(abs(value - expected) for value, expected in zip(corner, LAVENDER)) > 18:
        return False, "not-standard-lavender-board"

    old_body_top = find_body_top(image)
    if old_body_top is None or not 168 <= old_body_top <= 176:
        return False, "not-legacy-header"

    spans = title_spans(image, old_body_top)
    if len(spans) != 1 or spans[0][1] - spans[0][0] > 50:
        return False, "not-single-line-title"

    bottom = body_bottom(image)
    bounds = title_bounds(image, spans[0])
    if bottom is None or bounds is None:
        return False, "geometry-not-recognized"
    if not apply:
        return True, "candidate"

    title = image.crop(bounds)
    mask = title_mask(title)
    title_y = round((132 - title.height) / 2)

    # Preserve the body content, rebuild the taller white stage, and move the
    # legacy composition upward by half of the recovered 40 px.
    content_bottom = bottom - 16
    content = image.crop((96, 172, 1504, content_bottom))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1600, 172), fill=LAVENDER)
    draw.rounded_rectangle((80, 132, 1520, bottom), radius=16, fill=WHITE)
    image.paste(content, (96, 152))
    image.paste(title, (bounds[0], title_y), mask)

    if path.suffix.lower() == ".png":
        image.save(path)
    else:
        image.save(path, quality=94, subsampling=0)
    return True, "updated"


def main():
    parser = ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write compacted images in place")
    args = parser.parse_args()

    matched = 0
    for root in ROOTS:
        for path in sorted(root.rglob("*")):
            if not eligible(path):
                continue
            changed, status = compact(path, args.apply)
            if changed:
                matched += 1
                print(f"{status:9} {path.relative_to(ROOT)}")
    print(f"{'updated' if args.apply else 'candidates'}: {matched}")


if __name__ == "__main__":
    main()

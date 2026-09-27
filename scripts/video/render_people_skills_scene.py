#!/usr/bin/env python3
"""Export the scene and render the two card boards with canonical typography."""
from pathlib import Path
import base64
import hashlib
import json
import zlib

from PIL import Image
from course_credit import save_course_image, policy

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / 'course-assets/people-skills'
SOURCE_DIR = ROOT / 'scripts/video/assets/people-skills-scene'
POLICY = ROOT / 'scripts/video/course-credit-policy.json'


def save(image, name, *, native=False):
    """Reserve the new board's blank footer explicitly, then apply the shared credit."""
    dest = ASSETS / name
    rel = dest.relative_to(ROOT).as_posix()
    spec_path = json.loads(POLICY.read_text())
    box = [900, image.height - 32, 1599, image.height - 1]
    footer = image.crop(box) if native else image.crop((40, box[1], 120, box[3])).resize((box[2] - box[0], box[3] - box[1]))
    spec_path['boards'][rel] = {
        'size': list(image.size), 'clear_box': box,
        'background_rgb_zlib': base64.b64encode(zlib.compress(footer.tobytes())).decode(),
        'approved_sha256': spec_path['boards'].get(rel, {}).get('approved_sha256', ''),
    }
    POLICY.write_text(json.dumps(spec_path, indent=2) + '\n')
    policy.cache_clear()
    save_course_image(image, dest, quality=95, subsampling=0, optimize=True)
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    manifest_path = ROOT / 'course-assets/manifest.json'
    manifest = json.loads(manifest_path.read_text())
    found = False
    for key in ('assets', 'generated_assets'):
        for record in manifest.get(key, []):
            if record['new'] == rel:
                record['sha256'] = digest
                if 'width' in record:
                    record['width'], record['height'] = image.size
                if 'bytes' in record:
                    record['bytes'] = dest.stat().st_size
                found = True
    if not found:
        manifest.setdefault('generated_assets', []).append({
            'new': rel, 'sha256': digest, 'bytes': dest.stat().st_size,
            'width': image.width, 'height': image.height,
            'generator': 'scripts/video/render_people_skills_scene.py',
            'reference_files': ['lessons/people-skills.md', 'index.html'],
            'purpose': 'Approved People Skills capstone shared by the page and video preparation.',
        })
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(f'{rel}: {image.width}x{image.height}')


def main():
    # Complete boards generated with the approved references. Keep their scene,
    # typography, and card layout intact; normalize only output size/encoding.
    for source, dest in [
        ('next-move-stars.png', 'people-skills-why-people-matter.jpg'),
        ('four-ways-original.jpg', 'people-skills-four-ways.jpg'),
        ('matter-more.png', 'people-skills-matter-more.jpg'),
    ]:
        import sys
        if '--scene-only' in sys.argv and source != 'next-move-stars.png':
            continue
        if '--capstone-only' in sys.argv and source != 'matter-more.png':
            continue
        if '--cards-only' in sys.argv and source == 'next-move-stars.png':
            continue
        if source in ('four-ways-original.jpg', 'matter-more.png'):
            from render_people_skills_cards import render_cards
            key = 'four-ways' if source == 'four-ways-original.jpg' else 'matter-more'
            save(render_cards(key), dest, native=True)
            continue
        image = Image.open(SOURCE_DIR / source).convert('RGB')
        height = round(image.height * 1600 / image.width)
        image = image.resize((1600, height), Image.Resampling.LANCZOS)
        save(image, dest)

    # Keep face-free Notebook stand-ins current whenever page boards are rebuilt.
    from render_people_skills_uploads import main as render_uploads
    render_uploads()


if __name__ == '__main__':
    main()

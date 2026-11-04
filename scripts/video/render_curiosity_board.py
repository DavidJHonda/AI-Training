#!/usr/bin/env python3
"""Render both Curiosity lesson boards with exact copy and photographic artwork.

Artwork: built-in imagegen, prompt and source sheet in assets/curiosity-2026-11-04.
Layout and typography use the existing EE-4FB course renderer.
"""
import base64
import hashlib
import json
import zlib

from render_editorial_full_bleed_batch import BOARDS, ROOT, render
from course_credit import POLICY_PATH, policy, save_course_image


def render_board(board, prompt_file):
    image = render(board)
    output = ROOT / board.page_output
    # The approved copy determines the canvas height. Reserve the existing
    # bottom margin for the course credit and record its clean background.
    credit_policy = json.loads(POLICY_PATH.read_text())
    box = (image.width - 400, image.height - 35, image.width - 30, image.height - 4)
    credit_policy['boards'][board.page_output] = {
        'size': list(image.size),
        'clear_box': list(box),
        'background_rgb_zlib': base64.b64encode(zlib.compress(image.crop(box).tobytes())).decode(),
        'approved_sha256': ''
    }
    POLICY_PATH.write_text(json.dumps(credit_policy, indent=2) + '\n')
    policy.cache_clear()
    save_course_image(image, output, quality=95, subsampling=0, optimize=True)
    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    credit_policy['boards'][board.page_output]['approved_sha256'] = digest
    POLICY_PATH.write_text(json.dumps(credit_policy, indent=2) + '\n')
    manifest_path = ROOT / 'course-assets/manifest.json'
    manifest = json.loads(manifest_path.read_text())
    for entry in manifest['assets']:
        if entry.get('new') == board.page_output:
            entry.update(sha256=digest, bytes=output.stat().st_size)
    generated = manifest.setdefault('generated_assets', [])
    generated[:] = [e for e in generated if e.get('new') != board.page_output]
    generated.append({
        'new': board.page_output, 'sha256': digest, 'bytes': output.stat().st_size,
        'width': image.width, 'height': image.height,
        'generator': 'scripts/video/render_curiosity_board.py',
        'reference_files': ['lessons/curiosity.md',
                            'scripts/video/render_editorial_full_bleed_batch.py',
                            board.art_sheet, 'scripts/video/assets/curiosity-2026-11-04/' + prompt_file],
        'purpose': board.title + ': natural photographic scenes with students in Dallas Stars jerseys, matching the What’s Next? lesson. Artwork generated with built-in imagegen; approved copy and EE-4FB layout rendered locally.'
    })
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'{board.page_output}: {image.width}x{image.height}')


if __name__ == '__main__':
    prompts = {'curiosity-four-ways': 'curiosity-stars-prompt.txt',
               'curiosity-ai-habits': 'ai-habits-prompt.txt'}
    for board in BOARDS:
        if board.key in prompts:
            render_board(board, prompts[board.key])

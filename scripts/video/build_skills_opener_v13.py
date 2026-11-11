#!/usr/bin/env python3
"""Same approved sound edit; fix donor exit picture and encoded ring thickness."""
from collections import OrderedDict
import hashlib
import json

import build_skills_opener_v11 as engine
import build_skills_opener_v12 as plan

ROOT = engine.ROOT
plan.OUT = ROOT / 'video-audit/build-skills-opener-v13-2026-11-11'
plan.DEST = ROOT / 'Prompts/build-your-skills-opener-v13.mp4'

# The corner-cleaning algorithm reads only this region (including its shifted
# donors and border bands) and changes only BOX. Identical region bytes produce
# an identical patch. Cache that exact result; do not reuse patches across motion.
original_clean = engine.clean_frame
cache = OrderedDict()
stats = {'hits': 0, 'misses': 0}


def cached_clean(frame, mask):
    region = frame[528:720, 890:1280]
    key = hashlib.blake2b(region.tobytes(), digest_size=20).digest()
    if key in cache:
        patch, method = cache.pop(key)
        cache[key] = (patch, method)
        out = frame.copy()
        out[666:716, 1128:1279] = patch
        stats['hits'] += 1
        return out, method
    out, method = original_clean(frame, mask)
    cache[key] = (out[666:716, 1128:1279].copy(), method)
    if len(cache) > 2048:
        cache.popitem(last=False)
    stats['misses'] += 1
    return out, method


original_cover = engine.cover


def fixed_cover(b, start, end, video_start, video_end=None, video_src=None):
    if start == 4995 and end == 5061 and video_start == 4266:
        # Source roll 2 cuts to an unrelated capability chart at f4289.
        # The planner's last clean frame is f4288; hold it through this clause.
        video_end = 4289
    return original_cover(b, start, end, video_start, video_end, video_src)


original_compact = engine.compact_leg


def aligned_compact(b):
    # Integer centerlines make four full output pixels survive 4:2:0 encoding.
    b.pixel_aligned_rings = True
    return original_compact(b)


def main():
    engine.clean_frame = cached_clean
    engine.cover = fixed_cover
    engine.compact_leg = aligned_compact
    plan.main()
    manifest_path = plan.OUT / 'edit-manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['visual_revision'] = {
        'supersedes': str(ROOT / 'Prompts/build-your-skills-opener-v12.mp4'),
        'narration_unchanged_from_v12': True,
        'planner_last_clean_source_frame': 4288,
        'ring_centerlines_aligned_to_output_pixel_grid': True,
        'corner_cache': stats,
        'corner_cache_policy': 'Only identical full input regions reuse their exact deterministic cleanup patch.',
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""October 1 board-edge repair, using the approved v3 assembly and original source."""
import json
import sys

import build_wheres_the_line_v3 as base

base.OUT = base.ROOT / 'video-audit/wheres-the-line-board-edges-2026-10-01-v4'
base.DEST = base.ROOT / 'Prompts/wheres-the-line-v4.mp4'

if __name__ == '__main__':
    base.main()
    if '--prepare-only' not in sys.argv:
        path = base.OUT / 'edit-manifest.json'
        manifest = json.loads(path.read_text())
        manifest.update(
            scope='Narrow board-edge repair: remove art-sheet divider slivers from all six cards. '
                  'Retain the approved v3 assembly, camera, highlights, audio, and timing.',
            prior_candidate=str(base.ROOT / 'Prompts/wheres-the-line-v3.mp4'),
            prior_candidate_sha256=base.sha(base.ROOT / 'Prompts/wheres-the-line-v3.mp4'),
            board_crop_change={'sheet_display_width_before': 1488, 'sheet_display_width_after': 1504,
                               'right_crop_x_before': -744, 'right_crop_x_after': -760,
                               'vertical_scale_and_offsets_unchanged': True},
        )
        path.write_text(json.dumps(manifest, indent=2) + '\n')

#!/usr/bin/env python3
"""Approved v9 deletion: keep the AI-era bridge, then go straight to the map.

Reassemble from v9's original sources, preserving its map and closing treatment.
The only editorial change is deleting v9 frames [1668,2679), 55.6–89.3 seconds.
"""
import json
import os
import shutil
from pathlib import Path
import numpy as np
import build_build_your_skills_opener_v9 as previous
from editspec_build import Build, SPF, writewav, sha

OLD_OUT = previous.OUT
CUT_IN, CUT_OUT = 1668, 2679
REMOVED = CUT_OUT - CUT_IN


class ShortenedBuild(Build):
    def finish_audio(self):
        original = np.concatenate(self.parts)
        assert len(original) == 5237 * SPF
        head = original[:CUT_IN * SPF].copy()
        tail = original[CUT_OUT * SPF:].copy()
        # Both cuts sit in the sentence gap. Only a 5 ms edge fade, no new pause.
        ramp = np.linspace(0, 1, 240)
        head[-240:] *= 1-ramp
        tail[:240] *= ramp
        audio = np.concatenate([head, tail])
        rows = []
        for row in self.rows:
            for lo, hi in [(0, CUT_IN), (CUT_OUT, 5237)]:
                s, e = max(row['start_frame'], lo), min(row['end_frame'], hi)
                if e <= s:
                    continue
                r = dict(row)
                if r['kind'] == 'source':
                    r['source_start'] += s - row['start_frame']
                    r['source_end'] = r['source_start'] + e-s
                    if 'video_start' in r:
                        r['video_start'] += s-row['start_frame']
                shift = REMOVED if s >= CUT_OUT else 0
                r.update(start_frame=s-shift, end_frame=e-shift)
                rows.append(r)
        self.rows = rows
        self.cursor -= REMOVED
        self.total = self.cursor
        self.close_start -= REMOVED
        assert self.total == 4226 and len(audio) == self.total*SPF
        assert all(a['end_frame']==b['start_frame'] for a,b in zip(rows, rows[1:]))
        writewav(self.out/'edited.wav', audio)

    def render_legs(self):
        # The map's pictures and relative timing are exactly the approved v9 leg.
        old = json.loads((OLD_OUT/'leg-map.json').read_text())
        new = json.loads((self.out/'leg-map.json').read_text())
        if not (OLD_OUT/'leg-map.mkv').exists() or not Path(old['image']).exists():
            return super().render_legs()
        assert sha(old.pop('image')) == sha(new.pop('image'))
        assert old == new
        dest = self.out/'leg-map.mkv'
        if not dest.exists():
            os.link(OLD_OUT/'leg-map.mkv', dest)

    def state_sheet(self, key):
        shutil.copy2(OLD_OUT/f'states-{key}.jpg', self.out/f'states-{key}.jpg')

    def manifest(self, extra=None):
        extra = dict(extra or {})
        extra.update(
            authorization='2026-11-04: approved removing the redundant pre-map passage, retaining the AI-era bridge.',
            build_scope='Narrow deletion from v9; review candidate only.',
            deleted_v9_frames=[CUT_IN,CUT_OUT], deleted_v9_seconds=[CUT_IN/30,CUT_OUT/30],
            removed_seconds=REMOVED/30, output_join_frame=CUT_IN,
            join_text='...the mental tools of the AI era. This roadmap shows...',
            rebuild='Original source footage and audio; unchanged lossless map leg reused.')
        extra['accepted_compromises']=[s for s in extra['accepted_compromises'] if not s.startswith('Formal phrases')]
        return super().manifest(extra)


if __name__ == '__main__':
    previous.Build = ShortenedBuild
    previous.OUT = previous.ROOT/'video-audit/build-your-skills-opener-v10-2026-11-04'
    previous.DEST = previous.ROOT/'Prompts/build-your-skills-opener-v10.mp4'
    previous.main()

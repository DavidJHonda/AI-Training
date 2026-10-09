#!/usr/bin/env python3
"""v13's approved assembly with the erroneous generated GPA graphic repaired.

Rebuild from pristine rolls and the verified board legs; narration is identical.
"""
from pathlib import Path
import os
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_ai_is_different_v13 as base
from editspec_build import Build as OriginalBuild, sha

ROOT = base.ROOT
PREVIOUS = base.OUT
OUT = ROOT / 'video-audit/ai-is-different-build-2026-10-09-v14'
DEST = ROOT / 'Prompts/ai-is-different-v14.mp4'


class Build(OriginalBuild):
    def keep(self, s, e, label, visual='source', **kwargs):
        super().keep(s, e, label, visual, **kwargs)
        if s == 5198 and e == 5751:
            row = self.rows.pop()
            cut = 5585  # Original roll-5 cut from GPA to illustrated campus photo.
            duration = cut-s
            # Source 6 has a correct worked example: 16+11.1+9.9 = 37;
            # ten credits yield 3.70. Preserve its reveal, then hold the last
            # complete table before its fade. Audio remains one continuous part.
            self.rows.append(dict(row, source_end=cut, end_frame=row['start_frame']+duration,
                video_start=3630, video_end=3903, video_src=str(base.R6),
                label='Correct GPA table from roll 6; final complete table held'))
            self.rows.append(dict(row, source_start=cut, start_frame=row['start_frame']+duration,
                label='Original illustrated campus photo'))

    def manifest(self, extra=None):
        extra = dict(extra or {})
        extra['visual_qa_repair'] = {
            'previous_candidate':str(ROOT/'Prompts/ai-is-different-v13.mp4'),
            'issue':'Roll-5 visual showed GPA 3.8 for grades/credits that imply about 3.67 on the displayed conventional scale.',
            'repair':'Use roll-6 GPA table with explicit points: (16+11.1+9.9)/10 = 3.70.',
            'source_frames':[3630,3903], 'output_frames':[4973,5360],
            'held_final_frames':114,
            'audio_identical_to_v13':sha(self.out/'edited.wav')==sha(PREVIOUS/'edited.wav'),
        }
        assert extra['visual_qa_repair']['audio_identical_to_v13']
        return super().manifest(extra)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # Lossless board legs and extracted PCM can be reused without re-encoding.
    for name in ['source.wav','graft-r4-consistency.wav','graft-r6-substitutions.wav',
                 'leg-rules.mkv','leg-cooking.mkv']:
        if not (OUT/name).exists():
            os.link(PREVIOUS/name, OUT/name)
    base.OUT, base.DEST, base.Build = OUT, DEST, Build
    if '--reuse-legs' not in sys.argv:
        sys.argv.append('--reuse-legs')
    base.main()


if __name__ == '__main__':
    main()

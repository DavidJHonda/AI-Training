"""Use the approved take 3 Power explanation between take 1's card labels."""
from build_fake_trap_v14 import ROOT, PICTURE, build_cut, paused_mix
from build_fake_trap_v15 import MOTIVES_IN


def power_mix(work, sound, sources):
    parts = []
    for name, source, start, end in sound:
        if name == 'motives':
            parts.extend([
                (name, source, MOTIVES_IN, 94.87),
                ('power explanation', '3', 88.36, 92.26),
                ('fame and cruelty', source, 97.72, end),
            ])
        else:
            parts.append((name, source, start, end))
    return paused_mix(work, parts, sources)


if __name__ == '__main__':
    cues = [('fame and cruelty', at, kind, *args)
            if beat == 'motives' and args[0] in ('fame', 'cruelty')
            else (beat, at, kind, *args)
            for beat, at, kind, *args in PICTURE]
    build_cut(ROOT / 'Prompts/fake-trap-v16.mp4',
              ROOT / 'video-audit/fake-trap-v16-2026-11-16',
              mix=power_mix, motives_start=MOTIVES_IN, cues=cues)

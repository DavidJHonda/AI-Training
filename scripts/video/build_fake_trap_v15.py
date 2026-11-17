"""Restore roll one's transition from the hockey joke into the four motives."""
from build_fake_trap_v14 import ROOT, build_cut, paused_mix

MOTIVES_IN = 81.90


def transition_mix(work, sound, sources):
    # Use one continuous take through the motives so the narrator's pause survives.
    extended = [(name, source, MOTIVES_IN if name == 'motives' else start, end)
                for name, source, start, end in sound]
    return paused_mix(work, extended, sources)


if __name__ == '__main__':
    build_cut(ROOT / 'Prompts/fake-trap-v15.mp4',
              ROOT / 'video-audit/fake-trap-v15-2026-11-16',
              mix=transition_mix, motives_start=MOTIVES_IN)

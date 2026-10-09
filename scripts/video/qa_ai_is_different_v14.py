#!/usr/bin/env python3
"""Encoded v14 verification, including exact narration equivalence to v13."""
from pathlib import Path
import json
import subprocess
import imageio_ffmpeg
import qa_ai_is_different_v13 as qa

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/ai-is-different-build-2026-10-09-v14'


def main():
    qa.OUT = OUT
    qa.VIDEO = ROOT / 'Prompts/ai-is-different-v14.mp4'
    qa.main()
    hashes = {}
    for n in [13,14]:
        r = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v','error','-i',
            str(ROOT/f'Prompts/ai-is-different-v{n}.mp4'), '-map','0:a','-c:a','copy',
            '-f','hash','-hash','sha256','-'], capture_output=True,text=True,check=True)
        hashes[str(n)] = r.stdout.strip()
    assert hashes['13']==hashes['14'], hashes
    (OUT/'audio-equivalence.json').write_text(json.dumps({
        'encoded_aac_hashes':hashes,'identical':True,
        'transcript_source':'../ai-is-different-build-2026-10-09-v13/encoded-transcript.json',
    },indent=2))


if __name__ == '__main__':
    main()

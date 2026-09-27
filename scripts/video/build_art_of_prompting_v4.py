#!/usr/bin/env python3
"""Build the Art of Prompting v4 review candidate (2026-09-26).

Narrow narration repair on the live 20260916ship1 video (the only source: the
09-16 raw rolls and donor were deleted 2026-09-15). Two approved complete-sentence
cuts, placed on the measured waveform, not the ASR estimates:

1. "To successfully package that question for AI, however, we use a specific
   framework of instructions," -- audio removed live frames 1478-1646 (49.267-
   54.867 s), both joins in -66..-70 dB silence. The good-question board now ends
   in its Open-Ended dive (the pull-back/full-hold covered only the cut sentence):
   live frames 1472-1647 dropped, the static dive frame 1471 held 8 extra frames
   so everything downstream stays in sync.
2. "You don't need to apply this entire framework every single time." -- audio
   and picture removed live frames 6027-6131 (200.900-204.400 s). The approved
   one-second pause after the thesis example is kept whole; the picture cuts from
   the Move 4 drawing straight to Notebook's finished Simple Query drawing (its
   fade-in and typing played under the cut sentence).

No rings, boards, or close are re-rendered; every kept frame is the live frame.
Review candidate only; the live video and lesson page are unchanged.
"""

from pathlib import Path
import hashlib
import subprocess
import wave

import cv2
import imageio_ffmpeg
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / "course-assets/art-of-prompting/art-of-prompting.mp4"
LIVE_SHA = "c0b9ecb5460aee21892e7a663356346d681073ee55217d6e507a4dd3a7f347ab"
OUT = ROOT / "video-audit/art-of-prompting-repair-2026-09-26"
DEST = ROOT / "Prompts/art-of-prompting-v4.mp4"

FPS, SR = 30, 48000
SPF = SR // FPS
XF = 480  # 10 ms crossfade, centred on each join, inside silence

AUDIO_CUTS = [(1478, 1646), (6027, 6132)]  # live frames [a, b) removed
VIDEO_DROP = [(1472, 1648), (6027, 6132)]
HOLD = {1471: 8}  # live frame -> extra copies (static Open-Ended dive)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    assert sha(LIVE) == LIVE_SHA, "live file changed since measurement"
    OUT.mkdir(parents=True, exist_ok=True)
    ff = imageio_ffmpeg.get_ffmpeg_exe()

    live_wav = OUT / "live.wav"
    subprocess.run([ff, "-y", "-v", "error", "-i", str(LIVE), "-vn", "-c:a", "pcm_s16le", str(live_wav)], check=True)
    with wave.open(str(live_wav)) as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64)

    t = np.linspace(0, np.pi / 2, XF)
    fade_out, fade_in = np.cos(t), np.sin(t)
    pieces, pos = [], 0
    for fa, fb in AUDIO_CUTS:
        c0, c1 = fa * SPF, fb * SPF
        pieces.append(a[pos:c0 - XF // 2])
        pieces.append(a[c0 - XF // 2:c0 + XF // 2] * fade_out + a[c1 - XF // 2:c1 + XF // 2] * fade_in)
        pos = c1 + XF // 2
    pieces.append(a[pos:])
    edited = np.clip(np.concatenate(pieces), -32768, 32767).astype(np.int16)
    edited_wav = OUT / "edited.wav"
    with wave.open(str(edited_wav), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(edited.tobytes())

    cap = cv2.VideoCapture(str(LIVE))
    n_live = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    removed = sum(b - a_ for a_, b in VIDEO_DROP) - sum(HOLD.values())
    assert removed == sum(b - a_ for a_, b in AUDIO_CUTS)
    planned = n_live - removed
    enc = subprocess.Popen(
        [ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1280x720", "-r", str(FPS),
         "-i", "pipe:0", "-i", str(edited_wav), "-map", "0:v", "-map", "1:a",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(DEST)],
        stdin=subprocess.PIPE,
    )
    written, i = 0, 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        if not any(a_ <= i < b for a_, b in VIDEO_DROP):
            for _ in range(1 + HOLD.get(i, 0)):
                enc.stdin.write(f.tobytes())
                written += 1
        i += 1
    enc.stdin.close()
    enc.wait()
    assert i == n_live, (i, n_live)
    assert written == planned, (written, planned)
    assert sha(LIVE) == LIVE_SHA
    print(f"live {n_live} frames -> {DEST.name} {written} frames ({written / FPS:.2f}s); "
          f"audio {len(edited) / SR:.3f}s")


if __name__ == "__main__":
    main()

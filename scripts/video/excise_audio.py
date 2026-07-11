#!/usr/bin/env python
"""WORD EXCISION — remove a stray spoken word from the AUDIO only; video stream
copied untouched (shipped: how-an-llm-works seam word "first", 163.50-164.02).

CAVEAT: the audio track gets shorter by (end - start), so everything AFTER the
cut plays that much earlier relative to the video. Only invisible when the
remainder sits over static boards (e.g. a close-board tail). Not for mid-video
cuts over moving visuals.

--probe first: prints 20ms RMS windows around the suspect span so you can place
the cut on the word's true boundaries (cut in the silence shoulders).

Usage:
  .video-venv/bin/python scripts/video/excise_audio.py in.mp4 --probe 163.0 164.5
  .video-venv/bin/python scripts/video/excise_audio.py in.mp4 --cut 163.50 164.02 -o out.mp4
"""
import argparse
import os
import subprocess
import sys
import tempfile
import wave


def probe(ffmpeg, path, start, end):
    lead = 0.5
    s = max(0.0, start - lead)
    with tempfile.TemporaryDirectory() as td:
        wav = os.path.join(td, "probe.wav")
        subprocess.run(
            [ffmpeg, "-y", "-hide_banner", "-loglevel", "error",
             "-ss", str(s), "-to", str(end + lead), "-i", path,
             "-ac", "1", "-ar", "44100", wav],
            check=True)
        with wave.open(wav, "rb") as w:
            rate = w.getframerate()
            data = w.readframes(w.getnframes())
    import numpy as np
    samples = np.frombuffer(data, dtype=np.int16).astype(np.float64)
    win = int(rate * 0.020)
    for i in range(0, len(samples) - win, win):
        t = s + i / rate
        rms = float(np.sqrt((samples[i:i + win] ** 2).mean()))
        bar = "#" * min(60, int(rms / 100))
        print(f"{t:8.3f}  {rms:7.0f}  {bar}")


def cut(ffmpeg, path, start, end, out):
    graph = (f"[0:a]atrim=0:{start},asetpts=PTS-STARTPTS[a1];"
             f"[0:a]atrim={end},asetpts=PTS-STARTPTS[a2];"
             f"[a1][a2]concat=n=2:v=0:a=1[a]")
    subprocess.run(
        [ffmpeg, "-y", "-hide_banner", "-i", path,
         "-filter_complex", graph,
         "-map", "0:v", "-c:v", "copy",
         "-map", "[a]", "-c:a", "aac", "-b:a", "128k", out],
        check=True)
    print(f"removed audio [{start}, {end}] ({end - start:.2f}s); video copied -> {out}")
    print(f"NOTE: audio after {start}s now plays {end - start:.2f}s early vs video — "
          "only OK over static boards. David ear-tests before ship.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input")
    ap.add_argument("--probe", nargs=2, type=float, metavar=("S", "E"))
    ap.add_argument("--cut", nargs=2, type=float, metavar=("S", "E"))
    ap.add_argument("-o", "--out", help="output path (required with --cut)")
    args = ap.parse_args()

    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    if args.probe:
        probe(ffmpeg, args.input, *args.probe)
    elif args.cut:
        if not args.out:
            sys.exit("--cut needs -o out.mp4")
        cut(ffmpeg, args.input, *args.cut, args.out)
    else:
        sys.exit("pass --probe S E or --cut S E -o out.mp4")


if __name__ == "__main__":
    main()

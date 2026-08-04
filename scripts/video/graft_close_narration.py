#!/usr/bin/env python3
"""Replace a video's closing narration with a donor span and rebuild the close
as the standard Ken Burns board leg (close-copy retrofit, 2026-08-04).

Audio timeline: base [0..cut] (optionally minus a deleted mid-span) + mirror-
tiled room tone (never anullsrc) + loudness-matched donor span + tone tail with
a 0.2s end fade. Video timeline: base frames [0..arrival) + board push-in leg
sized to the new audio length. One re-encode pass; total duration may change.

Donor span boundaries are refined from RMS (whisper end stamps undershoot
trailing sibilants): the span is extracted with padding, then trimmed to first/
last energy with 10ms fades. Verification per build: decoded frame count vs
audio ticks, silence continuity at the joins, and the tail re-transcribed so
the new lines can be read in the log.

Driven by a VIDEOS dict in the companion build script — see
close-audit-2026-08-04.md for the parameter provenance.
"""
import os
import subprocess
import sys

import cv2
import numpy as np
from imageio_ffmpeg import get_ffmpeg_exe

FF = get_ffmpeg_exe()
SR = 44100


def run(cmd):
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        sys.exit(f"cmd failed: {' '.join(map(str, cmd))}\n"
                 + r.stderr.decode()[-1500:])
    return r


def decode_audio(path):
    raw = subprocess.run([FF, "-i", path, "-vn", "-ac", "1", "-ar", str(SR),
                          "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def speech_rms(a):
    hop = SR // 50
    n = len(a) // hop
    r = np.sqrt((a[:n * hop].reshape(n, hop) ** 2).mean(axis=1))
    r = r[r > 0.02]
    return float(np.median(r)) if len(r) else 0.0


def fade(a, ms_in=10, ms_out=10):
    n_in, n_out = SR * ms_in // 1000, SR * ms_out // 1000
    a = a.copy()
    if n_in and len(a) > n_in:
        a[:n_in] *= np.linspace(0, 1, n_in)
    if n_out and len(a) > n_out:
        a[-n_out:] *= np.linspace(1, 0, n_out)
    return a


def mirror_tone(base, t0, t1, need):
    seg = base[int(t0 * SR):int(t1 * SR)]
    # the tone window must be pure room tone: a window that clips a word tail
    # gets mirror-tiled into an audible echo (evaluate's "professional", 8/4)
    if speech_rms_all(seg) > 0.012:
        sys.exit(f"tone window {t0:.2f}-{t1:.2f} is not silent "
                 f"(rms {speech_rms_all(seg):.4f}) — pick a window inside a "
                 f"measured silence")
    tile = np.concatenate([seg, seg[::-1]])
    reps = int(np.ceil(need * SR / len(tile)))
    return np.tile(tile, reps)[:int(need * SR)]


def speech_rms_all(a):
    hop = SR // 50
    n = max(len(a) // hop, 1)
    r = np.sqrt((a[:n * hop].reshape(-1, hop) ** 2).mean(axis=1)) if len(a) >= hop else np.array([np.sqrt((a ** 2).mean())])
    return float(r.max())


def trough_cut(ad, t, direction, thresh=0.01, run_ms=40):
    """Nearest sustained RMS trough to time t (donor samples), searching
    forward (+1, for span ends) or backward (-1, for span starts). Whisper end
    stamps undershoot trailing sibilants and the next word can start with no
    stamped gap — cutting at the trough keeps the sibilant and drops the leak."""
    hop = SR // 200  # 5ms
    back = 0.45 if direction < 0 else 0.15
    lo = int(max(0, (t - back) * SR))
    hi = int(min(len(ad), (t + 0.60 - back) * SR))
    seg = ad[lo:hi]
    n = len(seg) // hop
    r = np.sqrt((seg[:n * hop].reshape(n, hop) ** 2).mean(axis=1))
    need = run_ms // 5
    idxs = range(n - need) if direction > 0 else range(n - need, -1, -1)
    for i in idxs:
        if (r[i:i + need] < thresh).all():
            return (lo + (i + need // 2) * hop) / SR
    return t + 0.12 * direction


def build(name, base, donor, out, board, arrival_frame, cut_t, donor_t0,
          donor_t1, gap=0.55, tail=1.2, tone_win=None, delete_span=None):
    print(f"=== {name} ===")
    ab = decode_audio(base)
    ad = decode_audio(donor)

    s0 = trough_cut(ad, donor_t0, -1)
    s1 = trough_cut(ad, donor_t1, +1)
    span = fade(ad[int(s0 * SR):int(s1 * SR)])
    g = speech_rms(ab[-40 * SR:]) / max(speech_rms(span), 1e-6)
    g = float(np.clip(g, 0.6, 1.6))
    span = span * g

    head = ab[:int(cut_t * SR)]
    if delete_span:
        d0, d1 = delete_span
        head = np.concatenate([fade(ab[:int(d0 * SR)], 0, 8),
                               fade(ab[int(d1 * SR):int(cut_t * SR)], 8, 0)])
    tw = tone_win or (cut_t - 0.42, cut_t - 0.05)
    # tail: tone faded to zero across its WHOLE length — a held-level tone tile
    # after the donor's last word exposes the donor->base room-tone shift and
    # the tile's own periodicity (tokens, 8/4); a full-length fade masks both
    tail_tone = mirror_tone(ab, tw[0], tw[1], tail)
    tail_tone *= np.linspace(1.0, 0.0, len(tail_tone)) ** 1.5
    audio = np.concatenate([
        fade(head, 0, 8),
        fade(mirror_tone(ab, tw[0], tw[1], gap), 8, 8),
        fade(span, 10, 40),
        tail_tone,
    ])
    total = int(round(len(audio) / SR * 30))
    audio = np.resize(audio, int(total / 30 * SR))
    N = total - arrival_frame
    z = min(1 + 0.2 * N / 210, 1.2)
    wav = out + ".wav"
    import wave
    with wave.open(wav, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(audio, -1, 1) * 32767).astype(np.int16).tobytes())

    graph = (
        f"[1:v]scale=3840:2160:flags=lanczos,"
        f"zoompan=z='1+{z - 1:.6f}*on/({N}-1)':x='(iw-iw/zoom)/2'"
        f":y='(ih-ih/zoom)/2':d={N}:s=1280x720:fps=30,"
        f"format=yuv420p,setsar=1,settb=1/30,setpts=N/(30*TB),"
        f"trim=start_frame=0:end_frame={N},setpts=PTS-STARTPTS[mid];"
        f"[0:v]trim=start_frame=0:end_frame={arrival_frame},"
        f"setpts=PTS-STARTPTS[pre];"
        f"[pre][mid]concat=n=2:v=1:a=0[v]"
    )
    run([FF, "-y", "-i", base, "-i", board, "-i", wav,
         "-filter_complex", graph, "-map", "[v]", "-map", "2:a",
         "-c:v", "libx264", "-crf", "18", "-preset", "medium",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", out])
    os.remove(wav)

    cap = cv2.VideoCapture(out)
    dec = 0
    while cap.read()[0]:
        dec += 1
    cap.release()
    ok = dec in (total, total - 1)
    print(f"  gain {g:.2f}  donor {len(span)/SR:.2f}s  total {total}f "
          f"({total/30:.2f}s)  decoded {dec} {'OK' if ok else 'FAIL'}")
    if not ok:
        sys.exit("VERIFY FAILED: frame count")
    return out

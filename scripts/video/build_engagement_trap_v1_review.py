#!/usr/bin/env python3
"""Build the approved Engagement Trap live repair review candidate.

The shipped lesson remains the narration and picture spine. Three complete
audio beats repair it: engagement-trap-1 supplies Raskin's half-million human
lifetimes estimate; engagement-trap-2 supplies the business-incentive
explanation and exact two-line close. Candidate 2's unsupported metric graphics
are never used. The live illustrations beneath the longer business beat are
retimed, the first comparison-board entry is corrected to open on the complete
board, and the canonical close receives the standard house move.

Review only: writes Prompts/engagement-trap-v1.mp4 and a new audit directory.
It never modifies the live video, either donor, index.html, or lesson Markdown.
"""

from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json
import math
import subprocess
import sys
import wave

import cv2
import imageio_ffmpeg
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from editspec_build import Build, NEUTRAL  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / "course-assets/engagement-trap/engagement-trap.mp4"
DONOR1 = ROOT / "Prompts/engagement-trap-1.mp4"
DONOR2 = ROOT / "Prompts/engagement-trap-2.mp4"
DEST = ROOT / "Prompts/engagement-trap-v1.mp4"
OUT = ROOT / "video-audit/engagement-trap-repair-2026-09-18"

ASSETS = ROOT / "course-assets/engagement-trap"
COMPARISON = ASSETS / "engagement-trap-comparison.jpg"
SCROLL = ASSETS / "engagement-trap-scroll.jpg"
STOPPING = ASSETS / "engagement-trap-stopping-point.jpg"
CLOSE = ASSETS / "engagement-trap-close.jpg"
LESSON = ROOT / "lessons/engagement-trap.md"
INDEX = ROOT / "index.html"

LIVE_SHA = "059cc08a18c4b7807b310aa80fb7ad86fc273e7dd3346c37ccccf2ed9340ee6e"
DONOR1_SHA = "55a02f15462124d0865bb6c10fa833b1fd4e52777e88a168d3f745b3ba87dd07"
DONOR2_SHA = "a453869e52e4f0a96dd9d3580587faa4c4155995be2bbc9731ec09f708ed0933"

FPS = 30
SR = 48_000
SPF = SR // FPS
W, H = 1280, 720
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# All cut ranges are half-open integer 30 fps intervals chosen inside measured
# silence. They intentionally differ from the rounded review timestamps.
BASE_GRAFT1 = (4710, 4971)       # 157.000-165.700, live regret-only sentence
DONOR1_GRAFT1 = (4005, 4284)     # 133.500-142.800, regret + half-million estimate
PAUSE1 = 12                      # raises strict post-statistic silence to ~0.75s

BASE_GRAFT2 = (5610, 5946)       # 187.000-198.200, live thin business explanation
DONOR2_GRAFT2 = (5307, 6006)     # 176.900-200.200, four approved sentences only
PAUSE2 = 11                      # raises strict pre-business silence to ~0.75s

BASE_CLOSE = 7026                # 234.200, silence before the shipped close wording
DONOR2_CLOSE = (6869, 6987)      # 228.967-232.900, exact two-line close only
CLOSE_FRAMES = 48 + 150 + 120

BOARD1 = (501, 1207)             # exact live visual cut: 16.700-40.233

GRAFT1_OUT = (BASE_GRAFT1[0], BASE_GRAFT1[0] + (DONOR1_GRAFT1[1] - DONOR1_GRAFT1[0]) + PAUSE1)
MIDDLE1_OUT = (GRAFT1_OUT[1], GRAFT1_OUT[1] + (BASE_GRAFT2[0] - BASE_GRAFT1[1]))
PAUSE2_OUT = (MIDDLE1_OUT[1], MIDDLE1_OUT[1] + PAUSE2)
GRAFT2_OUT = (PAUSE2_OUT[1], PAUSE2_OUT[1] + (DONOR2_GRAFT2[1] - DONOR2_GRAFT2[0]))
MIDDLE2_OUT = (GRAFT2_OUT[1], GRAFT2_OUT[1] + (BASE_CLOSE - BASE_GRAFT2[1]))
CLOSE_OUT = (MIDDLE2_OUT[1], MIDDLE2_OUT[1] + CLOSE_FRAMES)
TOTAL_FRAMES = CLOSE_OUT[1]

# The source's drawing begins three frames after the audio resumes from graft 1.
# Advancing that destination shot over the three silent audio-shoulder frames
# avoids a rejected 3-frame old-board island without altering narration timing.
MIDDLE1_VISUAL_START = 4974


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def media_properties(path: Path) -> tuple[int, float, int, int]:
    cap = cv2.VideoCapture(str(path))
    if not cap.isOpened():
        raise SystemExit(f"cannot open {path}")
    props = (
        int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        cap.get(cv2.CAP_PROP_FPS),
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )
    cap.release()
    return props


def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path), "rb") as wav:
        assert wav.getframerate() == SR and wav.getnchannels() == 1
        return np.frombuffer(wav.readframes(wav.getnframes()), np.int16).astype(np.float64)


def write_wav(path: Path, samples: np.ndarray) -> None:
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SR)
        wav.writeframes(np.clip(samples, -32768, 32767).astype(np.int16).tobytes())


def decode_audio(source: Path, dest: Path, gain_db: float = 0.0) -> None:
    if dest.exists():
        return
    audio_filter = None
    if gain_db:
        audio_filter = (
            f"volume={gain_db:.2f}dB,"
            "alimiter=limit=0.95:attack=5:release=50:level=false"
        )
    command = [FFMPEG, "-y", "-v", "error", "-i", str(source), "-vn"]
    if audio_filter:
        command += ["-af", audio_filter]
    command += ["-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(dest)]
    subprocess.run(command, check=True)


def at(samples: np.ndarray, start: float, end: float) -> np.ndarray:
    return samples[round(start * SR):round(end * SR)]


def loop_tone(seed: np.ndarray, samples: int) -> np.ndarray:
    seed = seed.copy()
    seed -= seed.mean()
    return np.resize(np.r_[seed, seed[::-1]], samples)


def bridge(left: np.ndarray, right: np.ndarray, seed: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Meet two fixed-length clips through continuous matched tone over 5 ms."""
    n = min(240, len(left), len(right))
    tone = loop_tone(seed, n * 2)
    ramp = np.linspace(0.0, 1.0, n)
    left = left.copy()
    right = right.copy()
    left[-n:] = left[-n:] * (1.0 - ramp) + tone[:n] * ramp
    right[:n] = tone[n:] * (1.0 - ramp) + right[:n] * ramp
    return left, right


def prepare_audio() -> dict:
    live_path = OUT / "live.wav"
    donor1_path = OUT / "donor1-plus-1.01db.wav"
    donor2_business_path = OUT / "donor2-plus-0.44db.wav"
    donor2_close_path = OUT / "donor2-close-plus-2.35db.wav"
    decode_audio(LIVE, live_path)
    decode_audio(DONOR1, donor1_path, 1.01)
    decode_audio(DONOR2, donor2_business_path, 0.44)
    decode_audio(DONOR2, donor2_close_path, 2.35)

    live = read_wav(live_path)
    donor1 = read_wav(donor1_path)
    donor2_business = read_wav(donor2_business_path)
    donor2_close = read_wav(donor2_close_path)
    s = lambda frame: frame * SPF

    before1 = live[:s(BASE_GRAFT1[0])]
    graft1 = donor1[s(DONOR1_GRAFT1[0]):s(DONOR1_GRAFT1[1])]
    pause1 = loop_tone(at(live, 165.56, 165.66), PAUSE1 * SPF)
    middle1 = live[s(BASE_GRAFT1[1]):s(BASE_GRAFT2[0])]
    pause2 = loop_tone(at(live, 186.90, 187.00), PAUSE2 * SPF)
    graft2 = donor2_business[s(DONOR2_GRAFT2[0]):s(DONOR2_GRAFT2[1])]
    middle2 = live[s(BASE_GRAFT2[1]):s(BASE_CLOSE)]
    close = donor2_close[s(DONOR2_CLOSE[0]):s(DONOR2_CLOSE[1])]
    tail_frames = CLOSE_FRAMES - (DONOR2_CLOSE[1] - DONOR2_CLOSE[0])
    close_tail = loop_tone(at(donor2_close, 232.67, 232.82), tail_frames * SPF)
    close_tail *= np.linspace(1.0, 0.0, len(close_tail)) ** 1.5

    before1, graft1 = bridge(before1, graft1, at(live, 156.90, 157.00))
    graft1, pause1 = bridge(graft1, pause1, at(donor1, 142.67, 142.77))
    pause1, middle1 = bridge(pause1, middle1, at(live, 165.56, 165.66))
    middle1, pause2 = bridge(middle1, pause2, at(live, 186.90, 187.00))
    pause2, graft2 = bridge(pause2, graft2, at(donor2_business, 176.78, 176.88))
    graft2, middle2 = bridge(graft2, middle2, at(live, 198.08, 198.18))
    middle2, close = bridge(middle2, close, at(live, 234.07, 234.17))
    close, close_tail = bridge(close, close_tail, at(donor2_close, 232.67, 232.82))

    parts = [before1, graft1, pause1, middle1, pause2, graft2, middle2, close, close_tail]
    edited = np.concatenate(parts)
    assert len(edited) == TOTAL_FRAMES * SPF, (len(edited), TOTAL_FRAMES * SPF)
    write_wav(OUT / "edited.wav", edited)

    return {
        "sample_rate": SR,
        "crossfade_to_matched_tone_ms": 5,
        "gains_db": {
            "half-million-estimate": 1.01,
            "business-incentive": 0.44,
            "exact-close": 2.35,
        },
        "limiter": "0.95 linear (-0.45 dBFS), attack 5 ms, release 50 ms, auto-level disabled",
        "grafts": [
            {
                "label": "half-million-estimate",
                "base_frames": list(BASE_GRAFT1),
                "base_seconds": [v / FPS for v in BASE_GRAFT1],
                "donor": str(DONOR1),
                "donor_frames": list(DONOR1_GRAFT1),
                "donor_seconds": [v / FPS for v in DONOR1_GRAFT1],
                "output_frames": [GRAFT1_OUT[0], GRAFT1_OUT[1] - PAUSE1],
                "words": "Raskin later regretted what this design became. By his own estimate, the Infinite Scroll now consumes half a million human lifetimes every single month.",
            },
            {
                "label": "business-incentive",
                "base_frames": list(BASE_GRAFT2),
                "base_seconds": [v / FPS for v in BASE_GRAFT2],
                "donor": str(DONOR2),
                "donor_frames": list(DONOR2_GRAFT2),
                "donor_seconds": [v / FPS for v in DONOR2_GRAFT2],
                "output_frames": list(GRAFT2_OUT),
                "words": "Tech companies rigorously track retention, session length, and habit formation. High engagement metrics drive immediate revenue through ad placements, direct purchases, and long-term subscriptions. AI companies benefit significantly when you start using their product as an embedded daily routine rather than an occasional utility. Helpful follow-up offers facilitate that transition smoothly.",
                "excluded_next_sentence_begins_at_source_frame": 6013,
            },
            {
                "label": "exact-close",
                "base_frames": [BASE_CLOSE, 7265],
                "base_seconds": [BASE_CLOSE / FPS, 7265 / FPS],
                "donor": str(DONOR2),
                "donor_frames": list(DONOR2_CLOSE),
                "donor_seconds": [v / FPS for v in DONOR2_CLOSE],
                "output_frames": [CLOSE_OUT[0], CLOSE_OUT[0] + DONOR2_CLOSE[1] - DONOR2_CLOSE[0]],
                "words": "Know what you came for. When you have it, choose what happens next.",
            },
        ],
        "approved_pauses": [
            {
                "after": "half-million estimate",
                "inserted_frames": PAUSE1,
                "inserted_seconds": PAUSE1 / FPS,
                "planned_total_strict_silence_seconds": 0.75,
            },
            {
                "before": "business-incentive explanation",
                "inserted_frames": PAUSE2,
                "inserted_seconds": PAUSE2 / FPS,
                "planned_total_strict_silence_seconds": 0.75,
            },
        ],
        "close_tail_frames": tail_frames,
    }


def target(label: str, at_seconds: float, rect: list[int], camera: list[int]) -> dict:
    return {
        "label": label,
        "at": at_seconds,
        "rects": [rect],
        "cam": camera,
        "color": NEUTRAL,
        "radius": 18,
    }


def prepare_visuals() -> tuple[Build, np.ndarray]:
    builder = Build(ROOT, LIVE, OUT, DEST, protected=[DONOR1, DONOR2, LESSON, INDEX, COMPARISON, SCROLL, STOPPING, CLOSE])
    builder.board(
        "comparison-first-entry",
        COMPARISON,
        BOARD1[0],
        BOARD1[1],
        "dense",
        [
            target(
                "complete AI answer and follow-up",
                18.700,
                [80, 452, 1001, 668],
                [40, 127, 1560, 708],
            )
        ],
        push=False,
    )
    chat_only = OUT / "comparison-chat-only.png"
    if not chat_only.exists():
        comparison = cv2.imread(str(COMPARISON))
        assert comparison is not None and comparison.shape[0] >= 740
        cv2.imwrite(str(chat_only), comparison[:740])
    builder.board(
        "comparison-chat-only",
        chat_only,
        0,
        BOARD1[1] - BOARD1[0] - 60,
        "compact",
        [
            target(
                "complete AI answer and follow-up",
                0.000,
                [80, 452, 1001, 668],
                [0, 0, 1600, 740],
            )
        ],
        min_open=0,
        push=False,
    )
    required_legs = {
        "comparison-first-entry": BOARD1[1] - BOARD1[0],
        "comparison-chat-only": BOARD1[1] - BOARD1[0] - 60,
    }
    if any(
        not (OUT / f"leg-{key}.mkv").exists()
        or media_properties(OUT / f"leg-{key}.mkv")[0] != frames
        for key, frames in required_legs.items()
    ):
        builder.render_legs()
    builder.state_sheet("comparison-first-entry")
    builder.state_sheet("comparison-chat-only")

    close_png = OUT / "close.png"
    if not close_png.exists():
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/video/make_close_board.py"),
                "--lesson",
                "engagementtrap",
                "--out",
                str(close_png),
            ],
            check=True,
        )
    close_image = cv2.imread(str(close_png))
    assert close_image is not None
    return builder, close_image


class Reader:
    def __init__(self, path: Path):
        self.cap = cv2.VideoCapture(str(path))
        self.index = -1
        self.image = None

    def at(self, frame: int) -> np.ndarray:
        assert frame >= self.index, (frame, self.index)
        while self.index < frame:
            ok, self.image = self.cap.read()
            assert ok, (frame, self.index)
            self.index += 1
        return self.image.copy()


def close_frame(image: np.ndarray, relative: int) -> np.ndarray:
    q = np.clip((relative - 48) / 149, 0, 1)
    zoom = 1 + 0.2 * q * q * (3 - 2 * q)
    h, w = image.shape[:2]
    crop_w = w / zoom
    crop_h = crop_w * 9 / 16
    return cv2.warpAffine(
        image,
        np.float32(
            [
                [crop_w / W, 0, (w - crop_w) / 2],
                [0, crop_h / H, (h - crop_h) / 2],
            ]
        ),
        (W, H),
        flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP,
    )


def render(close_image: np.ndarray) -> None:
    assert not DEST.exists(), f"{DEST} exists; choose a new version instead of overwriting"
    live = Reader(LIVE)
    board1_full = Reader(OUT / "leg-comparison-first-entry.mkv")
    board1_chat = Reader(OUT / "leg-comparison-chat-only.mkv")
    process = subprocess.Popen(
        [
            FFMPEG,
            "-y",
            "-v",
            "error",
            "-f",
            "rawvideo",
            "-pix_fmt",
            "bgr24",
            "-s",
            f"{W}x{H}",
            "-r",
            str(FPS),
            "-i",
            "pipe:0",
            "-i",
            str(OUT / "edited.wav"),
            "-map",
            "0:v",
            "-map",
            "1:a",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-preset",
            "medium",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-movflags",
            "+faststart",
            str(DEST),
        ],
        stdin=subprocess.PIPE,
    )

    for frame in range(TOTAL_FRAMES):
        if frame < BASE_GRAFT1[0]:
            if BOARD1[0] <= frame < BOARD1[0] + 60:
                image = board1_full.at(frame - BOARD1[0])
            elif BOARD1[0] + 60 <= frame < BOARD1[1]:
                image = board1_chat.at(frame - BOARD1[0] - 60)
            else:
                image = live.at(frame)
        elif frame < GRAFT1_OUT[1]:
            # Last live board frame already carries the existing takeaway ring.
            image = live.at(BASE_GRAFT1[0] - 1)
        elif frame < MIDDLE1_OUT[1]:
            source = min(
                MIDDLE1_VISUAL_START + (frame - MIDDLE1_OUT[0]),
                BASE_GRAFT2[0] - 1,
            )
            image = live.at(source)
        elif frame < PAUSE2_OUT[1]:
            image = live.at(BASE_GRAFT2[0] - 1)
        elif frame < GRAFT2_OUT[1]:
            # Preserve, rather than duplicate, the live phone/person sequence.
            # Its 337 source frames are evenly retimed across the 699-frame donor.
            relative = frame - GRAFT2_OUT[0]
            source = BASE_GRAFT2[0] - 1 + math.floor(
                relative * (BASE_GRAFT2[1] - BASE_GRAFT2[0]) /
                (GRAFT2_OUT[1] - GRAFT2_OUT[0])
            )
            source = min(source, BASE_GRAFT2[1] - 1)
            image = live.at(source)
        elif frame < MIDDLE2_OUT[1]:
            source = BASE_GRAFT2[1] + (frame - MIDDLE2_OUT[0])
            image = live.at(source)
        else:
            image = close_frame(close_image, frame - CLOSE_OUT[0])
        process.stdin.write(image.tobytes())

    process.stdin.close()
    if process.wait() != 0:
        raise SystemExit("ffmpeg failed while writing review candidate")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    assert sha(LIVE) == LIVE_SHA
    assert sha(DONOR1) == DONOR1_SHA
    assert sha(DONOR2) == DONOR2_SHA
    assert media_properties(LIVE) == (7265, 30.0, 1280, 720)
    assert media_properties(DONOR1) == (7603, 30.0, 1280, 720)
    assert media_properties(DONOR2) == (7081, 30.0, 1280, 720)

    protected = [LIVE, DONOR1, DONOR2, LESSON, INDEX, COMPARISON, SCROLL, STOPPING, CLOSE]
    protected_hashes = {str(path): sha(path) for path in protected}
    audio = prepare_audio()
    builder, close_image = prepare_visuals()

    boundaries = [
        {"frame": BOARD1[0], "label": "corrected-full-comparison-board-in"},
        {"frame": BOARD1[0] + 60, "label": "full-comparison-to-complete-top-chat"},
        {"frame": BOARD1[1], "label": "corrected-comparison-board-out"},
        {"frame": GRAFT1_OUT[0], "label": "half-million-graft-and-board-hold-in"},
        {"frame": GRAFT1_OUT[1], "label": "half-million-board-hold-out"},
        {"frame": GRAFT2_OUT[0], "label": "business-graft-retime-in"},
        {"frame": GRAFT2_OUT[1], "label": "business-graft-retime-out"},
        {"frame": CLOSE_OUT[0], "label": "canonical-close-in"},
    ]
    manifest = {
        "output": str(DEST),
        "scope": "Approved narrow live repair review candidate; live video and lesson materials unchanged",
        "sources": {
            "live": {"path": str(LIVE), "sha256": LIVE_SHA},
            "engagement-trap-1": {"path": str(DONOR1), "sha256": DONOR1_SHA},
            "engagement-trap-2": {"path": str(DONOR2), "sha256": DONOR2_SHA},
        },
        "fps": FPS,
        "total_frames": TOTAL_FRAMES,
        "duration": TOTAL_FRAMES / FPS,
        "audio": audio,
        "visuals": {
            "comparison_first_entry": {
                "source_frames": list(BOARD1),
                "treatment": "current canonical board: 60-frame complete-board hold, then a clean complete top-chat crop with AI-answer ring; no partial outcome cards",
                "asset": str(COMPARISON.relative_to(ROOT)),
                "board_specs": {
                    "full": builder.boards["comparison-first-entry"],
                    "top_chat": builder.boards["comparison-chat-only"],
                },
            },
            "half_million_graft": "hold the live scroll-board takeaway-ring frame; no donor visuals",
            "half_million_graft_exit": {
                "audio_resumes_at_source_frame": BASE_GRAFT1[1],
                "picture_resumes_at_source_frame": MIDDLE1_VISUAL_START,
                "reason": "advance the approved destination drawing over three silent shoulder frames; prevents a 3-frame old-board island",
            },
            "business_graft": {
                "source_frames": [BASE_GRAFT2[0] - 1, BASE_GRAFT2[1]],
                "treatment": "evenly retime the existing live phone/person sequence; no donor metrics graphics",
            },
            "stopping_point": "existing live board and banner highlight preserved after the graft",
            "close": {
                "asset": str(CLOSE.relative_to(ROOT)),
                "frames": CLOSE_FRAMES,
                "prehold_frames": 48,
                "push_frames": 150,
                "settled_frames": 120,
            },
        },
        "boundaries": boundaries,
        "protected_hashes": protected_hashes,
        "listening_status": "Automated acoustic checks only; final headphone audition required",
    }
    (OUT / "edit-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("Prepared", TOTAL_FRAMES, f"{TOTAL_FRAMES / FPS:.3f}s", flush=True)
    if args.prepare_only:
        return

    render(close_image)
    assert media_properties(DEST) == (TOTAL_FRAMES, 30.0, 1280, 720)
    current = json.loads((OUT / "edit-manifest.json").read_text())
    current["render_sha256"] = sha(DEST)
    current["protected_files_unchanged"] = {
        path: sha(Path(path)) == digest for path, digest in protected_hashes.items()
    }
    assert all(current["protected_files_unchanged"].values())
    (OUT / "edit-manifest.json").write_text(json.dumps(current, indent=2) + "\n")
    print(DEST, media_properties(DEST), flush=True)


if __name__ == "__main__":
    main()

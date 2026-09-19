#!/usr/bin/env python3
"""Build the approved Training Bias best-of review candidate (2026-09-18).

The shipped 30 fps lesson is the narration and picture spine. Two complete
teaching beats come from training-bias-2: the exact three student prompts and
the Cooper Flagg/current-source explanation. All five course boards are rebuilt
from the current JPGs, retained Notebook frames have the Gemini corner mark
cleaned, and the current standard close replaces the engine close.

Review only: writes Prompts/training-bias-v3.mp4 and a new audit directory.
It never modifies the live video, either source roll, or lesson materials.
"""

from __future__ import annotations

from fractions import Fraction
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
from editspec_build import (  # noqa: E402
    AMBER,
    BLUE,
    CLOSE_PREHOLD,
    CLOSE_PUSH,
    NEUTRAL,
    PURPLE,
    TEAL,
    Build,
)
from gemini_mark import clean_frame, glyph_mask  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "course-assets/training-bias/training-bias.mp4"
DONOR = ROOT / "Prompts/training-bias-2.mp4"
DEST = ROOT / "Prompts/training-bias-v3.mp4"
OUT = ROOT / "video-audit/training-bias-repair-2026-09-18-v3"

ASSETS = ROOT / "course-assets/training-bias"
WRONG = ASSETS / "training-bias-wrong-pattern.jpg"
MECHANISMS = ASSETS / "training-bias-how-bias-happens.jpg"
QUESTIONS = ASSETS / "training-bias-questions-to-ask.jpg"
STALE = ASSETS / "training-bias-stale.jpg"
RAG = ASSETS / "training-bias-rag.jpg"
CLOSE = ASSETS / "training-bias-close.jpg"
LESSON = ROOT / "lessons/training-bias.md"
INDEX = ROOT / "index.html"

FPS = 30
DONOR_FPS = 24
SR = 48_000
SPF = SR // FPS
W, H = 1280, 720
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# Approved whole-beat replacement ranges. All intervals are half-open.
BASE_GRAFT_1 = (3636, 4245)  # 2:01.20-2:21.50; return after "examples"
DONOR_GRAFT_1 = (4055, 4825)  # 2:48.958-3:21.042 at 24 fps
BASE_GRAFT_2 = (4884, 6180)  # 2:42.80-3:26.00; enter after "outdated picture", return after "RAG"
DONOR_GRAFT_2 = (5420, 7250)  # 3:45.833-5:02.083 at 24 fps


def donor_to_output(frame: int) -> int:
    return math.ceil(frame * FPS / DONOR_FPS)


GRAFT_1_FRAMES = donor_to_output(DONOR_GRAFT_1[1]) - donor_to_output(DONOR_GRAFT_1[0])
GRAFT_2_FRAMES = donor_to_output(DONOR_GRAFT_2[1]) - donor_to_output(DONOR_GRAFT_2[0])
DELTA_1 = GRAFT_1_FRAMES - (BASE_GRAFT_1[1] - BASE_GRAFT_1[0])
DELTA_2 = GRAFT_2_FRAMES - (BASE_GRAFT_2[1] - BASE_GRAFT_2[0])
GRAFT_1_OUT = (BASE_GRAFT_1[0], BASE_GRAFT_1[0] + GRAFT_1_FRAMES)
GRAFT_2_OUT = (
    BASE_GRAFT_2[0] + DELTA_1,
    BASE_GRAFT_2[0] + DELTA_1 + GRAFT_2_FRAMES,
)

# The donor cuts from its historical-chat composite to a clean Notebook drawing
# at 4:20.542. At 4:57.208 it cuts to an obsolete embedded RAG board, so the
# last clean drawing holds for the remaining 4.9 seconds of the donor beat.
DONOR_NOTEBOOK_START = 6253
DONOR_NOTEBOOK_END = 7133
STALE_OUT_END = GRAFT_2_OUT[0] + (
    donor_to_output(DONOR_NOTEBOOK_START) - donor_to_output(DONOR_GRAFT_2[0])
)

# Exact live visual cuts established by sequential frame inspection.
LIVE_CUTS = {
    "wrong_in": 453,
    "wrong_out": 854,
    "mechanisms_in": 1781,
    "mechanisms_out": 2984,
    "questions_in": 3404,
    "questions_out": 4271,
    "close_in": 7233,
    "end": 7488,
}


def base_to_output(frame: int) -> int:
    if frame <= BASE_GRAFT_1[0]:
        return frame
    if frame >= BASE_GRAFT_2[1]:
        return frame + DELTA_1 + DELTA_2
    if frame >= BASE_GRAFT_1[1]:
        return frame + DELTA_1
    raise ValueError(f"base frame {frame} lies inside a replaced span")


CLOSE_START = base_to_output(LIVE_CUTS["close_in"])
TOTAL_FRAMES = base_to_output(LIVE_CUTS["end"])


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frame_count(path: Path) -> tuple[int, float, int, int]:
    cap = cv2.VideoCapture(str(path))
    result = (
        int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        cap.get(cv2.CAP_PROP_FPS),
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )
    cap.release()
    return result


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


def rms(samples: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(samples))))


def decode_base_audio(path: Path) -> None:
    if path.exists():
        return
    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-v",
            "error",
            "-i",
            str(BASE),
            "-vn",
            "-ac",
            "1",
            "-ar",
            str(SR),
            "-c:a",
            "pcm_s16le",
            str(path),
        ],
        check=True,
    )


def decode_filtered_donor(path: Path, start: int, end: int, gain_db: float) -> None:
    if path.exists():
        return
    start_seconds = float(Fraction(start, DONOR_FPS))
    duration_seconds = float(Fraction(end - start, DONOR_FPS))
    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-v",
            "error",
            "-i",
            str(DONOR),
            "-ss",
            f"{start_seconds:.9f}",
            "-t",
            f"{duration_seconds:.9f}",
            "-vn",
            "-af",
            f"volume={gain_db:.2f}dB,alimiter=limit=0.95:attack=5:release=50:level=false",
            "-ac",
            "1",
            "-ar",
            str(SR),
            "-c:a",
            "pcm_s16le",
            str(path),
        ],
        check=True,
    )


def best_room_tone(base: np.ndarray) -> tuple[np.ndarray, tuple[float, float], float]:
    windows = (
        (28.20, 30.20),
        (49.60, 49.80),
        (139.20, 142.20),
        (201.00, 201.20),
        (221.20, 224.20),
        (240.20, 242.20),
    )
    candidates = []
    for start, end in windows:
        for t in np.arange(start, end - 0.10, 0.01):
            segment = base[round(t * SR):round((t + 0.10) * SR)]
            candidates.append((rms(segment), float(t), segment.copy()))
    level, at, seed = min(candidates, key=lambda item: item[0])
    seed -= seed.mean()
    return np.r_[seed, seed[::-1]], (at, at + 0.10), level


def fade_to_tone(
    samples: np.ndarray,
    loop: np.ndarray,
    *,
    fade_in: bool = False,
    fade_out: bool = False,
    fade_samples: int = 240,
) -> np.ndarray:
    out = samples.copy()
    bed = np.resize(loop, len(out))
    ramp = np.linspace(0.0, 1.0, fade_samples)
    if fade_in:
        out[:fade_samples] = bed[:fade_samples] * (1.0 - ramp) + out[:fade_samples] * ramp
    if fade_out:
        out[-fade_samples:] = out[-fade_samples:] * (1.0 - ramp) + bed[-fade_samples:] * ramp
    return out


def fit_audio(samples: np.ndarray, length: int, loop: np.ndarray) -> np.ndarray:
    if len(samples) >= length:
        return samples[:length].copy()
    return np.concatenate([samples, np.resize(loop, length - len(samples))])


def prepare_audio() -> dict:
    base_path = OUT / "base.wav"
    graft_1_path = OUT / "graft-questions.wav"
    graft_2_path = OUT / "graft-stale.wav"
    decode_base_audio(base_path)

    # EBU R128 measurements on speech windows gave -17.95 LUFS for the live
    # neighborhood versus -23.51 for graft 1, and -16.93 versus -21.72 for
    # graft 2. Peak-safe limiting after the corresponding gains keeps both
    # inserts within 0.2 LU of their live neighborhoods without clipping.
    decode_filtered_donor(graft_1_path, *DONOR_GRAFT_1, gain_db=5.56)
    decode_filtered_donor(graft_2_path, *DONOR_GRAFT_2, gain_db=4.79)

    base = read_wav(base_path)
    graft_1 = read_wav(graft_1_path)
    graft_2 = read_wav(graft_2_path)
    loop, tone_window, tone_level = best_room_tone(base)
    graft_1 = fit_audio(graft_1, GRAFT_1_FRAMES * SPF, loop)
    graft_2 = fit_audio(graft_2, GRAFT_2_FRAMES * SPF, loop)

    before = fade_to_tone(base[:BASE_GRAFT_1[0] * SPF], loop, fade_out=True)
    graft_1 = fade_to_tone(graft_1, loop, fade_in=True, fade_out=True)
    middle = fade_to_tone(
        base[BASE_GRAFT_1[1] * SPF:BASE_GRAFT_2[0] * SPF],
        loop,
        fade_in=True,
        fade_out=True,
    )
    graft_2 = fade_to_tone(graft_2, loop, fade_in=True, fade_out=True)
    after = fade_to_tone(
        base[BASE_GRAFT_2[1] * SPF:LIVE_CUTS["end"] * SPF],
        loop,
        fade_in=True,
    )
    edited = np.concatenate([before, graft_1, middle, graft_2, after])
    assert len(edited) == TOTAL_FRAMES * SPF, (len(edited), TOTAL_FRAMES * SPF)
    write_wav(OUT / "edited.wav", edited)
    return {
        "sample_rate": SR,
        "room_tone_source_seconds": list(tone_window),
        "room_tone_rms": tone_level,
        "join_crossfade_ms": 5,
        "graft_1_gain_db": 5.56,
        "graft_2_gain_db": 4.79,
        "graft_limiter": "0.95 linear (-0.45 dBFS), attack 5 ms, release 50 ms, auto-level disabled",
        "measurement": {
            "graft_1_live_lufs": -17.95,
            "graft_1_donor_lufs": -23.51,
            "graft_1_filtered_lufs": -18.05,
            "graft_2_live_lufs": -16.93,
            "graft_2_donor_lufs": -21.72,
            "graft_2_filtered_lufs": -17.10,
        },
        "added_teaching_pauses": [],
    }


def target(label: str, frame: int, rect: list[int], color: str) -> dict:
    return {
        "label": label,
        "at": frame / FPS,
        "rects": [rect],
        "cam": rect,
        "color": color,
        "radius": 18,
    }


def donor_onset(seconds: float, graft_start: tuple[int, int], output_start: int) -> int:
    return output_start + round((seconds - float(Fraction(graft_start[0], DONOR_FPS))) * FPS)


def build_boards(builder: Build, spans: dict[str, tuple[int, int]]) -> None:
    builder.board(
        "wrong-pattern",
        WRONG,
        *spans["wrong-pattern"],
        "compact",
        [target("takeaway banner", 714, [40, 1180, 1560, 1269], NEUTRAL)],
        push=False,
    )

    cards = ([40, 127, 526, 652], [558, 127, 1044, 652], [1076, 127, 1560, 652])
    builder.board(
        "mechanisms",
        MECHANISMS,
        *spans["mechanisms"],
        "compact",
        [
            target("Defaults", 1956, list(cards[0]), PURPLE),
            target("Blind Spots", 2256, list(cards[1]), BLUE),
            target("Wrong Patterns", 2586, list(cards[2]), AMBER),
        ],
        push=False,
    )

    q_start = GRAFT_1_OUT[0]
    builder.board(
        "questions",
        QUESTIONS,
        *spans["questions"],
        "compact",
        [
            target(
                "takeaway banner",
                donor_onset(171.52, DONOR_GRAFT_1, q_start),
                [40, 697, 1560, 786],
                NEUTRAL,
            ),
            target(
                "Ask What's Missing",
                donor_onset(184.96, DONOR_GRAFT_1, q_start),
                list(cards[0]),
                PURPLE,
            ),
            target(
                "Ask for Exceptions",
                donor_onset(189.44, DONOR_GRAFT_1, q_start),
                list(cards[1]),
                BLUE,
            ),
            target(
                "Remove the Famous",
                donor_onset(195.36, DONOR_GRAFT_1, q_start),
                list(cards[2]),
                AMBER,
            ),
        ],
        push=False,
    )

    builder.board(
        "stale",
        STALE,
        *spans["stale"],
        "compact",
        [
            target(
                "student statement",
                donor_onset(232.24, DONOR_GRAFT_2, GRAFT_2_OUT[0]),
                [611, 202, 1520, 338],
                NEUTRAL,
            ),
            target(
                "AI questions correct fact",
                donor_onset(237.76, DONOR_GRAFT_2, GRAFT_2_OUT[0]),
                [80, 401, 980, 537],
                NEUTRAL,
            ),
            target(
                "search and date prompt",
                donor_onset(247.36, DONOR_GRAFT_2, GRAFT_2_OUT[0]),
                [606, 600, 1520, 735],
                NEUTRAL,
            ),
            target(
                "corrected answer",
                donor_onset(250.24, DONOR_GRAFT_2, GRAFT_2_OUT[0]),
                [80, 799, 970, 934],
                NEUTRAL,
            ),
        ],
        push=False,
    )

    rag_start = GRAFT_2_OUT[1]
    builder.board(
        "rag",
        RAG,
        *spans["rag"],
        "compact",
        [
            target("Retrieve", rag_start + 90, [40, 127, 526, 611], PURPLE),
            target("Add to Context", rag_start + 210, [558, 127, 1044, 611], BLUE),
            target("Generate", rag_start + 450, [1076, 127, 1560, 611], TEAL),
            target("RAG caveat", rag_start + 660, [40, 650, 1560, 740], NEUTRAL),
        ],
        push=False,
    )


class Reader:
    def __init__(self, path: Path):
        self.cap = cv2.VideoCapture(str(path))
        self.index = -1
        self.image = None

    def at(self, frame: int) -> np.ndarray:
        assert frame >= self.index, (frame, self.index)
        while self.index < frame:
            ok, self.image = self.cap.read()
            assert ok, ("source exhausted", frame, self.index)
            self.index += 1
        return self.image.copy()


def base_frame_for_output(frame: int) -> int:
    if frame < GRAFT_1_OUT[0]:
        return frame
    if frame < GRAFT_1_OUT[1]:
        raise ValueError("graft 1 has no live source frame")
    if frame < GRAFT_2_OUT[0]:
        return frame - DELTA_1
    if frame < GRAFT_2_OUT[1]:
        raise ValueError("graft 2 has no live source frame")
    return frame - DELTA_1 - DELTA_2


def close_frame(image: np.ndarray, frame: int) -> np.ndarray:
    k = frame - CLOSE_START
    q = np.clip((k - CLOSE_PREHOLD) / (CLOSE_PUSH - 1), 0, 1)
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


def render(builder: Build, spans: dict[str, tuple[int, int]]) -> dict:
    assert not DEST.exists(), f"{DEST} exists; choose a new version instead of overwriting"
    base = Reader(BASE)
    donor = Reader(DONOR)
    legs = {key: Reader(OUT / f"leg-{key}.mkv") for key in spans}
    board_ranges = [(start, end, key) for key, (start, end) in spans.items()]
    mask = glyph_mask()
    corner = {
        "live": {"clone": 0, "inpaint": 0, "declined": []},
        "donor_notebook": {"clone": 0, "inpaint": 0, "declined": []},
    }

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
        if frame >= CLOSE_START:
            image = close_frame(builder.close_img, frame)
        else:
            board = next((key for start, end, key in board_ranges if start <= frame < end), None)
            if board is not None:
                image = legs[board].at(frame - spans[board][0])
            elif GRAFT_2_OUT[0] <= frame < GRAFT_2_OUT[1]:
                relative = frame - GRAFT_2_OUT[0]
                donor_frame = DONOR_GRAFT_2[0] + math.floor(relative * DONOR_FPS / FPS)
                donor_frame = min(donor_frame, DONOR_NOTEBOOK_END - 1)
                assert donor_frame >= DONOR_NOTEBOOK_START, donor_frame
                image = donor.at(donor_frame)
                image, method = clean_frame(image, mask)
                if method in ("clone", "inpaint"):
                    corner["donor_notebook"][method] += 1
                else:
                    corner["donor_notebook"]["declined"].append(
                        {"output_frame": frame, "donor_frame": donor_frame}
                    )
            else:
                source_frame = base_frame_for_output(frame)
                image = base.at(source_frame)
                image, method = clean_frame(image, mask)
                if method in ("clone", "inpaint"):
                    corner["live"][method] += 1
                else:
                    corner["live"]["declined"].append(
                        {"output_frame": frame, "source_frame": source_frame}
                    )
        process.stdin.write(image.tobytes())

    process.stdin.close()
    assert process.wait() == 0
    return corner


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    protected = [BASE, DONOR, LESSON, INDEX, WRONG, MECHANISMS, QUESTIONS, STALE, RAG, CLOSE]
    hashes = {str(path): sha(path) for path in protected}
    assert frame_count(BASE) == (7488, 30.0, 1280, 720), frame_count(BASE)
    assert frame_count(DONOR) == (8492, 24.0, 1280, 720), frame_count(DONOR)
    assert (GRAFT_1_FRAMES, GRAFT_2_FRAMES, TOTAL_FRAMES) == (963, 2288, 8834)

    spans = {
        "wrong-pattern": (LIVE_CUTS["wrong_in"], LIVE_CUTS["wrong_out"]),
        "mechanisms": (LIVE_CUTS["mechanisms_in"], LIVE_CUTS["mechanisms_out"]),
        "questions": (
            LIVE_CUTS["questions_in"],
            base_to_output(LIVE_CUTS["questions_out"]),
        ),
        "stale": (GRAFT_2_OUT[0], STALE_OUT_END),
        "rag": (GRAFT_2_OUT[1], CLOSE_START),
    }
    audio = prepare_audio()
    builder = Build(ROOT, BASE, OUT, DEST, protected=protected[1:])
    build_boards(builder, spans)
    prepared_legs = True
    for key, (start, end) in spans.items():
        leg = OUT / f"leg-{key}.mkv"
        if not leg.exists() or frame_count(leg)[0] != end - start:
            prepared_legs = False
            break
    if not prepared_legs:
        for key, board in builder.boards.items():
            leg = OUT / f"leg-{key}.mkv"
            expected = board["src_out"] - board["src_in"]
            if leg.exists() and frame_count(leg)[0] == expected:
                continue
            (OUT / "preview" / key).mkdir(parents=True, exist_ok=True)
            subprocess.run(
                [
                    str(builder.py),
                    str(builder.kb),
                    str(OUT / f"leg-{key}.json"),
                    "--preview",
                    str(OUT / "preview" / key),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            subprocess.run(
                [
                    str(builder.py),
                    str(builder.kb),
                    str(OUT / f"leg-{key}.json"),
                    str(leg),
                ],
                check=True,
                stdout=subprocess.DEVNULL,
            )
            assert frame_count(leg)[0] == expected, (key, frame_count(leg)[0], expected)
    for key in spans:
        builder.state_sheet(key)
    close_canvas, _, _, _, _ = builder.compose(CLOSE, "close")
    builder.close_img = cv2.imread(str(close_canvas))

    boundaries = sorted(
        [
            {"frame": GRAFT_1_OUT[0], "label": "questions-audio-graft-in"},
            {"frame": GRAFT_1_OUT[1], "label": "questions-audio-graft-out"},
            {"frame": GRAFT_2_OUT[0], "label": "stale-audio-graft-in"},
            {"frame": STALE_OUT_END, "label": "stale-board-to-donor-notebook"},
            {"frame": GRAFT_2_OUT[1], "label": "stale-audio-graft-out-and-rag-board-in"},
            {"frame": CLOSE_START, "label": "standard-close-in"},
            *[
                {"frame": point, "label": f"{key}-{'in' if point == start else 'out'}"}
                for key, (start, end) in spans.items()
                for point in (start, end)
                if point not in (GRAFT_2_OUT[0], STALE_OUT_END, GRAFT_2_OUT[1], CLOSE_START)
            ],
        ],
        key=lambda row: row["frame"],
    )

    manifest = {
        "output": str(DEST),
        "base": str(BASE),
        "donor": str(DONOR),
        "scope": "Review-only live-base repair; published video and lesson materials unchanged",
        "fps": FPS,
        "total_frames": TOTAL_FRAMES,
        "duration": TOTAL_FRAMES / FPS,
        "approved_plan": "Live narration spine; exact prompt and Cooper Flagg donor beats; current boards; no added teaching pauses; canonical close",
        "grafts": [
            {
                "label": "exact student prompts",
                "live_frames": list(BASE_GRAFT_1),
                "live_seconds": [v / FPS for v in BASE_GRAFT_1],
                "donor_frames_24fps": list(DONOR_GRAFT_1),
                "donor_seconds": [float(Fraction(v, DONOR_FPS)) for v in DONOR_GRAFT_1],
                "output_frames": list(GRAFT_1_OUT),
                "output_seconds": [v / FPS for v in GRAFT_1_OUT],
                "visual": "current Three Questions That Reveal Bias board",
            },
            {
                "label": "Cooper Flagg example, causal caveat, and RAG lead-in",
                "live_frames": list(BASE_GRAFT_2),
                "live_seconds": [v / FPS for v in BASE_GRAFT_2],
                "donor_frames_24fps": list(DONOR_GRAFT_2),
                "donor_seconds": [float(Fraction(v, DONOR_FPS)) for v in DONOR_GRAFT_2],
                "output_frames": list(GRAFT_2_OUT),
                "output_seconds": [v / FPS for v in GRAFT_2_OUT],
                "visual": "current stale chat board, then donor current-source/outside-information Notebook drawings",
            },
        ],
        "audio": audio,
        "boards": builder.boards,
        "board_output_spans": {key: list(value) for key, value in spans.items()},
        "board_treatment": "All five current JPGs are static full views with post-crop rings; no zoom or pan",
        "donor_notebook_visual": {
            "source_frames_24fps": [DONOR_NOTEBOOK_START, DONOR_NOTEBOOK_END],
            "hold_last_frame_after": DONOR_NOTEBOOK_END - 1,
            "reason": "Avoid donor's obsolete embedded RAG board while retaining the current-source and outside-information drawings",
        },
        "close": {
            "start_frame": CLOSE_START,
            "prehold_frames": CLOSE_PREHOLD,
            "push_frames": CLOSE_PUSH,
            "zoom_endpoint": 1.2,
            "settled_frames": TOTAL_FRAMES - CLOSE_START - CLOSE_PREHOLD - CLOSE_PUSH,
            "current_asset": str(CLOSE.relative_to(ROOT)),
        },
        "boundaries": boundaries,
        "protected_hashes": hashes,
        "human_listening_required": "Final four graft joins and perceived voice/room match must be auditioned on headphones",
    }
    (OUT / "edit-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("Prepared", TOTAL_FRAMES, f"{TOTAL_FRAMES / FPS:.3f}s", spans, flush=True)
    if args.prepare_only:
        return

    corner = render(builder, spans)
    actual = frame_count(DEST)
    assert actual == (TOTAL_FRAMES, 30.0, 1280, 720), actual
    current = json.loads((OUT / "edit-manifest.json").read_text())
    current["corner_mark"] = corner
    current["render_sha256"] = sha(DEST)
    current["protected_files_unchanged"] = {
        path: sha(Path(path)) == digest for path, digest in hashes.items()
    }
    assert all(current["protected_files_unchanged"].values())
    (OUT / "edit-manifest.json").write_text(json.dumps(current, indent=2) + "\n")
    print(DEST, actual, flush=True)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the approved Hallucination best-of review candidate (2026-09-18).

Full production pass from Prompts/hallucination-2.mp4.  The narration stays on
roll 2 except for one approved whole-beat audio graft from the shipped roll:
the grammatical pizza-question sentence.  The graft sits over roll 2's static
pizza drawing.  Current course JPGs replace every Notebook course-board render,
the engine outro is removed, and the canonical standard close is the final frame.

Review only: writes Prompts/hallucination-v4.mp4 and an audit directory.  It
does not touch the live video, lesson, assets, or older candidates.
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
BASE = ROOT / "Prompts/hallucination-2.mp4"
DONOR = ROOT / "course-assets/hallucination/hallucination.mp4"
DEST = ROOT / "Prompts/hallucination-v4.mp4"
OUT = ROOT / "video-audit/hallucination-best-of-2026-09-18"

ASSETS = ROOT / "course-assets/hallucination"
EXAMPLE = ASSETS / "hallucination-example.jpg"
WHY = ASSETS / "hallucination-why-ai-makes-things-up.jpg"
REAL_TEXT = ASSETS / "hallucination-glue-on-pizza.jpg"
CHECK = ASSETS / "hallucination-check-claim.jpg"
CLOSE = ASSETS / "hallucination-close.jpg"
LESSON = ROOT / "lessons/hallucination.md"

FPS = 30
BASE_FPS = 24
SR = 48_000
SPF = SR // FPS
W, H = 1280, 720
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# Whole-beat graft boundaries selected inside measured silence windows.
# Base 3:28.833-3:39.500 is replaced by donor 1:51.767-2:03.967.
BASE_GRAFT = (5012, 5268)       # 24 fps frames, half-open
DONOR_GRAFT = (3353, 3719)      # 30 fps frames, half-open
GRAFT_OUT_START = BASE_GRAFT[0] * FPS // BASE_FPS
GRAFT_FRAMES = DONOR_GRAFT[1] - DONOR_GRAFT[0]
BASE_GRAFT_OUT_FRAMES = (BASE_GRAFT[1] - BASE_GRAFT[0]) * FPS // BASE_FPS
DELTA = GRAFT_FRAMES - BASE_GRAFT_OUT_FRAMES
GRAFT_OUT_END = GRAFT_OUT_START + GRAFT_FRAMES

# Exact visual cuts found by sequential decode in the 24 fps base roll.
BASE_CUTS = {
    "intro_to_question": 570,
    "question_to_small_board": 1646,
    "example_to_definition": 2310,
    "definition_to_why": 3316,
    "why_to_pizza": 4541,
    "pizza_quote_to_context": 5309,
    "context_to_takeaway": 6060,
    "takeaway_to_check": 6690,
    "check_to_close": 7953,
    "close_to_engine_outro": 8107,
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def base_seconds(frame: int) -> Fraction:
    return Fraction(frame, BASE_FPS)


def donor_seconds(frame: int) -> Fraction:
    return Fraction(frame, FPS)


def base_frame_to_output(frame: int) -> int:
    """First 30 fps output frame at or after a 24 fps source-frame onset."""
    mapped = math.ceil(frame * FPS / BASE_FPS)
    if frame >= BASE_GRAFT[1]:
        mapped += DELTA
    return mapped


def output_frame_from_base_time(seconds: float) -> int:
    frame = round(seconds * FPS)
    if seconds >= float(base_seconds(BASE_GRAFT[1])):
        frame += DELTA
    return frame


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


def decode_audio(source: Path, dest: Path) -> None:
    if dest.exists():
        return
    subprocess.run(
        [
            FFMPEG,
            "-y",
            "-v",
            "error",
            "-i",
            str(source),
            "-vn",
            "-ac",
            "1",
            "-ar",
            str(SR),
            "-c:a",
            "pcm_s16le",
            str(dest),
        ],
        check=True,
    )


def fade_edge_to_tone(
    samples: np.ndarray,
    tone: np.ndarray,
    *,
    fade_in: bool,
    fade_out: bool,
    frames: int = 240,
) -> np.ndarray:
    out = samples.copy()
    ramp = np.linspace(0.0, 1.0, frames)
    if fade_in:
        out[:frames] = tone[:frames] * (1.0 - ramp) + out[:frames] * ramp
    if fade_out:
        out[-frames:] = out[-frames:] * (1.0 - ramp) + tone[-frames:] * ramp
    return out


def prepare_audio(total_frames: int) -> dict:
    base_wav = OUT / "base.wav"
    donor_wav = OUT / "donor.wav"
    decode_audio(BASE, base_wav)
    decode_audio(DONOR, donor_wav)
    base = read_wav(base_wav)
    donor = read_wav(donor_wav)

    b0 = round(float(base_seconds(BASE_GRAFT[0])) * SR)
    b1 = round(float(base_seconds(BASE_GRAFT[1])) * SR)
    bend = round(float(base_seconds(BASE_CUTS["close_to_engine_outro"])) * SR)
    d0 = round(float(donor_seconds(DONOR_GRAFT[0])) * SR)
    d1 = round(float(donor_seconds(DONOR_GRAFT[1])) * SR)

    # Speech-only windows sit inside the selected beats and exclude boundary tone.
    base_speech = base[round(209.015 * SR):round(219.336 * SR)]
    donor_speech = donor[round(112.073 * SR):round(123.686 * SR)]
    gain = rms(base_speech) / rms(donor_speech)
    gain_db = 20 * math.log10(gain)

    # Matched base-roll room tone from the same leading silence as the graft.
    seed = base[round(208.72 * SR):round(208.82 * SR)].copy()
    seed -= seed.mean()
    tone_loop = np.r_[seed, seed[::-1]]

    before = base[:b0]
    graft = donor[d0:d1] * gain
    after = base[b1:bend]
    before_tone = np.resize(tone_loop, len(before))
    graft_tone = np.resize(tone_loop, len(graft))
    after_tone = np.resize(tone_loop, len(after))
    before = fade_edge_to_tone(before, before_tone, fade_in=False, fade_out=True)
    graft = fade_edge_to_tone(graft, graft_tone, fade_in=True, fade_out=True)
    after = fade_edge_to_tone(after, after_tone, fade_in=True, fade_out=True)

    used = len(before) + len(graft) + len(after)
    target = total_frames * SPF
    assert used < target
    tail = np.resize(tone_loop, target - used)
    edited = np.concatenate([before, graft, after, tail])
    assert len(edited) == target
    write_wav(OUT / "edited.wav", edited)
    return {
        "sample_rate": SR,
        "base_cut_seconds": [float(base_seconds(BASE_GRAFT[0])), float(base_seconds(BASE_GRAFT[1]))],
        "donor_seconds": [float(donor_seconds(DONOR_GRAFT[0])), float(donor_seconds(DONOR_GRAFT[1]))],
        "donor_gain_db": gain_db,
        "crossfade_to_matched_tone_ms": 5,
        "room_tone_source_seconds": [208.72, 208.82],
        "engine_outro_audio_removed_from_seconds": float(base_seconds(BASE_CUTS["close_to_engine_outro"])),
        "settled_close_tone_seconds": (target - used) / SR,
    }


def target(label: str, at_frame: int, rect: list[int], color: str, *, full_view: bool = False) -> dict:
    return {
        "label": label,
        "at": at_frame / FPS,
        "rects": [rect],
        "cam": rect,
        "color": color,
        "radius": 18,
        "full_view": full_view,
    }


class SourceReader:
    """Sequential 24 fps decoder; repeated output frames reuse the current image."""

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


class LegReader:
    def __init__(self, path: Path):
        self.cap = cv2.VideoCapture(str(path))
        self.index = -1
        self.image = None

    def at(self, frame: int) -> np.ndarray:
        assert frame >= self.index, (frame, self.index)
        while self.index < frame:
            ok, self.image = self.cap.read()
            assert ok, ("leg exhausted", frame, self.index)
            self.index += 1
        return self.image.copy()


def build_boards(builder: Build, spans: dict[str, tuple[int, int]]) -> None:
    question = output_frame_from_base_time(33.68)
    answer = output_frame_from_base_time(44.16)
    false_banner = output_frame_from_base_time(71.86)
    builder.board(
        "example",
        EXAMPLE,
        *spans["example"],
        "compact",
        [
            target("question bubble", question, [605, 203, 1520, 338], NEUTRAL),
            target("AI response bubble", answer, [80, 401, 989, 618], NEUTRAL),
        ],
        banner_at=false_banner / FPS,
        banner=[40, 697, 1560, 786],
        push=False,
    )

    why_cards = [
        [56, 164, 362, 794],
        [452, 164, 756, 794],
        [844, 164, 1150, 794],
        [1234, 164, 1548, 794],
    ]
    builder.board(
        "why",
        WHY,
        *spans["why"],
        "dense",
        [
            target("Learns From the Text It's Fed", output_frame_from_base_time(147.70), why_cards[0], PURPLE),
            target("One Token at a Time", output_frame_from_base_time(157.38), why_cards[1], BLUE),
            target("Keeps Trying to Answer", output_frame_from_base_time(167.48), why_cards[2], TEAL),
            target("Probable Does Not Equal True", output_frame_from_base_time(180.84), why_cards[3], AMBER, full_view=True),
        ],
        lead_camera=True,
    )

    builder.board(
        "real-text",
        REAL_TEXT,
        *spans["real-text"],
        "compact",
        [],
        banner_at=output_frame_from_base_time(231.64) / FPS,
        push=False,
    )

    check_cards = [
        [70, 175, 500, 718],
        [585, 175, 1015, 718],
        [1100, 175, 1530, 718],
    ]
    builder.board(
        "check",
        CHECK,
        *spans["check"],
        "dense",
        [
            target("Notice the Claim", output_frame_from_base_time(286.66), check_cards[0], PURPLE),
            target("Find the Source", output_frame_from_base_time(301.30), check_cards[1], BLUE),
            target("Check the Match", output_frame_from_base_time(324.52), check_cards[2], TEAL),
        ],
        lead_camera=True,
    )


def source_frame_for_output(frame: int) -> int:
    if frame < GRAFT_OUT_START:
        return math.floor(frame * BASE_FPS / FPS)
    if frame < GRAFT_OUT_END:
        return BASE_GRAFT[0]
    return math.floor((frame - DELTA) * BASE_FPS / FPS)


def render(builder: Build, spans: dict[str, tuple[int, int]], total_frames: int, close_start: int) -> dict:
    assert not DEST.exists(), f"{DEST} exists; choose a new version instead of overwriting"
    close_image = builder.close_img
    mask = glyph_mask()
    source = SourceReader(BASE)
    legs = {key: LegReader(OUT / f"leg-{key}.mkv") for key in spans}
    corner = {"clone": 0, "inpaint": 0, "declined": []}
    board_by_frame = []
    for key, (start, end) in spans.items():
        board_by_frame.append((start, end, key))

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

    for frame in range(total_frames):
        if frame >= close_start:
            k = frame - close_start
            q = np.clip((k - CLOSE_PREHOLD) / (CLOSE_PUSH - 1), 0, 1)
            zoom = 1 + 0.2 * q * q * (3 - 2 * q)
            h, w = close_image.shape[:2]
            crop_w = w / zoom
            crop_h = crop_w * 9 / 16
            image = cv2.warpAffine(
                close_image,
                np.float32(
                    [
                        [crop_w / W, 0, (w - crop_w) / 2],
                        [0, crop_h / H, (h - crop_h) / 2],
                    ]
                ),
                (W, H),
                flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP,
            )
        else:
            board = next((key for start, end, key in board_by_frame if start <= frame < end), None)
            if board is not None:
                image = legs[board].at(frame - spans[board][0])
            else:
                source_frame = source_frame_for_output(frame)
                image = source.at(source_frame)
                image, method = clean_frame(image, mask)
                if method in ("clone", "inpaint"):
                    corner[method] += 1
                else:
                    corner["declined"].append({"output_frame": frame, "source_frame": source_frame})
        process.stdin.write(image.tobytes())

    process.stdin.close()
    assert process.wait() == 0
    return corner


def frame_count(path: Path) -> tuple[int, float, int, int]:
    cap = cv2.VideoCapture(str(path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return count, fps, width, height


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    protected = [BASE, DONOR, LESSON, EXAMPLE, WHY, REAL_TEXT, CHECK, CLOSE]
    protected_hashes = {str(path): sha(path) for path in protected}
    expected_base = frame_count(BASE)
    expected_donor = frame_count(DONOR)
    assert expected_base == (8180, 24.0, 1280, 720), expected_base
    assert expected_donor == (7018, 30.0, 1280, 720), expected_donor

    spans = {
        "example": (
            base_frame_to_output(BASE_CUTS["intro_to_question"]),
            base_frame_to_output(BASE_CUTS["example_to_definition"]),
        ),
        "why": (
            base_frame_to_output(BASE_CUTS["definition_to_why"]),
            base_frame_to_output(BASE_CUTS["why_to_pizza"]),
        ),
        "real-text": (
            base_frame_to_output(BASE_CUTS["pizza_quote_to_context"]),
            base_frame_to_output(BASE_CUTS["context_to_takeaway"]),
        ),
        "check": (
            base_frame_to_output(BASE_CUTS["takeaway_to_check"]),
            base_frame_to_output(BASE_CUTS["check_to_close"]),
        ),
    }
    close_start = base_frame_to_output(BASE_CUTS["check_to_close"])
    close_audio_end = base_frame_to_output(BASE_CUTS["close_to_engine_outro"])
    total_frames = close_audio_end + 120

    audio_manifest = prepare_audio(total_frames)
    builder = Build(ROOT, BASE, OUT, DEST, protected=protected[1:])
    build_boards(builder, spans)
    builder.render_legs()
    for key in spans:
        builder.state_sheet(key)
    builder.make_close("hallucination")

    manifest = {
        "output": str(DEST),
        "base": str(BASE),
        "donor": str(DONOR),
        "scope": "Full production review candidate; live video and lesson unchanged",
        "approved_plan": "Hallucination-2 narration spine; one Hallucination-1 pizza-beat graft; current boards; no added teaching pauses; canonical close",
        "fps": FPS,
        "total_frames": total_frames,
        "duration": total_frames / FPS,
        "source_properties": {
            "base": {"frames": expected_base[0], "fps": expected_base[1]},
            "donor": {"frames": expected_donor[0], "fps": expected_donor[1]},
        },
        "source_visual_cuts_24fps": BASE_CUTS,
        "graft": {
            "target_base_frames_24fps": list(BASE_GRAFT),
            "target_base_seconds": [float(base_seconds(v)) for v in BASE_GRAFT],
            "donor_frames_30fps": list(DONOR_GRAFT),
            "donor_seconds": [float(donor_seconds(v)) for v in DONOR_GRAFT],
            "output_frames": [GRAFT_OUT_START, GRAFT_OUT_END],
            "words": "When users searched for a way to keep cheese from sliding off a pizza ... Mix about one-eighth of a cup of non-toxic glue into the tomato sauce.",
            "visual": "Hallucination-2 static pizza scene held under the longer donor beat",
        },
        "audio": audio_manifest,
        "boards": builder.boards,
        "board_output_spans": {key: list(value) for key, value in spans.items()},
        "board_density": {
            "Nothing Sounds Wrong": "compact",
            "Why Hallucinations Happen": "dense",
            "Real Text. Wrong Meaning.": "compact",
            "Check the Claim": "dense",
        },
        "close": {
            "start_frame": close_start,
            "prehold_frames": CLOSE_PREHOLD,
            "push_frames": CLOSE_PUSH,
            "zoom_endpoint": 1.2,
            "settled_frames": total_frames - close_start - CLOSE_PREHOLD - CLOSE_PUSH,
            "asset": str(CLOSE.relative_to(ROOT)),
        },
        "engine_outro_removed": {
            "source_frames_24fps": [BASE_CUTS["close_to_engine_outro"], expected_base[0]],
        },
        "approved_added_pauses": [],
        "notebook_interleaves": [
            [0, spans["example"][0]],
            [spans["example"][1], spans["why"][0]],
            [spans["why"][1], spans["real-text"][0]],
            [spans["real-text"][1], spans["check"][0]],
        ],
        "longest_unbroken_board_run_frames": max(end - start for start, end in spans.values()),
        "boundaries": sorted(
            [
                {"frame": GRAFT_OUT_START, "label": "pizza-graft-in"},
                {"frame": GRAFT_OUT_END, "label": "pizza-graft-out"},
                {"frame": close_start, "label": "standard-close-in"},
                *[
                    {"frame": point, "label": f"{key}-{'in' if point == start else 'out'}"}
                    for key, (start, end) in spans.items()
                    for point in (start, end)
                ],
            ],
            key=lambda row: row["frame"],
        ),
        "protected_hashes": protected_hashes,
    }
    (OUT / "edit-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("Prepared", total_frames, f"{total_frames / FPS:.3f}s", spans, "close", close_start, flush=True)
    if args.prepare_only:
        return

    corner = render(builder, spans, total_frames, close_start)
    actual = frame_count(DEST)
    assert actual == (total_frames, 30.0, 1280, 720), actual
    current = json.loads((OUT / "edit-manifest.json").read_text())
    current["corner_mark"] = corner
    current["render_sha256"] = sha(DEST)
    current["protected_files_unchanged"] = {
        path: sha(Path(path)) == digest for path, digest in protected_hashes.items()
    }
    assert all(current["protected_files_unchanged"].values())
    (OUT / "edit-manifest.json").write_text(json.dumps(current, indent=2) + "\n")
    print(DEST, actual, flush=True)


if __name__ == "__main__":
    main()

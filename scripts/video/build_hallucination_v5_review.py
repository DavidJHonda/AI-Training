#!/usr/bin/env python3
"""Build the approved Hallucination live-best-of review candidate (2026-09-18).

The shipped video is the picture and narration spine.  Three approved, complete
beats repair its teaching:

1. Hallucination-2 replaces the claim that every impressive detail was fake.
2. Hallucination-1 supplies the missing "not finding is not disproving" caution.
3. Hallucination-2 supplies the exact two-line close.

Every graft is under a course board.  Current course JPGs replace all shipped
board legs, retained Notebook frames have the engine corner mark cleaned, and
the canonical standard close is the literal final frame.  Review only: neither
the live video nor lesson materials are changed.
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
import build_your_choices_reroll_review as common  # noqa: E402
import build_avoid_illustration_sync as sync  # noqa: E402
from build_work_changes_hybrid import render_leg  # noqa: E402
from gemini_mark import clean_frame, glyph_mask  # noqa: E402
from make_close_board import close_board_copy  # noqa: E402


ROOT = Path(__file__).resolve().parents[2]
LIVE = ROOT / "course-assets/hallucination/hallucination.mp4"
DONOR1 = ROOT / "Prompts/halllucination-1.mp4"
DONOR2 = ROOT / "Prompts/hallucination-2.mp4"
DEST = ROOT / "Prompts/hallucination-v8.mp4"
OUT = ROOT / "video-audit/hallucination-live-best-of-2026-09-19-v8"

ASSETS = ROOT / "course-assets/hallucination"
EXAMPLE = ASSETS / "hallucination-example.jpg"
WHY = ASSETS / "hallucination-why-ai-makes-things-up.jpg"
REAL_TEXT = ASSETS / "hallucination-glue-on-pizza.jpg"
CHECK = ASSETS / "hallucination-check-claim.jpg"
CLOSE = ASSETS / "hallucination-close.jpg"
LESSON = ROOT / "lessons/hallucination.md"

LIVE_SHA = "0198c0dc16dc880fe4344f31cfd8f0037f95a82d5536c56bb40e29346d98ae88"
DONOR1_SHA = "eede6a44bd7c336397a3387b0b4a4d4e203a1e5c560ce3ab1e31df464791ce3b"
DONOR2_SHA = "147ede28bf9a8403bdc005e5d0e1f70df57a0479f2d273dd7df6021794b5ab9d"

FPS = 30
SR = 48_000
SPF = SR // FPS
W, H = 1280, 720
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

# Boundaries are 30 fps frames selected inside the transcript's surrounding
# silence windows.  They include room tone at both ends of every donor beat.
BASE_GRAFT1 = (1190, 1304)      # 39.667-43.467: wrong "every detail" sentence
DONOR2_GRAFT1 = (1060, 1233)    # 35.333-41.100: real fact + invented detail
BASE_INSERT2 = 5779             # 192.633: gap before "If you do find..."
DONOR1_GRAFT2 = (5958, 6189)    # 198.600-206.300: not finding != disproving
BASE_CLOSE_START = 6612         # 220.400: shipped close-board onset
DONOR2_CLOSE = (6466, 6670)     # 215.533-222.333: exact two-line close

DELTA1 = (DONOR2_GRAFT1[1] - DONOR2_GRAFT1[0]) - (BASE_GRAFT1[1] - BASE_GRAFT1[0])
DELTA2 = DONOR1_GRAFT2[1] - DONOR1_GRAFT2[0]
CLOSE_START = BASE_CLOSE_START + DELTA1 + DELTA2
CLOSE_FRAMES = 48 + 150 + 120
TOTAL_FRAMES = CLOSE_START + CLOSE_FRAMES

# Replace long stretches of the opening example board with teaching visuals
# already present in the two approved alternate edits. Audio always remains the
# repaired v7 program; only picture is borrowed here.
OPENING_OVERLAYS = (
    {
        "label": "laptop-and-prompt",
        "output": (0, 383),
        "source": DONOR2,
        "source_frames": (0, 383),
        "mapping": "exact",
    },
    {
        "label": "stanford-and-authority",
        "output": (653, 1027),
        "source": DONOR1,
        "source_frames": (1487, 1855),
        "mapping": "hold-last-frame",
    },
    {
        "label": "response-anatomy",
        "output": (1027, 1370),
        "source": DONOR1,
        "source_frames": (1144, 1487),
        "mapping": "exact",
    },
    {
        "label": "hallucination-title",
        "output": (1370, 1616),
        "source": DONOR2,
        "source_frames": (1243, 1445),
        "mapping": "stretch",
    },
)

P, B, T, A, VP = "#4f2fc4", "#1652f0", "#0e8f86", "#a9760c", "#6e51ff"
CHECK_RECTS = [(70, 175, 500, 718), (585, 175, 1015, 718), (1100, 175, 1530, 718)]


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


def map_base_frame(frame: int) -> int:
    """Map a live-video frame to the repaired output timeline."""
    if frame < BASE_GRAFT1[0]:
        return frame
    if frame < BASE_GRAFT1[1]:
        return BASE_GRAFT1[0]
    mapped = frame + DELTA1
    if frame >= BASE_INSERT2:
        mapped += DELTA2
    return mapped


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


def decode_audio(source: Path, dest: Path) -> None:
    if dest.exists():
        return
    subprocess.run(
        [
            FFMPEG, "-y", "-v", "error", "-i", str(source), "-vn",
            "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(dest),
        ],
        check=True,
    )


def rms(samples: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(samples))))


def at(samples: np.ndarray, start: float, end: float) -> np.ndarray:
    return samples[round(start * SR):round(end * SR)]


def loop_tone(seed: np.ndarray, frames: int) -> np.ndarray:
    seed = seed.copy()
    seed -= seed.mean()
    return np.resize(np.r_[seed, seed[::-1]], frames)


def fade_to_tone(samples: np.ndarray, tone: np.ndarray, *, fade_in: bool, fade_out: bool) -> np.ndarray:
    out = samples.copy()
    n = min(240, len(out), len(tone))
    ramp = np.linspace(0.0, 1.0, n)
    if fade_in:
        out[:n] = tone[:n] * (1.0 - ramp) + out[:n] * ramp
    if fade_out:
        out[-n:] = out[-n:] * (1.0 - ramp) + tone[-n:] * ramp
    return out


def bridge(left: np.ndarray, right: np.ndarray, seed: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Meet two clips sample-continuously through a 5 ms room-tone fade."""
    n = min(240, len(left), len(right))
    target = float(np.mean(seed))
    ramp = np.linspace(0.0, 1.0, n)
    left = left.copy()
    right = right.copy()
    left[-n:] = left[-n:] * (1.0 - ramp) + target * ramp
    right[:n] = target * (1.0 - ramp) + right[:n] * ramp
    return left, right


def prepare_audio() -> dict:
    live_wav = OUT / "live.wav"
    donor1_wav = OUT / "donor1.wav"
    donor2_wav = OUT / "donor2.wav"
    decode_audio(LIVE, live_wav)
    decode_audio(DONOR1, donor1_wav)
    decode_audio(DONOR2, donor2_wav)
    live = read_wav(live_wav)
    donor1 = read_wav(donor1_wav)
    donor2 = read_wav(donor2_wav)

    g1_gain = rms(at(live, 39.94, 43.14)) / rms(at(donor2, 35.62, 40.78))
    g2_gain = rms(at(live, 185.12, 192.28)) / rms(at(donor1, 198.98, 205.90))
    close_gain = rms(at(live, 220.56, 233.48)) / rms(at(donor2, 215.88, 221.92))

    s = lambda frame: frame * SPF
    before1 = live[:s(BASE_GRAFT1[0])]
    graft1 = donor2[s(DONOR2_GRAFT1[0]):s(DONOR2_GRAFT1[1])] * g1_gain
    middle1 = live[s(BASE_GRAFT1[1]):s(BASE_INSERT2)]
    graft2 = donor1[s(DONOR1_GRAFT2[0]):s(DONOR1_GRAFT2[1])] * g2_gain
    middle2 = live[s(BASE_INSERT2):s(BASE_CLOSE_START)]
    close = donor2[s(DONOR2_CLOSE[0]):s(DONOR2_CLOSE[1])] * close_gain

    before1, graft1 = bridge(before1, graft1, at(live, 39.55, 39.65))
    graft1, middle1 = bridge(graft1, middle1, at(live, 43.35, 43.45))
    middle1, graft2 = bridge(middle1, graft2, at(live, 192.48, 192.58))
    graft2, middle2 = bridge(graft2, middle2, at(live, 192.68, 192.78))
    middle2, close = bridge(middle2, close, at(live, 220.15, 220.25))
    target_samples = TOTAL_FRAMES * SPF
    used = sum(map(len, (before1, graft1, middle1, graft2, middle2, close)))
    assert used < target_samples
    # Use the genuinely quiet post-word bed, not the final /s/ of "source."
    # The latter becomes a perceptible buzz when looped through the settled hold.
    tail_seed = at(donor2, 222.16, 222.22)
    tail = loop_tone(tail_seed, target_samples - used)
    close, tail = bridge(close, tail, tail_seed)

    edited = np.concatenate([before1, graft1, middle1, graft2, middle2, close, tail])
    assert len(edited) == target_samples
    write_wav(OUT / "edited.wav", edited)

    graft1_out = (BASE_GRAFT1[0], BASE_GRAFT1[0] + len(graft1) // SPF)
    graft2_out_start = map_base_frame(BASE_INSERT2) - DELTA2
    graft2_out = (graft2_out_start, graft2_out_start + len(graft2) // SPF)
    close_out = (CLOSE_START, CLOSE_START + len(close) // SPF)
    return {
        "sample_rate": SR,
        "crossfade_to_matched_tone_ms": 5,
        "gains_db": {
            "real-fact-graft": 20 * math.log10(g1_gain),
            "unverified-caution-graft": 20 * math.log10(g2_gain),
            "exact-close-graft": 20 * math.log10(close_gain),
        },
        "grafts": [
            {
                "label": "real-fact-graft",
                "base_frames": list(BASE_GRAFT1),
                "base_seconds": [v / FPS for v in BASE_GRAFT1],
                "donor": str(DONOR2),
                "donor_frames": list(DONOR2_GRAFT1),
                "donor_seconds": [v / FPS for v in DONOR2_GRAFT1],
                "output_frames": list(graft1_out),
                "words": "So it attaches an invented detail to a fact that is real, making the error much harder to spot.",
            },
            {
                "label": "unverified-caution-graft",
                "base_insert_frame": BASE_INSERT2,
                "base_insert_seconds": BASE_INSERT2 / FPS,
                "donor": str(DONOR1),
                "donor_frames": list(DONOR1_GRAFT2),
                "donor_seconds": [v / FPS for v in DONOR1_GRAFT2],
                "output_frames": list(graft2_out),
                "words": "Failing to find a source doesn't automatically prove a claim false, but it means the claim remains unverified and shouldn't be trusted.",
            },
            {
                "label": "exact-close-graft",
                "base_frames": [BASE_CLOSE_START, 7018],
                "base_seconds": [BASE_CLOSE_START / FPS, 7018 / FPS],
                "donor": str(DONOR2),
                "donor_frames": list(DONOR2_CLOSE),
                "donor_seconds": [v / FPS for v in DONOR2_CLOSE],
                "output_frames": list(close_out),
                "words": "Hallucinations sound like every other AI answer. When something doesn't add up, trace the claim to its source.",
            },
        ],
        "settled_close_tone_frames": len(tail) // SPF,
    }


def build_legs() -> tuple[list[tuple[int, int, Path]], list[dict]]:
    common.CUTS = ()
    common.output_frame = lambda frame: frame
    work = OUT / "work"
    work.mkdir(exist_ok=True)
    renders: list[tuple[int, int, Path]] = []
    spans: list[dict] = []

    def add(name: str, asset: Path, points: tuple[int, ...], states: tuple) -> None:
        leg = common.make_leg(name, asset, points, states)
        path = work / f"{name}.mkv"
        print("Rendering", name, points[0], points[-1], flush=True)
        render_leg(leg, path)
        assert common.frame_count(path) == leg.frames == points[-1] - points[0]
        cursor = points[0]
        manifest_states = []
        for state in leg.states:
            manifest_states.append(
                {
                    "label": state.label,
                    "start": cursor,
                    "end": cursor + state.frames,
                    "rect": state.ring,
                    "color": state.color,
                    "camera": state.camera,
                    "move": state.move_frames,
                }
            )
            cursor += state.frames
        renders.append((points[0], points[-1], path))
        spans.append(
            {
                "key": name,
                "start": points[0],
                "end": points[-1],
                "asset": str(asset.relative_to(ROOT)),
                "states": manifest_states,
            }
        )

    add(
        "example",
        EXAMPLE,
        (0, 30, 273, 1028, map_base_frame(1374), map_base_frame(1908)),
        (
            ("full", None, VP, None, 0),
            ("your-full-prompt", (605, 203, 1520, 338), VP, None, 0),
            ("full-ai-bubble", (80, 401, 989, 618), VP, (550, 490, 1180), 24),
            ("full-takeaway", (40, 697, 1560, 786), VP, None, 24),
            ("example-in-context", None, VP, None, 0),
        ),
    )
    add(
        "why",
        WHY,
        tuple(map_base_frame(v) for v in (1908, 2079, 2325, 2565, 2838, 3208)),
        (
            ("full", None, VP, None, 0),
            ("learns-from-text", (56, 164, 362, 794), P, (209, 479, 1200), 24),
            ("one-token", (452, 164, 756, 794), B, (604, 479, 1200), 24),
            ("keeps-answering", (844, 164, 1150, 794), T, (997, 479, 1200), 24),
            ("probable-not-true", (1234, 164, 1548, 794), A, (1391, 479, 1200), 24),
        ),
    )

    rt_start, rt_takeaway, rt_end = (map_base_frame(v) for v in (3724, 3847, 3974))
    rt = {
        "asset": str(REAL_TEXT),
        "start": rt_start,
        "end": rt_end,
        "states": [
            sync.state(rt_start, "full-illustration"),
            sync.state(rt_takeaway, "full-takeaway", sync.gold_bounds(REAL_TEXT)),
        ],
        "push": 0,
    }
    rt_path = work / "real-text.mkv"
    if rt_path.exists():
        rt_path.unlink()
    print("Rendering real-text", rt_start, rt_end, flush=True)
    sync.render_leg(rt, rt_path, OUT)
    assert common.frame_count(rt_path) == rt_end - rt_start
    renders.append((rt_start, rt_end, rt_path))
    spans.append(
        {
            "key": "real-text",
            "start": rt_start,
            "end": rt_end,
            "asset": str(REAL_TEXT.relative_to(ROOT)),
            "states": rt["states"],
        }
    )

    add(
        "check-claim",
        CHECK,
        tuple(map_base_frame(v) for v in (4600, 4714, 5252, 5784, 6302, 6612)),
        (
            ("full", None, VP, None, 0),
            ("notice-the-claim", CHECK_RECTS[0], P, (285, 446.5, 1050), 24),
            ("find-the-source", CHECK_RECTS[1], B, (800, 446.5, 1050), 24),
            ("check-the-match", CHECK_RECTS[2], T, (1315, 446.5, 1050), 24),
            ("three-step-recap", None, VP, None, 24),
        ),
    )

    close_png = OUT / "close.png"
    if not close_png.exists():
        subprocess.run(
            [sys.executable, str(ROOT / "scripts/video/make_close_board.py"), "--lesson", "hallucination", "--out", str(close_png)],
            check=True,
            stdout=subprocess.DEVNULL,
        )
    close_1600 = work / "close-1600.png"
    cv2.imwrite(str(close_1600), cv2.resize(cv2.imread(str(close_png)), (1600, 900), interpolation=cv2.INTER_AREA))
    common.BOARDS["close"] = close_1600
    close_path = work / "close.mkv"
    common.render_close(close_path, CLOSE_FRAMES)
    assert common.frame_count(close_path) == CLOSE_FRAMES
    renders.append((CLOSE_START, TOTAL_FRAMES, close_path))
    spans.append(
        {
            "key": "close",
            "start": CLOSE_START,
            "end": TOTAL_FRAMES,
            "asset": str(CLOSE.relative_to(ROOT)),
            "states": [],
        }
    )
    renders.sort(key=lambda row: row[0])
    return renders, spans


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


def render(renders: list[tuple[int, int, Path]]) -> dict:
    assert not DEST.exists(), f"{DEST} exists; choose a new version instead of overwriting"
    readers = {(start, end): Reader(path) for start, end, path in renders}
    overlay_readers = {row["label"]: Reader(row["source"]) for row in OPENING_OVERLAYS}
    live = Reader(LIVE)
    mask = glyph_mask()
    corner = {"clone": 0, "inpaint": 0, "declined": []}
    process = subprocess.Popen(
        [
            FFMPEG, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24",
            "-s", f"{W}x{H}", "-r", str(FPS), "-i", "pipe:0",
            "-i", str(OUT / "edited.wav"), "-map", "0:v", "-map", "1:a",
            "-c:v", "libx264", "-crf", "18", "-preset", "medium",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", str(DEST),
        ],
        stdin=subprocess.PIPE,
    )
    for frame in range(TOTAL_FRAMES):
        overlay = next((row for row in OPENING_OVERLAYS if row["output"][0] <= frame < row["output"][1]), None)
        leg = next(((start, end) for start, end, _ in renders if start <= frame < end), None)
        if overlay:
            out_start, out_end = overlay["output"]
            src_start, src_end = overlay["source_frames"]
            offset = frame - out_start
            if overlay["mapping"] == "stretch":
                output_length = out_end - out_start
                source_length = src_end - src_start
                source_frame = src_start + round(offset * (source_length - 1) / (output_length - 1))
            else:
                source_frame = min(src_start + offset, src_end - 1)
            image = overlay_readers[overlay["label"]].at(source_frame)
            image, method = clean_frame(image, mask)
            if method in ("clone", "inpaint"):
                corner[method] += 1
            else:
                corner["declined"].append({"output_frame": frame, "source_frame": source_frame, "overlay": overlay["label"]})
        elif leg:
            image = readers[leg].at(frame - leg[0])
        else:
            # Both retained Notebook spans occur after graft 1 and before the
            # later insertion, so their source mapping is the same fixed shift.
            source_frame = frame - DELTA1
            image = live.at(source_frame)
            image, method = clean_frame(image, mask)
            if method in ("clone", "inpaint"):
                corner[method] += 1
            else:
                corner["declined"].append({"output_frame": frame, "source_frame": source_frame})
        process.stdin.write(image.tobytes())
    process.stdin.close()
    assert process.wait() == 0
    return corner


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "states").mkdir(exist_ok=True)

    assert sha(LIVE) == LIVE_SHA
    assert sha(DONOR1) == DONOR1_SHA
    assert sha(DONOR2) == DONOR2_SHA
    assert media_properties(LIVE) == (7018, 30.0, 1280, 720)
    assert media_properties(DONOR1) == (6977, 30.0, 1280, 720)
    assert media_properties(DONOR2) == (6761, 30.0, 1280, 720)
    assert close_board_copy("hallucination") == (
        "Hallucinations sound like every other AI answer.",
        "When something doesn’t add up, trace the claim to its source.",
    )

    protected = [LIVE, DONOR1, DONOR2, LESSON, EXAMPLE, WHY, REAL_TEXT, CHECK, CLOSE]
    protected_hashes = {str(path): sha(path) for path in protected}
    audio = prepare_audio()
    renders, spans = build_legs()
    expected_visual_spans = [
        (0, map_base_frame(1908)),
        (map_base_frame(1908), map_base_frame(3208)),
        (map_base_frame(3724), map_base_frame(3974)),
        (map_base_frame(4600), map_base_frame(6612)),
        (CLOSE_START, TOTAL_FRAMES),
    ]
    assert [(a, b) for a, b, _ in renders] == expected_visual_spans

    boundaries = [
        {"frame": 383, "label": "laptop-prompt-to-example"},
        {"frame": 653, "label": "example-to-stanford-authority"},
        {"frame": 1027, "label": "authority-to-response-anatomy"},
        {"frame": 1370, "label": "response-anatomy-to-hallucination-title"},
        {"frame": 1616, "label": "hallucination-title-to-example"},
        {"frame": map_base_frame(1908), "label": "example-to-why"},
        {"frame": map_base_frame(3208), "label": "why-to-pizza-drawing"},
        {"frame": map_base_frame(3724), "label": "real-text-in"},
        {"frame": map_base_frame(3974), "label": "real-text-out"},
        {"frame": map_base_frame(4600), "label": "check-claim-in"},
        {"frame": CLOSE_START, "label": "canonical-close-in"},
    ]
    manifest = {
        "output": str(DEST),
        "scope": "Approved full production review candidate; live video and lesson unchanged",
        "approved_plan": "Live picture/narration spine; three complete board-covered narration grafts; current boards; retained existing subject-change pause; canonical close",
        "opening_overlays": [
            {
                "label": row["label"],
                "output_frames": list(row["output"]),
                "output_seconds": [value / FPS for value in row["output"]],
                "source": str(row["source"]),
                "source_frames": list(row["source_frames"]),
                "source_seconds": [value / FPS for value in row["source_frames"]],
                "mapping": row["mapping"],
            }
            for row in OPENING_OVERLAYS
        ],
        "sources": {
            "live": {"path": str(LIVE), "sha256": LIVE_SHA},
            "hallucination-1": {"path": str(DONOR1), "sha256": DONOR1_SHA},
            "hallucination-2": {"path": str(DONOR2), "sha256": DONOR2_SHA},
        },
        "fps": FPS,
        "total_frames": TOTAL_FRAMES,
        "duration": TOTAL_FRAMES / FPS,
        "audio": audio,
        "board_spans": spans,
        "board_density": {
            "Nothing Sounds Wrong": "dense AI-chat treatment retained from live",
            "Why Hallucinations Happen": "dense",
            "Real Text. Wrong Meaning.": "compact",
            "Check the Claim": "dense",
        },
        "close": {
            "start_frame": CLOSE_START,
            "frames": CLOSE_FRAMES,
            "prehold_frames": 48,
            "push_frames": 150,
            "settled_frames": 120,
            "asset": str(CLOSE.relative_to(ROOT)),
        },
        "approved_added_pauses": [],
        "retained_existing_pause": "Approximately one second before the real-source-misinterpretation section",
        "notebook_spans": [
            [map_base_frame(3208), map_base_frame(3724)],
            [map_base_frame(3974), map_base_frame(4600)],
        ],
        "longest_unbroken_board_run_frames": max(row["end"] - row["start"] for row in spans),
        "boundaries": boundaries,
        "protected_hashes": protected_hashes,
    }
    (OUT / "edit-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print("Prepared", TOTAL_FRAMES, f"{TOTAL_FRAMES / FPS:.3f}s", expected_visual_spans, flush=True)
    if args.prepare_only:
        return

    corner = render(renders)
    assert media_properties(DEST) == (TOTAL_FRAMES, 30.0, 1280, 720)
    current = json.loads((OUT / "edit-manifest.json").read_text())
    current["corner_mark"] = corner
    current["render_sha256"] = sha(DEST)
    current["protected_files_unchanged"] = {
        path: sha(Path(path)) == digest for path, digest in protected_hashes.items()
    }
    assert all(current["protected_files_unchanged"].values())
    (OUT / "edit-manifest.json").write_text(json.dumps(current, indent=2) + "\n")
    print(DEST, media_properties(DEST), flush=True)


if __name__ == "__main__":
    main()

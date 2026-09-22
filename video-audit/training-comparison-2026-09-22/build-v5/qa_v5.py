#!/usr/bin/env python3
"""QA for the Training v5 review candidate (Edit Spec 10). Artifacts land next to this file."""
from pathlib import Path
import json, subprocess, re, sys
import cv2, numpy as np, imageio_ffmpeg
ROOT = Path("/Users/davidobrien/Developer/AI-Training"); OUT = ROOT / "video-audit/training-comparison-2026-09-22/build-v5"
DEST = ROOT / "Prompts/training-v5.mp4"; FF = imageio_ffmpeg.get_ffmpeg_exe(); PY = ROOT / ".video-venv/bin/python"
m = json.load(open(OUT / "edit-manifest.json")); rows = m["timeline"]; total = m["total_frames"]; FPS = 30
report = {}

# 1. decoded frame count
cap = cv2.VideoCapture(str(DEST)); n = 0; first = None; kept = []
src_rows = [r for r in rows if r["kind"] == "source" and r.get("visual") == "source" and "graft_audio" not in r]
while True:
    ok, im = cap.read()
    if not ok: break
    if n == 0: first = im.copy(); cv2.imwrite(str(OUT / "output-frame-0000.jpg"), im, [cv2.IMWRITE_JPEG_QUALITY, 92])
    if any(r["start_frame"] <= n < r["end_frame"] for r in src_rows) and n % 30 == 0:
        c = cv2.resize(im, (320, 180)); cv2.putText(c, f"o{n} {n/30:.1f}s", (6, 20), cv2.FONT_HERSHEY_SIMPLEX, .55, (0, 0, 255), 2); kept.append(c)
    n += 1
report["decoded_frames"] = n; report["plan_frames"] = total
while len(kept) % 8: kept.append(np.zeros_like(kept[0]))
cv2.imwrite(str(OUT / "kept-notebook-spans.jpg"), cv2.vconcat([cv2.hconcat(kept[k:k + 8]) for k in range(0, len(kept), 8)]), [cv2.IMWRITE_JPEG_QUALITY, 85])
report["kept_notebook_sampled_frames"] = len([k for k in kept if k.any()])

# 2. transition guard on every row boundary
bounds = [f"{r['start_frame']}:{re.sub(r'[^A-Za-z0-9]+', '-', r['label'])[:40]}" for r in rows[1:]]
gd = OUT / "guard"; gd.mkdir(exist_ok=True)
args = [str(PY), str(ROOT / "scripts/video/transition_guard.py"), str(DEST), "--outdir", str(gd)]
for b in bounds: args += ["--boundary", b]
g = subprocess.run(args, capture_output=True, text=True); (OUT / "guard-stdout.txt").write_text(g.stdout + "\n--stderr--\n" + g.stderr)
report["guard_returncode"] = g.returncode; report["guard_tail"] = g.stdout[-1500:]

# 3. silencedetect on the finished file
s = subprocess.run([FF, "-hide_banner", "-i", str(DEST), "-af", "silencedetect=n=-35dB:d=0.3", "-f", "null", "-"], capture_output=True, text=True).stderr
sil = re.findall(r"silence_start: ([\d.]+)\n.*?silence_end: ([\d.]+) \| silence_duration: ([\d.]+)", s, re.S)
report["silences_ge_0p9s"] = [(float(a), float(b), float(c)) for a, b, c in sil if float(c) >= 0.9]
report["silences_all"] = [(float(a), float(b), float(c)) for a, b, c in sil]

# 4. volumedetect windows across each graft join and the close graft
def vol(t0, t1):
    o = subprocess.run([FF, "-hide_banner", "-nostdin", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", str(DEST), "-vn", "-af", "volumedetect", "-f", "null", "-"], capture_output=True, text=True).stderr
    mean = re.search(r"mean_volume: ([-\d.]+) dB", o); mx = re.search(r"max_volume: ([-\d.]+) dB", o)
    if not mean: return dict(window=[round(t0, 2), round(t1, 2)], error=o[-400:])
    return dict(window=[round(t0, 2), round(t1, 2)], mean_db=float(mean.group(1)), max_db=float(mx.group(1)))
gd_row = next(r for r in rows if "graft d" in r["label"]); gf_row = next(r for r in rows if "graft f" in r["label"])
d0, d1 = gd_row["start_frame"] / FPS, gd_row["end_frame"] / FPS; f0, f1 = gf_row["start_frame"] / FPS, gf_row["end_frame"] / FPS
report["levels"] = {
    "d_before(roll1 answer lines)": vol(d0 - 2.6, d0 - 0.4), "d_graft": vol(d0 + 0.2, d1 - 0.3), "d_after(roll1 answer lines)": vol(d1 + 0.3, d1 + 2.6),
    "f_before(roll1 feedback line)": vol(f0 - 5.0, f0 - 0.5), "f_graft": vol(f0 + 0.2, f1 - 0.3), "f_after(roll1 weights lines)": vol(f1 + 0.4, f1 + 5.0),
}

# 5. transcript of the finished file (small.en, word stamps)
from faster_whisper import WhisperModel
wav = OUT / "output-16k.wav"
subprocess.run([FF, "-y", "-v", "error", "-i", str(DEST), "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)], check=True)
model = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, _ = model.transcribe(str(wav), word_timestamps=True)
lines = []; words = []
for sg in segs:
    lines.append(f"[{sg.start:7.2f}-{sg.end:7.2f}] {sg.text.strip()}")
    for w in sg.words: words.append(f"{w.start:7.2f} {w.end:7.2f} {w.word}")
(OUT / "output-transcript-small.txt").write_text("\n".join(lines) + "\n"); (OUT / "output-words-small.txt").write_text("\n".join(words) + "\n")
text = " ".join(l.split("] ", 1)[1] for l in lines)
norm = lambda t: re.sub(r"[^a-z0-9 ]", "", t.lower().replace("—", " ").replace("-", " ")).replace("  ", " ")
T = norm(text)
verbatim = ["AI training follows a similar pattern guess check and adjust", "Repeat with more examples The patterns build", "How do I shoot a basketball",
            "Training adjusts its internal numbers called weights", "Feedback helps improve the answers but AI can still give a wrong answer that sounds right",
            "It can work with new information you give it but your conversation does not change those weights", "AI learns from examples and feedback", "Guess check adjust repeat"]
gone = ["This diagram shows", "Dualness", "This panel shows", "study the ball", "architecture is locked", "builds upon itself", "This graphic summarizes", "deployed for everyday use", "accurately follows instructions"]
present = ["steady the ball", "heavy lifting is done", "packaged up and ready for public use", "When those three phases of training conclude"]
report["verbatim_lines_found"] = {v: norm(v) in T for v in verbatim}
report["cut_phrases_absent"] = {v: norm(v) not in T for v in gone}
report["graft_phrases_present"] = {v: norm(v) in T for v in present}
report["last_words"] = words[-6:]
report["transcript_tail"] = lines[-3:]
report["protected_files_unchanged"] = m.get("protected_files_unchanged"); report["corner_mark"] = {k: (len(v) if isinstance(v, list) else v) for k, v in m["corner_mark"].items()}
(OUT / "qa-report.json").write_text(json.dumps(report, indent=2)); print(json.dumps(report, indent=2))

import sys
from faster_whisper import WhisperModel
src, out = sys.argv[1], sys.argv[2]
m = WhisperModel("medium.en", compute_type="int8")
segs, _ = m.transcribe(src, language="en", beam_size=5, word_timestamps=True, vad_filter=False)
with open(out, "w") as f:
    for s in segs:
        f.write(f"## [{s.start:.2f}-{s.end:.2f}] {s.text.strip()}\n")
        for w in s.words:
            f.write(f"{w.start:7.2f} {w.end:7.2f} {w.probability:.3f} {w.word}\n")

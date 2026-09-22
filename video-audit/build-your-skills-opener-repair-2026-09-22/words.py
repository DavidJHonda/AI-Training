import sys, json
from faster_whisper import WhisperModel
src = sys.argv[1]; out = sys.argv[2]
m = WhisperModel("small.en", device="cpu", compute_type="int8")
segs, info = m.transcribe(src, word_timestamps=True, beam_size=5)
rows = []
for s in segs:
    for w in s.words:
        rows.append(dict(start=round(w.start, 2), end=round(w.end, 2), word=w.word))
json.dump(rows, open(out, "w"), indent=0)
for r in rows: print(f"{r['start']:7.2f} {r['end']:7.2f} {r['word']}")

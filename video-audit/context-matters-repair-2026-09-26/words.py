import sys, json
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2], device="cpu", compute_type="int8")
segs, _ = m.transcribe(sys.argv[1], word_timestamps=True, language="en", beam_size=5)
out = []
for s in segs:
    for w in s.words: out.append([round(w.start,2), round(w.end,2), w.word.strip()])
json.dump(out, open(sys.argv[3], "w"))
print(len(out))

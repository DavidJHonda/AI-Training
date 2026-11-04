import sys, json
from faster_whisper import WhisperModel
m = WhisperModel("medium.en", device="cpu", compute_type="int8")
segs, _ = m.transcribe(sys.argv[1], word_timestamps=True, beam_size=5, language="en")
out = []
for s in segs:
    for w in s.words: out.append([round(w.start,2), round(w.end,2), w.word, round(w.probability,3)])
json.dump(out, open(sys.argv[2], "w"))
print(len(out))

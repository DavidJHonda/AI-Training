import sys
from faster_whisper import WhisperModel
for m in sys.argv[2:]:
    mod = WhisperModel(m, device="cpu", compute_type="int8")
    segs, _ = mod.transcribe(sys.argv[1], word_timestamps=True, language="en", beam_size=5)
    print(m, '|', ' '.join(f"{w.word.strip()}[{w.start:.2f}]" for s in segs for w in s.words))

import json, sys
from faster_whisper import WhisperModel
m = WhisperModel('medium.en', device='cpu', compute_type='int8')
for n in (1, 2):
    src = f'Prompts/build-your-skills-opener-{n}.mp4'
    segs, info = m.transcribe(src, word_timestamps=True, beam_size=5)
    words = []
    with open(f'video-audit/build-your-skills-opener-map-walk-2026-09-26/roll{n}-transcript.txt', 'w') as f:
        for s in segs:
            f.write(f'{s.start:7.2f}-{s.end:7.2f} {s.text.strip()}\n')
            words += [dict(w=w.word, s=round(w.start, 2), e=round(w.end, 2)) for w in s.words]
    json.dump(words, open(f'video-audit/build-your-skills-opener-map-walk-2026-09-26/roll{n}-words.json', 'w'))
    print(n, 'done', info.duration)

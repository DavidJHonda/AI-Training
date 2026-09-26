import json
from faster_whisper import WhisperModel
m = WhisperModel('medium.en', device='cpu', compute_type='int8')
segs, _ = m.transcribe('course-assets/build-your-skills-opener/build-your-skills-opener.mp4', word_timestamps=True, beam_size=5)
w = [dict(w=x.word, s=round(x.start, 2), e=round(x.end, 2)) for s in segs for x in s.words]
json.dump(w, open('video-audit/build-your-skills-opener-map-walk-2026-09-26/live-words.json', 'w'))
print(' '.join(f"{x['s']}{x['w']}" for x in w))

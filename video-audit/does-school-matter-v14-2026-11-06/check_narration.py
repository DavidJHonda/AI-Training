from pathlib import Path
import sys,json,re,subprocess
import numpy as np
sys.path.insert(0,str(Path('scripts/video').resolve()))
import build_does_school_matter_v14 as b
from faster_whisper import WhisperModel
class StableMel(np.ndarray):
 def __matmul__(self,x):return np.einsum('ij,jk->ik',np.asarray(self),x,optimize=False)
m=WhisperModel('base.en',device='cpu',compute_type='int8',cpu_threads=2,local_files_only=True)
m.feature_extractor.mel_filters=m.feature_extractor.mel_filters.view(StableMel)
audio=np.frombuffer(subprocess.check_output([b.FF,'-v','error','-i',str(b.DEST),'-vn','-ac','1','-ar','16000','-f','f32le','pipe:1']),np.float32)
segs,_=m.transcribe(audio,language='en',beam_size=5,word_timestamps=True,vad_filter=False)
rows=[];words=[]
for seg in segs:
 rows.append(dict(start=seg.start,end=seg.end,text=seg.text.strip()))
 words.extend(dict(start=w.start,end=w.end,word=w.word.strip()) for w in seg.words)
(b.OUT/'encoded-transcript.json').write_text(json.dumps(dict(segments=rows,words=words),indent=2)+'\n')
(b.OUT/'encoded-transcript.txt').write_text('\n'.join(f"{x['start']:.2f}-{x['end']:.2f} {x['text']}" for x in rows)+'\n')
normalize=lambda s:re.sub(r'[^a-z0-9 ]','',s.lower())
text=normalize(' '.join(x['text'] for x in rows))
required=[
'Using the math skills you learned in school, you work through the costs and find a more profitable pricing option.',
'Using the writing skills you developed in English class, you make the message clearer and more persuasive.',
'Using the research skills you developed in school, you compare sources and identify a more promising group of customers.',
'The tool may be the same. What you bring to it is yours.',
'You started with similar AI answers. You ended with different work.',
'School is where you get to build what you bring to the work.',
'The opportunity to learn is already in front of you.',
'Choose something you want to get better at. Start there.'
]
checks={line:normalize(line) in text for line in required}
report=dict(required_lines=checks,removed_guarantee_absent='guarantees an average result' not in text,
 problem_solving_retained='solve complex problems' in text,build_and_people_retained='write build and work with other people' in text,
 critical_thinking_retained=all(s in text for s in ['critical thinking','question claims','informed decision']),
 source='Actual encoded candidate; ASR is not listening certification.')
(b.OUT/'narration-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
assert all(checks.values()) and report['removed_guarantee_absent'] and report['problem_solving_retained'] and report['critical_thinking_retained']

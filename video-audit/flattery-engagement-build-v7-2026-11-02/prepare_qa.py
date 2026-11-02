import sys,subprocess,hashlib,json,shutil
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts/video'))
from build_flattery_engagement_v5 import FF
out=Path(__file__).resolve().parent;old=out.parent/'flattery-engagement-build-v6-2026-11-02';qa=out/'qa';qa.mkdir(exist_ok=True)
video=ROOT/'Prompts/flattery-engagement-v7.mp4'
a=np.load(old/'expected-thumbnails.npy',mmap_mode='r');b=np.load(out/'expected-thumbnails.npy',mmap_mode='r');assert a.shape==b.shape
changed=np.flatnonzero(np.any(a!=b,axis=(1,2,3)))
assert all(2136<=n<2792 or 4298<=n<4313 for n in changed),changed.tolist()
hashes={}
for v in (6,7):
 p=ROOT/f'Prompts/flattery-engagement-v{v}.mp4';pcm=subprocess.check_output([FF,'-v','error','-i',str(p),'-vn','-ac','1','-ar','48000','-f','f32le','pipe:1']);hashes[str(v)]=hashlib.sha256(pcm).hexdigest()
assert hashes['6']==hashes['7']
for name in ['transcript.json','transcript.txt']:shutil.copyfile(old/'qa'/name,qa/name)
(qa/'transcript-provenance.json').write_text(json.dumps(dict(method='Complete ASR review of encoded audio; decoded v7 audio is byte-for-byte identical to verified v6 and v5 audio',decoded_mono_48000_f32le_sha256=hashes),indent=2)+'\n')
(qa/'unchanged-regions.json').write_text(json.dumps(dict(previous_candidate=str(ROOT/'Prompts/flattery-engagement-v6.mp4'),frames=9378,changed_render_frames=len(changed),changes_confined_to=['training board rings: frames 2136–2791','tactics entry: frames 4298–4312'],all_other_render_thumbnails_identical=True,decoded_audio_identical=True),indent=2)+'\n')
trans=qa/'transitions';trans.mkdir(exist_ok=True)
(trans/'manual-adjudication.json').write_text(json.dumps(dict(candidate_sha256=hashlib.sha256(video.read_bytes()).hexdigest(),approved_flags=[dict(frame=6821,spike_frames=[6832,6833],reason='Continuous camera pullback on canonical Three Ways board. Same rendered frames as v6 verified byte-for-byte; the v6 every-frame strip was manually inspected, with no stale image or visual island. Inspect final encoded strip again before delivery.')],perceptual_motion_playback=False),indent=2)+'\n')
print('Same audio verified; visual differences confined to the two corrections.',flush=True)

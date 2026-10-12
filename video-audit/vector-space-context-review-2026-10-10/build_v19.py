"""Approved narrow sentence repair; reconstruct v18 pictures from native sources."""
from pathlib import Path
import sys, json, subprocess, functools, math, hashlib
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from editspec_build import Build, Reader, fr, sha, readwav, writewav, rms
from gemini_mark import clean_frame, glyph_mask
from build_vector_space_v11 import opening

AUDIT = Path(__file__).resolve().parent
OUT = ROOT / 'video-audit/vector-space-build-v18-2026-10-08'
DEST = ROOT / 'Prompts/vector-space-v19.mp4'
LIVE = ROOT / 'course-assets/vector-space/vector-space.mp4'
DONOR = ROOT / 'Prompts/vector-space-11.mp4'
S8 = ROOT / 'Prompts/vector-space-8.mp4'
D = ROOT / 'course-assets/vector-space'
FPS, SR, SPF = 30, 48000, 1600
assert not DEST.exists(), 'Never overwrite a review candidate'
assert sha(LIVE) == 'cd895007b43e295a86f7aaea199014cec17e17bd332bf6ceaac08506e87ac805'
assert sha(DONOR) == '87f79e9589ec4d8b56881a272a85306c9b95c3cdd8603fbdde470032aca2aa1f'
protected = [LIVE, DONOR, ROOT/'index.html', D/'vector-space-meaning-map.jpg', D/'vector-space-close.jpg', OUT/'build.py']
protected_hashes = {str(p): sha(p) for p in protected}
old_manifest = json.loads((OUT/'edit-manifest.json').read_text())
b = Build(ROOT, S8, AUDIT, DEST, protected=protected)
b.rows = old_manifest['timeline']
b.close_start = old_manifest['visual_sections']['close'][0]
b.total = old_manifest['total_frames']

# Reuse the exact approved native picture functions. Skip the old audio assembly,
# manifest writes, and render entry point; all new outputs stay in AUDIT.
original_code = (OUT/'build.py').read_text()
native_code = original_code[original_code.index('def mf(t):'):original_code.index('\nboundaries=')]
exec(compile(native_code, str(OUT/'build.py') + ':native-picture-functions', 'exec'), globals())
assert (context_start, board_start, b.total) == (6188, 6540, 7699)
sentence_im = cv2.imread(str(AUDIT/'proposed-sentence-card.png'))
assert sentence_im.shape == (720, 1280, 3)

for source, name in [(LIVE, 'live-decoded.wav'), (DONOR, 'donor11-decoded.wav')]:
    subprocess.run([b.ff, '-v', 'error', '-i', str(source), '-vn', '-ac', '1', '-ar', str(SR), '-c:a', 'pcm_s16le', str(AUDIT/name)], check=True)
live_audio = readwav(AUDIT/'live-decoded.wav')
donor_audio = readwav(AUDIT/'donor11-decoded.wav')

def active_level(a, start, end):
    a = a[round(start*SR):round(end*SR)]
    blocks = a[:len(a)//960*960].reshape(-1, 960)
    levels = np.sqrt(np.mean(blocks**2, axis=1))
    return float(np.median(levels[levels > .03*32768]))

base_level = active_level(live_audio, 210, 228)
donor_level = active_level(donor_audio, 218, 227)
gain_db = 20*math.log10(base_level/donor_level)
cut_in, cut_out, donor_in, donor_out = 6370, 6524, 6623, 6771
delta = (donor_out-donor_in)-(cut_out-cut_in)
assert delta == -6
total = b.total + delta
insert = donor_audio[donor_in*SPF:donor_out*SPF].copy() * 10**(gain_db/20)
# Five-ms ramps entirely inside measured silence, to the adjacent base pause
# samples. No speech is stretched and no pause duration is added.
fade = 240
ramp = np.linspace(0, 1, fade)
insert[:fade] = live_audio[cut_in*SPF:cut_in*SPF+fade]*(1-ramp) + insert[:fade]*ramp
insert[-fade:] = insert[-fade:]*(1-ramp) + live_audio[cut_out*SPF-fade:cut_out*SPF]*ramp
audio = np.concatenate([live_audio[:cut_in*SPF], insert, live_audio[cut_out*SPF:b.total*SPF]])
assert len(audio) == total*SPF
assert np.array_equal(audio[:cut_in*SPF], live_audio[:cut_in*SPF])
resume = cut_in+donor_out-donor_in
assert np.array_equal(audio[resume*SPF:], live_audio[cut_out*SPF:b.total*SPF])
assert np.max(abs(audio)) < 32768
writewav(AUDIT/'v19-assembled.wav', audio)
manifest = dict(
    approval='User: Build uit (2026-10-10), approving the narrow roll-11 sentence plan.',
    output=str(DEST), fps=FPS, total_frames=total, duration=total/FPS,
    base=str(LIVE), donor=str(DONOR), protected_hashes=protected_hashes,
    picture_provenance=str(OUT/'build.py'), native_picture_code_sha256=hashlib.sha256(native_code.encode()).hexdigest(),
    old_audio_frames=[cut_in, cut_out], donor_audio_frames=[donor_in, donor_out],
    output_graft_frames=[cut_in, resume], timing_delta_frames=delta,
    changed_picture_frames=[context_start, board_start+delta],
    audio=dict(gain_db=gain_db, base_active_rms=base_level, donor_active_rms=donor_level,
               sample_rate=SR, seam_ramp_ms=5, peak=float(np.max(abs(audio))/32768),
               unaffected_pcm_identical_before_encoding=True, encoding='One AAC encode after approved audio splice'),
    boundaries=[dict(frame=n, label=label) for n,label in [
        (context_start,'Revised sentence card'),(cut_in,'Donor sentence begins'),
        (resume,'Original narration resumes'),(board_start+delta,'Canonical context board'),
        *[(t[0]+delta,'Preserved context focus') for t in ctx_targets],
        (b.close_start+delta,'Preserved close')]],
    context_board=dict(title='How Context Changes IT’s Position', density='compact',
        frames=[board_start+delta,b.close_start+delta], treatment='Preserved native v18 framing and timed rings'),
    direct_listening=False, full_file_watch=False, installed=False,
)
(AUDIT/'v19-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Rendering', total, 'frames; donor gain', round(gain_db,3), 'dB', flush=True)
p = subprocess.Popen([b.ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
    '-i',str(AUDIT/'v19-assembled.wav'),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','17',
    '-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
for n in range(total):
    old_n = n if n<cut_in else n-delta
    im = frame(old_n)
    p.stdin.write(im.tobytes())
    if n%900 == 0: print('Rendered', n, '/', total, flush=True)
p.stdin.close()
assert p.wait() == 0
assert all(sha(Path(path)) == digest for path,digest in protected_hashes.items())
manifest.update(render_sha256=sha(DEST), protected_files_unchanged=True)
(AUDIT/'v19-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Finished', DEST, flush=True)

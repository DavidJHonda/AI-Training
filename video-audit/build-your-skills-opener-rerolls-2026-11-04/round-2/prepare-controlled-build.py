"""Prepare reusable silent footage and exact narration; no finished candidate yet.

Run from the repository with .video-venv/bin/python. Decode sequentially, retaining
original motion and frame rate. Final edit points depend on the new voice track.
"""
from pathlib import Path
import sys, json, hashlib, subprocess
import cv2
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts/video'))
from editspec_build import Reader, Build
from gemini_mark import clean_frame, glyph_mask
from make_close_board import compose_canonical_for_video
import imageio_ffmpeg

OUT = Path(__file__).parent / 'controlled-build'
FF = imageio_ffmpeg.get_ffmpeg_exe()
SLUG = 'build-your-skills-opener'
MAP = ROOT / f'course-assets/{SLUG}/{SLUG}-section-map.jpg'
CLOSE = ROOT / f'course-assets/{SLUG}/{SLUG}-close.jpg'
SOURCE = ROOT / 'lessons/Opener-Build.md'

# Native frame spans, exclusive end. Sports from roll 6 replace roll 8's
# combined skateboard/basketball scene. No narration from either source is used.
SELECTS = [
    (8, 'changing-tools', 0, 158, 'AI tools will keep changing.'),
    (8, 'reading', 158, 304, 'The skills you build can stay with you.'),
    (8, 'small-bike', 304, 390, 'Think about learning to ride a bike.'),
    (8, 'grown-up-bike', 390, 589, 'You outgrew it and moved on to another bike.'),
    (8, 'cyclist', 899, 985, 'That skill made you a better cyclist'),
    (6, 'skating', 1440, 1605, 'such as skating'),
    (6, 'basketball', 1680, 1830, 'or playing basketball.'),
    (8, 'serious-and-casual', 1208, 1352, 'Whether you became a serious cyclist or just rode for fun'),
    (8, 'park-cyclist', 1352, 1467, 'the skill stayed with you.'),
    (8, 'practicing-balance', 1467, 1592, 'Nobody could give you balance. You had to build it.'),
    (8, 'collaboration', 2135, 2334, 'skills you strengthen through practice'),
    (8, 'ai-practice', 2334, 2447, 'You’ll use AI to practice'),
    (8, 'school-work-life', 2447, 2663, 'at school, at work, and in everyday life.'),
    (8, 'individual-judgment', 2966, 3290, 'Your choices, questions, and judgment matter'),
    (8, 'reflection', 4968, 5122, 'Keep one question in mind through the whole section.'),
    (8, 'same-tool', 5122, 5343, 'Everyone will have the same tool.'),
    (8, 'your-contribution', 5343, 5499, 'What do I bring that it doesn’t?'),
    (8, 'building-skills', 5499, 5746, 'This section is how you build your answer.'),
]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    OUT.mkdir(exist_ok=True)
    clips = OUT / 'silent-selects'; clips.mkdir(exist_ok=True)
    stills = OUT / 'stills'; stills.mkdir(exist_ok=True)
    # Exclude all heading, image and production-metadata lines. Preserve wording.
    paragraphs = [p.strip() for p in SOURCE.read_text().split('\n\n')
                  if p.strip() and not p.lstrip().startswith(('#', '**', '!['))]
    script = '\n\n'.join(paragraphs) + '\n'
    assert len(script.split()) == 256
    (OUT / 'narration-verbatim.txt').write_text(script)
    sources = {n: ROOT / f'Prompts/{SLUG}-{n}.mp4' for n in (6, 8)}
    hashes = {str(p.relative_to(ROOT)): sha(p) for p in [SOURCE, MAP, CLOSE, *sources.values()]}
    mask = glyph_mask(); rows = []
    for roll in (6, 8):
        reader = Reader(sources[roll])
        for _, key, start, end, cue in sorted([r for r in SELECTS if r[0] == roll], key=lambda r:r[2]):
            dest = clips / f'{key}.mp4'
            assert not dest.exists(), f'Prepared clip exists: {dest}'
            proc = subprocess.Popen([FF, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
                '-s', '1280x720', '-r', '30', '-i', 'pipe:0', '-an', '-c:v', 'libx264',
                '-crf', '16', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                str(dest)], stdin=subprocess.PIPE)
            methods = {}; samples = []
            for frame in range(start, end):
                im, method = clean_frame(reader.at(frame), mask)
                methods[str(method)] = methods.get(str(method), 0) + 1
                proc.stdin.write(im.tobytes())
                if frame in (start, (start+end)//2, end-1):
                    samples.append(Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)).resize((480,270)))
            proc.stdin.close(); assert proc.wait() == 0
            sheet = Image.new('RGB', (1440, 305), 'white')
            for i, sample in enumerate(samples): sheet.paste(sample, (i*480,35))
            ImageDraw.Draw(sheet).text((12,10), f'{key} | roll {roll} | frames {start}:{end} | silent source selection', fill='black')
            sheet.save(stills / f'{key}.jpg')
            rows.append(dict(key=key, source=str(sources[roll].relative_to(ROOT)),
                source_frames=[start,end], source_seconds=[start/30,end/30], cue=cue,
                file=str(dest.relative_to(ROOT)), frames=end-start, fps=30,
                audio=False, corner_cleanup=methods, final_timing=None))
            print(f'Prepared {key}: {end-start} frames', flush=True)
        reader.c.release()
    # Standard canonical close canvas, ready for the established hold/push/hold.
    compose_canonical_for_video(CLOSE, OUT / 'canonical-close-canvas.png', '#ffffff')
    from types import SimpleNamespace
    canvas, cw, ch, ox, oy = Build.compose(SimpleNamespace(out=OUT, tall_margin=False), MAP, 'map')
    # Correct current row bounds: second row is now two lines tall.
    targets = [
        dict(cue='One. Judgment and Responsibility.', rect=[100,143,1400,160], color='#4f2fc4'),
        dict(cue='Two. People Skills and Creative Thinking', rect=[100,335,1400,160], color='#1652f0'),
        dict(cue='Three. Curiosity and Your Next Steps', rect=[100,527,1400,120], color='#0e8f86'),
        dict(cue='Build the skills you keep when the tool changes.', rect=[40,702,1520,88], color='#6e51ff'),
    ]
    manifest = dict(status='Prepared visuals; awaiting a complete approved narration recording',
        script='narration-verbatim.txt', script_words=256, source_hashes=hashes,
        narration_file=None, narration_provider=None, voice=None, final_candidate=None,
        selects=sorted(rows, key=lambda r:next(i for i,x in enumerate(SELECTS) if x[1]==r['key'])),
        map=dict(asset=str(MAP.relative_to(ROOT)), canvas=str(canvas.relative_to(ROOT)),
                 canvas_size=[cw,ch], asset_offset=[ox,oy], density='compact',
                 camera='Full view; no pan or zoom', stroke_at_720p=4,
                 intro='This road map shows what we’ll explore in this section. Build Your Skills.',
                 targets=targets, final_timing=None),
        close=dict(asset=str(CLOSE.relative_to(ROOT)), prehold_frames=48,
                   push_frames=150, zoom=1.2, minimum_settled_tail_frames=120),
        source_audio_used=False, direct_listening_performed=False,
        continuous_motion_review_performed=False, installed=False)
    for p,h in hashes.items(): assert sha(ROOT/p)==h
    (OUT/'assembly-plan.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
    print('Ready for narration:', OUT, flush=True)

if __name__ == '__main__': main()

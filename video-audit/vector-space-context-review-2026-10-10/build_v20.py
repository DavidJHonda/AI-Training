"""Picture-only change: use the actual lesson sentence card; copy v19 AAC."""
from pathlib import Path
import json, subprocess
from PIL import Image
HERE=Path(__file__).resolve().parent
card=Image.open(HERE/'lesson-sentence-v20.png').convert('RGB')
width=1160;height=round(card.height*width/card.width)
canvas=Image.new('RGB',(1280,720),'white')
canvas.paste(card.resize((width,height),Image.Resampling.LANCZOS),((1280-width)//2,(720-height)//2))
canvas.save(HERE/'sentence-frame-v20.png')
# Reuse v19's original-source picture setup without running its audio assembly.
setup=(HERE/'build_v19.py').read_text().split('\nfor source, name in ')[0]
setup=setup.replace("'Prompts/vector-space-v19.mp4'", "'Prompts/vector-space-v20.mp4'")
setup=setup.replace("'proposed-sentence-card.png'", "'sentence-frame-v20.png'")
exec(compile(setup,str(HERE/'build_v19.py')+':picture-setup','exec'),globals())
BASE=ROOT/'Prompts/vector-space-v19.mp4'
protected_hashes[str(BASE)]=sha(BASE)
total=7693
manifest=dict(output=str(DEST),base=str(BASE),fps=30,total_frames=total,duration=total/30,
    approval='User: The lesson has the sentence in a different format. Let’s use that instead.',
    scope='Only sentence card replaced; audio copied from v19 and all timing preserved.',
    changed_picture_frames=[6188,6534],card_source='Actual index.html THE SENTENCE element captured with local Plus Jakarta Sans font',
    card_asset=str(AUDIT/'sentence-frame-v20.png'),card_sha256=sha(AUDIT/'sentence-frame-v20.png'),
    audio_mode='AAC stream copy from v19',protected_hashes=protected_hashes,
    boundaries=[dict(frame=6188,label='Lesson sentence card begins'),dict(frame=6534,label='Canonical context board resumes')],
    board_plan=dict(title='THE SENTENCE',camera='Static full card',highlighting='Existing teal CAT and blue IT badges; no added rings',
                    start=6188/30,end=6534/30,breaks=None),installed=False,direct_listening=False)
(AUDIT/'v20-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
p=subprocess.Popen([b.ff,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r','30','-i','pipe:0',
    '-i',str(BASE),'-map','0:v','-map','1:a','-c:v','libx264','-preset','fast','-crf','17','-pix_fmt','yuv420p',
    '-c:a','copy','-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
for n in range(total):
    p.stdin.write(frame(n if n<6370 else n+6).tobytes())
    if n%1500==0:print('Rendered',n,'/',total,flush=True)
p.stdin.close();assert p.wait()==0
assert all(sha(Path(p))==h for p,h in protected_hashes.items())
manifest.update(render_sha256=sha(DEST),protected_files_unchanged=True)
(AUDIT/'v20-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Finished',DEST,flush=True)

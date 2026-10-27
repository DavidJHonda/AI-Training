#!/usr/bin/env python3
"""Build the three approved Fola repairs as an unpublished Opener v9.

The current live edit is the only surviving complete source. Preserve all
unaffected timing/content, render changed boards from canonical assets, and
encode once. Never overwrite the originals or an existing review candidate.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import subprocess
import sys
import types
import wave

import cv2
import imageio_ffmpeg
import numpy as np

from editspec_build import Build, Reader

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / 'video-audit/work-with-ai-opener-fola-repair-2026-09-26'
DONORS = ROOT / 'Prompts/narration-repairs/work-with-ai-opener'
SOURCE = ROOT / 'course-assets/work-with-ai-opener/work-with-ai-opener.mp4'
DEST = ROOT / 'Prompts/work-with-ai-opener-v9.mp4'
SOURCE_SHA = '48c90ec931943f0a98464aafe74d5b99c3ff7967db9d4b0af16bde6f146ac4ed'
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, SR, SPF = 30, 48000, 1600
SCRIPTS = [
    "Don’t just ask. Aim.\nDon’t just copy. Check.\nDon’t just use AI. Work with it.\n"
    "It doesn’t replace your thinking. It multiplies it.\n"
    "You’ve met the tool and seen what it can do. Now it gets practical: how do you actually work with it?",
    'Giving AI the right details helps it give you a better answer.',
    'The result depends on how you use the tool.',
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def read(p):
    with wave.open(str(p)) as w:
        assert (w.getframerate(), w.getnchannels(), w.getsampwidth()) == (SR, 1, 2)
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32768


def write(p, x):
    with wave.open(str(p), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(np.round(np.clip(x, -1, 32767/32768)*32768).astype(np.int16).tobytes())


def gated_db(x):
    bins = np.array([np.sqrt(np.mean(x[i:i+960]**2)) for i in range(0, len(x), 960)])
    active = bins[bins > 10**(-38/20)]
    return float(20*np.log10(np.sqrt(np.mean(active**2))))


def run(cmd):
    subprocess.run(list(map(str, cmd)), check=True)


def board(key, asset, frames, rings):
    canvas, cw, ch, ox, oy = Build.compose(types.SimpleNamespace(out=AUDIT, tall_margin=False), asset, key)
    adjusted = [{**r, 'rect': [r['rect'][0]+ox, r['rect'][1]+oy, *r['rect'][2:]],
                 'pad': 0, 'radius': 16} for r in rings]
    spec = dict(image=str(canvas), fps=FPS, out_w=1280, out_h=720, upscale=3,
                beats=[dict(label='full-view', frames=frames, **{'from': [cw/2,ch/2,float(cw)], 'to': [cw/2,ch/2,float(cw)]})], rings=adjusted)
    p = AUDIT / f'leg-{key}.json'; p.write_text(json.dumps(spec, indent=2)+'\n')
    leg = AUDIT / f'leg-{key}.mkv'
    if leg.exists(): leg.unlink()
    run([sys.executable, ROOT/'scripts/video/ken_burns_path.py', p, leg])
    return leg, spec


def main():
    global AUDIT, DEST
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=Path, help='Revision-specific output, timing, and provenance settings')
    args = parser.parse_args()
    config = json.loads(args.config.read_text()) if args.config else {}
    AUDIT = ROOT / config.get('audit', str(AUDIT))
    DEST = ROOT / config.get('destination', str(DEST))
    assert sha(SOURCE) == SOURCE_SHA, 'Live source changed; re-evaluate the edit.'
    assert not DEST.exists(), 'Candidate already exists; use a new version.'
    AUDIT.mkdir(exist_ok=True)
    sources = [DONORS/f'opener-clip-{i}.wav' for i in (1,2,3)]
    protected = {str(p): sha(p) for p in sources+[SOURCE, ROOT/'index.html']}
    source_wav = AUDIT/'source-audio.wav'
    run([FF, '-v','error','-y','-i',SOURCE,'-vn','-ac','1','-ar',SR,'-c:a','pcm_s16le',source_wav])
    original = read(source_wav)
    # Quiet source room tone, inspected at the old transition. No new teaching pauses.
    seed = original[round(25.5*SR):round(25.7*SR)].copy(); seed -= seed.mean()
    tone_loop = np.r_[seed, seed[::-1]]
    tone = lambda n: np.resize(tone_loop, n)
    refs = [(26.5,34), (103,123), (133,140.4)]
    clips, provenance = [], []
    for idx, (p, ref) in enumerate(zip(sources, refs), 1):
        converted = AUDIT/f'donor-{idx}-resampled.wav'
        run([FF,'-v','error','-y','-i',p,'-ac','1','-ar',SR,'-c:a','pcm_s16le',converted])
        raw = read(converted)
        target = gated_db(original[round(ref[0]*SR):round(ref[1]*SR)])
        gain = target-gated_db(raw)
        processed = AUDIT/f'donor-{idx}-processed.wav'
        filt = f'volume={gain:.6f}dB,alimiter=limit=0.891250938:level=false:attack=5:release=50:latency=true'
        run([FF,'-v','error','-y','-i',converted,'-af',filt,'-ac','1','-ar',SR,'-c:a','pcm_s16le',processed])
        data = read(processed); assert len(data)==len(raw), (idx,len(data),len(raw))
        n = math.ceil(len(data)/SPF); padding = n*SPF-len(data)
        # Preserve complete original take. Add only frame-alignment tone (<1 frame).
        data = np.r_[data, tone(padding)]
        data += tone(len(data))
        ramp = np.linspace(0,1,240)
        bed = tone(len(data))
        data[:240] = data[:240]*ramp+bed[:240]*(1-ramp)
        data[-240:] = data[-240:]*(1-ramp)+bed[-240:]*ramp
        clips.append(data)
        provenance.append(dict(file=str(p), sha256=sha(p), script=SCRIPTS[idx-1],
            selected_source_seconds=[0,len(raw)/SR], original_rate=24000, output_rate=SR,
            output_frames=n, gain_db=gain, target_gated_db=target, processed_gated_db=gated_db(data),
            limiter_ceiling_db=-1, limiter_attack_ms=5, limiter_release_ms=50,
            filter=filt, frame_alignment_tone_samples=padding,
            voice=config.get('voice', 'Fola (user supplied)'), model_version='not provided',
            style=config.get('style', 'default; none requested; generation settings export not supplied'),
            generation_date='2026-09-26', audition='not performed; review required'))
    n1,n2,n3 = [len(c)//SPF for c in clips]
    # All source audio boundaries are in waveform-checked gaps, not guessed from ASR.
    # Video returns to the first clean title frame (794), avoiding 14 obsolete frames.
    rows = [
        dict(kind='clip', clip=1, frames=n1, source_replaced=[0,780], visual='refrain'),
        dict(kind='source', start=780, end=3345, frames=2565, initial_picture_clone=794),
        dict(kind='clip', clip=2, frames=n2, source_replaced=[3345,3483], visual='retimed-drawing'),
        dict(kind='source', start=3483, end=4212, frames=729),
        dict(kind='clip', clip=3, frames=n3, source_replaced=[4212,4384], visual='map-takeaway'),
        dict(kind='source', start=4384, end=4737, frames=353),
    ]
    parts=[]; at=0
    for r in rows:
        r['output_start']=at; at+=r['frames']; r['output_end']=at
        if r['kind']=='clip': data=clips[r['clip']-1]
        else:
            data=original[r['start']*SPF:r['end']*SPF].copy()
            # Only five milliseconds at graft joins; no speech falls in these windows.
            ramp=np.linspace(0,1,240); bed=tone(len(data))
            data[:240]=data[:240]*ramp+bed[:240]*(1-ramp)
            if r['end']!=4737: data[-240:]=data[-240:]*(1-ramp)+bed[-240:]*ramp
        assert len(data)==r['frames']*SPF
        parts.append(data)
    assembled=np.concatenate(parts); write(AUDIT/'edited.wav',assembled)
    refrain = ROOT/'course-assets/work-with-ai-opener/work-with-ai-opener-refrain.jpg'
    map_asset = ROOT/'course-assets/work-with-ai-opener/work-with-ai-opener-section-map.jpg'
    for p in [refrain,map_asset]: protected[str(p)]=sha(p)
    # Tight text rings, updated on the actual Fola phrase onsets. The board remains
    # full view; first spoken item arrives before two seconds, per Edit Spec §3.
    starts=config.get('opening_ring_frames', [15,86,154,239])
    ends=starts[1:]+[config.get('opening_ring_end_frame', 345)]
    rects=[[106,348,455,60],[106,421,550,69],[106,495,685,60],[106,563,865,61]]
    rings=[dict(start=a,end=b,rect=rect,color='#f2cf5b') for a,b,rect in zip(starts,ends,rects)]
    leg1,spec1=board('refrain',refrain,n1,rings)
    leg3,spec3=board('map-takeaway',map_asset,n3,[dict(start=config.get('map_ring_frame', 9),end=n3,rect=[40,743,1520,88],color='#6e51ff')])
    manifest=dict(candidate=str(DEST),source=str(SOURCE),source_sha256=SOURCE_SHA,
        scope='Three approved Fola passages; unpublished narrow repair',fps=FPS,total_frames=at,
        duration=at/FPS,rows=rows,donors=provenance,protected=protected,
        picture_notes=['Opening board held through transition; technical-diagram bridge removed.',
            'Source audio resumes at frame 780; title frame 794 covers preceding 14 obsolete picture frames.',
            'Clip 2 keeps the same precision/context drawing, retimed from source frames 3345–3482.',
            'Clip 3 rebuilds canonical map/banner; begins two frames before old visual cut to avoid orphan drawing.',
            'All other pictures/timing retained; single final H.264 encode from the live source.'],
        room_tone_source=[25.5,25.7],join_fades_ms=5,new_pauses='none; source and donor gaps retained',
        ring_px_at_720=4,board_specs=[spec1,spec3],audition='not performed')
    (AUDIT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (DONORS/config.get('provenance_filename', 'repair-provenance-2026-09-26.json')).write_text(json.dumps(provenance,indent=2)+'\n')
    (DONORS/'approved-script-2026-09-26.txt').write_text('\n\n'.join(f'CLIP {i+1}\n{s}' for i,s in enumerate(SCRIPTS))+'\n')
    reader=Reader(SOURCE); boards={1:Reader(leg1),3:Reader(leg3)}
    proc=subprocess.Popen([FF,'-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r',str(FPS),
        '-i','pipe:0','-i',str(AUDIT/'edited.wav'),'-map','0:v','-map','1:a',
        '-c:v','libx264','-profile:v','high','-level:v','3.1','-crf','16','-preset','fast','-pix_fmt','yuv420p',
        '-c:a','aac','-b:a','192k','-ar',str(SR),'-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for row in rows:
        for j in range(row['frames']):
            if row['kind']=='source':
                idx=row['start']+j
                if row.get('initial_picture_clone'): idx=max(idx,row['initial_picture_clone'])
                im=reader.at(idx)
            elif row['clip'] in (1,3): im=boards[row['clip']].at(j)
            else:
                a,b=row['source_replaced']; idx=a+round(j*(b-a-1)/(row['frames']-1));im=reader.at(idx)
            proc.stdin.write(im.tobytes())
        print('RENDERED',row['output_start'],row['output_end'],flush=True)
    proc.stdin.close(); assert proc.wait()==0
    for p,h in protected.items(): assert sha(p)==h, f'Protected input changed: {p}'
    cap=cv2.VideoCapture(str(DEST));count=0
    while cap.grab():count+=1
    cap.release();assert count==at,(count,at)
    manifest.update(candidate_sha256=sha(DEST),decoded_frames=count,protected_inputs_unchanged=True)
    (AUDIT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    boundaries=[]
    for row in rows[1:]:boundaries+=['--boundary',f"{row['output_start']}:passage-{rows.index(row)+1}"]
    guard=subprocess.run([sys.executable,str(ROOT/'scripts/video/transition_guard.py'),str(DEST),*boundaries,'--outdir',str(AUDIT/'transitions')])
    print('COMPLETE',DEST,'frames',count,'guard',guard.returncode,flush=True)


if __name__=='__main__': main()

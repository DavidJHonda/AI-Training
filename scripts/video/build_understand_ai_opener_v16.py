#!/usr/bin/env python3
"""Reorder the first two roadmap topics using only existing v15 narration."""
import json
import subprocess
from pathlib import Path

import cv2
import imageio_ffmpeg
import numpy as np

from build_understand_ai_opener_v12 import sha, render_states
import build_understand_ai_opener_v12 as renderer
from editspec_build import Build

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'Prompts/understand-ai-opener-v15.mp4'
ASSET = ROOT / 'course-assets/understand-ai-opener/understand-ai-opener-section-map.jpg'
OUT = ROOT / 'video-audit/understand-opener-reorder-2026-11-04'
DEST = ROOT / 'Prompts/understand-ai-opener-v16.mp4'
EXPECTED = 'a00f07b22a8764ba7e4950d7473a25ceb5eb505f165c2da20c4f19cce948ceaa'
FPS, TOTAL, SR = 30, 4187, 48000
MAP_START, MAP_END = 2229, 3920
BREAK_START, BREAK_END = 3041, 3367
# Measured quiet phoneme boundaries, checked by isolated-phrase transcription.
# Preserve both original introductions: "We'll start with" and "Second is".
A, B, C, D = 87.245, 93.650, 94.535, 101.650
SPANS = [(0, A), (C, D), (B, C), (A, B), (D, TOTAL / FPS)]


def main():
    assert sha(SOURCE) == EXPECTED
    assert not DEST.exists(), 'Never overwrite a review candidate.'
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'preview').mkdir(exist_ok=True)
    asset_hash = sha(ASSET)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    original = np.frombuffer(subprocess.check_output([
        ff, '-v', 'error', '-i', str(SOURCE), '-vn', '-ac', '1', '-ar', str(SR),
        '-f', 'f32le', '-']), dtype='<f4')
    pieces = [original[round(s*SR):round(e*SR)].copy() for s, e in SPANS]
    timeline, cursor = [], 0
    for (s, e), piece in zip(SPANS, pieces):
        timeline.append(dict(source_seconds=[s, e], output_seconds=[cursor/SR, (cursor+len(piece))/SR]))
        cursor += len(piece)
    edited = np.concatenate(pieces)
    assert len(edited) == TOTAL * SR // FPS
    # Five-ms cross-blends use the following source's preceding quiet handle,
    # without changing duration or introducing a digital-silence gap.
    seams, cursor, fade = [], 0, 240
    for i in range(1, len(pieces)):
        cursor += len(pieces[i-1])
        donor = round(SPANS[i][0]*SR)
        mix = np.linspace(0, 1, fade, dtype=np.float32)
        edited[cursor-fade:cursor] = edited[cursor-fade:cursor]*(1-mix) + original[donor-fade:donor]*mix
        seams.append(cursor/SR)
    audio = OUT / 'edited-audio.f32'
    edited.astype('<f4').tofile(audio)

    build = Build(ROOT, SOURCE, OUT, DEST, protected=[ASSET])
    canvas, cw, ch, ox, oy = build.compose(ASSET, 'map')
    assert (cw, ch, ox, oy) == (2096, 1180, 248, 44)
    # Exact current board row boundaries; preserve the existing full-view camera.
    rows = [(127,151), (278,152), (430,150), (580,193), (773,152)]
    onsets = [86.26, A + (D-C) + (93.76-B), 102.34, 112.92, 122.82]
    colors = ['#4f2fc4','#1652f0','#0e8f86','#0f7a4a','#a9760c']
    starts = [round(t*FPS)-MAP_START for t in onsets]
    ends = starts[1:] + [MAP_END-MAP_START]
    spec = dict(image=str(canvas), fps=FPS, out_w=1280, out_h=720, upscale=3,
                beats=[dict(label='full-view',frames=MAP_END-MAP_START,
                            **{'from':[cw/2,ch/2,float(cw)],'to':[cw/2,ch/2,float(cw)]})],
                rings=[dict(start=s,end=e,rect=[80+ox,y+oy,1440,h],color=c,pad=0,radius=18)
                       for s,e,(y,h),c in zip(starts,ends,rows,colors)],
                provenance=dict(canonical_asset=str(ASSET),sha256=asset_hash,offset=[ox,oy],density='compact',ring_px=4))
    (OUT / 'leg-map.json').write_text(json.dumps(spec,indent=2)+'\n')
    renderer.OUT = OUT
    states = render_states(spec, 'map')
    boundaries = [dict(frame=f,label=l) for f,l in
                  [(MAP_START,'updated-map-entry'),(BREAK_START,'token-animation-entry'),
                   (BREAK_END,'return-to-map'),(MAP_END,'preserved-close')]]
    boundaries += [dict(frame=round(s*FPS),label=f'audio-splice-{i+1}') for i,s in enumerate(seams)]
    manifest = dict(scope='Narrow roadmap reorder requested November 4; review candidate only.',
        source=str(SOURCE),source_sha256=EXPECTED,candidate=str(DEST),asset=str(ASSET),asset_sha256=asset_hash,
        fps=FPS,output_frames=TOTAL,duration=TOTAL/FPS,audio_timeline=timeline,audio_seams_seconds=seams,
        boundaries=sorted(boundaries,key=lambda b:b['frame']),ring_onsets_seconds=onsets,
        map_source_frames=[MAP_START,MAP_END],preserved_animation_frames=[BREAK_START,BREAK_END],
        board_plan='Understand AI: full unmarked opening, fixed full view, one 4px row outline at each spoken topic. Updated five-row JPG. Existing token animation retained.',
        narration='We’ll start with why probability matters ... Second is how AI learned ... Third, how words become numbers ... Fourth is how meaning takes shape ... Finally, how AI builds an answer.',
        pauses='Original audio samples reordered; no added pause, no removed words, unchanged total duration. Four 5ms quiet-handle blends.',
        limitations=['Uses the existing finished v15, with one video/audio re-encode.',
                     'Automated transcription and waveform checks do not certify natural-sounding joins; listening review remains.',
                     'No local installation, commit, or publication authorized by this build.'])
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    command=[ff,'-n','-v','error','-f','rawvideo','-pix_fmt','bgr24','-s','1280x720','-r',str(FPS),
        '-i','pipe:0','-f','f32le','-ar',str(SR),'-ac','1','-i',str(audio),
        '-map','0:v:0','-map','1:a:0','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p',
        '-c:a','aac','-b:a','192k','-movflags','+faststart',str(DEST)]
    proc=subprocess.Popen(command,stdin=subprocess.PIPE)
    cap=cv2.VideoCapture(str(SOURCE)); count=0
    while True:
        ok, frame=cap.read()
        if not ok: break
        if MAP_START <= count < MAP_END and not BREAK_START <= count < BREAK_END:
            frame=next(im for s,e,im in states if s <= count-MAP_START < e)
        proc.stdin.write(frame.tobytes()); count+=1
        if count % 900 == 0: print(f'Encoded {count}/{TOTAL} frames',flush=True)
    cap.release();proc.stdin.close()
    assert proc.wait() == 0 and count == TOTAL
    assert sha(SOURCE) == EXPECTED and sha(ASSET) == asset_hash
    manifest['candidate_sha256']=sha(DEST)
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    audio.unlink()
    print(DEST,flush=True)


if __name__ == '__main__':
    cv2.setNumThreads(1)
    main()

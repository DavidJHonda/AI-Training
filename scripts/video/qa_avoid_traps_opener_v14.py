#!/usr/bin/env python3
"""Check the requested cut, retained pictures/speech, and one-second ending."""
import json
import re
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw

import build_avoid_traps_opener_v14 as b
from editspec_build import Reader, readwav, sha, SPF


def main():
    manifest = json.loads((b.OUT/'edit-manifest.json').read_text())
    subprocess.run([b.FF,'-y','-v','error','-i',str(b.DEST),'-vn','-ac','1','-ar','48000',
        '-c:a','pcm_s16le',str(b.OUT/'candidate.wav')],check=True)
    source = readwav(b.OUT/'source.wav')
    planned = readwav(b.OUT/'edited.wav')
    actual = readwav(b.OUT/'candidate.wav')
    join = b.CUT_START*SPF
    assert np.array_equal(planned[:join-240],source[:join-240])
    assert np.array_equal(planned[join+240:],source[b.CUT_END*SPF+240:b.SOURCE_END*SPF])
    audio_corr = float(np.corrcoef(planned,actual[:len(planned)])[0,1])
    assert audio_corr > .995
    rows = b.picture_rows()
    states = b.OUT/'encoded-states'
    states.mkdir(exist_ok=True)
    wanted = set(range(0,b.TOTAL,120)) | {b.TOTAL-1,b.CUT_START-1,b.CUT_START,b.TOTAL-31,b.TOTAL-30}
    wanted |= {row['start'] for row in rows}
    cap = cv2.VideoCapture(str(b.DEST))
    count = 0
    tiles = []
    errors = []
    tail = []
    last_frame = None
    for row in rows:
        file,_ = b.picture_location(row,row['start'])
        reader = Reader(file)
        for f in range(row['start'],row['end']):
            ok,frame = cap.read()
            assert ok,f
            _,sf = b.picture_location(row,f)
            expected = reader.at(sf)
            small = cv2.resize(frame,(320,180)).astype(float)
            reference = cv2.resize(expected,(320,180)).astype(float)
            error = float(abs(small-reference).mean())
            assert error < 4,(f,error)
            errors.append(error)
            if f >= b.TOTAL-30:
                tail.append(small)
            if f in wanted:
                cv2.imwrite(str(states/f'{f:05}.jpg'),frame)
                tile = Image.new('RGB',(384,240),'white')
                tile.paste(Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)).resize((384,216)),(0,24))
                ImageDraw.Draw(tile).text((5,5),f'f{f} / {f/30:.3f}s',fill='black')
                tiles.append(tile)
            count += 1
            last_frame = frame
        reader.c.release()
    assert count==b.TOTAL and not cap.read()[0]
    cap.release()
    cv2.imwrite(str(b.OUT/'final-frame.jpg'),last_frame)
    for k in range(0,len(tiles),12):
        batch = tiles[k:k+12]
        sheet = Image.new('RGB',(1536,240*((len(batch)+3)//4)),'#eee')
        for j,tile in enumerate(batch):sheet.paste(tile,(j%4*384,j//4*240))
        sheet.save(b.OUT/f'encoded-review-{k//12+1}.jpg')
    subprocess.run([b.FF,'-v','info','-i',str(b.DEST),'-vn','-af',
        'silencedetect=noise=-38dB:d=0.12','-f','null','-'],check=True,
        stdout=subprocess.DEVNULL,stderr=(b.OUT/'encoded-silences.txt').open('w'))
    silences = []
    start = None
    for line in (b.OUT/'encoded-silences.txt').read_text().splitlines():
        s = re.search(r'silence_start: ([0-9.]+)',line)
        e = re.search(r'silence_end: ([0-9.]+).*silence_duration: ([0-9.]+)',line)
        if s:start=float(s.group(1))
        if e and start is not None:
            silences.append(dict(start=start,end=float(e.group(1)),duration=float(e.group(2))))
            start=None
    final_silence = silences[-1]
    silent_video_tail = b.TOTAL/30-final_silence['start']
    assert abs(silent_video_tail-1)<1/30,(silent_video_tail,final_silence)
    gap = next(s for s in silences if s['start']<=b.CUT_START/30<=s['end'])
    tail_motion = max(float(abs(x-tail[0]).mean()) for x in tail)
    assert tail_motion<.2,tail_motion
    for path,h in manifest['protected_hashes'].items():assert sha(path)==h,path
    guard = [str(b.ROOT/'.video-venv/bin/python'),str(b.ROOT/'scripts/video/transition_guard.py'),str(b.DEST)]
    for row in rows[1:]:guard += ['--boundary',f"{row['start']}:{row['label']}"]
    guard += ['--outdir',str(b.OUT/'guard')]
    subprocess.run(guard,check=True)
    q = dict(decoded_frames=count,duration=count/30,source_cut_seconds=[40.9,55.5],
        all_visual_frames_compared=count,max_mean_pixel_error=max(errors),
        retained_PCM_identical_outside_join_fades=True,encoded_audio_correlation=audio_corr,
        encoded_audio_peak_dbfs=float(20*np.log10(abs(actual).max()/32768)),
        join_quiet_interval=gap,final_quiet_interval=final_silence,
        silent_tail_to_final_video_frame_end_seconds=silent_video_tail,
        final_settled_frames=30,maximum_settled_frame_mean_difference=tail_motion,
        source_hashes_unchanged=True,candidate_sha256=sha(b.DEST),
        direct_listening_performed=False,continuous_audiovisual_review_performed=False)
    (b.OUT/'qa.json').write_text(json.dumps(q,indent=2)+'\n')
    print(json.dumps(q,indent=2))


if __name__=='__main__':main()

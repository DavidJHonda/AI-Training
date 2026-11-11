#!/usr/bin/env python3
"""Requested 0:41–0:56 deletion and one-second closing tail; review candidate."""
from pathlib import Path
import json
import subprocess
import wave

import cv2
import numpy as np

import build_avoid_traps_opener_v13 as previous
from editspec_build import Reader, readwav, writewav, sha, SPF

ROOT = previous.ROOT
SRC = previous.DEST
DEST = ROOT/'Prompts/avoid-traps-opener-v14.mp4'
OUT = ROOT/'video-audit/avoid-opener-v14-2026-11-11'
FF = previous.FF
SOURCE_HASH = 'abd6bc63e60ed125b052ed5ae552a22963b430ad633104182c85f4bfca488a88'
CUT_START, CUT_END = 1227, 1665  # 40.900–55.500, both within measured quiet intervals.
SOURCE_END = 4030               # 134.333, ~1.000 s beyond final speech at 133.336.
REMOVED = CUT_END-CUT_START
TOTAL = SOURCE_END-REMOVED
ORIGINAL_CLOSE = 3835
CLOSE_START = ORIGINAL_CLOSE-REMOVED
CLOSE_HOLD, CLOSE_PUSH, CLOSE_TAIL = 48, 117, 30


def picture_rows():
    rows = []
    # Preserve the exact v13 donor/frame mapping. Truncating rows must not
    # rescale their retained animation or change earlier/later reveal timing.
    for start, end, shift in [(0,CUT_START,0),(CUT_END,ORIGINAL_CLOSE,REMOVED)]:
        for original in previous.ROWS:
            a, b = max(start,original['start']), min(end,original['end'])
            if a < b:
                rows.append(dict(start=a-shift,end=b-shift,previous_frames=[a,b],
                    previous_row=original,label=original['label'],kind='retained'))
    rows += [
        dict(start=CLOSE_START,end=CLOSE_START+CLOSE_HOLD,kind='close-hold',
             source_start=3835,source_end=3883,label='Existing full-view closing hold'),
        dict(start=CLOSE_START+CLOSE_HOLD,end=CLOSE_START+CLOSE_HOLD+CLOSE_PUSH,
             kind='close-push',source_start=3883,source_end=4033,
             label='Complete existing closing push by final word'),
        dict(start=TOTAL-CLOSE_TAIL,end=TOTAL,kind='close-tail',source_start=4033,
             source_end=4034,label='One-second settled closing tail'),
    ]
    assert rows[0]['start']==0 and rows[-1]['end']==TOTAL
    assert all(a['end']==b['start'] for a,b in zip(rows,rows[1:]))
    return rows


def picture_location(row, f):
    if row['kind']=='retained':
        old = row['previous_frames'][0]+f-row['start']
        original = row['previous_row']
        return original['file'],previous.source_frame(original,old)
    i = f-row['start']
    count = row['end']-row['start']
    sf = row['source_start']+round(i*(row['source_end']-row['source_start']-1)/max(1,count-1))
    return str(previous.BASE),sf


def make_audio():
    wav = OUT/'source.wav'
    if not wav.exists():
        subprocess.run([FF,'-v','error','-i',str(SRC),'-vn','-ac','1','-ar','48000',
            '-c:a','pcm_s16le',str(wav)],check=True)
    audio = readwav(wav)
    left = audio[:CUT_START*SPF].copy()
    right = audio[CUT_END*SPF:SOURCE_END*SPF].copy()
    # Existing room tone in the quiet handles, with 5 ms edge blends only.
    seed = audio[round(40.75*48000):round(40.80*48000)].copy()
    tone = np.resize(seed,240)
    ramp = np.linspace(0,1,240)
    left[-240:] = left[-240:]*(1-ramp)+tone*ramp
    right[:240] = right[:240]*ramp+tone*(1-ramp)
    edited = np.r_[left,right]
    assert len(edited)==TOTAL*SPF
    writewav(OUT/'edited.wav',edited)


def main():
    assert not DEST.exists(),'Use a new candidate version; never overwrite.'
    assert sha(SRC)==SOURCE_HASH
    for path,expected in previous.EXPECTED.items():
        assert sha(path)==expected,path
    OUT.mkdir(exist_ok=True,parents=True)
    make_audio()
    rows = picture_rows()
    manifest = dict(
        authorization='User: Do you think we can delete from :41 to :56? Also, trim the end so there is only a 1 second dead space at the end.',
        scope='Narrow removal of the indicated passage and shortening of the closing tail; live-graphics sequence retained',
        source=str(SRC),source_sha256=SOURCE_HASH,output=str(DEST),fps=30,
        frames=TOTAL,duration=TOTAL/30,
        audio_keep_frames=[[0,CUT_START],[CUT_END,SOURCE_END]],
        removed_source_frames=[CUT_START,CUT_END],removed_source_seconds=[CUT_START/30,CUT_END/30],
        removed_words='A synthetic image or a cloned voice ... naturally accept it as truth. To understand how this deception works ... look at the physical world.',
        retained_entry='Think about a coastal rip current.',
        cut_output_frame=CUT_START,
        quiet_source_runs_seconds=[[40.37,41.26],[54.675,55.70],[133.305,138.45]],
        final_speech_source_end_seconds=133.336396,
        predicted_silent_tail_seconds=SOURCE_END/30-133.336396,
        added_instructional_pauses=0,
        visual_rows=rows,
        closing=dict(start_frame=CLOSE_START,full_view_hold_frames=CLOSE_HOLD,
            push_frames=CLOSE_PUSH,settled_tail_frames=CLOSE_TAIL,
            reason='Requested one-second silence overrides the longer default close. Finish the existing 1.2x push with the final word, then hold for 30 frames.'),
        protected_hashes={str(SRC):SOURCE_HASH,**{str(p):h for p,h in previous.EXPECTED.items()}},
        narration_note='Requested deletion removes the opening fake-media example and bridge. The third exact guiding question still introduces convincing fakes; the rip-current analogy remains intact.',
        direct_listening_performed=False,continuous_audiovisual_review_performed=False,installed=False,
    )
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    p = subprocess.Popen([FF,'-n','-v','error','-f','rawvideo','-pix_fmt','bgr24',
        '-s','1280x720','-r','30','-i','pipe:0','-i',str(OUT/'edited.wav'),
        '-map','0:v:0','-map','1:a:0','-c:v','libx264','-threads','2','-crf','16',
        '-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
        '-movflags','+faststart',str(DEST)],stdin=subprocess.PIPE)
    for row in rows:
        file,_ = picture_location(row,row['start'])
        reader = Reader(file)
        for f in range(row['start'],row['end']):
            _,sf = picture_location(row,f)
            p.stdin.write(reader.at(sf).tobytes())
        reader.c.release()
        print(f"Rendered {row['end']/30:.3f}s: {row['label']}",flush=True)
    p.stdin.close()
    assert p.wait()==0
    assert all(sha(path)==expected for path,expected in manifest['protected_hashes'].items())
    manifest['sha256']=sha(DEST)
    manifest['protected_inputs_unchanged']=True
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Completed {DEST}; {TOTAL} frames / {TOTAL/30:.3f}s',flush=True)


if __name__=='__main__':
    main()

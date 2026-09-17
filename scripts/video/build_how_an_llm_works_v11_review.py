#!/usr/bin/env python3
"""Narrow v10 repair: only the two jelly-row outlines at 4:35.8–4:42.5.

The owner asked whether graphics existed for 2:21–2:46; that section remains
unchanged pending selection. Rebuild visuals from pristine sources; copy AAC.
"""
import argparse
import json
import subprocess
import cv2
import build_how_an_llm_works_v10_review as base
from editspec_build import sha, PURPLE

ROOT=base.ROOT
PREVIOUS=ROOT/'Prompts/how-an-llm-works-v10.mp4'
OLD=base.OUT
OUT=ROOT/'video-audit/how-an-llm-works-repair-2026-09-17-v11'
DEST=ROOT/'Prompts/how-an-llm-works-v11.mp4'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-only',action='store_true');args=ap.parse_args()
    old=json.loads((OLD/'edit-manifest.json').read_text())
    assert sha(PREVIOUS)==old['render_sha256']
    for path,digest in old['protected_hashes'].items():assert sha(path)==digest,path
    base.OUT=OUT;base.DEST=DEST
    b=base.prepare()
    b.hashes[str(PREVIOUS)]=sha(PREVIOUS)
    b.tone_meta=dict(old['audio'],delivery='AAC stream copied bit-for-bit from v10; no audio edits')
    b.grafts=old['grafts']
    start,end=base.A(94.1),base.A(100.8)
    def rows_only(spec):
        chosen=[r for r in spec['rings'] if r['start']==start-b.boards['odds']['src_in']]
        assert len(chosen)==2
        for r,rect in zip(chosen,[[62,368,756,445],[842,671,1536,754]]):
            replacement=base.ring(b,'odds',start,end,rect,PURPLE)
            r.update(replacement)
    base.update_spec(b,'odds',rows_only)
    b.boards['odds']['comparison_highlights']='Only complete jelly rows (word, bar, percentage); purple accent on both.'
    base.previews(b)
    b.manifest(dict(scope_detail='Narrow visual repair: replace whole-card comparison outlines with jelly-row outlines; everything else unchanged.',
                    previous_candidate=str(PREVIOUS),previous_sha256=sha(PREVIOUS),
                    changed_output_frames=[[start,end]],changed_output_seconds=[[start/30,end/30]],
                    unchanged_patterns_section='2:21–2:46; donor options inspected, not inserted without selection.',
                    long_board_exception=old['long_board_exception'],
                    timing_coordinate_system=old['timing_coordinate_system'],
                    literal_listening_performed=False))
    if args.prepare_only:return
    base.render(b,copy_audio_from=PREVIOUS)
    def audio_hash(path):
        return subprocess.check_output([b.ff,'-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-'],text=True).strip()
    hashes={p.name:audio_hash(p) for p in (PREVIOUS,DEST)}
    assert len(set(hashes.values()))==1,hashes
    cap=cv2.VideoCapture(str(DEST));count=0
    metadata=dict(fps=cap.get(cv2.CAP_PROP_FPS),width=cap.get(cv2.CAP_PROP_FRAME_WIDTH),height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    want={start-1,start,start+1,start+30,end-1,end,base.TOTAL-1}
    qa=OUT/'encoded-checks';qa.mkdir(exist_ok=True)
    while True:
        ok,im=cap.read()
        if not ok:break
        if count in want:cv2.imwrite(str(qa/f'f{count:05d}.jpg'),im,[cv2.IMWRITE_JPEG_QUALITY,96])
        count+=1
    cap.release();assert count==base.TOTAL
    assert metadata==dict(fps=30.,width=1280.,height=720.)
    (qa/'verification.json').write_text(json.dumps(dict(decoded_frames=count,metadata=metadata,audio_hashes=hashes,
                                                       audio_bitstream_identical=True),indent=2))
    subprocess.run([str(ROOT/'.video-venv/bin/python'),str(ROOT/'scripts/video/transition_guard.py'),str(DEST),
                    '--outdir',str(OUT/'transitions'),'--boundary',f'{start}:jelly-row-comparison',
                    '--boundary',f'{end}:comparison-to-takeaway'],check=True)


if __name__=='__main__':main()

#!/usr/bin/env python3
"""Keep the approved community donor, starting after its incoming scene cut."""
import build_big_upside_v10 as repair

lab_plan=repair.corrected_plan

def final_plan(rows):
    spans=lab_plan(rows)
    for span in spans:
        if span['start_frame']==701:
            assert span['state'][3]=='community benefits'
            span['state']=('clip',2,7200,'community benefits')
    return spans

def configure():
    root=repair.b.ROOT
    repair.SOURCE=root/'Prompts/big-upside-v11.mp4'
    repair.OLD_OUT=root/'video-audit/big-upside-build-2026-11-03-v11'
    repair.OUT=root/'video-audit/big-upside-build-2026-11-03-v12'
    repair.DEST=root/'Prompts/big-upside-v12.mp4'
    repair.FIX_RANGE=(701,874)
    repair.REASON='Begin community donor at source 240.0 seconds, after its incoming scene cut; avoid five frames of the preceding river scene.'
    repair.corrected_plan=final_plan
    repair.configure()

if __name__=='__main__':
    configure()
    repair.main()

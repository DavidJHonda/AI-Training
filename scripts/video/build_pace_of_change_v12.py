#!/usr/bin/env python3
"""Same approved v11 assembly, fixing four short donor-scene leaks from pristine rolls."""
import build_pace_of_change_v11 as b

def configure():
    b.OUT=b.ROOT/'video-audit/pace-of-change-build-2026-11-03-v12'
    b.DEST=b.ROOT/'Prompts/pace-of-change-v12.mp4'
    # Hold the last valid picture for 2, 4, 6 and 5 frames respectively.
    # Audio, duration, other picture frames and every planned splice are unchanged.
    b.VIDEO_LIMITS={'person working with context':763,'competition':3215,
                    'limitation can change':4164,'human work':4510}

if __name__=='__main__':
    configure()
    b.main()

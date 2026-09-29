#!/usr/bin/env python3
"""V14 QA correction: cut away before the two-frame banner flash."""
import build_how_an_llm_works_v14 as repair

repair.OUT = repair.ROOT / 'video-audit/how-an-llm-works-repair-2026-09-28-v15'
repair.DEST = repair.ROOT / 'Prompts/how-an-llm-works-v15.mp4'
repair.LOOP_IN = 8296

if __name__ == '__main__':
    repair.main()

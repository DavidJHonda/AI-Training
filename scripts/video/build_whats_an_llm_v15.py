#!/usr/bin/env python3
"""V14 QA correction: cut away before the two-frame banner flash."""
import build_whats_an_llm_v14 as repair

repair.OUT = repair.ROOT / 'video-audit/whats-an-llm-repair-2026-09-28-v15'
repair.DEST = repair.ROOT / 'Prompts/whats-an-llm-v15.mp4'
repair.LOOP_IN = 8296

if __name__ == '__main__':
    repair.main()

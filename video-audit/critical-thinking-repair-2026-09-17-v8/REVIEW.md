# Critical Thinking v8 — pre-banner whistle removal

## Recommendation

**KEEP after David's targeted listen at 2:53–2:55.** V8 removes the separate low-level burst immediately before the habits-board banner highlight. V7 silenced the gap after that burst but still retained the burst itself.

Direct audio playback is unavailable in this runtime. Signal analysis confirms the suspicious burst has been removed from the finished output, but David's listening check remains required.

## Output

- Candidate: `Prompts/critical-thinking-v8.mp4`
- SHA-256: `3ff25acf0e0823e88c112f45818f8bf4b340a79ed1436d3ecf502fa629008deb`
- Exact decode: 5,935 frames / 3:17.83 at 30 fps, 1280×720
- Live course video and all protected sources/materials: unchanged
- Publishing/deployment: not performed

## Repair

- Signal review located the remaining burst at approximately **2:53.64–2:53.73** in v7.
- The donor now ends four frames earlier, at output frame **5,209** / **2:53.63**, after the useful decay of “more.”
- The donor tail fades directly to silence instead of to the previous room-tone seed.
- Output frames **5,209–5,227** are silent; clean base narration resumes at frame **5,228**.
- The banner highlight begins at frame **5,209**, matching the location David described.
- Duration and all downstream narration timing remain unchanged.

## QA

- Decode/count: **PASS**, 5,935/5,935 frames.
- Targeted decoded-audio measurement: **PASS**; the removed interval is effectively zero-level after AAC decoding.
- Protected hashes: **PASS**.
- Transition guard: **12/13 automatic PASS**. The one flag is a false positive caused by the intended smooth pullback from Habit 5 to the full board at frames 5,197–5,208; manual inspection shows no stale-frame island.
- Duration and downstream visual timeline: unchanged.

Please listen to **2:53.2–2:54.8**. If the whistle is gone and “more” still sounds complete, v8 is the final KEEP candidate.

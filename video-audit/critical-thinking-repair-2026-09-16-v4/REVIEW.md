# Critical Thinking v4 — post-listen boundary repairs

## Recommendation

**KEEP after David's targeted listen.** V4 repairs the three defects David found in v3: the split word “bias” at 2:06–2:07, the stray next-word remnant at 2:54, and the old-graphic flash at 3:02. No reroll or Training Bias donor was required.

Direct audio playback is unavailable in this runtime. Finished-video medium English transcription and waveform analysis confirm the intended words and silent boundaries, but David's ear remains the final authority.

## Output

- Candidate: `Prompts/critical-thinking-v4.mp4`
- SHA-256: `088ca6b96fb7676b97623ba64c18c95847c98e5312cf61a636a3b5e24505b0b2`
- Format: 1280×720, 30 fps, H.264/AAC mono at 48 kHz
- Exact decode: 5,935 frames / 3:17.83
- Live course video and all protected sources/materials: unchanged
- Publishing/deployment: not performed

## Repairs

### 1. “Confirmation bias” at 2:06–2:07

V3 split the last syllable because its pause began at source frame 3,776, before the word had finished. V4 moves the edit to source frame 3,798 (2:06.60), the deepest measured silence after the complete word and before “This board.”

- Finished ASR: “...vulnerable to confirmation bias.” ends at **2:06.64**.
- The half-second matched-room-tone pause runs at output frames **3,813–3,828** (**2:07.10–2:07.60**).
- “This board outlines five habits...” begins at **2:07.76**.

The existing reroll therefore contains a complete usable “bias”; the Training Bias lesson was not needed.

### 2. Stray word remnant at 2:54

V3 kept donor audio through source frame 5,117, exposing the low-level onset of reroll 3's next word, “These.” V4 ends the donor at frame **5,114** (2:50.47), before that onset.

- “...when you learn more.” ends at **2:53.76**.
- “These five questions...” begins from the base roll at **2:54.46**.
- The 0.70-second intervening gap is classified as breath/room sound; no extra word appears in the finished transcript.

### 3. Old graphic flash at 3:02

V3 retained a 24-frame laptop bridge before the corrected AI diagram. V4 removes that bridge. The canonical Five Habits board now cuts directly to reroll 3's accurate AI decision diagram at output frame **5,441** (**3:01.37**), so the old graphic never appears.

## QA

- Finished-video transcription: **PASS**, 511 words; “confirmation bias,” Habit 5, the AI distinction, and the exact close are intact.
- Transition guard: **PASS, 11/11 boundaries**, no stale-frame islands.
- Whole-video contact-sheet review: **PASS**.
- Decode/count: **PASS**, 5,935/5,935 frames.
- Corner-mark cleanup: 1,604 cloned frames, 420 inpainted frames, 0 declined.
- Canonical close: **PASS**, literal final frame at the prescribed settled size.
- Protected files: **PASS**, all hashes unchanged.

## Targeted listen

Please listen to:

1. **2:05.8–2:08.2** — complete “confirmation bias,” pause, and “This board.”
2. **2:53.2–2:55.0** — “learn more” into “These five questions,” with no stray onset.
3. **3:00.8–3:03.5** — board-to-diagram transition; visually there is no old laptop flash.

If those windows sound clean, v4 is the KEEP candidate.

See `edit-manifest.json`, `transcript/`, `audio-gap-review/`, `transition-guard/`, `full-pass/`, and `final-frame.jpg` for the supporting evidence.

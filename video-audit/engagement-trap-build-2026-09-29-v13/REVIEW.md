# Engagement Trap v13 — approved repair candidate

Built September 29, 2026 after David's “Agree with all. Build please.”

**Candidate:** `Prompts/engagement-trap-v13.mp4` — 4:21.07, 1280×720, 30 fps, 7,832 frames. Review candidate only; not installed, committed, or published.

## What changed

- Corrected the settlement phone's false 60-minute and 10 p.m.–7 a.m. labels to two hours and midnight–6 a.m.; removed the unsupported “Unrestricted” claim. Kept the paper setting and animated arrow, and rebuilt the phone interface with a stable shell and progressive controls.
- Restored **UP TO $17.1B** in the following scene, matching the figure's entrance to the source reveal. The surrounding illustrative animation remains.
- Removed the compulsory “typing a rejection” sentence, the clause asserting that extra time directly translates into higher revenue, and “Interrupting alerts now appear.” The last edit now reads: “The middle panel outlines prompts to pause after fifteen minutes of continuous use, and again at sixty and ninety minutes of total daily use.”
- Rebuilt the first, third and fourth canonical boards at full view with fixed four-pixel rings. Their full-view frames were inspected at delivery size. The first board is small but readable; its conversation is never cropped or zoomed. The final board reads comfortably without dives. The third board stays whole instead of diving into the illustration.
- Broke up the long holds using the existing follow-up animation, a new animated 25-minute timer diagram, and an illustrative pause prompt. The longest uninterrupted board run is now **19.33 seconds**, down from 56.2 seconds.
- Preserved the other Notebook scenes, the short infinite-scroll board, and the canonical close through the literal last frame.

The new timer and prompt are code-rendered explanatory graphics, not regenerated course boards or photographs. Their source is retained in the builder. No external assets or synthesized narration were introduced.

## Output timeline

| Output | Treatment |
|---|---|
| 0:30.27–0:48.50 | Full first board; question then answer bubble highlighted |
| 0:48.50–0:58.90 | Existing follow-up animation, ending on the complete three offers |
| 0:58.90–1:10.70 | First board; stop then trap outcomes |
| 1:10.70–1:16.97 | Animated 25-minute detour graphic |
| 1:16.97–1:26.47 | First-board takeaway |
| 1:33.80–1:52.20 | Existing infinite-scroll board, unchanged |
| 2:25.60–2:38.50 | Complete AI Won’t Quit for You board and takeaway |
| 3:04.47–3:10.17 | Corrected settlement phone |
| 3:10.17–3:19.33 | Qualified settlement amount, surrounding source animation retained |
| 3:19.33–3:32.60 | Complete stopping-points board; daily limit then prompts |
| 3:32.60–3:37.07 | Animated fifteen-minute pause prompt |
| 3:37.07–3:56.40 | Board returns for sixty/ninety-minute detail, night block and takeaway |
| 4:08.70–4:21.07 | Preserved canonical closing sequence |

No new pauses were added. Returning to a previously established board resumes its current highlight.

## Audio edits to listen to

| Output join | Removed source span | Result / evidence |
|---|---|---|
| **2:31.27** | 2:31.267–2:34.767, “You must manually insert your own friction by typing a rejection.” | “follow-up task” → “Successfully using AI…”; both cut edges in measured quiet intervals |
| **2:44.23** | 2:47.733–2:51.467, “because more time spent directly translates into higher revenue.” | “session length” → “These metrics drive…”; both edges quiet |
| **3:34.30** | 3:41.533–3:43.500, “Interrupting alerts now appear” | “prompts to pause” → “after fifteen minutes…”; quiet boundary before the complete word “after” |

All cuts use the same source voice, no gain changes, and five-millisecond source-room-tone crossfades. Picture-only cuts never divide the audio. The joined wording was checked by fresh small.en transcription. v13 changes only the five-millisecond room-tone fades from v12, using contiguous samples across each join; the speech is identical. Transcription and waveform checks are not listening. The retained phrase “Engagement is an engineered outcome” was truncated by one diagnostic ASR crop and misread as “Management”; it is untouched source audio, not a new defect.

## Source and build provenance

- Verified source: `course-assets/engagement-trap/engagement-trap.mp4`.
- SHA-256: `edb8ed9171d06d3755335f0b63985424cbc59ef32c8411a0d63bb749ba0e7740`.
- The original raw rolls remain absent. This candidate uses the finished file, with one new encode from that source; v12 is not an encode of v11. Changed boards come directly from the exact canonical JPGs.
- Visual builder: `scripts/video/build_engagement_trap_v12.py`; final audio/remux: `scripts/video/build_engagement_trap_v13.py`. QA: corresponding `qa_engagement_trap_v12.py` and `qa_engagement_trap_v13.py`.
- `edit-manifest.json` records every source/output span, boundary, protected asset hash and candidate hash.
- v11 was an internal intermediate. v12 corrects premature overlay entrances and ends the borrowed follow-up footage before its subsequent reaction scene. No narration or runtime changed between those versions. v13 stream-copies v12’s exact video packets and makes the recorded room tone continuous across the audio joins; the sample jump falls from 80 to 4 PCM counts. There is no additional video encode.

## Verification and limitations

See `qa.json`, `join-transcripts.json`, `join-sample-check.json`, the encoded frames and transition strips for results. The review's final verification addendum records the completed encoded-file checks.

Continuous whole-file viewing and audio listening were not available in this session. The three joins above require listening review. No formal narration KEEP or ship-ready status is claimed.

Pre-existing narration limitation retained: the slope formula is spoken, but the definition of slope is still only displayed rather than fully explained aloud. No usable donor is available. This narrow repair does not invent one or replace the narrator. The course boards and lesson copy remain unchanged.

## Completed verification

- Full v12 decode: 7,832 frames, exactly the planned 4:21.07. v13’s video packet hash is identical, so the decoded picture checks and transition evidence apply unchanged.
- Transition guard: **17/17 pass**. All boundary strips inspected; no stale intermediate scenes seen. The inherited Notebook fade-ins remain where appropriate.
- Encoded frames across the whole picture timeline and full-resolution replacement states inspected. Canonical final frame retained.
- Audio decoding matches planned PCM with correlation above **0.99998** for every retained span. All unaffected PCM is bit-identical before AAC encoding, apart from the deliberate five-millisecond seam fades.
- Changed wording checked by transcription; no remaining compulsory rejection, absolute-revenue clause, or rollout assertion in the edited spans.
- Protected live video, canonical boards and lesson Markdown hashes unchanged.
- Final SHA-256: `e53a9faa4e1fa1026d780f8846bc917c04f4456d3f444a4c1dfede1b2b3db044`.
- Visual QA evidence is retained in `../engagement-trap-build-2026-09-29-v12/`; final audio and identity evidence live here.

**Ready for owner review; not a ship-ready sign-off.** Listen at **2:31**, **2:44**, and **3:34** for cadence and clean word edges. Continuous whole-file playback/listening and the pre-existing spoken slope-definition gap remain as noted above.

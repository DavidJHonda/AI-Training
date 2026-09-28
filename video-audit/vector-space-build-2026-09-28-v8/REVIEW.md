# Vector Space v8 — map bridge and shorter drink explanation

[Review candidate](/Users/davidobrien/Developer/AI-Training/Prompts/vector-space-v8.mp4): **3:25.13**, 6,154 frames, 1280 × 720 at 30 fps. This narrow revision is 17.70 seconds shorter than v7. Live and v7 remain unchanged; publication is not part of this task.

## Changes requested

**Map transition found in Roll 2, 0:32.64–0:35.60:** “To understand how this works, we can look at a standard geographic map.” Roll 1 and Roll 3 move directly into the map description. V8 inserts Roll 2's complete sentence after “That's the idea behind vector space.” The city board arrives at 0:31.67, and the added sentence is transcribed at 0:32.14–0:35.10. The later latitude/longitude-to-seven-dimensions connection remains.

**Removed the three full drink vectors**, formerly v7 2:01.33–2:16.93. The neighborhood explanation now flows directly into the mystery-drink introduction.

**Removed the mystery drink's full-vector readout**, formerly v7 2:20.37–2:26.10. This follows the stated interpretation of the user's second cut: keep the introduction and the explanation of what differs. V8 retains “The first six scores match Pepsi exactly,” the citrus values 9 versus 10 versus 1, and the gaps of 1 and 8.

**Restored the live-style neighborhood presentation:** larger complete-board framing and rounded outlines around the soft-drinks and hot-drinks groups. The mystery board uses the same larger framing, then highlights the matching rows and citrus comparison. No complete row is read aloud. Canonical JPGs remain untouched.

| Affected board | Treatment | Output span |
| --- | --- | --- |
| Three Cities, Two Coordinates Each | Complete unmarked map during new bridge; existing city highlights and framing retained | 0:31.67–0:54.67 |
| A Map of Drink Similarities | Full board; rounded blue soft-drinks group, then purple hot-drinks group; restrained complete-board push matching live treatment | 1:46.23–2:04.97 |
| Use the Map to Find the Closest Drink | Full board; introduction, matching Pepsi/mystery rows, citrus 9/10, citrus 9/1, takeaway banner | 2:04.97–2:26.23 |

No pauses were added. Complete sentences are joined in low-level gaps with the existing 4 ms ramps. Roll 2 is level-matched by +0.1302 dB; the existing Roll 1 adjustment remains −0.8325 dB. Exact source/output intervals and protected source hashes are recorded in `edit-manifest.json`.

## Verification and listening review

Full encoded decode passed: 6,154 frames, correct dimensions and frame rate. All 19 declared boundaries passed the automated transition guard. Every-frame strips for the five affected picture/audio boundaries were inspected, along with fresh whole-video contact sheets, changed board states, and the literal final frame. No stray frames were observed in those checks. Other boundary strips are retained but were not individually re-inspected for this narrow revision.

Fresh full-file ASR confirms the inserted map sentence, removal of both full-vector readouts, retained neighborhood explanation, correct citrus values/gaps, and intact closing lines. The transcript is machine-generated and does not certify pronunciation or cadence. Encoded audio has no sample clipping; peak is approximately −1.38 dBFS and AAC/reference SNR is 44.66 dB. Nine sampled native ring states on the changed drink boards measure the specified 4 px at their straight sides. All three raw sources, live video, lesson Markdown, and seven canonical JPGs pass their protected-hash checks. V7's hash is also unchanged.

**Direct listening and continuous real-time playback were not performed.** Voice continuity at the new Roll 2 graft and shortened drink joins still needs listening review. Short contextual previews:

- [Map transition, candidate 0:27–0:42](/Users/davidobrien/Developer/AI-Training/video-audit/vector-space-build-2026-09-28-v8/audition/map-transition.mp4)
- [Shortened drink section, candidate 1:46–2:27](/Users/davidobrien/Developer/AI-Training/video-audit/vector-space-build-2026-09-28-v8/audition/shortened-drinks.mp4)
- [Complete encoded transcript](/Users/davidobrien/Developer/AI-Training/video-audit/vector-space-build-2026-09-28-v8/transcript.txt)

The drink-board run is reduced from 94.4 to 73.07 seconds. Remaining boards over 20 seconds: cities 23.0 s, taste 33.07 s, mystery 21.27 s, context 21.53 s. Existing teaching schematics and previously accepted paraphrases remain. No unrelated narration or artwork redesign was undertaken.

Notebook drawing spans are the meaning-neighborhood illustration at 0:23.23–0:31.67 and 2:26.23–2:39.37, the calculated-gap drawing at 1:09.67–1:13.17, and the IT/cat ambiguity drawing at 2:39.37–2:49.20. Other visual treatment follows v7, apart from the affected boards above.

Candidate SHA-256: `a9036b7095f6b21866bec03dde40d72dd9c599d4c065eb669141d673f604af77`.

Build: `scripts/video/build_vector_space_v8.py` (refuses to overwrite an existing candidate; reuses the v7 audit's protected drawing excerpts). QA: `.video-venv/bin/python scripts/video/qa_vector_space_v6.py --version 8`. Evidence: `qa.json`, `edit-manifest.json`, `transcript.json`, `changed-ring-verification.json`, `changed-join-gaps.json`, `guard/`, `changed-boundaries-*.jpg`, `encoded/`, and `encoded-sheet-*.jpg`.

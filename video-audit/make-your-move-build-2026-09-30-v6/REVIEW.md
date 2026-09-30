# Make Your Move v6 — review build

Built September 30, 2026, following David's “Build it please” approval of the preceding evaluation. Candidate: [make-your-move-v6.mp4](../../Prompts/make-your-move-v6.mp4), **4:54.17**, 8,825 frames at 30 fps, 1280×720 H.264/AAC. SHA-256: `3162a39fa46d8fe2bca309a3af0bb905c34db439b111e22791a72a8aeb4949bd`.

**Built for review; not shipped.** Technical and transcript checks pass. Listening and continuous motion-with-sound review remain outstanding. The canonical MP4, lesson, and board assets retain their original hashes. No website entry, tracker, commit, or deployment was changed.

## Changes

- Rebuilt both career boards from their current canonical JPGs, with a complete fixed full view, legible headings, and the renderer's current 4-pixel outline setting. Each career progresses from the whole card to “AI may help” and then “People still own.” Card-specific purple, blue, and teal accents are preserved.
- Added four purpose-generated photographic cutaways with restrained 2.5% pushes. Their placement reduces the longest uninterrupted career-board run from 56.5 seconds to **17.53 seconds**. The longest retained board run elsewhere remains approximately 19.5 seconds.
- Removed the repeated opening extension: “Theory and practice can only take you so far. It is time to step onto the court and put those skills to work in the real world.” Source **28.4667–35.8000** removed, saving **7.333 seconds**. The skills graphic's final source frame at 25.00 is held through the preceding complete sentence, removing the “YOUR NEXT MOVE” intertitle as well. New join: **0:28.47**.
- Replaced “Yet the human tasks remain untouched” with the same narrator's **“But humans still own the core responsibilities.”** Donor is source **61.60–64.70**; target is source **79.10–82.20**, identical duration. New output span **1:11.77–1:14.87**. This now leads into “knowing the individual student, building motivation…” Both ends use 8 ms crossfades within quiet intervals; speech was not stretched.
- Applied **−1.3 dB** uniform gain to restore headroom. Encoded output measures **−18.4 LUFS integrated**, **−1.2 dBTP**, with **zero decoded samples at or above full scale**. No compressor or limiter changed the delivery.
- Preserved the later skills/action card zooms, supporting Notebook scenes, natural section gaps, and existing close. No added pauses.

## Career cutaways

| Asset | Output time | Teaching purpose |
|---|---|---|
| Patient care | 0:57.77–1:03.87 | Physician explains choices to a student patient and parent; human context and care. |
| Teacher judgment | 1:16.47–1:22.27 | Teacher responds to an individual student, supporting motivation and adaptation. |
| Electrical diagnosis | 1:53.17–1:56.87 | Instructor and apprentice inspect a disconnected component against a diagram. Placed under physical diagnosis, after the “live wires” wording. |
| Design judgment | 2:08.17–2:12.67 | Student designer compares alternatives and chooses a direction with audience and taste in mind. |

All four images use the built-in ImageGen tool. Final assets and exact prompts are retained in [the asset folder](../../scripts/video/assets/make-your-move-cutaways-2026-09-30/) and [prompts.json](../../scripts/video/assets/make-your-move-cutaways-2026-09-30/prompts.json). No unknown-source stock imagery was added.

## Board treatment and retained scenes

| Board | Output topic span | Treatment / breaks |
|---|---|---|
| How AI Might Change Careers (1 of 2) | 0:42.50–1:38.93 | Full board. Doctor → Teacher → Lawyer, each whole card → AI assistance → human ownership. Patient and teacher cutaways as above. First unmarked full view lasts 3 seconds. |
| How AI Might Change Careers (2 of 2) | 1:43.07–2:30.20 | Full board. Electrician → Graphic Designer → Entrepreneur, with the same section progression. Electrical/design cutaways as above. First item is named at arrival: board appears unmarked for its first frame, then rings in the full view under Edit Spec 3's immediate-first-item exception. There is no dive. |
| Four Skills to Build | approximately 2:39.6–3:34.1 | Retained full view and complete-card zooms, including listening/explanation and creative-thinking supporting sequences. |
| Moves to Make | approximately 3:44.5–4:38.1 | Retained complete-card zooms, conversation, keyboard/notes, and donation-drive cutaways. |
| Closing board | approximately 4:38.1–4:54.17 | Existing unmarked hold/push/settled close preserved. Literal last decoded frame shows the closing board. |

Other retained supporting scenes: opening basketball/skills sequence 0:00–0:28.47; career/task graphics 0:28.47–0:42.50; strategy-board drawing 1:38.93–1:43.07; clipboard/team meeting approximately 2:30.2–2:39.6; listening/explanation approximately 2:45.3–2:52.3; creative thinking approximately 3:10.5–3:20.0; city/foundation approximately 3:34.1–3:44.5; conversation approximately 3:52.5–3:58.7; keyboard/notes approximately 4:07.5–4:12.8; donation drive approximately 4:32.2–4:38.1. These are existing scenes carried forward with the opening's time shift.

## Verification

- Full encoded decode: **8,825 frames**, constant 30 fps, continuous frame timestamps, no decode errors, no detected black intervals.
- Transition guard: **33 declared boundaries, 0 failures**. Inspected before/at/after strips for every declared boundary; no stale source graphic appears at an edited transition.
- Inspected all career ring states in sheets and selected states at full output resolution; complete relevant sections, readable text, uncropped board headings. Inspected generated assets and their encoded transition frames. The changed career boards have no camera movement; photo pushes retain the important faces, hands, and objects.
- Encoded audio compared with assembled PCM: correlation **0.9999879**, **46.06 dB** signal-to-error ratio. This verifies the intended assembly through AAC encoding, not subjective seam quality.
- Fresh transcription of the actual encoded opening join confirms “…going to do with them. When thinking about how AI will change careers…”; the deleted extension is absent.
- Fresh transcription of the actual encoded graft confirms “But humans still own the core responsibilities, knowing the individual student…”; “untouched” is absent.
- Fresh encoded close transcription confirms both required lines: “You know how to be smarter than the tool” and “Keep learning. Keep building. Make your move.”
- Final quiet tail begins at **4:49.60** and lasts approximately **4.58 seconds**. No added silence was introduced. Silence detection reports a contiguous below−40 dB interval of **28.378–28.594** at the opening join and **71.486–71.966** before the replacement clause; word spacing is longer where low-level breath/release sounds remain.

Teaching assessment remains **KEEP on transcript evidence**: all essential points from the evaluation are retained, with the specific “untouched” overstatement removed. The other previously noted qualifications (“AI can/AI excels,” “physical and trades work,” “live wires,” and compressed example lists) remain. They were not silently expanded into additional narration edits.

**Still to listen to:** the opening transition around **0:26–0:31** and teacher replacement around **1:10–1:17**, plus a continuous playback for delivery and motion rhythm. No audio was directly auditioned by the agent. This candidate has not completed the whole-file shipping checklist and is not represented as ready to ship.

## Reproduction and provenance

The source is the retained `video-audit/make-your-move-note-cut/make-your-move-without-note.mp4`, hash `d2aeeba98a33c91657fe75368d46502671af1c47a35e51f2e32cd5b663951d60`, identical to the evaluated canonical MP4. The raw generation no longer exists in the available workspace. This build therefore uses one final encode from that surviving finished source, preserving unchanged source frames as planar YUV to avoid an extra RGB color conversion. Audio is re-encoded because of the approved trim, clause replacement, and level adjustment.

Build: `.video-venv/bin/python scripts/video/build_make_your_move_v6.py`.
QA: `.video-venv/bin/python scripts/video/qa_make_your_move_v6.py`.

Details: `edit-manifest.json`, `source-words.json`, `donor-words.json`, `transitions/transition-guard.json`, and `encoded-qa/verification.json`. Source identity, exact source/output frames, image hashes, ring geometry, and protected-file hashes are recorded in the manifest. Do not rerun over the existing candidate; use a new version for revisions.

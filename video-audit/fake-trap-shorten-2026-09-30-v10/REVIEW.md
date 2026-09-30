# Fake Trap v10 — approved shortening and lesson copy edit

Status: **shipped locally; queued for batch deployment**. Owner approved shipping after the disclosed listening limitation. Local commit `68a802e986d9f3703a75eff1f242771dd595d7b6`. No push or deployment performed.

## Scope and authorization

David approved the proposed cuts: remove the repeated school-closure walkthrough while retaining the distinction that reposts are not independent confirmation; remove the eyes/lie-detector restatement; remove the targeted-person reassurance. He also explicitly requested deleting “You did nothing wrong by being targeted.” from the lesson page.

The page paragraph, corresponding Markdown sentence, and generation prompt's required-verbatim entry are removed. The Fake Trap upload bundle is synchronized and its check passes. Other lesson prose is unchanged. The local page and canonical video are installed and committed; the public site awaits separate batch deployment.

This is a narrow shortening pass, retaining v8's approved visual repairs. The raw generations are unavailable. The build uses frozen v6, SHA-256 `8fffe6bdf9de2fc9e8b6736a18b2235f5b54e6992ec8fd1873a3bdd7195ab24e`, and v8's retained lossless donor clips and PNG board states. It reconstructs those repairs before a single final H.264 encode; it does not re-encode the v8 MP4. AAC is encoded once because the approved cuts change narration.

Candidate: `Prompts/fake-trap-v10.mp4`, **4:15.167**, 7,655 frames at 30 fps, 1280×720. Removed **52.833 seconds** from 5:08. Candidate SHA-256: `dcd676e967cd72c4a63aec8d42a047c7ac99e8529586786340bbadbffab178b5`.

## Cuts and joins

Intervals are half-open; picture and sound remove equal durations. Audio cuts use measured quiet shoulders. Small picture offsets land on existing scene changes and preserve the complete standard close.

| Removed source audio | Removed source picture frames | Content | New audio join |
|---|---|---|---|
| 3:09.300–3:38.567 | 5679–6557 | Repeated school-closure application before “Remember, another random account…” | 3:09.300 |
| 3:44.300–3:56.200 | 6738–7095 | Remaining walkthrough after “…independent confirmation.” | 3:15.033 |
| 4:17.000–4:26.000 | 7718–7988 | Eyes-still-work / lie-detector restatement | 3:35.833 |
| 4:56.400–4:59.067 | 8886–8966 | “You did nothing wrong by being targeted.” | 4:06.233 |

The three checks now lead into the repost distinction and then the verification rule and saved-number callback. “Verify information somewhere the sender does not control” arrives around 3:18, approximately 41 seconds earlier. The original example already teaches official-source checking and the unverified verdict. Practical support instructions, the under-18 image rule, Take It Down, and CyberTipline remain.

A three-frame picture hold repeats source frame 6734 over frames 6735–6737, eliminating a flash from the deleted walkthrough caught in v9. The corrected file is v10; v9 is superseded. No new pause, fade, speech, speed change, or illustration was added. Original quiet shoulders supply the gaps. The standard close retains all 274 frames: 48-frame hold, 150-frame push to 1.2×, 76-frame settle, starting at output frame 7381 (4:06.033).

## Board and camera treatment

| Board | Treatment |
|---|---|
| The Same Clip. Two Eras. | Preserve v8's camera, rings, principal-phone cutaway, and unmarked return; 17.10 s and 20.00 s runs. |
| Why Some Fakes Aren't Friendly | Preserve the accepted four-card walk, 21.57 s; longest unbroken board run. |
| Check the Source, Not the Pixels | Preserve the 9.70 s span. |
| Move the Test Off the Image | Preserve full compact opening, 4 px Source/Context/Corroboration rings, context-date cutaway, and cleared summary. Exit seven frames earlier at the new splice; runs 8.93 s and 16.50 s. |
| Standard close | Preserve the entire original hold/push/settle, retimed by the cuts. |

The source/callback and victim-support Notebook scenes remain. The repost diagram retains its reveal. There are no newly introduced supporting illustrations. v8's principal-phone and context-date donor animations remain at 1×.

## Verification and limits

- Independently decoded 7,655 frames, 30 fps, 1280×720; duration 255.167 s.
- All four transition guards pass. Every frame in all four boundary strips was visually inspected; v10 removes the three-frame flash found in v9. The new verification diagram retains its original fade-in reveal.
- 604 mapped picture samples, including every one of the 274 closing frames, match the intended v8 states (allowing the declared three-frame hold). Comparison at 320×180: mean absolute RGB difference 0.028/255, maximum 0.389/255. No ordering or timing discrepancy found.
- Encoded audio correlates 0.99977 with the exact approved PCM cut assembly. The four 10 ms cut windows measure −66.8, −64.7, −65.6, and −69.5 dBFS. Contiguous quiet gaps below −42 dBFS measure 0.53, 0.52, 0.56, and 0.41 seconds. No new silence was inserted.
- Fresh whole-file ASR confirms the deleted passages are absent, the repost distinction and verification rule remain, and the complete safety guidance and two-line close survive. v10's encoded AAC payload is identical to transcribed v9 (SHA-256 `98b94a77901b810a042ecd02371cf914116ee2e403d269be14189f16270fc4f4`); transcript provenance is recorded. ASR's “reported” and “NC mecs” are not established narration errors.
- The lesson page's inline JavaScript parses, `git diff --check` passes, and Fake Trap's synchronized upload bundle passes its source check. The deleted sentence is absent from the page, Markdown, prompt, and generated upload text.
- Build-time hashes confirm the installed video, canonical boards, frozen source, and edited page were unchanged during rendering.

Evidence: `verification.json`, `encoded-silence-gaps.json`, `audio-transcript-provenance.json`, `qa.log`, `transitions/`, `transcript.txt`, and `manifest.json`. Context WAV clips for the four joins are `join-1.wav` through `join-4.wav`. Build and verification entry points: `scripts/video/build_fake_trap_v10.py` and `scripts/video/qa_fake_trap_v10.py` (reuse the v9 assembly/check functions).

The owner explicitly authorized local shipping after the listening limitation was disclosed. This authorization is recorded separately from the checks; no whole-file listening certification is claimed. No real-time audiovisual playback or listening is claimed; waveform measurements, frame inspection, fresh ASR, and source correspondence do not substitute for audition. Listen especially at 3:09.3, 3:15.0, 3:35.8, and 4:06.2. The previously accepted narration paraphrases and older outline treatments outside v8's repair remain. The Video Tracker was not accessed or updated.

## Local release — 2026-09-30

Installed `course-assets/fake-trap/fake-trap.mp4`; SHA-256 `dcd676e967cd72c4a63aec8d42a047c7ac99e8529586786340bbadbffab178b5`. Cache key `20260930ship-faketrap-v10`, display `4 min`, actual 4:15.167. Exact approved hash and full FFmpeg audio/video decode verified; page JavaScript and source-bundle checks passed. Commit `68a802e986d9f3703a75eff1f242771dd595d7b6` contains only the video, its index entry/page deletion, Markdown deletion, and prompt deletion. Build/audit records remain local. Eight regenerable join WAV clips were removed after commit; the QA scripts can recreate them. No push, Vercel action, or public verification was performed.

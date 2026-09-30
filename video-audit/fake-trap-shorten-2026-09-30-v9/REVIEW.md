# Fake Trap v9 — approved shortening and lesson copy edit

Status: superseded by v10. Frame inspection caught three frames of a deleted illustration before join two. Do not use v9; v10 holds the outgoing repost diagram through those three frames without changing narration or duration.

## Scope and authorization

David approved the proposed cuts: remove the repeated school-closure walkthrough while retaining the distinction that reposts are not independent confirmation; remove the eyes/lie-detector restatement; remove the targeted-person reassurance. He also explicitly requested deleting “You did nothing wrong by being targeted.” from the lesson page.

The page paragraph, corresponding Markdown sentence, and generation prompt's required-verbatim entry are removed. The Fake Trap upload bundle is synchronized and its check passes. Other lesson prose is unchanged. The public page and installed video are not changed by this local work.

This is a narrow shortening pass, retaining v8's approved visual repairs. The raw generations are unavailable. The build uses frozen v6, SHA-256 `8fffe6bdf9de2fc9e8b6736a18b2235f5b54e6992ec8fd1873a3bdd7195ab24e`, and v8's retained lossless donor clips and PNG board states. It reconstructs those repairs before a single final H.264 encode; it does not re-encode the v8 MP4. AAC is encoded once because the approved cuts change narration.

Candidate: `Prompts/fake-trap-v9.mp4`, **4:15.167**, 7,655 frames at 30 fps, 1280×720. Removed **52.833 seconds** from 5:08. Candidate SHA-256: `cb5d90d0df59e23525a1720896365cd70a423a8be5e30bd4e6dcfb10ed4400e7`.

## Cuts and joins

Intervals are half-open; picture and sound remove equal durations. Audio cuts use measured quiet shoulders. Small picture offsets land on existing scene changes and preserve the complete standard close.

| Removed source audio | Removed source picture frames | Content | New audio join |
|---|---|---|---|
| 3:09.300–3:38.567 | 5679–6557 | Repeated school-closure application before “Remember, another random account…” | 3:09.300 |
| 3:44.300–3:56.200 | 6738–7095 | Remaining walkthrough after “…independent confirmation.” | 3:15.033 |
| 4:17.000–4:26.000 | 7718–7988 | Eyes-still-work / lie-detector restatement | 3:35.833 |
| 4:56.400–4:59.067 | 8886–8966 | “You did nothing wrong by being targeted.” | 4:06.233 |

The three checks now lead into the repost distinction and then the verification rule and saved-number callback. “Verify information somewhere the sender does not control” arrives around 3:18, approximately 41 seconds earlier. The original example already teaches official-source checking and the unverified verdict. Practical support instructions, the under-18 image rule, Take It Down, and CyberTipline remain.

No new pause, fade, speech, speed change, or illustration was added. Original quiet shoulders supply the gaps. The standard close retains all 274 frames: 48-frame hold, 150-frame push to 1.2×, 76-frame settle, starting at output frame 7381 (4:06.033).

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

Pending encoded-candidate checks are recorded separately in `verification.json`, `qa.log`, `transitions/`, and the fresh transcript. Context WAV clips for the four joins are `join-1.wav` through `join-4.wav`.

This candidate is for review, not a whole-file shipping certification. No real-time audiovisual playback or listening is claimed; waveform measurements, frame inspection, fresh ASR, and source correspondence do not substitute for audition. Listen especially at 3:09.3, 3:15.0, 3:35.8, and 4:06.2. The previously accepted narration paraphrases and older outline treatments outside v8's repair remain. The Video Tracker was not accessed or updated.

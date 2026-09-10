# Layers owner revisions — review v4

**2:39 (158.9 seconds)**. Candidate: `videos/layers-v4.mp4`. Live video unchanged.

- **Highlight first board title when spoken**: Title outline 0:10.33–0:12.90; purple, no text shading.
- **Replace strange graphic at 0:30**: Original Notebook animation from Layers 2: horse sentence changes from an incorrect parse to horse/fell, shown 0:29.30–0:34.77.
- **Replace repeated strange graphic at 1:10**: Generated Notebook-style illustration of a magnifying glass examining IT in a book, shown 1:10.03–1:17.90 with restrained push.
- **Remove Test Sentence**: Removed source 1 85.5–86.7333; sentence now starts directly.
- **Explain Repeat after layers 1 and 2**: Extended the existing source 2 narration through its complete sentence ending building over successive layers. Repeat outline 1:35.63–1:37.53, then Result. No synthetic voice used; box name itself is not spoken.
- **Fix strange This at 1:46**: Removed entire This naturally raises a question lead-in. New section starts Exactly how many layers are required in a real-world AI model? at about 1:50.5.
- **Remove added pause near 2:20**: Depth and cost narration now use one continuous source span, preserving the original natural breath and removing the inserted one-second pause.

All 19 transition checks pass; all 19 adjacent-frame strips and four full-video contact sheets visually reviewed. New title and Repeat outlines inspected at full-frame size. Full final narration transcript reviewed: sentence starts directly, repeated-layer explanation complete, awkward lead-in gone. All source and live-file protection hashes pass.

Audio validation uses transcription, word-onset mapping, waveform and measured silence checks, not a claimed full real-time listen.

The new video-only illustration was made with built-in image_gen. Saved asset: `video-audit/layers-owner-revisions-2026-09-10/tracing-one-word.png`. Full prompt: `image-prompt.txt` alongside this report. Its brief is an editorial ink-and-watercolor book illustration with a magnifying glass over IT, without faces, a course title, or a banner.

Build: `scripts/video/build_layers_v4.py`. QA: `scripts/video/qa_layers_v4.py`. Full timeline and source hashes: `edit-manifest.json`. Final transcript: `final-transcript/layers-v4.txt`.

# What Is AI? v17 — remove the course-focus sentence

User authorized removing “This course focuses on generative AI” from v16 at approximately 2:32–2:35. This narrow edit removes the entire corresponding board-return span: **v16 2:32.000–2:35.100**, frames 4560–4653, end-exclusive. Ending at the actual 2:35.100 scene boundary avoids leaving three stray frames of the Types board. The everyday section now leads directly into “You've got a tool that can help. Start with something you want to do.”

Candidate: `Prompts/what-is-ai-v17.mp4`, 2:40.200, 4,806 frames at 30 fps, 1280 × 720. Review candidate only; not installed or published. Written lesson content is outside this video-only edit.

The existing v16 ordering, illustrations, highlights, camera framing, pauses, and closing are preserved. No new board treatment or pause duration is introduced. The closing begins at output **2:32.000**. The standard closing motion remains unchanged. Existing one-second hold at the end of Everyday AI remains.

Reassembled from the same retained source files and v14 PCM as v16, omitting the focus segment, so no extra v16-to-v17 video encoding generation is added. At the newly noncontiguous audio boundary, 5 ms ramps fall within measured silence. Source/course assets and v16 are protected by hash. Exact source/output ranges and source identities are in `edit-manifest.json`.

Verification results are recorded in `qa.json` and `transitions/`. A targeted transcript of the encoded ending checks that the removed line is absent and both closing lines survive. Direct listening is not available and is not claimed; the join to audition is **2:32**. This narrow edit is not a new whole-file shipping certification.

## Final verification

- 4,806 decoded frames, continuous 30 fps timestamps, 2:40.200 runtime.
- All 11 transition gates passed; the newly joined boundary strip at 2:32 was inspected and goes directly from Everyday AI to the closing, with no leftover Types frames.
- Every encoded frame matches its declared source/render within compression tolerance; audio correlation to intended PCM is 0.999985.
- Fresh ending transcript confirms the focus sentence is absent and both closing lines remain.
- The retained quiet gap across the new join measures 150.663–152.267 seconds (1.604 seconds). No pause was added.
- Source, course files, and v16 hashes remain unchanged. Direct listening remains unperformed.

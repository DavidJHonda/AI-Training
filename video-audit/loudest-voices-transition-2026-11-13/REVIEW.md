# Loudest Voices transition review

Candidate in `Prompts/loudest-voices-v15.mp4`, SHA-256 `d753fd5e9b012797d00ad935f3add73b11e218621e60f1aeb3600762438d6e6a`. Runtime 3:59.800 at 30 fps. Built from v14, which includes the 2:12 pause. Saved for review.

The transition uses the five approved sentences in the updated lesson. The new narrator is Kokoro v1.0 af_heart, rendered locally. The original habits image holds into the transition. The complete In Your Hands board first appears on frame 4453 (2:28.433), at “What’s actually in your hands?” The source walkthrough resumes after “That’s where to put your energy.”

Decoded all 7,194 frames. Checked every splice with transition_guard.py and inspected the strips. Verified identical H.264 and AAC packet payloads outside the edited ranges, including the previously approved one-second hold. Fresh transcription from the candidate matches the approved speech, with “What’s” at 2:28.44. Audio timing and levels were checked programmatically. Direct listening remains for review.

## Local release

David approved shipping v15. Installed and committed the reviewed candidate on main at `bcd17e524739b0f43b7e005077514d6ef8f42d1b`. The installed video fully decoded and matched the approved bytes. Asset integrity, player layout and lesson prep sync passed. The committed player uses cache key `20261113ship15`. Queued for batch deployment.

# Does School Matter? — working v12

Completed the approved shortened lesson using the continuous ending from reroll 3. Runtime: **141.700 seconds (2:22 rounded), 4,251 frames at 30 fps**. Review candidate only; the installed video and lesson files are unchanged.

## Ending

- **2:07.800:** roll-3 audio begins in silence while the current two-card board remains on screen.
- **2:08.133:** fixed 4px outline emphasizes the banner as the takeaway begins.
- **2:11.800:** cut in the natural speech gap to the current canonical closing image. Standard 48-frame hold, 150-frame push to 1.2×, then 99-frame hold.
- All three required sentences appear verbatim in the fresh complete output transcript. Roll 3 has no internal narration cuts.
- Donor gain +2.7 dB; donor PCM peak approximately 0.966. The existing body PCM matches v11 exactly, including its prior encoding-related peaks and PCM conversion. No new pause inserted.

## Verification

- Decoded every output frame and compared it with its planned source/artwork; maximum mean absolute pixel error 3.09, consistent with encoding.
- Frame count, 30fps timing and continuous timestamps pass.
- Encoded audio correlation with planned PCM: 0.999989.
- Transition guard passes all 12 boundaries. Inspected all-frame strips around the three new ending boundaries and encoded ending states; no unwanted inserted frame or old outro appears.
- Fresh small.en transcript read in full; all required ending words intact. Join silence measures 0.527 seconds between the body and new takeaway. The closing image changes during the 0.890-second pause before “The opportunity…”
- Protected source, installed video, lesson, index and canonical artwork hashes unchanged.

No direct listening audition was available. Please listen from 2:03 through the new ending to assess narrator continuity, tone and the join at 2:08.

[Three-roll comparison](../does-school-matter-ending-2026-10-22/REVIEW.md) · [Fresh transcript](transcripts/does-school-matter-v12.txt) · [Technical QA](qa.json) · [Edit manifest](edit-manifest.json)

from pathlib import Path
import hashlib,json
import numpy as np

p=Path(__file__).resolve().parent;old=p.with_name('big-downside-build-2026-11-17-v12')
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
m=json.loads((p/'edit-manifest.json').read_text());q=json.loads((p/'encoded-qa.json').read_text())
t=json.loads((p/'transitions/transition-guard.json').read_text());r=json.loads((p/'ring-qa/ring-stroke.json').read_text())
assert t['pass'] and q['decoded_frames']==8480 and all(q['protected_files_unchanged'].values())
assert h(p/'encoded-audio.wav')==h(old/'encoded-audio.wav'),'Audio changed; fresh transcript review required'
identity=json.loads((p/'audio-identity-to-v12.json').read_text())
identity.update(encoded_pcm_identical=True,encoded_pcm_sha256=h(p/'encoded-audio.wav'),
 reviewed_transcript=str(old/'render-transcript/big-downside-v12.txt'))
(p/'audio-identity-to-v12.json').write_text(json.dumps(identity,indent=2)+'\n')
board_runs=[x for x in m['visual_runs'] if x['visual'].startswith('board-')]
samples=[x for x in r['rows'] if any(b['start_frame']/30<=x['t']<b['end_frame']/30 for b in board_runs)]
stats=dict(sample_count=len(samples),median=float(np.median([x['stroke'] for x in samples])),
 minimum=min(x['stroke'] for x in samples),maximum=max(x['stroke'] for x in samples))
(p/'course-board-ring-summary.json').write_text(json.dumps(stats,indent=2)+'\n')
s=(old/'REVIEW.md').read_text();start=s.index('## Narration changes');end=s.index('## Verification')
body=s[start:end]
head=f'''# Big Downside — revised video from uploaded version 5

Built 2026-11-17 under the approved narration and visual plan. **Current review candidate: `Prompts/big-downside-v13.mp4`.**

Duration **4:42.667**, 8,480 frames, 1280×720 at 30 fps, H.264/AAC, {m['size_bytes']:,} bytes. SHA-256: `{m['render_sha256']}`.

**Ready for owner review, with direct listening and an end-to-end motion watch still outstanding.** The build and technical checks are complete; no shipping certification is claimed. Meaning-preserving paraphrases pass. All requested narration repairs and visual updates are implemented. Version 13 supersedes v12 solely to use the shared course-board outline renderer; its audio is exactly identical after decoding.

'''
verification=f'''## Verification of the delivered v13 file

- All 8,480 frames decode. Video and audio both measure 282.667 seconds.
- Audio is byte-identical, after PCM decoding, to v12's completely reviewed 695-word exported-file transcript. All essential teaching and all three replacement passages are present. Transcript evidence: `../big-downside-build-2026-11-17-v12/render-transcript/big-downside-v12.txt`; identity evidence: `audio-identity-to-v12.json`. No transcription result is presented as direct listening.
- Encoded audio correlation to the assembly is {q['audio_correlation_to_assembly']:.8f}; peak {q['audio_peak_db']:.3f} dBFS, with {q['audio_clipped_samples']} clipped samples. All twelve seams fall in quiet gaps, with 5 ms room-tone fades. Signal checks do not certify how the voices sound together.
- Transition guard passes all {len(t['boundaries'])} edited boundaries. Every frame in the ±12-frame boundary strips and the complete four-second-sampled contact sheets were visually inspected on this export. No stale-picture island was found.
- Course-board outlines use the same `ken_burns_path.draw_ring` and `ring_px(720)` as the established course renderer. The encoded board-only measurement has {stats['sample_count']} samples, median {stats['median']:.1f} px, range {stats['minimum']:.1f}–{stats['maximum']:.1f} px at the tool's solid-color threshold. This threshold varies with anti-aliasing and compression; the requested drawing width is a fixed 4 px. Unrelated colored shapes in supporting scenes are excluded from this summary. All ten ring targets also passed a short encoded calibration before the full build.
- Current canonical boards remain complete and legible. Highlights follow the named cards and callback banner. The canonical closing message is the literal final frame, with the standard 48/150/120-frame hold/push/settled timing.
- Source videos, canonical board JPGs, and lesson Markdown hashes are unchanged. No installation or publishing occurred.

## Listening handoff

`narration-join-reel.mp4` is a **42-second local reel** containing three seconds before and four seconds after each cross-roll boundary. Each excerpt labels its timestamp in the full candidate. `audio-joins/` holds all twelve edit seams individually.

The six donor joins are at **0:54.067, 1:16.067, 3:02.400, 3:17.533, 4:20.833, and 4:32.067**. They still need direct listening for voice continuity, cadence, pronunciation, and natural pacing. The complete candidate also needs an end-to-end watch/listen before it can be called ready to ship.

## Reproduction

Builder: `scripts/video/build_big_downside_v13.py`, using the v12 timeline/visual renderer plus the shared course ring implementation. `edit-manifest.json` records exact source/output spans, gains, asset hashes, and final hash. `verify_export.py` checks the actual export and makes the six-join reel. Existing numbered candidates are never overwritten.
'''
(p/'REVIEW.md').write_text(head+body+verification)
m['ring_renderer']='ken_burns_path.draw_ring with ring_px(720)'
m['review_status']='Ready for owner review; direct listening and end-to-end motion review outstanding'
m['audio_identical_to_reviewed_v12']=True
(p/'edit-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps(dict(candidate=m['output'],sha256=m['render_sha256'],bytes=m['size_bytes'],rings=stats,audio_identical=True),indent=2))

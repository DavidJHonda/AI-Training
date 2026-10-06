# Vector Space: build the maps in place

Scope: implement the agreed lesson interactions and match their sequence in a visual-only review candidate. The lesson and video use VectorMapFrame and VectorMapDiagram from index.html. The generated preview comes from scripts/video/preview_vector_space.cjs, so there is no separately maintained video drawing.

## Video plan

Source: the installed course-assets/vector-space/vector-space.mp4, identical to the previously approved v11 candidate. Output: Prompts/vector-space-v14.mp4. V12 and v13 are superseded internal exports. The final capture fixes the scene height so caption lengths cannot shift the map; the final encoder reads unchanged footage as YUV directly to avoid the color shift from an unnecessary RGB round trip. Preserve all 6,278 frames at 30 fps, current narration, timing, and other scenes. The current finished video supplies unchanged pictures; those pictures undergo one new encode. Copy the compressed AAC audio without re-encoding. This is a review candidate, not installation or deployment.

| Scene | New treatment | Framing and span |
| --- | --- | --- |
| Add a position to the map | Three known cities stay fixed; reveal the first new position, then its nearest-city outline and connection; repeat for the second. | Complete stationary scene, 0:31.67–1:09.67. First position at 0:59.4, answer at 1:01.6; second at 1:03.0, answer at 1:04.8. |
| Build a map from the numbers | Add Coke, Pepsi, and coffee in turn as the narrator explains their positions. Keep the ratings table in the same scene. | Complete stationary scene, 1:46.23–2:26.23. Coke at 1:49.0, Pepsi at 1:50.3, coffee at 1:55.9. |
| Mystery drink, within the same map | Ratings appear at 2:04.97; place the mystery point at 2:08.0; outline Pepsi and compare the first six values and Citrus at 2:11.8. | Same framing and fixed known points throughout. |
| Watch IT’s position change | Show the starting numbers and IT marker. At 3:05.2, update the numbers and move the marker using the lesson’s actual CSS transition. | Complete stationary scene, 2:53.33–3:14.87. Preserve the source’s sentence introduction before this scene. |

These interactive, code-native diagrams replace the static map-board pairs under the user-approved treatment. The printed lesson shows their completed states. The original JPGs remain on disk for historical builds. No added audio pauses or narration edits.

## Lesson checks

Browser checks cover each reveal, separate city answer steps, mystery ratings before placement, keyboard activation, replay, stable diagram dimensions, 390/350px layouts, reduced motion, completed print states, and runtime errors. Desktop and phone screenshots are in output/vector-space-interactions.

The global design check has the same pre-existing flags as HEAD: two Georgia font literals and five em dashes against a baseline of six. No new design drift. The existing 2048 game overflows at 350px; the new map components do not.

## Verification

The browser checks pass for every reveal, replay, keyboard activation, stable map size, 390/350px map layouts, reduced motion, completed print states, and no runtime errors. Encoded v14 verification passed: 6,278 frames at 30 fps (3:29.27), full-file decode, exact compressed-AAC identity with the installed source, and 12 comparisons of encoded states with the shared lesson captures. Representative encoded before/after and intermediate-motion frames were visually inspected for all three scenes. Unchanged-span sample error is at most 0.313/255, consistent with re-encoding; the earlier RGB color shift is absent. The installed source hash is unchanged.

The audio was not re-auditioned; this pass verifies exact compressed-audio identity and inherits the prior source’s listening limitations. V14 is a review candidate, not a whole-file recertification or an installed release. No commit, push, or deployment.

Reproduce: generate the preview with `node scripts/video/preview_vector_space.cjs`, capture with `scripts/video/capture_vector_space.cjs` (Playwright plus the local server), then run `.video-venv/bin/python scripts/video/build_vector_space_v14.py` and `.video-venv/bin/python scripts/video/qa_vector_space_v14.py`. The builder refuses to overwrite an existing candidate.

## Geographic map revision, October 4

Following review of the interactive preview, replaced the rough city-map polygon with a local, Census-derived US Atlas SVG. The outline now uses an Albers equal-area projection with detailed coastlines and state boundaries. All five point positions use the same projection. The lesson and preview are updated, and the full interaction browser checks pass again at desktop and phone sizes. V14 retains the earlier outline; this appearance revision has not yet been rendered into another video candidate.

#!/usr/bin/env python3
"""Remove the two approved detours, preserving v3's retained original footage."""
import json
import build_flattery_engagement_v3 as previous
from build_flattery_engagement_v3 import ROOT,SOURCES,FPS,SR,SPF,sha,close_frame
base=previous.base
OUT=ROOT/'video-audit/flattery-engagement-trim-v4-2026-11-02'
DEST=ROOT/'Prompts/flattery-engagement-v4.mp4'
NEW_CUTS=[(9790,10700,'Infinite Scroll history/comparison and dependent missing-page-break introduction.'),
 (10866,11267,'Engagement is an engineered outcome … turn occasional product use into a daily habit.')]
base.CUTS=sorted([c for c in base.CUTS if not any(a<=c[0] and c[1]<=b for a,b,_ in NEW_CUTS)]+NEW_CUTS)
base.REPAIRS=[r for r in base.REPAIRS if not any(a<=r['v1_frames'][0] and r['v1_frames'][1]<=b for a,b,_ in NEW_CUTS)]
base.OUT=OUT;base.DEST=DEST

def main():
 OUT.mkdir(exist_ok=True)
 (OUT/'EDIT-PLAN.md').write_text('''# Approved ending trim — v4

Scope: remove the two passages already deleted from the on-page lesson. Preserve all earlier approved cuts and the 1:49 baked-in exception. Build a new review candidate from the original finished Flattery v13 and Engagement v15; do not encode v3 again.

## New narration cuts (v3 timeline)

- 4:17.500–4:45.467: “This design logic traces back to 2006” through “their own invisible version of the missing page break.” Removes the Infinite Scroll history, comparison and dependent introduction.
- 4:51.000–5:04.367: “Engagement is an engineered outcome” through “turn occasional product use into a daily habit.” Removes company-incentives teaching.

Keep unchanged: “When the answer ends, the conversation continues. The system instantly generates a follow-up task.” Then the shared close: “Look for specifics, not approval. Know what you came for. When you have it, choose what happens next.”

The frame boundaries are within measured quiet shoulders. No pauses added, no global gain changes, no new words. Total removal 41.333 seconds; expected runtime 4:34.600.

## Board/camera treatment

| Board/scene | Treatment | Timing |
|---|---|---|
| One Answer. Two Endings. | Preserve the original retained comparison and takeaway framing/highlight. | Continue through the complete flattery-engagement-followup sentence, then cut directly to the original AI-chat illustration. |
| What Infinite Scroll Removed | Remove the entire board, its lead-in and narration. | No retained frames. |
| AI follow-up illustration | Keep the original animation accompanying the two retained sentences. | About 5.53 seconds. |
| Commercial-incentives illustration | Remove with its narration. | No retained frames. |
| Shared closing | Exact current canonical asset and identical v3 motion: 48-frame hold, 150-frame push, settled ending. | Preserve all 347 frames (11.567 seconds). |

All earlier boards, prompt strategies, examples, the baked-in line and the Flattery-to-Engagement transition are unchanged. No on-page edits, source-media replacement, installation, commit or publishing in this build.
''')
 base.main()
 p=OUT/'edit-manifest.json';m=json.loads(p.read_text())
 m.update(scope='Approved narrow ending trim: remove Infinite Scroll and commercial incentives; preserve AI follow-up explanation and shared close.',
  authorization='User approved both on-page deletions, then requested: Now, let’s update the video.',
  previous_candidate=str(previous.DEST),previous_duration_seconds=9478/30,removed_from_previous_seconds=(9478-m['frames'])/30,
  new_v3_cuts=[dict(frames=[7725,8564],seconds=[7725/30,8564/30]),dict(frames=[8730,9131],seconds=[8730/30,9131/30])],
  ending_bridge='When the answer ends, the conversation continues. The system instantly generates a follow-up task.')
 p.write_text(json.dumps(m,indent=2)+'\n')
if __name__=='__main__':main()

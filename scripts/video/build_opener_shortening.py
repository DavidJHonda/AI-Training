#!/usr/bin/env python3
"""Apply approved tighter opener narration from the pristine pre-cut versions.

Reuses blue-board removal in the same encode, rather than stacking another lossy
repair on the approved intermediate candidates. New versions only.
"""
from concurrent.futures import ThreadPoolExecutor
import json
import build_opener_blue_board_cuts as base

OUT=base.ROOT/'video-audit/opener-shortening-2026-10-27'
APPROVAL='Agree. Make the change to Avoid the Traps and Embrace the Future.'
BASE_REVIEW=base.ROOT/'video-audit/opener-blue-board-cuts-2026-10-27'

def main():
 base.OUT=OUT
 base.PLANS={
  'avoid-traps-opener':dict(version=11,channels=1,blue_end=393,
   spans=[(389,3014),(3733,6458)],
   scope='Approved removal of post-analogy repeated explanation, retaining prior approved blue-board cuts.',authorization=APPROVAL,
   removed='From “A rip current is not the ocean malfunctioning” through “you can avoid the current entirely instead of fighting it.” Approved v10 cut: 87.500–111.467 s.',
   retained='Keep the hidden-failure introduction, complete rip-current analogy, all three map categories, and close. Move from “the most dangerous areas often look the most helpful and inviting” directly into “This roadmap shows what we’ll explore in this section.”',
   board_plan='No new board, ring, camera, or pause. Retain prior map and close treatment. Remove the repeated rip-current/pipe-maze/train-your-eye visuals with their narration.'),
  'embrace-the-future-opener':dict(version=8,channels=2,blue_end=307,
   spans=[(303,2455),(2781,3129),(3679,4271),(4641,5919)],
   clean_heads={1:2788,2:3686,3:4648},
   replace=(1062,1291),asset='course-assets/embrace-the-future-opener/embrace-the-future-opener-edge-of-the-map.jpg',
   scope='Approved removal of Magellan detour and repeated uncertainty commentary, retaining prior approved blue-board cuts.',authorization=APPROVAL,
   removed='Approved v7 cuts: 71.733–82.600 s (“Both the utopian and dystopian extremes…” through “…fears and hopes to fill it”); 94.200–112.533 s (“Consider Ferdinand Magellan” through “No”); 132.267–144.600 s (“Because this technology is a permanent fixture…” through “…clinging to extreme predictions”).',
   retained='Keep optimist/worrier contrast, uncertainty, old-map analogy, unexpected discoveries, taking both views seriously, AI-is-here-to-stay qualification, section map, and close.',
   board_plan='Keep previous map illustration replacement and all retained camera/rings. At each new join hold the first clean incoming frame for seven frames while keeping audio cuts inside silence; no orphan map/Magellan/X/trajectory frames.'),
 }
 manifests=[]
 with ThreadPoolExecutor(max_workers=2) as pool:manifests=list(pool.map(base.build,base.PLANS))
 for m in manifests:
  previous=json.loads((BASE_REVIEW/m['slug']/'edit-manifest.json').read_text())
  m['previous_approved_candidate']=previous['candidate'];m['previous_approved_sha256']=previous['candidate_sha256']
  m['saved_since_approved_seconds']=previous['duration']-m['duration']
  m['pauses']='No added silence. Cuts use existing sentence-end gaps; 5 ms fades inside quiet handles.'
  m['boundaries']=[dict(b,label=b['label'].replace('narration-move','narration-cut')) for b in m['boundaries']]
  (OUT/m['slug']/'edit-manifest.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n')
 (OUT/'edit-manifest.json').write_text(json.dumps(manifests,indent=2,ensure_ascii=False)+'\n')
 print('Finished both shorter candidates.',flush=True)

if __name__=='__main__':main()

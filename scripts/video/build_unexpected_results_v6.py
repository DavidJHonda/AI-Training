#!/usr/bin/env python3
"""Final visual QA corrections to the approved v5 assembly, rebuilt from raw sources."""
import argparse
import json
import cv2
import build_unexpected_results_v5 as base

base.OUT = base.ROOT/'video-audit/unexpected-results-combined-v6-2026-10-23'
base.DEST = base.ROOT/'Prompts/unexpected-results-v6.mp4'
OriginalPicture = base.Picture


class Picture(OriginalPicture):
    def __init__(self, rows):
        super().__init__(rows)
        self.hanoi_street = None

    def draw(self, row, frame):
        sf = (row['source_start'] or 0)+frame-row['start']
        if row['kind']=='hanoi' and 1261<=sf<1388:
            if self.hanoi_street is None:
                self.hanoi_street = self.native(1388)
            return self.hanoi_street.copy(), 'hanoi-street-replaces-unrelated-explorer'
        image, kind = super().draw(row, frame)
        if row['kind']=='hanoi' and 2091<=sf<2295:
            # A clear qualifier preserves the useful animation without presenting
            # generated week-by-week numbers as historical observations.
            cv2.putText(image, 'Illustrative counts', (906, 671),
                cv2.FONT_HERSHEY_SIMPLEX, .58, (65,65,65), 1, cv2.LINE_AA)
            kind = 'illustrative-tail-count-animation'
        return image, kind


base.Picture = Picture

if __name__=='__main__':
    cv2.setNumThreads(2)
    parser=argparse.ArgumentParser()
    parser.add_argument('--prepare-only',action='store_true')
    args=parser.parse_args()
    manifest=base.prepare()
    manifest['visual_qa_corrections']=[
        'Source roll 1 frames 1261–1387 show an unrelated explorer and Video Panel 1 label; cover with the next Hanoi street illustration.',
        'Keep the tail-count animation at source frames 2091–2294 and label its generated numerical series Illustrative counts.']
    manifest['audio_same_as_v5']=True
    (base.OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    if not args.prepare_only:base.render(manifest)

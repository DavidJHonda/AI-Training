#!/usr/bin/env python3
"""Photographic student/laptop section intros matching Why Learn AI."""
import json,sys
import build_big_downside_v10 as build

build.OUT=build.ROOT/'video-audit/big-downside-build-2026-10-10-v11'
build.DEST=build.ROOT/'Prompts/big-downside-v11.mp4'

if __name__=='__main__':
    manifest=build.prepare()
    manifest['scope']='Correct overview titles and three photographic student/laptop section introductions, matching the supplied Why Learn AI reference. Replaces rejected comic-style v10. Review build only.'
    (build.OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2))
    build.render(manifest,'--preview' in sys.argv)

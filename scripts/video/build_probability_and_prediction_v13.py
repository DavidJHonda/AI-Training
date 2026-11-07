#!/usr/bin/env python3
"""Final spoken pickup: match the existing board's encoded color at the join."""
import json
import cv2
from PIL import Image
import build_probability_and_prediction_v12 as base
from build_probability_and_prediction_v12 import ROOT, SOURCE, FPS, RATE, SPF, OVERRIDES
from editspec_build import Reader

DEST = ROOT / 'Prompts/probability-and-prediction-v13.mp4'
OUT = ROOT / 'video-audit/probability-and-prediction-spoken-bridge-v13-2026-11-07'


def bridge_image():
    reader = Reader(SOURCE)
    frame = reader.at(4899)
    reader.c.release()
    return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


def main():
    base.DEST, base.OUT, base.bridge_image = DEST, OUT, bridge_image
    base.main()
    path = OUT / 'edit-manifest.json'
    m = json.loads(path.read_text())
    m['bridge']['picture_source_frame'] = 4899
    m['bridge']['picture_note'] = 'Existing unmarked canonical dog-board arrival, reused exactly to prevent color drift when narration rejoins the original video.'
    m['supersedes'] = 'v12 picture-only refinement; narration and timing are identical.'
    path.write_text(json.dumps(m, indent=2) + '\n')


if __name__ == '__main__':
    main()

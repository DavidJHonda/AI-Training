#!/usr/bin/env python
"""Find likely appearances of a reference illustration in a lesson video.

The scan is sequential because time-based OpenCV seeks are unreliable on the
course MP4s. SIFT matches plus a homography make the detector tolerant of the
engine's crops, zooms, camera moves, and overlaid borders.

Usage:
  .video-venv/bin/python scripts/video/find_illustration_spans.py \
      videos/lesson.mp4 old-illustration.jpg [--stride 10]
"""

import argparse
import sys

import cv2
import numpy as np


def fit_width(image, width=720):
    if image.shape[1] <= width:
        return image
    scale = width / image.shape[1]
    return cv2.resize(image, (width, round(image.shape[0] * scale)),
                      interpolation=cv2.INTER_AREA)


def score_frame(sift, matcher, ref_kp, ref_desc, frame):
    gray = cv2.cvtColor(fit_width(frame), cv2.COLOR_BGR2GRAY)
    kp, desc = sift.detectAndCompute(gray, None)
    if desc is None or len(kp) < 4:
        return 0
    pairs = matcher.knnMatch(ref_desc, desc, k=2)
    good = [a for a, b in pairs if a.distance < 0.72 * b.distance]
    if len(good) < 6:
        return 0
    src = np.float32([ref_kp[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst = np.float32([kp[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    _, mask = cv2.findHomography(src, dst, cv2.RANSAC, 5.0)
    return int(mask.sum()) if mask is not None else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("video")
    ap.add_argument("reference")
    ap.add_argument("--stride", type=int, default=10,
                    help="score every Nth frame (default: 10)")
    ap.add_argument("--min-inliers", type=int, default=8)
    ap.add_argument("--gap", type=float, default=1.0,
                    help="join positive samples separated by at most this many seconds")
    ap.add_argument("--start-frame", type=int, default=0,
                    help="begin scoring at this frame (decode remains sequential)")
    ap.add_argument("--end-frame", type=int,
                    help="stop after this frame, exclusive")
    args = ap.parse_args()

    ref = cv2.imread(args.reference, cv2.IMREAD_GRAYSCALE)
    if ref is None:
        sys.exit(f"cannot read reference: {args.reference}")
    ref = fit_width(ref)
    sift = cv2.SIFT_create(nfeatures=1800)
    ref_kp, ref_desc = sift.detectAndCompute(ref, None)
    if ref_desc is None:
        sys.exit("reference produced no SIFT descriptors")
    matcher = cv2.BFMatcher(cv2.NORM_L2)

    cap = cv2.VideoCapture(args.video)
    if not cap.isOpened():
        sys.exit(f"cannot open video: {args.video}")
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)

    hits = []
    idx = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if args.end_frame is not None and idx >= args.end_frame:
            break
        if idx >= args.start_frame and idx % args.stride == 0:
            score = score_frame(sift, matcher, ref_kp, ref_desc, frame)
            if score >= args.min_inliers:
                hits.append((idx, score))
        idx += 1
    cap.release()

    print(f"video={args.video} decoded={idx} total={total} fps={fps:.6f} "
          f"stride={args.stride} hits={len(hits)}")
    if not hits:
        print("no spans")
        return

    groups = []
    max_gap = max(args.stride, round(args.gap * fps))
    cur = [hits[0]]
    for hit in hits[1:]:
        if hit[0] - cur[-1][0] <= max_gap:
            cur.append(hit)
        else:
            groups.append(cur)
            cur = [hit]
    groups.append(cur)

    pad = args.stride
    for group in groups:
        start = max(0, group[0][0] - pad)
        end = min(args.end_frame or total or idx, group[-1][0] + pad + 1)
        peak_frame, peak_score = max(group, key=lambda item: item[1])
        print(f"[{start},{end}) {start/fps:.2f}-{end/fps:.2f}s "
              f"positive={group[0][0]}-{group[-1][0]} "
              f"samples={len(group)} peak={peak_score}@{peak_frame/fps:.2f}s")


if __name__ == "__main__":
    main()

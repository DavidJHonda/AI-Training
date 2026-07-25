#!/usr/bin/env python
"""Classify each repair target span as STATIC or MOVING.

Why: the r3 graders worked from contact sheets sampled every 4s. Two findings
(welcome's "corrupted" board, tokens' "wrong" numbers) turned out to be one
sampled frame of a pan and of a counting animation. A single-frame claim is
reliable on a STATIC span and needs eyeballing on a MOVING one.

Sequential decode only (CAP_PROP_POS_MSEC seeks lie on these mp4s).
"""
import sys

import cv2

# (slug, start_s, end_s, what the grader claimed)
TARGETS = [
    ("does-school-matter", 68, 72, "pseudo-math + nonsense flowchart"),
    ("does-school-matter", 132, 136, "pseudo-code monitor"),
    ("does-school-matter", 148, 152, "lorem ipsum research page"),
    ("ai-is-math", 148, 155, "chart reads 24/71 then 26/74"),
    ("fake-trap", 168, 201, "three-checks board bottom-cropped"),
    ("what-you-can-control", 98, 103, "FLUSTATORY CHART pseudo-text"),
    ("why-learn-ai", 208, 215, "invented PROCESS/CONNECT/CREATE triangle"),
    ("layers", 10, 18, "scrambled dissolve, doubled card text"),
    ("hallucination", 72, 81, "gibberish thinking-process notebook"),
    ("hallucination", 128, 137, "pseudo-code"),
    ("hallucination", 140, 147, "fake journal tablet"),
    ("hallucination", 224, 227, "garbled RAG code block"),
    ("opener-avoid", 154, 161, "invented verify/audit/question board"),
    ("evaluate-the-results", 216, 240, "three-outcomes cards overlap/clip"),
    ("how-an-llm-works", 121, 129, "invented 85%/94%"),
    ("learn-with-ai", 124, 131, "broken-English chat prop"),
    ("learn-with-ai", 156, 163, "murky illegible discs"),
    ("what-is-ai", 96, 132, "movie-task board cropped both edges"),
    ("what-is-ai", 144, 148, "GI fragment on name-game board"),
    ("embeddings", 96, 104, "three-drink table cropped, CITRUS off-frame"),
    ("mind-trap", 206, 215, "dots-on-black + empty boxes under the payoff"),
    ("document-trap", 28, 37, "garbled rulebook + tournament-exception prop"),
    ("does-ai-think", 70, 82, "invented non-Chinese glyphs"),
    ("does-ai-think", 118, 130, "invented glyphs on reply note"),
    ("where-ai-works-best", 42, 48, "garbled code under the A+ claim"),
    ("where-ai-works-best", 230, 236, "nonsense-label diagram"),
    ("where-ai-works-best", 242, 248, "word-salad highlighted page"),
    ("context-window", 90, 116, "flat hold, narration past the visual"),
    ("training", 209, 224, "REVIEWER RANKINGS static lettering card"),
    ("training", 60, 66, "coach diagram mis-maps the analogy"),
    ("ai-is-different", 192, 205, "duplicate-layer text collision"),
]


def profile(path, a, b):
    cap = cv2.VideoCapture(path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
    fa, fb = int(a * fps), int(b * fps)
    prev, idx, diffs = None, 0, []
    while idx < fb:
        ok, frame = cap.read()
        if not ok:
            break
        if idx >= fa:
            small = cv2.cvtColor(cv2.resize(frame, (160, 90)),
                                 cv2.COLOR_BGR2GRAY).astype("int32")
            if prev is not None:
                diffs.append(abs(small - prev).mean())
            prev = small
        idx += 1
    cap.release()
    return diffs


print(f"{'slug':22} {'span':>13}  {'mean':>6} {'max':>6} {'moving%':>8}  verdict")
for slug, a, b, what in TARGETS:
    d = profile(f"videos/{slug}.mp4", a, b)
    if not d:
        print(f"{slug:22} {a:>5}-{b:<7} NO FRAMES"); continue
    mean = sum(d) / len(d)
    mx = max(d)
    moving = 100.0 * sum(1 for x in d if x > 0.5) / len(d)
    if moving < 10:
        v = "STATIC  -> single-frame finding RELIABLE"
    elif moving > 70:
        v = "MOVING  -> EYEBALL, may be pan/build/counter"
    else:
        v = "MIXED   -> eyeball"
    print(f"{slug:22} {a:>5}-{b:<7} {mean:6.2f} {mx:6.2f} {moving:7.0f}%  {v}")
    print(f"{'':22} claim: {what}")

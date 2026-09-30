#!/usr/bin/env python3
"""Verify v7 against its assembly source and confirm v6 preservation outside the quote."""
import json
import cv2
import numpy as np
import build_big_upside_v7 as v7
import qa_big_upside_v6 as qa


def main():
    v7.configure()
    qa.main()
    prior = v7.ROOT/'Prompts/big-upside-v6.mp4'
    assert v7.b.sha(prior) == '19002f4eaef7fa1a8bc984acec41fc682c164bf8a206870cedae2cf2fe91aae7'
    a, b = cv2.VideoCapture(str(prior)), cv2.VideoCapture(str(v7.DEST))
    errors, quote_errors = [], []
    quote = cv2.imread(str(v7.ASSET))
    n = 0
    while True:
        oka, x = a.read()
        okb, y = b.read()
        assert oka == okb
        if not oka:
            break
        if not v7.START <= n < v7.END:
            errors.append(float(cv2.absdiff(x,y).mean()))
        else:
            quote_errors.append(float(cv2.absdiff(quote,y).mean()))
        n += 1
    a.release(); b.release()
    assert n == 7719 and max(errors) < 5
    assert len(quote_errors) == v7.END-v7.START and max(quote_errors) < 5
    p = v7.OUT/'verification.json'
    checks = json.loads(p.read_text())
    checks['v6_preservation'] = dict(source=str(prior),frames_compared=len(errors),
        mean_absolute_error=float(np.mean(errors)),max_mean_absolute_error=max(errors),
        excluded_quote_frames=[v7.START,v7.END],pass_tolerance=5,passed=True)
    checks['full_quote_span'] = dict(frames_compared=len(quote_errors),
        max_mean_absolute_error=max(quote_errors),passed=True)
    p.write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps(checks['v6_preservation'],indent=2))


if __name__ == '__main__':
    main()

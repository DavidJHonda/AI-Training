#!/usr/bin/env python3
"""Verify encoded frame count, untouched picture spans, cutaway states, and audio."""
import json
from pathlib import Path
import cv2
import numpy as np
import build_work_changes_v4 as b


def encoding_outlier(a, z):
    """A high absolute delta can be fine-grain codec noise; check structure and color bias."""
    bias=np.mean(z.astype(np.float32)-a,axis=(0,1))
    x=cv2.cvtColor(a,cv2.COLOR_BGR2GRAY).astype(np.float32)
    y=cv2.cvtColor(z,cv2.COLOR_BGR2GRAY).astype(np.float32)
    u=cv2.GaussianBlur(x,(11,11),1.5);v=cv2.GaussianBlur(y,(11,11),1.5)
    vx=cv2.GaussianBlur(x*x,(11,11),1.5)-u*u
    vy=cv2.GaussianBlur(y*y,(11,11),1.5)-v*v
    cov=cv2.GaussianBlur(x*y,(11,11),1.5)-u*v
    ssim=((2*u*v+6.5025)*(2*cov+58.5225))/((u*u+v*v+6.5025)*(vx+vy+58.5225))
    return dict(ssim=float(ssim.mean()),channel_bias=bias.tolist())


def main():
    cv2.setNumThreads(2)
    out = b.OUT / 'encoded-qa'; out.mkdir(exist_ok=True)
    a = cv2.VideoCapture(str(b.SOURCE)); z = cv2.VideoCapture(str(b.DEST))
    assert z.isOpened()
    fps = z.get(cv2.CAP_PROP_FPS)
    wanted = {x for t in b.BOUNDARIES for x in [t-1,t,t+15]}
    wanted |= {4770, 6420, 6510, b.TOTAL-1}
    errors = []; outliers = []; samples = []; i = 0; means = []
    while True:
        oka, ia = a.read(); okz, iz = z.read()
        assert oka == okz, f'Source/candidate decode lengths differ at {i}'
        if not oka: break
        changed = any(s <= i < e for s,e in (b.PHOTO,b.ANIMATION))
        if not changed:
            # Composition and timing should match; allow only compression differences.
            diff = float(np.mean(cv2.absdiff(ia, iz)))
            means.append(diff)
            if diff > 1.5:
                detail=dict(frame=i,mean_absolute_error=diff,**encoding_outlier(ia,iz))
                outliers.append(detail)
                if diff>3 or detail['ssim']<.99 or max(abs(x) for x in detail['channel_bias'])>1:
                    errors.append(detail)
        if i in wanted:
            cv2.imwrite(str(out / f'{i:06d}.jpg'), iz)
            cell=cv2.resize(iz,(640,360))
            cv2.putText(cell,f'{i/30:.2f}s / frame {i}',(10,25),cv2.FONT_HERSHEY_SIMPLEX,.7,(0,0,220),2)
            samples.append(cell)
        i+=1
    a.release(); z.release()
    assert i == b.TOTAL and fps == b.FPS
    assert not errors, errors[:5]
    while len(samples)%3:samples.append(samples[-1]*0+255)
    cv2.imwrite(str(out/'contact-sheet.jpg'),cv2.vconcat([cv2.hconcat(samples[n:n+3]) for n in range(0,len(samples),3)]))
    audio_packets = b.audio_hash(b.SOURCE) == b.audio_hash(b.DEST)
    audio_decoded = b.audio_hash(b.SOURCE,True) == b.audio_hash(b.DEST,True)
    assert audio_packets and audio_decoded
    result=dict(decoded_frames=i,fps=fps,duration=i/fps,
                modified_frames=sum(e-s for s,e in (b.PHOTO,b.ANIMATION)),
                unmodified_frames_compared=len(means),
                unmodified_mean_absolute_error=float(np.mean(means)),
                unmodified_max_frame_mean_absolute_error=float(max(means)),
                reviewed_compression_outliers=outliers,
                mismatches=errors,audio_packets_identical=audio_packets,
                decoded_pcm_identical=audio_decoded,
                source_still_matches_verified_live=b.sha(b.SOURCE)==b.EXPECTED,
                candidate_sha256=b.sha(b.DEST))
    (out/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()

"""Owner's v13 revisions: pause, Dallas Stars Stanley Cup scene and four-card camera walk."""
import json

import cv2
import numpy as np

from build_fake_trap_v13 import (
    FPS, H, PICTURE, REGIONS, ROOT, SR, W, Build, LessonBoard,
    audio_track, camera, ease, fr, render, sha,
)

OUT = ROOT / 'Prompts/fake-trap-v14.mp4'
AUDIT = ROOT / 'video-audit/fake-trap-v14-2026-11-13'
HOCKEY = ROOT / 'scripts/video/assets/fake-trap-hockey/dallas-stars-cup.png'
PAUSE = dict(after='hook', start_frame=fr(14.3), added_frames=FPS, added_seconds=1)
FRAME_SAMPLES = SR // FPS


def paused_mix(work, sound, sources):
    tracks, gains = audio_track(work, sound, sources)
    cut = tracks[0]['end']
    assert cut == PAUSE['start_frame']
    path = work / 'mix.f32'
    pcm = np.fromfile(path, '<f4')
    at = cut * FRAME_SAMPLES
    seed = pcm[at-SR//10:at].copy()
    seed -= seed.mean()
    tone = np.resize(np.r_[seed, seed[::-1]], SR)
    assert np.max(np.abs(tone)) < .005
    np.concatenate((pcm[:at], tone, pcm[at:])).astype('<f4').tofile(path)
    for track in tracks[1:]:
        track['start'] += FPS
        track['end'] += FPS
    tracks.insert(1, dict(name='pause after hook', start=cut, end=cut+FPS))
    return tracks, gains


class MotivesCamera(LessonBoard):
    def view(self, state):
        if self.key != 'reasons' or state == 'full':
            return super().view(state)
        left, top, right, bottom = REGIONS['reasons'][state][0]
        width = Build.fit_w(right-left, bottom-top)
        # Clamp the view before interpolating so the pan starts on the first frame
        # of travel and settles on the last, including at the two outside cards.
        cx = np.clip(self.ox+(left+right)/2, width/2, self.image.shape[1]-width/2)
        return np.array([cx, self.oy+(top+bottom)/2, width])


def hockey_frames(count):
    image = cv2.imread(str(HOCKEY))
    h,w = image.shape[:2]
    full = min(w, h*W/H)
    for i in range(count):
        zoom = 1+.025*ease(i/(count-1))
        yield camera(image,w/2,h/2,full/zoom)[0]


def build_cut(out=OUT, audit=AUDIT, mix=paused_mix, motives_start=None, cues=PICTURE):
    picture = []
    for beat, at, kind, *params in cues:
        if beat == 'joke':
            kind, params = 'hockey', []
        if beat == 'motives' and params == ['full'] and motives_start is not None:
            at = motives_start
        if beat == 'comparison' and kind == 'comparison' and params == ['full']:
            # Let the new second settle on the opening board before the principal speaks.
            at -= 1
        picture.append((beat, at, kind, *params))
    render(out, audit, picture, mix, MotivesCamera,
           inserts={'hockey': hockey_frames}, pauses=[PAUSE], pan_motives=True)
    manifest = audit / 'edit-manifest.json'
    data = json.loads(manifest.read_text())
    data['sources'][str(HOCKEY.relative_to(ROOT))] = sha(HOCKEY)
    data['motives_camera'] = 'Full view, then one complete card at a time, with 36-frame eased travels.'
    manifest.write_text(json.dumps(data,indent=2)+'\n')


if __name__ == '__main__':
    build_cut()

#!/usr/bin/env python3
"""Approved version-3 visual edit. Copies its audio stream without alteration."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

import av
import cv2
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from build_work_changes_v8 import Board, lerp
from make_close_board import compose_canonical_for_video

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/work-changes-v9-2026-11-20'
DEST = ROOT / 'Prompts/work-changes-v9.mp4'
SOURCE = ROOT / 'Prompts/work-changes-3.mp4'
DONOR = ROOT / 'Prompts/work-changes-2.mp4'
ASSIGN = ROOT / 'course-assets/work-changes/work-changes-assignment-short.jpg'
CONCEPTS = ROOT / 'course-assets/work-changes/work-changes-automation-and-augmentation.jpg'
CLOSE = ROOT / 'course-assets/work-changes/work-changes-close.jpg'
CHECK = ROOT / 'scripts/video/assets/work-changes-cutaways-2026-09-30/check-reviews.png'
FF = imageio_ffmpeg.get_ffmpeg_exe()
FPS, W, H = 30, 1280, 720
FONT = '/System/Library/Fonts/Supplemental/Arial.ttf'
BOLD = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'


def fr(s):
    return round(s * FPS)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# Exact source visual cuts from sequential decoding, plus approved narration beats.
ASSIGN_IN, ASSIGN_OUT = 1504, 4156
CHECK_IN, CHECK_OUT = fr(91.68), fr(101.92)
CONCEPT_IN, CONCEPT_OUT = 4365, 5676
DIAGRAM_IN, DIAGRAM_OUT = 6435, 6726
TIMER_IN, TIMER_OUT = 6726, 6966
SCHOOL_IN, CLOSE_IN = 7451, fr(259.60)
SCHOOL_DONOR_IN, SCHOOL_DONOR_OUT = 6699, 6891

LEFT = [40, 334, 784, 1339]
RIGHT = [816, 334, 1560, 1339]
SCENARIO = [40, 112, 1560, 303]
BEFORE_L = [58, 969, 766, 1105]
WITH_L = [58, 1135, 766, 1321]
BEFORE_R = [834, 969, 1542, 1105]
WITH_R = [834, 1135, 1542, 1321]
BANNER = [40, 1378, 1560, 1467]
PURPLE, AMBER, TEAL, GENERAL = '#4f2fc4', '#a9760c', '#0e8f86', '#6e51ff'


def image_push(im, progress, amount=.02):
    h, w = im.shape[:2]
    zoom = 1 + amount * np.clip(progress, 0, 1)
    scale = max(W / w, H / h) * zoom
    matrix = np.array([[scale, 0, (W-w*scale)/2], [0, scale, (H-h*scale)/2]])
    return cv2.warpAffine(im, matrix, (W, H), flags=cv2.INTER_CUBIC)


def repair_label(frame, rect, text, size=22, final_color=(56, 65, 62), bold=False):
    """Replace only a video text region, following the source's reveal opacity.

    Geometry, arrows, icons, and animation remain from the current source frame.
    The patch background is sampled inside the same flat diagram component.
    """
    x0, y0, x1, y1 = rect
    crop = frame[y0:y1, x0:x1]
    corners = np.concatenate([crop[:2].reshape(-1, 3), crop[-2:].reshape(-1, 3)])
    bg = np.median(corners, axis=0).astype(np.uint8)
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
    # Earliest reveal frames carry almost no ink; do not force fully opaque text.
    opacity = float(np.clip((float(bg.mean()) - float(np.percentile(gray, 3))) / 145, 0, 1))
    patch = Image.new('RGB', (x1-x0, y1-y0), tuple(int(v) for v in bg[::-1]))
    draw = ImageDraw.Draw(patch)
    font = ImageFont.truetype(BOLD if bold else FONT, size)
    color = np.array(final_color)
    mixed = tuple(int(v) for v in (bg[::-1]*(1-opacity) + color*opacity))
    box = draw.multiline_textbbox((0, 0), text, font=font, spacing=4, align='center')
    x = ((x1-x0)-(box[2]-box[0]))/2-box[0]
    y = ((y1-y0)-(box[3]-box[1]))/2-box[1]
    draw.multiline_text((x, y), text, fill=mixed, font=font, spacing=4, align='center')
    frame[y0:y1, x0:x1] = np.array(patch)[:, :, ::-1]


def repair_diagram(frame, n):
    frame = frame.copy()
    repair_label(frame, (390, 28, 900, 65), 'WHEN OUTPUT GETS AHEAD OF KNOWLEDGE', 23,
                 (35, 79, 70), True)
    repair_label(frame, (158, 272, 365, 300), 'Customer complaints', 22)
    repair_label(frame, (530, 271, 750, 300), 'Option A: Product fix', 20)
    # Preserve the source's change from a possible suggestion to an unchecked fix.
    wrong = n >= fr(219.25)
    repair_label(frame, (530, 326, 750, 353),
                 'Option B: Unchecked fix' if wrong else 'Option B: Clearer guidance',
                 18, (189, 78, 44) if wrong else (56, 65, 62))
    repair_label(frame, (530, 380, 750, 408), 'Option C: Better support', 19)
    bad_recommendation = n >= fr(221.0)
    repair_label(frame, (902, 272, 1138, 301),
                 'Unchecked recommendation' if bad_recommendation else 'Your recommendation',
                 18, (189, 78, 44) if bad_recommendation else (56, 65, 62), True)
    repair_label(frame, (902, 302, 1138, 326),
                 'A flawed suggestion accepted' if bad_recommendation else 'Choose what to do',
                 17, (189, 78, 44) if bad_recommendation else (56, 65, 62))
    repair_label(frame, (303, 531, 585, 557), 'Ideas generated quickly', 20)
    repair_label(frame, (700, 531, 990, 557), 'Knowledge you still need', 20, (189, 78, 44))
    repair_label(frame, (370, 616, 1090, 666),
                 'Productive output does not guarantee good judgment.', 22, (35, 79, 70))
    return frame


def repair_timer(frame):
    frame = frame.copy()
    # A video label overlay removes the numerical promise while preserving the
    # illustration, its arrows, the review stack, and the time-saved relationship.
    x0, y0, x1, y1 = 179, 310, 477, 391
    patch = Image.new('RGB', (x1-x0, y1-y0), (224, 239, 232))
    draw = ImageDraw.Draw(patch)
    font = ImageFont.truetype(BOLD, 49)
    text = 'LEARN'
    b = draw.textbbox((0, 0), text, font=font)
    draw.text(((x1-x0-b[2]+b[0])/2, (y1-y0-b[3]+b[1])/2-b[1]),
              text, font=font, fill=(36, 60, 58))
    frame[y0:y1, x0:x1] = np.array(patch)[:, :, ::-1]
    return frame


class Edit:
    def __init__(self):
        self.assignment = Board(ASSIGN)
        self.concepts = Board(CONCEPTS)
        self.check = cv2.imread(str(CHECK))
        OUT.mkdir(parents=True, exist_ok=True)
        compose_canonical_for_video(CLOSE, OUT/'close-canvas.png', '#ffffff')
        self.close = cv2.imread(str(OUT/'close-canvas.png'))
        self.school = []
        with av.open(str(DONOR)) as container:
            container.seek(int(SCHOOL_DONOR_IN/FPS*1e6), backward=True)
            for f in container.decode(video=0):
                n = round(f.time*FPS)
                if n >= SCHOOL_DONOR_OUT:
                    break
                if n >= SCHOOL_DONOR_IN:
                    self.school.append(f.to_ndarray(format='bgr24'))
        assert len(self.school) == SCHOOL_DONOR_OUT-SCHOOL_DONOR_IN

    def assignment_frame(self, n):
        a = self.assignment
        full, scen, left, right = a.full, a.fit(SCENARIO), a.fit(LEFT), a.fit(RIGHT)
        ring, color = None, PURPLE
        if n < fr(54.12):
            camera, label = full, 'assignment-full'
        elif n < fr(63.28):
            camera = lerp(full, scen, n-fr(54.12), 30)
            ring, label = SCENARIO, 'assignment-scenario'
        elif n < fr(66.36):
            camera = lerp(scen, full, n-fr(63.28), 30)
            label = 'assignment-two-stages'
        elif n < CHECK_IN:
            camera = lerp(full, left, n-fr(66.36), 30)
            if n < fr(70.52):
                ring, label = LEFT, 'routine-purpose'
            elif n < fr(79.28):
                ring, label = BEFORE_L, 'routine-before-ai'
            else:
                ring, label = WITH_L, 'routine-with-ai'
        elif n < CHECK_OUT:
            return image_push(self.check, (n-CHECK_IN)/(CHECK_OUT-CHECK_IN)), 'checking-reviews-cutaway'
        elif n < fr(129.76):
            camera, color = right, AMBER
            if n < fr(109.44):
                ring, label = RIGHT, 'judgment-purpose'
            elif n < fr(117.84):
                ring, label = BEFORE_R, 'judgment-before-ai'
            else:
                ring, label = WITH_R, 'judgment-with-ai'
        else:
            # Complete-board pullback, then a readable full-width banner framing.
            camera = lerp(right, full, n-fr(129.76), 30)
            ring, color, label = BANNER, GENERAL, 'assignment-responsibility'
        # The target may be outside a moving camera: start its ring only once
        # all four sides fit, never draw a clipped outline during the move.
        if ring is not None:
            cx, cy, width = camera
            height = width*H/W
            bounds = [ring[0]+a.ox, ring[1]+a.oy, ring[2]+a.ox, ring[3]+a.oy]
            if min(bounds[0]-(cx-width/2), bounds[1]-(cy-height/2),
                   cx+width/2-bounds[2], cy+height/2-bounds[3]) < 10:
                ring = None
        return a.render(camera, ring, color), label

    def frame(self, source_frame, n):
        if ASSIGN_IN <= n < ASSIGN_OUT:
            return self.assignment_frame(n)
        if CONCEPT_IN <= n < CONCEPT_OUT:
            c = self.concepts
            rect, color, label = None, GENERAL, 'concepts-full'
            if n >= fr(178):
                rect, label = [40, 757, 1560, 846], 'concepts-ownership'
            elif n >= fr(162.48):
                rect, color, label = [816, 128, 1560, 717], TEAL, 'concepts-augment'
            elif n >= fr(149.84):
                rect, color, label = [40, 128, 784, 717], PURPLE, 'concepts-automate'
            return c.render(rect=rect, color=color), label
        if DIAGRAM_IN <= n < DIAGRAM_OUT:
            return repair_diagram(source_frame.to_ndarray(format='bgr24'), n), 'knowledge-gap-label-repair'
        if TIMER_IN <= n < TIMER_OUT:
            return repair_timer(source_frame.to_ndarray(format='bgr24')), 'saved-time-learn-label'
        if SCHOOL_IN <= n < CLOSE_IN:
            # Continuous donor sequence, slowed to fit, never looped or frozen.
            k = min(len(self.school)-1, int((n-SCHOOL_IN)*len(self.school)/(CLOSE_IN-SCHOOL_IN)))
            return self.school[k], 'school-donor-roll-2'
        if n >= CLOSE_IN:
            age = n-CLOSE_IN
            z = 1 if age < 48 else 1+.2*np.clip((age-48)/150, 0, 1)
            h, w = self.close.shape[:2]
            scale = W/w*z
            m = np.array([[scale, 0, (W-w*scale)/2], [0, scale, (H-h*scale)/2]])
            return cv2.warpAffine(self.close, m, (W, H), flags=cv2.INTER_CUBIC), 'canonical-close'
        return None, 'retained-roll-3'


PREVIEW_TIMES = [50.14, 53, 56, 64.5, 68, 72, 82, 95, 104, 112, 122, 132,
                 145.6, 153, 168, 182, 215.2, 216, 218, 220, 222, 224.3,
                 226, 231.9, 249, 255, 259.6, 262, 266.5, 268.3]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--preview', action='store_true')
    args = parser.parse_args()
    cv2.setNumThreads(2)
    edit = Edit()
    (OUT/'preview').mkdir(exist_ok=True)
    protected = {str(p.relative_to(ROOT)):sha(p) for p in
                 [SOURCE, DONOR, ASSIGN, CONCEPTS, CLOSE, CHECK, ROOT/'index.html',
                  ROOT/'course-assets/work-changes/work-changes.mp4']}
    wanted = {fr(t) for t in PREVIEW_TIMES}
    if not args.preview:
        assert not DEST.exists(), 'Never overwrite a candidate.'
        encoder = subprocess.Popen([FF, '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'yuv420p',
            '-s', f'{W}x{H}', '-r', str(FPS), '-i', 'pipe:0', '-i', str(SOURCE),
            '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-crf', '17',
            '-preset', 'fast', '-threads', '4', '-profile:v', 'high', '-level:v', '3.1',
            '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(DEST)],
            stdin=subprocess.PIPE)
    spans, current, written = [], None, 0
    with av.open(str(SOURCE)) as container:
        stream = container.streams.video[0]
        stream.codec_context.thread_count = 2
        total = stream.frames
        for f in container.decode(stream):
            n = round(f.time*FPS)
            assert n == written
            written += 1
            if args.preview and n not in wanted:
                continue
            im, label = edit.frame(f, n)
            if im is None:
                raw = f.to_ndarray(format='yuv420p')
            else:
                raw = av.VideoFrame.from_ndarray(im, format='bgr24').to_ndarray(format='yuv420p')
            if not args.preview:
                encoder.stdin.write(raw.tobytes())
                if current is None or label != current['label']:
                    if current:
                        current['end_frame'] = n; spans.append(current)
                    current = dict(start_frame=n, label=label)
                if written % 900 == 0:
                    print(f'Rendered {written}/{total}', flush=True)
            if n in wanted:
                if im is None:
                    im = f.to_ndarray(format='bgr24')
                cv2.imwrite(str(OUT/'preview'/f'{n:06d}-{label}.jpg'), im)
    assert written == total
    if args.preview:
        print('Previews complete', flush=True)
        return
    encoder.stdin.close()
    assert encoder.wait() == 0
    current['end_frame'] = total; spans.append(current)
    assert all(sha(ROOT/path) == digest for path,digest in protected.items())
    manifest = dict(candidate=str(DEST.relative_to(ROOT)), candidate_sha256=sha(DEST),
        source=str(SOURCE.relative_to(ROOT)), protected_sources=protected,
        frames=total, fps=FPS, duration=total/FPS, visual_spans=spans,
        audio='Original version-3 AAC packets copied. No cuts, fades, gain changes, pauses, or grafts.',
        density={'assignment':'dense, complete-card framing', 'concepts':'compact, full view'},
        geometry={'assignment':{'scenario':SCENARIO,'left':LEFT,'right':RIGHT,
            'before_left':BEFORE_L,'with_left':WITH_L,'before_right':BEFORE_R,
            'with_right':WITH_R,'banner':BANNER},'ring_width_output_px':4},
        school_donor={'source':str(DONOR.relative_to(ROOT)), 'source_frames':[SCHOOL_DONOR_IN,SCHOOL_DONOR_OUT],
                      'output_frames':[SCHOOL_IN,CLOSE_IN], 'treatment':'continuous slowed sequence; no loop'},
        close={'start_frame':CLOSE_IN,'hold_frames':48,'push_frames':150,'zoom':1.2,
               'last_frame':total-1},
        approval='Agree. Use version 3 and make the visual edits you recommended.',
        status='Review candidate; canonical video and lesson reference unchanged',
        listening='Not perceptually auditioned in this tool environment')
    (OUT/'edit-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('COMPLETE',DEST,total/FPS,flush=True)


if __name__ == '__main__':
    main()

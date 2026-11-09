#!/usr/bin/env python3
"""Match the takeaway highlight to the yellow banner's actual outer border.

Rebuild v18's pictures from its original sources and stream-copy approved v18
audio. Only the banner outline at 2:46.5–2:49.0 changes.
"""
import collections
import json
import subprocess

import cv2
import imageio_ffmpeg

import build_embeddings_v18 as prior
from ken_burns_path import draw_ring, hex_bgr

b = prior.build
ROOT = b.ROOT
OUT = ROOT / 'video-audit/embeddings-banner-v19-2026-11-09'
DEST = ROOT / 'Prompts/embeddings-v19.mp4'
AUDIO = ROOT / 'Prompts/embeddings-v18.mp4'
BANNER = (40, 901, 1560, 989)
START = b.output_frame(round(209.86 * 30))
END = b.output_frame(6372)


class Render(b.Render):
    def ring(self, im, key, rect, color='#6e51ff'):
        if key == 'comparison' and rect == (54, 912, 1544, 979):
            scale, x, y = self.transforms[key]
            left, top, right, bottom = BANNER
            draw_ring(im, x + left * scale, y + top * scale,
                      x + right * scale, y + bottom * scale,
                      hex_bgr(color), 12 * scale, 4)
        else:
            super().ring(im, key, rect, color)


def audio_hash(path):
    return subprocess.check_output([
        imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'error', '-i', str(path),
        '-map', '0:a:0', '-c:a', 'copy', '-f', 'hash', '-hash', 'sha256', '-'
    ]).decode().strip()


def main():
    OUT.mkdir(exist_ok=True)
    assert not DEST.exists(), f'Refusing to overwrite {DEST}'
    assert b.base.sha(AUDIO) == 'db3d09b6cd6bca93d896c8beb0ed1761521b18a32c37978f6cc01f218ff17f01'
    assert b.base.sha(b.SOURCE) == '07fae845877f4c704acaefddad84b780f011466fc33a97103c4ae766a241f127'
    installed = ROOT / 'course-assets/embeddings/embeddings.mp4'
    installed_hash = b.base.sha(installed)
    renderer = Render()
    preview, _ = renderer.frame(round(210.3666667 * 30), None)
    cv2.imwrite(str(OUT / 'after-167s.png'), preview)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    command = [ff, '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24',
               '-s', '1280x720', '-r', '30', '-i', 'pipe:0', '-i', str(AUDIO),
               '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'libx264', '-preset', 'fast',
               '-crf', '16', '-pix_fmt', 'yuv420p', '-c:a', 'copy', '-movflags', '+faststart', str(DEST)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    source = cv2.VideoCapture(str(b.SOURCE))
    count = 0
    types = collections.Counter()
    try:
        for f in range(8232):
            ok, native = source.read()
            assert ok, f
            if not any(a <= f < z for a, z in b.KEEP):
                continue
            picture, name = renderer.frame(f, native)
            process.stdin.write(picture.tobytes())
            types[name] += 1
            count += 1
            if count % 900 == 0:
                print(f'Encoded {count}/{b.TOTAL}', flush=True)
        process.stdin.close()
        assert process.wait() == 0
    finally:
        source.release()
        if process.poll() is None:
            process.kill()
    assert count == b.TOTAL
    assert audio_hash(DEST) == audio_hash(AUDIO)
    assert b.base.sha(installed) == installed_hash
    manifest = dict(candidate=str(DEST.relative_to(ROOT)), source=str(b.SOURCE.relative_to(ROOT)),
                    source_sha256=b.base.sha(b.SOURCE), output_sha256=b.base.sha(DEST),
                    audio_source=str(AUDIO.relative_to(ROOT)), copied_audio_sha256=audio_hash(DEST),
                    frames=count, fps=30, duration=count / 30, changed_output_frames=[START, END],
                    banner_bounds_source_pixels=BANNER, banner_corner_radius_source_pixels=12,
                    highlight_width_output_pixels=4, previous_bounds=[54, 912, 1544, 979],
                    installed_unchanged_sha256=installed_hash, encode_command=command,
                    frame_types=dict(types), scope='Only the banner highlight border; no timing or narration edits.')
    (OUT / 'edit-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(dict(output=str(DEST), duration=count / 30, changed_seconds=[START / 30, END / 30])))


if __name__ == '__main__':
    main()

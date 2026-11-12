"""Cut the v22 recap and extend its last Check the Match frame through the qualification."""
from pathlib import Path
import subprocess
import sys
import cv2
import imageio_ffmpeg

root = Path(__file__).resolve().parents[2]
source = root / 'Prompts/hallucination-v22.mp4'
output = Path(sys.argv[1])
if output.exists():
    raise FileExistsError(output)
fps = 30
samples_per_frame = 1600
cut_start, cut_end = 161 * fps, 182 * fps
checking_end, closing_start = 4710, 5749
source_frames = 6067
frames = source_frames - (cut_end - cut_start)
hold = closing_start - checking_end - (cut_end - cut_start)
audio_filter = (f"asetnsamples=n={samples_per_frame}:p=0,"
                f"aselect='lt(n,{cut_start})+gte(n,{cut_end})',"
                f"asetpts=N/SR/TB,atrim=end_sample={frames * samples_per_frame}")
cmd = [imageio_ffmpeg.get_ffmpeg_exe(), '-n', '-v', 'error',
       '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', '1280x720', '-r', str(fps), '-i', 'pipe:0',
       '-i', str(source), '-map', '0:v:0', '-map', '1:a:0', '-af', audio_filter,
       '-c:v', 'libx264', '-crf', '15', '-preset', 'fast', '-threads', '4', '-pix_fmt', 'yuv420p',
       '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', str(output)]
reader = cv2.VideoCapture(str(source))
encoder = subprocess.Popen(cmd, stdin=subprocess.PIPE)
written = 0
for index in range(source_frames):
    assert reader.grab()
    if checking_end <= index < closing_start:
        continue
    pixels = reader.retrieve()[1].tobytes()
    repeat = hold + 1 if index == checking_end - 1 else 1
    for _ in range(repeat):
        encoder.stdin.write(pixels)
    written += repeat
encoder.stdin.close()
assert encoder.wait() == 0 and written == frames

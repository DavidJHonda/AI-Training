"""Read-only source diagnostics for the approved split-lesson build."""
from pathlib import Path
import argparse
import json
import subprocess
import cv2
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'video-audit/how-an-llm-works-repair-2026-09-17-v10'

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--words', action='store_true')
    p.add_argument('--loudness-only', action='store_true')
    args = p.parse_args()
    OUT.mkdir(exist_ok=True)
    if args.words:
        from faster_whisper import WhisperModel
        model = WhisperModel('small.en', device='cpu', compute_type='int8', cpu_threads=2, local_files_only=True)
        for name in ('learns-1', 'answers-2'):
            dest = OUT / (name + '-words.json')
            if dest.exists():
                continue
            segs, _ = model.transcribe(str(ROOT / 'Prompts' / f'how-the-model-{name}.mp4'), language='en', beam_size=5, word_timestamps=True)
            result = [dict(start=s.start, end=s.end, text=s.text, words=[dict(start=w.start, end=w.end, word=w.word) for w in s.words]) for s in segs]
            dest.write_text(json.dumps(result, indent=2))
            print('transcribed', name, flush=True)
        return
    requests = {
        'learns-1': [0, 253, 254, 1264, 1265, 1290, 1400, 1428, 1500, 1521, 1522],
        'learns-2': [5241, 5250, 5310, 5370, 5430, 5460],
        'answers-1': [560, 600, 690, 720, 780, 810, 840, 870, 900, 930, 960],
        'answers-2': [4735, 4736, 4737, 4800, 4980, 5040, 5100, 5130, 5160, 5190, 5220, 5250, 5280, 5310, 5315, 5370, 5460, 5600, 5748, 5749, 5944, 5945],
    }
    for name, want in requests.items():
        if args.loudness_only:
            continue
        path = ROOT / 'Prompts' / f'how-the-model-{name}.mp4'
        dest = OUT / 'source-checks' / name
        dest.mkdir(parents=True, exist_ok=True)
        c = cv2.VideoCapture(str(path))
        wanted = set(want)
        cells = []
        for i in range(max(want) + 1):
            ok, im = c.read()
            assert ok
            if i not in wanted:
                continue
            cv2.imwrite(str(dest / f'f{i:05d}.jpg'), im, [cv2.IMWRITE_JPEG_QUALITY, 95])
            cell = cv2.resize(im, (480, 270))
            cv2.putText(cell, f'f{i} {i/30:.3f}s', (10, 25), cv2.FONT_HERSHEY_SIMPLEX, .65, (0,0,255), 2)
            cells.append(cell)
        c.release()
        for j in range(0, len(cells), 9):
            chunk = cells[j:j+9]
            while len(chunk) % 3:
                chunk.append(chunk[0] * 0)
            cv2.imwrite(str(dest / f'sheet-{j//9}.jpg'), cv2.vconcat([cv2.hconcat(chunk[k:k+3]) for k in range(0,len(chunk),3)]))
        print('frames', name, flush=True)
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    for name in requests:
        p = subprocess.run([ff, '-hide_banner', '-i', str(ROOT/'Prompts'/f'how-the-model-{name}.mp4'), '-af', 'loudnorm=I=-18:TP=-2:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True, check=True)
        meta = json.JSONDecoder().raw_decode(p.stderr[p.stderr.rfind('{'):])[0]
        (OUT / f'{name}-loudness.json').write_text(json.dumps(meta, indent=2))
        print(name, 'LUFS',meta['input_i'], 'true peak',meta['input_tp'],flush=True)

if __name__ == '__main__':
    main()

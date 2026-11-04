#!/usr/bin/env python3
"""Verify the encoded v6, capture edit transitions, and transcribe its soundtrack."""
import argparse
import json
import re
import subprocess

import av
import cv2
import numpy as np

import build_beyond_the_first_answer_v6 as v


def transcribe():
    from faster_whisper import WhisperModel
    out = v.OUT/'qa'
    out.mkdir(exist_ok=True)
    model = WhisperModel('small.en', device='cpu', compute_type='int8',
                         cpu_threads=4, local_files_only=True)
    segments, _ = model.transcribe(str(v.DEST), language='en', beam_size=5,
                                   word_timestamps=True, vad_filter=False)
    records, lines = [], []
    for s in segments:
        records.append({'start': s.start, 'end': s.end, 'text': s.text,
                        'words': [{'start': w.start, 'end': w.end, 'word': w.word}
                                  for w in s.words]})
        lines.append(f'[{s.start:.2f}-{s.end:.2f}] {s.text.strip()}')
    (out/'transcript.json').write_text(json.dumps(records, indent=2)+'\n')
    (out/'transcript.txt').write_text('\n'.join(lines)+'\n')
    print('Encoded-file transcription complete.', flush=True)


def main():
    cv2.setNumThreads(2)
    out = v.OUT/'qa'
    out.mkdir(exist_ok=True)
    manifest = json.loads((v.OUT/'edit-manifest.json').read_text())
    wants = {v.TOTAL-1} | set(range(0, v.TOTAL, 225))
    for b in manifest['boundaries']:
        wants.update(b['frame']+offset for offset in [-1,0,1,12,30])
    donors = v.donor_frames()
    deltas, errors, tiles = [], [], []
    count = 0
    with av.open(str(v.SOURCE)) as src, av.open(str(v.DEST)) as dst:
        for c in (src,dst):
            c.streams.video[0].codec_context.thread_count = 2
        ds = dst.streams.video[0]
        assert (ds.width,ds.height) == (1280,720) and ds.average_rate == 30
        frames = iter(dst.decode(video=0))
        for n, f in enumerate(src.decode(video=0)):
            if v.removed(n):
                continue
            actual = next(frames)
            assert abs(float(actual.pts*actual.time_base)-count/30) < 0.00001
            donor = v.visual_source(n)
            expected = donors[donor] if donor != n else f.to_ndarray(format='yuv420p')
            encoded = actual.to_ndarray(format='yuv420p')
            delta = float(np.abs(encoded[::4,::4].astype(np.int16)-expected[::4,::4].astype(np.int16)).mean())
            deltas.append(delta)
            if delta > 2.5:
                errors.append({'output_frame': count, 'source_frame': n,
                               'visual_source_frame': donor, 'mae': delta})
            if count in wants:
                im = actual.to_ndarray(format='bgr24')
                cv2.imwrite(str(out/f'{count:06d}.jpg'), im)
                tile = cv2.resize(im, (384,216))
                cv2.rectangle(tile, (0,0), (384,25), (255,255,255), -1)
                cv2.putText(tile, f'{count/30:.2f}s | v5 {n/30:.2f}s', (6,18),
                            cv2.FONT_HERSHEY_SIMPLEX, .45, (0,0,190), 1)
                tiles.append(tile)
            count += 1
            if count % 2000 == 0:
                print(f'Verified {count}/{v.TOTAL}', flush=True)
        assert next(frames,None) is None and count == v.TOTAL
    for i in range(0,len(tiles),16):
        p = tiles[i:i+16]
        while len(p)%4:
            p.append(np.full_like(p[0],255))
        cv2.imwrite(str(out/f'sheet-{i//16+1}.jpg'),
                    cv2.vconcat([cv2.hconcat(p[j:j+4]) for j in range(0,len(p),4)]))
    subprocess.run([v.FF, '-v','error','-y','-i',str(v.DEST),'-vn','-ac','1',
                    '-ar',str(v.SR),str(out/'encoded.wav')], check=True)
    expected = v.read_pcm(v.OUT/'edited.wav')/32768
    encoded = v.read_pcm(out/'encoded.wav')[:len(expected)]/32768
    assert len(encoded) == len(expected)
    correlation = float(np.corrcoef(expected,encoded)[0,1])
    assert correlation > .999
    joins = []
    for cut in manifest['cuts']:
        q = cut['output_frame']*1600
        window = encoded[q-960:q+960]
        joins.append({'label': cut['label'], 'output_seconds': q/v.SR,
                      'rms_dbfs_40ms': float(20*np.log10(max(np.sqrt(np.mean(window**2)),1e-12))),
                      'peak_dbfs_40ms': float(20*np.log10(max(abs(window).max(),1e-12))),
                      'step_at_join': float(abs(encoded[q]-encoded[q-1]))})
    result = subprocess.run([v.FF,'-hide_banner','-i',str(v.DEST),'-vn','-af',
        'silencedetect=noise=-35dB:d=0.12','-f','null','-'],capture_output=True,text=True,check=True)
    (out/'encoded-silences.txt').write_text(result.stderr)
    starts = [float(s) for s in re.findall(r'silence_start: ([\d.]+)',result.stderr)]
    ends = [float(s) for s in re.findall(r'silence_end: ([\d.]+)',result.stderr)]
    for join in joins:
        span = next(((a,b) for a,b in zip(starts,ends) if a <= join['output_seconds'] <= b),None)
        assert span is not None, join
        join['measured_silence_seconds'] = list(span)
        join['measured_gap_seconds'] = span[1]-span[0]
    verification = {'decoded_frames': count, 'duration_seconds': count/30,
        'saved_seconds': manifest['seconds_removed'], 'max_sampled_yuv_mae': max(deltas),
        'mean_sampled_yuv_mae': float(np.mean(deltas)), 'visual_errors': errors,
        'audio_correlation_to_edit': correlation,
        'audio_peak_dbfs': float(20*np.log10(max(abs(encoded)))), 'audio_joins': joins,
        'protected_files_unchanged': all(v.sha(p)==h for p,h in manifest['protected_hashes'].items()),
        'candidate_sha256': v.sha(v.DEST), 'listening': 'Not performed; no subjective listening pass claimed.'}
    (out/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
    assert not errors and verification['protected_files_unchanged']
    args = [str(v.ROOT/'.video-venv/bin/python'),str(v.ROOT/'scripts/video/transition_guard.py'),
            str(v.DEST),'--outdir',str(out/'transitions')]
    for b in manifest['boundaries']:
        args += ['--boundary',f"{b['frame']}:{b['label']}"]
    proc = subprocess.run(args, check=False)
    print(f'Technical verification complete; transition guard exit {proc.returncode}.',flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--transcribe', action='store_true')
    args = parser.parse_args()
    transcribe() if args.transcribe else main()

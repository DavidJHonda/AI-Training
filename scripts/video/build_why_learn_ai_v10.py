#!/usr/bin/env python3
"""Photographic replacement of the four v9 custom inserts; review only."""
import argparse
import json
import subprocess
import build_why_learn_ai_v9 as v9


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--preview', action='store_true')
    args = ap.parse_args()
    prior_dir = v9.OUT
    prior_video = v9.DEST
    prior = json.loads((prior_dir / 'edit-manifest.json').read_text())
    assert v9.sha(prior_video) == prior['render_sha256']
    for path, digest in prior['protected_hashes'].items():
        assert v9.sha(path) == digest, f'Source changed since v9: {path}'
    v9.OUT = v9.AUDIT / 'build-v10'
    v9.DEST = v9.ROOT / 'Prompts/why-learn-ai-v10.mp4'
    v9.ASSETS = v9.OUT / 'assets'
    for key in ['navigation', 'chatbot', 'feedback', 'document']:
        assert (v9.ASSETS / f'{key}.png').is_file(), key
    b, m = v9.prepare()
    assert m['visual_timeline'] == prior['visual_timeline']
    assert m['total_frames'] == prior['total_frames'] == 7075
    m['build_script'] = str(v9.ROOT / 'scripts/video/build_why_learn_ai_v10.py')
    m['revision'] = {
        'purpose': 'Replace four custom cartoon inserts with photographic images; realistic high school students in people scenes.',
        'base_video': str(prior_video),
        'base_sha256': prior['render_sha256'],
        'assets': {key: {'path': str(v9.ASSETS / f'{key}.png'), 'sha256': v9.sha(v9.ASSETS / f'{key}.png')} for key in ['navigation', 'chatbot', 'feedback', 'document']},
        'changed_spans': [r for r in m['visual_timeline'] if r['kind'] == 'still'],
        'audio': 'Copy v9 AAC stream without re-encoding',
        'timing_unchanged': True,
        'publication': 'Review candidate only',
    }
    v9.render(b, m, args.preview, audio_source=prior_video)
    if args.preview:
        return
    def audio_md5(path):
        return subprocess.check_output([b.ff, '-v', 'error', '-i', str(path), '-map', '0:a:0', '-c:a', 'copy', '-f', 'md5', '-'], text=True).strip()
    old_audio, new_audio = audio_md5(prior_video), audio_md5(v9.DEST)
    assert old_audio == new_audio
    assert v9.sha(prior_video) == prior['render_sha256']
    m['revision']['audio_packet_md5'] = {'v9': old_audio, 'v10': new_audio, 'identical': True}
    (v9.OUT / 'edit-manifest.json').write_text(json.dumps(m, indent=2))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Verify the published November 11 batch without saving remote video copies."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import ssl
import subprocess
import time
import urllib.error
import urllib.request

import certifi

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
BASE = 'https://besmarterthanthetool.com'
COMMIT = subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip()
CONTEXT = ssl.create_default_context(cafile=certifi.where())
PAGE = (ROOT / 'index.html').read_bytes()
MANIFEST = json.loads((ROOT / 'course-assets/manifest.json').read_text())
KEYS = ['openerworkwith', 'openerfoundations', 'openerprotect', 'openerrealworld', 'openerskills']


def refs(text):
    result = {}
    for key in KEYS:
        match = re.search(r'^\s*' + key + r': \{ src: "([^"]+)"', text, re.M)
        assert match, key
        result[key] = match.group(1)
    return result


def read(url):
    req = urllib.request.Request(url, headers={
        'Cache-Control': 'no-cache', 'User-Agent': 'AI-Training-release-verification',
    })
    with urllib.request.urlopen(req, context=CONTEXT, timeout=45) as response:
        return response.read(), dict(status=response.status, url=response.url,
                                     server=response.headers.get('server'))


def verify_file(relative, expected_sha, expected_bytes=None):
    url = BASE + '/' + relative
    digest = hashlib.sha256()
    size = 0
    req = urllib.request.Request(url, headers={'User-Agent': 'AI-Training-release-verification'})
    with urllib.request.urlopen(req, context=CONTEXT, timeout=90) as response:
        while True:
            block = response.read(1024 * 1024)
            if not block:
                break
            size += len(block)
            digest.update(block)
        result = dict(url=response.url, status=response.status, bytes=size, sha256=digest.hexdigest())
    assert result['sha256'] == expected_sha, result
    if expected_bytes is not None:
        assert size == expected_bytes, result
    result['matches_local'] = True
    return result


def main():
    expected = refs(PAGE.decode())
    deadline = time.monotonic() + 600
    print('Waiting for the production alias to serve the release...', flush=True)
    while True:
        served, metadata = read(BASE + '/course?release=' + COMMIT)
        if refs(served.decode()) == expected and b'var REMAINING_PHONE_BOARDS' in served:
            break
        if time.monotonic() > deadline:
            raise SystemExit('Production did not serve the expected batch within ten minutes.')
        time.sleep(10)
    assert hashlib.sha256(served).digest() == hashlib.sha256(PAGE).digest()
    print('Production course source matches the release byte for byte.', flush=True)
    by_path = {row['new']: row for row in MANIFEST['video_assets']}
    jobs = []
    for key, relative in expected.items():
        row = by_path[relative.split('?')[0]]
        jobs.append((key, relative, row['sha256'], row['bytes']))
    for name in ['landing.html', 'landing.css', 'entry-flow.css', 'start-course.js', 'course-assets/manifest.json']:
        local = (ROOT / name).read_bytes()
        jobs.append((name, name + '?release=' + COMMIT, hashlib.sha256(local).hexdigest(), len(local)))
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [(key, pool.submit(verify_file, relative, digest, size))
                   for key, relative, digest, size in jobs]
        results = {}
        for key, future in futures:
            results[key] = future.result()
            print('PASS public bytes: ' + key, flush=True)
    result = dict(
        source_commit=COMMIT, verified_at_utc=datetime.now(timezone.utc).isoformat(),
        public_course=BASE + '/course', course_response=metadata,
        course_page_sha256=hashlib.sha256(served).hexdigest(),
        course_page_matches_local=True, files=results,
        all_five_opener_videos_match_local=True, phone_and_entry_files_match_local=True,
        video_verification='Streamed each public response into SHA-256; no remote media copies retained.',
        status='Verified live',
    )
    (OUT / 'publication.json').write_text(json.dumps(result, indent=2) + '\n')
    print('Verified live: all five opener videos, course page, phone/entry files, and asset manifest.', flush=True)


if __name__ == '__main__':
    main()

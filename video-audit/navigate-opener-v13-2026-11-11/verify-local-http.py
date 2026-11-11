from pathlib import Path
import importlib.util, threading, urllib.request, json, hashlib
spec = importlib.util.spec_from_file_location('local_site', 'scripts/serve-site.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
server = mod.ThreadingHTTPServer(('127.0.0.1', 0), mod.Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}'
try:
    entry = 'course-assets/navigate-the-future-opener/navigate-the-future-opener.mp4?v=20261111ship13'
    html = urllib.request.urlopen(base + '/index.html').read().decode()
    assert html.count(entry) == 1
    with urllib.request.urlopen(base + '/' + entry) as response:
        data = response.read(); mime = response.headers.get('Content-Type')
        assert response.status == 200
    digest = hashlib.sha256(data).hexdigest()
    assert digest == '9a98d0bcc07916ca1b9fe6987b5d49e736565c0af676f6fa29908052258754e2'
    assert mime == 'video/mp4'
    p = Path('video-audit/navigate-opener-v13-2026-11-11/local-release.json')
    d = json.loads(p.read_text())
    d['local_http_verification'] = dict(html_reference_matches=True, video_http_status=200, content_type=mime, served_sha256=digest, served_bytes=len(data))
    p.write_text(json.dumps(d, indent=2) + '\n')
    print('Local HTTP course reference and served MP4 hash verified.')
finally:
    server.shutdown(); server.server_close()

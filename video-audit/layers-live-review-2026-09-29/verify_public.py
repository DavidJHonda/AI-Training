import urllib.request, hashlib, re, json, datetime, pathlib
root = pathlib.Path(__file__).resolve().parents[2]
out = pathlib.Path(__file__).resolve().parent
base = 'https://besmarterthanthetool.com/'
p = urllib.request.urlopen(base, timeout=30).read().decode()
(out/'public-index.html').write_text(p)
entry = re.search(r'  layers: \{ src: "([^"]+)"[^\n]+', p).group(0)
paths = [re.search(r'src: "([^"]+)"', entry).group(1)]
paths += re.findall(r'src: "(course-assets/layers/[^\"]+)', p)
paths += ['course-assets/layers/layers-close.jpg']
results = []
for path in dict.fromkeys(paths):
    h = hashlib.sha256(); size = 0
    with urllib.request.urlopen(base+path, timeout=30) as r:
        while chunk := r.read(1048576):
            h.update(chunk); size += len(chunk)
    local = root/path.split('?')[0]
    lh = hashlib.sha256(local.read_bytes()).hexdigest()
    results.append(dict(url=base+path, bytes=size, sha256=h.hexdigest(), local_sha256=lh, matches_local=h.hexdigest()==lh))
result = dict(checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(), page=base, entry=entry, assets=results)
(out/'public-verification.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))

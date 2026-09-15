"""Resolve course image paths without coupling build scripts to folder layout.

The migration manifest distinguishes same-named assets from the two old folders.
New generated assets use the lesson prefix map; new lessons should extend that map.
"""
from functools import lru_cache
from pathlib import Path
import fnmatch
import json

ROOT = Path(__file__).resolve().parents[2]

@lru_cache(maxsize=1)
def _manifest():
    return json.loads((ROOT / 'course-assets/manifest.json').read_text())

@lru_cache(maxsize=1)
def _paths():
    return {row['old']: row['new'] for row in _manifest()['assets']}

def asset_path(origin, filename):
    """Return the absolute path for an original folder and preserved filename."""
    filename = str(filename)
    if Path(filename).name != filename:
        raise ValueError('Expected a filename, not a path: ' + filename)
    key = origin + '/' + filename
    if any(row['old'] == key for row in _manifest().get('retired_assets', [])):
        raise ValueError('Retired source asset: ' + key + '. Use a current lesson board instead.')
    relative = _paths().get(key)
    if relative is None:
        prefixes = _manifest()['prefixes']
        stem = Path(filename).stem
        group = next((prefixes[p] for p in sorted(prefixes, key=len, reverse=True)
                      if stem == p or stem.startswith(p + '-')), None)
        if group is None:
            raise ValueError('Add a lesson prefix to course-assets/manifest.json before generating ' + key)
        relative = 'course-assets/' + group + '/' + filename
    return ROOT / relative

class AssetDirectory:
    """A manifest-backed view for existing generators that enumerate one origin."""
    def __init__(self, origin):
        if origin not in ('lessons', 'illustrations'):
            raise ValueError(origin)
        self.origin = origin
    def __truediv__(self, name):
        return asset_path(self.origin, name)
    def iterdir(self):
        # Multiple original paths can now resolve to one retained asset.
        paths = dict.fromkeys(row['new'] for row in _manifest()['assets']
                              if row['old'].startswith(self.origin + '/'))
        return (ROOT / relative for relative in paths)
    def glob(self, pattern):
        return (p for p in self.iterdir() if fnmatch.fnmatch(p.name, pattern))
    def rglob(self, pattern):
        return self.glob(pattern)
    def exists(self):
        return (ROOT / 'course-assets').exists()

def asset_dir(origin):
    return AssetDirectory(origin)

if __name__ == '__main__':
    import sys
    print(asset_path(sys.argv[1], sys.argv[2]))

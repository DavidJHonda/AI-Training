"""Locate current finished videos from the website catalogue."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[2]
ALIASES = {'does-school-matter': 'beyond-the-average', 'which-app': 'your-home-base', 'opener-work': 'work-with-ai-opener', 'opener-understand': 'understand-ai-opener', 'opener-avoid': 'avoid-traps-opener', 'opener-build': 'build-your-skills-opener', 'opener-embrace': 'embrace-the-future-opener', 'transformers-quiz': 'ai-brain-break'}

def current_video_paths():
    text = (ROOT / 'index.html').read_text()
    return [ROOT / p for p in sorted(set(re.findall(r'course-assets/[A-Za-z0-9_./-]+\.mp4', text)))]

def current_video_path(slug):
    name = Path(slug).stem if slug.endswith('.mp4') else slug
    name = ALIASES.get(name, name)
    found = next((p for p in current_video_paths() if p.stem == name), None)
    if found is None:
        raise FileNotFoundError('No current course video for ' + slug)
    return found

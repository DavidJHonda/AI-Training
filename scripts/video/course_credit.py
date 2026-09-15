"""Write approved course boards with one website credit and unchanged geometry."""
from pathlib import Path
from functools import lru_cache
import base64
import hashlib
import json
import zlib

ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / 'scripts/video/course-credit-policy.json'

@lru_cache(maxsize=1)
def policy():
    return json.loads(POLICY_PATH.read_text())['boards']

def _relative(path):
    try:
        return Path(path).resolve().relative_to(ROOT).as_posix()
    except (TypeError, ValueError):
        return None

def _marker(spec):
    return ('course-credit-v1:' + hashlib.sha256(json.dumps(spec,sort_keys=True).encode()).hexdigest()).encode()

def paint_credit(image, spec):
    """Reset the reserved footer patch before drawing; never stack the lettering."""
    from PIL import Image, ImageDraw
    try:
        from .editorial_typography import face
    except ImportError:
        from editorial_typography import face
    if tuple(spec['size']) != image.size:
        raise ValueError(f"Board dimensions changed: expected {spec['size']}, got {image.size}. Review the credit placement before rebuilding.")
    result = image.convert('RGB').copy()
    x0,y0,x1,y1 = spec['clear_box']
    patch = Image.frombytes('RGB', (x1-x0,y1-y0), zlib.decompress(base64.b64decode(spec['background_rgb_zlib'])))
    result.paste(patch,(x0,y0))
    scale = result.width / 1600
    ImageDraw.Draw(result).text((result.width-round(40*scale),result.height-round(10*scale)),
        'besmarterthanthetool.com',font=face('medium',round(20*scale)),fill='#625c7a',anchor='rd')
    return result

def save_course_image(image, fp, *args, **kwargs):
    """Pillow-compatible save. Non-course and unapproved outputs are untouched."""
    relative = _relative(fp)
    if relative and relative.startswith('course-assets/'):
        manifest = json.loads((ROOT / 'course-assets/manifest.json').read_text())
        retired = next((r for r in manifest.get('retired_assets', []) if r['new'] == relative), None)
        if retired:
            replacement = retired.get('replaced_by', 'a current lesson board')
            raise ValueError(f'Retired asset output: {relative}. Use {replacement}; do not rerun the old renderer over its replacement.')
    spec = policy().get(relative) if relative and relative.startswith('course-assets/') else None
    if spec is None:
        return image.save(fp,*args,**kwargs)
    credited = paint_credit(image,spec)
    kwargs['comment'] = _marker(spec)
    # Newly rendered boards must use the standard name; no attributed derivative.
    return credited.save(fp,*args,**kwargs)

def finalize(path):
    """For native/shell outputs. Skip already credited bytes or stamped exports."""
    path = Path(path).resolve()
    relative = _relative(path)
    spec = policy().get(relative)
    if spec is None:
        return False
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() == spec['approved_sha256']:
        return False
    from PIL import Image,JpegImagePlugin
    import io
    with Image.open(io.BytesIO(raw)) as source:
        if source.size != tuple(spec['size']):
            raise ValueError(f'Unexpected dimensions for {relative}: {source.size}')
        if source.info.get('comment') == _marker(spec):
            return False
        kwargs = dict(optimize=True,progressive=True)
        if source.format=='JPEG':
            kwargs.update(qtables=source.quantization,subsampling=JpegImagePlugin.get_sampling(source))
        image = paint_credit(source,spec)
    buffer = io.BytesIO()
    image.save(buffer,'JPEG',comment=_marker(spec),**kwargs)
    path.write_bytes(buffer.getvalue())
    return True

if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('paths',nargs='*')
    p.add_argument('--all',action='store_true')
    args=p.parse_args()
    targets=[ROOT / k for k in policy()] if args.all else args.paths
    if not targets:p.error('Provide a file path or --all')
    for target in targets:finalize(target)

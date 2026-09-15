"""Read-only usage audit. Writes reports; never deletes or changes course assets."""
from pathlib import Path
import collections,hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
if not (ROOT/'index.html').exists():ROOT=Path('/Users/davidobrien/Developer/AI-Training')
index=(ROOT/'index.html').read_text()
exts={'.jpg','.jpeg','.png','.webp','.svg','.pdf','.mp4'}
web=set(re.findall(r'course-assets/[A-Za-z0-9_./-]+\.(?:jpg|jpeg|png|webp|svg|pdf|mp4)',index))
web.update('course-assets/training/'+s for s in re.findall(r'board\("([^"\n]+\.jpg)"',index))
manifest=json.loads((ROOT/'course-assets/manifest.json').read_text())
aliases=collections.defaultdict(set)
for r in manifest['assets']:
 aliases[r['new']].add(r['old'])
assets=sorted(p for p in (ROOT/'course-assets').rglob('*') if p.is_file() and p.suffix.lower() in exts)
byhash=collections.defaultdict(list)
for p in assets:byhash[hashlib.sha256(p.read_bytes()).hexdigest()].append(p.relative_to(ROOT).as_posix())
sources=[]
for folder in ['scripts','lessons','Prompts']:
 for p in (ROOT/folder).rglob('*'):
  if p.is_file() and p.suffix in {'.py','.js','.cjs','.json','.sh','.md','.html','.tsv'} and p.name not in {'course-credit-policy.json','audit-course-asset-usage.py'}:
   sources.append((p.relative_to(ROOT).as_posix(),p.read_text(errors='replace')))
rows=[]
for p in assets:
 rel=p.relative_to(ROOT).as_posix();digest=hashlib.sha256(p.read_bytes()).hexdigest()
 names={rel,p.name}|aliases[rel]
 patterns=[re.compile(r'(?<![A-Za-z0-9_./-])'+re.escape(n)+r'(?![A-Za-z0-9_.-])') for n in names]
 refs=[f for f,t in sources if any(pattern.search(t) for pattern in patterns)]
 video=[f for f in refs if f.startswith('scripts/video/paths/') or Path(f).name.startswith(('build_','prepare_'))]
 kit=[f for f in refs if f.startswith(('lessons/','Prompts/'))]
 same_lesson=[x for x in byhash[digest] if x!=rel and Path(x).parent==Path(rel).parent and x in web]
 if rel in web:status='current_page'
 elif same_lesson:status='exact_duplicate_in_lesson'
 elif video:status='video_reference_review'
 elif kit:status='lesson_or_upload_reference_review'
 elif refs:status='generator_only_review'
 else:status='no_source_reference_found'
 rows.append(dict(path=rel,category=status,bytes=p.stat().st_size,sha256=digest,identical_current_same_lesson=same_lesson,references=refs))
counts=dict(collections.Counter(r['category'] for r in rows))
out=ROOT/'docs/course-assets-final-usage-audit.json'
out.write_text(json.dumps({'counts':counts,'files':rows,'notes':['Static source audit, including dynamically constructed Training paths and original-path aliases.','A video script reference does not establish that an image appears in the latest finished video.','Verify that candidates are unused by current lessons and downloads; historical generator or video references alone do not justify retention.','No assets were modified or deleted.']},indent=2)+'\n')
lines=['# Course assets: final usage audit','', 'Read-only inventory of current page references, video dependencies, and likely superseded images. No assets deleted.','',f'{len(rows)} media files; {counts.get("current_page",0)} referenced by the current page; {len(rows)-counts.get("current_page",0)} require cleanup review.','', 'Current lesson images and downloads are the source of truth. Historical video scripts and highlight plans do not protect superseded images; future video updates should use current lesson boards.','', '## Counts','']
lines.extend(f'- {k}: {v}' for k,v in counts.items())
for lesson in sorted({Path(r['path']).parts[1] for r in rows}):
 group=[r for r in rows if Path(r['path']).parts[1]==lesson];extra=[r for r in group if r['category']!='current_page']
 if not extra:continue
 lines.extend(['',f'## {lesson}','', '**Current page files:** '+', '.join('`'+Path(r['path']).name+'`' for r in group if r['category']=='current_page'), ''])
 for r in extra:
  lines.append(f'- **{Path(r["path"]).name}** — {r["category"].replace("_"," ")}')
  if r['identical_current_same_lesson']:lines.append('  Identical to: '+', '.join('`'+Path(x).name+'`' for x in r['identical_current_same_lesson']))
  if r['references']:lines.append('  References: '+', '.join('`'+x+'`' for x in r['references']))
(ROOT/'docs/course-assets-final-usage-audit.md').write_text('\n'.join(lines)+'\n')
print(json.dumps(counts,indent=2))
for lesson,count in collections.Counter(Path(r['path']).parts[1] for r in rows if r['category']!='current_page').most_common(8):print(lesson,count)

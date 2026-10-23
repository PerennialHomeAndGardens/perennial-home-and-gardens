"""Use the same versioned app artwork on every HTML page; preserve app identity."""
from pathlib import Path
import os,re,json,hashlib
ROOT=Path('.')
# The loader and shared interactions must change URL together for returning visitors.
version=hashlib.sha256((ROOT/'app-assets/install.js').read_bytes()+(ROOT/'app-assets/site-experience.js').read_bytes()).hexdigest()[:12]
for page in ROOT.rglob('*.html'):
 value=page.read_text()
 value=re.sub(r'(<script\b[^>]*\bsrc=["\'][^"\']*app-assets/install\.js)(?:\?[^"\']*)?(["\'])',lambda m:m[1]+'?v='+version+m[2],value,flags=re.I)
 def remove_icon(match):
  tag=match[0]
  rel=re.search(r'\brel\s*=\s*["\']([^"\']+)',tag,re.I)
  if rel and any(x in rel[1].lower().split() for x in ['icon','apple-touch-icon','apple-touch-icon-precomposed']):return ''
  return tag
 value=re.sub(r'<link\b[^>]*>',remove_icon,value,flags=re.I)
 prefix=os.path.relpath(ROOT/'app-assets',page.parent).replace(os.sep,'/')
 links=f'<link rel="icon" type="image/png" sizes="64x64" href="{prefix}/icon-64-large-20261015.png">\n<link rel="apple-touch-icon" sizes="180x180" href="{prefix}/icon-180-large-20261015.png">'
 value=re.sub(r'\s*</head>',lambda _: '\n'+links+'\n</head>',value,count=1)
 page.write_text(value)
print('Versioned app/favicons applied')

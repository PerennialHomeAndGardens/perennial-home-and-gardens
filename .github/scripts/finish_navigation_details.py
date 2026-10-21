"""Keep direct library access and compact home previews on retained pages."""
from pathlib import Path
from bs4 import BeautifulSoup as Soup
R=Path(__file__).resolve().parents[2]
VERSION='20261021-soft-whirl'
pages=[R/'index.html',R/'garden-books.html',*R.glob('tools/*/index.html'),*R.glob('articles/*.html'),*R.glob('legal/*.html'),*R.glob('books/*.html'),*R.glob('help/*.html')]
for p in pages:
 d=Soup(p.read_text(),'html.parser')
 for nav in d.select('#navlinks,.phg-footer-nav'):
  if not nav.select_one('a[href="/tools/garden-library/"]'):
   a=d.new_tag('a',href='/tools/garden-library/');a.string='Garden Library'
   apps=next((x for x in nav.select('a') if x.get_text(strip=True)=='Garden Apps'),None)
   if apps:apps.insert_after(a)
   else:nav.append(a)
 for n in d.select('link[href*="app-navigation.css"],script[src*="app-navigation.js"]'):
  key='href' if n.name=='link' else 'src';n[key]='/app-assets/'+('app-navigation.css' if key=='href' else 'app-navigation.js')+'?v='+VERSION
 if p==R/'index.html':
  for h,title in zip(d.select('#services article h3'),['Coaching','Design Templates','Garden Installation']):h.string=title
 if p==R/'tools/garden-library/index.html':
  dictionary=d.select_one('section.glossary');assert dictionary is not None
  dictionary['id']='phgDictionary'
  jumps=d.select_one('.phg-library-launches');assert jumps is not None
  if not jumps.select_one('a[href="#phgDictionary"]'):
   a=d.new_tag('a',href='#phgDictionary');a['class']='phg-app-open';a.string='Aa Dictionary'
   search=jumps.select_one('a');search.insert_after(a)
 p.write_text(str(d))
p=R/'app-assets/app-navigation.css';css=p.read_text();marker='/* Compact previews and selected transition audio timing */'
css=css.split(marker)[0].rstrip()+'\n\n'+marker+'''
.phg-home-app .b17PreviewInner,.phg-home-app [class$="-inner"]{align-items:start!important}
.phg-home-app .phg-app-copy{height:auto!important}
.phg-home-app .phg-app-launch{margin-top:0!important;padding-top:12px}
.phg-home-app .b17AppIsland,.phg-home-app [class$="-preview"],.phg-home-app .phg-harvest-preview{align-self:start!important;height:auto!important;min-height:0!important}
.phg-home-app .b17App{min-height:0!important}
.phg-portal::before,.phg-portal::after{animation-duration:1.3s}
#phgDictionary{scroll-margin-top:110px}
@media(max-width:600px){.phg-home-app{padding-top:34px!important;padding-bottom:34px!important}}
'''
p.write_text(css)
(R/'app-assets/footer.html').write_text(str(Soup((R/'index.html').read_text(),'html.parser').footer))
print('Restored Garden Library navigation on',len(pages),'pages; Dictionary shortcut, compact previews and service titles ready.')

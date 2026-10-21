"""Idempotent polish of retained pages: no article or app content regeneration."""
from pathlib import Path
from bs4 import BeautifulSoup as Soup
import re,json,urllib.request
ROOT=Path(__file__).resolve().parents[2]
VERSION='20261020-polish'
icons={}
for name in ['pinterest','etsy','redbubble']:
 p=ROOT/'app-assets'/('social-'+name+'.svg')
 if not p.exists():
  p.write_bytes(urllib.request.urlopen('https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/'+name+'.svg',timeout=20).read())
 svg=Soup(p.read_text(),'html.parser').svg;svg.attrs={'viewBox':'0 0 24 24','aria-hidden':'true'}
 if svg.title:svg.title.decompose()
 icons[name]=str(svg)
pages=[ROOT/'index.html',*sorted((ROOT/'tools').glob('*/index.html')),*sorted((ROOT/'articles').glob('*.html')),*sorted((ROOT/'legal').glob('*.html'))]
arrival="""(()=>{try{const a=JSON.parse(sessionStorage.getItem('phg-app-arrival')||'null');sessionStorage.removeItem('phg-app-arrival');if(a&&a.path===location.pathname&&Date.now()-a.at<10000&&!matchMedia('(prefers-reduced-motion: reduce)').matches){document.documentElement.classList.add('phg-arriving');setTimeout(()=>document.documentElement.classList.remove('phg-arriving'),1400)}}catch{}})();"""
for page in pages:
 d=Soup(page.read_text(),'html.parser');d.body['data-site-slug']='perennial-home-and-gardens'
 for n in d.select('.phg-free-tag,.phg-preview-caption'):n.decompose()
 if page.name=='index.html' and page.parent==ROOT or 'tools' in page.relative_to(ROOT).parts:
  for n in list(d.find_all(string=True)):
   if n.parent.name not in ['script','style'] and re.search(r'\bfree\b',str(n),re.I):
    n.replace_with(re.sub(r'\bfree(?:[- ]+)?','',str(n),flags=re.I).strip())
 if page==ROOT/'index.html':
  for n in d.find_all(string=re.compile(r'^garden tools$',re.I)):n.replace_with('Garden Apps')
 if page.parent.name=='plant-identifier':
  for heading in d.select('h3'):
   if heading.get_text(strip=True)=='1. Build a Photo Set':
    heading.string='1. Upload plant photos';heading.find_next_sibling('p').string='Choose Upload under Whole Plant, Close-up or another view to add a photo. Photos stay in this browser session; saved reports store observations rather than full images.'
  for script in d.find_all('script'):
   code=script.get_text()
   if 'function buildPhotos()' in code:
    code=code.replace('photos[id]={name:file.name,data:r.result}', 'photos[id]={type:id,name:file.name,data:r.result}')
    code=code.replace('📷 ', 'Upload · ')
    code=code.replace("'<b>'+PHOTO_TYPES[i]?.title||\"Photo\"+':</b> '","'<b>'+(PHOTO_TYPES.find(x=>x.id===p.type)?.title||'Photo')+':</b> '")
    script.string=code
 for n in d.select('header a,footer a,.b21StickyBrand a'):
  if 'free' in n.get_text().lower() and not n.find('svg'):
   for t in list(n.find_all(string=True)):t.replace_with(re.sub(r'\bfree(?:[- ]+)?','',str(t),flags=re.I).strip())
 h=d.select_one('.b21StickyBrand')
 if h:
  h['class']=list(dict.fromkeys(h.get('class',[])+['phg-compact-header']))
  wood=h.select_one('.b20WoodBar');nav=h.select_one('#navlinks');actions=h.select_one('.newActions')
  if wood and actions and nav:
   for n in actions.select('.desktopShare,.desktopJoin'):n.decompose()
   wood.append(actions.extract());wood.append(nav.extract())
   for empty in h.select(':scope > .nav'):empty.decompose()
   music=wood.select_one('#music');music['aria-label']='Open Perennial Home and Gardens jukebox';music.attrs.pop('title',None);music['data-phg-tooltip']='Jukebox'
   music.clear();music.append(Soup('<span class="phg-equalizer" aria-hidden="true"><i></i><i></i><i></i></span>','html.parser'))
   menu=wood.select_one('.cleanMenu');menu['aria-label']='Open navigation';menu['aria-controls']='navlinks';menu['aria-expanded']='false';menu['data-phg-tooltip']='Menu'
   if page!=ROOT/'index.html' and not wood.select_one('.phg-back'):
    fallback='/articles/' if page.parent.name=='articles' and page.name!='index.html' else '/#tools'
    wood.insert(0,Soup('<a class="phg-back" href="'+fallback+'" aria-label="Go back" data-phg-tooltip="Back"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m14 5-7 7 7 7M7 12h14"/></svg></a>','html.parser'))
 social=d.select_one('.phg-socials')
 if social:
  for n,name in zip(social.select('a'),['pinterest','etsy','redbubble']):
   n.clear();n['aria-label']=name.title() if name!='redbubble' else 'Redbubble';n['title']=n['aria-label'];n.append(Soup(icons[name],'html.parser'))
 for n in d.select('link[data-phg-polish],script[data-phg-polish]'):n.decompose()
 for link in d.select('link[href*="site-experience.css"]'):link.decompose()
 link=d.new_tag('link',rel='stylesheet',href='/app-assets/site-experience.css?v='+VERSION);link['data-phg-polish']='';d.head.append(link)
 link=d.new_tag('link',rel='stylesheet',href='/app-assets/app-navigation.css?v='+VERSION);link['data-phg-polish']='';d.head.append(link)
 boot=d.new_tag('script');boot['data-phg-polish']='';boot.string=arrival;d.head.append(boot)
 js=d.new_tag('script',src='/app-assets/app-navigation.js?v='+VERSION);js['defer']='';js['data-phg-polish']='';d.head.append(js)
 for script in d.select('script[src*="install.js"]'):script['src']=re.sub(r'\?.*','',script['src'])+'?v='+VERSION
 if d.select_one('#ap'):
  ref=d.new_tag('script',src='/app-assets/tanya-reference.js?v='+VERSION);ref['defer']='';ref['data-phg-polish']='';d.head.append(ref)
 page.write_text(str(d))
print('Polished',len(pages),'pages; removed third-grid captions and redundant badges; static compact header retained.')

(ROOT/'app-assets/footer.html').write_text(str(Soup((ROOT/'index.html').read_text(),'html.parser').footer))

"""Targeted refinements: existing profile, course layout and shared help access."""
from pathlib import Path
from bs4 import BeautifulSoup as Soup
import re,html,base64
R=Path(__file__).resolve().parents[2]
def e(s):return html.escape(s,quote=True)
def frag(s):return Soup(s,'html.parser')
p=R/'index.html';d=Soup(p.read_text(),'html.parser')
text='Rooted in the meaning of perennial, we believe in creating gardens, outdoor spaces, and lasting home experiences that renew, endure, and bring beauty, nourishment, and value for generations.'
if not d.find(id='phg-perennial-meaning'):
 target=d.select_one('#about p');target.insert_after(frag('<p id="phg-perennial-meaning">'+text+'</p>'))
# Preserve course photography bytes; move text into the card body, never across the photo.
assets=R/'app-assets/course-originals';assets.mkdir(exist_ok=True)
for i,c in enumerate(d.select('#courses article')):
 strip=c.select_one('.courseStrip')
 if not strip:continue
 src=re.search(r'url\([\"\']?(.*?)[\"\']?\)',strip.get('style',''))
 if not src:continue
 url=src.group(1)
 if url.startswith('data:'):
  meta,data=url.split(',',1);ext=meta.split('/')[1].split(';')[0];f=assets/('course-'+str(i+1)+'.'+ext);f.write_bytes(base64.b64decode(data));url='/'+str(f.relative_to(R))
 image=d.new_tag('img',src=url,alt=['Garden foundations learning materials and growing space','Garden planning and production learning path','Advanced garden systems learning path'][i]);image['class']='phg-course-photo';image['loading']='lazy'
 caption=strip.get_text(' ',strip=True);strip.decompose();c.insert(0,image)
 if caption and not c.select_one('.phg-course-caption'):
  h=c.find('h3');h.insert_after(frag('<p class="phg-course-caption">'+e(caption)+'</p>'))
# Install the six user-approved photographs while retaining the previous bytes.
originals=R/'app-assets/home-originals';originals.mkdir(exist_ok=True)
for section_id,slugs in [('services',['garden-coaching','garden-design','garden-installation']),('shop',['raised-beds','greenhouse','high-tunnel'])]:
 images=d.select('#'+section_id+' article img');assert len(images)==3
 for image,slug in zip(images,slugs):
  old=image.get('src','')
  if old.startswith('data:'):
   meta,data=old.split(',',1);ext=meta.split('/')[1].split(';')[0];(originals/(slug+'.'+ext)).write_bytes(base64.b64decode(data))
  image['src']='/app-assets/approved-home/'+slug+'.webp';image['loading']='lazy';image['width']='1280';image['height']='720'
  image['alt']={'garden-coaching':'Remote garden coaching consultation using a laptop in the garden','garden-design':'Garden planting plans, reference materials and a digital layout','garden-installation':'Professional garden installation team building and planting an outdoor space','raised-beds':'Productive raised garden beds in a landscaped outdoor space','greenhouse':'Glass hobby greenhouse with planted beds and flowers','high-tunnel':'High tunnel sheltering productive garden beds'}[slug]
p.write_text(str(d))
p=R/'tools/my-garden/index.html';d=Soup(p.read_text(),'html.parser')
heading=d.find('h2',string='Coming Next')
if heading:
 section=heading.find_parent('section');note=section.select_one('.section-note')
 if note:note.string='Your garden profile and saved records stay in this browser on this device. Use each tool’s Save control, and export backups where offered. No membership is required. Clearing browser data removes saved records.';section.insert_before(note.extract())
 section.decompose()
grid=d.select_one('.toolgrid')
order=['growing-zone','garden-planner','garden-calculator','plant-companions','seasonal-calendar','plant-identifier','harvest-checker','garden-library','seed-starting','garden-journal','harvest-records','garden-inventory']
for slug in order:
 a=grid.select_one('a[href="../'+slug+'/"]');assert a is not None;grid.append(a.extract())
for f in d.select('.field'):
 label=f.find('label');field=f.find(['input','select'])
 if label and field and field.get('id'):label['for']=field['id']
p.write_text(str(d))
# Shared styles are appended once and keep original colorful card backgrounds.
p=R/'app-assets/app-navigation.css';s=p.read_text();marker='/* Connected garden finishing */';s=s.split(marker)[0]
s+='''\n/* Connected garden finishing */
.toolgrid a.tool{display:grid;grid-template-columns:30px minmax(0,1fr);align-content:start;column-gap:10px;row-gap:10px}.toolgrid a.tool>.icon{grid-column:1;grid-row:1;margin:0;align-self:center}.toolgrid a.tool>b{grid-column:2;grid-row:1;margin:0;align-self:center}.toolgrid a.tool>span:not(.icon){grid-column:1/-1}.phg-context-help{display:block;max-width:1200px;margin:18px auto;padding:0 22px;color:#3c613c;font:14px/1.6 Georgia,serif}.phg-course-photo{display:block;width:calc(100% + 48px);max-width:none;height:210px;object-fit:cover;margin:-24px -24px 22px;border-radius:18px 18px 0 0}.phg-course-caption{font-size:14px;color:#647455}.courseVisualCard{overflow:hidden}.phg-guide{max-width:1040px;margin:auto;padding:42px 22px 70px;font:17px/1.75 Georgia,serif;color:#2e402e}.phg-guide h1{font:500 clamp(38px,5vw,62px)/1.1 Georgia,serif;color:#213622}.phg-guide-search{display:grid;gap:8px;margin:24px 0}.phg-guide-search input{font:16px Georgia,serif;padding:13px;border:1px solid #becbb1;border-radius:10px}.phg-guide details{padding:18px 22px;border:1px solid #ced8c2;background:#fffdf6;border-radius:14px;margin:14px 0;scroll-margin-top:115px}.phg-guide summary{cursor:pointer;font-weight:700;color:#315936}.phg-guide a{color:#315936}.phg-guide .guide-intro{background:#edf1e3;border-radius:16px;padding:24px}.phg-guide video,.phg-guide iframe{width:100%;aspect-ratio:16/9;border:0;border-radius:12px}#ap .tanya-help{color:#446238;font:12px Georgia,serif;justify-self:end;margin:0 16px -5px} @media(max-width:520px){.phg-course-photo{height:185px}.phg-guide{padding:26px 17px 50px}.phg-guide details{padding:15px}}
''';p.write_text(s)
# Add the same help destination to the existing navigation and footer on every retained page.
paths=[R/'index.html',R/'garden-books.html']+list((R/'tools').glob('*/index.html'))+list((R/'articles').glob('*.html'))+list((R/'legal').glob('*.html'))+list((R/'books').glob('*.html'))
for p in paths:
 d=Soup(p.read_text(),'html.parser')
 for nav in d.select('#navlinks,.phg-footer-nav'):
  if not nav.select_one('a[href="/help/"]'):nav.append(frag('<a href="/help/">Help &amp; Tutorials</a>'))
 if '/tools/' in str(p) and not d.select_one('.phg-context-help'):
  slug=p.parent.name
  help=frag('<a class="phg-context-help" href="/help/#'+slug+'">Need a hand? Open this tool’s step-by-step guide →</a>')
  if d.main:d.main.insert(0,help)
 for link in d.select('link[href*="app-navigation.css"]'):link['href']='/app-assets/app-navigation.css?v=20261021-garden-start'
 p.write_text(str(d))
# The assistant keeps both categories, voice, audio and compose controls untouched.
p=R/'app-assets/tanya-assistant.js';s=p.read_text();s=s.replace("panel.replaceChildren(head,categories,chat,back,audioBox,form,status);","const help=make('a','tanya-help','Help & Tutorials →');help.href='/help/';back.append(help);panel.replaceChildren(head,categories,chat,back,audioBox,form,status);") if "const help=make('a','tanya-help'" not in s else s
# back is a button; keep its existing text/click action, put the tutorial link separately inside categories instead.
s=s.replace("back.append(help);panel.replaceChildren", "categories.append(help);panel.replaceChildren")
p.write_text(s)
print('Preserved About photography, refined connected cards and course layout; shared help links installed.')

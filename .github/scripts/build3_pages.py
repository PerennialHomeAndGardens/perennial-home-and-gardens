from pathlib import Path
import re,base64
from bs4 import BeautifulSoup
p=Path('index.html');s=p.read_text()
# Retire both old automatic campaigns; manual resource buttons remain intact.
s,n=re.subn(r"function scheduleFreebiePopup\(\)\{.*?\n\}\nfunction closeFreebie", "function scheduleFreebiePopup(){}\nfunction closeFreebie",s,count=1,flags=re.S)
assert n==1
s,n=re.subn(r"window.addEventListener\('load', \(\)=>\{\s*setTimeout\(\(\)=>\{ if\(localStorage.getItem\('phg_freebie_claimed'\).*?\}, 10000\);\s*setTimeout\(\(\)=>\{ if\(localStorage.getItem\('phg_freebie_claimed'\).*?\}, 300000\);\s*\}\);","",s,count=1,flags=re.S)
assert n==1
s=re.sub(r'(app-assets/install\.js)(?:\?[^"\s<>]*)?',r'\1?v=20261020-build3',s)
# Repair the older community form's literal newlines so its welcome functions can load.
broken="+n+'\nEmail: '+e+'\nWhat they hope to grow: '+g+'\nWhat they hope to gain: '+h"
fixed="+n+'\\nEmail: '+e+'\\nWhat they hope to grow: '+g+'\\nWhat they hope to gain: '+h"
assert broken in s
s=s.replace(broken,fixed)
s=s.replace('Join our list and open the current free-resource folder.', 'Open the current free-resource folder with the form below.')
p.write_text(s)
soup=BeautifulSoup(s,'html.parser')
header=soup.select_one('.b21StickyBrand')
assert header and soup.select_one('#contact .contactGrid')
logo=header.select_one('.b20Logo img')['src']
wood=re.search(r'\.b20WoodBar\s*\{.*?background:url\("([^"]+)"\)',s,re.S)[1]
def save_data(data,name):
 assert data.startswith('data:')
 typ,encoded=data.split(',',1)
 ext=typ.split('/')[1].split(';')[0].replace('svg+xml','svg').replace('jpeg','jpg')
 path=Path('app-assets')/(name+'.'+ext)
 path.write_bytes(base64.b64decode(encoded))
 return '/'+str(path)
logo_url=save_data(logo,'header-logo')
wood_url=save_data(wood,'header-wood')
header.select_one('.b20Logo img')['src']=logo_url
for a in header.select('a[href^="#"]'):a['href']='/'+a['href']
# Tool pages retain their existing body, controls and in-app links.
for page in Path('tools').glob('*/index.html'):
 t=page.read_text()
 if 'phg-shared-header-build3' in t:continue
 # Preserve local tool navigation; the old masthead is replaced only.
 t=re.sub(r'<header\b[^>]*>.*?</header>','',t,count=1,flags=re.S)
 h=str(header)
 h=h.replace('href="/#top"','href="/"')
 inject='<style id="phg-shared-header-build3">.b21StickyBrand{position:sticky;top:0;z-index:100;background:#302015}.b20WoodBar{display:flex;align-items:center;justify-content:center;background:url("'+wood_url+'") center/cover}.b20Logo{display:flex;align-items:center;justify-content:center;height:100%}.b20Logo img{width:auto;object-fit:contain}.b21StickyBrand .nav{display:none}.b21StickyBrand .cleanMenu span{display:block}</style>'+h
 inject+='<script>if(window.top!==window.self)document.querySelector(".b21StickyBrand")?.remove();</script>'
 t=re.sub(r'(<body\b[^>]*>)',lambda m:m[1]+inject,t,count=1)
 t=t.replace('</body>','<script src="/app-assets/install.js?v=20261020-build3"></script></body>')
 page.write_text(t)
print('Patched campaign timers; shared header added to',len(list(Path('tools').glob('*/index.html'))),'tool pages.')

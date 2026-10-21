"""Expand retained PHG topics and repair routes without changing garden app logic."""
from pathlib import Path
from bs4 import BeautifulSoup as Soup
import re, json, html, math, base64, subprocess
ROOT=Path(__file__).resolve().parents[2]
BASE='8ec40f7d8baddd30d24b470a1d82b032945f945b'
def original(path): return subprocess.check_output(['git','show',BASE+':'+str(path)],cwd=ROOT).decode()
def esc(x):return html.escape(str(x),quote=True)
def slug(x):return re.sub('[^a-z0-9]+','-',x.lower()).strip('-')
def fragment(x):return Soup(x,'html.parser')
def wc(a):
 text=a['title']+' '+a['summary']+' '+' '.join(a['goals'])+' '+a['activity']+' '+' '.join(a['checklist'])
 for s in a['sections']:text+=' '+s['heading']+' '+' '.join(s.get('paragraphs',[]))+' '+' '.join(s.get('steps',[]))
 for v in a['vocabulary']:text+=' '+v['term']+' '+v['meaning']
 for q in a['pretest']+a['quiz']:text+=' '+q['question']+' '+' '.join(q['options'])+' '+q['explanation']
 return len(re.findall(r"\b[\w’'-]+\b",text))
if not (ROOT/'app-assets/ie-logo.png').exists():
 import urllib.request
 urllib.request.urlretrieve('https://raw.githubusercontent.com/inactentertainment/ie/main/assets/brand-ie.png',ROOT/'app-assets/ie-logo.png')
s=original('index.html');doc=fragment(s)
header=doc.select_one('.b21StickyBrand');header.select_one('.b20Logo img')['src']='/app-assets/header-logo.webp'
for a in header.select('a[href^="#"]'):a['href']='/'+a['href']
for a in header.select('a'):
 if a.get('href')=='/#blog':a['href']='/articles/';a.string='Articles'
header_html=str(header)
policies=dict(re.findall(r'(privacy|terms|affiliate|cookies|accessibility):\s*`([\s\S]*?)`',s));assert len(policies)==5
footer='''<footer class="footer phg-footer"><div class="phg-footer-main"><div class="phg-footer-brand"><a href="/" aria-label="Perennial home"><img src="/app-assets/header-logo.webp" alt="Perennial Home &amp; Gardens"></a><p>Plan it. Grow it. Live it.</p></div><nav class="phg-footer-nav" aria-label="Footer navigation"><a href="/#tools">Garden Apps</a><a href="/#services">Services</a><a href="/#courses">Courses</a><a href="/#shop">Garden Structures</a><a href="/#free-resources">Free Resources</a><a href="/#products">Perennial Collection</a><a href="/articles/">Articles</a><a href="/#about">About</a><a href="/#contact">Contact</a></nav></div><div class="phg-footer-bottom"><nav class="footerLegal" aria-label="Legal and installation"><a href="/legal/privacy.html">Privacy Policy</a><a href="/legal/terms.html">Terms of Use</a><a href="/legal/affiliate.html">Affiliate Disclosure</a><a href="/legal/cookies.html">Cookie Notice</a><a href="/legal/accessibility.html">Accessibility</a></nav><nav class="phg-socials" aria-label="Shops and social"><a href="https://pin.it/5lgbMVS4S" target="_blank" rel="noopener">Pinterest</a><a href="https://perennialhomegardens.etsy.com" target="_blank" rel="noopener">Etsy</a><a href="https://www.redbubble.com/people/perennialhandg/shop" target="_blank" rel="noopener">Redbubble</a></nav></div><p class="phg-footer-copy">© 2026 Perennial Home &amp; Gardens LLC. Product links currently go directly to vendors. Reserved partner spaces are not active advertisements.</p></footer>'''
def set_footer(d):
 old=d.find('footer');n=fragment(footer).footer
 if old:old.replace_with(n)
 else:d.body.append(n)
(ROOT/'app-assets/footer.html').write_text(footer)
photos={};cards=doc.select('#blog .blogSlideCard');assert len(cards)==9
(ROOT/'articles/images').mkdir(parents=True,exist_ok=True)
for i,c in enumerate(cards):
 image=c.find('img');src=image['src']
 if src.startswith('data:'):
  meta,data=src.split(',',1);ext=meta.split('/')[1].split(';')[0].replace('jpeg','jpg')
  path=Path('articles/images')/('story-'+str(i)+'.'+ext);(ROOT/path).write_bytes(base64.b64decode(data));src='/'+str(path)
 photos[20+i]=src
# Explicit app routes supersede the accumulated label-matching event handlers.
for script in list(doc.find_all('script',id=True)):
 if re.match(r'phg-(seasonal-calendar|garden-calculator|plant-companions|harvest-checker|harvest|growing-zone|garden-library)-(link|nav|route|routing)',script['id']):script.decompose()
routes={'My Growing Zone':'growing-zone','Map Garden Space':'garden-planner','Garden Calculator':'garden-calculator','Plant Companions':'plant-companions','Seasonal Calendar':'seasonal-calendar','Plant Identifier':'plant-identifier','Harvest Checker':'harvest-checker','Garden Library':'garden-library'}
unlock='<span class="phg-free-tag"><svg viewBox="0 0 20 20" aria-hidden="true"><rect x="4" y="9" width="12" height="9" rx="2"/><path d="M7 9V5a4 4 0 0 1 7-2"/></svg>Free tool</span>'
for c in doc.select('#tools .creamTool'):
 name=c.find('h3').get_text(strip=True);c.name='a';c['href']='/tools/'+routes[name]+'/'
 c.attrs.pop('onclick',None);c.attrs.pop('title',None);c.append(fragment(unlock))
open_routes={'OPEN HARVEST RECORDS':'harvest-records','OPEN MY GROWING ZONE':'growing-zone','OPEN GARDEN PLANNER':'garden-planner','OPEN GARDEN CALCULATOR':'garden-calculator','OPEN PLANT COMPANIONS':'plant-companions','OPEN SEASONAL CALENDAR':'seasonal-calendar','OPEN IDENTIFIER':'plant-identifier','OPEN GARDEN IDENTIFIER':'plant-identifier','OPEN HARVEST':'harvest-checker','OPEN GARDEN LIBRARY':'garden-library','OPEN LIBRARY':'garden-library'}
for n in list(doc.select('a,button')):
 for label,path in open_routes.items():
  if n.get_text(' ',strip=True).upper().startswith(label):
   n.name='a';n['href']='/tools/'+path+'/';n.attrs.pop('onclick',None);n.attrs.pop('type',None);break
for p in doc.select('.b17AppIsland'):
 p['inert']='';p['aria-label']='Visual app preview';p['class']=p.get('class',[])+['phg-preview-surface']
 caption=doc.new_tag('p',attrs={'class':'phg-preview-caption'});caption.string='App preview · Open the free tool to use it';p.insert_after(caption)
for dup in doc.find_all(id='garden-library')[:-1]:dup.decompose()
doc.select_one('#blog .head h2').string='Learn it. Grow it. Make it your own.'
for k in doc.select('#blog .kicker'):
 if 'Blog' in k.get_text():k.string='Articles for learning'
intro=doc.new_tag('p');intro.string='In-depth garden articles with clear steps, useful visuals, videos and questions to help you put each idea into practice.';doc.select_one('#blog .head').append(intro)
articles=[]
for path in sorted((ROOT/'content/manuscripts').glob('article-*.json')):
 data=json.loads(path.read_text());articles+=data if isinstance(data,list) else [data]
articles.sort(key=lambda a:a['id']);assert [a['id'] for a in articles]==list(range(29)),[a['id'] for a in articles]
for a in articles:
 a['words']=wc(a);assert a['words']>=3000,(a['id'],a['words'])
 a['slug']=slug(a['title']);a['url']='/articles/'+a['slug']+'.html'
 assert len(a['quiz'])>=3 and a['pretest'] and a['sources']
 for q in a['pretest']+a['quiz']:assert 0<=q['answer']<len(q['options'])
for i,c in enumerate(cards):
 for n in c.select('button,a'):n.name='a';n['href']=articles[20+i]['url'];n.attrs.pop('onclick',None);n.attrs.pop('type',None)
for n in doc.select('[onclick*="showAllBlogs"]'):n.name='a';n['href']='/articles/';n.attrs.pop('onclick',None)
for n in doc.select('a[href="#blog"]'):n['href']='/articles/';n.string='Articles'
set_footer(doc);s=str(doc)
for name,replacement in [('renderBlogs','function renderBlogs(){}'),('article',"function article(i){location.href='/articles/';}"),('showAllBlogs',"function showAllBlogs(){location.href='/articles/';}")]:s=re.sub(r'function '+name+r'\([^\n]*?\)\{[^\n]*\}',lambda m:replacement,s,count=1)
s=s.replace("function drawGardens(){let g=","function drawGardens(){const gc=document.getElementById('gc'),gardens=document.getElementById('gardens');if(!gc||!gardens)return;let g=")
s=s.replace("if(localStorage.phg_zone){zone.value=localStorage.phg_zone;zm.textContent=localStorage.phg_zone}","if(localStorage.phg_zone&&document.getElementById('zone')&&document.getElementById('zm')){zone.value=localStorage.phg_zone;zm.textContent=localStorage.phg_zone}")
s=re.sub(r'(app-assets/install\.js)(?:\?[^"\s<>]*)?',r'\1?v=20261020-final',s)
redirect='<script>window.article=function(i){var urls='+json.dumps([a['url'] for a in articles[:20]])+';location.href=urls[i]||"/articles/";};</script>'
s=s.replace('</body>',redirect+'</body>',1);(ROOT/'index.html').write_text(s)
def shell(title,body,reader=False):
 styles='<link rel="stylesheet" href="/app-assets/articles.css"><link rel="stylesheet" href="/app-assets/site-experience.css?v=20261020-final">'
 scripts='<script src="/app-assets/install.js?v=20261020-final" defer></script><script src="/app-assets/article-learning.js" defer></script>'
 if reader:
  for f in ['read-aloud.css','reader-comfort.css','reader-brand.css']:styles+='<link rel="stylesheet" href="/app-assets/'+f+'">'
  for f in ['reader-setup.js','read-aloud.js','reader-comfort.js']:scripts+='<script src="/app-assets/'+f+'" defer></script>'
 return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+esc(title)+' | Perennial Home &amp; Gardens</title><meta name="description" content="'+esc(title+' — practical garden learning from Perennial.')+'">'+styles+scripts+'</head><body'+(' data-reader="true" class="article-page lights-on"' if reader else '')+'>'+header_html+body+footer+'</body></html>'
def artwork(a):
 if a['id'] in photos:return photos[a['id']]
 t=a['title'].lower();mode='greenhouse' if 'greenhouse' in t or 'tunnel' in t else 'water' if 'water' in t else 'bed' if 'bed' in t or 'lawn' in t else 'flower' if 'flower' in t or 'lavender' in t else 'leaf'
 shapes={'greenhouse':'<path d="M160 310V160L320 65l160 95v150ZM160 160h320M320 65v245M240 112v198M400 112v198M160 230h320"/>','water':'<path d="M320 75C285 140 220 195 220 250a100 100 0 0 0 200 0c0-55-65-110-100-175Z"/>','bed':'<path d="m120 250 220-80 200 75-220 85ZM120 250v55l200 85 220-85v-60M320 330v60"/><path d="M320 250v-85m0 40q-65 0-65-55 65 0 65 55m0 0q65 0 65-55-65 0-65 55"/>','flower':'<path d="M320 350V175"/><ellipse cx="320" cy="115" rx="22" ry="65"/><ellipse cx="320" cy="115" rx="22" ry="65" transform="rotate(60 320 115)"/><ellipse cx="320" cy="115" rx="22" ry="65" transform="rotate(120 320 115)"/><circle cx="320" cy="115" r="22"/>','leaf':'<path d="M320 350V95M320 180q-110 0-110-85 110 0 110 85m0 70q110 0 110-85-110 0-110 85m0 60q-110 0-110-85 110 0 110 85"/>'}
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 420"><title>'+esc(a['title'])+'</title><style>.growth{transform-origin:320px 350px;animation:g 5s ease-in-out infinite alternate}@keyframes g{from{transform:scale(.92);opacity:.6}to{transform:scale(1);opacity:1}}@media(prefers-reduced-motion:reduce){.growth{animation:none}}</style><rect width="640" height="420" fill="#ece8d8"/><circle cx="320" cy="210" r="180" fill="#dee7ce"/><g class="growth" fill="none" stroke="#78966a" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">'+shapes[mode]+'</g></svg>'
 path=Path('articles/images')/(a['slug']+'.svg');(ROOT/path).write_text(svg);return '/'+str(path)
def reserved():return '<aside class="phg-affiliate-space" aria-label="Reserved affiliate partner space"><span aria-hidden="true">❧</span><div><strong>Room for a future garden partner</strong>Affiliate space reserved · thoughtful tools for the way you grow</div></aside>'
def quiz(qs,label,pre=False):
 out='<section class="phg-quiz"'+(' data-pretest' if pre else '')+'><h2>'+label+'</h2><p>'+('Try these first. Notice what you already know.' if pre else 'Check your reasoning. You can try again.')+'</p>'
 for i,q in enumerate(qs):
  out+='<fieldset data-answer="'+str(q['answer'])+'" data-explanation="'+esc(q['explanation'])+'"><legend>'+esc(q['question'])+'</legend>'
  for j,opt in enumerate(q['options']):out+='<label><input type="radio" name="'+('pre' if pre else 'quiz')+str(i)+'" value="'+str(j)+'">'+esc(opt)+'</label>'
  out+='<button type="button" class="phg-check-answer">Check answer</button><output class="phg-feedback" role="status"></output></fieldset>'
 return out+'</section>'
def chart(a):
 c=a['chart'];vals=c['values'];labels=c['labels'];assert len(vals)==len(labels)>0
 maximum=max([float(v) for v in vals]+[1]);w=500/len(vals)
 out='<figure class="phg-chart"><h3>'+esc(c['title'])+'</h3><svg viewBox="0 0 600 300" role="img" aria-label="'+esc(c['title'])+'">'
 for i,v in enumerate(vals):
  h=float(v)/maximum*200;x=50+i*w;out+='<rect x="'+str(x)+'" y="'+str(240-h)+'" width="'+str(w*.65)+'" height="'+str(h)+'" rx="5" fill="#8ba776"/><text x="'+str(x+w*.325)+'" y="'+str(230-h)+'" text-anchor="middle" font-size="14">'+esc(v)+'</text><text x="'+str(x+w*.325)+'" y="270" text-anchor="middle" font-size="12">'+str(i+1)+'</text>'
 out+='</svg><figcaption>'+esc(c['note'])+'</figcaption><table><thead><tr><th>Example</th><th>'+esc(c.get('unit','Value'))+'</th></tr></thead><tbody>'
 return out+''.join('<tr><td>'+esc(label)+'</td><td>'+esc(v)+'</td></tr>' for label,v in zip(labels,vals))+'</tbody></table></figure>'
def video(a):
 v=a.get('video') or json.loads((ROOT/'content/video-fallbacks.json').read_text()).get(str(a['id']))
 assert v and re.fullmatch('[\\w-]{11}',v['id']),(a['id'],'video')
 return '<figure class="phg-video"><h2>Watch it in practice</h2><div class="phg-video-stage"><div><p>'+esc(v['title'])+'</p><button type="button" class="phg-video-play" data-video="'+v['id']+'" data-title="'+esc(v['title'])+'">Play the garden video</button></div></div><figcaption>Video plays here in the article. <a href="'+esc(v['sourceUrl'])+'" target="_blank" rel="noopener">Original video source</a>.</figcaption></figure>'
for a in articles:
 a['image']=artwork(a)
 b='<main class="phg-article-shell"><header class="phg-article-hero"><a href="/articles/">← All articles</a><p class="phg-eyebrow">'+esc(a['category'])+' · Articles for learning</p><h1>'+esc(a['title'])+'</h1><p class="phg-article-dek">'+esc(a['summary'])+'</p><p class="phg-article-meta">'+str(a['words'])+' words · '+str(math.ceil(a['words']/200))+' min read · Read, try, reflect</p><img class="phg-article-art" src="'+a['image']+'" alt="'+esc(a['title'])+'"></header><div class="phg-article-layout"><article class="phg-article-content"><section class="phg-summary"><h2>The useful idea first</h2><p>'+esc(a['summary'])+'</p><h3>What you will be able to do</h3><ul>'+''.join('<li>'+esc(x)+'</li>' for x in a['goals'])+'</ul></section>'+quiz(a['pretest'],'Before you begin',True)+'<section class="phg-learning"><h2>Words worth knowing</h2><dl class="phg-vocabulary">'+''.join('<div><dt>'+esc(x['term'])+'</dt><dd>'+esc(x['meaning'])+'</dd></div>' for x in a['vocabulary'])+'</dl></section>'+reserved()
 toc=[]
 for i,sec in enumerate(a['sections']):
  toc.append('<a href="#lesson-'+str(i)+'">'+esc(sec['heading'])+'</a>');b+='<section><h2 id="lesson-'+str(i)+'">'+esc(sec['heading'])+'</h2>'+''.join('<p>'+esc(p)+'</p>' for p in sec.get('paragraphs',[]))
  if sec.get('steps'):b+='<ol>'+''.join('<li>'+esc(x)+'</li>' for x in sec['steps'])+'</ol>'
  b+='</section>'
  if i==len(a['sections'])//2:b+=chart(a)+video(a)
 b+='<section class="phg-activity"><h2>Try it in your own space</h2><p>'+esc(a['activity'])+'</p><h3>Your next-step checklist</h3><ul>'+''.join('<li>'+esc(x)+'</li>' for x in a['checklist'])+'</ul></section>'+quiz(a['quiz'],'Check your understanding')+reserved()
 related=sorted((x for x in articles if x['id']!=a['id']),key=lambda x:x['category']!=a['category'])[:4]
 b+='<section class="phg-related"><h2>Keep growing your understanding</h2><div>'+''.join('<a href="'+x['url']+'">'+esc(x['title'])+' →</a>' for x in related)+'</div></section><section class="phg-source-list"><h2>References and further reading</h2><p>Original teaching text by Perennial. These references provide deeper detail and local guidance.</p><ul>'+''.join('<li><a href="'+esc(x['url'])+'" target="_blank" rel="noopener">'+esc(x['title'])+'</a></li>' for x in a['sources'])+'</ul></section></article><aside class="phg-article-aside"><b>In this article</b><nav aria-label="Article contents">'+''.join(toc)+'</nav><a href="/tools/my-garden/">Open My Garden →</a></aside></div></main>'
 (ROOT/'articles'/(a['slug']+'.html')).write_text(shell(a['title'],b,True))
catalog=[{k:a[k] for k in ['id','title','slug','url','category','summary','words','image']} for a in articles]
(ROOT/'articles/catalog.json').write_text(json.dumps(catalog,indent=2))
b='<main class="phg-article-shell"><div class="phg-catalog-head"><p class="phg-eyebrow">Articles for learning</p><h1>Good garden ideas. Deeper roots.</h1><p>Clear steps, garden science, useful visuals and small checks for understanding. Choose a topic and try one idea in your own space.</p></div><section class="phg-catalog-feature" aria-label="Seasonal featured article"></section><div class="phg-catalog-controls"><input type="search" id="article-search" placeholder="Find a garden topic" aria-label="Search articles"><select id="article-category" aria-label="Filter by topic"><option value="">All topics</option>'+''.join('<option>'+esc(c)+'</option>' for c in sorted({a['category'] for a in articles}))+'</select></div><p id="article-count" role="status">29 articles</p><div class="phg-catalog-grid">'
for a in articles:b+='<article class="phg-article-card" data-id="'+str(a['id'])+'" data-category="'+esc(a['category'])+'"><img src="'+a['image']+'" alt="'+esc(a['title'])+'" loading="lazy"><div><span class="phg-eyebrow">'+esc(a['category'])+'</span><h2>'+esc(a['title'])+'</h2><p>'+esc(a['summary'])+'</p><a href="'+a['url']+'">Read and explore →</a></div></article>'
(ROOT/'articles/index.html').write_text(shell('Articles for learning',b+'</div></main>'))
(ROOT/'legal').mkdir(exist_ok=True)
for name,copy in policies.items():(ROOT/'legal'/(name+'.html')).write_text(shell(name.title(),'<main class="phg-article-shell"><article class="phg-article-content">'+copy+'</article></main>'))
for page in (ROOT/'tools').glob('*/index.html'):
 source=original(page.relative_to(ROOT))
 # Repair three pre-existing syntax errors exposed by the app regression checks.
 if page.parent.name=='my-garden':source=source.replace(');\\nconst',');\nconst').replace(';\\n const',';\n const').replace('}\\n if','}\n if').replace(');\\n if',');\n if')
 if page.parent.name=='garden-library':source=source.replace('JSON.parse(localStorage.getItem(shelfKey)||"{}")}catch(e){}','JSON.parse(localStorage.getItem(shelfKey)||"{}")}}catch(e){}')
 if page.parent.name=='garden-planner':source=source.replace('Use paths and hose/drip routes to minimize traffic through beds and avoid wetting foliage unnecessarily.</div>\';','Use paths and hose/drip routes to minimize traffic through beds and avoid wetting foliage unnecessarily.</div>";')
 d=fragment(source)
 if page.parent.name=='garden-planner':
  # Recover the app controls removed by the earlier shared-header build.
  previous=fragment(subprocess.check_output(['git','show','bcfb41c:tools/garden-planner/index.html'],cwd=ROOT).decode())
  controls=previous.select_one('header.header');controls['class']=controls.get('class',[])+['phg-planner-controls']
  controls.select_one('a[href*="my-garden"]')['href']='/tools/my-garden/'
  d.select_one('#app .top').insert_after(controls)
  style=d.new_tag('style');style.string='html,body{overflow:auto!important}#app{height:max(620px,calc(100dvh - 94px));grid-template-rows:auto auto minmax(0,1fr)}.phg-planner-controls.header{height:auto;min-height:58px;flex-wrap:wrap}.phg-planner-controls .header-actions{flex-wrap:wrap}@media(max-width:720px){#app{grid-template-rows:auto minmax(0,1fr)}.phg-planner-controls .header-actions{width:100%;margin:0}.phg-planner-controls .header-actions .pill{display:inline-flex!important}}'
  d.head.append(style)
 old=d.select_one('.b21StickyBrand')
 if old:old.replace_with(fragment(header_html))
 else:d.body.insert(0,fragment(header_html))
 set_footer(d)
 if page.parent.name!='my-garden' and not d.select_one('a[href*="my-garden"]'):
  link=d.new_tag('a',attrs={'class':'phg-my-garden-universal','href':'/tools/my-garden/'});link.string='My Garden →';d.select_one('.b21StickyBrand').insert_after(link)
 text=re.sub(r'(app-assets/install\.js)(?:\?[^"\s<>]*)?',r'\1?v=20261020-final',str(d));page.write_text(text)
print('Generated 29 learning articles, article index, 13 app shells, shared footer and legal pages.')
print('Word counts:',json.dumps({a['id']:a['words'] for a in articles}))

import asyncio,threading,http.server,socketserver,json
from datetime import datetime,timedelta,timezone
from pathlib import Path
from bs4 import BeautifulSoup as Soup
from playwright.async_api import async_playwright
ROOT=Path('.')
slugs=['growing-zone','garden-planner','garden-calculator','plant-companions','seasonal-calendar','plant-identifier','harvest-checker','garden-library','seed-starting','garden-journal','harvest-records','garden-inventory']
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=socketserver.TCPServer(('127.0.0.1',8767),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();URL='http://127.0.0.1:8767'
s=Soup(Path('index.html').read_text(),'html.parser')
sections=s.main.select(':scope > section');assert sections[0]['id']=='tools'
assert [n['id'] for n in sections[-3:]]==['blog','about','contact']
assert not s.select('body > section')
assert s.main.find_next_sibling().name=='footer'
links=[a['href'] for a in s.select('#tools .creamTool')];assert links==['/tools/'+x+'/' for x in slugs]
ads=[]
for section in sections:
 if section.get('id')=='tools':continue
 for a in section.select('a[href]'):
  href='/'+a['href'].lstrip('/')
  if href.startswith('/tools/') and href!='/tools/my-garden/':ads.append(href)
assert ads==links,(ads,links)
assert len(s.select('section#garden-planner,section#plant-identifier'))==2
for anchor in ['tool-map','tool-identifier']:assert s.select_one('#'+anchor)
async def main():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch();ctx=await browser.new_context();await ctx.add_init_script("sessionStorage.setItem('phg-b3-resource-offer','1');sessionStorage.setItem('phg-b3-tool-offer','1')")
  page=await ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  await page.goto(URL,wait_until='load');await page.wait_for_selector('#ap[data-enhanced]',state='attached')
  for w in [1440,768,390,360]:
   await page.set_viewport_size({'width':w,'height':844});assert await page.locator('#tools .creamTool').count()==12
   assert await page.locator('#tools .creamTool').evaluate_all('(es)=>es.every(e=>e.scrollWidth<=e.clientWidth+1)'),w
   assert await page.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth+1'),w
   assert await page.locator('#tools .creamTool h3').evaluate_all('(es)=>es.every(e=>e.scrollWidth<=e.clientWidth+1)'),w
  for r in slugs[-4:]:
   await page.goto(URL,wait_until='load');await page.locator('#tools a[href="/tools/'+r+'/"]').click();await page.wait_for_url('**/tools/'+r+'/')
  await page.goto(URL,wait_until='load');await page.set_viewport_size({'width':390,'height':844})
  for anchor in ['blog','about','contact']:
   await page.goto(URL+'/#'+anchor,wait_until='load');assert await page.locator('#'+anchor).is_visible()
  # Returning from app pages keeps the real closing sections in the same DOM order.
  assert await page.locator('main > section').evaluate_all('(es)=>es.slice(-3).map(e=>e.id)')==['blog','about','contact']
  Path('qa').mkdir(exist_ok=True)
  await page.goto(URL,wait_until='load');await page.screenshot(path='qa/home-directory-mobile.png')
  await page.goto(URL+'/#contact',wait_until='load');await page.wait_for_function("document.querySelector('#contact').getBoundingClientRect().top<200");await page.screenshot(path='qa/home-contact-footer-mobile.png')
  print('PASS12 directory routes match12 advertisements, no duplicate ads, closing order and four responsive widths')
  # Fresh article visitor: neither prompt fires early, both contain distinct offers.
  article=await browser.new_context(viewport={'width':390,'height':844});ap=await article.new_page();ap.on('pageerror',lambda e:errors.append(str(e)))
  await ap.clock.install();await ap.clock.pause_at(datetime.now(timezone.utc)+timedelta(seconds=1))
  await ap.goto(URL+'/articles/asparagus-is-a-long-game.html',wait_until='load');await ap.wait_for_function('window.__siteExperience===true')
  await ap.clock.fast_forward(24000);assert await ap.locator('dialog[open]').count()==0
  await ap.clock.fast_forward(1000);d=ap.locator('#phg-resource-prompt');assert await d.is_visible()
  assert await d.get_by_role('radio').count()==2
  await d.get_by_role('radio',name='Houseplant Care Worksheet',exact=False).check()
  assert await d.get_by_role('radio',name='Houseplant Care Worksheet',exact=False).is_checked()
  await d.get_by_role('button',name='Open download folder',exact=True).click();assert await d.is_visible();assert not await d.locator('input[type=email]').evaluate('(e)=>e.validity.valid')
  await d.locator('.x-dialog-heading button').click()
  await ap.clock.fast_forward(94000);assert await ap.locator('#phg-newsletter-prompt').count()==0
  await ap.clock.fast_forward(1000);n=ap.locator('#phg-newsletter-prompt');assert await n.is_visible()
  assert await n.get_by_role('heading',name='Perennial Garden Magazine',exact=True).count()==1
  assert 'Monthly garden ideas, gifts and coupons' in await n.inner_text()
  assert 'Opens your email app' in await n.inner_text()
  await n.locator('.x-dialog-heading button').click();await ap.clock.fast_forward(180000);assert await ap.locator('dialog[open]').count()==0
  await ap.goto(URL+'/articles/mint-without-regret.html',wait_until='load');await ap.clock.fast_forward(120000);assert await ap.locator('dialog[open]').count()==0
  print('PASS article worksheets with two choices at25s, distinct Magazine at120s, invalid-email protection, no repeat across articles')
  assert not errors,errors
  await browser.close();print('PASS no uncaught browser errors')
asyncio.run(main());server.shutdown()

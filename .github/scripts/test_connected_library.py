"""Real-browser checks for the integrated shelf, private notes, help and library microphone."""
import asyncio,json,threading,http.server,socketserver
from pathlib import Path
from bs4 import BeautifulSoup as Soup
from playwright.async_api import async_playwright
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=socketserver.TCPServer(('127.0.0.1',8771),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();URL='http://127.0.0.1:8771'
books=json.loads(Path('books/catalog.json').read_text())['books'];assert len(books)==100
assert books[11]['title']=='From Seed to Skillet' and 'Jimmy Williams' in books[11]['authors']
for b in books:
 assert Path('books/'+b['slug']+'.html').exists() and b['coverUrl'].startswith(('https://','/books/covers/')) and b['verified']
 d=Soup(Path('books/'+b['slug']+'.html').read_text(),'html.parser');assert d.select_one('.phg-book-amazon')['href']==b['amazonUrl'];assert d.select_one('.phg-book-cover')['src']==b['coverUrl']
assert 'phg-integrated-library-link' in Path('garden-books.html').read_text()
async def main():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch();ctx=await browser.new_context();await ctx.add_init_script("sessionStorage.setItem('phg-b3-resource-offer','1');sessionStorage.setItem('phg-b3-tool-offer','1');window.SpeechRecognition=class{start(){this.onstart?.()}stop(){this.onend?.()}abort(){this.onend?.()}};")
  p=await ctx.new_page();errors=[];p.on('pageerror',lambda x:errors.append(str(x)))
  await p.goto(URL+'/tools/garden-library/',wait_until='load');await p.wait_for_selector('.phg-book-card');assert await p.locator('.phg-book-card').count()==25
  first_cover=await p.locator('.phg-book-card img').first.element_handle()
  for total in [50,75,100]:
   await p.locator('#phgBooksMore').click();assert await p.locator('.phg-book-card').count()==total;assert await first_cover.evaluate('(e)=>e.isConnected')
  assert not await p.locator('#phgBooksMore').is_visible()
  await p.locator('#phgBookSearch').fill('Jimmy Williams');assert await p.locator('.phg-book-card').count()==1;assert 'From Seed to Skillet' in await p.locator('.phg-book-card').inner_text()
  await p.locator('.phg-book-card .phg-book-save').click();assert await p.locator('.phg-book-card .phg-book-save').get_attribute('aria-pressed')=='true'
  await p.locator('.phg-book-detail-link').click();await p.locator('#phgBookNotes').fill('Try one crop from seed to a family meal.');await p.locator('#phgBookReadingStatus').select_option('reading');await p.locator('#phgSaveBookNotes').click();await p.reload();assert await p.locator('#phgBookNotes').input_value()=='Try one crop from seed to a family meal.';assert await p.locator('#phgBookReadingStatus').input_value()=='reading'
  await p.goto(URL+'/tools/garden-library/',wait_until='load');await p.locator('#phgUnifiedInput').fill('unfinished search');await p.locator('#phgUnifiedMic').press('Enter');assert await p.locator('#phgUnifiedMic').get_attribute('aria-pressed')=='true';await p.locator('#phgUnifiedMic').press('Enter');assert await p.locator('#phgUnifiedMic').get_attribute('aria-pressed')=='false';assert await p.locator('#phgUnifiedInput').input_value()=='unfinished search'
  assert await p.locator('#phgUnifiedMic svg').count()==1
  for w in [1440,768,390,360]:
   await p.set_viewport_size({'width':w,'height':844});assert await p.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth+1'),('library overflow',w)
   if w==1440:assert await p.locator('#phgBooksGrid').evaluate('(e)=>getComputedStyle(e).gridTemplateColumns.split(" ").length')==5
  await p.goto(URL+'/help/',wait_until='load');assert await p.locator('#gardenGuides details').count()==13;await p.locator('#guideSearch').fill('germination');assert await p.locator('#gardenGuides details:visible').count()==1
  await p.locator('#guideSearch').fill('');await p.locator('#garden-planner summary').click();assert await p.locator('#garden-planner').get_attribute('open') is not None
  for w in [1440,768,390,360]:
   await p.set_viewport_size({'width':w,'height':844});assert await p.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth+1'),('help overflow',w)
  await p.goto(URL+'/tools/my-garden/',wait_until='load');assert await p.locator('.toolgrid .tool').count()==12;assert not await p.get_by_role('heading',name='Coming Next',exact=True).count()
  for w in [1440,390]:
   await p.set_viewport_size({'width':w,'height':844});assert await p.locator('.toolgrid .tool').evaluate_all('(es)=>es.every(e=>Math.abs(e.querySelector(".icon").getBoundingClientRect().top-e.querySelector("b").getBoundingClientRect().top)<20)')
  await p.locator('#gardenName').fill('QA garden');await p.locator('#profileZone').fill('7b');await p.locator('#profileLocation').fill('Maryland');await p.locator('#saveProfile').click();await p.reload();assert await p.locator('#gardenName').input_value()=='QA garden'
  for a in await p.locator('.toolgrid .tool').all():assert (await ctx.request.get(URL+'/tools/'+(await a.get_attribute('href')).split('/')[-2]+'/')).status==200
  await p.goto(URL,wait_until='load');await p.wait_for_selector('#ap[data-enhanced]',state='attached');assert await p.locator('#ap .tanya-help').get_attribute('href')=='/help/';assert await p.locator('#navlinks a[href="/help/"]').count()==1;assert await p.locator('footer a[href="/help/"]').count()==1
  assert await p.locator('#services article img[src*="approved-home"]').count()==3;assert await p.locator('#shop article img[src*="approved-home"]').count()==3;
  for image in await p.locator('#services article img,#shop article img').all():
   response=await ctx.request.get(URL+await image.get_attribute('src'));assert response.status==200;assert (await response.body()).startswith(b'RIFF')
  assert await p.locator('#courses .courseStrip').count()==0;assert await p.locator('#courses .phg-course-photo').count()==3
  await p.goto(URL+'/garden-books.html',wait_until='load');assert await p.locator('.b21StickyBrand').count()==1;assert await p.locator('footer.phg-footer').count()==1;assert await p.locator('#phg-integrated-library-link').count()==1
  assert not errors,errors
  await browser.close()
  print('PASS 100 real catalog records and guide routes;25→50→75→100;search;private reading list;notes persist;silver SVG microphone and mocked start/stop;unfinished search preserved;5 columns desktop;mobile/tablet layout;13 searchable guides;12 dashboard tool routes;profile persistence;help entry points;course title placement. Real speech permission/dictation and every remote cover image are not claimed tested.')
asyncio.run(main());server.shutdown()

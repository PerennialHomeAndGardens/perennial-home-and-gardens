import asyncio,json,threading,http.server,socketserver,re
from pathlib import Path
from playwright.async_api import async_playwright
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=socketserver.TCPServer(('127.0.0.1',8766),Handler);threading.Thread(target=server.serve_forever,daemon=True).start();URL='http://127.0.0.1:8766'
async def main():
 async with async_playwright() as p:
  browser=await p.chromium.launch();ctx=await browser.new_context();await ctx.add_init_script("sessionStorage.setItem('phg-b3-resource-offer','1');sessionStorage.setItem('phg-b3-tool-offer','1')")
  page=await ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(page.url+' '+str(e)))
  await page.goto(URL,wait_until='load');await page.wait_for_selector('#ap[data-enhanced]',state='attached')
  assert await page.locator('.phg-free-tag,.phg-preview-caption').count()==0
  assert await page.locator('.b17PreviewInner').evaluate_all('(es)=>es.every(e=>e.children.length===2)')
  assert not re.search(r'\bfree\b',await page.locator('h1').inner_text(),re.I)
  for width in [1440,768,390,360]:
   await page.set_viewport_size({'width':width,'height':900})
   assert await page.locator('.b17PreviewInner').evaluate_all('(es)=>es.every(e=>e.getBoundingClientRect().width<=innerWidth+1)')
   for item in await page.locator('.b17PreviewInner').all():
    boxes=await item.evaluate('(e)=>Array.from(e.children).map(n=>{const r=n.getBoundingClientRect();return{x:r.x,y:r.y,r:r.right,b:r.bottom}})')
    a,b=boxes;assert a['r']<=b['x']+2 or a['b']<=b['y']+2 or b['r']<=a['x']+2 or b['b']<=a['y']+2,(width,boxes)
  print('PASS six preview layouts have two children and no overlapping columns at four widths')
  await page.set_viewport_size({'width':390,'height':844})
  footer=page.locator('footer');assert await footer.locator('.phg-footer-bottom').evaluate('(e)=>getComputedStyle(e).borderTopWidth')=='0px'
  assert await footer.locator('.phg-footer-bottom').evaluate('(e)=>getComputedStyle(e).backgroundImage')=='none'
  for name in ['Pinterest','Etsy','Redbubble']:
   a=footer.get_by_role('link',name=name,exact=True);assert await a.locator('svg').count()==1;assert await a.inner_text()==''
  assert await footer.locator('.phg-socials a svg').evaluate_all('(es)=>es.every(e=>getComputedStyle(e).fill===getComputedStyle(e.parentElement).color)')
  # Source rendering is stable even if the late enhancement script cannot load.
  early=await browser.new_context(viewport={'width':390,'height':844});await early.route('**/site-experience.js*',lambda r:r.abort());ep=await early.new_page()
  await ep.goto(URL+'/tools/growing-zone/',wait_until='load');assert await ep.locator('.b21StickyBrand').evaluate('(e)=>Math.round(e.getBoundingClientRect().height)')==94
  assert await ep.locator('.b20Logo img').evaluate('(e)=>Math.round(e.getBoundingClientRect().height)')==80
  assert await ep.locator('.b20WoodBar .newActions').count()==1;assert await ep.locator('.b21StickyBrand > .nav').count()==0
  await early.close();print('PASS compact header exists before enhancement; no old large-logo markup layout')
  # An actual tool click animates; scrolling/hash and reduced-motion navigation do not.
  await page.locator('#tools a[href="/tools/growing-zone/"]').click();await page.wait_for_selector('.phg-portal.active');await page.wait_for_url('**/tools/growing-zone/')
  assert await page.get_by_role('link',name='Go back',exact=True).count()==1
  assert await page.locator('.phg-back').evaluate('(e)=>getComputedStyle(e).borderTopWidth')=='0px'
  await page.get_by_role('link',name='Go back',exact=True).click();await page.wait_for_url(URL+'/');await page.wait_for_timeout(100);assert await page.locator('.phg-portal').count()==0
  await page.get_by_role('link',name='Explore Tools',exact=True).click();assert await page.locator('.phg-portal').count()==0
  await page.emulate_media(reduced_motion='reduce');await page.locator('#tools a[href="/tools/garden-calculator/"]').click();await page.wait_for_url('**/tools/garden-calculator/');assert await page.locator('.phg-portal').count()==0
  await page.emulate_media(reduced_motion='no-preference');print('PASS app-entry transition, history arrow, hash-link exclusion and reduced-motion path')
  direct=await ctx.new_page();await direct.goto(URL+'/tools/plant-companions/',wait_until='load');await direct.locator('.phg-back').click();await direct.wait_for_url('**/#tools');await direct.close();print('PASS direct-entry back-arrow fallback')
  await page.goto(URL,wait_until='load');await page.wait_for_selector('#ap[data-enhanced]',state='attached');await page.get_by_role('button',name='Open Tanya garden guide',exact=True).press('Enter')
  assert await page.locator('.tanya-categories button').count()==2;assert await page.locator('.tanya-question').count()==5
  base=json.loads(Path('app-assets/tanya-knowledge.json').read_text());aliases=json.loads(Path('app-assets/tanya-business-aliases.json').read_text());experts=json.loads(Path('app-assets/tanya-expert-knowledge.json').read_text());answers={e['id']:e['answer'] for e in base['entries']}
  assert len(aliases)>=100 and len(experts)==60
  for e in aliases:
   await page.evaluate('(q)=>{document.getElementById("q").value=q;return ask();}',e['question']);assert answers[e['answerId']] in await page.locator('#chat .bubble').last.inner_text(),e['question']
  for e in experts:
   await page.evaluate('(q)=>{document.getElementById("q").value=q;return ask();}',e['question']);assert e['answer'] in await page.locator('#chat .bubble').last.inner_text(),e['question']
  print('PASS all114 supported business/tool phrasings and60 expert answer records')
  for q,expected in [('What family is Salvia officinalis in?','Lamiaceae'),('What does abaxial mean?','underside'),('Which plants have pink flowers in spring and partial shade?','Examples from the Library')]:
   await page.locator('#q').fill(q);await page.get_by_role('button',name='Send',exact=True).click();await page.wait_for_timeout(100);assert expected.lower() in (await page.locator('#chat .bubble').last.inner_text()).lower(),q
  index=json.loads(Path('app-assets/tanya-botany-index.json').read_text());assert len(index['plants'])==2703 and sum(x[6] for x in index['plants'])==838
  assert Path('app-assets/tanya-botany-index.json.gz').stat().st_size<115000
  print('PASS compressed plant taxonomy/care, glossary definition and trait-filter lookups')
  # Exercise the existing photo flow with a deterministic local image, not a species-identification claim.
  await page.goto(URL+'/tools/plant-identifier/',wait_until='load');assert await page.get_by_role('heading',name='1. Upload plant photos',exact=True).count()==1
  import base64
  png=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jQ1sAAAAASUVORK5CYII=')
  await page.locator('#photo-close').set_input_files({'name':'photo-test.png','mimeType':'image/png','buffer':png});await page.wait_for_function('document.querySelector("#qualityList").textContent.includes("1×1")')
  assert 'Close-up' in await page.locator('#qualityList').inner_text();assert await page.locator('#img-close').is_visible()
  await page.locator('[data-remove-photo="close"]').click();assert not await page.locator('#img-close').is_visible();print('PASS photo upload, correctly labeled quality review and removal')
  assert not errors,errors
  Path('qa').mkdir(exist_ok=True)
  await page.goto(URL+'/tools/garden-planner/',wait_until='load');await page.screenshot(path='qa/polish-app-mobile.png')
  await page.goto(URL+'/#tool-map',wait_until='load');await page.screenshot(path='qa/polish-map-preview-mobile.png')
  await page.locator('.phg-socials a').first.focus();await page.screenshot(path='qa/polish-footer-mobile.png')
  await browser.close();print('PASS no uncaught browser errors')
asyncio.run(main());server.shutdown()

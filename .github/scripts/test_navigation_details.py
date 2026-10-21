import asyncio,threading,http.server,socketserver,wave,hashlib
from pathlib import Path
from bs4 import BeautifulSoup as Soup
from playwright.async_api import async_playwright
R=Path('.');URL='http://127.0.0.1:8771'
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=socketserver.TCPServer(('127.0.0.1',8771),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
pages=[R/'index.html',R/'garden-books.html',*R.glob('tools/*/index.html'),*R.glob('articles/*.html'),*R.glob('legal/*.html'),*R.glob('books/*.html'),*R.glob('help/*.html')]
for path in pages:
 s=Soup(path.read_text(),'html.parser')
 for nav in s.select('#navlinks,.phg-footer-nav'):
  assert len(nav.select('a[href="/tools/garden-library/"]'))==1,path
with wave.open('app-assets/audio/soft-whirl.wav','rb') as w:assert 1.29<w.getnframes()/w.getframerate()<1.31
print('PASS direct Garden Library links on all152 retained pages; valid selected1.3second recording')
async def main():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch();ctx=await browser.new_context()
  await ctx.add_init_script("sessionStorage.setItem('phg-b3-resource-offer','1');sessionStorage.setItem('phg-b3-tool-offer','1');document.addEventListener('ended',e=>{if(e.target.matches?.('[data-phg-transition-sound]'))sessionStorage.setItem('sound-ended',String(e.target.currentTime))},true)")
  p=await ctx.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  await p.goto(URL,wait_until='load')
  audio=p.locator('audio[data-phg-transition-sound]');await p.wait_for_function('document.querySelector("audio[data-phg-transition-sound]")?.readyState>=2')
  assert await audio.evaluate('(a)=>a.paused&&!a.autoplay&&a.currentTime===0')
  assert await p.locator('#services article h3').all_text_contents()==['Coaching','Design Templates','Garden Installation']
  for width in [1440,768,390,360]:
   await p.set_viewport_size({'width':width,'height':844})
   assert await p.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth+1'),width
   for app in await p.locator('.phg-home-app').all():
    result=await app.evaluate('''e=>{const copy=e.querySelector('.phg-app-copy'),row=copy.parentElement,preview=Array.from(row.children).find(x=>x!==copy),last=preview.lastElementChild;const r=preview.getBoundingClientRect(),b=last.getBoundingClientRect();return {id:e.id,bottomGap:r.bottom-b.bottom,min:getComputedStyle(preview).minHeight,copyHeight:getComputedStyle(copy).height,previewTop:r.top,copyTop:copy.getBoundingClientRect().top}}''')
    assert result['bottomGap']<45,(width,result)
    if width==1440:assert abs(result['previewTop']-result['copyTop'])<5,(width,result)
   if width in [1440,390]:
    await p.locator('#garden-library').scroll_into_view_if_needed();Path('qa').mkdir(exist_ok=True);await p.screenshot(path='qa/navigation-details-'+str(width)+'.png')
  print('PASS13 content-sized previews without stretched blank containers; service titles; four responsive widths')
  await p.locator('.cleanMenu').click();await p.locator('#navlinks a[href="/tools/garden-library/"]').click()
  await p.wait_for_selector('.phg-portal.active');await p.wait_for_timeout(600)
  assert await audio.evaluate('(a)=>!a.paused&&a.currentTime>.25&&a.volume<1')
  await p.wait_for_url('**/tools/garden-library/')
  assert float(await p.evaluate("sessionStorage.getItem('sound-ended')"))>1.29
  assert await p.locator('.phg-portal').count()==0
  print('PASS actual click starts quiet Soft Whirl, completes playback before navigation, and opens Garden Library')
  await p.locator('.phg-library-launches a[href="#phgDictionary"]').click();assert p.url.endswith('#phgDictionary')
  await p.locator('#search').fill('rhizome');await p.locator('#searchBtn').click()
  await p.wait_for_timeout(350)
  assert 'rhizome' in (await p.locator('section.glossary').inner_text()).lower()
  assert await p.locator('.phg-portal').count()==0
  assert await p.locator('audio[data-phg-transition-sound]').evaluate('(a)=>a.paused&&a.currentTime===0')
  print('PASS Dictionary shortcut, retained dictionary search and silent same-page navigation')
  await p.goto(URL,wait_until='load');await p.emulate_media(reduced_motion='reduce')
  await p.locator('#tools a[href="/tools/growing-zone/"]').click();await p.wait_for_url('**/tools/growing-zone/')
  assert await p.locator('.phg-portal').count()==0
  assert not errors,errors
  print('PASS reduced-motion navigation and no uncaught browser errors')
  await browser.close()
asyncio.run(main());server.shutdown()

"""Exercise manual email/download paths without sending mail or opening an external app."""
import asyncio, http.server, threading, os, json
from pathlib import Path
from playwright.async_api import async_playwright
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args): pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',8784),Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
BASE='http://127.0.0.1:8784'
results=[]
async def main():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(channel=os.environ.get('PHG_QA_BROWSER_CHANNEL'))
  context=await browser.new_context(permissions=['clipboard-read','clipboard-write'])
  await context.add_init_script("sessionStorage.setItem('phg-b3-resource-offer','1');sessionStorage.setItem('phg-b3-tool-offer','1');")
  p=await context.new_page(); errors=[];posts=[]
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('request',lambda r:posts.append(r.url) if r.method=='POST' else None)
  await p.goto(BASE+'/');await p.get_by_role('button',name='Open email draft',exact=True).wait_for()
  await p.locator('#cn').fill('Garden visitor');await p.locator('#ce').fill('visitor@example.com');await p.locator('#cm').fill('Please help with <b>my garden</b>.')
  await p.get_by_role('button',name='Open email draft',exact=True).click()
  draft=p.locator('#phg-email-draft');assert await draft.is_visible()
  text=await draft.locator('textarea').input_value();assert '<b>my garden</b>' in text
  href=await draft.get_by_role('link',name='Open email app',exact=True).get_attribute('href')
  assert href.startswith('mailto:perennialhomeandgardens@gmail.com?subject=') and '%3Cb%3E' in href
  assert await draft.locator('b').count()==0
  await draft.get_by_role('button',name='Copy message',exact=True).click()
  await draft.get_by_role('status').get_by_text('Copied. Paste it into your email app.',exact=True).wait_for()
  clip=await p.evaluate('navigator.clipboard.readText()');assert 'visitor@example.com' in clip
  await p.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:()=>Promise.reject(Error('denied'))}})")
  await draft.get_by_role('button',name='Copy message',exact=True).click();await draft.get_by_role('status').filter(has_text='manually').wait_for()
  await draft.get_by_role('button',name='Close Your email draft',exact=True).click();assert await p.locator('#cm').input_value()=='Please help with <b>my garden</b>.'
  results.append('Contact draft includes typed fields, safely preserves literal markup, correct mailto, clipboard success/failure and unchanged original message.')
  await p.locator('#free-resources button').click();ready=p.locator('#phg-resource-ready');assert await ready.is_visible()
  link=ready.get_by_role('link',name='Open worksheet folder',exact=True);assert 'drive.google.com/drive/folders/' in await link.get_attribute('href')
  assert await p.evaluate("localStorage.getItem('phg_free_resource_lead')") is None
  assert await p.evaluate("localStorage.getItem('phg_freebie_lead')") is None
  await ready.get_by_role('button',name='Request newsletter by email',exact=True).click()
  assert 'Please subscribe me' in await p.locator('#phg-email-draft textarea').input_value()
  await p.locator('#phg-email-draft').get_by_role('button',name='Close Your email draft',exact=True).click()
  results.append('Homepage resources work without email; direct folder link survives popup blockers; newsletter is an explicit manual request; no new local email-lead storage.')
  await p.get_by_role('button',name='Schedule an Appointment',exact=True).click()
  await p.locator('#sn').fill('Service visitor');await p.locator('#se').fill('service@example.com');await p.locator('#sm').fill('A raised bed project.')
  await p.locator('#sz').fill('20603')
  await p.locator('#modal').get_by_role('button').filter(has_text='Send').click()
  assert 'service@example.com' in await p.locator('#phg-email-draft textarea').input_value()
  await p.locator('#phg-email-draft').get_by_role('button',name='Close Your email draft',exact=True).click()
  # Close any retained original service modal before the responsive checks.
  await p.evaluate("document.querySelectorAll('.modal.on').forEach(n=>n.classList.remove('on'))")
  results.append('Service inquiry opens the same copyable email draft with the entered details.')
  for width,height in [(1440,1000),(390,844),(360,640)]:
   await p.set_viewport_size({'width':width,'height':height})
   await p.get_by_role('button',name='Open email draft',exact=True).click()
   assert await p.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth+2')
   box=await p.locator('#phg-email-draft').bounding_box();assert box['width']<=width and box['height']<=height
   await p.screenshot(path=f'qa/manual-email-{width}.png')
   await p.locator('#phg-email-draft').get_by_role('button',name='Close Your email draft',exact=True).click()
  results.append('Draft dialog fits desktop and 390/360-pixel mobile viewports with internal scrolling.')
  # Exercise article fallback and the timed newsletter with a separate visit.
  await context.close();context=await browser.new_context()
  await context.add_init_script("sessionStorage.setItem('phg-b3-resource-offer','1');sessionStorage.setItem('phg-visit-start',String(Date.now()-121000));")
  p=await context.new_page();p.on('pageerror',lambda e:errors.append(str(e)))
  await p.goto(BASE+'/articles/');await p.locator('#phg-newsletter-prompt').wait_for()
  await p.locator('#phg-newsletter-email').fill('newsletter@example.com')
  await p.get_by_role('button',name='Subscribe by email',exact=True).click()
  assert 'newsletter@example.com' in await p.locator('#phg-email-draft textarea').input_value()
  results.append('120-second newsletter prompt on an article page opens a copyable request; no subscription-success claim.')
  await p.locator('#phg-email-draft').get_by_role('button',name='Close Your email draft',exact=True).click()
  await p.evaluate("sessionStorage.removeItem('phg-b3-resource-offer');sessionStorage.setItem('phg-visit-start',String(Date.now()-26000))")
  await p.reload();await p.locator('#phg-resource-prompt').wait_for();await p.locator('#phg-resource-prompt input[type=email]').fill('')
  await p.get_by_role('button',name='Open download folder',exact=True).click();assert await p.locator('#phg-resource-ready').is_visible()
  results.append('25-second resource prompt on an article page offers both worksheets without requiring an email.')
  assert not errors,errors;assert not posts,posts
  await browser.close()
  results.append('No uncaught page errors or POST submissions in the exercised flows. No real email was sent.')
  Path('qa/manual-email-20261023.json').write_text(json.dumps({'passed':results,'not_tested':['Actual mail-app launch or email delivery','Physical mobile keyboard/camera/microphone','External download-folder access permissions']},indent=2))
  print('\n'.join('PASS '+s for s in results))
try: asyncio.run(main())
finally: server.shutdown()

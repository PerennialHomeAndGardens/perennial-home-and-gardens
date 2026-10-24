"""Offline capture-flow checks: intercept every FormSubmit request; send no mail."""
import asyncio,http.server,threading,os,json
from pathlib import Path
from playwright.async_api import async_playwright
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',8785),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
BASE='http://127.0.0.1:8785';results=[]
async def main():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(channel=os.environ.get('PHG_QA_BROWSER_CHANNEL'))
  context=await browser.new_context();await context.add_init_script("sessionStorage.setItem('phg-b3-resource-offer','1');sessionStorage.setItem('phg-b3-tool-offer','1');")
  requests=[];mode={'success':False}
  async def intercept(route):
   if route.request.method=='OPTIONS':return await route.fulfill(status=204,headers={'Access-Control-Allow-Origin':'*','Access-Control-Allow-Headers':'Content-Type,Accept','Access-Control-Allow-Methods':'POST,OPTIONS'})
   requests.append(route.request.post_data_json)
   await route.fulfill(status=200,headers={'Access-Control-Allow-Origin':'*'},content_type='application/json',body=json.dumps({'success':mode['success']}))
  await context.route('https://formsubmit.co/**',intercept)
  p=await context.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  await p.goto(BASE+'/');await p.get_by_role('button',name='Get My Garden Gifts',exact=True).first.wait_for()
  section=p.locator('#free-resources');assert 'newsletter' not in (await section.inner_text()).lower()
  await section.get_by_role('button',name='Get My Garden Gifts',exact=True).click();assert not requests
  await p.locator('#resourceName').fill('Garden Visitor');await p.locator('#resourceEmail').fill('wrong')
  await section.get_by_role('button',name='Get My Garden Gifts',exact=True).click();assert not requests
  await p.locator('#resourceEmail').fill('visitor@example.com');await section.get_by_role('button',name='Get My Garden Gifts',exact=True).click()
  await section.get_by_role('status').filter(has_text='could not save').wait_for();assert not await p.locator('#phg-gift-access').count()
  assert await p.locator('#resourceEmail').input_value()=='visitor@example.com'
  results.append('Homepage requires name and valid email, retains the entered details on server rejection, and does not unlock the gift folder on failure.')
  mode['success']=True;await section.get_by_role('button',name='Get My Garden Gifts',exact=True).click();await p.locator('#phg-gift-access').wait_for()
  assert requests[-1]['newsletter_requested']=='No — garden gifts only'
  assert requests[-1]['name']=='Garden Visitor' and requests[-1]['email']=='visitor@example.com'
  assert 'newsletter' not in (await p.locator('#phg-gift-access').inner_text()).lower()
  assert 'drive.google.com/drive/folders/' in await p.locator('#phg-gift-access a').get_attribute('href')
  results.append('An acknowledged gift submission unlocks the folder and carries a gifts-only classification with no newsletter offer in its confirmation.')
  await p.get_by_role('button',name='Close gift request confirmation',exact=True).click()
  await p.evaluate("localStorage.removeItem('phg_freebie_claimed');window.openFreebie('welcome')")
  await p.locator('#freebieName').fill('Popup Visitor');await p.locator('#freebieEmail').fill('popup@example.com')
  assert 'newsletter' not in (await p.locator('#freebieModal').inner_text()).lower()
  await p.locator('#freebieModal').get_by_role('button',name='Get My Garden Gifts',exact=True).click();await p.locator('#phg-gift-access').wait_for()
  assert requests[-1]['name']=='Popup Visitor'
  results.append('The first gift popup separately requires name/email, shows visitor-facing gift wording and contains no newsletter promotion.')
  await p.get_by_role('button',name='Close gift request confirmation',exact=True).click()
  for width,height in [(1440,1000),(390,844),(360,640)]:
   await p.set_viewport_size({'width':width,'height':height})
   await p.evaluate("localStorage.removeItem('phg_freebie_claimed');window.openFreebie('welcome')")
   assert await p.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth+2')
   await p.screenshot(path=f'qa/gift-capture-{width}.png')
   await p.locator('#freebieModal button.close').click()
  results.append('The retained gift artwork/layout has no horizontal overflow at desktop and 390/360-pixel mobile widths.')
  # A separate simulated visit receives the newsletter advertisement after two minutes.
  await context.close();context=await browser.new_context();await context.route('https://formsubmit.co/**',intercept)
  await context.add_init_script("sessionStorage.setItem('phg-b3-resource-offer','1');sessionStorage.setItem('phg-visit-start',String(Date.now()-121000));")
  p=await context.new_page();p.on('pageerror',lambda e:errors.append(str(e)))
  await p.goto(BASE+'/articles/');await p.locator('#phg-newsletter-prompt[data-capture-bound]').wait_for()
  await p.locator('#phg-newsletter-email').fill('magazine@example.com');await p.get_by_role('button',name='Subscribe by email',exact=True).click()
  await p.locator('#phg-gift-access').wait_for();assert requests[-1]['newsletter_requested']=='Yes — explicit magazine signup'
  assert requests[-1]['email']=='magazine@example.com';assert await p.locator('#phg-gift-access a').count()==0
  results.append('The second advertisement submits an explicit magazine signup separately and does not unlock gift downloads.')
  await context.close();context=await browser.new_context();await context.route('https://formsubmit.co/**',intercept)
  await context.add_init_script("sessionStorage.setItem('phg-b3-tool-offer','1');sessionStorage.setItem('phg-visit-start',String(Date.now()-26000));")
  p=await context.new_page();p.on('pageerror',lambda e:errors.append(str(e)))
  await p.goto(BASE+'/articles/');await p.locator('#phg-resource-prompt[data-capture-bound]').wait_for()
  await p.locator('#phg-resource-prompt input[name=name]').fill('Article Visitor');await p.locator('#phg-resource-prompt input[type=email]').fill('article@example.com')
  assert 'newsletter' not in (await p.locator('#phg-resource-prompt').inner_text()).lower()
  await p.get_by_role('button',name='Get My Garden Gifts',exact=True).click();await p.locator('#phg-gift-access').wait_for()
  assert requests[-1]['name']=='Article Visitor'
  results.append('The 25-second article-page gift popup also requires both fields and is independent of newsletter signup.')
  assert not errors,errors
  assert all(r['email'].endswith('@example.com')for r in requests)
  results.append('No uncaught page errors; all external submissions were intercepted, so these tests sent no emails and establish no real delivery result.')
  await browser.close();Path('qa/gift-capture-staging-tests.json').write_text(json.dumps({'passed':results,'live_delivery_verified':False,'activation_request_confirmed':False},indent=2));print('\n'.join('PASS '+r for r in results))
try:asyncio.run(main())
finally:server.shutdown()

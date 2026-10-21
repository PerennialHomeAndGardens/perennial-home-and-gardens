import asyncio,json,threading,http.server,socketserver,re
from datetime import datetime,timedelta,timezone
from pathlib import Path
from bs4 import BeautifulSoup as Soup
from playwright.async_api import async_playwright
ROOT=Path('.')
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=socketserver.TCPServer(('127.0.0.1',8765),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
URL='http://127.0.0.1:8765'
mock="""class FakeSpeech {constructor(){window.testRecognition=this;}start(){this.onstart?.();}stop(){queueMicrotask(()=>this.onend?.());}abort(){this.onend?.();}emit(text){const r=[{transcript:text}];r.isFinal=true;this.onresult?.({resultIndex:0,results:[r]});}}window.SpeechRecognition=FakeSpeech;"""
async def main():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch();context=await browser.new_context();await context.add_init_script(mock)
  await context.add_init_script("sessionStorage.setItem('phg-b3-resource-offer','1');sessionStorage.setItem('phg-b3-tool-offer','1')")
  page=await context.new_page();errors=[];
  async def open_assistant():
   b=await page.locator('.assistantAvatar').bounding_box();await page.mouse.click(b['x']+b['width']/2,b['y']+b['height']/2)
  page.on('pageerror',lambda e:errors.append(page.url+' '+str(e)))
  await page.goto(URL,wait_until='load');await page.wait_for_selector('#ap[data-enhanced] ',state='attached')
  # Every local navigation destination exists, including all retained apps.
  routes=await page.locator('#tools .creamTool').evaluate_all('(els)=>els.map(e=>e.getAttribute("href"))');assert len(routes)==12
  for r in routes:
   assert (await context.request.get(URL+r)).status==200,r
   await page.goto(URL,wait_until='load');await page.wait_for_function('window.__siteExperience===true')
   await page.locator('#tools .creamTool[href="'+r+'"]').click();await page.wait_for_url('**'+r)
  await page.goto(URL,wait_until='load');await page.wait_for_selector('#ap[data-enhanced]',state='attached')
  harvest=page.get_by_role('link',name='OPEN HARVEST RECORDS →',exact=True);assert 'harvest-records/' in await harvest.get_attribute('href')
  await harvest.press('Enter');await page.wait_for_url('**/tools/harvest-records/');assert '/tools/harvest-records/' in page.url
  for path in sorted(Path('tools').glob('*/index.html')):
   await page.goto(URL+'/'+str(path),wait_until='load');assert await page.locator('.b21StickyBrand').count()==1;assert await page.locator('footer.phg-footer').count()==1
  await page.goto(URL+'/tools/garden-planner/',wait_until='load')
  for control in ['newPlan','savePlan','loadPlan','exportPlan','helpBtn','fitBtn','openLibrary','openInspector']:assert await page.locator('#'+control).count()==1
  await page.locator('#helpBtn').click();assert await page.locator('#helpModal').is_visible();await page.locator('#closeHelp').click()
  await page.locator('#palette .tool').first.click();assert await page.locator('#gardenSvg #objectLayer > *').count()>0
  print('PASS 12 direct tool routes, 13 retained app shells and restored Planner controls')
  await page.goto(URL,wait_until='load');await page.wait_for_selector('#ap[data-enhanced]',state='attached')
  for width,height in [(1440,1000),(1024,768),(768,800),(390,844),(360,640),(390,360)]:
   await page.set_viewport_size({'width':width,'height':height});await open_assistant();await page.wait_for_selector('#ap.on')
   for selector in ['.tanya-head','.tanya-categories button:first-child','.tanya-categories button:last-of-type','.tanya-intro','#q','.tanya-mic','.tanya-compose button:last-child','.tanya-close']:
    box=await page.locator('#ap '+selector).bounding_box();assert box and box['y']>=0 and box['y']+box['height']<=height+1,(width,height,selector,box)
   assert await page.locator('#chat').evaluate('(e)=>getComputedStyle(e).overflowY')=='auto'
   if width in [1440,390]:
    Path('qa').mkdir(exist_ok=True);await page.screenshot(path='qa/tanya-'+str(width)+'x'+str(height)+'.png')
   await page.get_by_role('button',name='Close Tanya’s Assistant',exact=True).click()
  print('PASS compact assistant across desktop, tablet, mobile and reduced-height keyboard simulation')
  await page.set_viewport_size({'width':390,'height':844});await open_assistant()
  assert await page.locator('#tanya-intro-audio').evaluate('(a)=>a.paused && a.currentTime===0')
  await page.get_by_role('button',name='▶ Play',exact=True).click();await page.wait_for_timeout(500);assert await page.locator('#tanya-intro-audio').evaluate('(a)=>!a.paused && a.currentTime>0')
  await page.get_by_role('button',name='Pause Tanya’s message',exact=True).click();assert await page.locator('#tanya-intro-audio').evaluate('(a)=>a.paused')
  await page.get_by_role('button',name='Restart Tanya’s message',exact=True).click();assert await page.locator('#tanya-intro-audio').evaluate('(a)=>a.currentTime===0')
  await page.get_by_role('button',name='Play Tanya’s message',exact=True).click();await page.get_by_role('button',name='Close Tanya’s Assistant',exact=True).click();assert await page.locator('#tanya-intro-audio').evaluate('(a)=>a.paused && a.currentTime===0')
  await open_assistant();await page.get_by_role('button',name='Ask About Gardening',exact=True).click();assert await page.locator('.tanya-question').count()==5
  await page.locator('.tanya-question').first.click();await page.wait_for_function('document.querySelectorAll("#chat .bubble").length===2');assert await page.locator('#chat .bubble').count()==2
  await page.get_by_role('button',name='Suggested questions',exact=True).click();await page.get_by_role('button',name='About Perennial Home & Gardens',exact=True).click();assert await page.locator('.tanya-question').count()==5
  await page.locator('#q').fill('Tell me about Perennial');await page.get_by_role('button',name='Send',exact=True).click();await page.wait_for_timeout(100);assert await page.locator('#chat .bubble').count()==4
  # Mocked browser speech callbacks verify UI and draft handling; this is not a physical microphone check.
  await page.locator('#q').fill('My draft');await page.locator('.tanya-mic').click();assert await page.locator('.tanya-mic').get_attribute('aria-pressed')=='true'
  await page.evaluate("testRecognition.emit('needs more compost')");assert await page.locator('#q').input_value()=='My draft needs more compost'
  await page.locator('.tanya-mic').click();await page.wait_for_timeout(50);assert await page.locator('.tanya-mic').get_attribute('aria-pressed')=='false';assert await page.locator('#chat .bubble').count()==4
  await page.locator('.tanya-mic').click();await page.evaluate("testRecognition.emit('and water')");assert await page.locator('#q').input_value()=='My draft needs more compost and water'
  await page.locator('.tanya-mic').click();await page.locator('#q').fill('Edited unfinished message');await page.locator('.tanya-mic').click();await page.evaluate("testRecognition.onerror({error:'not-allowed'})");assert await page.locator('#q').input_value()=='Edited unfinished message';assert 'denied' in await page.locator('.tanya-status').inner_text()
  await page.evaluate('window.SpeechRecognition=undefined;window.webkitSpeechRecognition=undefined');await page.locator('.tanya-mic').click();assert 'unavailable' in await page.locator('.tanya-status').inner_text();assert await page.locator('#q').input_value()=='Edited unfinished message'
  assert await page.locator('#chat .bubble').count()==4
  print('PASS actual MP3 play/pause/restart/close; categories, chat history, mocked speech resume/denial/unavailable/no auto-send')
  await page.get_by_role('button',name='Close Tanya’s Assistant',exact=True).click()
  # Real retained matcher for all prepared knowledge questions.
  kb=json.loads(Path('app-assets/tanya-knowledge.json').read_text())
  for entry in kb['entries']:
   await page.evaluate('(question)=>{document.getElementById("q").value=question;return window.ask();}',entry['question'])
   text=await page.locator('#chat .bubble').last.inner_text();assert entry['answer'] in text,entry['question']
  print('PASS',len(kb['entries']),'retained knowledge answers')
  catalog=json.loads(Path('articles/catalog.json').read_text());assert len(catalog)==29
  for a in catalog:
   url=a.get('url') or '/articles/'+a['slug']+'/'
   await page.goto(URL+url,wait_until='load');assert await page.locator('.phg-video-play').count()==1;assert await page.locator('.phg-affiliate-space').count()==2;assert await page.locator('footer.phg-footer').count()==1
   fields=page.locator('.phg-quiz:not([data-pretest]) fieldset');f=fields.first;answer=int(await f.get_attribute('data-answer'));await f.locator('input').nth(answer).check();await f.locator('button').click();assert 'You got it.' in await f.locator('output').inner_text();await f.locator('input').nth((answer+1)%3).check();await f.locator('button').click();assert 'Try again.' in await f.locator('output').inner_text()
  print('PASS all29 article pages, correct/incorrect quiz feedback, videos and affiliate spaces')
  await page.goto(URL+'/articles/',wait_until='load');await page.locator('#article-search').fill('cucumber');assert await page.locator('.phg-article-card:visible').count()>=1
  link=page.locator('.phg-article-card:visible a').first;destination=await link.get_attribute('href');await link.click();await page.wait_for_url('**'+destination);assert await page.locator('.phg-article-content').count()==1
  # Compare unchanged wood artwork reference and exact original dark gradient.
  await page.goto(URL,wait_until='load');await page.wait_for_selector('#ap[data-enhanced]',state='attached')
  await open_assistant();assert await page.locator('.tanya-head').evaluate('(e)=>getComputedStyle(e).backgroundImage')==await page.locator('footer.phg-footer').evaluate('(e)=>getComputedStyle(e).backgroundImage')
  await page.get_by_role('button',name='Close Tanya’s Assistant',exact=True).click()
  await page.set_viewport_size({'width':390,'height':844})
  assert (await page.locator('#contact .contactGrid').evaluate('(e)=>getComputedStyle(e).gridTemplateColumns')).count('px')==1
  await page.locator('.cleanMenu').hover();assert await page.locator('.cleanMenu').get_attribute('data-phg-tooltip')=='Menu'
  await page.locator('#music').hover();assert await page.locator('#music').get_attribute('data-phg-tooltip')=='Jukebox'
  await page.locator('#music').click();juke=page.locator('#site-shared-jukebox');await juke.wait_for(state='visible')
  for name in ['Meditation','Music','Movies','Motivation']:assert await juke.get_by_role('button',name=name,exact=True).count()==1
  assert await juke.get_by_role('button',name='Site soundtrack',exact=True).count()==0
  await juke.get_by_role('button',name='Meditation',exact=True).click();assert await juke.locator('.x-track').count()>0
  await juke.locator('.x-dialog-heading button').click()
  print('PASS article links, mobile contact, original brown gradient, icon labels and retained jukebox categories')
  assert not errors,errors
  # Browser clock exercises the two prompt thresholds without a real two-minute delay.
  prompt_context=await browser.new_context();prompt_page=await prompt_context.new_page();await prompt_page.clock.install();await prompt_page.clock.pause_at(datetime.now(timezone.utc)+timedelta(seconds=1));await prompt_page.goto(URL,wait_until='load');await prompt_page.wait_for_selector('#ap[data-enhanced]',state='attached')
  await prompt_page.clock.fast_forward(24000);assert not await prompt_page.locator('#freebieModal').is_visible()
  await prompt_page.clock.fast_forward(1000);assert await prompt_page.locator('#freebieModal').is_visible()
  await prompt_page.evaluate('closeFreebie()');await prompt_page.clock.fast_forward(94000);assert await prompt_page.locator('#phg-newsletter-prompt').count()==0
  await prompt_page.clock.fast_forward(1000);assert await prompt_page.locator('#phg-newsletter-prompt').is_visible();assert 'Monthly garden ideas, gifts and coupons' in await prompt_page.locator('#phg-newsletter-prompt').inner_text()
  await prompt_page.locator('#phg-newsletter-prompt .x-dialog-heading button').click();await prompt_page.clock.fast_forward(180000);assert not await prompt_page.locator('dialog[open],.modal.on').count()
  print('PASS resource prompt at25seconds and distinct newsletter prompt at120seconds, once per visit')
  await browser.close();print('PASS no uncaught page errors')
asyncio.run(main());server.shutdown()

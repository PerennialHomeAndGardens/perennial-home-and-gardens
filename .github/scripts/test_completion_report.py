import asyncio,threading,http.server,os
from playwright.async_api import async_playwright
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',8775),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
async def main():
 async with async_playwright()as pw:
  browser=await pw.chromium.launch(channel=os.environ.get('PHG_QA_BROWSER_CHANNEL'));p=await browser.new_page();await p.goto('http://127.0.0.1:8775/qa/leaf-model-validation.html');assert '20 of 46'in await p.locator('main').inner_text();assert await p.locator('.b20Logo img').is_visible();await p.get_by_role('button',name='Open navigation',exact=True).click();assert await p.locator('#navlinks a[href="/tools/garden-library/"]').is_visible();assert await p.locator('#music').is_visible();assert not await p.locator('body').evaluate('(e)=>e.textContent.includes("None")');await p.set_viewport_size({'width':360,'height':780});assert await p.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth+2');await browser.close();print('PASS public model report, retained wood banner, menu and mobile width')
asyncio.run(main());server.shutdown()

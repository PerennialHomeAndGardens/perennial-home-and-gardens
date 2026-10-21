import asyncio,json,threading,http.server,socketserver,subprocess
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright
O=Path('help/media');m=json.loads((O/'frames-manifest.json').read_text());assert len(m['frames'])==14
for row in m['frames']:
 assert Image.open(O/'frames'/row['file']).size==(1920,1080)
 assert row['sourceUrl'].startswith('https://perennialhomeandgardens.com/')
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(O/'getting-started-with-my-garden.mp4')]))
assert abs(float(info['format']['duration'])-m['durationSeconds'])<.3
assert {s['codec_type']for s in info['streams']}=={'video','audio'}
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=socketserver.TCPServer(('127.0.0.1',8772),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
async def main():
 async with async_playwright() as pw:
  b=await pw.chromium.launch();p=await b.new_page()
  await p.add_init_script("sessionStorage.setItem('phg-b3-resource-offer','1');sessionStorage.setItem('phg-b3-tool-offer','1')")
  await p.goto('http://127.0.0.1:8772/help/',wait_until='load');v=p.locator('.phg-guide-video');assert await v.count()==1
  assert await v.evaluate('(v)=>v.paused&&!v.autoplay&&v.currentTime===0');await v.evaluate('(v)=>v.play()');await p.wait_for_function('document.querySelector(".phg-guide-video").currentTime>0');await v.evaluate('(v)=>v.pause()');assert await v.evaluate('(v)=>v.paused')
  for width in [1440,768,390,360]:
   await p.set_viewport_size({'width':width,'height':844});assert await p.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth+1')
  assert await p.locator('track[kind="captions"]').count()==1
  assert (await p.request.get('http://127.0.0.1:8772/help/media/perennial-garden-guide-editing-kit.zip')).status==200
  await b.close()
asyncio.run(main());server.shutdown();print('PASS14 real-site1920x1080frames; original-duration video/audio; no autoplay; actual playback/pause; captions; editing-kit download; four responsive widths')

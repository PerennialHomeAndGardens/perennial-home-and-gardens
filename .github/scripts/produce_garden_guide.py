"""Use actual deployed screenshots and the user's original MP3; no generated audio."""
import asyncio,io,json,subprocess,zipfile,hashlib
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image,ImageDraw,ImageFont
from playwright.async_api import async_playwright
R=Path('.');O=R/'help/media';F=O/'frames';F.mkdir(parents=True,exist_ok=True)
BASE='https://perennialhomeandgardens.com'
scenes=[('Opening introduction','/','section.hero','Getting Started With My Garden'),('Open My Garden','/','#tools .phg-garden-start','Begin with the green Open My Garden button'),('Garden Profile','/tools/my-garden/','#saveProfile','Name your garden and save your profile'),('Where to begin','/tools/my-garden/','.toolgrid a[href="../growing-zone/"]','Start with your growing environment'),('My Growing Zone','/tools/growing-zone/','main','Find your U.S. hardiness zone'),('Map Garden Space','/tools/garden-planner/','#gardenSvg','Map beds, paths and planting space'),('Seasonal Calendar','/tools/seasonal-calendar/','main','Plan seasonal work around local conditions'),('Plant Companions','/tools/plant-companions/','main','Compare growing needs and useful pairings'),('Garden Calculator','/tools/garden-calculator/','main','Check measurements before buying materials'),('Plant, Pest & Disease Identifier','/tools/plant-identifier/','main','Add evidence and review screening clues'),('Garden Journal','/tools/garden-journal/','main','Keep a history of your garden work'),('Harvest & Garden Records','/tools/harvest-records/','main','Track yields, quality and seasonal results'),('Connected tools','/tools/my-garden/','.toolgrid','Return to My Garden to review saved records'),('Keep learning','/help/','.guide-intro','Visit Help & Tutorials whenever you need a hand')]
manifest=[]
async def capture():
 async with async_playwright() as pw:
  b=await pw.chromium.launch();c=await b.new_context(viewport={'width':1920,'height':1080},reduced_motion='reduce')
  await c.add_init_script("sessionStorage.setItem('phg-b3-resource-offer','1');sessionStorage.setItem('phg-b3-tool-offer','1')")
  p=await c.new_page()
  for i,(title,path,selector,label) in enumerate(scenes,1):
   response=await p.goto(BASE+path,wait_until='load');assert response and response.status==200,path
   await p.wait_for_function('window.__siteExperience===true');await p.evaluate('document.fonts.ready')
   target=p.locator(selector).first;await target.wait_for(state='visible')
   if selector not in ['main','#gardenSvg']:await target.scroll_into_view_if_needed()
   box=await target.bounding_box();im=Image.open(io.BytesIO(await p.screenshot())).convert('RGBA');assert im.size==(1920,1080)
   overlay=Image.new('RGBA',im.size);d=ImageDraw.Draw(overlay)
   if box:
    x=max(8,int(box['x'])-10);y=max(105,int(box['y'])-10);right=min(1910,int(box['x']+box['width'])+10);bottom=min(925,int(box['y']+box['height'])+10)
    if right>x and bottom>y:d.rounded_rectangle((x,y,right,bottom),radius=14,outline='#e6ca7c',width=6)
   d.rectangle((0,940,1920,1080),fill=(31,54,34,248));d.text((48,955),'PERENNIAL GARDEN GUIDES  ·  '+str(i).zfill(2),font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',20),fill='#d5dfc6');d.text((48,996),label,font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf',34),fill='#fffdf4')
   name=str(i).zfill(2)+'-frame.png';Image.alpha_composite(im,overlay).convert('RGB').save(F/name,optimize=True)
   manifest.append({'frame':i,'file':name,'title':title,'sourceUrl':p.url,'capturedAt':datetime.now(timezone.utc).isoformat(),'annotation':label,'visual':'Actual live screenshot with instructional overlay'})
  await b.close()
asyncio.run(capture())
audio=O/'my-garden-introduction.mp3';duration=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',str(audio)]))
# Match the supplied narration, checked locally without paid transcription.
# Reuse genuine dashboard/help frames during the opening explanation.
timeline=[(0,5.32,0),(5.32,17.58,2),(17.58,35.72,13),(35.72,45.74,2),(45.74,51.04,1),(51.04,52.98,2),(52.98,54.5,3),(54.5,59.12,4),(59.12,62.92,5),(62.92,66.68,6),(66.68,70.34,7),(70.34,75.26,8),(75.26,82.6,9),(82.6,87.94,10),(87.94,91.22,11),(91.22,103.06,12),(103.06,duration,13)]
segments=[]
for i,(start,end,frame) in enumerate(timeline):
 row=manifest[frame];seconds=end-start;s=O/('segment-'+str(i)+'.mp4');segments.append(s)
 subprocess.run(['ffmpeg','-y','-loglevel','error','-loop','1','-i',str(F/row['file']),'-t',str(seconds),'-vf','scale=1280:720,fade=t=in:st=0:d=0.25,fade=t=out:st='+str(seconds-.25)+':d=0.25','-r','25','-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p',str(s)],check=True)
concat=O/'segments.txt';concat.write_text(''.join("file '"+s.name+"'\n" for s in segments));video=O/'getting-started-with-my-garden.mp4'
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','160k','-shortest','-movflags','+faststart',str(video)],check=True)
for s in segments+[concat]:s.unlink()
(O/'frames-manifest.json').write_text(json.dumps({'audio':'User-supplied MP3, unchanged original retained','audioSha256':hashlib.sha256(audio.read_bytes()).hexdigest(),'durationSeconds':duration,'timingNote':'Frame cuts aligned to the supplied recording; original audio is retained.','timeline':[{'start':a,'end':b,'frame':i+1}for a,b,i in timeline],'frames':manifest},indent=2))
readme='''Perennial Garden Guides | Getting Started With My Garden

14 individual 16:9 frames covering the 13 tutorial scenes use genuine deployed website screenshots and instructional highlights. No fictional interface was generated. The supplied MP3 remains unchanged; no generated narration is included. Frame timing follows the supplied recording and is editable in frames-manifest.json for Canva/CapCut.

YouTube title: Perennial Garden Guides | Getting Started With My Garden
Description: Start with My Garden, your browser-based planning hub from Perennial Home & Gardens. Explore growing zones, layouts, seasonal timing, companion plants, materials calculations, garden-health screening and garden records. Save in each tool; records stay in this browser on this device. Export backups where offered. Written guides: https://perennialhomeandgardens.com/help/

Plan It. Grow It. Live It.

YouTube hosting steps:
1. Open YouTube Studio for the intended Perennial channel.
2. Choose Create > Upload videos and select getting-started-with-my-garden.mp4.
3. Use the title and description above. Choose an actual tutorial frame as the thumbnail.
4. Answer audience/content questions accurately.
5. Under Visibility choose Unlisted, then Save.
6. Copy the video URL and provide it for the website embed. Unlisted videos can be viewed by anyone with the link.

Reusable individual tutorial opening:
Ready to make gardening a little easier? In this Perennial Garden Guide, we'll show you how to use [TOOL NAME] and make the most of what it has to offer. Let's get started!
Demonstrate the real interface step by step, then invite viewers to Help & Tutorials.
'''
# Accessible captions from local transcription; no paid transcription service used.
transcript=json.loads((R/'.github/data/supplied-tutorial-transcript.json').read_text())
def stamp(t):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);sec,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{sec:02}.{ms:03}'
vtt='WEBVTT\n\n'
for row in transcript:
 text=row['text'].replace('perennial','Perennial').replace('my garden','My Garden').replace('my growing zone','My Growing Zone').replace('map garden space','Map Garden Space').replace('seasonal calendar','Seasonal Calendar').replace('plant companions','Plant Companions').replace('garden calculator','Garden Calculator').replace('Planet grow it, live it.','Plan it. Grow it. Live it.')
 vtt+=stamp(row['start'])+' --> '+stamp(row['end'])+'\n'+text+'\n\n'
(O/'my-garden-captions.vtt').write_text(vtt)
(O/'README.txt').write_text(readme)
with zipfile.ZipFile(O/'perennial-garden-guide-editing-kit.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in [audio,O/'frames-manifest.json',O/'README.txt',O/'my-garden-captions.vtt']+list(F.glob('*.png')):z.write(f,f.relative_to(O))
# User-initiated native playback while the requested YouTube upload awaits account access.
from bs4 import BeautifulSoup as Soup
p=R/'help/index.html';d=Soup(p.read_text(),'html.parser');section=d.select_one('.guide-intro')
for old in section.select('.phg-guide-video'):old.decompose()
for old in section.select('a[href*="perennial-garden-guide-editing-kit"]'):
 parent=old.find_parent('p')
 if parent:parent.decompose()
 else:old.decompose()
v=d.new_tag('video',attrs={'class':'phg-guide-video','controls':'','preload':'metadata','playsinline':'','poster':'/help/media/frames/01-frame.png','aria-label':'Getting Started With My Garden tutorial'});v.append(d.new_tag('source',src='/help/media/getting-started-with-my-garden.mp4',type='video/mp4'));v.append(d.new_tag('track',kind='captions',src='/help/media/my-garden-captions.vtt',srclang='en',label='English'));section.append(v)
a=d.new_tag('p');a.append(Soup('<a href="/help/media/perennial-garden-guide-editing-kit.zip">Download the tutorial editing kit</a>','html.parser'));section.append(a);p.write_text(str(d))
config=O/'tutorial-config.json'
if not config.exists():config.write_text(json.dumps({'youtubeVideoId':None,'title':'Perennial Garden Guides | Getting Started With My Garden','autoplay':False},indent=2))
script=R/'app-assets/garden-guide-video.js'
script.write_text("(()=>{const v=document.querySelector('.phg-guide-video');if(!v)return;v.addEventListener('play',()=>document.querySelectorAll('audio,video').forEach(a=>{if(a!==v)a.pause();}));fetch('/help/media/tutorial-config.json').then(r=>r.json()).then(c=>{if(!/^[A-Za-z0-9_-]{11}$/.test(c.youtubeVideoId||''))return;const f=document.createElement('iframe');f.title=c.title;f.src='https://www.youtube-nocookie.com/embed/'+c.youtubeVideoId+'?rel=0';f.allow='accelerometer; encrypted-media; gyroscope; picture-in-picture';f.allowFullscreen=true;f.loading='lazy';v.replaceWith(f);}).catch(()=>{});})();")
d=Soup(p.read_text(),'html.parser')
if not d.select_one('script[src="/app-assets/garden-guide-video.js"]'):d.body.append(d.new_tag('script',src='/app-assets/garden-guide-video.js',defer=''))
p.write_text(str(d))
print('Produced14 real-site frames; user audio duration',duration)

"""Browser workflows in a fresh profile: no visitor data or external submissions."""
import asyncio,base64,json,threading,http.server,socketserver,traceback,os
from pathlib import Path
from io import BytesIO
from datetime import date
from PIL import Image
from playwright.async_api import async_playwright
ROOT=Path('.');BASE=os.environ.get('PHG_QA_BASE','http://127.0.0.1:8772')
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=None
if 'PHG_QA_BASE' not in os.environ:
 server=socketserver.TCPServer(('127.0.0.1',8772),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
report={'date':'2026-10-22','environment':'Chromium browser, isolated test profile','baseUrl':BASE,'tools':[],'limitations':['An experimental local leaf model covers 38 classes; broad species recognition is not provided.','Photo pixels are used for quality/color cues; screening matches use visitor-selected observations.','Uploaded photos are not retained in saved reports or after refresh.','Physical phone camera, HEIC conversion, microphone permissions and native print dialogs need device testing.','Browser-local saves do not provide cross-device accounts or cloud backups.']}
def png(color=(40,130,45),size=(1000,800),format='PNG'):
 b=BytesIO();Image.new('RGB',size,color).save(b,format=format);return b.getvalue()
async def fill(p,values):
 for k,v in values.items():await p.locator('#'+k).fill(str(v))
async def go(p,slug):await p.goto(BASE+'/tools/'+slug+'/',wait_until='load')
async def saved(p,key):return await p.evaluate('(k)=>JSON.parse(localStorage.getItem(k)||"null")',key)
async def download(p,selector):
 async with p.expect_download() as event:await p.locator(selector).click()
 return json.loads(Path(await (await event.value).path()).read_text())
async def identifier(p):
 await go(p,'plant-identifier');assert await p.locator('#photoGrid input[type=file]').count()==4
 uploads=[]
 p.on('request',lambda r:uploads.append(r.url) if r.method=='POST' else None)
 for slot,color in [('whole',(25,130,40)),('close',(180,145,30)),('under',(210,210,205)),('context',(100,70,35))]:
  fmt,mime,ext=('JPEG','image/jpeg','jpg') if slot=='whole' else ('WEBP','image/webp','webp') if slot=='under' else ('PNG','image/png','png')
  payload={'name':slot+'.'+ext,'mimeType':mime,'buffer':png(color,format=fmt)}
  if slot=='whole':
   async with p.expect_file_chooser() as chooser:await p.locator('label[for=photo-whole]').press('Enter')
   await (await chooser.value).set_files(payload)
  else:await p.locator('#photo-'+slot).set_input_files(payload)
  await p.wait_for_function('(s)=>document.querySelector("#photo-status-"+s)?.textContent.includes("ready")',arg=slot)
  assert await p.locator('#img-'+slot).is_visible()
 assert await p.locator('#qualityList .qualityItem').count()==4
 assert not uploads,'Photos unexpectedly posted to a server'
 await p.locator('[data-remove-photo="under"]').click();assert not await p.locator('#img-under').is_visible()
 await p.locator('#photo-under').set_input_files({'name':'tiny.png','mimeType':'image/png','buffer':png(size=(16,16))})
 await p.wait_for_function('document.querySelector("#qualityList").textContent.includes("16×16")')
 assert 'low resolution' in await p.locator('#qualityList').inner_text()
 await p.locator('#photo-under').set_input_files({'name':'bad.txt','mimeType':'text/plain','buffer':b'not an image'})
 assert 'Choose a JPG' in await p.locator('#photo-status-under').inner_text()
 await p.locator('#photo-under').set_input_files({'name':'corrupt.png','mimeType':'image/png','buffer':b'bad PNG bytes'})
 await p.wait_for_function('document.querySelector("#photo-status-under").textContent.includes("could not be opened")')
 await p.locator('#photo-under').set_input_files({'name':'huge.png','mimeType':'image/png','buffer':b'x'*(15*1024*1024+1)})
 assert '15 MB' in await p.locator('#photo-status-under').inner_text()
 await p.locator('#photo-under').set_input_files({'name':'phone.heic','mimeType':'image/heic','buffer':b'heic'})
 assert 'HEIC' in await p.locator('#photo-status-under').inner_text()
 # An invalid replacement keeps the previously valid photo instead of losing it.
 assert await p.locator('#img-under').is_visible()
 await fill(p,{'plantName':'QA Tomato <b>literal</b>','notes':'QA notes <img src=x onerror=alert(1)>'})
 for box,value in [('areas','leaves'),('symptoms','white coating'),('symptoms','spots'),('conditions','humid')]:
  q=p.locator('#'+box+' [data-value="'+value+'"]')
  if await q.count():await q.click()
 await p.locator('#identify').click();assert 'Powdery Mildew' in await p.locator('#cards').inner_text()
 assert await p.locator('#reportBody img,#reportBody b b').count()==0
 assert '<b>literal</b>' in await p.locator('#reportBody').inner_text()
 await p.locator('#saveReport').click();records=await saved(p,'phgGardenHealthReports');assert records[0]['photoCount']==4
 assert not any('data:image/' in str(v) for v in records[0].values())
 await p.locator('[data-mode=pest]').click();await p.locator('#symptoms [data-value=webbing]').click();await p.locator('#identify').click();assert 'Spider Mites' in await p.locator('#cards').inner_text()
 await p.locator('[data-mode=plant]').click();await p.locator('#identify').click();assert 'Trait Confirmation' in await p.locator('#cards').inner_text()
 await p.locator('#tryAI').click();assert 'on this device' in await p.locator('#aiStatus').inner_text()
 await p.evaluate('()=>{window.__printed=0;window.print=()=>{window.__printed++};}');await p.locator('#printReport').press('Enter');await p.wait_for_function('window.__printed===1');assert await p.locator('#report').is_visible()
 await p.reload();assert await p.locator('.photoSlot.has').count()==0;assert len(await saved(p,'phgGardenHealthReports'))==1
 await p.locator('#clear').click();await p.wait_for_load_state();assert await p.locator('.photoSlot.has').count()==0
 return ['Four photo slots upload/preview/quality checks','Remove, replace and invalid/corrupt/oversized/HEIC handling','Disease/pest/plant screening and safe report text','Save report without photo bytes, refresh persistence, print action, clear','No image POSTs; local model scope is truthful']
async def zone(p):
 await go(p,'growing-zone');await fill(p,{'zip':'123'});await p.locator('#find').click();assert 'valid 5-digit' in await p.locator('#message').inner_text()
 await fill(p,{'zip':'20603'});await p.locator('#find').click();await p.wait_for_selector('#result.show')
 expected=json.loads((ROOT/'tools/growing-zone/phzm_zip_2023.json').read_text())['20603'];assert (await p.locator('#zoneText').inner_text()).lower()==expected.lower()
 await p.locator('details.manual summary').click();await p.locator('#manualZone').select_option('7b');await p.locator('#manualBtn').click();await p.reload();assert (await saved(p,'phg-growing-zone'))['zone']=='7b'
 return ['Invalid ZIP feedback','20603 lookup against bundled USDA dataset','Manual zone selection survives refresh']
async def calculator(p):
 await go(p,'garden-calculator');await fill(p,{'soilL':8,'soilW':4,'soilD':12});await p.locator('#soilDU').select_option('12');await p.get_by_role('button',name='Calculate Soil',exact=True).click();assert '32.0 cubic feet' in await p.locator('#soilR').inner_text()
 await fill(p,{'soilL':-8});await p.get_by_role('button',name='Calculate Soil',exact=True).click();assert 'Check your measurements' in await p.locator('#soilR').inner_text()
 for tab,values,button,out,expected in [('mulch',{'mulchL':10,'mulchW':10,'mulchD':3},'Calculate Mulch','mulchR','25.0 cubic feet'),('compost',{'compL':10,'compW':10,'compD':1},'Calculate Compost','compR','8.3 cubic feet'),('plants',{'plantL':8,'plantW':4,'plantS':12},'Calculate Plants','plantR','32 plants'),('seeds',{'seedL':10,'seedRows':2,'seedS':6},'Calculate Seeds','seedR','40 positions')]:
  await p.locator('[data-tab="'+tab+'"]').click();await fill(p,values);await p.get_by_role('button',name=button,exact=True).click();assert expected in await p.locator('#'+out).inner_text()
 return ['All five calculator tabs and known-volume/count examples','Negative dimensions rejected']
async def planner(p):
 await go(p,'garden-planner');await p.locator('#palette .tool').first.click();await p.locator('#palette .tool').nth(1).click();assert await p.locator('#objectLayer .obj').count()==2
 await fill(p,{'gardenW':50,'gardenH':35});await p.locator('#applySize').click();assert await p.locator('#boundary').get_attribute('width')=='50'
 await p.locator('#zoomIn').click();assert await p.locator('#zoomLabel').inner_text()!='100%';await p.locator('#centerView').click();assert await p.locator('#zoomLabel').inner_text()=='100%'
 p.once('dialog',lambda d:d.accept('QA layout <b>literal</b>'));await p.locator('#savePlan').click();assert len(await saved(p,'phgGardenPlans'))==1
 await p.reload();await p.locator('#savedList button').first.click();assert await p.locator('#objectLayer .obj').count()==2
 await p.locator('#palette .tool').first.click();ids=await p.locator('#objectLayer .obj').evaluate_all('(es)=>es.map(e=>e.dataset.id)');assert len(set(ids))==3,ids
 assert await p.locator('#savedList b b').count()==0
 data=await download(p,'#exportPlan');assert len(data['garden']['objects'])==3
 await p.locator('#deleteObj').click();assert await p.locator('#objectLayer .obj').count()==2
 await p.locator('#togShade').click();assert 'on' not in (await p.locator('#togShade').get_attribute('class'))
 await p.locator('#helpBtn').click();assert await p.locator('#helpModal').is_visible();await p.locator('#closeHelp').click()
 await p.locator('#plantSearch').fill('Achillea');await p.wait_for_function('document.querySelector("#plantSearchCount").textContent.includes("matching Library plants")');assert await p.locator('#palette .tool').count()>0
 return ['Add objects, resize, zoom and center','Save/reopen and add another object without duplicate IDs','Plan export, library search and help dialog']
async def companions(p):
 await go(p,'plant-companions');await fill(p,{'search':'Tomato'});await p.locator('#searchBtn').click();assert 'Basil' in await p.locator('#content').inner_text();await p.locator('#saveBtn').click();await p.reload();assert 'Tomato' in await saved(p,'phg-companion-saved')
 await fill(p,{'search':'xyzqaunknown'});await p.locator('#searchBtn').click();assert 'No match yet' in await p.locator('#content').inner_text()
 return ['Companion search and related guidance','Saved favorites survive refresh','Unknown plant feedback']
async def calendar(p):
 await go(p,'seasonal-calendar');await p.locator('#zone').select_option('7b');await p.locator('#month').select_option('9');await p.locator('#focus').select_option('veg');await p.locator('#update').click();assert 'October' in await p.locator('#title').inner_text()
 await p.locator('#tasks input[type=checkbox]').first.check();await p.reload();assert await p.locator('#tasks input[type=checkbox]').first.is_checked();await p.locator('#reset').click();assert not await p.locator('#tasks input:checked').count()
 return ['Zone/month/focus updates','Task completion persists','Reset checked tasks']
async def harvest_checker(p):
 await go(p,'harvest-checker');await p.locator('#crop').select_option('Tomato');await p.locator('#stage').select_option('ready');await p.locator('#checkBtn').click();assert 'Looks Harvest-Ready' in await p.locator('#content').inner_text();await p.locator('#saveBtn').click();await p.reload();assert 'Tomato' in await saved(p,'phg-harvest-saved')
 await p.locator('#stage').select_option('wait');assert 'Give It More Time' in await p.locator('#content').inner_text()
 return ['Crop and selected readiness guidance','Save and reload favorites','Stage changes update guidance']
async def seeds(p):
 await go(p,'seed-starting');await fill(p,{'seedCrop':'QA Lettuce','seedVariety':'Test variety','seedDTM':45,'seedQty':'1 packet'});await p.locator('#addSeed').click();assert len((await saved(p,'phgSeedSystemV1'))['seeds'])==1
 await p.locator('[data-tab=trays]').click();await p.locator('#traySeed').select_option(index=1);await p.locator('#trayCells').select_option('6');await fill(p,{'trayName':'QA tray','traySow':'2026-10-22'});await p.locator('#addTray').click();assert await p.locator('[data-cell]').count()==6;await p.locator('[data-cell]').first.click();assert (await saved(p,'phgSeedSystemV1'))['trays'][0]['cellStates'][0]=='germ'
 await p.locator('[data-stage]').first.click();await p.locator('[data-tab=succession]').click();await p.locator('#succSeed').select_option(index=1);await fill(p,{'succStart':'2026-10-22','succRounds':3});await p.locator('#addSucc').click();assert len((await saved(p,'phgSeedSystemV1'))['successions'][0]['rounds'])==3
 await p.reload();assert len((await saved(p,'phgSeedSystemV1'))['trays'])==1
 return ['Add seed inventory','Create tray and cycle cells/advance stage','Build three dated succession rounds','Save persistence']
async def journal(p):
 await go(p,'garden-journal');before=len((await saved(p,'phgGardenJournalV1'))['entries']);assert before>=1,'Identifier report did not import'
 await fill(p,{'entryTarget':'QA Basil','entryNotes':'Watering test note','followDate':'2026-10-22'});await p.locator('#saveEntry').click();assert len((await saved(p,'phgGardenJournalV1'))['entries'])==before+1
 await p.reload();assert len((await saved(p,'phgGardenJournalV1'))['entries'])==before+1
 await fill(p,{'search':'QA Basil'});assert await p.locator('.entry').count()==1
 data=await download(p,'#exportJournal');assert len(data['entries'])==before+1
 p.once('dialog',lambda d:d.accept());await p.locator('[data-del]').first.click();assert len((await saved(p,'phgGardenJournalV1'))['entries'])==before
 return ['Identifier reports import once','Add journal entry/follow-up and reload','Search, JSON export and delete test entry']
async def harvest_records(p):
 await go(p,'harvest-records');await fill(p,{'hCrop':'QA Tomato','hWeight':1,'hCount':3});await p.locator('#hWeightUnit').select_option('kg');await p.locator('#addHarvest').click();assert len((await saved(p,'phgHarvestRecordsV1'))['records'])==1
 assert '2.20 lb' in await p.locator('.record').inner_text();await p.reload();assert len((await saved(p,'phgHarvestRecordsV1'))['records'])==1
 data=await download(p,'#exportRecords');assert data['records'][0]['weightUnit']=='kg'
 await fill(p,{'hCrop':'Invalid negative QA','hWeight':-1});await p.locator('#addHarvest').click();assert len((await saved(p,'phgHarvestRecordsV1'))['records'])==1
 return ['Save harvest with kg-to-lb conversion','Reload and JSON export','Negative harvest weight blocked']
async def inventory(p):
 await go(p,'garden-inventory');assert any(i.get('sourceSeedId') for i in (await saved(p,'phgGardenInventoryV1'))['inventory'])
 await fill(p,{'iName':'QA Compost','iQty':1,'iMin':2});await p.locator('#addItem').click();await fill(p,{'iSearch':'QA Compost'});assert 'Low' in await p.locator('#inventoryRows').inner_text();await p.locator('#inventoryRows [data-shop]').first.click()
 await p.locator('[data-tab=shopping]').click();p.once('dialog',lambda d:d.accept('25'));await p.locator('[data-buy]').first.click();assert (await saved(p,'phgGardenInventoryV1'))['purchases'][0]['cost']==25
 await p.locator('[data-tab=budget]').click();await fill(p,{'bSeason':'QA season','bTotal':100,'bSoil':50});await p.locator('#saveBudget').click();assert '$75.00' in await p.locator('#budgetBoxes').inner_text()
 await p.locator('[data-tab=purchases]').click();data=await download(p,'#exportData');assert data['budget']['total']==100
 await p.reload();assert (await saved(p,'phgGardenInventoryV1'))['budget']['total']==100
 return ['Seed inventory imports automatically','Low stock, shopping list and mark purchased','Budget spending/remaining calculation','JSON export and reload']
async def library(p):
 await go(p,'garden-library');await p.locator('.phg-library-launches a[href="#phgDictionary"]').press('Enter');await p.locator('#search').fill('rhizome');await p.locator('#searchBtn').click();await p.wait_for_function('document.querySelector("#results").textContent.toLowerCase().includes("rhizome")');await p.locator('#results .term').first.click();await p.locator('#phgSaveTerm').click()
 assert len((await saved(p,'phgGardenLibraryShelfV1'))['terms'])>=1
 await p.locator('.phg-library-launches a[data-library-mode=plants]').press('Enter');await p.locator('#phgPlantSearch').fill('Achillea');await p.locator('#phgPlantSearchBtn').click();await p.wait_for_function('document.querySelector("#phgPlantResults").textContent.toLowerCase().includes("achillea")');await p.locator('#phgPlantResults .phg-plant-card').first.click();await p.locator('#phgSavePlant').click()
 await p.locator('#phgBookSearch').fill('From Seed to Skillet');await p.wait_for_function('document.querySelectorAll(".phg-book-card").length===1');assert 'Jimmy Williams' in await p.locator('.phg-book-card').inner_text()
 await p.locator('.phg-book-save').click();assert await p.locator('.phg-book-save').get_attribute('aria-pressed')=='true'
 await p.locator('.phg-book-detail-link').click();await p.locator('#phgBookNotes').fill('QA seed-saving idea');await p.locator('#phgSaveBookNotes').click();await p.reload();assert await p.locator('#phgBookNotes').input_value()=='QA seed-saving idea'
 return ['Dictionary search/open/save term','Plant record search/open/save','Book search and private reading list']
async def dashboard(p):
 await go(p,'my-garden');await fill(p,{'gardenName':'QA Garden','profileZone':'7b','profileLocation':'QA test location'});await p.locator('#saveProfile').click();await p.reload();assert await p.locator('#gardenName').input_value()=='QA Garden'
 for id in ['statPlans','statHealth','statPlants']:assert int(await p.locator('#'+id).inner_text())>=1,id
 assert 'QA Tomato' in await p.locator('#healthReports').inner_text()
 for id in ['seedMeta','journalMeta','harvestRecordsMeta','inventoryMeta']:assert '0 '!= (await p.locator('#'+id).inner_text())[:2],id
 assert await p.locator('.toolgrid a.tool').count()==12
 return ['Profile save/reload','Saved plans, plants and health reports visible','Seed, journal, harvest and inventory summaries connected','12 tool links retained']
async def main():
 async with async_playwright() as pw:
  browser=await pw.chromium.launch(channel=os.environ.get('PHG_QA_BROWSER_CHANNEL'));ctx=await browser.new_context(accept_downloads=True);await ctx.add_init_script("sessionStorage.setItem('phg-b3-resource-offer','1');sessionStorage.setItem('phg-b3-tool-offer','1');")
  p=await ctx.new_page();errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.set_default_timeout(12000)
  for slug,fn in [('plant-identifier',identifier),('growing-zone',zone),('garden-calculator',calculator),('garden-planner',planner),('plant-companions',companions),('seasonal-calendar',calendar),('harvest-checker',harvest_checker),('seed-starting',seeds),('garden-journal',journal),('harvest-records',harvest_records),('garden-inventory',inventory),('garden-library',library),('my-garden',dashboard)]:
   item={'tool':slug};start_errors=len(errors)
   try:
    item['checks']=await fn(p);assert len(errors)==start_errors,errors[start_errors:];item['status']='pass';print('PASS',slug,':','; '.join(item['checks']),flush=True)
   except Exception as e:item.update(status='fail',error=str(e),trace=traceback.format_exc());print('FAIL',slug,item['trace'],flush=True)
   report['tools'].append(item)
  # Responsive smoke checks use the actual pages, not only the homepage advertisements.
  for width in [1440,768,390,360]:
   await p.set_viewport_size({'width':width,'height':844})
   for item in report['tools']:
    await go(p,item['tool'])
    if not await p.locator('body').evaluate('(e)=>e.scrollWidth<=innerWidth+2'):
     item.setdefault('layoutFailures',[]).append(width);item['status']='fail'
  report['uncaughtErrors']=errors;report['status']='pass' if all(x['status']=='pass' for x in report['tools']) and not errors else 'fail'
  Path('qa').mkdir(exist_ok=True);Path('qa/tools-functional-20261022.json').write_text(json.dumps(report,indent=2));print('QA_REPORT',json.dumps(report),flush=True)
  await browser.close()
asyncio.run(main())
if server:server.shutdown()
if report['status']!='pass':raise SystemExit(1)

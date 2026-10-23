"""Browser checks of local inference, all-garden backup round trips and print output."""
import asyncio,json,threading,http.server,socketserver,os,traceback
from pathlib import Path
from playwright.async_api import async_playwright
R=Path('.');BASE='http://127.0.0.1:8773'
class Handler(http.server.SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
socketserver.TCPServer.allow_reuse_address=True
server=socketserver.TCPServer(('127.0.0.1',8773),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
report={'status':'running','date':'2026-10-22','checks':[],'limits':['No physical iPhone/Android hardware available.','Native OS print dialogs and physical printers are not exercised.','Field-photo sample results do not establish diagnostic accuracy for all garden photos.']}
async def getfile(p,selector):
 async with p.expect_download()as d:await p.locator(selector).click()
 return Path(await(await d.value).path()).read_text()
async def main():
 async with async_playwright()as pw:
  browser=await pw.chromium.launch(channel=os.environ.get('PHG_QA_BROWSER_CHANNEL'))
  ctx=await browser.new_context(accept_downloads=True);p=await ctx.new_page();p.set_default_timeout(20000);errs=[];p.on('pageerror',lambda e:errs.append(str(e)))
  try:
   await p.goto(BASE+'/tools/plant-identifier/');requests=[];p.on('request',lambda r:requests.append((r.method,r.url)))
   assert not any('tf.min.js'in u or '.bin'in u for _,u in requests)
   await p.locator('#phgVisionRun').click();assert 'Choose the crop' in await p.locator('#phgVisionStatus').inner_text()
   await p.locator('#phgVisionCrop').select_option('Tomato');await p.locator('#phgVisionRun').click();assert 'Upload a leaf photo' in await p.locator('#phgVisionStatus').inner_text()
   casefile=json.loads((R/'.qa-leaf-cases/cases.json').read_text());labels=json.loads((R/'app-assets/plant-vision/class_indices.json').read_text())
   sample=next(c for c in casefile['cases']if c['expectedIndex']==29)
   await p.locator('#photo-close').set_input_files(str(R/sample['fixtureUrl'].lstrip('/')))
   await p.wait_for_function('document.querySelector("#photo-status-close").textContent.includes("ready")')
   await p.locator('#phgVisionRun').click();await p.wait_for_function('document.querySelector("#phgVisionStatus").textContent.includes("finished")',timeout=120000)
   assert await p.locator('#phgVisionResult p').count()>=2
   assert not any(method=='POST'for method,_ in requests)
   await p.locator('#saveReport').click();saved=await p.evaluate('JSON.parse(localStorage.getItem("phgGardenHealthReports"))[0]');assert saved['photoModelResult']['crop']=='Tomato';assert len(saved['photoModelResult']['matches'])==3
   await p.locator('#phgVisionCrop').select_option('Potato');assert await p.evaluate('PHGLeafVision.savedResult()')is None
   assert await p.locator('#phgCameraInput').get_attribute('capture')=='environment'
   async with p.expect_file_chooser()as chooser:await p.get_by_role('button',name='Take photo · Leaf Underside',exact=True).click()
   await(await chooser.value).set_files(str(R/sample['fixtureUrl'].lstrip('/')));await p.wait_for_function('document.querySelector("#photo-status-under").textContent.includes("ready")')
   report['checks'].append('Actual model download/inference UI, saved model results, crop-change invalidation, no photo POST and camera file-chooser path passed')
   # Deterministic labeled real-image sample; evaluate every selected case, including failures.
   results=[]
   for case in casefile['cases']:
    crop=labels[str(case['expectedIndex'])].split('___')[0]
    matches=await p.evaluate('''async ({url,crop})=>{const image=new Image();image.src=url;await image.decode();return PHGLeafVision.infer(image,crop);}''',{'url':case['fixtureUrl'],'crop':crop})
    top=matches[0];accepted=top['score']>=.70 and(len(matches)==1 or top['score']-matches[1]['score']>=.15)
    results.append({**{k:v for k,v in case.items()if k!='fixtureUrl'},'expectedLabel':labels[str(case['expectedIndex'])],'predictions':matches[:3],'correctTop1':top['index']==case['expectedIndex'],'correctTop3':case['expectedIndex']in[m['index']for m in matches[:3]],'meetsDisplayThreshold':accepted})
    print('LEAF_CASE',case['group'],top['label'],top['score'],'correct',results[-1]['correctTop1'],flush=True)
   n=len(results);accepted=[r for r in results if r['meetsDisplayThreshold']];metrics={'cases':n,'correctTop1':sum(r['correctTop1']for r in results),'correctTop3':sum(r['correctTop3']for r in results),'thresholdAccepted':len(accepted),'thresholdAcceptedCorrect':sum(r['correctTop1']for r in accepted)}
   validation={'modelRevision':'b7e8c6f5a1b3e1b7847f3e78f41a65a8a9110235','dataset':casefile['dataset'],'datasetRevision':casefile['revision'],'method':casefile['method'],'metrics':metrics,'cases':results,'limitations':report['limits']+['Known crop was supplied; this is not a species-identification test.','PlantDoc labels were not independently re-adjudicated by a plant pathologist.','Samples may contain mixed symptoms or domain differences from controlled training images.']}
   Path('qa/leaf-model-validation.json').write_text(json.dumps(validation,indent=2));report['leafMetrics']=metrics
   # Check all categories and expanded datasets are present in the actual running pages.
   await p.goto(BASE+'/tools/plant-companions/');assert await p.evaluate('Object.keys(DATA).length')==50
   await p.locator('#search').fill('Lavender');await p.locator('#searchBtn').click();assert 'Rosemary'in await p.locator('#content').inner_text()
   await p.goto(BASE+'/tools/harvest-checker/');assert await p.locator('#crop option').count()==51;await p.locator('#crop').select_option('Asparagus');assert 'crowns'in await p.locator('#content').inner_text()
   report['checks'].append('50 companion and 51 harvest entries render; new Lavender/Asparagus guides work')
   # Import a complete garden backup into a separate fresh context, using the visible file picker.
   await p.goto(BASE+'/tools/my-garden/');await p.locator('#gardenName').fill('Backup round-trip garden');await p.locator('#profileZone').fill('7b');await p.locator('#saveProfile').click()
   seed={'seeds':[{'id':'seed-qa','crop':'Lettuce','variety':'Test','year':'2026','qty':'1 packet','dtm':45,'spacing':6,'method':'Direct sow','source':'QA','notes':'Saved seed','created':'2026-10-22'}],'trays':[{'id':'tray-qa','seedId':'seed-qa','name':'Tray A','cells':6,'sow':'2026-10-22','transplant':'2026-11-10','germDays':7,'cellStates':['germ','planted','failed','empty','planted','planted'],'stage':'Sown','location':'Shelf'}],'successions':[{'id':'succ-qa','seedId':'seed-qa','count':1,'method':'Direct sow','rounds':[{'n':1,'sow':'2026-10-22','harvest':'2026-12-06','status':'Planned'}]}]}
   entries={'phgSeedSystemV1':seed,'phgGardenInventoryV1':{'inventory':[],'shopping':[],'purchases':[],'budget':{'total':100}},'phgGardenJournalV1':{'entries':[{'id':'entry-qa','date':'2026-10-22','type':'observation','target':'Lettuce','notes':'Keep this note','tags':[]}]},'phgHarvestRecordsV1':{'records':[]},'phgGardenBooksV1':{'from-seed-to-skillet-12':{'saved':True,'notes':'Seed memories','status':'want'}},'phgGardenLibraryShelfV1':{'plants':[],'terms':[],'resources':[]},'phg-cal-7b-per-9':['task-qa'],'phgGardenLibraryPlantNotesV1':{'plant-qa':'A saved plant note'}}
   await p.evaluate('(entries)=>{for(const[k,v]of Object.entries(entries))localStorage.setItem(k,JSON.stringify(v));}',entries)
   await p.locator('#phgBackupOpen').click();text=await getfile(p,'#phgBackupExport');backup=json.loads(text);assert 'phg-cal-7b-per-9'in backup['entries'];assert backup['entries']['phgSeedSystemV1']==seed
   fresh=await browser.new_context(accept_downloads=True);q=await fresh.new_page();await q.goto(BASE+'/tools/my-garden/');await q.locator('#phgBackupOpen').click()
   await q.locator('#phgBackupFile').set_input_files({'name':'garden.json','mimeType':'application/json','buffer':text.encode()})
   await q.wait_for_function('document.querySelector("#phgBackupStatus").textContent.includes("File checked")');assert await q.locator('#phgBackupApply').is_disabled();await q.locator('#phgBackupConfirm').check()
   async with q.expect_download():await q.locator('#phgBackupApply').click()
   assert 'sections restored'in await q.locator('#phgBackupStatus').inner_text();actual=await q.evaluate('PHGGardenBackup.snapshot().entries');assert actual==backup['entries']
   await q.locator('#phgBackupReload').click();assert await q.locator('#gardenName').input_value()=='Backup round-trip garden'
   await q.goto(BASE+'/tools/seed-starting/');assert await q.locator('[data-cell]').count()==6
   await q.goto(BASE+'/tools/garden-journal/');assert 'Keep this note'in await q.locator('#timeline').inner_text()
   await q.goto(BASE+'/books/from-seed-to-skillet-12.html');assert await q.locator('#phgBookNotes').input_value()=='Seed memories'
   await q.goto(BASE+'/tools/my-garden/');await q.locator('#phgBackupOpen').click()
   # Invalid files, unsupported version, unsafe property and wrong record types cannot change data.
   for bad in ['not JSON',json.dumps({'format':'perennial-garden-backup','version':2,'entries':entries}),'{"format":"perennial-garden-backup","version":1,"entries":{"__proto__":{}}}',json.dumps({'format':'perennial-garden-backup','version':1,'entries':{'phgSeedSystemV1':{'seeds':[],'trays':[{'cells':6,'cellStates':[]}],'successions':[]}}})]:
    before=await q.evaluate('PHGGardenBackup.snapshot().entries');await q.locator('#phgBackupFile').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':bad.encode()});await q.wait_for_timeout(60);assert await q.locator('#phgBackupApply').is_disabled();assert before==await q.evaluate('PHGGardenBackup.snapshot().entries')
   # Existing sections are kept by the default restore mode; deliberate replacement is previewed and confirmed.
   replacement={'format':'perennial-garden-backup','version':1,'entries':{'phgMyGardenProfileV1':{'gardenName':'Replacement garden','zone':'8a','location':''}}}
   await q.locator('#phgBackupFile').set_input_files({'name':'replace.json','mimeType':'application/json','buffer':json.dumps(replacement).encode()});await q.wait_for_function('document.querySelector("#phgBackupStatus").textContent.includes("File checked")');await q.locator('#phgBackupConfirm').check()
   async with q.expect_download():await q.locator('#phgBackupApply').click()
   assert 'All these sections already exist'in await q.locator('#phgBackupStatus').inner_text()
   await q.locator('#phgBackupMode').select_option('replace')
   async with q.expect_download():await q.locator('#phgBackupApply').click()
   assert await q.evaluate('JSON.parse(localStorage.getItem("phgMyGardenProfileV1")).gardenName')=='Replacement garden'
   report['checks'].append('Full backup export, preview/confirmation, new-browser restore, seed trays/journal/book notes, existing-data protection, replace mode and invalid-file rejection passed')
   # Actual print media + PDF output in Chrome; not an operating-system print dialog.
   await p.goto(BASE+'/tools/plant-identifier/');await p.locator('#plantName').fill('QA print tomato');await p.locator('#identify').click();await p.locator('#saveReport').click();await p.emulate_media(media='print')
   assert not await p.locator('header').is_visible();assert await p.locator('#report').is_visible();pdf=await p.pdf(format='Letter');assert pdf.startswith(b'%PDF')and len(pdf)>3000
   Path('qa/identifier-print-check.pdf').write_bytes(pdf);await p.emulate_media(media='screen');report['checks'].append('Chrome print-media report visibility and actual Letter PDF generation passed; physical printing remains untested')
   for w in [1440,768,390,360]:
    await q.set_viewport_size({'width':w,'height':780});await q.goto(BASE+'/tools/my-garden/');await q.locator('#phgBackupOpen').click();assert await q.locator('#phgBackupDialog').evaluate('(e)=>e.getBoundingClientRect().width<=innerWidth&&e.getBoundingClientRect().height<=innerHeight');await q.get_by_role('button',name='Close',exact=True).click()
   assert not errs,errs;report['checks'].append('Backup dialog fits four viewport widths; no uncaught browser errors');report['status']='pass'
  except Exception as e:report.update(status='fail',error=str(e),trace=traceback.format_exc());print(report['trace'],flush=True)
  finally:
   Path('qa/tools-completion-20261022.json').write_text(json.dumps(report,indent=2));print('COMPLETION_QA',json.dumps(report),flush=True);await browser.close()
asyncio.run(main());server.shutdown()
if report['status']!='pass':raise SystemExit(1)

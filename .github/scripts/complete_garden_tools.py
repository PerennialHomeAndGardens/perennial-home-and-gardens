"""Retain the existing tools and add shared backups, larger curated sets and local vision."""
from pathlib import Path
import json,re
from bs4 import BeautifulSoup as Soup
R=Path(__file__).resolve().parents[2]
for slug,filename,marker in [('plant-companions','companions-additions.json','const names='),('harvest-checker','harvest-additions.json','const names=')]:
 p=R/'tools'/slug/'index.html';s=p.read_text();s=re.sub(r'/\* PHG expanded collection \*/.*?/\* End expanded collection \*/\s*','',s,flags=re.S)
 data=json.loads((R/'data/garden-tools'/filename).read_text());s=s.replace(marker,'/* PHG expanded collection */\nObject.assign(DATA,'+json.dumps(data,ensure_ascii=False)+');\n/* End expanded collection */\n'+marker)
 d=Soup(s,'html.parser');old=d.select_one('#phgCollectionInfo')
 if old:old.decompose()
 info=d.new_tag('details',id='phgCollectionInfo');su=d.new_tag('summary');su.string='Collection coverage & references';info.append(su)
 pa=d.new_tag('p');pa.string=('50 companion planning entries. Match light, moisture, spacing and crop timing; a companion is not a guaranteed pest repellent.' if slug=='plant-companions' else '51 harvest guides. Use cultivar-specific maturity signs and local conditions; calendar days alone do not establish readiness.');info.append(pa)
 a=d.new_tag('a',href='/data/garden-tools/sources.json');a.string='Extension references and editorial method';info.append(a);d.main.append(info);p.write_text(str(d))
p=R/'tools/plant-identifier/index.html';s=p.read_text();s=re.sub(r'/\* PHG expanded diagnostics \*/.*?/\* End expanded diagnostics \*/\s*','',s,flags=re.S)
a=json.loads((R/'data/garden-tools/diagnostic-additions.json').read_text())
s=s.replace('const AREAS=','/* PHG expanded diagnostics */\nDATA.push(...'+json.dumps(a,ensure_ascii=False)+');\n/* End expanded diagnostics */\nconst AREAS=')
s=s.replace('let mode="disease",','SYM.push(...[...new Set(DATA.flatMap(x=>x.sym))].filter(x=>!SYM.includes(x)));\nCONDITIONS.push(...[...new Set(DATA.flatMap(x=>x.cond))].filter(x=>!CONDITIONS.includes(x)));\nlet mode="disease",') if 'SYM.push(' not in s else s
if 'Leaf photo comparison (experimental)' not in s:
 s=s.replace('$("reportBody").innerHTML=vals.map', 'const pv=window.PHGLeafVision?.savedResult();if(pv)vals.push(["Leaf photo comparison (experimental)",pv.matches.map(m=>m.label.replaceAll("_"," ")+" · "+Math.round(m.score*100)+"% model score").join("; ")]);$("reportBody").innerHTML=vals.map')
s=s.replace('screeningVersion:"build6"','screeningVersion:"build7-local-vision",photoModelResult:window.PHGLeafVision?.savedResult()||null')
s=s.replace('Guided screening · no automatic photo diagnosis','Guided screening + experimental leaf photo comparison')
s=s.replace('$("tryAI").textContent="Photo Analysis Status";','$("tryAI").textContent="About photo comparison";')
s=s.replace('Automatic photo identification is not connected. Your uploads support quality checks and guided symptom screening.','Leaf comparison runs on this device for supported crops. It is experimental, is not general species identification, and can be wrong. No account or photo upload to a server is needed.')
# Keep all analysis, observation chips, report controls and existing shared chrome.
d=Soup(s,'html.parser');panel=d.select_one('.aiBox');panel.name='details';panel['id']='phgVisionPanel';panel.clear();panel.append(Soup('''<summary>Experimental leaf photo comparison · limited accuracy</summary><h4>Compare a leaf photo</h4><p><strong>Field-photo check: the first suggestion matched 20 of 46 labeled images. Even high model scores can be wrong. This feature is for exploratory comparison, not diagnosis.</strong></p><p>Experimental comparison for 9 supported crops. Choose a crop you already know and a clear single leaf. The model loads only when clicked; photos stay on this device. Use guided screening for other plants.</p><label for="phgVisionCrop">Known crop</label><select id="phgVisionCrop"><option value="">Choose a supported crop</option><option value="Apple">Apple</option><option value="Cherry_(including_sour)">Cherry</option><option value="Corn_(maize)">Corn</option><option value="Grape">Grape</option><option value="Peach">Peach</option><option value="Pepper_bell">Bell pepper</option><option value="Potato">Potato</option><option value="Strawberry">Strawberry</option><option value="Tomato">Tomato</option></select><label for="phgVisionView">Photo to compare</label><select id="phgVisionView"><option value="close">Close-up</option><option value="under">Leaf underside</option><option value="whole">Whole plant</option><option value="context">Stem / fruit / context</option></select><p>For comparison, the selected image should show one leaf filling most of the frame. Whole-plant, fruit, insect and unrelated photos can give misleading results.</p><div class="actions"><button class="btn" id="phgVisionRun" type="button">Compare leaf photo (experimental)</button><button class="btn secondary" id="tryAI" type="button">About photo comparison</button></div><p id="phgVisionStatus" role="status">Select a crop and upload a leaf photo to start.</p><div id="phgVisionResult" aria-live="polite"></div><div class="statusLine"><span class="dot" id="aiDot"></span><span id="aiStatus">On-device model · experimental</span></div><p><a href="/qa/leaf-model-validation.html">Model scope &amp; field-photo test results</a></p>''','html.parser'))
old=d.select_one('#phgVisionBridge')
if old:old.decompose()
b=d.new_tag('script',id='phgVisionBridge');b.string='window.PHGIdentifier=Object.freeze({photos:()=>photos,readPhoto});';d.body.append(b)
old=d.select_one('#phgVisionStyle')
if old:old.decompose()
st=d.new_tag('style',id='phgVisionStyle');st.string='''#phgVisionCrop,#phgVisionView{display:block;max-width:100%;width:100%;margin:6px 0 12px;padding:10px;border:1px solid #9ba68b;border-radius:8px;background:#fffaf2;color:#2c251c;font:inherit}.phg-camera-button{display:block;margin-top:8px;padding:9px 12px;min-height:44px;border:1px solid #9ba68b;border-radius:8px;background:#f5f0e6;color:#294f30;font:700 13px Georgia,serif;cursor:pointer}#phgVisionResult p{overflow-wrap:anywhere}#symptoms,#conditions{max-height:220px;overflow:auto;padding:3px}#phgVisionStatus{overflow-wrap:anywhere}@media print{.phg-backup-launch,.phg-my-garden-link,.phgToolBack,.phg-camera-button{display:none!important}}''';d.head.append(st)
for n in d.select('script[src*="leaf-vision.js"]'):n.decompose()
x=d.new_tag('script',src='/app-assets/leaf-vision.js?v=20261022-complete');d.body.append(x)
p.write_text(str(d))
for p in [*R.glob('tools/*/index.html'),*R.glob('books/*.html')]:
 s=p.read_text();s=re.sub(r'<script src="/app-assets/garden-backup\.js[^"]*"[^>]*></script>\s*','',s)
 s=s.replace('</body>','<script src="/app-assets/garden-backup.js?v=20261022-complete"></script></body>');p.write_text(s)
p=R/'tools/my-garden/index.html';s=p.read_text().replace('Use each tool’s Save control, and export backups where offered.','Use each tool’s Save control, then Backup &amp; Restore My Garden to keep a file or move your garden to another device.');p.write_text(s)
print('Completed shared backup controls on 13 tool/dashboard pages; 50 companion, 51 harvest and 54 diagnostic/trait entries; local vision UI retained.')
p=R/'help/index.html';d=Soup(p.read_text(),'html.parser')
old=d.select_one('#backup-restore')
if old:old.decompose()
section=d.new_tag('details',id='backup-restore');summary=d.new_tag('summary');summary.string='Back up, restore or move your garden to another device';section.append(summary);ol=d.new_tag('ol')
for text in ["Save your work in each tool first. Unsaved work and photo files are not included in a backup.","Open Backup & Restore My Garden near the bottom of any tool. In Garden Planner, use Backup & Restore on the canvas.","Choose Download garden backup. Keep the JSON file somewhere private; it can include your garden location and personal notes.","On the same device or another device, open Perennial Home & Gardens, open Backup & Restore, then choose the file.","Review the listed sections. Add missing sections keeps sections already saved on that device. Replace included sections replaces only the sections listed in the file.","Check the confirmation box and choose Restore reviewed backup. Keep the automatic before-restore safety download, then choose Reload tools.","This transfers data by file. It does not create an account or turn on automatic cloud synchronization."]:
 li=d.new_tag('li');li.string=text;ol.append(li)
section.append(ol);d.select_one('#gardenGuides').append(section)
idguide=d.select_one('#plant-identifier ol')
if idguide:
 idguide.clear()
 for text in ["Use Upload for an existing photo or Take photo for your device's camera option. Add whole-plant, close-up, leaf-underside and context views as useful. JPG, PNG and WebP up to 15 MB are supported; convert HEIC to JPEG first.","Choose the symptoms and conditions you can confirm, then Analyze Evidence for guided screening.","For a known apple, cherry, corn, grape, peach, bell pepper, potato, strawberry or tomato, you can also select a leaf view and choose Compare leaf photo. The experimental model downloads once requested and runs on this device.","Read the model's measured limits. Its suggestions can be wrong and are not laboratory diagnoses or general species identification.","Choose Save comparison to My Garden, or use Analyze Evidence followed by Save to My Garden. The saved report contains observations and model suggestions, not photo files.","Print Report creates a printable health report. Saved reports also appear in My Garden and import into Garden Journal."]:
  li=d.new_tag('li');li.string=text;idguide.append(li)
# The guide search updates this count after page load; keep its initial value accurate too.
count=d.select_one('#guideCount')
if count:count.string=str(len(d.select('#gardenGuides details')))+' step-by-step guides'
p.write_text(str(d))

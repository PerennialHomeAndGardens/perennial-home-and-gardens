"""Compact the existing, sourced Library data for on-demand assistant lookup."""
import json,re,gzip
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def read(p):return json.loads((R/p).read_text())
plants=read('tools/garden-library/plant_profiles.json');care=read('tools/garden-library/plant_care_enrichment.json');usda=read('tools/garden-library/plant_enrichment.json')
fields={'light':'Light','soilTexture':'Soil texture','soilPH':'Soil pH','soilDrainage':'Drainage','usdaHardinessZones':'Hardiness zones','propagation':'Propagation','lifeCycle':'Life cycle','flowerColor':'Flower color','flowerBloomTime':'Bloom season','dimensions':'Dimensions','plantHabit':'Habit','problems':'Cautions'}
rows=[]
for p in plants:
 c=care.get(p['id'],{});u=usda.get(p['id'],{});facts={label:', '.join(c[key]) for key,label in fields.items() if c.get(key)}
 if not facts.get('Life cycle') and u.get('duration'):facts['Life cycle']=', '.join(u['duration'])
 names=[]
 for name in [p.get('displayName',''),*p.get('commonNames',[]),*p.get('synonyms',[])]:
  for n in re.split(r'[,;]',name):
   n=re.sub(r'^\(\d+\)\s*','',n).strip()
   if n and n not in names:names.append(n)
 rows.append([p['id'],p['scientificName'],names,p.get('family',''),facts,c.get('sourceUrl') or u.get('usdaProfileUrl') or '',bool(c)])
value={'version':'20261020-polish','fields':['id','scientificName','names','family','facts','source','extensionCare'],'plants':rows}
b=json.dumps(value,separators=(',',':'),ensure_ascii=False).encode();(R/'app-assets/tanya-botany-index.json').write_bytes(b);(R/'app-assets/tanya-botany-index.json.gz').write_bytes(gzip.compress(b,mtime=0))
kb=read('app-assets/tanya-knowledge.json');business_ids={'about','decade','services','coaching','design','installation','location','price','booking','free','email','join','app','share','jukebox','courses','products','statuary','structures','tools','library','zone','calendar','calculator','companions','identifier','harvest','journal'}
# These are alternate phrasings of confirmed existing answers, not new business claims.
phrases={
'about':['What is Perennial Home and Gardens?','What does Perennial do?','Tell me about your company','What is your business about?'],
'decade':['How many years have you been doing this?','How long has Perennial been around?','What is your business experience?'],
'services':['What can I hire Perennial to do?','What garden services are available?','Do you offer garden help?'],
'coaching':['Do you offer garden consultations?','Can Tanya help me plan my garden?','Can I get gardening coaching?'],
'design':['Do you offer garden design?','Can you help design a garden layout?','Can you plan my beds?'],
'installation':['Can you help build raised beds?','Do you offer garden installation?','Can I ask about installing beds?'],
'location':['What area do you serve?','Where is Perennial located?','Do you work in Southern Maryland?'],
'price':['Can I get a service quote?','What are your prices?','How do I find out the cost?'],
'booking':['How can I contact Perennial?','How do I request a consultation?','Where can I send a service inquiry?'],
'free':['Where are the resources?','How do I get the worksheets?','Where can I download garden worksheets?','How do I open the resource library?'],
'email':['Where does my signup email go?','Will the resource form add me to a mailing list?','How are resource signups stored?'],
'join':['What happens if I click Join?','How do I join the community?','What does joining give me?'],
'app':['Can I put this on my phone home screen?','How do I install Perennial?','Is there an app to install?'],
'share':['Can I share Perennial with a friend?','How can I send someone this website?','Where is the share control?'],
'jukebox':['Where is the music player?','How do I open the jukebox?','Can I listen to music here?'],
'courses':['Where are your classes?','What can I learn from Perennial?','Do you have gardening courses?'],
'products':['Where are the digital planners?','Do you sell garden journals?','What downloadable products do you have?'],
'statuary':['Do you have garden statues?','Where can I find garden accents?','What outdoor statuary is available?'],
'structures':['Where can I browse greenhouses?','Do you have garden structures?','Where are the garden structure products?'],
'tools':['What tools does the website include?','What can the garden apps do?','Show me the garden applications'],
'library':['How do I open the Garden Library?','Where is the plant reference library?','Where can I search gardening terms?'],
'zone':['Where can I look up my hardiness zone?','Which app finds my growing zone?','How do I find my frost dates?'],
'calendar':['Where is the seasonal planting calendar?','Which tool helps with planting dates?','How do I open Seasonal Calendar?'],
'calculator':['Which app calculates soil volume?','Where is the garden calculator?','How can I estimate compost quantities?'],
'companions':['Where is the companion planting app?','Which tool checks plant combinations?','How do I open Plant Companions?'],
'identifier':['Where do I add plant photos?','Which tool helps identify plants?','How does the plant identification app work?'],
'harvest':['Where is the Harvest Checker?','Which app helps decide harvest timing?','How do I open the harvest tool?'],
'journal':['Where can I record garden observations?','Where are garden logs?','How do I open the garden journal?']}
lookup={e['id']:e for e in kb['entries']};entries=[]
for id,qs in phrases.items():
 for q in qs:entries.append({'question':q,'answerId':id})
# Add only distinct, factual variants until there are at least100 supported business/tool intents.
for e in kb['entries']:
 if e['id'] in business_ids:entries.append({'question':e['question'],'answerId':e['id']})
(R/'app-assets/tanya-business-aliases.json').write_text(json.dumps(entries,separators=(',',':'),ensure_ascii=False))
print('Plant records:',len(rows),'Extension care profiles:',sum(x[6] for x in rows),'raw bytes:',len(b),'gzip bytes:',len(gzip.compress(b)),'business phrasings:',len(entries))

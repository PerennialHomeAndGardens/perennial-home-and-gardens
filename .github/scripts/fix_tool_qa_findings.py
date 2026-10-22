"""Targeted corrections discovered during functional tool QA; preserve saved data."""
from pathlib import Path
from bs4 import BeautifulSoup as Soup
R=Path(__file__).resolve().parents[2]
p=R/'tools/plant-identifier/index.html';s=p.read_text()
start=s.index('const photoRequests={};') if 'const photoRequests={};' in s else s.index('function readPhoto(');end=s.index('function renderPhotoAnalysis()',start)
s=s[:start]+'''const photoRequests={};
function photoMessage(id,text){let m=document.getElementById('photo-status-'+id);if(!m){m=document.createElement('small');m.id='photo-status-'+id;m.setAttribute('role','status');$('slot-'+id).append(m)}m.textContent=text;}
async function readPhoto(id,file){
 if(!file)return;const token=Symbol();photoRequests[id]=token;
 if(!/^image\\/(jpeg|png|webp)$/i.test(file.type)){photoMessage(id,'Choose a JPG, PNG or WebP photo. For HEIC, export or share a JPEG first.');$('photo-'+id).value='';return;}
 if(!file.size||file.size>15*1024*1024){photoMessage(id,'Choose a non-empty photo smaller than 15 MB.');$('photo-'+id).value='';return;}
 photoMessage(id,'Reading photo…');
 try{
  const src=await new Promise((resolve,reject)=>{const r=new FileReader();r.onload=()=>resolve(r.result);r.onerror=()=>reject(Error('read'));r.onabort=()=>reject(Error('read'));r.readAsDataURL(file)});
  const analysis=await analyzeImage(src,file);
  if(photoRequests[id]!==token)return;
  photos[id]={type:id,name:file.name,data:src,analysis};$('img-'+id).src=src;$('slot-'+id).classList.add('has');
  photoMessage(id,'Photo ready. Review the quality notes below.');renderPhotoAnalysis();
 }catch{if(photoRequests[id]!==token)return;photoMessage(id,'This photo could not be opened. Try a JPG, PNG or WebP image.');$('photo-'+id).value='';}
}
function removePhoto(id){photoRequests[id]=Symbol();delete photos[id];$('slot-'+id).classList.remove('has');$('img-'+id).removeAttribute('src');$('photo-'+id).value='';photoMessage(id,'Photo removed.');renderPhotoAnalysis();}
async function analyzeImage(src,file){const img=new Image();await new Promise((res,rej)=>{img.onload=res;img.onerror=rej;img.src=src});if(img.width*img.height>50000000)throw Error('dimensions');const canvas=document.createElement('canvas'),max=220,scale=Math.min(1,max/Math.max(img.width,img.height));canvas.width=Math.max(1,Math.round(img.width*scale));canvas.height=Math.max(1,Math.round(img.height*scale));const c=canvas.getContext('2d',{willReadFrequently:true});c.drawImage(img,0,0,canvas.width,canvas.height);const data=c.getImageData(0,0,canvas.width,canvas.height).data;let n=0,sum=0,sum2=0,green=0,yellow=0,brown=0,white=0,dark=0,edge=0,prev=null;for(let i=0;i<data.length;i+=4){const r=data[i],g=data[i+1],b=data[i+2],br=(r+g+b)/3;n++;sum+=br;sum2+=br*br;if(g>r*1.08&&g>b*1.08&&g>55)green++;if(r>115&&g>90&&g<r*1.08&&b<95)yellow++;if(r>70&&r>g*1.15&&g>b*1.05&&b<100)brown++;if(r>205&&g>205&&b>205)white++;if(br<55)dark++;if(prev!==null)edge+=Math.abs(br-prev);prev=br}const avg=sum/n,std=Math.sqrt(Math.max(0,sum2/n-avg*avg)),edgeAvg=edge/Math.max(1,n-1);return{w:img.width,h:img.height,size:file.size,brightness:avg,contrast:std,edge:edgeAvg,green:green/n,yellow:yellow/n,brown:brown/n,white:white/n,dark:dark/n};}
''' + s[end:]
s=s.replace('if(!arr.length){$("visualCueBox").style.display="none";return}', 'if(!arr.length){$("visualCueBox").style.display="none";document.querySelectorAll("#symptoms .suggested").forEach(b=>b.classList.remove("suggested"));return}')
s=s.replace("'<div class=\"line\"><b>'+a+'</b><span>'+b+'</span></div>'", "'<div class=\"line\"><b>'+safeReportText(a)+'</b><span>'+safeReportText(b)+'</span></div>'")
if 'function safeReportText(' not in s:s=s.replace('function reportLines(matches)', '''function safeReportText(v){return String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function reportLines(matches)''')
s=s.replace('<span class="badge">Secure-AI Ready</span>','<span class="badge">Guided screening · no automatic photo diagnosis</span>')
s=s.replace('Photos stay in this browser session; saved reports store observations rather than full images.', 'JPG, PNG and WebP photos up to 15 MB are supported. Photos stay in this tab until refresh or Clear; saved reports keep observations, not the photo files.')
s=s.replace('capture="environment"','') # Allow album selection and the browser\'s camera option.
s=s.replace('$("saveReport").onclick=()=>{const key=', '$("saveReport").onclick=()=>{identify();const key=')
s=s.replace('$("tryAI").onclick=async()=>{', '$("tryAI").onclick=async()=>{')
ai_start=s.index('$("tryAI").onclick=');ai_end=s.index('\nfetch("../garden-library/plant_profiles.json")',ai_start)
s=s[:ai_start]+'''$("tryAI").textContent="Photo Analysis Status";
$("tryAI").onclick=()=>{$("aiStatus").textContent="Automatic photo identification is not connected. Your uploads support quality checks and guided symptom screening.";$("aiDot").classList.remove("ready");};
'''+s[ai_end:]
s=s.replace('The app is now structured for a private server-side vision model. On GitHub Pages, API credentials cannot be safely stored in browser code, so the secure model call remains disabled until a dedicated Perennial backend is connected.', 'Automatic identification of a plant or disease from a photo is not available yet. Use the photo-quality notes and select the symptoms you can confirm, then choose Analyze Evidence for guided screening.')
if 'if(!Array.isArray(a))a=[];' not in s:s=s.replace("a.unshift({date:new Date().toISOString()", "if(!Array.isArray(a))a=[];a.unshift({date:new Date().toISOString()")
s=s.replace('localStorage.setItem(key,JSON.stringify(a.slice(0,75)));$("report")', 'try{localStorage.setItem(key,JSON.stringify(a.slice(0,75)))}catch{$("resultMeta").textContent="This browser could not save the report. Print it or free browser storage and try again.";return}$("report")')
p.write_text(s)
# Reject negative/nonfinite quantities instead of producing plausible-looking bad estimates.
p=R/'tools/garden-calculator/index.html';s=p.read_text();s=s.replace('num=id=>parseFloat($(id).value)||0', 'num=id=>{const v=Number($(id).value);return Number.isFinite(v)&&v>0?v:0}')
p.write_text(s)
# Saved layouts must keep unique object IDs after opening an existing layout.
p=R/'tools/garden-planner/index.html';s=p.read_text();s=s.replace('.replace(/D/g,"")','.replace(/\\D/g,"")')
if 'function safePlanName(' not in s:s=s.replace('function renderSaved(){','function safePlanName(s){const n=document.createElement("span");n.textContent=String(s??"");return n.innerHTML;}\nfunction renderSaved(){')
s=s.replace('+s.name+"</b>', '+safePlanName(s.name)+"</b>')
p.write_text(s)
# Enforce the existing input constraints before standalone save buttons run.
validation='''document.addEventListener('click',e=>{const id=e.target.closest('button')?.id;const fields={addItem:['iQty','iMin','iValue'],addShopping:['sQty','sPrice'],addPurchase:['pQty','pCost'],saveBudget:['bTotal','bPlants','bSoil','bTools','bOther'],addHarvest:['hWeight','hCount','hDays'],addSeed:['seedYear','seedDTM','seedSpacing'],addTray:['trayGermDays'],addSucc:['succRounds'],applySize:['gardenW','gardenH']}[id];if(!fields)return;for(const name of fields){const f=document.getElementById(name);if(f&&!f.checkValidity()){e.preventDefault();e.stopImmediatePropagation();f.reportValidity();return}}},true);'''
for slug in ['garden-inventory','harvest-records','seed-starting','garden-planner']:
 p=R/'tools'/slug/'index.html';d=Soup(p.read_text(),'html.parser')
 for n in d.select('#phg-qa-number-validation'):n.decompose()
 n=d.new_tag('script',id='phg-qa-number-validation');n.string=validation;d.body.append(n);p.write_text(str(d))
print('Applied identifier upload/error/race/text fixes, positive calculator validation and saved planner ID correction.')

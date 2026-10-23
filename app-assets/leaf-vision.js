/* On-device leaf comparison. Greenathon Plant AI, Apache-2.0; see plant-vision/NOTICE.md. */
(()=>{'use strict';const bridge=window.PHGIdentifier;if(!bridge)return;
const crop=document.getElementById('phgVisionCrop'),button=document.getElementById('phgVisionRun'),output=document.getElementById('phgVisionResult'),status=document.getElementById('phgVisionStatus'),view=document.getElementById('phgVisionView');
let ready=null,labels=null,result=null,resultSignature=null,revision=0,busy=false;
const el=(t,s)=>{const e=document.createElement(t);if(s)e.textContent=s;return e;};
const current=()=>bridge.photos()[view.value];
function signature(){return crop.value+'|'+view.value+'|'+(current()?.data||'');}
function invalidate(){revision++;result=null;resultSignature=null;output.replaceChildren();status.textContent=busy?'Photo selection changed. Run comparison again after loading finishes.':'Select a supported crop and a clear leaf photo. The comparison runs only when you click.';}
new MutationObserver(invalidate).observe(document.getElementById('photoGrid'),{subtree:true,attributes:true,attributeFilter:['src']});crop.onchange=invalidate;view.onchange=invalidate;
async function load(){
 if(ready)return ready;
 ready=(async()=>{
  if(!window.tf)await new Promise((resolve,reject)=>{const s=document.createElement('script');s.src='/app-assets/plant-vision/tf.min.js';s.onload=resolve;s.onerror=()=>{s.remove();reject(Error('The comparison engine could not download. Check your connection and retry.'));};document.head.append(s);});
  // CPU works without GPU permissions and avoids mobile WebGL context failures.
  await tf.setBackend('cpu');await tf.ready();
  const r=await fetch('/app-assets/plant-vision/class_indices.json');if(!r.ok)throw Error('The crop labels could not load.');labels=await r.json();
  return tf.loadLayersModel('/app-assets/plant-vision/model.json');
 })().catch(e=>{ready=null;throw e;});return ready;
}
async function infer(image,cropName){
 const model=await load();let x,y;
 try{
  x=tf.tidy(()=>tf.image.resizeBilinear(tf.browser.fromPixels(image,3),[224,224]).toFloat().div(255).expandDims());y=model.predict(x);const values=Array.from(await y.data());
  if(values.length!==38||values.some(v=>!Number.isFinite(v)))throw Error('The model returned an unreadable result.');
  return Object.entries(labels).map(([i,name])=>({index:+i,label:name,score:values[+i]})).filter(r=>r.label.split('___')[0]===cropName).sort((a,b)=>b.score-a.score);
 }finally{x?.dispose();y?.dispose();}
}
function display(r){
 output.replaceChildren();const strong=r.matches[0]?.score>=.70&&(r.matches.length===1||r.matches[0].score-r.matches[1].score>=.15);
 output.append(el('h4',strong?'Leaf patterns to compare — experimental':'No reliable photo suggestion'));
 output.append(el('p','This model was trained on 38 crop/leaf-condition classes. Field photos can be confidently misclassified. These scores are model outputs, not the probability of a correct diagnosis. Confirm with the symptom checklist and Extension.'));
 for(const m of r.matches.slice(0,3)){const row=el('p');row.append(el('strong',m.label.split('___')[1].replaceAll('_',' ')+' · '+Math.round(m.score*100)+'% model score'));output.append(row);}
 if(r.matches[0]?.label.endsWith('___healthy'))output.append(el('p','A “healthy” model label does not rule out pests, root problems or an unsupported disease.'));
 const save=el('button','Save comparison to My Garden');save.type='button';save.className='btn';save.id='phgSaveLeafComparison';save.onclick=()=>{document.getElementById('saveReport').click();status.textContent=document.getElementById('saveReport').textContent.includes('Saved')?'Comparison saved in your garden-health report.':'The report could not be saved. Review the report message.';};output.append(save);
 const a=el('a','Read the field-photo validation and model limits');a.href='/qa/leaf-model-validation.html';a.target='_blank';a.rel='noopener';output.append(a);
}
button.onclick=async()=>{
 if(busy)return;if(!crop.value){status.textContent='Choose the crop you already know. Unsupported plants require guided screening or expert identification.';crop.focus();return;}
 const p=current();if(!p){status.textContent='Upload a leaf photo in the selected view first.';return;}
 if(Math.min(p.analysis.w,p.analysis.h)<224||p.analysis.brightness<35||p.analysis.brightness>240||p.analysis.contrast<12){status.textContent='Choose a clearer, well-lit leaf photo with at least 224 × 224 pixels. Review the photo-quality notes.';return;}
 busy=true;button.disabled=true;result=null;output.replaceChildren();const token=++revision,sig=signature();status.textContent='Loading the leaf model and comparing on this device… First use downloads about 15 MB. Photos stay here.';
 try{const image=new Image();image.src=p.data;await image.decode();const matches=await infer(image,crop.value);if(token!==revision||sig!==signature()){status.textContent='The selection changed. Click Compare leaf photo again for the current image.';return;}
 result={version:'greenathon-mobilenet-38-b7e8c6f',crop:crop.value,view:view.value,date:new Date().toISOString(),experimental:true,matches:matches.slice(0,3)};resultSignature=sig;display(result);status.textContent='Photo comparison finished on this device. No photo was uploaded. Use the checklist to investigate further.';
 }catch(e){status.textContent=e.message||'This device could not run the model. Guided screening remains available.';}finally{busy=false;button.disabled=false;}
};
window.PHGLeafVision=Object.freeze({savedResult:()=>result&&signature()===resultSignature?result:null,infer,load});
// Camera and gallery remain separate choices; native camera availability depends on the device/browser.
const camera=el('input');camera.type='file';camera.accept='image/*';camera.setAttribute('capture','environment');camera.hidden=true;camera.id='phgCameraInput';document.body.append(camera);let slot='close';
for(const id of ['whole','close','under','context']){const b=el('button','Take photo');b.type='button';b.className='phg-camera-button';b.setAttribute('aria-label','Take photo · '+document.querySelector('label[for="photo-'+id+'"]').textContent.replace('Upload · ',''));b.onclick=()=>{slot=id;camera.value='';camera.click();};document.getElementById('slot-'+id).append(b);}
camera.onchange=()=>{const f=camera.files[0];if(f)bridge.readPhoto(slot,f);};
})();

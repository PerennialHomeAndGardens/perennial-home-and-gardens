/* Required gift-request collection; newsletter is a separate explicit request. */
(() => {
'use strict';
if(window.__phgGiftCapture)return;window.__phgGiftCapture=true;
const endpoint='https://formsubmit.co/ajax/perennialhomeandgardens@gmail.com';
const folder='https://drive.google.com/drive/folders/1Z8FywZpky3tPu-j7M_tYHOgGP5ZXG8bc?usp=drive_link';
const $=s=>document.querySelector(s), pending=new WeakSet();
const make=(tag,text)=>{const n=document.createElement(tag);if(text!==undefined)n.textContent=text;return n;};
function feedback(host){let n=host.querySelector('[data-phg-capture-status]');if(!n){n=make('p');n.dataset.phgCaptureStatus='';n.setAttribute('role','status');host.append(n);}return n;}
function finish(kind){
 $('#phg-gift-access')?.remove();
 const d=make('dialog');d.id='phg-gift-access';d.className='x-jukebox';d.style.cssText='max-height:90dvh;overflow:auto';
 const head=make('div');head.className='x-dialog-heading';const copy=make('div');copy.append(make('small','Perennial Home & Gardens'),make('h2',kind==='gift'?'Your garden gifts are ready':'Your newsletter request was received'));
 const close=make('button','×');close.type='button';close.className='x-action';close.setAttribute('aria-label','Close gift request confirmation');close.onclick=()=>d.close();head.append(copy,close);d.append(head);
 if(kind==='gift'){d.append(make('p','Choose the Plant Profile Sheet and Houseplant Care Worksheet in your gifts folder.'));const a=make('a','Open My Garden Gifts');a.className='x-action x-wide';a.href=folder;a.target='_blank';a.rel='noopener noreferrer';d.append(a);}
 else d.append(make('p','Thank you for requesting Perennial Garden Magazine. Your request has been submitted to Perennial Home & Gardens.'));
 document.body.append(d);d.showModal();
}
async function submit(host,nameInput,emailInput,kind,button){
 if(pending.has(host))return;
 const status=feedback(host);
 for(const input of [nameInput,emailInput].filter(Boolean)){input.value=input.value.trim();if(!input.reportValidity()){status.textContent=kind==='gift'?'Enter your name and a valid email to access your garden gifts.':'Enter a valid email to request the magazine.';return;}}
 if(kind==='gift'&&!nameInput?.value){status.textContent='Enter your name to access your garden gifts.';nameInput?.focus();return;}
 const trap=host.querySelector('[name="_honey"]');if(trap?.value)return;
 pending.add(host);if(button)button.disabled=true;status.textContent='Saving your details…';
 const controller=new AbortController(),timer=setTimeout(()=>controller.abort(),15000);
 try{
  const response=await fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},signal:controller.signal,body:JSON.stringify({name:nameInput?.value||'',email:emailInput.value,request_type:kind==='gift'?'Garden gifts download request':'Perennial Garden Magazine signup',newsletter_requested:kind==='gift'?'No — garden gifts only':'Yes — explicit magazine signup',requested_resource:host.querySelector('[name="phg-worksheet"]:checked')?.value||(kind==='gift'?'Plant Profile Sheet and Houseplant Care Worksheet':''),_subject:kind==='gift'?'[Perennial Garden Gifts] New download request':'[Perennial Garden Magazine] Newsletter request',_url:location.origin+location.pathname,_honey:trap?.value||''})});
  const result=await response.json();
  if(!response.ok||!(result.success===true||result.success==='true'))throw Error('Collection not acknowledged');
  if(kind==='gift'){try{localStorage.setItem('phg_freebie_claimed','1');}catch{}}
  status.textContent='Your request was received.';
  if(host.id==='freebieModal'&&!host.classList.contains('on'))return;
  if(host.tagName==='DIALOG'&&!host.open)return;
  if(host.tagName==='DIALOG')host.close();host.classList.remove('on');finish(kind);
 }catch{status.textContent='We could not save your request. Please try again. Your details are still here.';}
 finally{clearTimeout(timer);pending.delete(host);if(button)button.disabled=false;}
}
function inputs(nameId,emailId){
 const name=document.getElementById(nameId),email=document.getElementById(emailId);
 if(name){name.required=true;name.name='name';name.autocomplete='name';name.setAttribute('aria-label','Name');}
 if(email){email.required=true;email.name='email';email.type='email';email.autocomplete='email';email.placeholder='Your email address';email.setAttribute('aria-label','Email address');}
 return [name,email];
}
function honeypot(host){if(host.querySelector('[name="_honey"]'))return;const trap=make('input');trap.name='_honey';trap.type='text';trap.tabIndex=-1;trap.autocomplete='off';trap.hidden=true;host.append(trap);}
function refineHome(){
 const section=$('#free-resources');if(section){const p=section.querySelector('p');if(p)p.textContent='Two practical printables for your next growing project. Enter your name and email to access your garden gifts.';for(const n of section.querySelectorAll('p'))if(n!==p&&/Email is optional|valid email|Newsletter requests/.test(n.textContent))n.textContent='Enter your name and email to unlock the gifts folder.';const b=section.querySelector('button');if(b)b.textContent='Get My Garden Gifts';inputs('resourceName','resourceEmail');honeypot(section);}
 const modal=$('#freebieModal');if(modal){const title=modal.querySelector('h2'),intro=modal.querySelector('.freebieIntro'),fine=modal.querySelector('.freebieFine'),b=modal.querySelector('button.btn');if(title)title.textContent='A garden gift for you.';if(intro)intro.textContent='Enter your name and email to access your Plant Profile Sheet and Houseplant Care Worksheet.';if(fine)fine.textContent='Both fields are required to unlock your garden gifts.';if(b)b.textContent='Get My Garden Gifts';inputs('freebieName','freebieEmail');honeypot(modal);}
}
window.claimFreeResourceSection=()=>{const host=$('#free-resources');if(host)submit(host,...inputs('resourceName','resourceEmail'),'gift',host.querySelector('button'));};
window.claimFreebie=()=>{const host=$('#freebieModal');if(host)submit(host,...inputs('freebieName','freebieEmail'),'gift',host.querySelector('button.btn'));};
const previous=window.openFreebie;if(previous)window.openFreebie=(...args)=>{previous(...args);refineHome();};
function bindPrompts(){
 const gift=$('#phg-resource-prompt');if(gift&&!gift.dataset.captureBound){gift.dataset.captureBound='1';const form=gift.querySelector('form'),email=form?.querySelector('input[type=email]');if(form&&email){const label=make('label','Your name'),name=make('input');name.required=true;name.name='name';name.autocomplete='name';name.setAttribute('aria-label','Name');label.append(name);form.prepend(label);email.required=true;email.setAttribute('aria-label','Email address');const emailLabel=email.closest('label');if(emailLabel?.firstChild?.nodeType===3)emailLabel.firstChild.textContent='Email address';gift.querySelector('p').textContent='Enter your name and email to access your garden gifts.';honeypot(form);const b=form.querySelector('[type=submit]');b.textContent='Get My Garden Gifts';form.onsubmit=e=>{e.preventDefault();submit(gift,name,email,'gift',b);};}}
 const magazine=$('#phg-newsletter-prompt');if(magazine&&!magazine.dataset.captureBound){magazine.dataset.captureBound='1';const form=magazine.querySelector('form'),email=form?.querySelector('input[type=email]');if(form&&email){magazine.querySelector('p').textContent='Join Perennial Garden Magazine for monthly garden ideas, gifts and coupons. Enter your email to request your subscription.';form.querySelector('small')?.remove();honeypot(form);form.onsubmit=e=>{e.preventDefault();submit(magazine,null,email,'newsletter',form.querySelector('[type=submit]'));};}}
}
refineHome();bindPrompts();new MutationObserver(bindPrompts).observe(document.body,{childList:true,subtree:true});
})();

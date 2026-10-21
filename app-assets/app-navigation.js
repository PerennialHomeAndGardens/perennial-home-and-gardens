(()=>{'use strict';if(window.__phgNavigationPolish)return;window.__phgNavigationPolish=true;
let navigating=false,timer=null,whirl=null;const reduce=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
function reset(){navigating=false;clearTimeout(timer);document.querySelector('.phg-portal')?.remove();document.documentElement.classList.remove('phg-arriving');}
function init(){
 whirl=new Audio('/app-assets/audio/soft-whirl.wav');whirl.preload='auto';whirl.volume=.85;whirl.hidden=true;whirl.dataset.phgTransitionSound='';document.body.append(whirl);
 document.querySelectorAll('.phg-back').forEach(a=>a.addEventListener('click',e=>{if(e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;let internal=false;try{internal=!!document.referrer&&new URL(document.referrer).origin===location.origin;}catch{}if(internal&&history.length>1){e.preventDefault();history.back();}}));
 document.addEventListener('click',e=>{const a=e.target.closest?.('a[href]');if(!a||e.defaultPrevented||e.button!==0||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey||a.target==='_blank'||a.hasAttribute('download')||a.classList.contains('phg-back'))return;const url=new URL(a.href,location.href);if(url.origin!==location.origin||!/^\/tools\/[^/]+\/(?:index\.html)?$/.test(url.pathname)||url.pathname===location.pathname)return;if(reduce())return;e.preventDefault();if(navigating)return;navigating=true;try{sessionStorage.setItem('phg-app-arrival',JSON.stringify({path:url.pathname,at:Date.now()}));}catch{}const overlay=document.createElement('div');overlay.className='phg-portal active';overlay.setAttribute('aria-hidden','true');document.body.append(overlay);whirl.currentTime=0;whirl.play().catch(()=>{});timer=setTimeout(()=>location.assign(url.href),1350);});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
window.addEventListener('pageshow',e=>{if(e.persisted)reset();});window.addEventListener('pagehide',()=>{clearTimeout(timer);whirl?.pause();});
})();

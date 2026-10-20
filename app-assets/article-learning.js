(()=>{'use strict';
document.querySelectorAll('.phg-quiz').forEach(quiz=>quiz.querySelectorAll('[data-answer]').forEach(field=>{
 const button=field.querySelector('button'),output=field.querySelector('output');button.onclick=()=>{
  const chosen=field.querySelector('input:checked');if(!chosen){output.textContent='Choose an answer first.';return;}
  const correct=Number(chosen.value)===Number(field.dataset.answer);field.dataset.correct=String(correct);output.textContent=(correct?'You got it. ':'Try again. ')+field.dataset.explanation;
  if(!quiz.hasAttribute('data-pretest'))feedback(correct,button);
 };
}));
function feedback(correct,button){
 try{const C=window.AudioContext||window.webkitAudioContext;if(C){const c=new C(),o=c.createOscillator(),g=c.createGain();o.connect(g);g.connect(c.destination);o.frequency.value=correct?660:150;o.type=correct?'sine':'triangle';g.gain.setValueAtTime(.035,c.currentTime);g.gain.exponentialRampToValueAtTime(.001,c.currentTime+.2);o.start();o.stop(c.currentTime+.22);setTimeout(()=>c.close(),400);}}catch{}
 if(!correct||matchMedia('(prefers-reduced-motion: reduce)').matches)return;
 const r=button.getBoundingClientRect();for(let i=0;i<28;i++){const n=document.createElement('i');n.className='phg-confetti';n.style.cssText='left:'+(r.left+r.width/2)+'px;top:'+r.top+'px;background:'+['#91ae78','#fff','#d9b9cf','#c6bdd9','#e7dcc2'][i%5]+';--drift:'+(Math.random()*280-140)+'px';document.body.append(n);setTimeout(()=>n.remove(),1300);}
}
document.querySelectorAll('.phg-video-play').forEach(b=>b.onclick=()=>{const id=b.dataset.video;if(!/^[\w-]{11}$/.test(id))return;window.PHGMusic?.pause();const f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&enablejsapi=1';f.title=b.dataset.title||'Garden learning video';f.allow='autoplay; encrypted-media; picture-in-picture';f.allowFullscreen=true;b.closest('.phg-video-stage').replaceChildren(f);});
const search=document.getElementById('article-search'),category=document.getElementById('article-category');function filter(){let count=0;document.querySelectorAll('.phg-article-card').forEach(c=>{const show=(!search.value||c.textContent.toLowerCase().includes(search.value.toLowerCase()))&&(!category.value||c.dataset.category===category.value);c.hidden=!show;if(show)count++;});document.getElementById('article-count').textContent=count+' articles';}
search?.addEventListener('input',filter);category?.addEventListener('change',filter);
const feature=document.querySelector('.phg-catalog-feature');if(feature){const month=new Date().getMonth(),id=month>=8&&month<=10?25:month===11||month<2?15:month<5?0:21;const c=document.querySelector('.phg-article-card[data-id="'+id+'"]');if(c){const d=document.createElement('div'),k=document.createElement('span');k.className='phg-eyebrow';k.textContent='A seasonal place to begin';d.append(k,c.querySelector('h2').cloneNode(true),c.querySelector('p').cloneNode(true),c.querySelector('a').cloneNode(true));feature.append(c.querySelector('img').cloneNode(true),d);}}
})();

/* Shared interaction patterns; each site retains its catalog, identity and page routes. */
(() => {
'use strict';
if(window.__siteExperience)return;window.__siteExperience=true;
const cfg=window.__siteExperienceConfig;if(!cfg)return;
const base=new URL('./',document.currentScript.src), asset=n=>new URL(n,base).href;
const $=s=>document.querySelector(s), all=s=>[...document.querySelectorAll(s)];
const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!==undefined)n.textContent=text;return n;};
function action(text,fn,cls=''){const b=el('button','x-action '+cls,text);b.type='button';b.onclick=fn;return b;}
const icon='<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="4" width="16" height="16" rx="3"/><path d="M8 9h8M8 13h8M8 17h5"/></svg>';
function dialog(type,title){const d=el('dialog',type),head=el('div','x-dialog-heading'),img=el('img');img.src=asset('icon-192.png');img.alt='';const copy=el('div');copy.append(el('small','',cfg.name),el('h2','',title));const close=action('×',()=>d.close());close.setAttribute('aria-label','Close '+title);head.append(copy,close);d.append(head);d.addEventListener('click',e=>{if(e.target===d){const r=d.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)d.close();}});document.body.append(d);return d;}
function divider(index=0){const n=document.createElementNS('http://www.w3.org/2000/svg','svg');n.setAttribute('class','x-divider');n.setAttribute('viewBox','0 0 420 20');n.setAttribute('aria-hidden','true');const designs=['M0 10H100Q130 -5 160 10T220 10T280 10H420','M0 10H140C165 10 160 -6 180 4S170 25 200 10H420','M0 10Q70 2 140 10T280 10T420 10','M0 10H90L110 5L130 15L150 10H280Q300 0 320 10H420'];const start=65+index*11,bend=start+32;const unique='M0 10H'+start+'C'+bend+' 10 '+bend+' '+(1+index%4)+' '+(bend+18)+' '+(1+index%4)+'S'+(bend+7)+' '+(19-index%4)+' '+(bend+40)+' 10H420';n.innerHTML='<path d="M0 10H420" opacity=".3"/><path class="x-flow" d="'+unique+'"/>';n.querySelector('.x-flow').style.animationDuration=(10+index)+'s';n.style.setProperty('--x-divider-speed',(10+index)+'s');return n;}
function addMenu(){
 if(cfg.slug==='perennial-home-and-gardens')return;
 if(cfg.slug==='ie')return; // i.e. already uses the approved compact dropdown.
 const sources=all(cfg.navSources).filter(n=>!n.closest('.x-menu'));
 if(!sources.length)return;
 const host=$(cfg.header)||sources[0].parentElement;
 const menu=dialog('x-menu','Menu'),items=el('nav','x-menu-items');items.setAttribute('aria-label',cfg.name+' navigation');menu.append(items);menu.addEventListener('close',()=>{all('.x-menu-toggle').forEach(b=>b.setAttribute('aria-expanded','false'));});
 function refresh(){
  items.replaceChildren();const seen=new Set(),members=[];
  for(const source of sources)for(const n of source.querySelectorAll('a[href],button')){
   if(n.closest('.site-app-button')||n.matches('.site-app-button,.x-menu-toggle,.drop-toggle')||n.matches(cfg.mediaTrigger||'[data-no-media]')||/theme|sound|music|light|announcement/i.test(n.id+' '+n.getAttribute('data-etp-action')))continue;
   const label=n.getAttribute('data-label')||n.querySelector('.label,.nav-label,.wdw-sr-only')?.textContent||n.closest('.etp-nav-item')?.querySelector('.etp-tip')?.textContent||n.getAttribute('aria-label')||n.querySelector('span:last-child')?.textContent||n.textContent;
   const contextLabel=cfg.slug==='ie-casino-games'&&n.dataset.rule?(n.dataset.rule==='time'?'Time Travel Slots':'Casa 21')+' · House Rules':label;
   const text=String(contextLabel||'').replace(/\s+/g,' ').trim();if(!text||/^(close|close menu|close navigation)$/i.test(text)||text==='Install App'||seen.has(text))continue;seen.add(text);
   const b=el(n.tagName==='A'?'a':'button','x-menu-item');if(n.tagName==='A')b.href=n.href;else{b.type='button';b.disabled=n.disabled;}b.innerHTML=icon;const span=el('span','',text);b.append(span);
   b.addEventListener('click',e=>{e.preventDefault();menu.close();n.click();});
   if(/membership|members only|join|subscribe/i.test(text)){b.classList.add('x-membership');members.push(b);}else items.append(b);
  }
  if(cfg.slug==='basketball-brilliance'&&!items.children.length){for(const role of ['coach','player','parent']){const b=el('button','x-menu-item',role[0].toUpperCase()+role.slice(1));b.type='button';b.onclick=()=>{menu.close();document.querySelector('.hs-'+role)?.click();};items.append(b);}}
  members.forEach(n=>items.append(n));
  const install=el('button','x-menu-item','Install App');install.type='button';install.onclick=()=>{menu.close();window.siteInstallApp?.();};items.insertBefore(install,members[0]||null);
 }
 all(cfg.preserve||'[data-no-preserve]').forEach(n=>{if(sources.some(s=>s.contains(n)))host.append(n);});
 sources.forEach(n=>{n.classList.add('x-hidden-nav');n.style.setProperty('display','none','important');new MutationObserver(refresh).observe(n,{childList:true,subtree:true});});refresh();
 all(cfg.oldMenuTriggers||'[data-no-old-menu]').forEach(n=>{n.classList.add('x-hidden-nav');n.style.setProperty('display','none','important');});
 function toggle(){const b=el('button','x-menu-toggle');b.type='button';b.setAttribute('aria-label','Open '+cfg.name+' navigation');b.setAttribute('aria-haspopup','dialog');b.setAttribute('aria-expanded','false');b.setAttribute('aria-controls','site-experience-menu');b.innerHTML='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4v16M17 4v16"/></svg>';b.onclick=()=>{refresh();menu.showModal();b.setAttribute('aria-expanded','true');};return b;}
 menu.id='site-experience-menu';host.append(toggle());
 // The Basketball Brilliance entry screen intentionally has no header.
 if(cfg.slug==='basketball-brilliance'&&$('#entryStage')){const dock=el('div','x-entry-menu');dock.style.cssText='position:absolute;left:12px;top:12px;z-index:6';dock.append(toggle());$('#entryStage').append(dock);}
 // Keep install access outside the navigation containers that were collapsed.
 const top=$('.site-app-desktop');if(top&&!host.contains(top))host.insertBefore(top,host.lastElementChild);
}
function brandNative(){
 const panel=$(cfg.nativePanel||'[data-no-native]');if(!panel)return;
 panel.classList.add('x-native-panel');
 if(cfg.slug==='ie'){
  const identity=panel.querySelector('.music-identity');if(identity&&!identity.querySelector('.x-brand-name')){const small=el('small','x-brand-name','InAct Entertainment');small.style.cssText='display:block;font:11px Georgia,serif';identity.insertBefore(small,identity.lastElementChild);}
  return;
 }
 const heading=panel.querySelector('.jb-heading,.cb-music-heading,.etp-jukebox-brand');
 if(heading&&!panel.querySelector('.x-divider')){const old=panel.querySelector('.jb-divider,.cb-juke-divider,.etp-jukebox-divider');if(old)old.replaceWith(divider(cfg.divider));else heading.after(divider(cfg.divider));}
 if(cfg.slug==='divine-shades-of-brown'&&heading&&!heading.querySelector('.x-brand-name')){const small=el('small','x-brand-name',cfg.name);heading.querySelector('h2')?.before(small);}
 if(cfg.slug==='examine-the-past-home'){const copy=heading?.querySelector('div');if(copy){const h=copy.querySelector('h2'),s=copy.querySelector('span');if(h&&s){h.textContent='Jukebox';s.textContent=cfg.name;copy.prepend(s);}}}
 const summary=panel.querySelector('.jb-personal summary,.cb-favorites summary');if(summary){summary.textContent='› My playlists';}
 if(!panel.querySelector('.x-explore-footer')){const link=el('a','x-action x-wide x-explore-footer','Explore '+cfg.name);link.href=new URL('../',base).href;panel.append(link);}
}
async function genericPlayer(){
 if(!cfg.generic)return;
 const catalog=await fetch(asset('media-library.json')).then(r=>{if(!r.ok)throw Error();return r.json();}).catch(()=>({music:[],motivation:[],movies:[],quiet:[],failed:true}));
 const panel=dialog('x-jukebox','Jukebox');panel.id='site-shared-jukebox';panel.insertBefore(divider(cfg.divider),panel.children[1]||null);
 const back=action('‹ Back',()=>goBack());back.hidden=true;const view=el('div','x-player-view');panel.append(back,view);
 const mini=el('div','x-mini');mini.hidden=true;document.body.append(mini);
 const key='ie-'+cfg.slug+'-jukebox-v1';let saved=[];try{const parsed=JSON.parse(localStorage.getItem(key)||'[]');if(Array.isArray(parsed))saved=parsed.filter(t=>t&&(/^[\w-]{11}$/.test(t.videoId||'')||/^[\w-]{10,100}$/.test(t.listId||'')));}catch{}
 let stack=[],screen={type:'root'},queue=[],current=null,index=-1,yt=null,ready=false,epoch=0,shuffle=false,repeat=false,audio=null,playing=false,apiPromise=null,local=[],timer;
 const status=el('p','x-status');status.setAttribute('role','status');
 function stopOther(){all('audio').forEach(a=>{if(a!==audio&&!a.paused)a.pause();});all('iframe[src*="youtube"]').forEach(f=>{if(!panel.contains(f))f.contentWindow?.postMessage(JSON.stringify({event:'command',func:'pauseVideo',args:[]}),'*');});}
 function persist(){try{localStorage.setItem(key,JSON.stringify(saved.filter(t=>!t.local)));}catch{status.textContent='Saved for this visit; browser storage is unavailable.';}}
 function navigate(next){stack.push(screen);screen=next;render();}
 function goBack(){if(screen.type==='player')pause();screen=stack.pop()||{type:'root'};render();}
 function rootPlaylists(){const details=el('details','x-playlists'),summary=el('summary','','My playlists');details.append(summary,action('Open my playlist',()=>navigate({type:'list',title:'My playlist',items:[...saved,...local]})));
  const form=el('form'),label=el('label','','Add a YouTube video or playlist URL'),url=el('input');url.type='url';url.required=true;url.placeholder='https://www.youtube.com/watch?v=…';label.append(url);const add=action('Add to playlist',()=>{});add.type='submit';form.append(label,add);form.onsubmit=e=>{e.preventDefault();let parsed;try{parsed=new URL(url.value);}catch{status.textContent='Enter a YouTube URL.';return;}const host=parsed.hostname.replace(/^www\./,'');if(!['youtube.com','youtu.be','m.youtube.com','music.youtube.com'].includes(host)){status.textContent='Use a YouTube video or playlist link.';return;}const id=host==='youtu.be'?parsed.pathname.slice(1):parsed.searchParams.get('v'),listId=parsed.searchParams.get('list');if(!/^[\w-]{11}$/.test(id||'')&&!/^[\w-]{10,100}$/.test(listId||'')){status.textContent='That link needs a video or playlist ID.';return;}const t={title:'My YouTube selection',artist:'My playlist',...(id?{videoId:id}:{listId})};if(!saved.some(x=>(id&&x.videoId===id)||(listId&&x.listId===listId)))saved.push(t);persist();url.value='';status.textContent='Added to My playlist.';};details.append(form);
  const files=el('input');files.type='file';files.accept='audio/*';files.multiple=true;const fileLabel=el('label','','Add audio from this device');fileLabel.append(files);files.onchange=()=>{for(const f of files.files){if(!f.type.startsWith('audio/'))continue;local.push({title:f.name,artist:'Local audio',src:URL.createObjectURL(f),local:true});}status.textContent='Local audio added for this visit.';};details.append(fileLabel,el('p','','Your saved selections stay in this browser. Local files must be re-added on a future visit.'));return details;
 }
 function nativeTracks(){return all(cfg.audioSources||'[data-no-audio]').map((a,i)=>({title:a.dataset.trackTitle||a.id?.replace(/Track$/,'').replace(/([A-Z])/g,' $1')||'Site soundtrack',artist:cfg.name,audioId:a.id,id:'site-audio-'+i}));}
 function render(){view.replaceChildren();back.hidden=screen.type==='root';status.textContent='';
  if(screen.type==='root'){
   const grid=el('div','x-root-grid');const siteTracks=nativeTracks();
   if(siteTracks.length&&cfg.slug!=='perennial-home-and-gardens')grid.append(action(cfg.slug==='ie-casino-games'?'Casino Tunes':'Site soundtrack',()=>navigate({type:'list',title:cfg.name+' music',items:siteTracks})));
   if(cfg.slug==='livefit-info'){grid.append(action('Workout Music',()=>navigate({type:'genres'})),action('Recovery Music',()=>navigate({type:'list',title:'Recovery Music',items:catalog.quiet})),action('Quiet Listening',()=>navigate({type:'list',title:'Quiet Listening',items:catalog.quiet})));}else{grid.append(action('Meditation',()=>navigate({type:'list',title:'Meditation',items:catalog.meditation||[]})),action('Music',()=>navigate({type:'genres'})),action('Movies',()=>navigate({type:'list',title:'Movies, Trailers & Documentaries',items:catalog.movies})),action('Motivation',()=>navigate({type:'list',title:'Motivation',items:catalog.motivation})));}
   if(catalog.failed)status.textContent='The media collection could not load. Refresh to try again, or use a site soundtrack or your own audio.';view.append(grid,rootPlaylists());const explore=el('a','x-action x-wide','Explore our resources');explore.href='/#free-resources';explore.onclick=e=>{panel.close();if(!document.getElementById('free-resources'))return;e.preventDefault();document.getElementById('free-resources')?.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});};const credit=el('div','phg-jukebox-credit');credit.innerHTML='<img class="phg-ie-mark" src="/app-assets/ie-logo.png" alt="InAct Entertainment"/><span>Brought to you by InAct Entertainment LLC<br>© '+new Date().getFullYear()+' InAct Entertainment LLC</span>';view.append(explore,credit,status);return;
  }
  if(screen.type==='genres'){
   view.append(el('h3','','Choose a genre'));const grid=el('div','x-root-grid');for(const genre of [...new Set(catalog.music.map(t=>t.genre||'Music'))])grid.append(action(genre,()=>navigate({type:'list',title:genre,items:catalog.music.filter(t=>(t.genre||'Music')===genre)})));view.append(grid);return;
  }
  if(screen.type==='list'){
   view.append(el('h3','',screen.title));if(screen.title==='Movies, Trailers & Documentaries')view.append(el('p','x-status','Garden stories, botanical documentaries and published films. Each selection is labeled as a trailer, film or series. Full viewing may require a provider account or purchase.'));if(!screen.items.length)view.append(el('p','','Save a selection or add local audio in My playlists.'));
   screen.items.forEach((t,i)=>{const row=el('div','x-row');if(t.sourceUrl&&!t.videoId&&!t.listId){const a=el('a','x-action x-track',t.artist+' · '+t.title+' ↗');a.href=t.sourceUrl;a.target='_blank';a.rel='noopener noreferrer';row.append(a);view.append(row);return;}row.append(action(t.artist+' · '+t.title,()=>{queue=screen.items;index=i;navigate({type:'player'});play(t);},'x-track'));if(t.videoId){const exists=saved.some(x=>x.videoId===t.videoId);const save=action(exists?'✓':'+',()=>{saved=exists?saved.filter(x=>x.videoId!==t.videoId):[...saved,t];persist();render();},'x-save');save.setAttribute('aria-label',(exists?'Remove from':'Save to')+' My playlist');row.append(save);}view.append(row);});view.append(status);return;
  }
  if(screen.type==='player'){drawPlayer();}
 }
 function api(){if(window.YT?.Player)return Promise.resolve(window.YT);if(apiPromise)return apiPromise;apiPromise=new Promise((resolve,reject)=>{const old=window.onYouTubeIframeAPIReady;const timeout=setTimeout(()=>{apiPromise=null;reject(Error('Video controls could not connect. Try again.'));},12000);window.onYouTubeIframeAPIReady=()=>{old?.();clearTimeout(timeout);resolve(window.YT);};if(!document.querySelector('script[src*="youtube.com/iframe_api"]')){const s=el('script');s.src='https://www.youtube.com/iframe_api';document.head.append(s);}});return apiPromise;}
 function pause(){if(audio)audio.pause();try{yt?.pauseVideo();}catch{}playing=false;sync();}
 function stop(){pause();if(audio)try{audio.currentTime=0;}catch{}try{yt?.stopVideo();}catch{}sync();}
 window.PHGMusic={pause,stop};
 function sync(){const b=panel.querySelector('[data-x-play]');if(b)b.textContent=playing?'Pause':'Play';mini.hidden=panel.open||!playing;mini.replaceChildren(action('Pause',pause),action('Open',()=>{if(!panel.open)panel.showModal();mini.hidden=true;}),action('Stop',stop));}
 function drawPlayer(){
  view.append(el('h3','',current?current.artist+' · '+current.title:'Loading selection…'));
  const video=el('div','x-video');video.id='x-media-video';view.append(video);
  const controls=el('div','x-transport');const playButton=action('Play',()=>{if(playing)pause();else if(audio){stopOther();audio.play().catch(()=>{status.textContent='Tap Play again to allow audio.';});}else if(yt&&ready)yt.playVideo();else if(current)play(current);});playButton.dataset.xPlay='';
  const sh=action('Shuffle',()=>{shuffle=!shuffle;sh.setAttribute('aria-pressed',String(shuffle));});sh.setAttribute('aria-pressed',String(shuffle));const rp=action('Repeat',()=>{repeat=!repeat;rp.setAttribute('aria-pressed',String(repeat));if(audio)audio.loop=repeat;});rp.setAttribute('aria-pressed',String(repeat));
  controls.append(action('‹',()=>step(-1)),playButton,action('Stop',stop),sh,rp,action('›',()=>step(1)));controls.firstChild.setAttribute('aria-label','Previous track');controls.lastChild.setAttribute('aria-label','Next track');view.append(controls);
  const seek=el('input');seek.type='range';seek.min=0;seek.max=1;seek.value=0;seek.disabled=true;seek.setAttribute('aria-label','Track position');seek.dataset.xSeek='';seek.onchange=()=>{if(audio)audio.currentTime=Number(seek.value);else if(ready)yt.seekTo(Number(seek.value),true);};const vol=el('input');vol.type='range';vol.min=0;vol.max=100;vol.value=70;vol.setAttribute('aria-label','Volume');vol.oninput=()=>{if(audio)audio.volume=Number(vol.value)/100;if(ready)yt.setVolume(Number(vol.value));};const l=el('label','x-slider','Volume');l.append(vol);view.append(seek,l,status);
  view.append(action('Expand player ↗',()=>{const f=video.querySelector('iframe');f?.requestFullscreen?.().catch(()=>{status.textContent='Use the video fullscreen control.';});}));
 }
 async function play(t){
  const token=++epoch;try{yt?.destroy();}catch{}yt=null;ready=false;if(audio)audio.pause();audio=null;current=t;playing=false;view.replaceChildren();drawPlayer();stopOther();const video=$('#x-media-video');
  if(t.src||t.audioId){audio=t.audioId?document.getElementById(t.audioId):new Audio(t.src);if(!audio){status.textContent='The site soundtrack is unavailable on this page.';return;}audio.loop=repeat;audio.volume=.7;const img=el('img');img.src=asset('icon-192.png');img.alt=cfg.name;video.append(img);audio.onplay=()=>{playing=true;sync();};audio.onpause=()=>{playing=false;sync();};audio.onended=()=>repeat?audio.play():step(1);audio.onerror=()=>{status.textContent='Audio could not load. Choose another selection.';};try{await audio.play();}catch{status.textContent='Tap Play to start audio.';}return;}
  try{const YT=await api();if(token!==epoch)return;const target=el('div');video.append(target);yt=new YT.Player(target,{host:'https://www.youtube-nocookie.com',...(t.videoId?{videoId:t.videoId}:{}),playerVars:{autoplay:1,playsinline:1,rel:0,...(t.listId?{listType:'playlist',list:t.listId}:{})},events:{onReady:e=>{if(token!==epoch)return;ready=true;e.target.setVolume(70);e.target.playVideo();},onStateChange:e=>{if(token!==epoch)return;playing=e.data===1;if(e.data===0){if(repeat){yt.seekTo(0,true);yt.playVideo();}else step(1);}sync();},onError:()=>{status.textContent='This video cannot play here. Choose another selection or use its YouTube source.';const link=el('a','x-action','Open on YouTube');link.href=t.videoId?'https://www.youtube.com/watch?v='+t.videoId:'https://www.youtube.com/playlist?list='+t.listId;link.target='_blank';link.rel='noopener';status.append(link);}}});}catch(e){status.textContent=e.message;const source=el('a','x-action','Open on YouTube');source.href=t.videoId?'https://www.youtube.com/watch?v='+t.videoId:'https://www.youtube.com/playlist?list='+t.listId;source.target='_blank';source.rel='noopener';status.append(source);}
 }
 function step(direction){if(!queue.length)return;index=shuffle&&queue.length>1?(index+1+Math.floor(Math.random()*(queue.length-1)))%queue.length:(index+direction+queue.length)%queue.length;screen={type:'player'};render();play(queue[index]);}
 panel.addEventListener('close',sync);const updateClock=()=>{const seek=panel.querySelector('[data-x-seek]');if(!seek)return;let duration=0,time=0;try{duration=audio?audio.duration:ready?yt.getDuration():0;time=audio?audio.currentTime:ready?yt.getCurrentTime():0;}catch{}seek.disabled=!Number.isFinite(duration)||duration<=0;seek.max=String(Number.isFinite(duration)?duration:1);if(document.activeElement!==seek)seek.value=String(time||0);};timer=setInterval(updateClock,750);
 function open(){$('#navlinks')?.classList.remove('open');$('.cleanMenu')?.setAttribute('aria-expanded','false');if(current&&playing&&screen.type==='player'){if(!panel.open)panel.showModal();mini.hidden=true;return;}stack=[];screen={type:'root'};render();if(!panel.open)panel.showModal();mini.hidden=true;}
 document.addEventListener('click',e=>{const trigger=e.target.closest?.(cfg.mediaTrigger||'[data-no-media]');if(trigger){e.preventDefault();e.stopImmediatePropagation();open();}},true);
 if(!$(cfg.mediaTrigger||'[data-no-media]')){const b=action('♫',open);b.setAttribute('aria-label','Open '+cfg.name+' Jukebox');($(cfg.header)||$('header')||document.body).append(b);}
 all(cfg.replacePanel||'[data-no-panel]').forEach(n=>{n.classList.add('x-hidden-nav');n.style.setProperty('display','none','important');});
 window.addEventListener('pagehide',()=>{clearInterval(timer);stop();epoch++;try{yt?.destroy();}catch{}yt=null;ready=false;local.forEach(t=>URL.revokeObjectURL(t.src));local=[];});
 window.addEventListener('pageshow',e=>{if(e.persisted){stack=[];screen={type:'root'};queue=queue.filter(t=>!t.local);if(current?.local)current=null;render();timer=setInterval(updateClock,750);}});
 document.addEventListener('play',e=>{if(playing&&e.target!==audio&&e.target.matches?.('audio,video'))pause();},true);render();
}

function gardenNavigation(){
 const nav=$('#navlinks'),host=$('.newActions'),music=$('#music'),menu=$('.cleanMenu');
 if(!nav||!host||!music||!menu)return;
 const desktop=nav.cloneNode(true);desktop.id='phg-desktop-links';desktop.setAttribute('aria-label','Main navigation');
 desktop.querySelectorAll('button').forEach(n=>n.remove());nav.before(desktop);
 host.querySelectorAll('.desktopShare,.desktopJoin,.site-app-desktop').forEach(n=>n.remove());
 music.innerHTML='<span class="phg-equalizer" aria-hidden="true"><i></i><i></i><i></i></span>';
 music.setAttribute('aria-label','Open Perennial Home and Gardens jukebox');music.removeAttribute('onclick');
 host.append(music,menu);
 const wood=$('.b20WoodBar');if(wood){wood.append(host,nav);$('.b21StickyBrand')?.classList.add('phg-compact-header');}
 menu.setAttribute('aria-controls','navlinks');menu.setAttribute('aria-expanded','false');
 menu.setAttribute('aria-label','Open navigation');nav.setAttribute('aria-label','Full navigation');
 const close=()=>{nav.classList.remove('open');menu.setAttribute('aria-expanded','false');};
 window.toggleMenu=()=>{const open=!nav.classList.contains('open');if(open){$('#ap')?.classList.remove('on');}nav.classList.toggle('open',open);menu.setAttribute('aria-expanded',String(open));};
 nav.querySelectorAll('a,button').forEach(n=>n.addEventListener('click',close));
 document.addEventListener('click',e=>{if(!nav.contains(e.target)&&!menu.contains(e.target))close();});
 document.addEventListener('keydown',e=>{if(e.key==='Escape'){close();$('#ap')?.classList.remove('on');}});
 window.toggleAssistant=()=>{const ap=$('#ap');if(!ap)return;const open=!ap.classList.contains('on');close();$('#shareMenu')?.classList.remove('on');all('dialog[open]').forEach(d=>d.close());ap.classList.toggle('on',open);if(open)$('#q')?.focus();};
 // Mobile keeps the existing dropdown, including its raised Share/Join buttons.
}
function gardenAssistant(){
 const baseQuestion=$('#q'),chat=$('#chat');if(!baseQuestion||!chat)return;
 const get=(name,fallback)=>fetch(asset(name+'?v=20261021-organized')).then(r=>{if(!r.ok)throw Error();return r.json();}).catch(()=>fallback);
 const promise=Promise.all([get('tanya-knowledge.json',{entries:[]}),get('tanya-expert-knowledge.json',[]),get('tanya-business-aliases.json',[])]).then(([kb,extra,aliases])=>{const entries=[...kb.entries,...(Array.isArray(extra)?extra:extra.entries||[])];for(const a of aliases){const e=entries.find(e=>e.id===a.answerId);if(e)(e.aliases||(e.aliases=[])).push(a.question);}return{entries};});
 let last=null,busy=false;
 const normalize=s=>s.toLowerCase().replace(/[’']/g,'').replace(/[^a-z0-9 ]/g,' ').replace(/\s+/g,' ').trim();
 const stop=new Set('a an the i my me you your our we do does can could would should how what when where why is are of for to and in with it this that on about please tell want need have has us get'.split(' '));
 function find(question,kb){
  const q=normalize(question),stem=t=>t.length>4?t.replace(/ies$/,'y').replace(/s$/,''):t;
  const words=text=>[...new Set(normalize(text).split(' ').filter(t=>t.length>2&&!stop.has(t)).map(stem))];
  const exact=kb.entries.find(e=>normalize(e.question)===q||e.aliases?.some(a=>normalize(a)===q));if(exact)return exact;
  const tokens=words(question),docs=kb.entries.map(e=>new Set(words(e.question+' '+(e.keywords||'')+' '+(e.aliases||[]).join(' '))));
  let best=null,score=0;
  for(let i=0;i<kb.entries.length;i++){const e=kb.entries[i];let n=0;
   for(const p of e.phrases||[])if((' '+q+' ').includes(' '+normalize(p)+' '))n+=6+normalize(p).split(' ').length*2;
   for(const t of tokens)if(docs[i].has(t)){const count=docs.filter(d=>d.has(t)).length;n+=2+Math.log(kb.entries.length/count)*2;}
   if(e.exclude?.some(p=>(' '+q+' ').includes(' '+normalize(p)+' ')))n=0;
   if(n>score){score=n;best=e;}
  }
  return score>=7?best:null;
 }
 function bubble(label,text){const b=el('div','bubble'),strong=el('b','',label+': ');b.append(strong,document.createTextNode(text));chat.append(b);return b;}
 function appendAnswer(record){
  const b=bubble('Tanya',record.answer);
  if(record.link){const a=el('a','phg-answer-link',record.linkLabel||'Explore this on Perennial →');a.href=record.link;a.onclick=()=>{$('#ap')?.classList.remove('on');};b.append(el('br'),a);}
  if(record.source){const a=el('a','phg-answer-source','Read the gardening reference ↗');a.href=record.source;a.target='_blank';a.rel='noopener noreferrer';b.append(el('br'),a);}
  chat.scrollTop=chat.scrollHeight;
 }
 window.ask=async()=>{const question=baseQuestion.value.trim();if(!question||busy)return;busy=true;baseQuestion.value='';bubble('You',question);
  try{const kb=await promise;const normalized=normalize(question),exact=kb.entries.find(e=>normalize(e.question)===normalized||e.aliases?.some(a=>normalize(a)===normalized));const reference=exact?null:await window.PHGReference?.lookup(question);const answer=exact||reference||find(question,kb);if(answer){last=answer;appendAnswer(answer);}else appendAnswer({answer:kb.entries.length?'I need a little more detail to give you a useful answer. What plant or garden problem are you working on? Include your location or ZIP code, sunlight, soil moisture and what changed. For a difficult diagnosis, the Garden Library and a local Extension specialist can help; I do not have a confirmed answer for every question.':'My garden reference could not load. Please try again, or contact Perennial for help.',link:'tools/garden-library/',linkLabel:'Open the Garden Library →'});}finally{busy=false;}};
 window.quickAsk=t=>{baseQuestion.value=t;window.ask();};
 window.siteAsk=kind=>{const map={services:'What services do you offer?',statuary:'What kind of statuary do you have?',about:'Tell me about Perennial',courses:'What courses do you offer?'};baseQuestion.value=map[kind]||kind;window.ask();};
 const quick=chat.querySelector('.quick');
 for(const label of ['How long have you been in business?','Where are the free resources?','Why is my hydrangea not blooming?','How does soil pH affect nutrients?']){
  const b=el('button','',label);b.type='button';b.onclick=()=>window.quickAsk(label);quick?.append(b);
 }
 const response=$('#tanyaResponse');if(response)response.textContent='Ask about our services, garden tools, plants, soil, growing seasons or a specific garden problem.';
}


function gardenRefinements(){
 if(/^\/(tools|articles|legal)\//.test(location.pathname)){
  window.toggleShare=async()=>{const data={title:'Perennial Home & Gardens',url:location.origin+'/'};try{if(navigator.share)await navigator.share(data);else if(navigator.clipboard){await navigator.clipboard.writeText(data.url);alert('Website link copied.');}else prompt('Copy this website link:',data.url);}catch{}};
  window.openJoin=()=>location.assign('/?join=1');
 }else if(new URLSearchParams(location.search).get('join')==='1')window.openJoin?.();
 for(const [selector,label] of [['#music','Jukebox'],['.cleanMenu','Menu']]){const n=$(selector);if(n){n.removeAttribute('title');n.dataset.phgTooltip=label;}}
 const contact=$('#contact');
 if(contact){
  const intro=contact.querySelector('.contactGrid>div');
  if(intro){const h=intro.querySelector('h2'),p=intro.querySelector('p'),meta=intro.querySelector('.contactMeta');if(h)h.textContent='How can we help?';if(p)p.textContent='Choose a topic and send us a message.';if(meta)meta.textContent='Garden help, products and partnerships are welcome.';}
  for(const id of ['reason','cn','ce','cm']){const input=document.getElementById(id);const label=input?.closest('.field')?.querySelector('label');if(label)label.htmlFor=id;}
  $('#cn')?.setAttribute('autocomplete','name');$('#ce')?.setAttribute('autocomplete','email');
  const reasonLabel=$('#reason')?.closest('.field')?.querySelector('label');if(reasonLabel)reasonLabel.textContent='Topic';
  const button=contact.querySelector('[type=submit]');if(button)button.textContent='Send message';
  const old=window.updateContactPrompt;
  if(old){window.updateContactPrompt=()=>{old();const m=$('#cm');if(m&&m.value===m.placeholder)m.value='';};window.updateContactPrompt();}
 }
 const footer=$('footer');const install=footer?.querySelector('.site-app-footer-text');if(install)footer.querySelector('.footerLegal')?.append(install);
 const header=$('.b21StickyBrand');
 if(header){
  const embedded=window.top!==window.self;if(embedded){header.hidden=true;header.style.setProperty('display','none','important');}
  else{
   header.addEventListener('focusin',()=>header.classList.remove('phg-header-away'));
  }
 }
 all('a[href="#blog"]').forEach(a=>{if(a.textContent.trim()==='Blog')a.textContent='Articles';});
 if(!location.pathname.includes('/tools/'))gardenPrompts();
 if(window.openFreebie&&!window.openFreebie.phgPolished){const previous=window.openFreebie;const polished=(...args)=>{previous(...args);const modal=document.getElementById('freebieModal')||document.getElementById('phg-resource-prompt');if(modal){const walker=document.createTreeWalker(modal,NodeFilter.SHOW_TEXT);let n;while(n=walker.nextNode()){if(!['SCRIPT','STYLE'].includes(n.parentElement.tagName))n.textContent=n.textContent.replace(/\bfree(?:[- ]+)?/gi,'');}}};polished.phgPolished=true;window.openFreebie=polished;}
}
function gardenPrompts(){
 const read=k=>{try{return sessionStorage.getItem(k);}catch{return null;}};
 const save=k=>{try{sessionStorage.setItem(k,'1');}catch{}};
 const claimed=()=>{try{return localStorage.getItem('phg_freebie_claimed')==='1';}catch{return false;}};
 const busy=()=>document.hidden||!!$('dialog[open],.modal.on,#ap.on,#navlinks.open')||!!document.activeElement?.closest('form')||all('.b17Preview').some(n=>{const r=n.getBoundingClientRect();return r.top<120&&r.bottom>innerHeight*.4;});
 let start=Date.now();try{const previous=Number(sessionStorage.getItem('phg-visit-start'));if(previous>0)start=previous;else sessionStorage.setItem('phg-visit-start',String(start));}catch{}
 if(typeof window.openFreebie!=='function')window.openFreebie=()=>{
  const existing=document.getElementById('phg-resource-prompt');if(existing){existing.showModal();return;}
  const d=dialog('x-jukebox','Two worksheets for your next garden idea');d.id='phg-resource-prompt';d.append(el('p','','Choose a printable to start with. Both worksheets are available in our download folder.'));
  const choices=el('fieldset','phg-resource-choices');choices.append(el('legend','','Choose your worksheet'));
  for(const [i,title,description] of [[0,'Plant Profile Sheet','Plan and record the plants you grow.'],[1,'Houseplant Care Worksheet','Organize your indoor plant care.']]){const label=el('label','phg-resource-choice'),radio=el('input');radio.type='radio';radio.name='phg-worksheet';radio.value=title;radio.checked=i===0;const copy=el('span');copy.append(el('strong','',title),el('small','',description));label.append(radio,copy);choices.append(label);}d.append(choices);
  const form=el('form','phg-newsletter-form'),label=el('label','','Email address'),input=el('input');input.type='email';input.required=true;input.autocomplete='email';label.append(input);const b=action('Open download folder',()=>{});b.type='submit';form.append(label,b);
  form.onsubmit=e=>{e.preventDefault();if(!form.reportValidity())return;try{localStorage.setItem('phg_freebie_claimed','1');localStorage.setItem('phg_freebie_lead',JSON.stringify({email:input.value.trim(),worksheet:d.querySelector('input[name=phg-worksheet]:checked')?.value,time:new Date().toISOString()}));}catch{}window.open('https://drive.google.com/drive/folders/1Z8FywZpky3tPu-j7M_tYHOgGP5ZXG8bc?usp=drive_link','_blank','noopener');d.close();};d.append(form);d.showModal();
 };
 let tick;const check=()=>{
  const elapsed=Date.now()-start;
  if(elapsed>=25000&&!read('phg-b3-resource-offer')){
   if(claimed()){save('phg-b3-resource-offer');}
   else if(!busy()){save('phg-b3-resource-offer');window.openFreebie?.('welcome');}
  }
  if(elapsed>=120000&&!read('phg-b3-tool-offer')&&!busy()){
   save('phg-b3-tool-offer');
   const d=dialog('x-jukebox','Perennial Garden Magazine');d.id='phg-newsletter-prompt';
   d.append(el('p','','Monthly garden ideas, gifts and coupons. A seasonal newsletter from Perennial Home & Gardens. Subscribe by sending your request to Perennial.'));
   const form=el('form','phg-newsletter-form'),label=el('label','','Email address'),input=el('input');input.type='email';input.name='email';input.required=true;input.autocomplete='email';input.id='phg-newsletter-email';label.htmlFor=input.id;label.append(input);
   const submit=action('Subscribe by email',()=>{});submit.type='submit';form.append(label,submit,el('small','','Opens your email app. Send the message to request a subscription.'));
   form.onsubmit=e=>{e.preventDefault();if(!form.reportValidity())return;location.href='mailto:perennialhomeandgardens@gmail.com?subject='+encodeURIComponent('Perennial Garden Magazine newsletter signup')+'&body='+encodeURIComponent('Please subscribe this address to Perennial Garden Magazine, the monthly newsletter with garden ideas, gifts and coupons. Email: '+input.value.trim());};
   d.append(form);d.showModal();
  }
  if(read('phg-b3-resource-offer')&&read('phg-b3-tool-offer'))clearInterval(tick);
 };
 const resume=()=>{clearInterval(tick);tick=setInterval(check,1000);};resume();
 addEventListener('pagehide',()=>clearInterval(tick));
 addEventListener('pageshow',e=>{if(e.persisted)resume();});
}

function init(){
 const body=document.body;body.dataset.siteSlug=cfg.slug;for(const [key,value] of Object.entries({high:cfg.high,mid:cfg.mid,low:cfg.low,ink:cfg.ink}))body.style.setProperty('--x-'+key,value);
 if(!document.querySelector('link[href*="site-experience.css"]')){const link=el('link');link.rel='stylesheet';link.href=asset('site-experience.css?v=20261021-organized');document.head.append(link);}
 function syncTheme(){const m=getComputedStyle(document.body).color.match(/[\d.]+/g)||[240,240,240];const light=cfg.slug!=='ie'&&(+m[0]*.2126 + +m[1]*.7152 + +m[2]*.0722)<145;body.style.setProperty('--x-panel',light?'#f1eee7':'#0c100f');body.style.setProperty('--x-text',light?'#262923':'#eee');}
 syncTheme();for(const n of [document.body,document.documentElement])new MutationObserver(syncTheme).observe(n,{attributes:true,attributeFilter:['class','data-theme']});
 gardenNavigation();gardenAssistant();addMenu();brandNative();genericPlayer();gardenRefinements();
 if(document.getElementById("ap")){const t=el("script");t.src=asset("tanya-assistant.js?v=20261021-organized");document.body.append(t);}
 // ETP creates its jukebox on demand, so apply the same branding when it appears.
 if(cfg.slug==='examine-the-past-home')new MutationObserver(()=>{if($('.etp-jukebox-card:not(.x-native-panel)'))brandNative();}).observe(document.body,{childList:true,subtree:true});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();

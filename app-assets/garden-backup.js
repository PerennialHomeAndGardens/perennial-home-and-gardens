/* Perennial garden backup v1. Local files only; no accounts or server transfers. */
(()=>{'use strict';
const exact={
 phgMyGardenProfileV1:'Garden profile', 'phg-growing-zone':'Growing zone', 'phg-cal-prefs':'Calendar preferences',
 phgGardenPlans:'Garden plans', phgGardenHealthReports:'Health reports', phgSeedSystemV1:'Seeds, trays & succession plans',
 phgGardenJournalV1:'Garden journal', phgHarvestRecordsV1:'Harvest records', phgGardenInventoryV1:'Inventory, shopping & budget',
 'phg-companion-saved':'Companion favorites', 'phg-harvest-saved':'Harvest favorites', 'phg-harvest-last':'Last harvest check',
 phgGardenLibraryShelfV1:'Library shelf',phgGardenLibrarySavedResources:'Library resources',phgGardenLibraryRecentSearches:'Library search history',
 phgGardenLibraryProfileV1:'Library profile',phgGardenLibraryPlantNotesV1:'Plant notes',phgGardenLibraryCollectionsV1:'Plant collections',
 phgGardenBooksV1:'Book notes & reading list','phg-reader:v1':'Reading preferences'};
const arrayKeys=new Set(['phgGardenPlans','phgGardenHealthReports','phg-companion-saved','phg-harvest-saved','phgGardenLibrarySavedResources','phgGardenLibraryRecentSearches']);
const lists={phgSeedSystemV1:['seeds','trays','successions'],phgGardenJournalV1:['entries'],phgHarvestRecordsV1:['records'],phgGardenInventoryV1:['inventory','shopping','purchases'],phgGardenLibraryShelfV1:['plants','terms','resources']};
const allowed=k=>Object.hasOwn(exact,k)||/^phg-cal-\d{1,2}[ab]-(mixed|veg|per|edible)-\d{1,2}$/.test(k)||/^phg-reader:v1:(journal|place):\/(articles|books)\/[a-z0-9-]+\.html$/.test(k);
const label=k=>exact[k]|| (k.startsWith('phg-cal-')?'Calendar checked tasks':k.includes(':journal:')?'Article journal':'Saved reading place');
const object=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
function walk(v,depth=0,field=''){
 if(depth>18)throw Error('This file contains data nested too deeply.');
 if(typeof v==='string'){if(v.length>200000)throw Error('A text entry is too large.');if((field==='id'||field.endsWith('Id'))&&!/^[\w.:-]{0,160}$/.test(v))throw Error('An entry has an invalid identifier.');return;}
 if(typeof v==='number'){if(!Number.isFinite(v))throw Error('A number is invalid.');return;}
 if(v===null||typeof v==='boolean')return;
 if(Array.isArray(v)){if(v.length>30000)throw Error('A collection is too large.');v.forEach(x=>walk(x,depth+1));return;}
 if(!object(v))throw Error('Unsupported backup value.');
 for(const [k,val] of Object.entries(v)){if(['__proto__','constructor','prototype'].includes(k))throw Error('Unsafe backup property.');walk(val,depth+1,k);}
}
function validateValue(k,v){
 walk(v);
 if(arrayKeys.has(k)&&!Array.isArray(v))throw Error(label(k)+' must contain a list.');
 if(Object.hasOwn(exact,k)&&!arrayKeys.has(k)&&!object(v))throw Error(label(k)+' must contain an object.');
 if(lists[k])for(const f of lists[k])if(!Array.isArray(v[f]))throw Error(label(k)+' is missing '+f+'.');
 const stringLists=['phg-companion-saved','phg-harvest-saved','phgGardenLibrarySavedResources','phgGardenLibraryRecentSearches'];
 if(stringLists.includes(k)&&v.some(x=>typeof x!=='string'))throw Error(label(k)+' contains an invalid list item.');
 if(k==='phgGardenLibraryShelfV1')for(const f of lists[k])if(v[f].some(x=>typeof x!=='string'))throw Error('Invalid Library shelf entry.');
 if(k.startsWith('phg-cal-')&&k!=='phg-cal-prefs'&&(!Array.isArray(v)||v.some(x=>typeof x!=='string')))throw Error('Invalid calendar checklist.');
 if(k.includes(':journal:')&&typeof v!=='string')throw Error('Invalid article journal.');
 if(k==='phgGardenBooksV1')for(const b of Object.values(v))if(!object(b)||('notes'in b&&typeof b.notes!=='string'))throw Error('Invalid book notes.');
 if(k==='phgSeedSystemV1'){
  for(const t of v.trays)if(!object(t)||!Array.isArray(t.cellStates)||!Number.isInteger(t.cells)||t.cells<1||t.cells>512||t.cellStates.length!==t.cells||t.cellStates.some(s=>!['planted','germ','failed','empty'].includes(s)))throw Error('Invalid seed tray cells.');
  for(const p of v.successions)if(!object(p)||!Array.isArray(p.rounds))throw Error('Invalid succession plan.');
 }
 // These fields are rendered as numbers by the existing tools. Never accept HTML or strings in them.
 const fail=msg=>{throw Error(label(k)+': '+msg);};
 const str=(o,f,required=false)=>{if(required&&typeof o[f]!=='string')fail('missing '+f);if(f in o&&typeof o[f]!=='string')fail(f+' must be text');};
 const num=(o,f,required=false,min=0)=>{if(required&&typeof o[f]!=='number')fail('missing numeric '+f);if(f in o&&o[f]!==null&&(typeof o[f]!=='number'||!Number.isFinite(o[f])||o[f]<min))fail('invalid '+f);};
 const date=(o,f,required=false)=>{str(o,f,required);if(o[f]&&!/^\d{4}-\d{2}-\d{2}$/.test(o[f]))fail('invalid '+f+' date');};
 const record=(o)=>{if(!object(o))fail('invalid record');if('id'in o&&!(typeof o.id==='number'&&Number.isFinite(o.id))&&!(typeof o.id==='string'&&/^[\w.:-]{1,160}$/.test(o.id)))fail('invalid record ID');};
 if(lists[k])for(const f of lists[k])if(k!=='phgGardenLibraryShelfV1')for(const o of v[f])record(o);
 if(k==='phgSeedSystemV1'){
  for(const o of v.seeds){str(o,'id',true);str(o,'crop',true);for(const f of ['variety','qty','notes','method','source'])str(o,f);num(o,'dtm');num(o,'spacing');if(o.year&&!/^\d{4}$/.test(String(o.year)))fail('invalid seed year');}
  for(const o of v.trays){str(o,'id',true);str(o,'seedId',true);str(o,'name',true);date(o,'sow',true);date(o,'transplant');num(o,'germDays',true);str(o,'stage');}
  for(const o of v.successions){str(o,'id',true);str(o,'seedId',true);num(o,'count',true);for(const r of o.rounds){record(r);num(r,'n',true);date(r,'sow',true);date(r,'harvest');str(r,'status',true);}}
 }
 if(k==='phgGardenJournalV1')for(const o of v.entries){str(o,'id',true);date(o,'date',true);for(const f of ['notes','target','type','location','time','followDate'])str(o,f);if('tags'in o&&(!Array.isArray(o.tags)||o.tags.some(x=>typeof x!=='string')))fail('invalid journal tags');}
 if(k==='phgHarvestRecordsV1')for(const o of v.records){str(o,'id',true);str(o,'crop',true);date(o,'date',true);for(const f of ['weight','count','days'])num(o,f);for(const f of ['variety','location','notes','weightUnit','countUnit','quality','use','storage'])str(o,f);}
 if(k==='phgGardenInventoryV1'){
  if(!object(v.budget))fail('missing budget');for(const f of ['total','plants','soil','tools','other'])num(v.budget,f);
  for(const o of v.inventory){str(o,'id',true);str(o,'name',true);num(o,'qty',true);num(o,'min',true);}
  for(const o of v.shopping){str(o,'id',true);str(o,'name',true);num(o,'qty',true);num(o,'targetPrice');}
  for(const o of v.purchases){str(o,'id',true);str(o,'item',true);date(o,'date',true);num(o,'cost',true);num(o,'qty',true);}
 }
 if(k==='phgGardenPlans')for(const p of v){record(p);str(p,'name',true);if(!object(p.garden)||!Array.isArray(p.garden.objects))fail('invalid garden layout');num(p.garden,'w',true,.01);num(p.garden,'h',true,.01);const ids=new Set();for(const o of p.garden.objects){record(o);str(o,'id',true);str(o,'name',true);str(o,'type',true);for(const f of ['x','y','rot'])num(o,f,true,-100000);num(o,'w',true,.01);num(o,'h',true,.01);if(ids.has(o.id))fail('duplicate layout object IDs');ids.add(o.id);}}
 if(k==='phgGardenHealthReports')for(const o of v){record(o);str(o,'plant',true);str(o,'date',true);for(const f of ['matches','symptoms','conditions','areas','photoTypes'])if(f in o&&(!Array.isArray(o[f])||o[f].some(x=>typeof x!=='string')))fail('invalid health report '+f);}
 if(k==='phg-cal-prefs'){if(!Number.isInteger(v.month)||v.month<0||v.month>11||!['mixed','veg','per','edible'].includes(v.focus))fail('invalid calendar preference');}
 if(k==='phgGardenLibraryPlantNotesV1')for(const n of Object.values(v))if(typeof n!=='string')fail('invalid plant note');

}
function snapshot(){const entries={};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(!allowed(k))continue;const raw=localStorage.getItem(k);try{entries[k]=JSON.parse(raw);}catch{throw Error(label(k)+' contains unreadable saved data. Nothing was changed.');}}return{format:'perennial-garden-backup',version:1,createdAt:new Date().toISOString(),entries};}
function saveFile(payload,name='Perennial-Garden-Backup'){
 const a=document.createElement('a'),u=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));a.href=u;a.download=name+'-'+new Date().toISOString().slice(0,10)+'.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),2000);
}
function legacy(p){
 if(object(p)&&p.version===2&&object(p.garden)&&!p.format)return {format:'perennial-garden-backup',version:1,entries:{phgGardenPlans:[{id:Date.now(),name:'Imported garden plan',date:p.exportedAt||new Date().toISOString(),version:2,garden:p.garden,settings:p.settings||{}}]}};
 if(object(p)&&object(p.books)&&!p.format)return {format:'perennial-garden-backup',version:1,entries:{phgGardenBooksV1:p.books}};
 if(object(p)&&Array.isArray(p.entries)&&!p.format)return {format:'perennial-garden-backup',version:1,entries:{phgGardenJournalV1:{entries:p.entries}}};
 if(object(p)&&Array.isArray(p.records)&&!p.format)return {format:'perennial-garden-backup',version:1,entries:{phgHarvestRecordsV1:{records:p.records}}};
 if(object(p)&&Array.isArray(p.inventory)&&Array.isArray(p.shopping)&&Array.isArray(p.purchases)&&!p.format)return {format:'perennial-garden-backup',version:1,entries:{phgGardenInventoryV1:{inventory:p.inventory,shopping:p.shopping,purchases:p.purchases,budget:p.budget||{}}}};
 if(object(p)&&p.version===1&&p.profile&&p.plantNotes&&!p.format)return{format:'perennial-garden-backup',version:1,entries:{phgGardenLibraryProfileV1:p.profile,phgGardenLibraryPlantNotesV1:p.plantNotes,phgGardenLibraryCollectionsV1:p.collections||{favorites:[]}}};
 return p;
}
function parse(text){let p;try{p=legacy(JSON.parse(text));}catch{throw Error('This is not a readable JSON backup.');}
 if(!object(p)||p.format!=='perennial-garden-backup'||p.version!==1||!object(p.entries))throw Error('Choose a Perennial Garden Backup (version 1) or a supported older tool export.');
 const keys=Object.keys(p.entries);if(!keys.length||keys.length>1000)throw Error('The backup is empty or contains too many sections.');
 for(const k of keys){if(!allowed(k))throw Error('The file contains an unsupported section: '+k);validateValue(k,p.entries[k]);}return p;
}
function restore(p,replace){p=parse(JSON.stringify(p));const changes=Object.entries(p.entries).filter(([k])=>replace||localStorage.getItem(k)===null);if(!changes.length)throw Error('All these sections already exist. Choose Replace included sections if you want to replace them.');
 const before=new Map(changes.map(([k])=>[k,localStorage.getItem(k)]));try{for(const[k,v]of changes)localStorage.setItem(k,JSON.stringify(v));}catch{let restored=true;for(const[k,v]of before)try{v===null?localStorage.removeItem(k):localStorage.setItem(k,v);}catch{restored=false;}throw Error(restored?'Storage is full or unavailable. The original data was restored.':'Storage failed. Keep this page open and download the safety copy before retrying.');}return changes.length;
}
const el=(tag,text,cls)=>{const e=document.createElement(tag);if(text)e.textContent=text;if(cls)e.className=cls;return e;};
const css=el('style');css.textContent=`.phg-backup-launch{margin:18px 0;padding:12px 15px;border:1px solid #a3ac94;border-radius:12px;background:#f4f0e8;color:#294f30;font:700 15px Georgia,serif;cursor:pointer}.phg-backup-dialog{width:min(520px,calc(100vw - 24px));max-height:85dvh;box-sizing:border-box;overflow:auto;border:0;border-radius:18px;padding:22px;background:#fffaf2;color:#31271f;font:16px/1.5 Georgia,serif}.phg-backup-dialog::backdrop{background:#160f09b8}.phg-backup-dialog h2{font-size:24px;margin:0 0 12px}.phg-backup-dialog button,.phg-backup-dialog input,.phg-backup-dialog select{font:inherit;box-sizing:border-box;max-width:100%}.phg-backup-dialog button{padding:10px 14px;border:1px solid #a3ac94;border-radius:10px;cursor:pointer;background:#294f30;color:white;min-height:44px}.phg-backup-dialog button:disabled{opacity:.5;cursor:default}.phg-backup-dialog label{display:block;margin:13px 0}.phg-backup-dialog input[type=file]{width:100%}.phg-backup-dialog select{padding:8px;width:100%}.phg-backup-preview{max-height:170px;overflow:auto;background:#eee8dc;padding:10px;border-radius:10px}.phg-backup-actions{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}.phg-backup-status{white-space:pre-wrap;margin-top:12px}@media print{.phg-backup-launch,.phg-backup-dialog{display:none!important}}`;document.head.append(css);
const main=document.querySelector('main');if(!main)return;const launch=el('button','Backup & Restore My Garden','phg-backup-launch');launch.type='button';launch.id='phgBackupOpen';main.append(launch);
let d,pending,safety;
launch.onclick=()=>{
 if(d){d.showModal();return;}d=el('dialog',null,'phg-backup-dialog');d.id='phgBackupDialog';d.setAttribute('aria-labelledby','phgBackupTitle');const h=el('h2','Keep a copy of your garden');h.id='phgBackupTitle';d.append(h,el('p','One backup includes saved data from all garden tools, Library shelves and book notes in this browser. Photo files and unsaved work are not included.'));
 const status=el('p','','phg-backup-status');status.id='phgBackupStatus';status.setAttribute('role','status');
 const exportBtn=el('button','Download garden backup');exportBtn.id='phgBackupExport';exportBtn.onclick=()=>{try{const s=snapshot();saveFile(s);status.textContent=Object.keys(s.entries).length+' saved sections downloaded. Keep this file private. To move devices, open this site there and restore this file.';}catch(e){status.textContent=e.message;}};d.append(exportBtn);
 const lab=el('label','Restore from a backup file');const file=el('input');file.type='file';file.accept='.json,application/json';file.id='phgBackupFile';lab.append(file);d.append(lab);
 const preview=el('div','','phg-backup-preview');preview.id='phgBackupPreview';preview.hidden=true;d.append(preview);
 const modeLabel=el('label','How should this file be restored?'),select=el('select');select.id='phgBackupMode';for(const[value,title]of [['missing','Add missing sections only — keep existing data'],['replace','Replace included sections — use backup values']]){const o=el('option',title);o.value=value;select.append(o);}modeLabel.append(select);d.append(modeLabel);
 const confirmLabel=el('label'),check=el('input');check.type='checkbox';check.id='phgBackupConfirm';confirmLabel.append(check,document.createTextNode(' I reviewed this backup and want to restore these sections.'));d.append(confirmLabel);
 const actions=el('div',null,'phg-backup-actions'),apply=el('button','Restore reviewed backup'),reload=el('button','Reload tools'),close=el('button','Close');apply.id='phgBackupApply';apply.disabled=true;reload.id='phgBackupReload';reload.hidden=true;reload.onclick=()=>location.reload();close.onclick=()=>{d.close();launch.focus();};actions.append(apply,reload,close);d.append(actions,status);document.body.append(d);
 let fileToken=0;file.onchange=async()=>{const token=++fileToken;pending=null;apply.disabled=true;check.checked=false;preview.replaceChildren();preview.hidden=true;const f=file.files[0];if(!f)return;try{if(!f.size||f.size>10*1024*1024)throw Error('Choose a non-empty backup smaller than 10 MB.');const text=await f.text();if(token!==fileToken)return;pending=parse(text);for(const[k,v]of Object.entries(pending.entries)){const count=Array.isArray(v)?v.length:object(v)?Object.keys(v).length:1;preview.append(el('div',label(k)+' · '+count+' items/fields'+(localStorage.getItem(k)!==null?' · already saved here':'')));}preview.hidden=false;status.textContent='File checked. Review the sections and restore option. Nothing has changed yet.';}catch(e){if(token===fileToken)status.textContent=e.message;}};
 check.onchange=()=>apply.disabled=!pending||!check.checked;
 apply.onclick=()=>{if(!pending||!check.checked)return;try{safety=snapshot();saveFile(safety,'Perennial-Before-Restore');const n=restore(pending,select.value==='replace');apply.disabled=true;check.checked=false;pending=null;file.value='';reload.hidden=false;status.textContent=n+' sections restored. A safety backup was downloaded first. Reload tools to display the restored data.';}catch(e){status.textContent=e.message;}};
 d.showModal();
};
// A small, stable contract for our own regression tests and future tool integrations.
window.PHGGardenBackup=Object.freeze({snapshot,parse,restore,allowed});
})();

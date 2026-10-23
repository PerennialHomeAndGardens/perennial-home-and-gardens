/* Fault injection: an interrupted restore must not leave a partially restored garden. */
const vm=require('vm'),fs=require('fs'),assert=require('node:assert/strict');
class Store{constructor(){this.m=new Map()}get length(){return this.m.size}key(i){return [...this.m.keys()][i]}getItem(k){return this.m.get(k)??null}setItem(k,v){this.m.set(k,String(v))}removeItem(k){this.m.delete(k)}}
const make=()=>({append(){},setAttribute(){},className:'',textContent:''}),storage=new Store(),c={window:{},document:{createElement:make,head:make(),querySelector:make},localStorage:storage,console};vm.createContext(c);vm.runInContext(fs.readFileSync('app-assets/garden-backup.js','utf8'),c);const api=c.window.PHGGardenBackup;
const payload={format:'perennial-garden-backup',version:1,entries:{phgMyGardenProfileV1:{gardenName:'Before',zone:'7b',location:''}}};api.restore(payload,false);assert.equal(JSON.parse(storage.getItem('phgMyGardenProfileV1')).gardenName,'Before');
const bad=[JSON.stringify({...payload,version:2}),'{"format":"perennial-garden-backup","version":1,"entries":{"__proto__":{}}}',JSON.stringify({format:'perennial-garden-backup',version:1,entries:{phgSeedSystemV1:{seeds:[],trays:[{cells:8,cellStates:[]}],successions:[]}}})];for(const x of bad)assert.throws(()=>api.parse(x));assert(api.allowed('phg-cal-7b-per-9'));assert(!api.allowed('phg_freebie_lead'));
const before=storage.getItem('phgMyGardenProfileV1'),original=storage.setItem.bind(storage);let calls=0;storage.setItem=(k,v)=>{if(++calls===2)throw Error('quota');original(k,v)};
assert.throws(()=>api.restore({format:'perennial-garden-backup',version:1,entries:{phgMyGardenProfileV1:{gardenName:'After'},phgGardenBooksV1:{}}},true));assert.equal(storage.getItem('phgMyGardenProfileV1'),before);assert.equal(storage.getItem('phgGardenBooksV1'),null);
console.log('PASS backup invalid formats, key scope, restore and partial-write rollback');
const wrap=entries=>({format:'perennial-garden-backup',version:1,entries});
for(const input of [
 {version:1,exportedAt:'2026-10-22',entries:[]},
 {version:1,records:[]},
 {exported:'2026-10-22',books:{'test-book':{notes:'Remember this',saved:true}}},
 {version:1,inventory:[],shopping:[],purchases:[],budget:{}},
 {version:1,profile:{},plantNotes:{},collections:{favorites:[]}},
 {version:2,garden:{w:40,h:30,objects:[]},settings:{}}
])assert.equal(api.parse(JSON.stringify(input)).format,'perennial-garden-backup');
assert.throws(()=>api.parse(JSON.stringify(wrap({phgGardenJournalV1:{entries:[{id:'ok',date:'2026-99-99'}]}}))));
assert.throws(()=>api.parse(JSON.stringify(wrap({phgGardenInventoryV1:{inventory:[],shopping:[{id:'ok',name:'Test',qty:1,targetPrice:'25'}],purchases:[],budget:{}}}))));
console.log('PASS all supported older exports; impossible dates and string prices rejected');

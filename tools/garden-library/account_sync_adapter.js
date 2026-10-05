// Perennial Garden Library — Phase 9 account-sync adapter
// Local-first today; designed so a Supabase-backed provider can replace local storage
// without changing the Garden Library UI contract.
(function(global){
  const STATE_KEY="phgGardenLibraryAccountStateV1";
  const PROFILE_KEY="phgGardenLibraryProfileV1";
  const NOTES_KEY="phgGardenLibraryPlantNotesV1";
  const COLLECTIONS_KEY="phgGardenLibraryCollectionsV1";

  function read(key,fallback){
    try{return {...fallback,...JSON.parse(localStorage.getItem(key)||"{}")}}catch(e){return {...fallback}}
  }
  function write(key,value){localStorage.setItem(key,JSON.stringify(value));}
  const api={
    mode:"local",
    getState(){return read(STATE_KEY,{provider:"local",signedIn:false,lastSync:null,status:"Saved on this device"});},
    getProfile(){return read(PROFILE_KEY,{displayName:"",homeZone:"",locationLabel:""});},
    saveProfile(p){write(PROFILE_KEY,p);return p;},
    getPlantNotes(){return read(NOTES_KEY,{});},
    savePlantNote(plantId,note){
      const n=this.getPlantNotes(); if(note)n[plantId]=note; else delete n[plantId]; write(NOTES_KEY,n); return n;
    },
    getCollections(){return read(COLLECTIONS_KEY,{favorites:[]});},
    saveCollections(c){write(COLLECTIONS_KEY,c);return c;},
    addPlantToCollection(plantId,name="favorites"){
      const c=this.getCollections(); c[name]=Array.isArray(c[name])?c[name]:[]; if(!c[name].includes(plantId))c[name].push(plantId);write(COLLECTIONS_KEY,c);return c;
    },
    removePlantFromCollection(plantId,name="favorites"){
      const c=this.getCollections(); c[name]=(c[name]||[]).filter(x=>x!==plantId);write(COLLECTIONS_KEY,c);return c;
    },
    async sync(){
      // Intentionally local-only until a Perennial Supabase project is connected.
      const s=this.getState();s.lastSync=new Date().toISOString();s.status="Local save refreshed";write(STATE_KEY,s);return s;
    },
    exportLocal(){
      return {
        version:1,
        exportedAt:new Date().toISOString(),
        profile:this.getProfile(),
        plantNotes:this.getPlantNotes(),
        collections:this.getCollections(),
        accountState:this.getState()
      };
    },
    importLocal(payload){
      if(payload.profile)write(PROFILE_KEY,payload.profile);
      if(payload.plantNotes)write(NOTES_KEY,payload.plantNotes);
      if(payload.collections)write(COLLECTIONS_KEY,payload.collections);
      return true;
    }
  };
  global.PerennialLibrarySync=api;
})(window);

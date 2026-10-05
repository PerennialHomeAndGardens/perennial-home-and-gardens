import json,re,urllib.request,time
from pathlib import Path
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT=Path(".")
PROFILES=ROOT/"tools/garden-library/plant_profiles.json"
CARE_OUT=ROOT/"tools/garden-library/plant_care_enrichment.json"
SUMMARY_OUT=ROOT/"tools/garden-library/plant_care_enrichment_summary.json"
INDEX=ROOT/"tools/garden-library/index.html"
profiles=json.loads(PROFILES.read_text(encoding="utf-8"))
UA="PerennialHomeAndGardens/1.0 (+https://perennialhomeandgardens.github.io/)"

def fetch(url,timeout=35):
    req=urllib.request.Request(url,headers={"User-Agent":UA,"Accept":"text/html,application/xhtml+xml,application/xml"})
    with urllib.request.urlopen(req,timeout=timeout) as r:
        return r.read().decode("utf-8","replace")

def slugify(name):
    s=(name or "").strip().replace("×"," x ")
    s=re.sub(r"\bsubsp\.\s*","subsp ",s,flags=re.I)
    s=re.sub(r"\bssp\.\s*","subsp ",s,flags=re.I)
    s=re.sub(r"\bvar\.\s*","var ",s,flags=re.I)
    s=re.sub(r"\bf\.\s*","f ",s,flags=re.I)
    s=s.lower()
    return re.sub(r"[^a-z0-9]+","-",s).strip("-")

print("Downloading NC State Extension Gardener Plant Toolbox sitemap...")
sitemap=fetch("https://plants.ces.ncsu.edu/sitemap.xml",60)
urls=re.findall(r"<loc>(https://plants\.ces\.ncsu\.edu/plants/[^<]+/)</loc>",sitemap)
slug_to_url={u.rstrip("/").split("/")[-1]:u for u in urls}
print("NCSU plant URLs:",len(slug_to_url))

matches={}
for p in profiles:
    names=[p.get("scientificName","")]+list(p.get("synonyms") or [])+list(p.get("historicalNames") or [])
    for name in names:
        sl=slugify(name)
        if sl in slug_to_url:
            matches[p["id"]]=slug_to_url[sl]
            break
print("Exact Perennial to NCSU profile matches:",len(matches))

wanted=[
    "USDA Plant Hardiness Zone","Light","Soil Texture","Soil pH","Soil Drainage",
    "Available Space To Plant","Recommended Propagation Strategy","Country Or Region Of Origin",
    "Life Cycle","Wildlife Value","Play Value","Particularly Resistant To (Insects/Diseases/Other Problems)",
    "Dimensions","Fire Risk Rating","Flower Color","Flower Bloom Time","Flower Value To Gardener",
    "Landscape Location","Landscape Theme","Design Feature","Attracts","Resistance To Challenges",
    "Problems","Poison Severity","Plant Habit","Growth Rate","Maintenance","NC Region"
]
wanted_l={x.lower():x for x in wanted}

def parse_dl(soup):
    data={}
    for dt in soup.find_all("dt"):
        label=dt.get_text(" ",strip=True).rstrip(":").strip()
        canon=wanted_l.get(label.lower())
        if not canon:
            continue
        vals=[]
        node=dt.find_next_sibling()
        while node is not None and getattr(node,"name",None)!="dt":
            if getattr(node,"name",None)=="dd":
                val=re.sub(r"\s+"," ",node.get_text(" ",strip=True)).strip()
                if val and val not in vals:
                    vals.append(val)
            node=node.find_next_sibling()
        if vals:
            data[canon]=vals
    return data

def one(pid,url):
    last=None
    for attempt in range(3):
        try:
            soup=BeautifulSoup(fetch(url),"html.parser")
            d=parse_dl(soup)
            return pid,{
                "source":"North Carolina Extension Gardener Plant Toolbox",
                "sourceUrl":url,
                "retrieved":"2026-10-05",
                "usdaHardinessZones":d.get("USDA Plant Hardiness Zone",[]),
                "light":d.get("Light",[]),
                "soilTexture":d.get("Soil Texture",[]),
                "soilPH":d.get("Soil pH",[]),
                "soilDrainage":d.get("Soil Drainage",[]),
                "availableSpace":d.get("Available Space To Plant",[]),
                "propagation":d.get("Recommended Propagation Strategy",[]),
                "origin":d.get("Country Or Region Of Origin",[]),
                "lifeCycle":d.get("Life Cycle",[]),
                "wildlifeValue":d.get("Wildlife Value",[]),
                "playValue":d.get("Play Value",[]),
                "resistantTo":d.get("Particularly Resistant To (Insects/Diseases/Other Problems)",[]),
                "dimensions":d.get("Dimensions",[]),
                "fireRisk":d.get("Fire Risk Rating",[]),
                "flowerColor":d.get("Flower Color",[]),
                "flowerBloomTime":d.get("Flower Bloom Time",[]),
                "flowerValue":d.get("Flower Value To Gardener",[]),
                "landscapeLocation":d.get("Landscape Location",[]),
                "landscapeTheme":d.get("Landscape Theme",[]),
                "designFeature":d.get("Design Feature",[]),
                "attracts":d.get("Attracts",[]),
                "resistanceChallenges":d.get("Resistance To Challenges",[]),
                "problems":d.get("Problems",[]),
                "poisonSeverity":d.get("Poison Severity",[]),
                "plantHabit":d.get("Plant Habit",[]),
                "growthRate":d.get("Growth Rate",[]),
                "maintenance":d.get("Maintenance",[]),
                "ncRegion":d.get("NC Region",[])
            }
        except Exception as e:
            last=e
            time.sleep(0.7*(attempt+1))
    raise last

care={}
failures=[]
with ThreadPoolExecutor(max_workers=7) as pool:
    futs={pool.submit(one,pid,url):pid for pid,url in matches.items()}
    done=0
    for fut in as_completed(futs):
        pid=futs[fut]
        try:
            k,v=fut.result()
            care[k]=v
        except Exception as e:
            failures.append({"id":pid,"error":repr(e)})
        done+=1
        if done%100==0:
            print("Fetched",done,"/",len(futs))

CARE_OUT.write_text(json.dumps(care,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
fields=[
    "usdaHardinessZones","light","soilTexture","soilPH","soilDrainage","availableSpace",
    "propagation","origin","lifeCycle","wildlifeValue","resistantTo","dimensions","fireRisk",
    "flowerColor","flowerBloomTime","flowerValue","landscapeLocation","landscapeTheme",
    "designFeature","attracts","resistanceChallenges","problems","poisonSeverity",
    "growthRate","maintenance"
]
coverage={f:sum(1 for x in care.values() if x.get(f)) for f in fields}
summary={
    "totalPlantProfiles":len(profiles),
    "ncsuPlantPagesInSitemap":len(slug_to_url),
    "exactMatchedProfiles":len(matches),
    "successfullyEnriched":len(care),
    "failedRequests":len(failures),
    "fieldCoverage":coverage,
    "source":"North Carolina Extension Gardener Plant Toolbox",
    "sourceHome":"https://plants.ces.ncsu.edu/",
    "method":"Exact scientific-name or verified-synonym slug match only. Structured factual fields were extracted from Plant Toolbox profile labels; unmatched plants were left blank.",
    "failures":failures[:50]
}
SUMMARY_OUT.write_text(json.dumps(summary,indent=2),encoding="utf-8")
print(json.dumps(summary,indent=2))

# ---- UI upgrade ----
h=INDEX.read_text(encoding="utf-8",errors="ignore")
marker="phg-phase5-care-v1"
if marker not in h:
    css=r"""
<style id="phg-phase5-care-v1">
.phg-care-title{margin:20px 0 10px;padding-top:16px;border-top:1px solid #cbd8c3;color:#29492e;font:500 24px Georgia,serif}
.phg-care-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:9px}.phg-care-card{background:#fffdf8;border:1px solid #dcd4c8;border-radius:14px;padding:12px}
.phg-care-card small{display:block;text-transform:uppercase;letter-spacing:.08em;color:#75806f;font-size:9px;font-weight:bold;margin-bottom:5px}.phg-care-card strong{display:block;color:#2e5032;font-size:14px;line-height:1.4}.phg-care-card span{display:block;color:#70665d;font-size:11px;line-height:1.42;margin-top:4px}
.phg-trusted{display:flex;gap:7px;flex-wrap:wrap;margin-top:12px}.phg-trusted a{display:inline-block;text-decoration:none;background:#315936;color:#fff;border-radius:999px;padding:8px 10px;font-size:11px;font-weight:bold}.phg-trusted a.secondary{background:#fffaf2;color:#35543a;border:1px solid #bfd0b8}
.phg-care-note{margin-top:10px;font-size:11px;color:#746960;line-height:1.45}.phg-safety{background:#fff8ea;border:1px solid #e6d4ae;border-radius:13px;padding:10px 12px;margin-top:10px;color:#68583f;font-size:12px;line-height:1.45}
@media(max-width:600px){.phg-care-grid{grid-template-columns:1fr}}
</style>
"""
    h=h.replace("</head>",css+"</head>",1)
    target='<div id="phgSourceBox" class="phg-sourcebox" style="display:none"></div>'
    addition=target+r"""
<div id="phgCareSection">
  <h3 class="phg-care-title">Garden Use, Ecology &amp; Trusted Resources</h3>
  <div id="phgCareGrid" class="phg-care-grid"></div>
  <div id="phgSafetyBox" class="phg-safety" style="display:none"></div>
  <div id="phgTrusted" class="phg-trusted"></div>
  <div id="phgCareNote" class="phg-care-note"></div>
</div>
"""
    if target not in h:
        raise SystemExit("Phase 4 source box not found")
    h=h.replace(target,addition,1)
    h=h.replace('let P=[],E={},page=0,current=null;const PAGE=24;','let P=[],E={},C={},page=0,current=null;const PAGE=24;',1)

    needle='  function openProfile(x){'
    helper=r"""
  function careCard(label,vals,note){
    vals=Array.isArray(vals)?vals:(vals?[vals]:[]);
    if(!vals.length)return "";
    const value=vals.join(" · ");
    return '<div class="phg-care-card"><small>'+label+'</small><strong>'+value+'</strong>'+(note?'<span>'+note+'</span>':'')+'</div>';
  }
  function renderCare(x){
    const c=C[x.id]||{};
    const e=E[x.id]||{};
    const grid=$("phgCareGrid"),trusted=$("phgTrusted"),note=$("phgCareNote"),safety=$("phgSafetyBox");
    let cards=[];
    cards.push(careCard("Published hardiness zones",c.usdaHardinessZones,"From NC State Extension Plant Toolbox"));
    cards.push(careCard("Light",c.light));
    cards.push(careCard("Soil texture",c.soilTexture));
    cards.push(careCard("Soil drainage",c.soilDrainage));
    cards.push(careCard("Soil pH",c.soilPH));
    cards.push(careCard("Propagation",c.propagation));
    cards.push(careCard("Landscape uses",c.landscapeLocation));
    cards.push(careCard("Garden themes",c.landscapeTheme));
    cards.push(careCard("Design features",c.designFeature));
    cards.push(careCard("Attracts",c.attracts));
    cards.push(careCard("Wildlife value",c.wildlifeValue));
    cards.push(careCard("Resists / tolerates",(c.resistanceChallenges||[]).length?c.resistanceChallenges:c.resistantTo));
    cards.push(careCard("Flower value",c.flowerValue));
    cards.push(careCard("Origin",c.origin));
    cards.push(careCard("Maintenance",c.maintenance));
    cards=cards.filter(Boolean);
    grid.innerHTML=cards.join("") || '<div class="phg-enrichment-missing">No exact NC State Extension care profile is available for this plant yet. Existing USDA NRCS data above remains available where matched.</div>';
    let hazards=[...(c.problems||[])];
    if(c.poisonSeverity&&c.poisonSeverity.length)hazards.push("Poison severity: "+c.poisonSeverity.join(", "));
    if(hazards.length){
      safety.style.display="block";
      safety.innerHTML="<strong>Safety / problem flags:</strong> "+hazards.join(" · ")+"<br><span>Use these as reference flags, not as medical or veterinary advice. Verify edibility or toxicity with an appropriate authoritative source before ingestion or exposure decisions.</span>";
    }else safety.style.display="none";
    trusted.innerHTML="";
    function add(label,url,secondary){
      if(!url)return;
      let a=document.createElement("a");a.textContent=label+" →";a.href=url;a.target="_blank";a.rel="noopener";if(secondary)a.className="secondary";trusted.appendChild(a);
    }
    add("NC State Extension",c.sourceUrl,false);
    add("USDA PLANTS",e.usdaProfileUrl,true);
    if(x.wfoIds&&x.wfoIds.length)add("World Flora Online","https://wfoplantlist.org/plant-list/taxon/"+encodeURIComponent(x.wfoIds[0]),true);
    add("Biodiversity Heritage Library","https://www.biodiversitylibrary.org/search?searchTerm="+encodeURIComponent(x.scientificName)+"&searchCat=scientific_names",true);
    note.textContent=c.sourceUrl
      ?"Additional care fields are sourced from the North Carolina Extension Gardener Plant Toolbox. Plant performance varies by climate, cultivar, soil and local conditions."
      :"This profile does not yet have an exact NC State Extension care match. Trusted taxonomy and USDA NRCS data remain available above where present.";
  }
"""
    if needle not in h:
        raise SystemExit("Plant profile function not found")
    h=h.replace(needle,helper+needle,1)
    h=h.replace('    renderEnrichment(x);\n    loadImage(x);','    renderEnrichment(x);\n    renderCare(x);\n    loadImage(x);',1)

    old='''  Promise.all([
    fetch("plant_profiles.json",{cache:"no-store"}).then(r=>r.json()),
    fetch("plant_enrichment.json",{cache:"no-store"}).then(r=>r.json()).catch(()=>({}))
  ]).then(([data,enrichment])=>{
    P=data;E=enrichment||{};
    $("termBadge").textContent=(P.length+(window.DATA?.length||0)).toLocaleString()+" library records";
    render();
    let h=decodeURIComponent(location.hash.replace("#",""));
    if(h.startsWith("plant-")){let x=P.find(p=>"plant-"+p.id===h);if(x)openProfile(x)}
  }).catch(()=>{$("phgPlantCount").textContent="Plant profile database is temporarily unavailable."});'''
    new='''  Promise.all([
    fetch("plant_profiles.json",{cache:"no-store"}).then(r=>r.json()),
    fetch("plant_enrichment.json",{cache:"no-store"}).then(r=>r.json()).catch(()=>({})),
    fetch("plant_care_enrichment.json",{cache:"no-store"}).then(r=>r.json()).catch(()=>({}))
  ]).then(([data,enrichment,care])=>{
    P=data;E=enrichment||{};C=care||{};
    $("termBadge").textContent=(P.length+(window.DATA?.length||0)).toLocaleString()+" library records";
    render();
    let h=decodeURIComponent(location.hash.replace("#",""));
    if(h.startsWith("plant-")){let x=P.find(p=>"plant-"+p.id===h);if(x)openProfile(x)}
  }).catch(()=>{$("phgPlantCount").textContent="Plant profile database is temporarily unavailable."});'''
    if old not in h:
        raise SystemExit("Phase 4 Promise.all block not found")
    h=h.replace(old,new,1)
    INDEX.write_text(h,encoding="utf-8")
else:
    print("Phase 5 UI already installed; refreshed data only.")

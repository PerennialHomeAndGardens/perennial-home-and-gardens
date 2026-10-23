"""Fetch pinned, licensed model/runtime assets and verify every byte before publishing."""
from pathlib import Path
import json,hashlib,urllib.request,concurrent.futures
R=Path(__file__).resolve().parents[2]
manifest=json.loads((R/'app-assets/plant-vision/assets-manifest.json').read_text())
def fetch(a):
 p=R/a['path'];p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256']:return
 data=urllib.request.urlopen(a['url'],timeout=90).read()
 if len(data)!=a['bytes'] or hashlib.sha256(data).hexdigest()!=a['sha256']:raise ValueError('Asset integrity mismatch: '+a['path'])
 p.write_bytes(data);print('Verified',a['path'],len(data),flush=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=4)as pool:list(pool.map(fetch,manifest))

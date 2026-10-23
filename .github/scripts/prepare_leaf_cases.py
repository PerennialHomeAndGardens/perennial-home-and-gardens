"""Deterministic external PlantDoc test samples; images never enter the published repository."""
import urllib.request,urllib.parse,json,hashlib,concurrent.futures
from pathlib import Path
from PIL import Image,ImageOps
from io import BytesIO
R=Path(__file__).resolve().parents[2];repo='pratikkayal/PlantDoc-Dataset';rev='5467f6012d78d1c446145d5f582da6096f852ae8'
mapping={'Apple Scab Leaf':0,'Apple leaf':3,'Apple rust leaf':2,'Bell_pepper leaf spot':18,'Bell_pepper leaf':19,'Cherry leaf':6,'Corn Gray leaf spot':7,'Corn leaf blight':9,'Corn rust leaf':8,'Peach leaf':17,'Potato leaf early blight':20,'Potato leaf late blight':21,'Strawberry leaf':27,'Tomato Early blight leaf':29,'Tomato Septoria leaf spot':32,'Tomato leaf bacterial spot':28,'Tomato leaf late blight':30,'Tomato leaf mosaic virus':36,'Tomato leaf yellow virus':35,'Tomato leaf':37,'Tomato mold leaf':31,'grape leaf black rot':11,'grape leaf':14}
tree=json.load(urllib.request.urlopen('https://api.github.com/repos/'+repo+'/git/trees/'+rev+'?recursive=1',timeout=60))['tree']
choices=[]
for group,index in mapping.items():
 files=sorted(x['path'] for x in tree if x['type']=='blob' and x['path'].startswith('test/'+group+'/'))[:2]
 for path in files:choices.append((group,index,path))
folder=R/'.qa-leaf-cases';folder.mkdir(exist_ok=True)
def get(entry):
 group,index,path=entry;url='https://raw.githubusercontent.com/'+repo+'/'+rev+'/'+urllib.parse.quote(path,safe='/')
 raw=urllib.request.urlopen(url,timeout=60).read();name=hashlib.sha256(path.encode()).hexdigest()[:18]+'.png';image=ImageOps.exif_transpose(Image.open(BytesIO(raw))).convert('RGB');image.thumbnail((1200,1200));image.save(folder/name)
 return {'group':group,'expectedIndex':index,'sourceUrl':url,'sourceSha256':hashlib.sha256(raw).hexdigest(),'fixtureUrl':'/.qa-leaf-cases/'+name}
with concurrent.futures.ThreadPoolExecutor(max_workers=5)as pool:cases=list(pool.map(get,choices))
(folder/'cases.json').write_text(json.dumps({'dataset':repo,'revision':rev,'method':'First two lexicographically sorted test files per mapped class; no selection based on predictions. Crop supplied from the dataset label. This small sample is not a deployment-wide accuracy guarantee.','cases':cases},indent=2));print('Prepared',len(cases),'external labeled cases',flush=True)

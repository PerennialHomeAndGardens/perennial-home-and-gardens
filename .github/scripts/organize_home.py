"""Retain homepage content while organizing twelve tools and the closing sections."""
from pathlib import Path
import json
from bs4 import BeautifulSoup as Soup
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'index.html';d=Soup(p.read_text(),'html.parser');main=d.main
cards=d.select_one('#tools .creamToolGrid')
new=[('seed-starting','◌','Seed Starting & Tray Tracker','Organize seeds, trays, germination, transplant dates and succession sowings.'),('garden-journal','▤','Garden Journal & Logs','Record watering, feeding, observations, treatments and follow-up tasks.'),('harvest-records','▥','Harvest & Garden Records','Track yields, crop quality, storage and production across the season.'),('garden-inventory','▣','Inventory, Shopping & Budget','Keep supplies, shopping lists, purchases and garden spending organized.')]
for slug,icon,title,desc in new:
 if not cards.select_one('a[href="/tools/'+slug+'/"]'):
  cards.append(Soup('<a class="card creamTool pad" href="/tools/'+slug+'/"><div class="toolTitleRow"><span class="toolMiniIcon" aria-hidden="true">'+icon+'</span><h3>'+title+'</h3></div><p>'+desc+'</p></a>','html.parser'))
for old in d.select('.phg-dashboard-link'):old.decompose()
head=d.select_one('#tools .head')
for old in head.select(':scope > p,.phg-tools-start'):old.decompose()
head.append(Soup('<div class="phg-tools-start"><p>Explore planning tools designed to help you understand your space, make confident garden decisions and move from idea to action. Start with My Garden to save your garden profile and bring your saved plans, plants and records together.</p><a class="phg-app-open phg-garden-start" href="/tools/my-garden/">Open My Garden →</a><small>No account needed. Saved in this browser.</small></div>','html.parser'))
# Keep the newer, accurate advertisements; preserve their old bookmark anchors.
for old,new_id in [('tool-map','garden-planner'),('tool-identifier','plant-identifier')]:
 old_section=d.select_one('section#'+old)
 if old_section:old_section.decompose()
 if not d.select_one('#'+old):
  anchor=d.new_tag('span',id=old);anchor['class']='phg-section-anchor';anchor['aria-hidden']='true';d.select_one('#'+new_id).insert(0,anchor)
if not d.select_one('#tool-harvest'):
 section=Soup('''<section class="section b17Preview" id="tool-harvest"><div class="wrap b17PreviewInner"><div class="b17PreviewCopy"><div class="kicker">Tool preview • Harvest Checker</div><h2>Pick it at the right moment.</h2><p>Review crop-specific signs of readiness before you harvest, cut or cure. Turn observations into a more confident next step.</p><ul><li>Crop and variety context</li><li>Color, texture and maturity clues</li><li>Harvest and storage guidance</li></ul><a class="btn sage" href="/tools/harvest-checker/">OPEN HARVEST CHECKER →</a></div><div class="phg-harvest-preview" aria-label="Visual app preview"><div class="phg-harvest-preview-head">HARVEST CHECKER <span aria-hidden="true">✓</span></div><p class="phg-preview-label">Look. Check. Harvest.</p><div><strong>Crop</strong><span>Choose what you’re growing</span></div><div><strong>Readiness</strong><span>Compare the signs you can see</span></div><div><strong>Next step</strong><span>Harvest now, wait or check again</span></div><p>Keep what you learn in Harvest Records.</p></div></div></section>''','html.parser').section
 d.select_one('#plant-identifier').insert_after(section)
hero=main.select_one(':scope > section.hero')
order=[hero,'tools','tool-zone','free-resources','garden-planner','tool-calc','services','tool-companion','tool-calendar','shop','products','plant-identifier','tool-harvest','courses','garden-library','seed-starting','statuary','garden-journal','harvest-records','my-garden','garden-inventory','blog','about','contact']
for item in order:
 n=d.select_one('section#'+item) if isinstance(item,str) else item
 assert n is not None,str(item)
 main.append(n.extract())
main.insert_after(d.footer.extract())
app_ids=['tool-zone','garden-planner','tool-calc','tool-companion','tool-calendar','plant-identifier','tool-harvest','garden-library','seed-starting','garden-journal','harvest-records','garden-inventory','my-garden']
stories=json.loads((ROOT/'.github/data/home-app-stories.json').read_text()) if (ROOT/'.github/data/home-app-stories.json').exists() else {}
for app_id in app_ids:
 section=d.select_one('#'+app_id)
 section['class']=list(dict.fromkeys(section.get('class',[])+['phg-home-app']))
 copy=section.find('h2').parent
 copy['class']=list(dict.fromkeys(copy.get('class',[])+['phg-app-copy']))
 for old in copy.select('.phg-app-story,.phg-app-save-note'):old.decompose()
 if app_id in stories:
  story=d.new_tag('div');story['class']='phg-app-story'
  for text in stories[app_id]['paragraphs']:
   paragraph=d.new_tag('p');paragraph.string=text;story.append(paragraph)
  lead=copy.find('p',recursive=False)
  if lead:lead.insert_after(story)
  else:copy.append(story)
  launch=copy.select_one('.phg-app-launch')
  if not launch:
   button=copy.select_one('a[href]');launch=d.new_tag('div');launch['class']='phg-app-launch'
   if button:button.wrap(launch)
  if launch:
   note=d.new_tag('small');note['class']='phg-app-save-note';note.string=stories[app_id]['saveNote'];launch.insert(0,note)
 for a in section.select('a[href]'):
  if '/tools/' in '/'+a['href'].lstrip('/') or a['href'].startswith('tools/'):
   a['class']=list(dict.fromkeys(a.get('class',[])+['phg-app-open']))
 for kicker in section.select('.kicker,[class$="-kicker"]'):
  kicker['class']=list(dict.fromkeys(kicker.get('class',[])+['phg-app-kicker']))
for section_id in ['free-resources','services','shop','products','courses','statuary']:
 section=d.select_one('#'+section_id);section['class']=list(dict.fromkeys(section.get('class',[])+['phg-home-offer']))
# Refresh only the homepage stylesheet URL when its presentation changes.
for link in d.select('link[href*="app-navigation.css"]'):link['href']='/app-assets/app-navigation.css?v=20261021-garden-start'
# Give the directory the exact same tool order as the advertisement sequence.
slugs=['growing-zone','garden-planner','garden-calculator','plant-companions','seasonal-calendar','plant-identifier','harvest-checker','garden-library','seed-starting','garden-journal','harvest-records','garden-inventory']
for slug in slugs:
 a=cards.select_one('a[href="/tools/'+slug+'/"]');assert a is not None,slug;cards.append(a.extract())
for icon in cards.select('.toolMiniIcon'):icon['aria-hidden']='true'
# Keep the directory count explicit.
assert len(cards.select('a'))==12
p.write_text(str(d));print('Organized twelve tool advertisements plus My Garden; final sections are Articles, About, Contact.')

# Preserve the final navigation, dictionary access and compact preview treatment.
import runpy
runpy.run_path(str(Path(__file__).resolve().parent/"finish_navigation_details.py"),run_name="__main__")

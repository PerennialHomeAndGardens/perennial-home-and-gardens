"""Retain homepage content while organizing twelve tools and the closing sections."""
from pathlib import Path
from bs4 import BeautifulSoup as Soup
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'index.html';d=Soup(p.read_text(),'html.parser');main=d.main
cards=d.select_one('#tools .creamToolGrid')
new=[('seed-starting','◌','Seed Starting & Tray Tracker','Organize seeds, trays, germination, transplant dates and succession sowings.'),('garden-journal','▤','Garden Journal & Logs','Record watering, feeding, observations, treatments and follow-up tasks.'),('harvest-records','▥','Harvest & Garden Records','Track yields, crop quality, storage and production across the season.'),('garden-inventory','▣','Inventory, Shopping & Budget','Keep supplies, shopping lists, purchases and garden spending organized.')]
for slug,icon,title,desc in new:
 if not cards.select_one('a[href="/tools/'+slug+'/"]'):
  cards.append(Soup('<a class="card creamTool pad" href="/tools/'+slug+'/"><div class="toolTitleRow"><span class="toolMiniIcon" aria-hidden="true">'+icon+'</span><h3>'+title+'</h3></div><p>'+desc+'</p></a>','html.parser'))
if not d.select_one('.phg-dashboard-link'):
 cards.insert_after(Soup('<p class="phg-dashboard-link">Your garden, together. <a href="/tools/my-garden/">Open My Garden →</a></p>','html.parser'))
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
order=['tools',hero,'tool-zone','free-resources','garden-planner','tool-calc','services','tool-companion','tool-calendar','shop','products','plant-identifier','tool-harvest','courses','garden-library','seed-starting','statuary','garden-journal','harvest-records','my-garden','garden-inventory','blog','about','contact']
for item in order:
 n=d.select_one('section#'+item) if isinstance(item,str) else item
 assert n is not None,str(item)
 main.append(n.extract())
main.insert_after(d.footer.extract())
# Give the directory the exact same tool order as the advertisement sequence.
slugs=['growing-zone','garden-planner','garden-calculator','plant-companions','seasonal-calendar','plant-identifier','harvest-checker','garden-library','seed-starting','garden-journal','harvest-records','garden-inventory']
for slug in slugs:
 a=cards.select_one('a[href="/tools/'+slug+'/"]');assert a is not None,slug;cards.append(a.extract())
for icon in cards.select('.toolMiniIcon'):icon['aria-hidden']='true'
# Keep the directory count explicit.
assert len(cards.select('a'))==12
p.write_text(str(d));print('Organized twelve tool advertisements plus My Garden; final sections are Articles, About, Contact.')

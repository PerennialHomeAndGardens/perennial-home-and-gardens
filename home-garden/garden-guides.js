/* Perennial Home & Gardens — garden reference library, Maryland zone 7b.
   Research starting points: University of Maryland Extension vegetable selection/care,
   fruit selection and fruit care. These are general guides, not diagnoses. */
(()=>{'use strict';
const fruit='https://extension.umd.edu/resource/fruits-home-garden';
const veg='https://extension.umd.edu/resource/vegetables-home-garden';
const fruitCare='https://www.extension.umd.edu/resource/fruit-plant-care';
const vegetableCare='https://extension.umd.edu/resources/yard-garden/vegetables/vegetable-care';
const flowering='https://extension.umd.edu/resource/native-plants-maryland-gardens';
const entries={
  apple:['Fruit tree','Full sun; well-drained soil; manage competing limbs and mulch outside the trunk flare.','Inspect winter branches and prune conservatively while dormant.','Thin crowded fruit after bloom; monitor scab, rust and fire blight symptoms.','Water deeply in drought; remove dropped or infected fruit; harvest by variety.','Collect leaves and fruit; avoid late nitrogen feeding.','Codling moth, apple maggot, scab, cedar-apple rust and fire blight; remove infected debris and use targeted, labeled management after identifying the cause.',fruit],
  pear:['Fruit tree','Full sun with good air movement; check compatibility among grafts; keep graft unions above soil.','Remove damaged or crossing wood during dormancy.','Check blossom health and fire blight; thin overfilled clusters.','Water during dry spells; watch for psylla; harvest at cultivar-appropriate maturity.','Rake diseased debris and mulch without piling mulch against bark.','Fire blight, pear psylla, rust and scale; prune infected wood with careful sanitation and follow extension guidance.',fruit],
  peach:['Stone fruit tree','Full sun, drainage and annual training; peaches usually need more disease attention.','Prune toward an open center close to late winter, avoiding severe cold.','Protect blossoms from frost where practical; thin young fruit.','Monitor brown rot and borers; remove fallen fruit and harvest promptly.','Remove mummified fruit and diseased twigs; protect young trunks.','Brown rot, peach tree borer, leaf curl and plum curculio; sanitation and correctly timed, locally labeled treatment are key.',fruit],
  plum:['Stone fruit tree','Full sun; maintain open branch structure; avoid wet feet.','Inspect scaffolds and remove damaged limbs when appropriate.','Check pollination and thin heavy sets; watch for plum curculio.','Harvest promptly and remove dropped/mummified fruit.','Clean fallen fruit and leaves; mulch roots, not trunk.','Brown rot, black knot, plum curculio; prune and discard visibly affected wood according to extension guidance.',fruit],
  cherry:['Stone fruit tree','Full sun, good air circulation and multiple suitable pollinizers where required.','Inspect for cankers, dead limbs and winter injury.','Watch frost at flowering; check for leaf spot and fruit set.','Net fruit against birds where feasible; pick promptly; remove diseased leaves.','Clean fallen leaves and mummified cherries; avoid unnecessary fall cuts.','Cherry leaf spot, brown rot, canker, aphids and birds; sanitation, airflow and site-specific controls.',fruit],
  crabapple:['Flowering / fruit tree','Full sun gives best flowering; select disease-tolerant cultivars.','Check crossing limbs in late winter.','Enjoy bloom; watch for scab or rust on new leaves.','Water young trees during drought and inspect fruiting.','Rake diseased leaves if disease pressure was high.','Apple scab, cedar-apple rust, fire blight, aphids; choose resistant plants and avoid excess fertilizer.',fruit],
  blueberry:['Berry shrub','Needs acidic soil (generally pH 4.5–5.5), consistent moisture, organic mulch and sun.','Prune mature shrubs selectively while dormant; check buds.','Feed based on soil test; protect flowers and monitor moisture.','Harvest fully colored berries; net against birds; avoid drying out roots.','Mulch, water if dry and limit late-season fertilization.','Birds, spotted-wing drosophila, mummy berry and leaf spots; sanitation, netting and ripe-fruit picking help.',fruit],
  strawberry:['Berry perennial','Full sun, well-drained soil and straw mulch; renew overcrowded beds.','Check winter protection and remove badly damaged leaves.','Keep flowers off bare soil and water evenly; protect ripening berries.','Pick frequently; renovate appropriate June-bearing plantings after harvest.','Remove diseased material; provide winter mulch once dormant.','Slugs, gray mold, birds, spotted-wing drosophila; mulch, airflow, sanitation and timely picking.',fruit],
  tomato:['Warm-season vegetable','Full sun; deep watering; mulch; support vines; rotate planting area.','Plan varieties, stakes and seed-starting schedule.','Harden off and transplant after frost; avoid wet foliage.','Water evenly; inspect leaves and pick fruit frequently.','Remove spent plants and infected debris; rotate crops.','Hornworms, early blight, septoria leaf spot and blossom-end rot; handpick pests, mulch and water consistently.',veg,'GNm3s9pmUuA'],
  cucumber:['Warm-season vegetable','Full sun, fertile soil, consistent water and trellis space.','Plan trellis and choose disease-resistant varieties.','Sow after soil warms; guide young vines onto support.','Harvest often; water at soil level; watch flower pollination.','Remove spent vines and weeds.','Cucumber beetles, powdery mildew, bacterial wilt and squash bugs; use early monitoring, barriers when appropriate and sanitation.',veg],
  squash:['Warm-season vine','Full sun; allow sprawling room; mulch; avoid waterlogged soil.','Prepare fertile bed and planting space.','Sow or transplant after frost; protect young plants from cold.','Water deeply; monitor stems and hand-pollinate if needed.','Harvest before hard frost; cure mature winter squash.','Squash vine borer, squash bugs and powdery mildew; inspect undersides and stems, remove eggs and discard infested vines.',veg],
  watermelon:['Warm-season vine','Needs long warm season, full sun, generous room and steady moisture during fruit set.','Plan a sunny large bed and select suitable short-season cultivars.','Sow after soil warms; protect seedlings.','Monitor ripeness by tendril and ground spot; reduce stress.','Harvest before frost and clean diseased vines.','Aphids, cucumber beetles, anthracnose, powdery mildew; good airflow, clean tools and targeted monitoring.',veg],
  pumpkin:['Warm-season vine','Full sun, rich soil, wide spacing and good pollination.','Plan space and soil preparation.','Plant after frost and keep vines off wet paths where possible.','Water during fruit development; rotate fruit off soggy ground.','Cure mature pumpkins and remove vines.','Squash bugs, vine borers, powdery mildew; regularly inspect leaf backs and remove pests and debris.',veg],
  asparagus:['Perennial vegetable','Deep, drained soil; keep crown area weed-free and avoid harvesting new beds too early.','Clear dead ferns before shoots emerge if not done earlier.','Harvest established spears for a limited season; stop to let ferns grow.','Leave healthy ferns to replenish crowns; water in drought.','Cut back dead ferns after dormancy and mulch lightly.','Asparagus beetles, rust, crown rot; remove old fronds and avoid saturated soil.',veg],
  onion:['Allium vegetable','Full sun, loose soil, consistent water while bulbing; select day-length appropriate types.','Plan seed or set timing.','Plant early; keep weeds controlled.','Reduce water when tops fall; cure bulbs dry with airflow.','Store in cool dry conditions; rotate bed.','Onion thrips and downy mildew; spacing, weed control and avoiding prolonged leaf wetness.',veg],
  garlic:['Fall-planted allium','Plant separate cloves in fall, pointed end up; mulch and keep well drained.','Check mulch; do not overwater winter soil.','Maintain weed-free bed; remove hardneck scapes if desired.','Harvest as lower leaves brown; cure thoroughly.','Plant healthy cloves after cooling weather; mulch.','White rot, onion maggot, bulb mites; use clean planting stock and long rotation.',veg],
  potato:['Tuber vegetable','Plant certified disease-free seed potatoes in loose drained soil; hill soil over developing tubers.','Plan spring planting; avoid green or sprouted grocery potatoes as seed.','Plant early in workable soil; hill as stems grow.','Water evenly during tuber formation; harvest carefully when skins set.','Store cool dark and remove diseased tubers.','Colorado potato beetle, early/late blight, scab; handpick insects, rotate and remove infected debris.',veg],
  sweetpotato:['Warm-season tuber','Plant rooted slips in warm soil with long growing season and good drainage.','Plan certified healthy slips.','Set slips after frost and keep newly planted roots moist.','Control weeds early and water during drought.','Dig before frost and cure roots in warm conditions.','Wireworms, flea beetles, root-knot nematodes; crop rotation and clean slips.',veg],
  beans:['Climbing legume','Full sun, warm soil, sturdy trellis; avoid excessive nitrogen.','Prepare trellis and select varieties.','Direct sow after frost; do not work plants while wet.','Harvest pods often to extend production.','Remove spent vines and rotate location.','Mexican bean beetle, aphids, rust and bacterial blights; handpick and improve airflow.',veg],
  peas:['Cool-season legume','Climbing support and cool weather; sow early, maintain even moisture.','Direct sow when soil is workable.','Train vines and pick pods while tender.','Remove spent vines as heat rises; consider fall sowing.','Clear debris and plan early spring crop.','Aphids, powdery mildew and root rots; trellis, rotate and avoid soggy soil.',veg],
  lentil:['Cool-season legume','Well-drained soil, moderate fertility and cool growing conditions; trial crop locally.','Research adapted cultivars for the area.','Sow into workable soil; keep weeds down.','Allow pods to dry on plants before threshing.','Save clean dry seed and rotate crops.','Aphids, rust and root rot; spacing, rotation and dry foliage.',veg],
  carrot:['Root vegetable','Loose stone-free soil; direct sow; thin to prevent crowded roots.','Prepare fine seedbed.','Sow shallowly as weather allows; maintain moisture for germination.','Thin and harvest when roots reach desired size; succession sow.','Protect fall crop with mulch and remove damaged roots.','Carrot rust fly, leaf blight and root-knot nematodes; rotate and use insect mesh as needed.',veg],
  lettuce:['Cool-season leafy green','Partial afternoon shade helps in warm spells; water evenly for tenderness.','Plan early sowings and cold protection.','Direct sow or transplant and thin for airflow.','Harvest before bolting; start another crop for fall.','Protect fall greens from hard freezes; mulch.','Slugs, aphids and downy mildew; hand removal, airflow and clean leaves.',veg],
  cabbage:['Cool-season brassica','Full sun, fertile soil and consistent water; protect transplants from cabbage caterpillars.','Start early plants or plan purchases.','Set out transplants, use row cover before pests arrive.','Monitor heads and harvest before splitting.','Clear brassica debris and rotate bed.','Imported cabbageworm, cabbage looper, flea beetles, clubroot; inspect undersides and use mesh and labeled Bt for young caterpillars.',veg],
  kale:['Leafy brassica','Cool weather improves flavor; feed lightly and harvest outer leaves first.','Start early seed or transplants.','Use insect netting to deter cabbage pests.','Harvest continuously; start fall plants.','Many plants tolerate cold; harvest through cool months.','Cabbageworms, aphids, flea beetles and black rot; inspect foliage and rotate.',veg],
  collards:['Leafy brassica','Full sun, rich drained soil; often best in cool weather.','Plan spring and fall sowings.','Protect starts from flea beetles and cabbageworms.','Harvest lower leaves regularly; water during dry spells.','Keep plants growing into cool weather where conditions permit.','Cabbageworms, aphids, flea beetles and leaf spots; insect netting, sanitation and crop rotation.',veg],
  corn:['Warm-season grass','Plant in blocks rather than single rows for wind pollination; water at tasseling.','Plan a sufficiently large block and fertile soil.','Sow when ground warms and thin carefully.','Water during silking and check ear readiness.','Remove residues and rotate.','Corn earworm, fall armyworm, raccoons and deer; check silks, monitor and protect ears.',veg],
  turnip:['Cool-season root','Best in cool weather; sow directly and thin roots.','Plan early crop.','Sow as soil becomes workable; maintain even moisture.','Harvest roots and greens young; sow fall crop.','Harvest fall crop before severe freezing or use protection.','Flea beetles, cabbageworms and root maggots; mesh covers, rotation and sanitation.',veg],
  herbs:['Perennial / annual herb','Well-drained soil and adequate sun; harvest lightly without stripping all growth.','Inspect overwintering plants and remove damaged parts.','Plant or divide as temperatures suit the species.','Harvest small amounts regularly; avoid wet crowns.','Mulch selectively and prepare tender plants for frost.','Aphids, spider mites and root rot; rinse insects, improve airflow and reduce excess moisture.',flowering],
  rosemary:['Woody Mediterranean herb','Needs especially good drainage, bright sun and protection from winter wet and cold.','Keep sheltered and barely moist; inspect winter dieback.','Prune lightly after new growth starts, not into old leafless wood.','Harvest small tips; let soil partly dry between watering.','Protect from deep freezes; pots may need a cool bright protected location.','Root rot, spider mites, scale; focus on airflow and avoiding waterlogged soil.',flowering],
  sage:['Perennial culinary herb','Full sun and sharply drained soil; mature plants become woody.','Remove frost damage after new spring growth appears.','Trim lightly to encourage fresh growth; avoid cutting into bare old stems.','Harvest leaves before flowering; water deeply but infrequently.','Avoid heavy fall pruning and soggy mulch on crown.','Root rot, powdery mildew, spider mites; space widely and improve drainage.',flowering],
  lavender:['Fragrant perennial','Full sun, lean well-drained soil, little extra fertilizer and airflow.','Check overwintering stems; do not prune into dead wood.','Trim lightly once new growth is clear.','Enjoy bloom and shear spent flowers without cutting into bare wood.','Avoid late hard cuts; keep crown free of wet mulch.','Root rot, spittlebugs and leaf spots; drainage and good airflow are primary defenses.',flowering],
  mint:['Spreading herb','Best contained in a pot or bounded patch; partial sun is fine; regularly harvest.','Check roots and containers for winter damage.','Divide or repot and trim vigorous shoots.','Water consistently and cut back to keep tidy.','Remove dead stems and contain creeping roots.','Rust, aphids, flea beetles and powdery mildew; thin, remove infected leaves and provide airflow.',flowering],
  thyme:['Low-growing herb','Needs sunny, well-drained soil; tolerate some drought once established.','Avoid soggy winter crowns and heavy foot traffic when frozen.','Trim dead tips as growth resumes.','Shear lightly after flowering and water sparingly.','Maintain drainage; avoid aggressive late pruning.','Root rot, mites and mildew in damp shade; increase sun and airflow.',flowering],
  salvia:['Flowering perennial','Sun to light shade, good drainage; remove spent flowers for repeat bloom.','Clear old stems when new growth starts.','Check crown and gently thin crowded shoots.','Deadhead and water deeply during long dry spells.','Leave some stems for wildlife or cut after frost.','Powdery mildew, aphids and leafhoppers; airflow, monitoring and washing pests off.',flowering],
  echinacea:['Native-style perennial','Full sun, well-drained soil; established plants tolerate drought; leave some seed heads for birds.','Leave dormant crown intact; remove damaged debris when growth starts.','Divide only if a clump becomes crowded; avoid soggy roots.','Deadhead for longer bloom or leave seeds; water new plants during drought.','Retain seed heads for wildlife and avoid heavy wet mulch on crown.','Japanese beetles, aster yellows and leaf spots; handpick beetles and remove plants with confirmed aster yellows.',flowering],
  iris:['Rhizomatous perennial','Full sun, shallow exposed rhizomes and good air circulation.','Clear dead leaves and inspect rhizomes.','Divide overcrowded clumps after bloom as appropriate.','Remove spent flower stalks; avoid burying rhizomes.','Clean up old foliage to limit borers.','Iris borers and soft rot; remove affected tissue and keep rhizomes dry and exposed.',flowering],
  peony:['Long-lived perennial','Sun, well-drained soil and shallow crown planting; avoid frequent relocation.','Check emerging shoots without disturbing roots.','Support heavy blossoms and avoid overhead water.','Remove spent flowers; keep foliage if healthy.','Cut diseased foliage after frost and discard, not compost.','Botrytis blight, leaf blotch and ants on buds (ants usually do not need control); airflow and sanitation.',flowering],
  rose:['Flowering shrub','Sun and air circulation; water at root level; fertilize according to growth.','Prune dead or weak canes near appropriate late-winter timing.','Inspect new growth for aphids and black spot.','Deadhead and irrigate deeply in drought.','Collect fallen leaves and avoid excessive late-season pruning.','Black spot, powdery mildew, Japanese beetles and aphids; sanitation, handpicking and resistant varieties.',flowering],
  dogwood:['Ornamental tree','Morning sun or part shade, cool mulched roots, good drainage.','Inspect twigs; avoid unnecessary heavy pruning.','Protect shallow roots from digging and drought.','Water during prolonged dry spells; monitor leaf scorch.','Maintain a wide shallow mulch ring and remove diseased leaves.','Dogwood anthracnose, powdery mildew and borers; site selection and reduced stress help.',flowering],
  crape:['Flowering landscape tree','Full sun, adequate room and good air movement; avoid topping.','Prune only crossing or damaged growth while dormant.','Watch for emerging growth and scale.','Enjoy flowering; water newly planted trees.','Clean up leaf litter if disease present.','Crape myrtle bark scale, aphids and powdery mildew; diagnose first, then treat appropriately.',flowering],
  evergreen:['Woody evergreen','Match sunlight and moisture needs; mulch roots, not the trunk.','Inspect wind or snow damage and evergreen browning.','Use only light selective pruning at suitable timing.','Water in extended drought; watch for mites.','Water before freeze if dry; avoid late fertilizer.','Bagworms, spider mites and scale; inspect early and remove pests before damage spreads.',flowering],
  shrubs:['Landscape shrub','Water during establishment; mulch root zone and avoid crowding.','Identify buds before pruning flowering shrubs.','Prune according to species bloom time.','Check leaves, scale insects and water stress.','Remove diseased debris and protect roots.','Scale, aphids, mites and leaf spots; improve airflow and identify before treating.',flowering],
  beds:['Raised-bed infrastructure','Check soil drainage, access from all sides and structural stability.','Top up settled soil and plan crop rotations.','Refresh compost if indicated by soil test; sow according to soil temperature.','Keep mulch and irrigation consistent; clean tools.','Remove diseased crop debris, protect soil with cover crops or mulch.','Slugs, weeds and soil-borne disease; sanitation, healthy soil and physical barriers. Inspect metal edges and timber condition.',veg,'9SMedSGbB1Q'],
  fence:['Garden gate / fence','Check post stability, hinge movement and gate clearances.','Inspect freeze-thaw shifts and hardware.','Tighten fittings and remove encroaching growth.','Check sagging, latch fit and climbing weeds.','Clear leaves and inspect corrosion or damage.','Not a plant; look for rust, damaged mesh, leaning posts and gaps that admit wildlife.',veg],
  tree:['Landscape tree','Check species-specific site needs, soil drainage, mulch and root flare.','Inspect broken branches and identify correct pruning window.','Watch emerging leaves and flower buds.','Water during drought; monitor canopy and trunk.','Clear competing vegetation around roots and remove diseased debris.','Species-specific leaf spots, borers, aphids and scale; identify issue before treatment.',flowering]
};
const classify=(name,group)=>{
 const n=(name||'').toLowerCase();
 if(group==='beds')return 'beds';
 if(n.includes('gate'))return 'fence';
 if(/blueberry/.test(n))return 'blueberry';
 if(/strawberr/.test(n))return 'strawberry';
 if(/apple/.test(n)&&!n.includes('crab'))return 'apple';
 if(/crabapple/.test(n))return 'crabapple';
 if(/pear/.test(n))return 'pear';
 if(/peach/.test(n))return 'peach';
 if(/plum/.test(n))return 'plum';
 if(/cherry/.test(n))return 'cherry';
 if(/tomato/.test(n))return 'tomato';
 if(/cucumber/.test(n))return 'cucumber';
 if(/butternut|squash/.test(n))return 'squash';
 if(/watermelon/.test(n))return 'watermelon';
 if(/pumpkin/.test(n))return 'pumpkin';
 if(/asparagus/.test(n))return 'asparagus';
 if(/garlic/.test(n))return 'garlic';
 if(/onion/.test(n))return 'onion';
 if(/sweet.potato/.test(n))return 'sweetpotato';
 if(/potato/.test(n))return 'potato';
 if(/snap.pea/.test(n))return 'peas';
 if(/bean/.test(n))return 'beans';
 if(/lentil/.test(n))return 'lentil';
 if(/carrot/.test(n))return 'carrot';
 if(/lettuce/.test(n))return 'lettuce';
 if(/cabbage/.test(n))return 'cabbage';
 if(/kale/.test(n))return 'kale';
 if(/collard/.test(n))return 'collards';
 if(/corn/.test(n))return 'corn';
 if(/turnip/.test(n))return 'turnip';
 if(/rosemary/.test(n))return 'rosemary';
 if(/sage/.test(n))return 'sage';
 if(/lavender/.test(n))return 'lavender';
 if(/mint/.test(n))return 'mint';
 if(/thyme/.test(n))return 'thyme';
 if(/salvia/.test(n))return 'salvia';
 if(/echinacea|coneflower/.test(n))return 'echinacea';
 if(/iris/.test(n))return 'iris';
 if(/peon/.test(n))return 'peony';
 if(/rose/.test(n))return 'rose';
 if(/dogwood/.test(n))return 'dogwood';
 if(/myrtle/.test(n))return 'crape';
 if(/pine|juniper/.test(n))return 'evergreen';
 if(/euonymus/.test(n))return 'shrubs';
 if(/shrub/.test(n))return 'shrubs';
 if(group==='vegetables')return 'herbs';
 return 'tree';
};
window.PHG_GUIDES={
 forAsset:(asset,displayName)=>{
  const filename=String(asset||'').split('/').pop().replace(/\.png$/i,'').replace(/_/g,' ');
  const key=classify(filename,String(asset||'').split('/')[0]);
  const v=entries[key]||entries.tree;
  const specific=filename.replace(/\b\w/g,c=>c.toUpperCase());
  const query=key==='beds'?'raised bed vegetable gardening':key==='fence'?'chain link garden gate installation':specific+' growing care university extension';
  return {key,title:specific,type:v[0],overview:v[1],spring:v[3],summer:v[4],fall:v[5],winter:v[2],pests:v[6],source:v[7],verifiedVideoId:v[8]||'',videoQuery:query,searchUrl:'https://www.youtube.com/results?search_query='+encodeURIComponent(query)};
 },
 references:{fruit,veg,fruitCare,vegetableCare,flowering}
};
})();
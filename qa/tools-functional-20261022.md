# Perennial Home & Gardens — Tool QA

October 22, 2026

All 12 garden tools and My Garden passed the software workflows below in an isolated Chromium/Chrome browser profile. The identifier is **guided screening; automatic photo identification remains unconnected**.

| Tool | Result | Functions exercised |
|---|---|---|
| plant-identifier | Pass | Four photo slots upload/preview/quality checks; Remove, replace and invalid/corrupt/oversized/HEIC handling; Disease/pest/plant screening and safe report text; Save report without photo bytes, refresh persistence, print action, clear; No image POSTs; automatic-AI status is truthful |
| growing-zone | Pass | Invalid ZIP feedback; 20603 lookup against bundled USDA dataset; Manual zone selection survives refresh |
| garden-calculator | Pass | All five calculator tabs and known-volume/count examples; Negative dimensions rejected |
| garden-planner | Pass | Add objects, resize, zoom and center; Save/reopen and add another object without duplicate IDs; Plan export, library search and help dialog |
| plant-companions | Pass | Companion search and related guidance; Saved favorites survive refresh; Unknown plant feedback |
| seasonal-calendar | Pass | Zone/month/focus updates; Task completion persists; Reset checked tasks |
| harvest-checker | Pass | Crop and selected readiness guidance; Save and reload favorites; Stage changes update guidance |
| seed-starting | Pass | Add seed inventory; Create tray and cycle cells/advance stage; Build three dated succession rounds; Save persistence |
| garden-journal | Pass | Identifier reports import once; Add journal entry/follow-up and reload; Search, JSON export and delete test entry |
| harvest-records | Pass | Save harvest with kg-to-lb conversion; Reload and JSON export; Negative harvest weight blocked |
| garden-inventory | Pass | Seed inventory imports automatically; Low stock, shopping list and mark purchased; Budget spending/remaining calculation; JSON export and reload |
| garden-library | Pass | Dictionary search/open/save term; Plant record search/open/save; Book search and private reading list |
| my-garden | Pass | Profile save/reload; Saved plans, plants and health reports visible; Seed, journal, harvest and inventory summaries connected; 12 tool links retained |

Layouts were checked at 1440, 768, 390 and 360 pixels on all 13 pages. No uncaught browser errors occurred. The tests used controlled JPEG, PNG and WebP image fixtures and dummy garden records, not visitor data. Print Report was verified with an instrumented browser print callback; native print dialogs and paper/PDF output were not tested.

## Corrections

- Added format, size and decode-error feedback to photo uploads, plus keyboard activation of the file picker and protection against stale asynchronous photo reads.
- Kept valid photos when a replacement file is invalid; removal clears the preview and input.
- Escaped typed identifier report fields and saved planner names so text remains text.
- Blocked negative calculator dimensions and enforced numeric save constraints in records, seed, inventory and planner controls.
- Corrected duplicate garden-object IDs after opening a saved plan.
- Connected Save Plant and Save Term to the current opened record.
- Clarified that automatic photo identification and cloud sync are not connected.
- Removed an old personal-name/family relationship reference remaining in the book collection introduction.

## What the identifier does today

Choose Upload under Whole Plant, Close-up, Leaf Underside or Stem/Fruit/Context. JPG, PNG and WebP images up to 15 MB are supported; HEIC requires conversion to JPEG. Images are processed on the page for resolution, brightness, contrast and broad color cues. Visitors then confirm symptoms and conditions and choose Analyze Evidence. Saving creates a report visible in My Garden and imported into Garden Journal. The photo files themselves are not saved; leaving or refreshing the page removes them.

## Remaining work

1. Connect a secure image-recognition backend for actual species, pest and disease recognition. Current matching uses 13 disease/damage patterns, 7 pest patterns and 3 broad plant-trait paths. It is not a complete photo-diagnosis service.
2. Validate screening accuracy against real, labeled plant-health cases; the upload tests check software mechanics, not diagnostic accuracy.
3. Add consistent backup-file import/restore across tools and complete seed/tray backup export. Existing local saves do not transfer automatically between devices.
4. Add accounts/cloud sync only if wanted later. Current use requires no membership.
5. Test real Android/iPhone camera and gallery pickers, phone-specific image formats/orientation, speech permissions, and native printing. Browser viewport emulation does not establish those physical-device results.
6. Expand the curated companion and harvest collections (currently 21 and 23 crop entries) as a content improvement.


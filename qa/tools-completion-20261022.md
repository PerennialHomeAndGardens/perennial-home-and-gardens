# Perennial tools: completion QA

October 22, 2026

- Actual model download/inference UI, saved model results, crop-change invalidation, no photo POST and camera file-chooser path passed
- 50 companion and 51 harvest entries render; new Lavender/Asparagus guides work
- Full backup export, preview/confirmation, new-browser restore, seed trays/journal/book notes, existing-data protection, replace mode and invalid-file rejection passed
- Chrome print-media report visibility and actual Letter PDF generation passed; physical printing remains untested
- Backup dialog fits four viewport widths; no uncaught browser errors

## Measured leaf-model results

46 PlantDoc test images; known crop supplied. Top-1 correct: 20 of 46 (43.5%). Top-3 correct: 34 of 46 (73.9%). Threshold accepted: 18, of which 12 matched the label. This is a small sample, not a diagnostic certification. See `leaf-model-validation.json` for every case.

## Delivered

- On-device, click-to-run leaf comparison, with explicit limitations and no photo POSTs.
- Separate photo-library and camera-picker controls.
- Backup & Restore across the twelve tools and My Garden, also accessible on book pages. Profiles, plans, trays, successions, notes, reports, collections and calendar task selections are included; photos and unsaved work are excluded.
- Preview, confirmation, protection of existing sections by default, deliberate replacement, automatic before-restore download and rollback on storage-write failures.
- Older journal, harvest, inventory, library, book-note and Gen 2 plan exports are accepted.
- 50 companion entries, 51 harvest guides, 54 screening/trait entries.

## Still requiring physical-device access

1. On iPhone Safari and Android Chrome, open the identifier and choose Upload for a gallery photo. Verify preview, rotate/orientation and replacement.
2. Choose Take photo, capture a clear leaf, and verify the preview and Cancel behavior. HEIC is not decoded by this tool; choose/export JPEG where necessary.
3. Choose a supported crop, select the matching photo view and click Compare leaf photo. Compare the result with a known diagnosis; record errors as well as correct matches.
4. Analyze Evidence, then Print Report. Verify the native print sheet and Print/Save as PDF on the phone or computer.
5. Download a garden backup on one device, move the file privately to another, and restore it there after reviewing the preview.

No accounts or cloud sync were added. The backup file enables manual device transfer. Automatic cloud sync is optional future scope. Real-phone picker behavior and physical printing cannot be certified by desktop emulation.

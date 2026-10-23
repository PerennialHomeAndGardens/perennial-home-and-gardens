# Perennial Home & Gardens — current launch checklist
Reviewed October 23, 2026 against main a68840f and clarification commit e998919.

This is the current status summary. The remaining-work lists in earlier dated reports are historical: the October 22 completion build subsequently added universal backups, larger collections, and an experimental local leaf model.

## Completed and retained
- 12 garden tools, plus the separate My Garden dashboard. The homepage lists the 12 tools in order; My Garden introduces browser-local saved records.
- Direct Garden Library menu access. Library includes dictionary, plant records and 100 individual gardening-book guides, with reading lists and notes.
- 29 educational article pages plus their index, reading controls, quizzes, related links and reserved partner spaces.
- Shared wood-grain branding, compact menu/jukebox, app transitions, footer and mobile contact arrangement.
- Tanya's existing recorded introduction with manual playback, categories, scrolling chat history and browser speech input. There are 112 original and 60 additional prepared reference answers; this is a curated matcher, not an unrestricted AI service.
- Universal backup/download/import/restore across all 13 tool/dashboard pages and book pages. Browser-local records can be transferred manually with JSON files. Photos and unsaved work are excluded.
- Expanded collections: 50 companion entries, 51 harvest guides and 54 guided diagnostic patterns.
- Four identifier photo slots, image preview/quality feedback, camera-picker controls, saved observation reports, journal import and printing.
- Installable website support. No account is needed; automatic cross-device synchronization remains unconnected.

## Work resumed in this review
- Audited local href/src destinations across 145 homepage/tool/article/book HTML pages: zero missing local targets. This checks local paths, not every external vendor, video or reference URL.
- Confirmed on the live website that the menu opens the Garden Library and that dictionary/plant/book sections are present.
- Clarified the homepage contact action as “Open email draft,” with visible instructions to press Send in the visitor's email app and a direct-address fallback.
- Replaced the directory's overpromising “scan, identify, diagnose” description with guided photo/symptom comparison language.
- Checked the changed JavaScript with node --check. Full regression results below come from the preceding build, not a new complete test run.

## Prior verified software tests
Completion workflow 39878858496 passed tool workflows, browser-local persistence, backup round trips and failure handling, photo upload/replace/remove/error paths, responsive widths 1440/768/390/360, model UI/inference and browser PDF output. See tools-completion-20261022.md and its JSON report.
The earlier final-build-report.md records Tanya audio/chat, mocked speech recognition, article and mobile-layout tests.
These do not establish physical-device permissions, real speech accuracy, native camera/print behavior, or human editorial correctness.

## Must resolve or explicitly accept before promotion
1. **Email capture is not automatic.** Resource forms open the download folder and store the entered lead in the visitor's browser; they do not deliver it to the business or create a remote mailing list. Newsletter requests and contact/service inquiries use the visitor's email app. Do not describe these as completed automatic subscriptions or automatic message delivery.
   - Owner: choose the mailing-list/form service you want to own and connect it, or provide its hosted signup/form endpoint.
   - Implementation: connect both resource choices and newsletter to that endpoint with consent, success/error feedback and appropriate privacy wording.
   - Acceptance: submit a test address, verify it reaches the business/provider, verify both downloads and any promised welcome message, then test unsubscribe where applicable.
   - Contact can remain manual email if that delivery method is acceptable.
2. **The plant model is experimental, not dependable diagnosis.** Saved PlantDoc evaluation: first choice 20/46 (43.5%); top three 34/46 (73.9%). The interface already labels the comparison experimental and keeps it collapsed. Guided screening works, but broader reliable image recognition remains unfinished.
   - For launch, retain the limitation and market it as screening/evidence organization.
   - To promise automatic diagnosis, first replace/improve the model and pass an independent, representative validation set. No new paid provider or account has been created.
3. **Physical phone acceptance remains.**
   - On an iPhone in Safari and Android phone in Chrome, open Plant Identifier; try Take Photo and Upload in all four slots, replace/remove, and inspect orientation and image-format errors.
   - In Tanya, allow microphone once, dictate, stop/restart, edit the text, then press Send. Repeat with permission denied; text input must remain usable. Open the mobile keyboard and confirm input/Send/Close stay reachable.
   - Save a test garden, download a backup, restore on another browser/device, and verify the records. Try native printing.
   - Report device/browser and any failing step. A cloud-browser simulation cannot replace these checks.
4. **Business/content readiness.** Confirm actual service availability, course-preview promises, contact inbox, product destinations and the two resource files' public access. Affiliate spaces are currently reserved; affiliate account/tag activation is still owner-dependent. Do not assume all book vendor links earn commission. Review legal/business copy against actual operations.

## Optional after launch
Accounts, membership, automatic cross-device sync, broader curated knowledge and a general AI answer backend are additional product work, not prerequisites for a browser-local tools launch.

## Recommendation
A limited visitor preview is reasonable with explicit browser-local saving, manual email and experimental screening disclosures. A full launch promising automatic email collection and reliable plant diagnosis is not ready.
Live site: https://perennialhomeandgardens.com/

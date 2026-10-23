# Perennial Home & Gardens — current launch checklist
Updated October 23, 2026 after the verified manual-email build. Previous clarification deployment succeeded in GitHub Pages run 39946573659.

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

## Manual-email build completed in this pass
- Owner selected “Keep manual email for now.” No mailing provider, membership system, paid audio generation or new hosting was introduced.
- Contact, service inquiry and newsletter requests share a draft-review dialog. The original contact message remains when the dialog closes. Literal markup stays text.
- Worksheet access uses a persistent direct link, so a blocked programmatic popup no longer silently loses the download. Email is optional; newsletter enrollment requires an explicit request.
- Current privacy copy explains manual delivery, browser-local records and temporary plant photos.
- GitHub Actions run **39966866129**, job **120458880497**, passed the new email/download acceptance checks and all 12 tool workflows plus My Garden. The draft fits 1440×1000, 390×844 and 360×640; tool layouts also passed their existing responsive checks. No uncaught page errors occurred in the exercised flows.
- The first test run read asynchronous clipboard feedback too early; the test was corrected to await completion. Resource and newsletter timing tests were also isolated into separate visits. The corrected runs passed before publication, including a second full pass after versioned loading was added.
- Public browser checks opened the Google Drive folder signed out and opened both Plant_Profile_Gardening_Sheet.pdf and Houseplant_Care_Sheet.pdf previews. Actual file saving and native printing were not exercised in that check.
- The visible homepage, articles, books, wood-grain artwork, Tanya recording, jukebox and tool implementations were retained. Shared script URLs are stamped from the code content during deployment so returning visitors request the new interface code; page artwork and content are not replaced.
- Evidence: manual-email-20261023.json, manual-email-{1440,390,360}.png and refreshed tools-functional-20261022.json. The date in the latter filename is retained for compatibility; use the workflow above for this rerun's time.

- Follow-up correction: a live browser retained the previous shared JavaScript after successful deployment. The loader now carries its version into the shared script request; deployment stamps 166 HTML loader references using the loader plus shared-code hash. This directly addresses stale shared-interface code after updates.

## Prior verified software tests
Completion workflow 39878858496 passed tool workflows, browser-local persistence, backup round trips and failure handling, photo upload/replace/remove/error paths, responsive widths 1440/768/390/360, model UI/inference and browser PDF output. See tools-completion-20261022.md and its JSON report.
The earlier final-build-report.md records Tanya audio/chat, mocked speech recognition, article and mobile-layout tests.
These do not establish physical-device permissions, real speech accuracy, native camera/print behavior, or human editorial correctness.

## Must resolve or explicitly accept before promotion
1. **Manual email accepted by the owner for this launch.** Contact/service/newsletter requests now open a reviewable draft with an email-app link, copyable message and address, and a manual-copy fallback. Nothing is sent until the visitor sends it in their email service. Downloads are available without entering an email, and optional newsletter requests are clearly separate. This version no longer writes new resource-email leads into browser storage. Existing garden data is retained.
   - Owner: check perennialhomeandgardens@gmail.com and handle incoming inquiries and explicit newsletter requests. Automatic mailing-list delivery remains optional future work.
   - Actual operating-system email-app launch and inbox delivery still require a real send by the owner or tester; no test email was sent by this build.
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
A limited visitor preview is reasonable with explicit browser-local saving, manual email and experimental screening disclosures. Do not promise automatic subscriptions or reliable plant diagnosis. The chosen manual-email mode itself no longer blocks a launch that describes these limits accurately.
Live site: https://perennialhomeandgardens.com/

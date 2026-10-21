# Perennial Home & Gardens — completed build and Tanya assistant

Continued the existing site and separate Perennial repository. Original source: 8ec40f7d8baddd30d24b470a1d82b032945f945b. No replacement website, new hosting service, paid infrastructure or generated introduction audio.

## A. Previous requests completed

- Eight homepage tool cards link to their app pages; Open buttons use explicit destinations. Harvest Records no longer goes to Harvest Checker. Homepage previews remain advertisements rather than working embedded tools.
- Preserved all13 existing tool pages. Repaired pre-existing syntax errors in My Garden, Garden Library and Garden Planner. Recovered the original Planner controls removed by the earlier shared-header build, including Save, Layouts, Export, Help and mobile panels. Verified Help and placing a plant on the map.
- Permanently sticky wood-grain branding; small unboxed menu and animated jukebox icons; labels above icons. Shared thinner footer, legal pages, app installation and professional single-column mobile contact form.
- Expanded the20 existing catalog topics and9 existing photo stories into29 full educational articles, each at least3000 teaching words. No new topic batch. Preserved the9 photographs; added animated gardening illustrations for remaining topics, primary references, goals, vocabulary, pretests, labeled illustrative charts, embedded-video controls, activities, review quizzes, related links and two reserved affiliate design spaces per article.
- Full article index with seasonal feature, search and topic filtering. Full article pages replace popup excerpts. Perennial Reading Bar includes comfort, light/dark, text, focus, breaks, journal and listening controls and stops above the footer.
- Completed the previously requested jukebox root choices Meditation, Music, Movies, Motivation; restored the actual small i.e. mark and kept the free-resources destination. The Tanya redesign did not replace jukebox internals.
- First resource offer25seconds; distinct monthly newsletter offer120seconds; each once per visit. Busy forms/panels defer prompts.

## B. Tanya improvements

- Uses assets/tanya-garden-guide-intro.mp3, unchanged,22.36seconds. Compact Hear Tanya’s Message above the input; click to play, pause, restart and stop/reset on close. Coordinates with other site media to prevent overlapping audio.
- Two stacked business/gardening category buttons; five suggestions each. Shared internally scrolling suggestions and conversation, retained history, newest-answer scrolling and return-to-suggestions control. Existing112 prepared knowledge answers retained.
- Native browser speech recognition with neutral/green raised microphone, editable draft, resume/appending,4.5second silence timer and explicit Send only. Drafts survive stopping, denied permission and unavailable recognition. Late recognition events cannot interrupt a newer session.
- Constrained responsive popup, fixed input controls and visualViewport handling. Desktop600px maximum; mobile fits available height with internal scrolling.
- Footer and assistant header use the recovered original navigation gradient: linear-gradient(90deg,#070503 0%,#110b07 61%,#4b260e 100%). Wood-grain artwork remains byte-for-byte unchanged.

## C. Actual verification

GitHub Actions run39539447749 passed the full browser suite:13 app pages and restored Planner actions; actual MP3 play/pause/restart/close; both categories and chat history;112 known answers; all29 article pages and correct/incorrect quiz feedback; article navigation; mobile contact; matching gradients; icon labels; four jukebox categories;25/120second prompts using a browser clock; no uncaught page errors. Responsive assistant checks passed1440x1000,1024x768,768x800,390x844,360x640 and390x360. The last is a reduced-height keyboard simulation.

Speech callbacks were mocked for repeatable activation, stopping, resuming, permission denial, unavailable recognition and no-auto-send assertions. Physical microphones, real speech transcription, actual iOS/Android keyboards, audible sound quality and playback availability of every third-party video were not verified. Video controls and supplied primary-source links were checked; external providers can impose playback restrictions.

Additional local checks found no broken local hrefs across49 generated/current HTML pages and no inline JavaScript syntax errors. MP3 and wood artwork matched the original file hashes. Browser preview checks confirmed an actual Tanya answer, actual MP3 playback and close-to-stop, article quiz feedback, reading toolbar, dark mode and the corrected Harvest Records destination.

## D. Remaining work / participation

1. On a phone, open the live site and Tanya. Tap the neutral microphone, allow browser microphone access, speak, stop and resume. Confirm the text remains editable and no question sends until pressing the green Send button. Check the keyboard keeps input/Send accessible. This physical-device check cannot be replaced by browser mocks.
2. Newsletter automation is not connected to a mailing-list backend. The120second offer explicitly opens an email request through Subscribe by email; the visitor must send it. The existing resource form unlocks the Drive resources and keeps its lead in that browser; it does not silently add an address to a remote list. For automatic subscriber storage and welcome emails, provide the signup-form or endpoint URL from your chosen mailing-list service. No Supabase account is required for this UI build.
3. The assistant uses the retained curated answer library and a useful fallback for unmatched questions, rather than a newly provisioned general-purpose AI backend.

Live site: https://perennialhomeandgardens.com/

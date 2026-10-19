# Chengdu travel slides: historical local draft checkpoint

This is the **pre-amendment checkpoint**, preserved as history rather than current release status. The user subsequently changed gift filtering to community opinions. See [the community release verification](chengdu-slides-community-release-verification.md) for the later 15/15/15 dataset and its actual verification.

Date:2026-10-19. **The original end-to-end publication task is not complete.**

## Actual content and artifacts

- 15 attraction identities and15 distinct restaurant brands, with source-specific branches and paired Thai/simplified-Chinese content.
- 0 qualified gifts. No unavailable Shopee result or uncertain China/Thai price has been converted into a verified recommendation.
- 166 rendered pages: identical-language ordering is adjacent Thai then Chinese; dense units are paginated at corresponding bullet boundaries without dropping text.
- Original, explicitly non-documentary conceptual illustrations on every draft page; no retrieved Commons photo was claimed as downloaded.
- A working self-contained HTML draft and a real166-page Chromium PDF exist in the ignored `_reports/chengdu-slides/draft/` directory. All runtime image/font bytes in the standalone HTML are embedded.

## Verification actually executed

- `python3 -m unittest discover -s tests/chengdu_slides -p 'test_*.py' -v`: **46 passed**.
- `npm test` from `tests/chengdu_slides`: **11 real Chromium tests passed**.
- Actual-page browser checks cover every page's language adjacency, image decoding, font loading, and copy/caption clearance above the footer.
- Browser checks include mobile reading without horizontal overflow, natural-scroll position preservation across language/view changes, native PageDown in reading view, per-section font scoping, narrow-screen no-JavaScript geometry, keyboard/browser-history/wheel/horizontal-touch navigation, ignored editable focus, rejected fullscreen, and offline HTML/PDF export with zero HTTP requests.
- `pdfinfo` confirms166 pages at1440×810 points. The HTML/PDF are not fabricated API output or placeholder screenshots.
- Original font SHA256 and generated WOFF2 SHA256 values were read and checked against `slides/chengdu/fonts/source-manifest.json`.
- Upstream OFL notice files retain their original bytes, including upstream trailing whitespace; staged whitespace checks exclude only `slides/chengdu/fonts/*_OFL.txt`, not application code or content.
- Release-builder negative check returned exit1 and did **not** create `slides/chengdu/index.html`.
- Existing Jekyll production build ran successfully in the existing local verification image before the final reviewed UI fixes. This is not a claim that a new public slide route was exercised or deployed. Its original test suite also has pre-existing metadata findings; it is not reported as universally clean.

## Review findings and disposition

Read-only review found no Critical issue and two Important issues. Both received reproduced failures followed by fixes and passing browser/unit coverage:

- Reading view did not synchronize the visible section with navigation state. It now synchronizes natural scroll, keeps native scrolling keys, uses viewport-fixed controls, and retains the current language pair when returning to slides.
- Standalone export omitted complete font notices. Font assets now require a real contained nonempty notice file, and standalone HTML embeds full copyright/license notices as non-executable JSON. License bytes also contribute to content versioning.
- The review's narrow-screen no-JavaScript concern was reproduced with copy-column geometry, then fixed by reusing responsive reading-layout CSS in the fallback.

Only the two supplied panda screenshots were visually reviewed. Full source-by-source and bilingual editorial review of all entries remains pending; structural tests and sampled direct source rechecks are not represented as that full audit.

## Still blocked / not performed

- At least15 gifts meeting the agreed strict market-evidence policy are missing. Current source access/availability/comparability did not establish them.
- Attractions/restaurants remain`sourced_draft`, not silently promoted to`editorial_ready`.
- Final public-route generation, merge into the publishing branch, push and live deployment/version read-back have **not** occurred.
- This checkpoint must not be presented as satisfying all three requested categories or as already online.

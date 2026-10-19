# Chengdu slides: community-curated local release verification

Date: 2026-10-19. Content version: `e62fd48ce3c2e24c`. This is a **local release checkpoint**, not a claim that GitHub Pages has been updated.

## Delivered content

- 15 attractions, 15 distinct restaurant brands and 15 distinct gift types.
- 306 illustrated pages: adjacent Thai/simplified-Chinese pairs, with corresponding bullet pagination.
- 140 entry units and 13 supporting units. Ten supporting pairs filter lower-priority/avoid purchases; they do not increase the recommendation count.
- 83 retained source-observation records, representing 73 distinct literal URL strings. Those totals are not independent-author or unique-website counts.
- Original conceptual illustrations on every page, clearly disclosed as non-photographic. Local licensed WOFF2 fonts and original OFL notices are retained.

## Approved gift-policy amendment

The user replaced the direct-marketplace requirement with community-comment synthesis/filtering. The active opt-in is `community_curated` / Route C. It records dated/explicitly-undated experiences, buying rationales, counterpoints and persistent bilingual uncertainty labels. Neither current Shopee/Lazada absence nor a 30% saving is claimed. Strict measured-search and like-for-like-price Routes E/P remain unchanged.

The Shanghai historical-map option was excluded as a weak Chengdu fit. A dated Chengdu Bestore walnut-stuffed-date tasting opinion replaced it conditionally, with distinct-SKU, allergen and import caveats. Historical Pantip Laz/Shopee mentions are explicitly not current stock verification. Foreign-market availability, single-OP questions and possible promotional links retain their limits.

All 27 selected-gift observation quotes were checked against the actual saved retrieval captures and bound to reviewed excerpt scope in the canonical source records. This does not establish that opinions are true or recover unseen replies. Every observed recommendation/countervoice must remain visibly cited somewhere on the relevant gift's pages; unrelated verified citations cannot substitute for the missing voices.

## Editorial review and corrections

A read-only internal review covered all 45 selected entries, 140 entry units, 13 supporting units and 83 retained source records. It checked bilingual meaning and consistency with retained observations, **not** an independent re-fetch of every remote page.

Three Important editorial findings were corrected: softened Thai poor-value wording, unsupported named bus-stop specificity, and a reversed Du Fu hall name. The Minor tour-shopping/group-buying translation distinction was also corrected. No numerical price/stock conclusion was invented to fill a count.

Two Important code findings were reproduced and fixed: observations could exceed source-excerpt scope, and qualifying voices could disappear from visible citations. Malformed evidence now returns findings instead of crashing. Negative coverage includes unseen quotations, non-string/blank locators, missing countervoice citations and malformed evidence payloads.

## Actual verification

- Python suite: **72 tests passed**.
- Real Chromium suite: **12 tests passed**.
- Publication validation returned `valid: true`, with no findings; the release builder generated the actual `slides/chengdu/index.html` and `manifest.json`.
- The full production Jekyll build exited 0. The generated route and manifest were actually served over loopback HTTP and read back: version `e62fd48ce3c2e24c`, counts 15/15/15, 306 pages.
- Every production page passed language adjacency, image decoding, font loading and body/caption clearance checks: 306 decoded images, no bad pairs/collisions, no unloaded fonts or page errors.
- Release mode contains no draft labels and retains 140 community-opinion labels.
- The actual standalone release HTML was opened offline: **zero HTTP requests**, working next-page navigation and mobile reading without horizontal overflow. It embeds actual images/fonts and complete font notices.
- The browser produced a real 306-page PDF at 1440×810 points. `pdfinfo` and text extraction confirmed the page count, Thai/Chinese content, walnut-date selection, historical Laz example and final tour-sales warning.
- Source and derivative SHA256 values for all three font files matched the retained manifest and actual files.

### Visual regression caught beyond geometry

Three production screenshots initially showed language ghost layers despite valid geometry. A reduced-motion regression reproduced both Thai and Chinese being painted after one click. The upstream stylesheet's global nonzero transition duration caused implicit fades. A later author-style reduced-motion override disables transitions/animations; the pinned upstream stylesheet remains unchanged.

The new immediate-paint regression passes. Fresh production captures assert exactly one painted target page. A read-only visual follow-up inspected the fresh Thai gift, Chinese gift and market-counterpoint screenshots and found no visible Critical/Important defect or remaining ghosting. Only these three screenshots were visually inspected; this is not a visual audit of all 306 pages.

### Website distribution and privacy

An actual early Jekyll build copied the new development tests/dependencies into the website output. Scoped `_config.yml` exclusions now remove the new script/test namespace and project spec/verification documents from the website distribution without changing existing articles or navigation. The rebuilt output was checked to exclude raw reports/data directories, worktrees, worker state and the new script/test directories. Development source/tests remain version-controlled repository content, distinct from consumer publication inputs.

Raw captures, workers, previews, dependency caches and generated verification outputs remain git-ignored. The public-content and staged-file secret/routing-pattern scans found no matches; no private worker/capture/cache paths were staged.

## Remaining external action

At this checkpoint, the feature is prepared locally on `feature/chengdu-slides`. Merge/push to the public publishing branch and live GitHub Pages content-version read-back have **not** occurred. Repository metadata confirms `lawdalana/lawdalana.github.io` is PUBLIC with default branch `main`; exact-scope public-publishing confirmation remains separate from command approval. Local success must not be reported as an online deployment.

Current prices, shop stock, source opinions and product-specific import eligibility are not certified by these tests. Check operator/official rules before travel; personal-use guidance is not automatic permission to import gifts.

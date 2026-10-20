# Chengdu bilingual travel slides

## Content and release state

The Thai-primary photographic release contains **15 attractions, 15 distinct restaurant brands and 15 gift types**, with **123 Thai pages and 130 simplified-Chinese pages (253 total)**. Every page uses a credited local photograph. Thai pages are packed using actual rendered space, not a fixed bullet limit; Chinese may span additional pages without forcing extra Thai pages. Original entry text, evidence and readable font sizes are preserved.

`index.html` and `manifest.json` are generated release artifacts for `/slides/chengdu/`. The canonical metadata value `published` means editorially approved for release generation; it does **not** by itself prove a GitHub push or a live deployment. Read back the deployed `content_version` to establish that separately. Existing site articles and navbar entries are preserved; the deck is additionally registered under Travel in the shared Slides menu and its folio provides a return link to the website. Deployment fingerprints include the renderer/template, viewport foundation, canonical data, styles, scripts and local assets.

## Presentation language navigation

Next/Previous, keyboard navigation, wheel and horizontal swipes advance within the current language. The bottom `ไทย / 中文` button always opens the **first page of the same topic** in the other language, including when switching from a continuation page. Contents, progress, footer numbering and first/last boundaries count the chosen language independently. Explicit continuation deep links and browser history work; legacy split-page links resolve to the original topic. No-JavaScript reading and bilingual print exports retain all text in both languages.

## Regenerating measured pagination

Run `python3 -m scripts.chengdu_slides.pagination --write` with the isolated browser-test dependencies installed, then `python3 -m scripts.chengdu_slides.cli build`. Chromium measures the real 1920×1080 layout with all three local fonts loaded. It merges old artificial splits, packs Thai first, and partitions each corresponding Chinese range only if necessary. Canonical `pagination` ranges must cover every source bullet exactly once. A layout-input signature rejects stale plans after source, rendering, font or stylesheet changes. Measurement reports stay under ignored `_reports/`, not in the public site.

## Community-based gift filtering

The user's amended policy is `gift_policy: community_curated` (Route C). It selects experiences from actual Pantip/public discussions, with both buying reasons and conflicting or limiting opinions. It does not require a marketplace API, prove whole-platform absence, or apply a mandatory 30% saving threshold. Strict measured-search/price Routes E/P remain available and unchanged when those claims are actually made.

- Fifteen selected product types are counted once each, not by color, size, tea example, pen model or city variant.
- Ten additional supporting pairs explain lower-priority/avoid examples, including historical Laz/Shopee mentions and tour-shop pressure. They do not inflate the 15 recommendations.
- Every selected observation is attributed, dated or explicitly undated, and bound to a reviewed short excerpt. All observed recommendation/countervoice sources must remain visibly cited somewhere on that gift's pages.
- Partial/indexed content is labeled as such; it is not a recovered full discussion. Multiple comments in one thread do not become independent surveys.
- US/other-overseas availability is not Thai stock evidence. Single-OP questions are not multi-person conclusions. Old prices do not become current quotes. A Shopee review with shop links has an explicit possible-commercial-bias caveat.
- The Bestore walnut-date option is a single dated Chengdu tasting opinion, conditional on labels/allergens/import checks, not a matched current SKU or a China-only claim.
- Personal-use FDA guidance and dated Customs context do not automatically authorize food gifts. No medical efficacy is endorsed.

The preceding community release's 45 entries and 13 supporting units received an internal bilingual/source-to-retained-observation review. The photographic edition preserves all original entry text/evidence and has 20 supporting units, including its new cover/chapter treatments. Photo review checks retained metadata and visible subjects; it is not a fresh factual audit of every travel source or certification of opinions, current prices, stock or import rules.

## Images and fonts

Every current page has an **actual local photographic bitmap**, not the preceding edition's conceptual SVGs. Projection mode uses large panels, alternating layouts, full-image chapter openers and readable attribution backings. Location images are reviewed for the actual place; restaurant dishes, product types, ingredients and cultural-context examples explicitly disclose when they are not the recommended restaurant plate, exact merchandise, certified workshop or current stock. Photos may be historical or undated.

`images/PHOTO_CREDITS.md` retains each work's supplied title, creator/credit, primary source, original image, license, retrieval date, modifications and derivative SHA256. Explicit Commons or Openverse/Flickr rights metadata is retained, not an independent ownership certification. CC BY-SA derivatives retain the stated license. Files are resized/re-encoded with metadata removed; display may crop and lightly change color. No photographic content was generated. Every photo is provenance-gated even if the edition flag is missing; `visual_policy: licensed_photography` additionally prohibits diagrams in this edition.

Local WOFF2 derivatives originate from Kanit, Noto Sans Thai and Noto Serif SC. Original OFL notices remain at `fonts/*_OFL.txt`; derivative family names were changed. The Chinese subset includes requested supported codepoints from canonical captions and the fixed interface; an explicit `--extra-text` input can cover private prototypes. `fonts/source-manifest.json` records original and derivative SHA256 values. Regenerating fonts requires the corresponding source TTF cache and verification of those hashes, licenses and derivative-name requirements.

The standalone HTML embeds actual font/image bytes plus full font and photo rights notices in non-executable JSON (`font-license-notices`, `photo-license-notices`). It needs no runtime CDN, analytics or network images. Single-file photographic exports are large because repeated image references are embedded; a portable directory/ZIP avoids that repetition. `render_standalone(data, site_root)` remains an explicitly labeled preview by default; the opt-in `publication=True` export rechecks publication/asset approval before retaining release labels and all community disclosures. Mobile reading collapses the toolbar by default, with an accessible reopen button; all paired content remains exposed.

The fixed-stage foundation comes from the MIT-licensed [frontend-slides](https://github.com/zarazhangrui/frontend-slides) skill at commit `9906a34d640d2111f724544cbc50f7f130569ae1`. Its notice remains at `scripts/chengdu_slides/FRONTEND_SLIDES_LICENSE.txt`.

## Source of truth

- `_data/chengdu_slides/`: canonical bilingual JSON and public-source observations from 2026-10-19; photographic research and metadata from 2026-10-20.
- `scripts/chengdu_slides/`: validation, evidence gate, deterministic renderer, illustration and font tooling.
- `deck.css` / `deck.js`: presentation styling/navigation, inlined by the renderer.
- `tests/chengdu_slides/`: Python contracts and actual Chromium tests.

Operator/museum notices take precedence over generic guide hours. Jinsha Site Museum is excluded during its announced 2025-12-05–2027-04-30 closure. Numeric secondary-guide budgets/hours retain their caveats; editorial transport/duration suggestions are distinguished from operator facts. Michelin listings do not prove a specific year's award or a numeric RMB price.

## Build and verify

From the repository root:

```sh
python3 -m scripts.chengdu_slides.cli validate --publication
python3 -m scripts.chengdu_slides.cli build
python3 -m scripts.chengdu_slides.cli preview
python3 -m unittest discover -s tests/chengdu_slides -p 'test_*.py' -v
cd tests/chengdu_slides
npm ci
npm exec -- playwright install chromium
npm test
```

The browser test server builds the local preview and an explicitly synthetic navigation fixture, binds only to 127.0.0.1, and shuts down after Playwright. Offline-export tests create actual screenshots and a printable PDF, not placeholder reports; they require Poppler's `pdfunite`/`pdfinfo`, print in bounded batches and verify the merged page count. Synthetic unit/navigation records are never canonical publication inputs. Scoped Jekyll exclusions keep build scripts, tests/dependencies and project verification/spec documents out of the website distribution; they remain version-controlled development sources. Raw research captures, worker reports, build outputs and dependency caches stay ignored; a clean checkout can build the release using checked-in canonical excerpts/assets without private captures.

Preview exports live under ignored `_reports/chengdu-slides/draft/`. The release gate rejects incomplete/unreviewed data, unsafe/missing assets and malformed or untraceable evidence. Do not set editorial flags to bypass real findings.

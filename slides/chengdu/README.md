# Chengdu bilingual travel slides

## Content and release state

The local release contains **15 attractions, 15 distinct restaurant brands and 15 gift types**, with **306 illustrated pages**. Every Thai page is immediately followed by its simplified-Chinese counterpart. Dense units split at the same bullet boundaries in both languages; content is not dropped or shrunk to force a slide to fit.

`index.html` and `manifest.json` are generated release artifacts for `/slides/chengdu/`. The canonical metadata value `published` means editorially approved for release generation; it does **not** by itself prove a GitHub push or a live deployment. Read back the deployed `content_version` to establish that separately. Existing site articles and navigation are unchanged.

## Community-based gift filtering

The user's amended policy is `gift_policy: community_curated` (Route C). It selects experiences from actual Pantip/public discussions, with both buying reasons and conflicting or limiting opinions. It does not require a marketplace API, prove whole-platform absence, or apply a mandatory 30% saving threshold. Strict measured-search/price Routes E/P remain available and unchanged when those claims are actually made.

- Fifteen selected product types are counted once each, not by color, size, tea example, pen model or city variant.
- Ten additional supporting pairs explain lower-priority/avoid examples, including historical Laz/Shopee mentions and tour-shop pressure. They do not inflate the 15 recommendations.
- Every selected observation is attributed, dated or explicitly undated, and bound to a reviewed short excerpt. All observed recommendation/countervoice sources must remain visibly cited somewhere on that gift's pages.
- Partial/indexed content is labeled as such; it is not a recovered full discussion. Multiple comments in one thread do not become independent surveys.
- US/other-overseas availability is not Thai stock evidence. Single-OP questions are not multi-person conclusions. Old prices do not become current quotes. A Shopee review with shop links has an explicit possible-commercial-bias caveat.
- The Bestore walnut-date option is a single dated Chengdu tasting opinion, conditional on labels/allergens/import checks, not a matched current SKU or a China-only claim.
- Personal-use FDA guidance and dated Customs context do not automatically authorize food gifts. No medical efficacy is endorsed.

All 45 entries and 13 supporting units received a complete internal bilingual/source-to-retained-observation review. This was not an independent re-fetch of all sources or certification that opinions, current prices, availability or import conditions are true. Supporting source records retain retrieval and publication context.

## Images and fonts

Every page has an **original conceptual SVG illustration**, visibly identified as not a documentary photograph. They are not photographs of actual dishes, restaurant interiors, exact building appearances or currently available product SKUs. Gift illustrations use appropriate subject motifs, including postcards, seals, textiles, pen, shirt, tote, calligraphy and walnut-stuffed dates.

Local WOFF2 derivatives originate from Kanit, Noto Sans Thai and Noto Serif SC. Original OFL notices remain at `fonts/*_OFL.txt`; derivative family names were changed. The Chinese subset preserves requested supported codepoints from the dataset. `fonts/source-manifest.json` records original and derivative SHA256 values. Regenerating fonts requires the corresponding source TTF cache and verification of those hashes, licenses and derivative-name requirements.

The standalone HTML embeds actual font/image bytes plus full font copyright/license notices in non-executable JSON (`font-license-notices`). It needs no runtime CDN, analytics or network images. `render_standalone(data, site_root)` remains an explicitly labeled preview by default; the opt-in `publication=True` export rechecks publication/asset approval before retaining release labels and all community disclosures.

The fixed-stage foundation comes from the MIT-licensed [frontend-slides](https://github.com/zarazhangrui/frontend-slides) skill at commit `9906a34d640d2111f724544cbc50f7f130569ae1`. Its notice remains at `scripts/chengdu_slides/FRONTEND_SLIDES_LICENSE.txt`.

## Source of truth

- `_data/chengdu_slides/`: canonical bilingual JSON and public-source observations retrieved on 2026-10-19.
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

The browser test server builds the local preview and an explicitly synthetic navigation fixture, binds only to 127.0.0.1, and shuts down after Playwright. Offline-export tests create actual screenshots and a printable PDF, not placeholder reports. Synthetic unit/navigation records are never canonical publication inputs. Scoped Jekyll exclusions keep the new build scripts, tests/dependency directory and project verification/spec documents out of the website distribution; they remain version-controlled development sources. Raw research captures, worker reports, build outputs and dependency caches stay in ignored local directories; a clean checkout can build the release using the checked-in canonical excerpts/assets without those private captures.

Preview exports live under ignored `_reports/chengdu-slides/draft/`. The release gate rejects incomplete/unreviewed data, unsafe/missing assets and malformed or untraceable evidence. Do not set editorial flags to bypass real findings.

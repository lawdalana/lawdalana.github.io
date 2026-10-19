# Chengdu bilingual travel slides — local draft

## Status

This is **not a completed or deployed travel guide**. The sourced draft contains15 attractions and15 distinct restaurant brands, but **zero gifts meet the purchase-evidence gate**. The current generated local preview has166 pages including guide/status pages. Thai pages are immediately followed by corresponding simplified-Chinese pages. Long units are split at identical bullet boundaries in both languages; no content is dropped to force a slide to fit.

There is intentionally no published `index.html` in this directory yet. Preview artifacts live only in the git-ignored `_reports/chengdu-slides/draft/` directory. No existing site article or navigation has been changed.

## Images and fonts

Every draft page has an **original conceptual SVG illustration**, visibly identified as not a documentary photograph. The Commons image metadata probe did not produce usable local photo downloads; illustrations must not be represented as photos of actual dishes, restaurant interiors or exact building appearances.

Local WOFF2 derivatives originate from Kanit, Noto Sans Thai and Noto Serif SC. Original OFL notices are retained in `fonts/*_OFL.txt`; derivative family names were changed. The Chinese subset preserves requested supported codepoints from the current dataset. The standalone draft embeds the actual font/image bytes and the full font copyright/license notices as non-executable JSON (`font-license-notices`); it requires no runtime network requests, analytics or CDN.

The fixed-stage foundation comes from the MIT-licensed [frontend-slides](https://github.com/zarazhangrui/frontend-slides) skill at commit`9906a34d640d2111f724544cbc50f7f130569ae1`. Its notice is retained at `scripts/chengdu_slides/FRONTEND_SLIDES_LICENSE.txt`.

## Actual source of truth

- `_data/chengdu_slides/`: canonical JSON files; public-source observations are dated2026-10-19.
- `scripts/chengdu_slides/`: validation, evidence gate, deterministic renderer, illustration and font tooling.
- `deck.css` / `deck.js`: editable presentation styling and navigation, inlined by the renderer.
- `tests/chengdu_slides/`: Python contracts/evidence/asset/render tests and real Chromium tests.

Operator/museum notices take precedence over generic guide hours. Jinsha Site Museum is excluded during its announced2025-12-05–2027-04-30 closure. Secondary numeric budgets/hours and editorial transport/duration suggestions retain their original caveats. Michelin listings are not treated as evidence of a specific year's award or a numeric RMB price.

## Run and verify

From the repository root:

```sh
python3 -m scripts.chengdu_slides.cli validate
python3 -m scripts.chengdu_slides.cli preview
python3 -m scripts.chengdu_slides.testing
python3 -m unittest discover -s tests/chengdu_slides -p 'test_*.py' -v
cd tests/chengdu_slides
npm ci
npm exec -- playwright install chromium
npm test
```

Browser tests expect the generated local preview and an explicitly synthetic navigation fixture. The test web server binds only to127.0.0.1 and is shut down by Playwright. The offline-export test creates actual standalone-preview screenshots and a printable PDF; the synthetic unit/navigation records are never publication inputs.

Local deliverables:

- `_reports/chengdu-slides/draft/Chengdu_Thai_Chinese_Draft.html`: fully self-contained offline draft.
- `_reports/chengdu-slides/draft/Chengdu_Thai_Chinese_Draft.pdf`: actual browser-printed draft, not a screenshot placeholder.

`python3 -m scripts.chengdu_slides.cli validate --publication` and the release `build` must fail in the current state. Do not set records to`editorial_ready` or metadata to`published` merely to bypass those findings.

## Unresolved release criteria

- At least15 gift records need exact-product current purchase evidence and either usable bounded Shopee-search observations or a like-for-like China/Thailand saving of at least30% after documented relevant costs. An inaccessible/empty rendered search is not evidence of absence. Reference/launch prices, unavailable stock and unknown fees do not become current available offers.
- Attraction/restaurant records remain`sourced_draft` pending full editorial and bilingual review. A few direct source rechecks and structural tests do not amount to an independent audit of every statement.
- Final generated public route, production Jekyll integration, public deployment and live content-version read-back remain undone. A local build/test result is not proof of online publication.

# Chengdu photographic refresh — local verification

Date: 2026-10-20

## Release identity

- Route: `/slides/chengdu/`
- Content version: `f18a5c2c3ba12292`
- Canonical entries: 15 attractions, 15 restaurant brands, 15 gift types.
- Output: 442 pages, adjacent Thai/simplified-Chinese pairs; 201 entry units and 20 supporting units.
- Visuals: 51 actual source photographs, stored locally with full title/credit/license/source/modification records. No canonical slide uses the preceding conceptual SVGs.
- All original entry bodies, facts, identity and purchase evidence were checked for equality before/after matched two-bullet pagination. No entry information was removed to fit the photographic layout.

## Actual execution

- Publication validation: valid, no findings.
- Python contracts: **88 passed**.
- Chromium deck tests: **14 passed**, including all 442 image decodes/pairs/layout bounds, desktop/mobile/no-JavaScript, tablet detail columns, natural reading scroll, collapsed mobile toolbar, keyboard/touch, denied fullscreen and reduced-motion language changes.
- Shared site menu regression: **13 passed**; measured menu-controller Chromium line coverage **82.9% (116/140)**. This is menu coverage, not a claim about all deck code.
- Latent Lab regression: **10 passed**.
- Direct production Jekyll Docker build: passed. Build tooling, tests and ignored reports remain outside the website distribution.
- All three derivative font hashes match their checked-in source manifest.
- Default standalone preview: actual embedded image/font bytes and full non-executable font/photo rights notices. Real offline execution passed with no HTTP(S) requests.
- Real draft PDF: **442 pages**, verified with `pdfinfo`; photos are re-encoded from the real decoded sources to bounded JPEGs for printing, then printed in batches and merged with Poppler. This avoids WebP/filter lossless-raster expansion; it does not substitute generated pictures.
- Release portable bundle: CRC verification passed; actual `file://` offline browser decoded all 442 images, loaded all three fonts, retained release labels and made no HTTP(S) requests. The ZIP has 62 files and two directory entries.

The shared menu/Latent checks reused the deck's installed Playwright through `NODE_PATH` plus the isolated shared test dependencies. The shared runner's separate default browser revision was not installed; this environmental mismatch was not reported as a site regression.

## Reviews and corrections

- Source-photo editors checked retained metadata and visible subjects. False matches were rejected, including the contemporary-art/science museums for Chengdu Museum, unrelated meals/objects and rendered avatars. Dish/product/cultural/ingredient examples explicitly do not certify restaurant provenance, exact SKU, authentic workshop, current display or stock.
- A bounded code review timed out after identifying concrete findings. A narrow follow-up reported all three resolved in inspected source: photo gates cannot be bypassed by removing the edition flag; standalone and preview notices are retained; details-layout overrides survive no-JavaScript/tablet/phone rendering. New negative/export and tablet geometry tests exercise these boundaries. The follow-up used synthetic probes and is not a substitute for the real execution above.
- Visual follow-up inspected five actual release screenshots: Thai cover, attractions opener, Thai restaurant entry, Chinese restaurant opener and mobile reading. No remaining Critical/Important defect was reported in those samples. This is **not** a manual visual review of every page.

## Rights, scope and deployment

Image licenses are explicit Commons/Openverse-Flickr catalog statements, not an independent certification of underlying ownership. `slides/chengdu/images/PHOTO_CREDITS.md` maps every included photograph to its attribution, source, stated license, retrieval date and changes. Historical/undated photos are not present-day stock or venue evidence. Community gift opinions, uncertainty and countervoices remain visible.

Raw captures, worker logs, download originals, dependencies, ZIP/PDF exports and private research ledgers are ignored and are not publication inputs. Legacy synthetic test/illustration tools are not canonical consumer data.

This report establishes local verification. A push is not deployment proof: rollout must separately verify the exact remote commit, actual Pages build/deployment and anonymous live `content_version`, image/font loading and navigation. The manifest is the content-identity readback target.

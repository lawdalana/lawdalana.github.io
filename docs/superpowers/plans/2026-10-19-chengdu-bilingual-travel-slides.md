# Chengdu Bilingual Travel Slides Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a sourced, illustrated Thai–Chinese Chengdu travel presentation at `/slides/chengdu/`, with 15 attractions, 15 restaurants, 15 qualifying gifts, and verified public deployment after explicit publishing approval.

**Architecture:** Keep the existing Jekyll garden intact and add a standalone static presentation generated from a canonical bilingual dataset. Separate evidence validation, rendering, deck-local interaction/styles, and browser/site checks. Publish no backend, analytics, external slideshow embed, or runtime CDN dependency.

**Tech Stack:** Python standard library for content validation/rendering and unit tests; semantic HTML, CSS, and vanilla JavaScript; Node.js with a pinned Playwright development dependency for Chromium checks; the existing locked Jekyll dependencies for production verification. Python 3.13.14, Node v22.23.3, npm, and a working Docker daemon were observed locally during planning; host Ruby/Bundler were not found.

**Spec:** `docs/superpowers/specs/2026-10-19-chengdu-bilingual-travel-slides-design.md`

**Review status:** The user's instruction to continue after the attached written spec is taken as approval to prepare this plan. Implementation still waits for this plan's review and an execution-method choice. Nothing in this plan authorizes a public push.

## Global Constraints

- Destination: **Chengdu and nearby excursions in Sichuan**; no personal departure date, group size, dietary requirement, or bookings are supplied.
- Target: **15 distinct attractions**, **15 distinct restaurants**, and **15 distinct gifts** meeting the purchase-evidence criterion; the original absolute floor is more than 10 per category. Do not reduce the agreed target without a scope decision.
- Base presentation: **45 items and 180 core slides**, arranged as introduction `th → zh-Hans`, then practical details `th → zh-Hans`. Add complete pairs when necessary for readability.
- Price-route threshold: **30% below the comparable Thai purchase price**; same authentic product, size, quantity, material/grade, and edition.
- A blocked Shopee check is **not evidence of absence**. Use only bounded, dated claims based on actual accessible searches.
- Jinsha closure: **2025-12-05 through 2027-04-30**. Do not count it as an open attraction as of the initial research date or assume reopening without a new official check.
- **Every slide—including supporting and reference slides—must include a meaningful visual.** A logo or decorative icon alone is insufficient.
- Keep images, required fonts, CSS, and JavaScript local. Preserve image/font rights and attribution. No invented documentary photos, product prices, search results, or restaurant visits.
- Preserve exact Chinese names, SKUs, product values, and qualifications. Pair translations must convey the same facts and warnings.
- Test viewports: **1920×1080, 1366×768, 768×1024, 390×844, and 360×800**. Split dense content into additional pairs rather than clip or make text illegible.
- New persistent project code stays in this existing repository. Knowledge-vault research stays outside the public source tree; capture useful Internet findings and retained Internet images there under the workspace's naming/source rules.
- The repository is **PUBLIC**. Immediately before pushing, identify the exact public file set and target `lawdalana/lawdalana.github.io`, then obtain explicit confirmation. Verify the remote commit and exact online content afterward.

## Review Focus

1. **Blocked searches and old catalogues:** a login wall, inaccessible search, or historical museum listing must never qualify a gift or imply current pickup availability. Pin with Task 1 evidence tests and Task 3 real-record checks.
2. **Plausible but inconsistent translations:** Thai and Chinese can look complete while changing a price, branch, date, warning, or meaning. Pin shared fact-token/pair checks in Task 5 and require a semantic bilingual review in Task 9.
3. **Unsafe or misleading asset references:** Unicode filenames, path traversal, hotlinks, missing licenses, or a generic food image mislabeled as the exact restaurant must not enter the public deck. Pin with Task 4 asset tests.
4. **Malformed deep links and interrupted interaction:** an unknown hash, editable-field focus, denied fullscreen, or cancelled touch gesture must leave normal navigation usable. Pin with Task 6 browser tests.
5. **Dense mobile text and delayed fonts/images:** layout must remain readable after actual Thai/CJK fonts and images load, not only before them. Pin all-slide geometry/load tests in Task 7, then repeat against Jekyll output in Task 8.

## File and data contracts

All paths below are repository-relative. Keep each Python module focused; do not add a framework or change existing article templates.

- `_data/chengdu_slides/meta.json`: bilingual title, research date, target `15`, saving threshold decimal string `"30"`, and editorial disclosure.
- `_data/chengdu_slides/sources.json`: source records keyed by stable ID; canonical URL, publisher, tier, retrieval date, supported facts, access state, and explicit human review state.
- `_data/chengdu_slides/{attractions,restaurants,gifts}.json`: distinct editorial item arrays; exact names, identity key, geographic classification/branch/SKU, canonical facts, observation dates, source IDs, and bilingual content units. Gifts also carry structured purchase evidence.
- `_data/chengdu_slides/support.json`: paired cover, usage, category navigation, closure warning, suggested-route, and reference/credit content units; never counted as items.
- `_data/chengdu_slides/assets.json`: local image/font paths, subject/type, source URL, creator, license/permission URL, modifications, dimensions where relevant, and illustration disclosure.
- `scripts/chengdu_slides/`: `__init__.py`, `model.py`, `evidence.py`, `validation.py`, `asset_validation.py`, `render.py`, `cli.py`, and `Jekyll.Dockerfile`.
- `slides/chengdu/`: generated `index.html` and `manifest.json`, authored `deck.css` and `deck.js`, plus cleared `images/` and `fonts/` assets and applicable license files.
- `tests/chengdu_slides/`: standard-library tests/explicitly synthetic fixtures, Playwright package/lock/config, and browser tests. Test fixtures are never travel evidence and must never be copied to the public deck.
- `_notes/Public/Other/Chengdu-Travel-Slides.md`: one new garden entry linking to the presentation, using the existing six-field frontmatter convention.
- `_reports/chengdu-slides/`: ignored local reports, screenshots, source audit, and review output. No unrelated vault files or personalized browser captures enter Git.

`model.load_dataset(data_dir: Path) -> dict` joins the named JSON files: `meta` is a dictionary; `sources`, `assets`, `attractions`, `restaurants`, `gifts`, and `support` are arrays of dictionaries. Source and asset IDs are globally unique. Items have at least two content units: `intro` and `details`; each unit has a stable ID, bilingual title/body, shared `fact_ids`, shared `source_ids`, a meaningful `asset_id`, and bilingual alt text. Additional units must be complete language pairs. Test helpers define `ROOT = Path(__file__).resolve().parents[2]` and `DATA_DIR = ROOT / "_data" / "chengdu_slides"` in `tests/chengdu_slides/fixtures.py`; tests import these rather than inventing alternate locations.

Body text is plain structured text, not trusted raw HTML. Named fact tokens in corresponding language blocks must match and resolve from the same canonical factual values. Human translation review is still mandatory: token equality alone does not prove semantic equivalence.

Common validation findings have `code`, `path`, and `message` string fields. `validation.validate_category(data: dict, category: str) -> list[dict]` checks that category's identity, content, evidence, references, and target, without checking on-disk assets. `validation.validate_dataset(data: dict, *, publication: bool = False) -> list[dict]` validates the full joined contract; publication mode requires all targets, editorial-ready records, paired supporting material, and all reference/asset mappings. Build/release commands always use publication mode; unit fixtures may use the nonpublication mode.

`evidence.evaluate_gift(item: dict, sources: dict[str, dict], minimum_saving: Decimal) -> dict` returns `qualified: bool`, `route: str | None`, `saving_percent: Decimal | None`, and `reasons: list[str]`. It computes eligibility from the evidence rather than trusting a manually set qualified flag.

`evidence.calculate_saving(china_cny: str, thb_per_cny: str, thai_thb: str, *, china_fees_thb: str = "0", thai_delivery_thb: str = "0") -> Decimal` uses Decimal arithmetic. China cost is the converted China price plus documented China-side fees; Thai comparison cost includes documented Thai delivery. Positive prices/rate and nonnegative fees are required. Compare the unrounded percentage to the threshold; round for display only.

## Execution order and stopping rules

Tasks 1–4 resolve the evidence and asset feasibility before investing in the full presentation UI. Tasks 5–8 produce and exercise the actual site artifact. Task 9 performs independent review and the separate publication gate.

Execute inline/native unless the user chooses subagent-driven execution. If workers are used, serialize edits to shared source/asset datasets and review each task's interfaces before the next task. Do not assume a delegate tool exists; use actual available worker tooling or report its absence honestly.

### Task 1: Make the content and gift-evidence contracts executable

**Files:** Create `scripts/chengdu_slides/{__init__,model,evidence,validation}.py`, `tests/chengdu_slides/{fixtures,test_contract,test_evidence}.py`, and the initially incomplete JSON dataset files listed above.

**Interfaces:** Consumes the written spec and the data contracts above. Produces `load_dataset`, `validate_category`, `validate_dataset`, `evaluate_gift`, and `calculate_saving` with exactly those signatures. Fixture helpers `sample_dataset() -> dict`, `sample_price_evidence() -> tuple[dict, dict[str, dict]]`, and `sample_absence_evidence() -> tuple[dict, dict[str, dict]]` live only in `tests/chengdu_slides/fixtures.py` and explicitly identify their records as synthetic. The price/absence helpers each return otherwise complete, qualifying evidence for their respective route, so a rejection test can isolate the one condition it changes.

- [ ] **Step 1:** At execution start, load the selected execution skill and `superpowers:test-driven-development`. Load the requested `frontend-slides` instructions and required references from the verified `zarazhangrui/frontend-slides` source before product implementation; record the actual source revision and license locally. Inspect relevant repository instructions. Resolve any material skill/spec conflict with the user instead of silently dropping requirements.
- [ ] **Step 2:** Write contract/evidence tests, including these assertions and separate tests for missing sources, duplicate IDs/identity keys, unreviewed facts, invalid dates, mismatched SKU/size/grade, unknown stock/channel access, zero/negative/nonfinite prices or rates, and negative/nonfinite fees:

```python
def test_price_threshold_uses_unrounded_decimal():
    assert calculate_saving("70", "5", "500") == Decimal("30")
    assert calculate_saving("70.001", "5", "500") < Decimal("30")

def test_blocked_search_never_qualifies():
    item, sources = sample_absence_evidence()
    assert evaluate_gift(item, sources, Decimal("30"))["qualified"] is True
    item["purchase_evidence"]["searches"][0]["access_state"] = "blocked"
    assert evaluate_gift(item, sources, Decimal("30"))["qualified"] is False
```

The numbers above are computed synthetic boundary fixtures, not observed product prices. Add `test_closed_pickup_without_verified_alternative_is_rejected`, `test_claimed_qualified_flag_does_not_override_evidence`, and `test_price_route_applies_threshold_after_costs_unrounded`. The last test must assert qualification at exactly 30%, rejection just below it, and rejection when documented fees bring an otherwise qualifying offer below the threshold.
- [ ] **Step 3:** Run `python3 -m unittest discover -s tests/chengdu_slides -p 'test_*.py' -v`; expect import/function failures before implementing the modules. Record the actual failure, not a planned output.
- [ ] **Step 4:** Implement the declared interfaces. Route E requires complete, bounded, dated actual search observations, no exact matching product found in the checked boundary, and a verified accessible China channel. Route P requires like-for-like reviewed offers, stock/channel evidence, a sourced dated currency rate, disclosed costs/exclusions, and saving at least `Decimal("30")`. Incomplete/challenged retrieval remains incomplete.
- [ ] **Step 5:** Run the same unit command; require all contract/evidence tests to pass while the incomplete real dataset remains ineligible for publication.
- [ ] **Step 6:** Commit only this task's code/tests/contract files as `feat: validate Chengdu slide content and gift evidence`.

### Task 2: Curate the attraction and restaurant content, not just name lists

**Files:** Populate `_data/chengdu_slides/{meta,sources,attractions,restaurants}.json`; create `tests/chengdu_slides/test_editorial.py`. Update the external topical Obsidian source note as research proceeds.

**Interfaces:** Consumes `load_dataset` and `validate_category`. Produces 15 reviewed attraction records and 15 reviewed restaurant records with complete Thai/Chinese introduction/details units, canonical factual tokens, relevant source IDs, and stable intended image IDs. Actual image files and rights are handled by Task 4.

- [ ] **Step 1:** Write `test_attractions_are_distinct_and_editorial_ready` and `test_restaurants_have_specific_verified_branches`:

```python
def test_attractions_are_distinct_and_editorial_ready():
    data = load_dataset(DATA_DIR)
    assert len(data["attractions"]) >= 15
    assert validate_category(data, "attractions") == []

def test_restaurants_have_specific_verified_branches():
    data = load_dataset(DATA_DIR)
    assert len(data["restaurants"]) >= 15
    assert validate_category(data, "restaurants") == []
```

Add `test_jinsha_is_not_counted_as_open_without_reopening_evidence`, `test_restaurant_branch_does_not_multiply_brand_count`, and tests for the required practical-detail fields from spec section 3.
- [ ] **Step 2:** Run `python3 -m unittest discover -s tests/chengdu_slides -p test_editorial.py -v`; the incomplete real lists must fail.
- [ ] **Step 3:** Resolve the existing discovery candidates through official sources where available. Research the actual branch/access details, prices and observation dates, reservation rules, ingredients/cautions, and geography. Write full equivalent Thai/Chinese text; clearly mark editorial budgets/durations and estimates. Replace closed/unverifiable candidates. Do not claim old article hours are live confirmation or a Michelin list proves an award edition.
- [ ] **Step 4:** Run the editorial tests and contract/evidence suite. Manually audit each record against its references and record unresolved disputes outside the publication-ready set. Require both category validators to return no findings.
- [ ] **Step 5:** Commit only the curated category/source updates and their tests as `content: research Chengdu attractions and restaurants bilingually`.

### Task 3: Qualify 15 gifts with actual purchase evidence and import guidance

**Files:** Populate `_data/chengdu_slides/gifts.json`, append relevant sources to `sources.json`; create `tests/chengdu_slides/test_gift_dataset.py`. Retain query/cost observations and useful research in the external knowledge vault.

**Interfaces:** Consumes `evaluate_gift`, `calculate_saving`, and `validate_category`. Produces 15 distinct editorial-ready gifts satisfying Route E or P, with exact item identity, accessible buying channel, dated price, caveats, full Thai/Chinese text, and evidence references. Historical catalogue existence alone is insufficient.

- [ ] **Step 1:** Write the real-dataset acceptance test:

```python
def test_every_gift_passes_a_purchase_evidence_route():
    data = load_dataset(DATA_DIR)
    sources = {row["id"]: row for row in data["sources"]}
    assert len(data["gifts"]) >= 15
    assert validate_category(data, "gifts") == []
    for item in data["gifts"]:
        assert evaluate_gift(item, sources, Decimal("30"))["qualified"]
```

Add `test_gift_cosmetic_variants_are_not_separate_items` and `test_food_and_controlled_goods_have_relevant_thai_import_sources`. Route E record tests must assert recorded query URLs/terms, date, actual accessible boundary, and qualified wording; Route P tests must assert exact comparability and dated costs/rate.
- [ ] **Step 2:** Run `python3 -m unittest discover -s tests/chengdu_slides -p test_gift_dataset.py -v`; initial unqualified discovery records must fail.
- [ ] **Step 3:** Research actual channels, products, Shopee checks or like-for-like China/Thailand prices, and official Thai customs/quarantine/carriage guidance. Use accessible public interfaces without bypassing controls. Broaden candidate discovery beyond the initial Jinsha-heavy list if needed; keep every recommendation genuinely purchasable through its stated channel. Compute every saving with the shared function and disclose model/material, warranty/region, fees, stock, and carriage limitations where relevant.
- [ ] **Step 4:** Run the gift and evidence tests and independently trace each factual assertion to its retained observation. If sufficient gifts cannot pass after real research, stop this task and report the precise evidence blocker for a scope decision; do not proceed as though the 15-gift criterion passed or publish filler.
- [ ] **Step 5:** Only when the gate passes, commit the real gift/source records and tests as `content: verify Chengdu gift purchase evidence`.

### Task 4: Clear and prepare meaningful local visuals and fonts

**Files:** Populate `_data/chengdu_slides/assets.json`; create `slides/chengdu/images/`, `slides/chengdu/fonts/`, applicable license files, `scripts/chengdu_slides/asset_validation.py`, and `tests/chengdu_slides/test_assets.py`. Assign cleared assets to all item/support units; create `support.json` content here.

**Interfaces:** Consumes the reviewed datasets and intended image IDs. Produces `asset_validation.validate_assets(data: dict, site_root: Path) -> list[dict]` and complete local asset/rights records. A shared visual is allowed within a language pair; decorative icons do not count as meaningful subject visuals.

- [ ] **Step 1:** Write `test_all_content_units_have_local_meaningful_cleared_visuals`, `test_asset_paths_cannot_escape_deck_or_hotlink`, `test_fonts_have_local_files_and_license_records`, and `test_generic_dish_photo_requires_illustration_disclosure`. Assert the validator reports findings for missing files/licenses, `../`/absolute/path-traversal paths, external image/CSS font URLs, mismatched subject claims, and logo-only units.
- [ ] **Step 2:** Run `python3 -m unittest discover -s tests/chengdu_slides -p test_assets.py -v`; missing assets and validator implementation must fail.
- [ ] **Step 3:** Implement `validate_assets`. Obtain rights-cleared subject photos with exact creator/license/modification credits, or create clearly labeled original diagrams from sourced facts. Retained Internet images first go to the prescribed knowledge-vault image directory; copy only cleared optimized publication assets into the project. Download and license local Thai/CJK fonts; verify coverage rather than silently falling back to missing glyphs. Do not republish extracted commercial photographs without permission.
- [ ] **Step 4:** Create supporting bilingual units, including the current Jinsha warning, how to use the presentation, geographic route suggestions labeled editorial, and credits guidance. Ensure every support unit has a meaningful visual too. Run asset and all prior tests; require `validate_assets(data, ROOT) == []`.
- [ ] **Step 5:** Commit only cleared assets, licenses, manifests, support text, and related validator/tests as `feat: add cleared local visuals for Chengdu slides`.

### Task 5: Generate deterministic semantic HTML with exact language pairing

**Files:** Create `scripts/chengdu_slides/{render,cli}.py`, `tests/chengdu_slides/test_render.py`, generated `slides/chengdu/{index.html,manifest.json}`.

**Interfaces:** Consumes the complete validated dataset and `validate_assets`. Produces `render.render_deck(data: dict) -> str`, `render.build_deck(data_dir: Path, site_root: Path) -> dict`, and CLI commands `python3 -m scripts.chengdu_slides.cli validate`, `build`, and `build --check`. Build uses publication validation, writes only the deck HTML/manifest, and returns actual category/item/slide counts plus a deterministic `content_version` derived from canonical input and asset content hashes. Check mode compares expected generated output without rewriting it and exits nonzero on drift.

- [ ] **Step 1:** Write `test_render_is_deterministic`, `test_all_pairs_are_adjacent_th_then_zh_hans`, `test_pair_fact_tokens_must_match_and_resolve`, `test_body_text_is_escaped_not_executable_html`, `test_support_slides_are_not_item_counts`, `test_no_javascript_still_exposes_content`, and `test_release_build_rejects_incomplete_or_unqualified_data`.

```python
def test_all_pairs_are_adjacent_th_then_zh_hans():
    slides = parse_slides(render_deck(sample_dataset()))
    assert len(slides) % 2 == 0
    for th, zh in zip(slides[0::2], slides[1::2]):
        assert (th["lang"], zh["lang"]) == ("th", "zh-Hans")
        assert th["pair_id"] == zh["pair_id"]
        assert th["fact_ids"] == zh["fact_ids"]
        assert th["source_ids"] == zh["source_ids"]
```

`parse_slides(html: str) -> list[dict]` is a test helper using the standard-library HTML parser, not a second production renderer.
- [ ] **Step 2:** Run `python3 -m unittest discover -s tests/chengdu_slides -p test_render.py -v`; verify real preimplementation failures.
- [ ] **Step 3:** Implement the declared functions/CLI. Render semantic sections with `data-slide-id`, `data-pair-id`, `data-lang`, `data-item-id`, `data-kind`, and factual/source metadata. Use UTF-8, escaped plain text, language-specific alt text, readable source/credit links, a table of contents, and visible control markup. Embed the exact `content_version` in both HTML metadata and manifest. Without JavaScript, show sequential readable sections rather than a blank deck.
- [ ] **Step 4:** Run unit tests, `python3 -m scripts.chengdu_slides.cli validate`, `python3 -m scripts.chengdu_slides.cli build`, and `python3 -m scripts.chengdu_slides.cli build --check`; all must exit zero with actual counts at or above the accepted targets and at least 180 item slides. Rebuild and require unchanged output.
- [ ] **Step 5:** Commit the renderer, CLI, tests, and actual generated deck as `feat: generate paired Thai Chinese travel presentation`.

### Task 6: Implement accessible progressive deck controls

**Files:** Create `slides/chengdu/deck.js`, `tests/chengdu_slides/{package.json,package-lock.json,playwright.config.mjs,navigation.spec.mjs}`; add only scoped development/report ignores to `.gitignore`.

**Interfaces:** Consumes Task 5's data attributes and controls. Produces initialization after DOM readiness, valid `#slide=<slide-id>` navigation, visible previous/next/progress/contents, pair-language jumps, safe keyboard/touch behavior, and graceful fullscreen fallback. Invalid hashes select the first slide. Do not expose application state as a required global API just for tests.

- [ ] **Step 1:** Prepare the locked Playwright development package: discover and pin the actual available `@playwright/test` version with npm during execution, retain the exact lockfile, and install Chromium. Add scoped ignores for its `node_modules/`, `test-results/`, `playwright-report/`, and `_reports/chengdu-slides/`.
- [ ] **Step 2:** Write navigation browser tests and their server configuration. Playwright must own a localhost-only Python HTTP server with `CHENGDU_SITE_ROOT` selecting repository output or `_site` and stop it with the test runner. Tests cover next/back, TOC deep links, pair jump preserving item/unit, first/last bounds, back/forward history, malformed/unknown hash, JavaScript-disabled readability, and keyboard focus. Specifically test `editable_focus_does_not_advance`, `denied_fullscreen_keeps_navigation_working`, and `cancelled_or_vertical_touch_does_not_change_slide`.
- [ ] **Step 3:** From the repository root, run `(cd tests/chengdu_slides && npm exec -- playwright test --config playwright.config.mjs navigation.spec.mjs)` and record actual initial failures with controls present but inert.
- [ ] **Step 4:** Implement `deck.js` against those contracts. Mark enhancement only after successful initialization; maintain meaningful document language, focus visibility, current-slide labels, and progress without focus traps. Never intercept text-editing keys or activate a navigation gesture originating on a link/button/control. Treat fullscreen as optional and catch promise rejection.
- [ ] **Step 5:** Run the same browser command; require all navigation tests to pass, no unexpected browser errors, and no runtime third-party resource requests.
- [ ] **Step 6:** Commit navigation code, locked dev tooling, scoped ignores, and tests as `feat: add accessible Chengdu presentation controls`.

### Task 7: Apply the approved visual system and test every slide at every viewport

**Files:** Create `slides/chengdu/deck.css`, `tests/chengdu_slides/layout.spec.mjs`; adjust only deck content-unit splits/assets and regenerate output when required. Store screenshots/reports under `_reports/chengdu-slides/`.

**Interfaces:** Consumes Task 5 markup and Task 6 navigation. Produces cream/jade/vermilion deck styling scoped to this route, local font faces, reduced-motion handling, visible focus, and all-slide responsive geometry checks. Core data and content-version contract remain unchanged.

- [ ] **Step 1:** Write `all_slides_fit_after_fonts_and_images_load` across the exact five specified viewports. Visit every slide through its real hash/control path, wait for `document.fonts.ready` and active meaningful image decode, then assert positive rendered image dimensions, no horizontal overflow, no clipped text/control geometry, and minimum body text size of 16 CSS px. Add `late_image_and_font_loading_does_not_break_layout`, `reduced_motion_is_respected`, and `no_runtime_cdn_or_tracker_requests`.
- [ ] **Step 2:** Run the new layout tests against the unstyled/partially styled deck; record actual failures.
- [ ] **Step 3:** Implement scoped `deck.css` using the frontend-slides workflow loaded at execution start. Preserve legibility and the visual hierarchy in the accepted design. Where dense content cannot fit, split the content unit into additional complete bilingual pairs and regenerate—never hide content or reduce text below the stated minimum merely to make a geometry test pass.
- [ ] **Step 4:** Run all browser/unit/content/asset checks and capture representative cover, attraction, restaurant, gift, dense Thai/Chinese, source/credit, and phone screenshots; require all automated checks to pass.
- [ ] **Step 5:** Inspect the captured screenshots through an actually available visual-review method. Explicitly review Thai combining marks and CJK glyphs; geometry alone is not visual approval. If screenshot inspection cannot be performed, report that limitation and obtain review rather than claiming it happened.
- [ ] **Step 6:** Commit styling, legitimate content splits, and test changes as `style: build responsive illustrated Chengdu slide layouts`. Keep generated screenshots/reports ignored, not publicly published by default.

### Task 8: Integrate the garden link and verify a real production Jekyll build

**Files:** Create `_notes/Public/Other/Chengdu-Travel-Slides.md`, `scripts/chengdu_slides/Jekyll.Dockerfile`, `tests/chengdu_slides/test_site_integration.py`; narrowly modify `_config.yml` to exclude `docs/superpowers`, `scripts/chengdu_slides`, and `tests/chengdu_slides` from the built site. Preserve all existing configuration. The raw repository remains public even for build-excluded files.

**Interfaces:** Consumes the actual generated deck and existing `scripts/validate_frontmatter.py` function `check_frontmatter(file_path)`. Produces a valid discoverable garden note and a verified `_site/slides/chengdu/index.html` whose content version/assets/pairs match the generated deck after the site's real plugins/minifier run.

- [ ] **Step 1:** Write `test_garden_entry_has_required_frontmatter_and_exact_deck_link`, `test_build_excludes_only_new_development_paths`, and production-output assertions for the exact route, local assets, item/pair counts, and matching `content_version`. Use `check_frontmatter` on the new note explicitly; the existing whole-repo validator prints failures without necessarily exiting nonzero, so its exit code alone is not a pass.
- [ ] **Step 2:** Run `python3 -m unittest discover -s tests/chengdu_slides -p test_site_integration.py -v`; missing note/config/build output must fail. Capture the existing frontmatter report as a baseline before judging unrelated existing notes.
- [ ] **Step 3:** Implement the new note with `title`, `notetype: feed`, ISO `date`/`last_modified`, tags, and `status: published`. Add only the specified exclusions. Create the isolated build Dockerfile using `ruby:3.3-bookworm`, container-local Node.js for ExecJS, Bundler **2.6.9** from the existing lockfile, and the unchanged repository Gemfile/Gemfile.lock. Do not restart the existing Compose service, alter the host Ruby setup, or blindly update locked gems.
- [ ] **Step 4:** Build from an explicit minimal context and run as the current user:

```bash
tar -czf - Gemfile Gemfile.lock scripts/chengdu_slides/Jekyll.Dockerfile | docker build -t chengdu-slides-jekyll:local -f scripts/chengdu_slides/Jekyll.Dockerfile -
docker run --rm --user "$(id -u):$(id -g)" -e JEKYLL_ENV=production -v "$PWD":/app -w /app chengdu-slides-jekyll:local bundle exec jekyll build --trace
```

Require actual zero exit and generated output; `scripts/build.sh` prints a success message even without fail-fast shell handling, so do not rely on that message. If dependency compatibility blocks the real path, record the failure and try a compatible isolated build route without silently dropping plugins or substituting a plain HTTP server for Jekyll verification.
- [ ] **Step 5:** Run all integration tests against `_site`, rerun the browser suite with `CHENGDU_SITE_ROOT=_site`, run `python3 scripts/validate_frontmatter.py`, compare the baseline/new-note results, and run `git diff --check`. Require unchanged existing configuration outside the explicit exclusions and no external deck asset requests. Commit the note, scoped build/config changes, and integration tests as `feat: integrate and verify Chengdu slides on Jekyll`.

### Task 9: Independent whole-branch review, explicit public gate, and verified deployment

**Files:** No new public files by default. Store actual review/test/release reports under ignored `_reports/chengdu-slides/`; fix only in-scope implementation/content defects with their regression tests.

**Interfaces:** Consumes the reviewed spec/plan, final diff, actual test reports, source evidence, asset rights, screenshots, and `manifest.json.content_version`. Produces a verified final commit and public URL only after all acceptance criteria and publication approval pass.

- [ ] **Step 1:** Run all unit/content/asset/generation checks, the production build, and browser tests. Save actual commands/results and programmatically derived category/item/slide totals. Confirm all published gifts still pass their evidence routes and that no placeholder, synthetic fixture, secret, private note, or uncleared asset entered the publication set.
- [ ] **Step 2:** Obtain a fresh read-only whole-branch review using actual available independent reviewer tooling; provide the spec, this plan, diff/base commit, sources, rights manifest, and test/screenshot outputs. Require semantic Thai/Chinese equivalence review, factual source tracing, price/availability reasoning, and runtime/accessibility checks. Never label the implementer's own check as independent. If the selected review method is unavailable, use an actually available separate-context alternative or report the blocker. Fix findings with regression tests and rerun affected/full checks before approval.
- [ ] **Step 3:** Inspect `git diff`, staged paths, and all commits ahead of the actual remote. Present the exact source/data/assets/licenses/garden-note/docs file set and explicitly name `lawdalana/lawdalana.github.io` and `https://lawdalana.github.io/slides/chengdu/` as the public targets. State that Git history/source will be public too. **Stop and wait for the user's explicit publication confirmation.** Earlier continuation/spec/plan approvals do not count for this gate.
- [ ] **Step 4:** After confirmation, create any final release commit and push only the approved scope to the existing branch without changing visibility. Read the remote back with `git ls-remote origin refs/heads/main` and compare its actual hash with local HEAD. If the remote moved, inspect/reconcile safely; never force-push or overwrite unrelated user commits.
- [ ] **Step 5:** Discover the repository's actual Pages mechanism via read-only GitHub metadata, then check the relevant build/deployment state. Retrieve the exact public deck and its assets; compare its embedded `content_version` and manifest with the intended commit, and exercise live navigation/pairing. A stale cached 200 is not successful deployment. Use bounded foreground polling if necessary; if deployment fails or times out, report the actual failure instead of claiming completion. Capture useful remote findings in the external knowledge vault before finishing.
- [ ] **Step 6:** Report the verified online URL, final commit, actual category/slide counts, tests exercised, and genuine remaining limits. The goal is complete only if every named content, image, language, build, Git, and online acceptance criterion is met.

## Self-review and execution handoff

Spec coverage mapping: sections 1–3 → Tasks 2, 3, 5, 7; sections 4–5 → Tasks 1–3 and 9; section 6 → Tasks 1 and 5–6; sections 7–8 → Tasks 5–8; section 9 → Task 4; section 10 → Tasks 1, 3, 5–8; section 11 → Tasks 1–9; section 12 → Task 9 and the approval gates; section 13 → research inputs for Tasks 2–4, not a claim of completed verification.

The five Review Focus risks each have an owning named test/review step above. Function names and data attributes are consistent across producer/consumer tasks. Test outcomes in this plan are acceptance expectations, not reports of execution; only planning/context checks have run so far.

**Recommended execution method: Native.** Most work shares the same evidence records, bilingual content units, and asset manifest, so keeping one implementation context reduces handoff drift. Use a fresh independent whole-branch reviewer before the public gate. Subagent-driven execution is an alternative if the user prefers separate implementer/reviewer contexts per task and accepts the additional coordination/resource cost.

**Next gate:** ask the user to review this file and choose Native or Subagent-driven execution. Do not start product implementation while this review/choice is outstanding.

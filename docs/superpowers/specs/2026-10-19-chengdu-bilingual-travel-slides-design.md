# Chengdu Thai–Chinese illustrated travel slides

- Date: 2026-10-19
- Stage: written design for user review; implementation is not authorized by this document alone.
- Selected approach: A — a standalone static HTML/CSS/JavaScript presentation within the existing Jekyll website.
- Design direction accepted for this stage: the user instructed the agent to continue after the recommended approach and content structure were presented.

## 1. Intended outcome

Produce a detailed, illustrated travel presentation that visitors can open at `https://lawdalana.github.io/slides/chengdu/`. The audience is Thai-speaking travelers and Chinese-speaking readers viewing equivalent content. Every Thai slide is immediately followed by a simplified-Chinese slide with the same substantive content.

The presentation covers places to visit, actual restaurants to eat at, and gifts worth buying locally because a specific product is not found in a documented Shopee Thailand check or because a like-for-like purchase in China is substantially cheaper. It must support practical decisions, not merely provide names and attractive photographs.

The destination is **Chengdu and nearby excursions in Sichuan**, adopted as an explicitly disclosed working assumption when the user asked to resume. No departure date, group size, dietary requirement, or actual personal itinerary has been supplied. Do not invent these. Visit guidance is current as of its recorded research date; sample routes must be labeled suggestions rather than personal bookings.

Success means complete, sourced bilingual content, usable presentation controls, an image on every slide, verified rendering, and—only after publication approval—a verified Git push and working public URL.

## 2. Scope and content volume

The accepted design target is:

- 15 distinct attractions.
- 15 distinct restaurants, not multiple branches counted as separate restaurants.
- 15 distinct gifts that actually satisfy one of the purchase-evidence routes in section 5.

The original request imposes an absolute floor of more than 10 entries per category. For this design, 15 is the delivery target; reducing it requires an explicit scope decision rather than silently treating discovery candidates as finished entries.

Each item receives two content pairs by default:

1. Thai introduction/highlights.
2. Equivalent Chinese introduction/highlights.
3. Thai practical details.
4. Equivalent Chinese practical details.

This yields 45 items and 180 core slides, as calculated during design preparation. Supporting material adds complete Thai–Chinese pairs: cover, how to use the deck, category navigation, date-sensitive travel alerts, suggested geographic groupings/routes, and source/image-credit guidance. Additional content pairs are allowed when needed for readability; do not cram text or count divider pages as researched items.

A product family’s cosmetic variants, the same restaurant’s branches, or adjoining parts of a single attraction must not be split simply to inflate coverage.

## 3. Editorial structure

### Attractions

For each attraction retain:

- Thai title, official Chinese name, and useful search term.
- What makes the visit worthwhile and the specific highlights to look for.
- Location and clear classification: central city, metropolitan outskirts, or intercity excursion.
- Practical access route with sourced stations/entrances where verified; distinguish travel-time estimates from timetables.
- Ticket/reservation method, indicative price with date, applicable conditions, and closure/last-entry rules.
- Suggested visit duration and best part of the day, labeled editorial advice where appropriate.
- Physical demands, weather exposure, crowds, and other material cautions.
- Nearby compatible stops only where the geography supports the pairing.

**Jinsha safeguard:** the official museum homepage states closure from 2025-12-05 through 2027-04-30. As of the initial research date it cannot count as an open attraction. Include a dated warning when useful and select an accessible alternative. A future reopening must be established by a new official check, not assumed from the scheduled end date.

### Restaurants

Recommend identifiable venues, not just food categories. Each record includes:

- Chinese restaurant name, Thai display name, and a specific branch/address that has been checked.
- Why it is included and its food/style, without claiming personal visits or guaranteed quality.
- Signature orders with Chinese menu terms and plain Thai/Chinese explanations.
- Indicative per-person budget, observation date, and what the estimate includes; separate menu evidence from an editorial meal budget.
- Opening/session times, booking/queue practices, and their verification status.
- How to reach the branch and which geographic sightseeing cluster it fits.
- Spice-level ordering phrases and material ingredient cautions. Do not guarantee allergy safety or vegetarian preparation without venue evidence.

A Michelin listing is evidence of the listing observed. It is not automatically evidence of a particular annual edition, star level, current hours, current price, or all branches of the brand. Extract and verify each claimed field separately.

### Gifts

Each included gift must identify an actual product or well-specified craft item, explain why it is worth carrying home, and name an accessible buying channel. Include price/date, authenticity or material checks, size/weight/fragility, shelf life where applicable, and Thai import/carriage cautions supported by relevant official guidance.

Local cultural significance is useful context but does not by itself satisfy the user’s purchase criterion. Generic hot-pot bases, teas, panda merchandise, or museum products do not qualify merely because they originate in Sichuan.

## 4. Sources and evidence lifecycle

Use official attraction/venue/museum/shop sources for operating facts when obtainable. Use authoritative heritage and customs sources for their respective subjects. Commercial travel guides and reputable editorial guides may support discovery, descriptions, and clearly dated indicative information; they are not live stock or booking guarantees.

A canonical research record moves through these states:

`discovered → identity_checked → practical_details_checked → editorial_ready`

Gift records additionally require `purchase_criterion_passed`. An item with missing required evidence remains a research candidate and does not count toward completion.

Retain canonical URLs, retrieval dates, publisher/source tier, the specific facts supported, and conflicts or limitations. Every published item needs directly relevant references that readers can open. Preserve Chinese identifiers and exact model/SKU values from the evidence; do not silently normalize a mismatched product into a comparison.

Useful Internet findings are also captured in the separate Obsidian knowledge vault according to the workspace rules. Private notes, personal travel plans, account data, browser cookies, and authentication material are not copied into the website repository.

Initial research contains 15 discovery candidates in each category, but **no gift has yet passed the purchase-evidence criterion**. These lists are not a finished deck or proof that the final gift target is feasible.

## 5. Gift qualification

At least one route must pass for every included gift.

### Route E — bounded Shopee absence observation

- Identify the exact item/edition or sufficiently specific handmade product.
- Conduct accessible Shopee Thailand searches using the brand, Chinese name, Thai/English variants, and product/SKU terms as relevant.
- Save the checked queries, search URLs, date, and observed result boundary.
- Use wording equivalent to “not found in the checked Shopee Thailand searches on [date].” Never claim permanent, platform-wide nonexistence.
- A search-engine miss, inaccessible search page, CAPTCHA, login wall, or blocked request is an incomplete check—not evidence of absence. Do not bypass access controls.
- Confirm a realistic China purchase channel and separately assess current availability. A historical catalogue does not establish present stock.

### Route P — verified substantial price advantage

- Compare the same authentic product, size, quantity, material/grade, and applicable edition through identifiable China and Thailand sellers.
- Record both offers, stock/offer conditions, currency-rate source/date, shipping/fees included, and any exclusions.
- The proposed editorial threshold for “substantially cheaper” is at least **30% below the comparable Thai purchase price**. This threshold is a design choice for written-spec review, not a newly discovered market fact.
- Calculate the difference programmatically. Do not compare a China single-unit price to a Thai bundle, a counterfeit to an authentic item, or a special membership/coupon offer to an unrestricted retail price without disclosure.
- State that the comparison concerns the documented purchase cost, not savings after airfare, accommodation, or the personal cost of making a shopping trip.

If neither route can be verified, the candidate is excluded and replaced. If enough qualifying gifts cannot be found, raise the evidence blocker and request a scope decision before declaring content complete. Do not manufacture prices, Shopee results, stock status, or exceptions to customs rules.

The official Jinsha catalogue already links products to online shopping, and the physical museum is closed during the stated interval. Neither museum branding nor a catalogue listing proves offline exclusivity or an accessible physical pickup point.

## 6. Language pairing and data model

Use one canonical content dataset with stable item IDs and language-neutral factual fields. Thai and Chinese narratives are associated translations of the same content units, not independent lists that can drift apart.

Each rendered slide has:

- A unique slide ID and stable content-pair ID.
- A language (`th` or `zh-Hans`).
- Category, item ID where relevant, and content-unit type.
- Title, structured body, image reference, language-appropriate alternative text, and relevant source references.

Each pair must render in the order `th → zh-Hans`, with the same item, factual values, qualifications, visual subject, and source set. Chinese text must convey the full information and warnings, not an abbreviated summary. Validate matching numbers, names, locations, prices, units, dates, and evidence labels in addition to checking the presence of both languages.

The standard presentation order always preserves adjacent pairs. A language control may jump to the paired page, but must not silently reorganize the deck into separate language sections.

## 7. Static-site architecture and integration

No backend, authentication, analytics, external slideshow service, or client framework is required.

Proposed component boundaries:

- **Content/source records:** canonical bilingual data and provenance; no rendering or navigation logic.
- **Static renderer/build step:** deterministic generation of presentation HTML and manifests from approved records.
- **Presentation shell:** semantic slide markup, controls, progress, and category navigation.
- **Local styling and fonts:** scoped to the deck so the existing garden’s styles are unaffected.
- **Small navigation script:** keyboard, previous/next, paired-language jump, deep links, and fullscreen enhancement.
- **Validation:** separate content/evidence, language-pair, asset, interaction, and site-build checks.

Expected implementation footprint:

- `slides/chengdu/index.html` and deck-local styles/scripts/data/assets.
- A focused generation/validation script and tests under the existing `scripts/` or a project-specific test location.
- One public garden note linking to `/slides/chengdu/`, using the repository’s existing note conventions.
- This design document and the later implementation plan.

Exact implementation filenames and commands belong in the reviewed implementation plan. Do not restructure existing article layouts, privacy settings, or unrelated content.

Generate usable HTML before JavaScript enhancement where practical, so a script failure does not erase all content. Keep images, required fonts, CSS, and JavaScript local. External references and map links open only when a reader chooses them; do not embed third-party tracking maps.

## 8. Visual and interaction design

Use a warm cream base with jade and vermilion accents. The visual hierarchy prioritizes the place, dish, or product photograph and readable text rather than decorative charts or dense cards.

Every slide—including supporting and reference slides—must include a meaningful visual. Suitable visuals are rights-cleared photographs or clearly labeled original diagrams/maps based on verified data. Do not fabricate a restaurant interior, product, price tag, or travel photograph and present it as documentary evidence.

Language pairs may reuse the same visual. A food-category image that is not verified as the specific restaurant’s dish must be clearly labeled illustrative. A logo or tiny decorative icon alone does not satisfy the image requirement.

Provide visible previous/next controls, keyboard navigation, progress, a table of contents, category/item deep links, and progressive fullscreen support. Do not trap keyboard focus or intercept keys while the reader is using an interactive control. Touch/swipe support must not interfere with ordinary vertical reading or source links.

Slides must remain readable on desktop and mobile without clipped content. If a content unit cannot fit legibly, split it into additional complete bilingual pairs rather than shrinking the text excessively or hiding overflow. Respect reduced-motion preferences and include visible focus indicators, descriptive alt text, and appropriate document/slide language attributes.

## 9. Image, font, and publication rights

A publicly accessible image URL is not reuse permission. For every retained photograph/font record the original source, creator, license or explicit permission, attribution requirements, and any modifications. Use only assets whose terms permit the intended public website use. Preserve applicable license files and satisfy share-alike or other requirements for derivatives where relevant.

Do not republish Michelin, museum, Xinhua, GoChengdu, or travel-company photographs solely because extraction exposed their URLs. Store retained Internet source images in the prescribed knowledge-vault asset location and copy only cleared publication assets into the project.

Optimize images for the presentation while retaining useful resolution. Load efficiently without making inactive slides permanently empty. The image manifest must map each public slide image to a local asset and its credit/rights record.

## 10. Failure behavior

- Missing facts, blocked retrieval, or conflicting source records remain explicitly unresolved and block affected item acceptance.
- An attraction closure supersedes ordinary opening hours printed elsewhere on the same secondary page.
- Price and stock observations always carry dates and limitations; no live-price guarantee is implied.
- A missing or undecodable image fails validation; a decorative fallback cannot silently count as the required subject image.
- Missing fullscreen support must leave ordinary navigation working.
- A bad deep link falls back to a valid initial slide with usable controls, not a blank page.
- Research may continue on unaffected categories while one category is blocked, but the entire deliverable cannot be called complete until all category criteria pass.

## 11. Verification and acceptance

Before publication:

1. Count distinct qualifying records programmatically; confirm the agreed category targets, unique IDs, and no inflated variants or branches.
2. Validate every gift’s evidence route and all published price arithmetic against recorded observations.
3. Verify that every Thai slide is followed by its corresponding Chinese slide; all slides belong to complete pairs and factual values match.
4. Verify every slide has a meaningful local image, language-specific alternative text, and a complete rights/credit record.
5. Build the deck deterministically and exercise navigation, pair jumps, deep links, keyboard/focus behavior, and graceful fullscreen failure.
6. Exercise representative desktop, tablet, and phone viewports, including 1920×1080, 1366×768, 768×1024, 390×844, and 360×800. Inspect all slide layouts for clipping, horizontal overflow, broken images, and illegible text; manually review representative dense Thai and Chinese pages.
7. Run the existing relevant repository validation and a production Jekyll build. Current local inspection did not find Ruby/Bundler on the executable path; establish a real supported build route during implementation rather than reporting an unexecuted build as passed.
8. Verify the new garden link and confirm that the existing site structure and privacy/no-tracking behavior remain intact.
9. Review the Git diff and staged paths; include no unrelated changes, secrets, private-vault content, raw account data, or uncleared assets.

After explicit publication approval:

10. Commit the complete approved artifact set and push to the existing target branch without changing repository visibility.
11. Read the remote branch back and verify it contains the intended commit. Do not treat a command’s success message alone as remote verification.
12. Verify deployment status through the available Pages/build mechanism and retrieve the exact public deck URL. Confirm that the published content version, assets, and navigation are the intended version; a stale HTTP 200 is insufficient.
13. Report the public URL, actual content/slide counts, verified commit, tests exercised, and any genuine remaining limitations.

## 12. Privacy, publishing, and workflow gates

`lawdalana/lawdalana.github.io` is already **PUBLIC**. A push exposes source files and repository history, not only the rendered presentation. Immediately before publishing, identify the exact content/assets/docs/source files being made public and the target repository/URL, then obtain the user’s explicit confirmation. General instructions to continue the task do not bypass this separate publication gate.

Local design commits are permitted at this stage; no push is performed as part of spec preparation. Any later public bundle must be reviewed for unnecessary personal data and unrelated files.

This written spec must be reviewed and approved by the user before invoking `superpowers:writing-plans`. After the written implementation plan is reviewed and an execution method is selected, load the requested `frontend-slides` implementation skill from a verified source, adapt its workflow to the available Hermes tools, and implement with real test/build output. Source discovery identified `zarazhangrui/frontend-slides` and its reported MIT license; the skill instructions have not yet been loaded or executed at this design stage.

## 13. Key source references already researched

These links establish specific background constraints; they are not a substitute for the per-item research and current checks described above.

- Official Jinsha museum: https://www.jinshasitemuseum.com/ — closure date range.
- Jinsha closure/refund notice: https://www.jinshasitemuseum.com/info/4707
- Official Jinsha cultural-product catalogue: https://www.jinshasitemuseum.com/node/195 — named products and online-purchase links.
- Official Jinsha 2026 product article: https://www.jinshasitemuseum.com/info/4870
- Official panda base: https://www.panda.org.cn/en/
- Official Sanxingdui museum: https://www.sxd.cn/
- UNESCO Qingcheng/Dujiangyan: https://whc.unesco.org/en/list/1001/
- Michelin Chengdu list: https://guide.michelin.com/en/cn/chengdu-municipality/chengdu/restaurants
- Secondary attraction discovery: https://www.travelchinaguide.com/attraction/sichuan/chengdu/
- Secondary restaurant discovery: https://www.travelchinaguide.com/cityguides/sichuan/chengdu-restaurants.htm
- Secondary shopping discovery: https://www.travelchinaguide.com/cityguides/sichuan/chengdu/shopping.htm
- Local craft reporting: https://www.gochengdu.cn/en/news/column_167089860862803
- Requested slide-skill source discovery: https://github.com/zarazhangrui/frontend-slides

# AGENTS.md — lawdalana.github.io

Follow the user's instructions. Check current configuration, templates, and scripts when they conflict with `README.md` or `CLAUDE.md`.

## Project

Thai/English digital garden on GitHub Pages: Jekyll 4.3.4, Liquid, Kramdown/GFM, Rouge, KaTeX, Bulma, and Lunr. Plugins: jekyll-feed, jekyll-tidy, jekyll-minifier. Plain HTML/CSS/JavaScript; no npm scripts or `package.json`.

## Key paths

- `_config.yml`: collections, permalinks, preferences; `Gemfile`/`Gemfile.lock`: dependencies.
- `_notes/Public/`: notes by topic; `_notes/Private/`: personal notes in the same collection; `_posts/`: `YYYY-MM-DD-slug.md`; `pages/`: site pages.
- Render path: `_layouts/Post.html` → `_includes/Content.html` → `_includes/content/`. Other includes handle navigation, feeds, backlinks, and the graph.
- `assets/css/`, `assets/js/`, `assets/img/`: styles, behavior, illustrations; `_includes/templates/`: note templates.
- `latent-ai-knowledge-base/index.html`: standalone Latent Lab with embedded assets/data, hash routes, and localStorage; sibling `knowledge/` and `original/`: readings and sources.
- `scripts/`: dev/build/validation; `Dockerfile`/`docker-compose.yml`: environment. Never edit or commit generated `_site/` or `.jekyll-cache/`.

## Commands

Run from the root. Requires Ruby/Bundler, a JavaScript runtime (Docker installs Node.js), and Python 3 for metadata validation.

```bash
bundle install                                     # Dependencies
bash scripts/dev.sh                                # Live reload, drafts, incremental build
JEKYLL_ENV=production bundle exec jekyll build       # Verify production build directly
bash scripts/test.sh                               # Build and basic metadata checks
bash scripts/test-slides.sh                        # Slide menu and browser checks (isolated Node tooling)
python3 scripts/validate_frontmatter.py             # Front matter report
docker compose up --build                           # Docker development
```

- Site: `http://localhost:4000`; legacy Compose: `docker-compose up --build`. Use `bash` because scripts lack executable bits.
- Restart Jekyll after config changes. Docker mounts only posts, notes, assets, and pages; rebuild its image after layout/include/config/dependency changes.

## Editing rules

- Preserve content language, voice, meaning, and references; choose the appropriate topic folder.
- Note front matter requires `title`, `notetype`, `date`, `last_modified`, `tags`, `status`. Use real `YYYY-MM-DD` dates; preserve creation date and update modification date.
- Note types: `feed`, `reference`, `permanent`; only `feed` appears in the feed. Use templates for examples.
- Wiki links `[[Note title]]` match titles exactly. Avoid duplicate titles; check backlinks after renames/moves. Inspect parsers for special syntax/aliases; post lookups currently get overwritten by note lookups.
- Preserve note/post routes `/notes/:title` and `/posts/:title`; verify links/assets before changing `url` or `baseurl`. Use labeled code fences and check rendered equations/tables.
- Add images by topic with descriptive names, alt text, and appropriate lazy loading. `convert_image_type.py` converts the entire image tree.
- Active CSS: `assets/css/style.css`, `main.css`, `Util.css`, `vendor/Katex.css`. The main layout does not load `style-new.css`, `main-new.css`, or modular component CSS.
- `assets/js/SearchData.json` is Liquid source, not generated JSON: preserve `jsonify`. Keep `preferences` toggles working when disabled.
- Follow existing style; use 2-space indentation for new sections, small functions, immutable state, boundary validation, and HTML/attribute escaping. Avoid unrelated formatting or new frameworks.
- Preserve mobile layouts, themes, keyboard/focus behavior, and Thai readability.
- Keep Latent Lab synchronized with its Markdown, references, equations, IDs, and prerequisites; avoid dumping/reformatting embedded vendor code or data.
- Latent Lab's README references `tools/build_learning_html.py` and `tools/learning_ui/story.json`, absent here. Verify tools exist before claiming regeneration.

## Presentation tabs

- When asked to turn notes, articles, or PPTX files into presentations, use the `frontend-slides` skill and follow its content/style workflow.
- Save each deck as `<topic>-slides/index.html` with inline CSS/JS and no Jekyll front matter or npm build. Register it in `_data/slides.yml` under a `category` with `decks` entries containing `title`, `url`, and optional `description`; the single `Slides` navbar dropdown lists them in catalog order. Preserve the first Latent Lab entry and provide return/source links in decks.
- Include the skill's full `viewport-base.css`; use a fixed 1920×1080 stage scaled uniformly at 16:9, keyboard/touch navigation, reduced-motion support, and no content overflow or overlap.
- Check the full Jekyll build, navbar/deck/return links, and rendered slides at 1280×720 and a phone viewport. Integrate with this GitHub Pages site; use other hosting only when requested.

## Privacy and publication

- `_notes/Private/` is in an `output: true` collection; search/graph use all `site.notes`. `unfeed` only hides feed entries, and `status: draft` is not a publication filter. Inspect output before relying on content hiding.
- Access personal notes only within authorized scope. Robots directives discourage indexing, not access; inspect standalone pages separately.
- Google Fonts, KaTeX, and D3 still use CDNs despite older local-only claims. Check network activity; add no tracking or secrets.
- No `.github/workflows/` exists here; do not assume Actions checks/deployment. Push, merge, publish, hosting changes, and third-party writes require explicit user authorization.

## Verification

- Check `git status --short`; preserve others' edits. Plan complex work and assign file ownership when agents are authorized. Review code for correctness, maintainability, and security.
- Use TDD for behavior changes and applicable unit/integration/E2E checks; verify UI in a real desktop/mobile browser and inspect console errors.
- Check note metadata, links, images, and equations. Run a full Jekyll build for config/template/JavaScript changes and inspect generated pages/JSON.
- Metadata validator reports issues without failing its exit code; `scripts/test.sh` does not fail on metadata warnings or run html-proofer. `scripts/build.sh` may print success after failure; use the direct build command above.
- Slide browser tests live in `tests/slides-dropdown.test.cjs`; the runner caches Node test dependencies outside the repo and uses Chrome/Chromium. Target ≥80% coverage for added code once measured; never invent results. Separate existing warnings from regressions and avoid unrelated bulk metadata edits.
- Report changes, actual verification, and unavailable tools/checks. Use conventional commits (`docs:`, `fix:`, `feat:`) when committing.

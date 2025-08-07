# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll-based digital garden/knowledge management site hosted on GitHub Pages. Version 2.0.0 combines traditional blogging with Obsidian-style note-taking features including wiki-style linking, backlinks, transclusion, and page previews, with significant improvements in privacy, performance, and maintainability.

## Version History

- **Version 1.0.0**: Initial Jekyll digital garden implementation
- **Version 2.0.0**: Major refactoring with privacy-first approach, performance optimizations, and modular architecture

## Development Environment

### Local Development Commands

**Using Docker (Recommended):**
```bash
docker-compose up --build
```
Site will be available at http://localhost:4000

**Using Native Ruby:**
```bash
bundle install
bundle exec jekyll serve --drafts
```

**Development Scripts (v2.0.0+):**
```bash
# Development server with live reload
./scripts/dev.sh

# Production build with optimizations
./scripts/build.sh

# Run validation tests
./scripts/test.sh
```

**Building for Production:**
```bash
JEKYLL_ENV=production bundle exec jekyll build
```

### Dependencies (v2.0.0)

- **Jekyll**: 4.3.4 (upgraded from 4.0.0)
- **Performance**: jekyll-minifier, html-proofer
- **Styling**: sassc (Alpine Linux compatibility)
- **Math**: kramdown-math-katex
- **Privacy**: No SEO plugins (intentional)

### Testing and Validation

**Automated Tools:**
- `scripts/validate_frontmatter.py` - Checks note metadata completeness
- `scripts/test.sh` - Comprehensive site validation
- `html-proofer` - Link and HTML validation (test environment)

**Manual Testing:**
- Wiki-style links `[[]]` resolve correctly
- Backlinks generation works
- Search functionality (full-text with autocomplete)
- Dark/light mode toggle
- Mathematical notation renders via KaTeX
- Page preview tooltips on hover
- Mobile responsiveness

## Architecture and Structure (v2.0.0)

### Modular Template System
```
_includes/
├── content/                # Modular content processors (v2.0.0)
│   ├── link-parser.html   # Parses [[]] wiki links
│   ├── internal-links.html # Processes internal links with previews
│   ├── external-links.html # Handles special syntax & external links
│   ├── highlighting.html  # Text highlighting features
│   ├── sidenotes.html     # Sidenote functionality
│   └── flashcards.html    # Flashcard/SRS features
├── templates/             # Content templates (v2.0.0)
│   ├── note-template.md   # Standard note template
│   ├── book-review-template.md
│   └── quick-note-template.md
├── Header.html            # Navigation (optimized)
└── Footer.html            # Site footer (optimized)
```

### CSS Architecture (v2.0.0)
```
assets/css/
├── base/
│   └── variables.css      # CSS custom properties, themes
├── components/            # Modular UI components
│   ├── navigation.css     # Navbar, menus, back buttons
│   ├── search.css         # Search input and results
│   ├── notes.css          # Note cards, tooltips, backlinks
│   └── highlighting.css   # Syntax highlighting
├── utilities/
│   └── helpers.css        # Utility classes
├── main.css              # Bulma framework (unchanged)
├── style.css             # Original styles (kept for reference)
└── style-new.css         # New organized stylesheet
```

### Content Organization

- `/_notes/` - Main knowledge base organized by topic:
  - `/Public/DS/` - Data Science topics
  - `/Public/LLM/` - Large Language Model topics  
  - `/Public/MLE/` - Machine Learning Engineering
  - `/Public/RecSys/` - Recommendation Systems
  - `/Public/Book/` - Book reviews and summaries
  - `/Public/Learning/` - Educational content
  - `/Public/Other/` - Miscellaneous technical topics
  - `/Private/` - Personal notes and thoughts
- `/_posts/` - Traditional blog posts
- `/pages/` - Static pages (index, notes, posts, 404)
- `/scripts/` - Development and validation utilities

## Key Features (v2.0.0)

### Privacy-First Design
- **No External Tracking**: No analytics, social widgets, or external trackers
- **Search Engine Protection**: robots.txt and noindex meta tags prevent indexing
- **Local Assets**: All CSS, JS, fonts served locally (no CDNs)
- **User Control**: Accessible to visitors but not indexed by search engines

### Performance Optimizations
- **Image Loading**: Lazy loading with `loading="lazy"` attributes
- **Script Loading**: Deferred JavaScript loading for better performance
- **Minification**: HTML, CSS, JS compression enabled
- **Caching**: Modular CSS architecture improves browser caching

### Wiki-Style Features
- **Internal Links**: `[[Note Title]]` syntax for seamless linking
- **Backlinks**: Automatic reverse linking between connected notes
- **Page Previews**: Hover tooltips showing note content
- **Transclusion**: Embed content from other notes
- **Search**: Full-text search with autocomplete
- **Special Syntax**: Highlighting, sidenotes, flashcards, image embedding

### Content Management
- **Standardized Frontmatter**: Consistent metadata across all notes
- **Note Types**: `feed`, `reference`, `permanent` for content classification
- **Status Tracking**: `draft`, `published` for workflow management
- **Templates**: Pre-built templates for different content types
- **Validation**: Automated frontmatter completeness checking

## Content Creation Guidelines (v2.0.0)

### Standardized Note Structure
```yaml
---
title: "Your Note Title"
notetype: feed  # feed, reference, permanent
date: YYYY-MM-DD
last_modified: YYYY-MM-DD
tags: [tag1, tag2, tag3]
status: published  # draft, published
---

Your note content here.

## Related Notes
- [[Internal Note Link]]
- [External Link](https://example.com)
```

### Wiki-Style Linking Syntax
- `[[Note Title]]` - Links to internal notes
- `[[text::highlight]]` - Highlights text with theme color
- `[[Note Title::rsn]]` - Creates right sidenote
- `[[Image URL::img]]` - Embeds images with lazy loading
- `[[text::wrap]]` - Wraps text in styled box
- `[[Link Text::https://example.com]]` - External links

### Content Templates Available
- **note-template.md**: General purpose notes
- **book-review-template.md**: Book reviews with ratings
- **quick-note-template.md**: Brief thoughts and links

## Configuration (v2.0.0)

### Key _config.yml Settings
```yaml
# Privacy settings (v2.0.0)
plugins:
  - jekyll-feed 
  - jekyll-tidy
  - jekyll-minifier  # Performance optimization

# Feature toggles
preferences:
  search:
    enabled: true
  wiki_style_link:
    enabled: true
  pagepreview:
    enabled: true
  backlinks:
    enabled: true
  highlighting:
    enabled: true
    color: DAEDFF  # Customizable highlight color

# Performance optimization
jekyll-minifier:
  preserve_php: true
  remove_spaces_inside_tags: true
  compress_css: true
  compress_javascript: true

sass:
  style: compressed
  implementation: sassc  # Alpine Linux compatibility
```

### Development Scripts
- `scripts/dev.sh` - Development server with live reload
- `scripts/build.sh` - Production build with optimization stats
- `scripts/test.sh` - Comprehensive validation suite
- `scripts/validate_frontmatter.py` - Check note metadata completeness

## Theme and Styling (v2.0.0)

### CSS Custom Properties
- Organized theme variables in `base/variables.css`
- Automatic dark mode support via `prefers-color-scheme`
- Manual toggle available in navigation
- Smooth transitions between themes

### Component-Based Styling
- Modular CSS architecture for better maintainability
- Separated concerns: navigation, search, notes, highlighting
- Responsive design with mobile-first approach
- Performance optimized with better caching

## Deployment

### GitHub Pages (Automatic)
Site deploys automatically to GitHub Pages when changes are pushed to the main branch. 

### Performance Notes
- Jekyll 4.3.4 provides better build performance
- Minification reduces file sizes significantly
- Modular CSS improves caching efficiency
- Lazy loading reduces initial page load

### Privacy Compliance
- No external requests (all assets local)
- No search engine indexing
- No user tracking or analytics
- GDPR compliant by design

## Troubleshooting

### Docker Issues (v2.0.0)
- **sass-embedded error**: Known issue with Alpine Linux, doesn't affect GitHub Pages
- **Workaround**: Use `sassc` gem (already configured)
- **Alternative**: Use native Ruby development instead of Docker

### Content Issues
- **Missing frontmatter**: Run `python3 scripts/validate_frontmatter.py`
- **Broken links**: Check `scripts/test.sh` output
- **Search not working**: Verify `_config.yml` search settings

### Performance Testing
- Use browser dev tools to verify lazy loading
- Check network tab for external requests (should be none)
- Verify minification in production builds
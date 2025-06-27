# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll-based digital garden/knowledge management site hosted on GitHub Pages. It combines traditional blogging with Obsidian-style note-taking features including wiki-style linking, backlinks, transclusion, and page previews.

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
bundle exec jekyll serve
```

**Building for Production:**
```bash
bundle exec jekyll build
```

### Testing and Validation

No automated test suite is configured. Manual testing involves:
- Verifying site builds without errors
- Checking that wiki-style links `[[]]` resolve correctly
- Ensuring backlinks are generated properly
- Testing search functionality
- Validating mathematical notation renders via KaTeX

## Architecture and Structure

### Content Organization

- `/_notes/` - Main knowledge base organized by topic:
  - `/Public/DS/` - Data Science topics
  - `/Public/LLM/` - Large Language Model topics  
  - `/Public/MLE/` - Machine Learning Engineering
  - `/Public/RecSys/` - Recommendation Systems
  - `/Private/` - Personal notes
- `/_posts/` - Traditional blog posts
- `/pages/` - Static pages (index, about, etc.)

### Key Jekyll Features

- **Collections**: Notes are handled as a Jekyll collection separate from posts
- **Wiki-style Links**: `[[Note Title]]` syntax for internal linking
- **Backlinks**: Automatic reverse linking between connected notes
- **Transclusion**: Embedding content from other notes using special syntax
- **Search**: JavaScript-powered search with autocomplete
- **Math Support**: KaTeX integration for mathematical notation

### Configuration

All site behavior is controlled via `_config.yml`:
- Feature toggles under `preferences:` section
- Wiki-style linking, backlinks, transclusion, search, etc.
- Collection configuration for notes vs posts
- Kramdown settings for markdown processing

### Theme and Styling

- Custom CSS with dark/light mode support
- Responsive design optimized for reading
- Syntax highlighting via Rouge
- Custom JavaScript for interactive features

## Content Creation Guidelines

### Note Structure
- Use frontmatter for metadata
- Leverage wiki-style `[[]]` links for connections
- Organize by topic in appropriate `/Public/` subdirectories
- Use descriptive filenames that match note titles

### Mathematical Content
- KaTeX is available for math rendering
- Use standard LaTeX syntax within markdown

### Linking Strategy
- Use `[[Note Title]]` for internal wiki-style links
- Regular markdown links for external references
- Backlinks are automatically generated and displayed

## Deployment

Site deploys automatically to GitHub Pages when changes are pushed to the main branch. No manual deployment steps required.
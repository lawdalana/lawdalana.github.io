# Digital Garden - Personal Knowledge Base

A privacy-focused Jekyll-based digital garden for managing and sharing knowledge. This site combines traditional blogging with Obsidian-style note-taking features including wiki-style linking, backlinks, transclusion, and page previews.

## 🌟 Features

### Knowledge Management
- **Wiki-style Links**: Use `[[Note Title]]` to link between notes
- **Backlinks**: Automatic reverse linking between connected notes  
- **Page Previews**: Hover over links to see note previews
- **Transclusion**: Embed content from other notes
- **Search**: Full-text search with autocomplete
- **Tags & Categories**: Organize notes by topic and type

### Digital Garden Functionality
- **Note Collections**: Separate from blog posts for better organization
- **Note Types**: `feed`, `reference`, `permanent` for different content types
- **Status Tracking**: `draft`, `published` for workflow management
- **Mathematical Notation**: KaTeX support for equations
- **Syntax Highlighting**: Code blocks with Rouge

### Privacy & Performance
- **Privacy-First**: No external analytics, tracking, or CDNs
- **Search Engine Protection**: robots.txt and noindex meta tags
- **Performance Optimized**: Lazy loading, deferred scripts, minification
- **Responsive Design**: Works on desktop and mobile

## 🚀 Quick Start

### Prerequisites
- Ruby 3.1+ 
- Bundler gem
- Git

### Local Development

#### Option 1: Docker (Recommended)
```bash
git clone <repository-url>
cd lawdalana.github.io
docker-compose up --build
```
Visit http://localhost:4000

#### Option 2: Native Ruby
```bash
git clone <repository-url>
cd lawdalana.github.io
bundle install
bundle exec jekyll serve --drafts
```
Visit http://localhost:4000

### Production Build
```bash
JEKYLL_ENV=production bundle exec jekyll build
```

## 📝 Content Creation

### Creating Notes
Notes are stored in `_notes/` directory with two main sections:
- `_notes/Public/` - Public knowledge areas (DS, LLM, MLE, etc.)
- `_notes/Private/` - Personal notes and thoughts

### Note Template
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

## Links
- [[Internal Note Link]]
- [External Link](https://example.com)
```

### Wiki-Style Linking
- `[[Note Title]]` - Links to internal notes
- `[[text::highlight]]` - Highlights text
- `[[Note Title::rsn]]` - Creates right sidenote
- `[[Image URL::img]]` - Embeds images
- `[[text::wrap]]` - Wraps text in a box

### Special Syntax
- **Highlighting**: `[[important text::highlight]]`
- **Sidenotes**: `[[sidenote text::rsn]]` (right), `[[text::lsn]]` (left)
- **Margin Notes**: `[[margin note::rmn]]` (right), `[[text::lmn]]` (left)
- **Images**: `[[/path/to/image.jpg::img]]`
- **External Links**: `[[Link Text::https://example.com]]`

## 🛠️ Development

### Project Structure
```
├── _config.yml           # Jekyll configuration
├── _includes/             # Reusable HTML components
│   ├── content/          # Modular content processors
│   ├── Header.html       # Site navigation
│   └── Footer.html       # Site footer
├── _layouts/             # Page templates
├── _notes/               # Note collection
│   ├── Public/          # Public knowledge areas
│   └── Private/         # Personal notes
├── _posts/               # Blog posts
├── assets/               # Static assets (CSS, JS, images)
├── pages/                # Static pages
└── scripts/              # Development utilities
```

### Key Configuration
Edit `_config.yml` to customize:
- Site metadata and URLs
- Feature toggles (search, backlinks, previews)
- Privacy settings
- Performance optimizations

### Development Scripts
```bash
# Validate note frontmatter
python3 scripts/validate_frontmatter.py

# Development server with live reload
bundle exec jekyll serve --livereload --drafts

# Production build with optimizations  
JEKYLL_ENV=production bundle exec jekyll build
```

## 🎨 Customization

### Themes
- Built-in dark/light mode toggle
- Customizable highlighting colors in `_config.yml`
- Responsive design with Bulma CSS framework

### Adding Features
The modular architecture makes it easy to:
- Add new content processors in `_includes/content/`
- Create custom note templates in `_includes/templates/`
- Extend search functionality
- Add new wiki-style syntax

## 🔒 Privacy Features

This digital garden is designed for privacy:
- **No Tracking**: No Google Analytics, social media widgets, or external trackers
- **Search Engine Protection**: robots.txt and noindex meta tags prevent indexing
- **Local Assets**: All CSS, JS, and fonts served locally
- **No CDNs**: No external dependencies for better privacy and performance

## 📚 Content Organization

### Recommended Structure
- **DS/**: Data Science topics (algorithms, metrics, ML concepts)
- **LLM/**: Large Language Model topics (RAG, transformers, etc.)
- **MLE/**: Machine Learning Engineering (tools, infrastructure)
- **Book/**: Book reviews and summaries  
- **Learning/**: Course notes and educational content
- **Other/**: Miscellaneous technical topics

### Note Types
- **feed**: Ongoing notes, frequently updated
- **reference**: Stable reference material
- **permanent**: Evergreen content, rarely changes

## 🚀 Deployment

### GitHub Pages
1. Push to main branch
2. GitHub Actions automatically builds and deploys
3. Site available at `https://username.github.io`

### Custom Domain
1. Add CNAME file with your domain
2. Configure DNS settings
3. Enable HTTPS in repository settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `bundle exec jekyll serve`
5. Submit a pull request

### Code Style
- Use 2 spaces for indentation
- Follow liquid templating best practices
- Add comments to complex logic
- Maintain modular architecture

## 📄 License

The theme (https://jekyll-garden.github.io/) is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).

## 🔗 Links

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Liquid Template Language](https://shopify.github.io/liquid/)
- [Jekyll Garden Theme](https://jekyll-garden.github.io/)
- [Obsidian](https://obsidian.md/) - Inspiration for wiki-style linking

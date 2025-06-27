#!/bin/bash

# Production build script
# Builds optimized site for deployment

echo "🏗️  Building site for production..."
echo "⚡ Performance optimizations enabled"
echo "🗜️  Minification enabled"
echo ""

JEKYLL_ENV=production bundle exec jekyll build

echo ""
echo "✅ Build complete!"
echo "📁 Site generated in _site/ directory"
echo "📊 Build statistics:"
du -sh _site/
echo "📄 Total files: $(find _site -type f | wc -l)"
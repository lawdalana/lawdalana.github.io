#!/bin/bash

# Development server script
# Starts Jekyll with live reload and drafts enabled

echo "🚀 Starting Jekyll development server..."
echo "📝 Drafts enabled"
echo "🔄 Live reload enabled"
echo "🌐 Site will be available at http://localhost:4000"
echo ""

bundle exec jekyll serve --livereload --drafts --incremental
#!/bin/bash

# Test script
# Validates the site build and content

echo "🧪 Running site tests..."
echo ""

# Build the site first
echo "1️⃣ Building site..."
bundle exec jekyll build --trace

if [ $? -ne 0 ]; then
    echo "❌ Site build failed!"
    exit 1
fi

echo "✅ Site builds successfully"
echo ""

# Validate frontmatter
echo "2️⃣ Validating note frontmatter..."
if [ -f "scripts/validate_frontmatter.py" ]; then
    python3 scripts/validate_frontmatter.py
else
    echo "⚠️  Frontmatter validation script not found"
fi

echo ""

# Check for broken internal links (basic)
echo "3️⃣ Checking for common issues..."

# Check for missing titles in notes
missing_titles=$(find _notes -name "*.md" -exec grep -L "title:" {} \;)
if [ -n "$missing_titles" ]; then
    echo "⚠️  Notes missing titles:"
    echo "$missing_titles"
else
    echo "✅ All notes have titles"
fi

# Check for very old dates (potential typos)
old_dates=$(find _notes -name "*.md" -exec grep -l "date.*: 202[0-1]" {} \;)
if [ -n "$old_dates" ]; then
    echo "ℹ️  Notes with old dates (check for typos):"
    echo "$old_dates" | head -3
fi

echo ""
echo "🎉 Testing complete!"
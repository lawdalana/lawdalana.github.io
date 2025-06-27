#!/bin/bash

# Script to update frontmatter in markdown files
# Usage: ./scripts/update_frontmatter.sh

find _notes -name "*.md" -print0 | while IFS= read -r -d '' file; do
    echo "Processing: $file"
    
    # Check if file has frontmatter
    if head -1 "$file" | grep -q "^---$"; then
        # Extract existing frontmatter fields
        title=$(sed -n '2,/^---$/p' "$file" | grep -E "^title\s*:" | head -1)
        notetype=$(sed -n '2,/^---$/p' "$file" | grep -E "^notetype\s*:" | head -1)
        date=$(sed -n '2,/^---$/p' "$file" | grep -E "^date\s*:" | head -1)
        
        # Normalize existing fields
        title=$(echo "$title" | sed 's/title\s*:/title:/' | sed 's/title: */title: /')
        notetype=$(echo "$notetype" | sed 's/notetype\s*:/notetype:/' | sed 's/notetype: */notetype: /')
        date=$(echo "$date" | sed 's/date\s*:/date:/' | sed 's/date: */date: /')
        
        echo "  Found: $title"
        echo "  Found: $notetype"  
        echo "  Found: $date"
    fi
    echo "---"
done
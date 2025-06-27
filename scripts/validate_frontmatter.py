#!/usr/bin/env python3

import os
import glob
import re
from pathlib import Path

def check_frontmatter(file_path):
    """Check if a markdown file has complete frontmatter"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if file starts with frontmatter
        if not content.startswith('---\n'):
            return False, "No frontmatter found"
        
        # Extract frontmatter
        try:
            end_index = content.index('---\n', 4)
            frontmatter = content[4:end_index]
        except ValueError:
            return False, "Frontmatter not properly closed"
        
        # Required fields
        required_fields = ['title:', 'notetype:', 'date:', 'last_modified:', 'tags:', 'status:']
        missing_fields = []
        
        for field in required_fields:
            if field not in frontmatter:
                missing_fields.append(field.replace(':', ''))
        
        if missing_fields:
            return False, f"Missing fields: {', '.join(missing_fields)}"
        
        # Check date format (YYYY-MM-DD)
        date_pattern = r'date:\s*(\d{4}-\d{2}-\d{2})'
        if not re.search(date_pattern, frontmatter):
            return False, "Date format should be YYYY-MM-DD"
        
        return True, "Complete"
        
    except Exception as e:
        return False, f"Error reading file: {str(e)}"

def main():
    """Check all markdown files in _notes directory"""
    note_files = glob.glob('_notes/**/*.md', recursive=True)
    
    print("Frontmatter Validation Report")
    print("=" * 50)
    
    complete_count = 0
    total_count = len(note_files)
    
    for file_path in sorted(note_files):
        is_complete, message = check_frontmatter(file_path)
        status = "✅" if is_complete else "❌"
        
        print(f"{status} {file_path}")
        if not is_complete:
            print(f"   → {message}")
        
        if is_complete:
            complete_count += 1
    
    print("\n" + "=" * 50)
    print(f"Summary: {complete_count}/{total_count} files have complete frontmatter")
    print(f"Completion rate: {complete_count/total_count*100:.1f}%")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Remove references to missing glyphs from features file.
"""

import sys
import re
from defcon import Font


def clean_features(ufo_path):
    """Remove glyph references that don't exist in the font."""
    font = Font(ufo_path)
    available_glyphs = set(font.keys())
    
    features_path = f"{ufo_path}/features.fea"
    
    with open(features_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all glyph references (uni#### pattern)
    glyph_pattern = r'\buni[0-9A-Fa-f]{4}\b'
    referenced_glyphs = set(re.findall(glyph_pattern, content))
    
    missing_glyphs = referenced_glyphs - available_glyphs
    
    if not missing_glyphs:
        print(f"✓ No missing glyphs in {ufo_path}")
        return
    
    print(f"⚠ Found {len(missing_glyphs)} missing glyphs in {ufo_path}")
    
    # Remove lines containing missing glyphs
    lines = content.split('\n')
    cleaned_lines = []
    removed_count = 0
    
    for line in lines:
        has_missing = False
        for missing_glyph in missing_glyphs:
            if missing_glyph in line:
                has_missing = True
                break
        
        if has_missing:
            removed_count += 1
        else:
            cleaned_lines.append(line)
    
    # Write back
    with open(features_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_lines))
    
    print(f"✓ Removed {removed_count} lines with missing glyph references from {ufo_path}")


if __name__ == "__main__":
    clean_features("Sahel.ufo")
    clean_features("Sahel-Bold.ufo")
    clean_features("Sahel-Black.ufo")

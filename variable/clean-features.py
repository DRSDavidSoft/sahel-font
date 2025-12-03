#!/usr/bin/env python3
"""
Remove references to missing glyphs from features file.
"""

import re
from defcon import Font


def clean_features(ufo_path):
    """Remove glyph references that don't exist in the font."""
    try:
        font = Font(ufo_path)
    except Exception as e:
        print(f"✗ Error loading UFO {ufo_path}: {e}")
        return False
    
    available_glyphs = set(font.keys())
    
    features_path = f"{ufo_path}/features.fea"
    
    try:
        with open(features_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"✗ Features file not found: {features_path}")
        return False
    except Exception as e:
        print(f"✗ Error reading features file {features_path}: {e}")
        return False
    
    # Find all glyph references (uni#### pattern with optional suffixes like .compact)
    glyph_pattern = r'\buni[0-9A-Fa-f]{4,6}(?:\.[a-zA-Z0-9_]+)?\b'
    referenced_glyphs = set(re.findall(glyph_pattern, content))
    
    missing_glyphs = referenced_glyphs - available_glyphs
    
    if not missing_glyphs:
        print(f"✓ No missing glyphs in {ufo_path}")
        return True
    
    print(f"⚠ Found {len(missing_glyphs)} missing glyphs in {ufo_path}")
    
    # Remove lines containing missing glyphs (using word boundaries)
    lines = content.split('\n')
    cleaned_lines = []
    removed_count = 0
    
    for line in lines:
        has_missing = False
        for missing_glyph in missing_glyphs:
            # Use word boundary regex to avoid partial matches
            if re.search(rf'\b{re.escape(missing_glyph)}\b', line):
                has_missing = True
                break
        
        if has_missing:
            removed_count += 1
        else:
            cleaned_lines.append(line)
    
    # Write back
    try:
        with open(features_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cleaned_lines))
    except Exception as e:
        print(f"✗ Error writing features file {features_path}: {e}")
        return False
    
    print(f"✓ Removed {removed_count} lines with missing glyph references from {ufo_path}")
    return True


if __name__ == "__main__":
    success = True
    success &= clean_features("Sahel.ufo")
    success &= clean_features("Sahel-Bold.ufo")
    success &= clean_features("Sahel-Black.ufo")
    
    if not success:
        exit(1)

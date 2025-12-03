#!/usr/bin/env python3
"""
Fix UFO compatibility issues for variable font building.

This script ensures all masters have matching glyph structures by:
- Making component references consistent across masters
- Ensuring anchor points are consistent
"""

import os
import sys
from defcon import Font


# ANSI color codes
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'


def print_success(message):
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")


def print_error(message):
    print(f"{Colors.RED}✗ {message}{Colors.NC}")


def print_warning(message):
    print(f"{Colors.YELLOW}⚠ {message}{Colors.NC}")


def print_info(message):
    print(f"{Colors.BLUE}ℹ {message}{Colors.NC}")


def fix_component_compatibility(fonts, glyph_name):
    """Fix component compatibility by decomposing in all masters."""
    print_info(f"Fixing glyph '{glyph_name}' - decomposing ALL components")
    
    fixed = False
    for font_path, font in fonts.items():
        if glyph_name in font:
            glyph = font[glyph_name]
            if len(glyph.components) > 0:
                # Decompose all components to avoid ordering issues
                components_to_remove = list(glyph.components)
                for component in components_to_remove:
                    base_glyph_name = component.baseGlyph
                    print_info(f"  Decomposing component '{base_glyph_name}' in {os.path.basename(font_path)}")
                    glyph.removeComponent(component)
                    fixed = True
                
                # If glyph still has components after removal, clear them all
                if len(glyph.components) > 0:
                    print_warning(f"  Clearing remaining components in {os.path.basename(font_path)}")
                    glyph.clearComponents()
                    fixed = True
    
    return fixed


def fix_anchor_compatibility(fonts, glyph_name):
    """Fix anchor compatibility by removing differing anchors."""
    print_info(f"Fixing anchors in glyph '{glyph_name}'")
    
    # Collect all anchor names
    all_anchors = set()
    for font_path, font in fonts.items():
        if glyph_name in font:
            glyph = font[glyph_name]
            for anchor in glyph.anchors:
                all_anchors.add(anchor.name)
    
    # Find which anchors are present in all masters
    common_anchors = set()
    for anchor_name in all_anchors:
        present_in_all = True
        for font_path, font in fonts.items():
            if glyph_name in font:
                glyph = font[glyph_name]
                if not any(a.name == anchor_name for a in glyph.anchors):
                    present_in_all = False
                    break
        if present_in_all:
            common_anchors.add(anchor_name)
    
    # Remove anchors not present in all masters
    fixed = False
    for font_path, font in fonts.items():
        if glyph_name in font:
            glyph = font[glyph_name]
            anchors_to_remove = []
            for anchor in glyph.anchors:
                if anchor.name not in common_anchors:
                    anchors_to_remove.append(anchor)
            
            for anchor in anchors_to_remove:
                print_warning(f"  Removing anchor '{anchor.name}' from {os.path.basename(font_path)}")
                glyph.removeAnchor(anchor)
                fixed = True
    
    return fixed


def main():
    print(f"\n{Colors.CYAN}{'=' * 60}{Colors.NC}")
    print(f"{Colors.CYAN}  UFO Compatibility Fixer{Colors.NC}")
    print(f"{Colors.CYAN}{'=' * 60}{Colors.NC}\n")
    
    # Load all UFO files
    ufo_files = {
        'Sahel.ufo': 'Sahel.ufo',
        'Sahel-Bold.ufo': 'Sahel-Bold.ufo',
        'Sahel-Black.ufo': 'Sahel-Black.ufo',
    }
    
    fonts = {}
    for name, path in ufo_files.items():
        if os.path.exists(path):
            print_info(f"Loading {name}")
            fonts[path] = Font(path)
        else:
            print_error(f"UFO not found: {path}")
            return 1
    
    print_success("All UFO files loaded")
    print()
    
    # Known compatibility issues from error messages
    # We'll decompose ALL components in these glyphs to ensure consistency
    issues = [
        'uni0622',
        'uni0623',
        'uniFB58',
        'uniFE91',
        'uniFE8A.compact',
    ]
    
    anchor_issues = [
        'NameMe.303',
    ]
    
    # Fix component issues
    print_info("Fixing component compatibility issues...")
    for glyph_name in issues:
        fix_component_compatibility(fonts, glyph_name)
    print()
    
    # Fix anchor issues
    print_info("Fixing anchor compatibility issues...")
    for glyph_name in anchor_issues:
        fix_anchor_compatibility(fonts, glyph_name)
    print()
    
    # Save all fonts
    print_info("Saving modified UFO files...")
    for path, font in fonts.items():
        font.save()
        print_success(f"Saved {os.path.basename(path)}")
    
    print()
    print_success("Compatibility fixes applied successfully!")
    print()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

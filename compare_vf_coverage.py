#!/usr/bin/env python3
"""
Compare glyph coverage between Variable Font and Static Fonts

This script analyzes and compares:
- Number of glyphs in VF vs static fonts
- Glyphs present in VF but not in static fonts
- Glyphs present in static fonts but not in VF
- Character coverage (Unicode codepoints)
"""

import sys
from pathlib import Path
from fontTools.ttLib import TTFont
from collections import defaultdict


# ANSI color codes
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    NC = '\033[0m'  # No Color


def print_header(message):
    """Print a header message"""
    print(f"\n{Colors.MAGENTA}{'=' * 70}{Colors.NC}")
    print(f"{Colors.MAGENTA}  {message}{Colors.NC}")
    print(f"{Colors.MAGENTA}{'=' * 70}{Colors.NC}\n")


def print_section(message):
    """Print a section message"""
    print(f"\n{Colors.CYAN}▶ {message}{Colors.NC}")


def print_success(message):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")


def print_error(message):
    """Print error message"""
    print(f"{Colors.RED}✗ {message}{Colors.NC}")


def print_warning(message):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.NC}")


def print_info(message):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {message}{Colors.NC}")


def get_glyph_names(font_path):
    """Get set of glyph names from a font"""
    try:
        font = TTFont(font_path)
        glyph_names = set(font.getGlyphNames())
        font.close()
        return glyph_names
    except Exception as e:
        print_error(f"Error reading {font_path}: {e}")
        return set()


def get_cmap(font_path):
    """Get character map (Unicode codepoint to glyph name mapping)"""
    try:
        font = TTFont(font_path)
        cmap = {}
        if 'cmap' in font:
            for table in font['cmap'].tables:
                cmap.update(table.cmap)
        font.close()
        return cmap
    except Exception as e:
        print_error(f"Error reading cmap from {font_path}: {e}")
        return {}


def get_font_info(font_path):
    """Get basic font information"""
    try:
        font = TTFont(font_path)
        info = {
            'num_glyphs': font['maxp'].numGlyphs if 'maxp' in font else 0,
            'is_variable': 'fvar' in font,
            'tables': list(font.keys())
        }
        font.close()
        return info
    except Exception as e:
        print_error(f"Error reading font info from {font_path}: {e}")
        return {}


def compare_fonts():
    """Compare VF and static fonts"""
    print_header("🔤 Sahel Font: VF vs Static Comparison")
    
    dist_dir = Path(__file__).parent / 'dist'
    
    # Check if dist directory exists
    if not dist_dir.exists():
        print_error(f"dist directory not found: {dist_dir}")
        return 1
    
    # Find fonts
    vf_font = dist_dir / 'Sahel-VF.ttf'
    static_fonts = {
        'Light': dist_dir / 'Sahel-Light.ttf',
        'Regular': dist_dir / 'Sahel.ttf',
        'SemiBold': dist_dir / 'Sahel-SemiBold.ttf',
        'Bold': dist_dir / 'Sahel-Bold.ttf',
        'Black': dist_dir / 'Sahel-Black.ttf',
    }
    
    # Check VF exists
    if not vf_font.exists():
        print_error(f"Variable font not found: {vf_font}")
        return 1
    
    print_success(f"Found variable font: {vf_font.name}")
    
    # Check which static fonts exist
    available_static = {}
    for name, path in static_fonts.items():
        if path.exists():
            available_static[name] = path
            print_success(f"Found static font: {path.name}")
        else:
            print_warning(f"Static font not found: {path.name}")
    
    if not available_static:
        print_error("No static fonts found!")
        return 1
    
    # Get VF info
    print_section("Variable Font Analysis")
    vf_info = get_font_info(vf_font)
    vf_glyphs = get_glyph_names(vf_font)
    vf_cmap = get_cmap(vf_font)
    
    print_info(f"Number of glyphs: {len(vf_glyphs)}")
    print_info(f"Number of mapped characters: {len(vf_cmap)}")
    print_info(f"Is variable: {vf_info.get('is_variable', False)}")
    print_info(f"Number of tables: {len(vf_info.get('tables', []))}")
    
    # Get static fonts info
    print_section("Static Fonts Analysis")
    static_info = {}
    for name, path in available_static.items():
        info = get_font_info(path)
        glyphs = get_glyph_names(path)
        cmap = get_cmap(path)
        static_info[name] = {
            'path': path,
            'info': info,
            'glyphs': glyphs,
            'cmap': cmap
        }
        print_info(f"{name}: {len(glyphs)} glyphs, {len(cmap)} mapped characters")
    
    # Compare glyphs
    print_section("Glyph Coverage Comparison")
    
    # Get union of all static font glyphs
    all_static_glyphs = set()
    for name, data in static_info.items():
        all_static_glyphs.update(data['glyphs'])
    
    print_info(f"Total unique glyphs across all static fonts: {len(all_static_glyphs)}")
    print_info(f"Variable font glyphs: {len(vf_glyphs)}")
    
    # Find differences
    vf_only = vf_glyphs - all_static_glyphs
    static_only = all_static_glyphs - vf_glyphs
    common = vf_glyphs & all_static_glyphs
    
    print_success(f"Common glyphs: {len(common)} ({len(common)/len(vf_glyphs)*100:.1f}% of VF)")
    
    if vf_only:
        print_warning(f"Glyphs only in VF: {len(vf_only)}")
        if len(vf_only) <= 20:
            print(f"  {', '.join(sorted(vf_only))}")
        else:
            print(f"  First 20: {', '.join(sorted(list(vf_only)[:20]))}")
    else:
        print_success("No glyphs exclusive to VF")
    
    if static_only:
        print_warning(f"Glyphs only in static fonts: {len(static_only)}")
        if len(static_only) <= 20:
            print(f"  {', '.join(sorted(static_only))}")
        else:
            print(f"  First 20: {', '.join(sorted(list(static_only)[:20]))}")
    else:
        print_success("No glyphs exclusive to static fonts")
    
    # Compare character coverage
    print_section("Character Coverage Comparison")
    
    all_static_chars = set()
    for name, data in static_info.items():
        all_static_chars.update(data['cmap'].keys())
    
    vf_chars = set(vf_cmap.keys())
    
    print_info(f"Total unique characters across all static fonts: {len(all_static_chars)}")
    print_info(f"Variable font characters: {len(vf_chars)}")
    
    vf_only_chars = vf_chars - all_static_chars
    static_only_chars = all_static_chars - vf_chars
    common_chars = vf_chars & all_static_chars
    
    print_success(f"Common characters: {len(common_chars)} ({len(common_chars)/len(vf_chars)*100:.1f}% of VF)")
    
    if vf_only_chars:
        print_warning(f"Characters only in VF: {len(vf_only_chars)}")
        if len(vf_only_chars) <= 20:
            chars_str = ', '.join([f"U+{c:04X} ({chr(c)})" if c < 0x10000 else f"U+{c:05X}" for c in sorted(vf_only_chars)])
            print(f"  {chars_str}")
    else:
        print_success("No characters exclusive to VF")
    
    if static_only_chars:
        print_warning(f"Characters only in static fonts: {len(static_only_chars)}")
        if len(static_only_chars) <= 20:
            chars_str = ', '.join([f"U+{c:04X} ({chr(c)})" if c < 0x10000 else f"U+{c:05X}" for c in sorted(static_only_chars)])
            print(f"  {chars_str}")
    else:
        print_success("No characters exclusive to static fonts")
    
    # Per-weight comparison
    print_section("Per-Weight Comparison")
    for name, data in static_info.items():
        static_glyphs = data['glyphs']
        missing_in_static = vf_glyphs - static_glyphs
        extra_in_static = static_glyphs - vf_glyphs
        
        coverage = len(vf_glyphs & static_glyphs) / len(vf_glyphs) * 100
        print_info(f"{name}: {coverage:.1f}% coverage of VF glyphs")
        
        if missing_in_static:
            print(f"  Missing from {name}: {len(missing_in_static)} glyphs")
        if extra_in_static:
            print(f"  Extra in {name}: {len(extra_in_static)} glyphs")
    
    # Summary
    print_header("📊 Summary")
    
    print(f"\n{Colors.CYAN}Variable Font (VF):{Colors.NC}")
    print(f"  • Glyphs: {len(vf_glyphs)}")
    print(f"  • Characters: {len(vf_chars)}")
    print(f"  • Tables: {len(vf_info.get('tables', []))}")
    
    print(f"\n{Colors.CYAN}Static Fonts (Combined):{Colors.NC}")
    print(f"  • Unique glyphs: {len(all_static_glyphs)}")
    print(f"  • Unique characters: {len(all_static_chars)}")
    print(f"  • Number of weights: {len(available_static)}")
    
    print(f"\n{Colors.CYAN}Coverage:{Colors.NC}")
    print(f"  • Common glyphs: {len(common)} ({len(common)/len(vf_glyphs)*100:.1f}% of VF)")
    print(f"  • VF-only glyphs: {len(vf_only)}")
    print(f"  • Static-only glyphs: {len(static_only)}")
    print(f"  • Common characters: {len(common_chars)} ({len(common_chars)/len(vf_chars)*100:.1f}% of VF)")
    print(f"  • VF-only characters: {len(vf_only_chars)}")
    print(f"  • Static-only characters: {len(static_only_chars)}")
    
    if len(vf_glyphs) == len(all_static_glyphs) and len(vf_only) == 0 and len(static_only) == 0:
        print(f"\n{Colors.GREEN}✅ Perfect match! VF and static fonts have identical glyph coverage.{Colors.NC}")
    elif len(vf_only) == 0 and len(static_only) == 0:
        print(f"\n{Colors.GREEN}✅ VF and static fonts have the same glyph set.{Colors.NC}")
    else:
        print(f"\n{Colors.YELLOW}⚠ VF and static fonts have different glyph coverage.{Colors.NC}")
    
    print()
    return 0


if __name__ == "__main__":
    sys.exit(compare_fonts())

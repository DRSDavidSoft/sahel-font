#!/usr/bin/env python3
"""
Enhance Sahel-VF with missing glyphs from static fonts
and add OpenType features for Farsi digit substitution
"""

import sys
from fontTools.ttLib import TTFont
from fontTools.feaLib.builder import addOpenTypeFeatures
from pathlib import Path

def copy_glyphs_from_static_to_vf(static_ttf_path, vf_ttf_path, output_path):
    """
    Copy missing glyphs from static font to variable font
    """
    print(f"Loading static font: {static_ttf_path}")
    static_font = TTFont(static_ttf_path)
    
    print(f"Loading variable font: {vf_ttf_path}")
    vf_font = TTFont(vf_ttf_path)
    
    static_glyphs = set(static_font.getGlyphOrder())
    vf_glyphs = set(vf_font.getGlyphOrder())
    
    missing_glyphs = static_glyphs - vf_glyphs
    
    print(f"\nFound {len(missing_glyphs)} missing glyphs in variable font")
    print(f"Sample missing glyphs: {sorted(list(missing_glyphs))[:20]}")
    
    # Copy glyph outlines
    print("\nCopying glyph outlines from glyf table...")
    copied_count = 0
    if 'glyf' in static_font and 'glyf' in vf_font:
        for glyph_name in sorted(missing_glyphs):
            if glyph_name in static_font['glyf'].glyphs:
                # Copy the glyph
                vf_font['glyf'].glyphs[glyph_name] = static_font['glyf'].glyphs[glyph_name]
                copied_count += 1
                if copied_count <= 10:
                    print(f"  Copied: {glyph_name}")
    
    print(f"  ... copied {copied_count} glyphs total")
    
    # Update glyph order
    print("\nUpdating glyph order...")
    new_glyph_order = list(vf_font.getGlyphOrder())
    for glyph in sorted(missing_glyphs):
        if glyph not in new_glyph_order:
            new_glyph_order.append(glyph)
    vf_font.setGlyphOrder(new_glyph_order)
    
    # Copy horizontal metrics
    print("\nUpdating horizontal metrics (hmtx)...")
    if 'hmtx' in static_font and 'hmtx' in vf_font:
        for glyph_name in missing_glyphs:
            if glyph_name in static_font['hmtx'].metrics:
                vf_font['hmtx'].metrics[glyph_name] = static_font['hmtx'].metrics[glyph_name]
    
    # Update cmap
    print("\nUpdating cmap table...")
    if 'cmap' in static_font and 'cmap' in vf_font:
        static_cmap = {}
        for table in static_font['cmap'].tables:
            static_cmap.update(table.cmap)
        
        # Find a suitable cmap table in VF to update
        for table in vf_font['cmap'].tables:
            for code, glyph in static_cmap.items():
                if glyph in missing_glyphs:
                    table.cmap[code] = glyph
    
    # Update maxp
    print("\nUpdating maxp table...")
    if 'maxp' in vf_font:
        vf_font['maxp'].numGlyphs = len(new_glyph_order)
    
    # Save the enhanced font
    print(f"\nSaving enhanced variable font to: {output_path}")
    vf_font.save(output_path)
    
    vf_font.close()
    static_font.close()
    
    print("\n✓ Glyph copying completed successfully!")
    return output_path

def add_farsi_digit_feature(font_path, output_path):
    """
    Add OpenType ss01 feature for Farsi digit substitution
    """
    print(f"\nAdding Farsi digit substitution feature...")
    print(f"Loading font: {font_path}")
    
    font = TTFont(font_path)
    
    # Define the feature code
    feature_code = """
# Stylistic Set 1: Farsi Digits
# Substitutes Western digits (0-9) with Farsi digit shapes
languagesystem DFLT dflt;
languagesystem arab dflt;

feature ss01 {
    sub zero by uni06F0;
    sub one by uni06F1;
    sub two by uni06F2;
    sub three by uni06F3;
    sub four by uni06F4;
    sub five by uni06F5;
    sub six by uni06F6;
    sub seven by uni06F7;
    sub eight by uni06F8;
    sub nine by uni06F9;
} ss01;
"""
    
    # Add the feature
    try:
        addOpenTypeFeatures(font, feature_code)
        print("✓ Added ss01 feature for Farsi digits")
    except Exception as e:
        print(f"Warning: Could not add feature automatically: {e}")
        print("Feature will need to be added manually to source files")
    
    # Save
    print(f"Saving font with features to: {output_path}")
    font.save(output_path)
    font.close()
    
    print("✓ Feature addition completed!")
    return output_path

def main():
    # Use script location to determine project root
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent
    dist_dir = base_dir / "dist"
    
    # Input files
    static_regular = dist_dir / "Sahel.ttf"
    vf_original = dist_dir / "Sahel-VF.ttf"
    
    # Output files
    vf_enhanced = dist_dir / "Sahel-VF-Enhanced.ttf"
    vf_final = dist_dir / "Sahel-VF-New.ttf"
    
    print("=" * 70)
    print("SAHEL VARIABLE FONT ENHANCEMENT")
    print("=" * 70)
    
    # Step 1: Copy glyphs
    print("\n[Step 1] Copying missing glyphs from static to variable font...")
    try:
        copy_glyphs_from_static_to_vf(static_regular, vf_original, vf_enhanced)
    except Exception as e:
        print(f"\n✗ Error during glyph copying: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Step 2: Add features
    print("\n[Step 2] Adding OpenType features...")
    try:
        add_farsi_digit_feature(vf_enhanced, vf_final)
    except Exception as e:
        print(f"\n✗ Error during feature addition: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "=" * 70)
    print("✓ ENHANCEMENT COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print(f"\nNew enhanced variable font: {vf_final}")
    print("\nNext steps:")
    print("1. Test the new font file")
    print("2. Generate WOFF2 version")
    print("3. Update documentation")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

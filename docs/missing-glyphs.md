# Glyph Set Parity Audit: Sahel-VF vs Static Variants

**Date:** 2025-12-03  
**Purpose:** Assess if the Sahel variable font (Sahel-VF) can serve as a complete replacement for all static font variants.

## Executive Summary

**Finding:** Sahel-VF currently **cannot** serve as a complete replacement without modifications.

**Missing Glyphs:** 223 glyphs are present in static fonts but absent in Sahel-VF  
**Recommendation:** Enhance Sahel-VF with missing glyphs and implement OpenType features for variant selection.

## Detailed Analysis

### Font Variant Comparison

| Font Variant | Glyph Count | Character Count | Western Digits | Farsi Digits | Latin Basic | Latin Extended |
|--------------|-------------|-----------------|----------------|--------------|-------------|----------------|
| **Sahel-VF** | **329** | **288** | **❌ 0** | **✅ 10** | **❌ 0** | **❌ 0** |
| Sahel-Regular | 552 | 545 | ✅ 10 | ✅ 10 | ✅ 52 | ✅ 38 |
| Sahel-FD | 552 | 545 | ✅ 10* | ✅ 10 | ✅ 52 | ✅ 38 |
| Sahel-WOL | 337 | 296 | ❌ 0 | ✅ 10 | ❌ 0 | ⚠️ 3 |
| Sahel-FD-WOL | 347 | 306 | ✅ 10* | ✅ 10 | ❌ 0 | ⚠️ 3 |

*FD variants: Western digit codepoints map to Farsi digit shapes

### Missing Glyphs in Sahel-VF

#### 1. Western Digits (10 glyphs)
```
U+0030 (0) - zero
U+0031 (1) - one
U+0032 (2) - two
U+0033 (3) - three
U+0034 (4) - four
U+0035 (5) - five
U+0036 (6) - six
U+0037 (7) - seven
U+0038 (8) - eight
U+0039 (9) - nine
```

#### 2. Latin Basic Alphabet (52 glyphs)
```
Uppercase: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
Lowercase: a b c d e f g h i j k l m n o p q r s t u v w x y z
```

#### 3. Latin Extended & Symbols (161 glyphs)
Including:
- Accented Latin characters (À, Á, É, etc.)
- Mathematical symbols (Δ, Ω, ≈, etc.)
- Currency symbols (€, ¢, £, etc.)
- Punctuation and special characters
- Common symbols (@, &, *, etc.)

### Variant-Specific Features

#### Farsi-Digits (FD) Variants
**Implementation Method:** Glyph component substitution
- Western digit glyphs (e.g., "eight") use Farsi digit glyphs (e.g., "uni06F8") as components
- Same glyph count as regular fonts (552)
- No OpenType features used for substitution

**Example from Sahel-FD.ttf:**
```xml
<TTGlyph name="eight">
  <component glyphName="uni06F8" x="0" y="0"/>
</TTGlyph>
```

#### Without-Latin (WOL) Variants
**Implementation Method:** Glyph removal
- Latin alphabet characters completely removed
- Reduces glyph count by ~215 glyphs
- Retains 3 Latin supplement characters needed for internal use
- 8 additional reference glyphs (.null, nonmarkingreturn, etc.)

## OpenType Features Analysis

### Current Features (All Variants)
All font variants use the same 9 OpenType features:
- `calt` - Contextual Alternates
- `fina` - Terminal Forms (Arabic)
- `init` - Initial Forms (Arabic)
- `kern` - Kerning
- `liga` - Standard Ligatures
- `mark` - Mark Positioning
- `medi` - Medial Forms (Arabic)
- `mkmk` - Mark to Mark Positioning
- `rlig` - Required Ligatures

### Missing Features for Variant Support
Currently **NO** OpenType features exist for:
- Switching between Western and Farsi digits
- Enabling/disabling Latin characters

## Recommendations

### 1. Enhance Sahel-VF to Include All Glyphs ✅ RECOMMENDED

**Benefits:**
- Single font file contains all character variants
- Reduces total file count from 42+ to 2 (TTF + WOFF2)
- Better for modern web usage
- Simplifies distribution and maintenance

**Implementation:**
- Add Western digits (0-9) to variable font source
- Add Latin alphabet (A-Z, a-z)
- Add extended Latin and symbols
- Ensure consistency across all weight masters

**File Size Impact:**
- Current Sahel-VF.ttf: ~28KB
- Current Sahel-Regular.ttf: ~73KB
- Estimated enhanced Sahel-VF.ttf: ~75-80KB
- Still reasonable for web usage

### 2. Implement OpenType Features for Digit Selection ✅ RECOMMENDED

**Proposed Feature:** Stylistic Set 1 (`ss01`)
- Purpose: Enable Farsi digits for Western digit codepoints
- Usage: `font-feature-settings: "ss01" 1;`
- Default: Western digits (0-9 display as Western numerals)
- With ss01: Western digits (0-9 display as Farsi numerals ۰-۹)

**Implementation Details:**
```fea
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
```

### 3. Handle Latin Character Variants ⚠️ NOT RECOMMENDED as OpenType Feature

**Reason:** Latin characters cannot be effectively removed via OpenType features
- OpenType features substitute glyphs but cannot remove them
- Would require substituting with empty glyphs (increases complexity)
- Better handled through separate build target if size optimization is critical

**Alternative Approaches:**
1. **Include Latin in default variable font** (RECOMMENDED)
   - Users who need Latin have it available
   - Users who don't need Latin simply don't use those characters
   - Minimal file size impact in WOFF2 format

2. **Separate WOL build** (if size critical)
   - Generate Sahel-VF-WOL.ttf as separate variant
   - Only for use cases where every KB matters
   - Keep as legacy support option

### 4. Migration Path

**Phase 1: Enhance Variable Font**
- ✅ Document current gaps
- Add missing glyphs to source files
- Implement `ss01` feature for Farsi digits
- Build enhanced Sahel-VF.ttf/woff2

**Phase 2: Documentation & Examples**
- Update README with new structure
- Provide CSS examples
- Create migration guide for existing users
- Document feature usage

**Phase 3: Deprecate Static Builds**
- Mark static fonts as legacy
- Keep pre-built versions for compatibility
- Update CI/CD to focus on variable font
- Update dist/ directory structure

## Technical Notes

### Variable Font Axes
Current axis:
- `wght` (Weight): 400-900 (Light, Regular, SemiBold, Bold, Black)

Potential future axes:
- `slnt` (Slant): For italic variants
- `wdth` (Width): For condensed variants

### Browser Support
OpenType features via CSS:
- `font-feature-settings`: Supported in all modern browsers
- `font-variation-settings`: Supported in all modern browsers
- Variable fonts: 97%+ global browser support

### Performance Considerations
- Variable font slightly larger than single static weight
- Much smaller than multiple static weights combined
- WOFF2 compression highly effective
- Recommended for web usage

## Conclusion

**Sahel-VF can and should become the default distribution** after implementing the recommended enhancements:

1. ✅ Add missing glyphs (Western digits, Latin alphabet, symbols)
2. ✅ Implement `ss01` for Farsi digit switching
3. ✅ Maintain single variable font as primary distribution
4. ⚠️ Keep static fonts for legacy support only
5. ❌ Do not implement Latin removal as OpenType feature

This approach provides maximum flexibility while maintaining minimal file sizes and complexity.

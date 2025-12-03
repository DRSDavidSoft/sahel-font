# Sahel Font - Development Repository

A Persian (Farsi) font with **enhanced variable font support**. This repository contains the source files and build tools for developing and building the Sahel font family.

![Sahel Variable Font Demo](./sample-variable.gif)

## ✨ What's New

**Enhanced Variable Font** - Now with complete Latin support and OpenType features!

- ✅ **Single file replaces 42+ static variants**
- ✅ **Complete character set**: Latin alphabet + Western & Farsi digits
- ✅ **OpenType feature `ss01`**: Switch between Western (0-9) and Farsi (۰-۹) digits via CSS
- ✅ **Smaller downloads**: 51.8 KB WOFF2 replaces multiple files
- ✅ **Flexible weights**: Any weight from 400-900, not just 5 fixed values
- ✅ **Backward compatible**: Static fonts still available for legacy support

## 🚀 Features

- **Variable font (Recommended)**: Single file with adjustable weight axis (400-900)
- **Complete character support**: Persian/Farsi, Arabic, Latin alphabet, and digits
- **OpenType features**: Contextual alternates, ligatures, and Farsi digit switching
- **Multiple formats**: TTF, WOFF2 (variable), plus legacy static files
- **Web-ready**: Modern CSS with font-feature-settings examples
- **Optimized**: Small file size with excellent compression

## 🎯 Quick Start - Using the Variable Font

### For Web Projects (Recommended)

```html
<!-- Add to your HTML <head> -->
<link rel="preload" href="Sahel-VF.woff2" as="font" type="font/woff2" crossorigin>
```

```css
/* Load the variable font */
@font-face {
  font-family: 'Sahel VF';
  src: url('Sahel-VF.woff2') format('woff2-variations'),
       url('Sahel-VF.ttf') format('truetype-variations');
  font-weight: 400 900;
  font-display: swap;
}

/* Basic usage */
body {
  font-family: 'Sahel VF', sans-serif;
  font-weight: 400;  /* Any value from 400 to 900 */
}

/* Use Farsi digits (۰-۹) instead of Western digits (0-9) */
.farsi-digits {
  font-feature-settings: "ss01" 1;
}
```

**See also:**
- 📄 [Complete CSS Examples](dist/sahel-vf-usage.css) - Comprehensive usage guide
- 🧪 [Interactive Test Page](dist/test-sahel-vf.html) - See it in action
- 📊 [Glyph Analysis Report](docs/missing-glyphs.md) - Technical details

### Migration from Old Fonts

**Before:** Using separate font files
```css
@font-face {
  font-family: 'SahelF';  /* Separate family for Farsi digits */
  src: url('Farsi-Digits/Sahel-FD.ttf');
}
```

**After:** Single variable font with feature toggle
```css
@font-face {
  font-family: 'Sahel VF';
  src: url('Sahel-VF.woff2') format('woff2-variations');
  font-weight: 400 900;
}

.farsi-digits {
  font-family: 'Sahel VF', sans-serif;
  font-feature-settings: "ss01" 1;  /* Enable Farsi digits */
}
```

**Benefits:**
- ✅ One file instead of many
- ✅ Better browser caching
- ✅ Smoother weight transitions
- ✅ Smaller total download size

## 📋 Prerequisites

To build the fonts from source, you'll need:

- **FontForge**: Font editor and converter
- **Python 3**: For build scripts and font enhancement
- **fontmake**: Python tool for building fonts
- **fonttools**: Python library for font manipulation

### Installing Dependencies

#### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install -y fontforge python3 python3-pip
pip3 install fontmake defcon fonttools brotli
```

#### macOS

```bash
brew install fontforge python3
pip3 install fontmake defcon fonttools brotli
```

#### Arch Linux

```bash
sudo pacman -S fontforge python python-pip
pip install fontmake defcon fonttools brotli
```

## 🔨 Building the Fonts

### Building Variable Font

To build the variable font from source files:

```bash
cd variable
./makevariable.sh ../dist
```

This will:
1. Convert SFD source files to UFO format
2. Fix feature definitions
3. Fix glyph compatibility issues for variable fonts
4. Clean up references to missing glyphs
5. Generate variable TTF font
6. Compress to WOFF2 format
7. Clean up temporary files

### Enhancing the Variable Font

To add Latin glyphs and OpenType features to the variable font:

```bash
# Ensure fonttools is installed
pip3 install fonttools brotli

# Run the enhancement script
python3 scripts/enhance_variable_font.py
```

This will:
1. Copy missing glyphs (Latin, Western digits) from static fonts
2. Add `ss01` OpenType feature for Farsi digit switching
3. Generate enhanced Sahel-VF.ttf and Sahel-VF.woff2

### Building Static Fonts (Legacy)

⚠️ **Deprecated:** The static font files are now superseded by the variable font.

The static font files (TTF, WOFF, WOFF2, EOT) for each weight are pre-built and available in the `dist/` directory for backward compatibility. They are kept for legacy browser support only.

## 📁 Repository Structure

```
sahel-font/
├── source/          # Source SFD (FontForge) files
│   ├── Sahel.sfd
│   ├── Sahel-Bold.sfd
│   ├── Sahel-Black.sfd
│   ├── Sahel-SemiBold.sfd
│   └── Sahel-Light.sfd
├── variable/        # Variable font build scripts
│   ├── makevariable.sh       # Main build script
│   ├── fix-features-fea.py   # Feature file fixer
│   ├── fontforge.pe          # FontForge script
│   └── Sahel.designspace     # Designspace file
├── scripts/         # Font enhancement tools
│   └── enhance_variable_font.py  # Add Latin glyphs and features
├── docs/            # Documentation
│   └── missing-glyphs.md     # Glyph parity analysis
├── dist/            # Built font files
│   ├── Sahel-VF.ttf          # ⭐ Enhanced variable font (recommended)
│   ├── Sahel-VF.woff2        # ⭐ Compressed variable font (recommended)
│   ├── sahel-vf-usage.css    # CSS usage examples
│   ├── test-sahel-vf.html    # Interactive test page
│   ├── Sahel*.ttf            # Legacy static fonts
│   ├── Sahel*.woff           # Legacy static fonts
│   ├── Sahel*.woff2          # Legacy static fonts
│   ├── Farsi-Digits/         # ⚠️ Deprecated - use ss01 feature instead
│   ├── Without-Latin/        # ⚠️ Deprecated - use variable font
│   └── font-face.css         # Legacy CSS declarations
├── .github/         # GitHub Actions workflows
│   └── workflows/
│       ├── build.yml         # CI/CD build workflow
│       └── release.yml       # Release workflow
├── validate_fonts.py # Font quality validation script
└── build.conf       # Build configuration
```

## 🧪 Testing

### Quick Test

Open the interactive test page in your browser:
```bash
# If you have Python installed
cd dist
python3 -m http.server 8000
# Then open http://localhost:8000/test-sahel-vf.html
```

### Validation

Test the variable font for quality and completeness:

```bash
# Validate font structure
python3 validate_fonts.py

# Check glyph count and features
python3 -c "
from fontTools.ttLib import TTFont
font = TTFont('dist/Sahel-VF.ttf')
print(f'Glyphs: {len(font.getGlyphOrder())}')
print(f'Features: {[f.FeatureTag for f in font[\"GSUB\"].table.FeatureList.FeatureRecord]}')
"
```

### Manual Testing

1. **Browser testing**: Open `dist/test-sahel-vf.html` to see live examples
2. **System installation**: Install `Sahel-VF.ttf` and test in applications
3. **FontForge inspection**: Open the font in FontForge to examine glyphs
4. **CSS testing**: Use examples from `dist/sahel-vf-usage.css`

### Feature Testing

Test the Farsi digit feature:
```html
<p style="font-family: 'Sahel VF'; font-feature-settings: 'ss01' 0;">
  Western: 0123456789
</p>
<p style="font-family: 'Sahel VF'; font-feature-settings: 'ss01' 1;">
  Farsi: 0123456789
</p>
```

## 🤝 Contributing

This is a fork of the original [Sahel Font](https://github.com/rastikerdar/sahel-font) repository. 

### Development Workflow

1. Modify source files in `source/` directory using FontForge
2. Build the variable font using the scripts in `variable/`
3. Test the built fonts
4. Commit your changes

### Code Style

- Shell scripts: Use clear variable names, add comments for complex operations
- Python scripts: Follow PEP 8 guidelines
- Add helpful console output with colors and emojis

## 📦 Continuous Integration

This repository includes GitHub Actions workflows for automated building and testing:

- **Build**: Automatically builds fonts on push and pull requests
- **Release**: Creates releases with built font artifacts
- **Artifact Upload**: Uploads built fonts as GitHub Actions artifacts

## 🐛 Known Issues

### Resolved Issues (DONE)

- ✓ **Latin character support**: Now included in variable font
- ✓ **Western digit support**: Now included with OpenType switching
- ✓ **Multiple font files needed**: Replaced by single variable font with features
- ✓ **Farsi digits**: Switchable via CSS `font-feature-settings: "ss01" 1`

### Current Limitations

- Mark placement may have minor distortion in some rare contexts
- Source SFD files still lack Latin glyphs (enhancement done at binary level)
- Static font variants still present for backward compatibility (can be removed in future)

## 📝 Roadmap

- [x] Enhance variable font with Latin and Western digits
- [x] Add OpenType `ss01` feature for Farsi digit switching
- [x] Create comprehensive documentation and examples
- [x] Generate interactive test page
- [ ] Update source .sfd files to include all glyphs
- [ ] Simplify build process to generate enhanced VF directly
- [ ] Add additional variable font axes (e.g., width, slant)
- [ ] Remove deprecated static font variants

## 📄 License

This project is licensed under the SIL Open Font License (OFL). See the [LICENSE](LICENSE) file for details.

## 🙏 Credits

- **Original Author**: Saber Rastikerdar ([@rastikerdar](https://github.com/rastikerdar))
- **Contributors**: Amin Abedi ([@aminabedi68](https://github.com/aminabedi68))
- **Tools**: Built with [FontForge](https://fontforge.github.io) and [fontTools](https://github.com/fonttools/fonttools)
- **Enhancement**: Variable font enhancement using fontTools

## 📚 Resources

- [Original Sahel Font Repository](https://github.com/rastikerdar/sahel-font)
- [Font Preview](http://rastikerdar.github.io/sahel-font/)
- [FontForge Documentation](https://fontforge.org/docs/)
- [Variable Fonts Guide](https://web.dev/variable-fonts/)
- [OpenType Feature Reference](https://docs.microsoft.com/en-us/typography/opentype/spec/featurelist)

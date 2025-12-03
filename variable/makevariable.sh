#!/usr/bin/env bash

# Sahel Variable Font Build Script
# This script builds the variable font from source files

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored messages
print_step() {
    echo -e "${CYAN}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if output directory is specified
if [ -z "$1" ]; then
    print_error "Output directory not specified!"
    print_info "Usage: $0 <output-directory>"
    exit 1
fi

OUTPUT_DIR="$1"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo ""
echo -e "${MAGENTA}╔═══════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║  🔤 Sahel Variable Font Builder 🔤      ║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════════════╝${NC}"
echo ""

# Check required tools
print_step "Checking required tools..."
command -v fontforge >/dev/null 2>&1 || { print_error "fontforge is not installed. Aborting."; exit 1; }
command -v python3 >/dev/null 2>&1 || { print_error "python3 is not installed. Aborting."; exit 1; }
command -v fontmake >/dev/null 2>&1 || { print_error "fontmake is not installed. Aborting."; exit 1; }
command -v woff2_compress >/dev/null 2>&1 || { print_error "woff2_compress is not installed. Aborting."; exit 1; }
print_success "All required tools are available"
echo ""

# Convert SFD to UFO format
print_step "📦 Converting source files to UFO format..."
print_info "Converting Sahel.sfd..."
fontforge -lang=ff -script ./fontforge.pe ../source/Sahel.sfd ./Sahel.ufo
print_info "Converting Sahel-Bold.sfd..."
fontforge -lang=ff -script ./fontforge.pe ../source/Sahel-Bold.sfd ./Sahel-Bold.ufo
print_info "Converting Sahel-Black.sfd..."
fontforge -lang=ff -script ./fontforge.pe ../source/Sahel-Black.sfd ./Sahel-Black.ufo
print_success "Conversion completed"
echo ""

# Fix feature files
print_step "🔧 Fixing feature definitions..."
print_info "Fixing Sahel.ufo/features.fea..."
python3 fix-features-fea.py "Sahel.ufo/features.fea" "Sahel.ufo/features.fea"
print_info "Fixing Sahel-Bold.ufo/features.fea..."
python3 fix-features-fea.py "Sahel-Bold.ufo/features.fea" "Sahel-Bold.ufo/features.fea"
print_info "Fixing Sahel-Black.ufo/features.fea..."
python3 fix-features-fea.py "Sahel-Black.ufo/features.fea" "Sahel-Black.ufo/features.fea"
print_success "Feature files fixed"
echo ""

# Fix glyph compatibility issues
print_step "🔧 Fixing glyph compatibility..."
python3 fix-compatibility.py
print_success "Compatibility fixes applied"
echo ""

# Clean up references to missing glyphs
print_step "🧹 Cleaning up features..."
python3 clean-features.py
print_success "Features cleaned"
echo ""

# Build variable font
print_step "🏗️  Building variable font..."
BUILD_OUTPUT=$(mktemp)
if fontmake -o variable -m Sahel.designspace --output-path="$OUTPUT_DIR/Sahel-VF.ttf" 2>&1 | tee "$BUILD_OUTPUT"; then
    print_success "Variable font built: $OUTPUT_DIR/Sahel-VF.ttf"
    rm -f "$BUILD_OUTPUT"
    echo ""
    
    # Compress to WOFF2
    print_step "📦 Compressing to WOFF2 format..."
    woff2_compress "$OUTPUT_DIR/Sahel-VF.ttf"
    print_success "WOFF2 file created: $OUTPUT_DIR/Sahel-VF.woff2"
    echo ""
    
    # Clean up temporary files
    print_step "🧹 Cleaning up temporary files..."
    rm -rf Sahel.ufo Sahel-Bold.ufo Sahel-Black.ufo
    print_success "Cleanup completed"
    echo ""
    
    echo -e "${GREEN}╔═══════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✨ Build completed successfully! ✨     ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════╝${NC}"
    echo ""
    print_info "Output files:"
    echo "  - $OUTPUT_DIR/Sahel-VF.ttf"
    echo "  - $OUTPUT_DIR/Sahel-VF.woff2"
    echo ""
else
    print_warning "Variable font build encountered compatibility issues"
    print_info "This is a known issue with the source files"
    print_info "Build log saved to: $BUILD_OUTPUT"
    echo ""
    
    # Clean up temporary files
    print_step "🧹 Cleaning up temporary files..."
    rm -rf Sahel.ufo Sahel-Bold.ufo Sahel-Black.ufo
    print_success "Cleanup completed"
    echo ""
    
    echo -e "${YELLOW}╔═══════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║  ⚠ Build completed with warnings ⚠      ║${NC}"
    echo -e "${YELLOW}╚═══════════════════════════════════════════╝${NC}"
    echo ""
    print_info "Note: Pre-built variable fonts are available in the dist/ directory"
    exit 1
fi

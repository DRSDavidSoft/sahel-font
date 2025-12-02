#!/usr/bin/env python3
"""
Font Quality Validation Script

This script validates font files to ensure they meet quality standards:
- File format validity
- Required tables presence
- Metadata completeness
- File size reasonableness
"""

import os
import sys
import subprocess
from pathlib import Path


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
    print(f"\n{Colors.MAGENTA}{'=' * 60}{Colors.NC}")
    print(f"{Colors.MAGENTA}  {message}{Colors.NC}")
    print(f"{Colors.MAGENTA}{'=' * 60}{Colors.NC}\n")


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


def check_ttx_available():
    """Check if ttx (fonttools) is available"""
    try:
        subprocess.run(['ttx', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def validate_ttf_structure(font_path):
    """Validate TTF font structure using ttx"""
    try:
        result = subprocess.run(
            ['ttx', '-l', font_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Count tables
        tables = [line.strip().split()[0] for line in result.stdout.split('\n') 
                  if line.strip() and not line.startswith('Listing') and not line.startswith('tag')]
        
        return True, len(tables), tables
    except subprocess.CalledProcessError as e:
        return False, 0, []


def check_required_tables(tables, is_variable=False):
    """Check if required font tables are present"""
    required_tables = ['head', 'hhea', 'maxp', 'post', 'name', 'cmap', 'glyf', 'loca', 'hmtx']
    variable_tables = ['fvar', 'gvar', 'HVAR']
    
    missing = []
    for table in required_tables:
        if table not in tables:
            missing.append(table)
    
    if is_variable:
        for table in variable_tables:
            if table not in tables:
                print_warning(f"Variable font table '{table}' is missing")
    
    return missing


def check_file_size(font_path, expected_min_kb=10, expected_max_kb=500):
    """Check if font file size is reasonable"""
    size_bytes = os.path.getsize(font_path)
    size_kb = size_bytes / 1024
    
    if size_kb < expected_min_kb:
        return False, size_kb, "too small"
    elif size_kb > expected_max_kb:
        return False, size_kb, "too large"
    else:
        return True, size_kb, "ok"


def validate_font(font_path, is_variable=False):
    """Validate a single font file"""
    print_section(f"Validating: {os.path.basename(font_path)}")
    
    # Check file exists
    if not os.path.exists(font_path):
        print_error("File not found!")
        return False
    
    # Check file size
    size_ok, size_kb, size_status = check_file_size(font_path)
    if size_ok:
        print_success(f"File size: {size_kb:.1f} KB ({size_status})")
    else:
        print_error(f"File size: {size_kb:.1f} KB ({size_status})")
        return False
    
    # Validate structure
    valid, table_count, tables = validate_ttf_structure(font_path)
    if not valid:
        print_error("Font structure validation failed!")
        return False
    
    print_success(f"Font structure is valid ({table_count} tables)")
    
    # Check required tables
    missing_tables = check_required_tables(tables, is_variable)
    if missing_tables:
        print_error(f"Missing required tables: {', '.join(missing_tables)}")
        return False
    else:
        print_success("All required tables present")
    
    print_success(f"Font validation passed: {os.path.basename(font_path)}")
    return True


def main():
    """Main validation function"""
    print_header("🔤 Sahel Font Quality Validation")
    
    # Check if ttx is available
    if not check_ttx_available():
        print_error("ttx (fonttools) is not available!")
        print_info("Install it with: pip install fonttools")
        return 1
    
    print_success("fonttools (ttx) is available")
    
    # Find the dist directory
    script_dir = Path(__file__).parent
    dist_dir = script_dir / 'dist'
    
    if not dist_dir.exists():
        print_error(f"dist directory not found: {dist_dir}")
        return 1
    
    print_info(f"Scanning fonts in: {dist_dir}")
    
    # Find all TTF files
    ttf_files = list(dist_dir.glob('*.ttf'))
    
    if not ttf_files:
        print_error("No TTF files found in dist directory!")
        return 1
    
    print_info(f"Found {len(ttf_files)} TTF files")
    
    # Validate each font
    results = []
    for font_path in sorted(ttf_files):
        is_variable = 'VF' in font_path.name
        result = validate_font(str(font_path), is_variable)
        results.append((font_path.name, result))
    
    # Print summary
    print_header("📊 Validation Summary")
    
    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed
    
    print(f"\nTotal fonts tested: {len(results)}")
    print_success(f"Passed: {passed}")
    if failed > 0:
        print_error(f"Failed: {failed}")
    
    # List failed fonts
    if failed > 0:
        print("\nFailed fonts:")
        for font_name, result in results:
            if not result:
                print(f"  - {font_name}")
        return 1
    else:
        print("\n" + Colors.GREEN + "🎉 All fonts passed validation!" + Colors.NC)
        return 0


if __name__ == "__main__":
    sys.exit(main())

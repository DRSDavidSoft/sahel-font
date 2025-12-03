#!/usr/bin/env python3
"""
Sahel Font Feature File Fixer

This script fixes positioning features in UFO feature files by:
- Removing empty positioning rules (< 0 0 0 0 >)
- Simplifying positioning rules to essential components
"""

import sys


# ANSI color codes
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color


def print_error(message):
    """Print error message in red"""
    print(f"{Colors.RED}✗ {message}{Colors.NC}")


def print_success(message):
    """Print success message in green"""
    print(f"{Colors.GREEN}✓ {message}{Colors.NC}")


def print_info(message):
    """Print info message in blue"""
    print(f"{Colors.BLUE}ℹ {message}{Colors.NC}")


def fix_line(line):
    r"""
    Fix a single line of feature code.
    
    The function processes positioning rules in the format:
    pos \uniXXXX <val1 val2 val3 val4> \uniYYYY <val5 val6 val7 val8> < val9 val10 val11 val12 >;
    
    We extract: [pos, \uniXXXX, \uniYYYY] + [<, val9, val10, val11, val12, >;]
    Which simplifies to: pos \uniXXXX \uniYYYY < val9 val10 val11 val12 >;
    
    Args:
        line: A line from the feature file
        
    Returns:
        Fixed line or empty string if line should be removed
    """
    trimmed_line = line.strip()
    
    # Only process positioning rules
    if not trimmed_line.startswith("pos uni"):
        return line

    # Remove empty positioning rules
    if trimmed_line.endswith("< 0 0 0 0 >;"):
        return ""

    # Simplify positioning rules by extracting key components
    # Expected format has 11 parts after splitting
    parts = list(filter(lambda x: x != "", trimmed_line.split(" ")))
    if len(parts) != 11:
        return line

    # Extract: command (parts[0]), glyph1 (parts[1]), glyph2 (parts[6]), 
    # and final positioning values (parts[-4:])
    return " ".join([parts[0], parts[1], parts[6]] + parts[-4:]) + "\n"


def main():
    """Main function to process feature files"""
    if len(sys.argv) < 3:
        print_error("Missing required arguments")
        print("Usage: fix-features-fea.py <input-file> <output-file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    print_info(f"Processing: {input_file}")

    try:
        # Read input file
        with open(input_file, 'r', encoding='utf-8') as f:
            input_lines = f.readlines()

        # Process lines
        fixed_lines = [fix_line(line) for line in input_lines]
        
        # Count changes
        original_count = len(input_lines)
        fixed_count = len([line for line in fixed_lines if line])
        removed_count = original_count - fixed_count

        # Write output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("".join(fixed_lines))

        print_success(f"Fixed {input_file}")
        if removed_count > 0:
            print_info(f"  Removed {removed_count} empty positioning rules")
        
        return 0

    except FileNotFoundError:
        print_error(f"File not found: {input_file}")
        return 1
    except Exception as e:
        print_error(f"Error processing file: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

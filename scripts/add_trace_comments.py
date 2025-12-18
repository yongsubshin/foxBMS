#!/usr/bin/env python3
"""
Add @trace comments to foxBMS source code.

This script reads the traceability matrix and adds @trace comments
after existing @requirement tags to show the full traceability chain.

Usage:
    python3 scripts/add_trace_comments.py [--dry-run]

Author: PARVIS-AICoder-Doxygen v1.1.0
Date: 2025-12-19
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Tuple, List, Optional

# Configuration
BASE_DIR = Path(__file__).parent.parent
FOXBMS_SRC = BASE_DIR / "foxbms-2" / "src"
MATRIX_FILE = BASE_DIR / "docs" / "parvis" / "traceability" / "full-traceability-matrix.json"

# Statistics
stats = {
    "files_scanned": 0,
    "files_modified": 0,
    "traces_added": 0,
    "traces_skipped": 0,
    "errors": []
}


def load_traceability_matrix() -> Dict[str, Tuple[str, str]]:
    """
    Load traceability matrix and build SW-REQ -> (SYS-REQ, TC) mapping.

    Returns:
        Dictionary mapping sw_req_id to (sys_req_id, tc_id) tuple
    """
    with open(MATRIX_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    mapping = {}
    for row in data.get('matrix', []):
        sw_req_id = row.get('sw_req_id', '')
        sys_req_id = row.get('sys_req_id', '')
        tc_id = row.get('tc_id', '')

        if sw_req_id:
            mapping[sw_req_id] = (sys_req_id, tc_id)

    return mapping


def find_source_files() -> List[Path]:
    """Find all C and H source files in foxBMS."""
    files = []
    for ext in ['*.c', '*.h']:
        files.extend(FOXBMS_SRC.rglob(ext))
    return sorted(files)


def process_file(filepath: Path, trace_mapping: Dict[str, Tuple[str, str]], dry_run: bool = False) -> bool:
    """
    Process a single source file, adding @trace comments.

    Args:
        filepath: Path to the source file
        trace_mapping: SW-REQ -> (SYS-REQ, TC) mapping
        dry_run: If True, don't modify files

    Returns:
        True if file was modified, False otherwise
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            original_content = content
    except Exception as e:
        stats["errors"].append(f"Read error {filepath}: {e}")
        return False

    # Pattern to find @requirement{ID} tags
    # Match: * @requirement{SW-REQ-XXX} or  * @requirement{FSR-XXX}
    pattern = r'(\s*\*\s*@requirement\{([A-Z0-9-]+)\})'

    modified = False

    def replace_func(match):
        nonlocal modified
        full_match = match.group(1)
        req_id = match.group(2)

        # Check if @trace already exists for this requirement
        # Look ahead to see if next line has @trace
        pos = match.end()
        next_lines = content[pos:pos+200]
        if '@trace' in next_lines.split('\n')[0:2]:
            stats["traces_skipped"] += 1
            return full_match

        # Get traceability info
        if req_id in trace_mapping:
            sys_req, tc_id = trace_mapping[req_id]
            if sys_req and tc_id:
                trace_comment = f"\n *  @trace {sys_req} -> {req_id} -> {tc_id}"
                modified = True
                stats["traces_added"] += 1
                return full_match + trace_comment

        return full_match

    new_content = re.sub(pattern, replace_func, content)

    if modified and not dry_run:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
        except Exception as e:
            stats["errors"].append(f"Write error {filepath}: {e}")
            return False

    return modified


def main():
    dry_run = '--dry-run' in sys.argv

    print("=" * 60)
    print("PARVIS @trace Comment Generator v1.1.0")
    print("=" * 60)

    if dry_run:
        print("\n[DRY RUN MODE - No files will be modified]\n")

    # Load traceability matrix
    print(f"Loading traceability matrix from {MATRIX_FILE}...")
    trace_mapping = load_traceability_matrix()
    print(f"  Loaded {len(trace_mapping)} requirement mappings")

    # Find source files
    print(f"\nScanning source files in {FOXBMS_SRC}...")
    source_files = find_source_files()
    print(f"  Found {len(source_files)} source files")

    # Process each file
    print("\nProcessing files...")
    for filepath in source_files:
        stats["files_scanned"] += 1
        if process_file(filepath, trace_mapping, dry_run):
            stats["files_modified"] += 1
            rel_path = filepath.relative_to(BASE_DIR)
            print(f"  [MODIFIED] {rel_path}")

    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Files scanned:    {stats['files_scanned']}")
    print(f"  Files modified:   {stats['files_modified']}")
    print(f"  @trace added:     {stats['traces_added']}")
    print(f"  @trace skipped:   {stats['traces_skipped']} (already exists)")

    if stats["errors"]:
        print(f"\n  Errors: {len(stats['errors'])}")
        for err in stats["errors"][:10]:
            print(f"    - {err}")

    if dry_run:
        print("\n[DRY RUN - No changes were made]")
    else:
        print("\n[COMPLETE - Changes applied]")

    return 0 if not stats["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())

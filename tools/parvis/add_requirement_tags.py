#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PARVIS Requirement Traceability Tag Insertion Tool

This script reads requirement data from unified-requirements.json and inserts
@requirement{FBMS-xxx-xxx-xxx} tags into foxBMS source files.

Strategy:
1. For file-level requirements, add tags to file header Doxygen block
2. For function-level requirements, find the function's Doxygen block
3. Create Doxygen blocks if they don't exist

Usage:
    python3 add_requirement_tags.py [--dry-run] [--module MODULE]
"""

import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Base paths
FOXBMS_ROOT = Path("/home/kevin/work/forBMS/foxBMS")
REQUIREMENTS_FILE = FOXBMS_ROOT / "docs/parvis/requirements/unified-requirements.json"
SOURCE_ROOT = FOXBMS_ROOT / "foxbms-2/src/app"


class RequirementTagger:
    """Handles insertion of @requirement tags into source files."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.requirements = []
        self.file_requirements: Dict[str, List[dict]] = defaultdict(list)
        self.stats = {
            "files_processed": 0,
            "files_modified": 0,
            "requirements_linked": 0,
            "requirements_skipped": 0,
            "errors": []
        }

    def load_requirements(self) -> bool:
        """Load requirements from JSON file."""
        try:
            with open(REQUIREMENTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.requirements = data.get('requirements', [])

            # Group requirements by source file
            for req in self.requirements:
                source = req.get('source', {})
                source_file = source.get('file', '')

                if source_file and (source_file.endswith('.c') or source_file.endswith('.h')):
                    # Normalize path
                    full_path = FOXBMS_ROOT / source_file
                    if full_path.exists():
                        self.file_requirements[str(full_path)].append({
                            'fbms_id': req.get('fbms_id'),
                            'line': source.get('line'),
                            'extraction_type': source.get('extraction_type'),
                            'content': req.get('content', '')[:100]
                        })

            print(f"Loaded {len(self.requirements)} requirements")
            print(f"Found {len(self.file_requirements)} files with requirements")
            return True

        except Exception as e:
            print(f"Error loading requirements: {e}")
            return False

    def parse_line_spec(self, line_spec: str) -> Tuple[int, int]:
        """Parse line specification like '115-152', '87', or '83,94'."""
        if not line_spec:
            return (0, 0)

        line_spec = str(line_spec).strip()

        try:
            # Handle range like '115-152'
            if '-' in line_spec:
                parts = line_spec.split('-')
                start = int(parts[0].strip())
                end = int(parts[1].strip())
                return (start, end)

            # Handle comma-separated like '83,94' or '79,342'
            if ',' in line_spec:
                parts = line_spec.split(',')
                # Use first line number
                first_line = int(parts[0].strip())
                return (first_line, first_line)

            # Single line
            line_num = int(line_spec)
            return (line_num, line_num)

        except (ValueError, IndexError):
            return (0, 0)

    def find_file_header_block(self, lines: List[str]) -> Tuple[int, int]:
        """Find the file header Doxygen block (/** @file ... */)."""
        block_start = -1
        block_end = -1
        in_file_block = False

        for i, line in enumerate(lines):
            stripped = line.strip()

            if stripped.startswith('/**'):
                block_start = i

            if block_start != -1:
                if '@file' in line:
                    in_file_block = True

                if stripped.endswith('*/') and in_file_block:
                    block_end = i
                    return (block_start, block_end)

                if stripped.endswith('*/') and not in_file_block:
                    # Reset - this was not a file header block
                    block_start = -1

        return (-1, -1)

    def find_function_doxygen_block(self, lines: List[str], target_line: int) -> Tuple[int, int]:
        """Find Doxygen block for function at target_line."""
        # Search backwards from target_line
        block_end = -1
        block_start = -1

        for i in range(target_line - 1, max(0, target_line - 60), -1):
            if i >= len(lines):
                continue

            stripped = lines[i].strip()

            # Skip empty lines
            if not stripped:
                continue

            # Found end of a Doxygen block
            if stripped.endswith('*/') and block_end == -1:
                block_end = i
                continue

            # Check if we found the start of the block
            if block_end != -1:
                if stripped.startswith('/**'):
                    block_start = i
                    return (block_start, block_end)
                elif not stripped.startswith('*') and not stripped.startswith('/*'):
                    # Hit non-comment content before finding start
                    return (-1, -1)
            else:
                # If we hit non-comment content before finding block end, no block exists
                if not stripped.startswith('*') and not stripped.startswith('//') and not stripped.startswith('/*'):
                    return (-1, -1)

        return (-1, -1)

    def find_function_start(self, lines: List[str], target_line: int) -> int:
        """Find the start line of a function containing target_line."""
        # Search backwards for function definition
        for i in range(target_line - 1, max(0, target_line - 50), -1):
            if i >= len(lines):
                continue

            stripped = lines[i].strip()

            # Check for function/extern/static declaration patterns
            patterns = [
                r'^(static\s+)?(extern\s+)?[\w_]+\s+[\w_]+\s*\([^;]*$',  # function def start
                r'^(static\s+)?(extern\s+)?[\w_]+\s+[\w_]+\s*\([^)]*\)\s*\{',  # function def with brace
                r'^(static\s+)?(extern\s+)?[\w_]+\s+[\w_]+\s*\([^)]*\)\s*;',  # function declaration
                r'^typedef\s+(struct|enum)',  # typedef
                r'^#define\s+\w+',  # macro
            ]

            for pattern in patterns:
                if re.match(pattern, stripped):
                    return i

        return target_line - 1

    def has_requirement_tag(self, lines: List[str], start: int, end: int, fbms_id: str) -> bool:
        """Check if requirement tag already exists in Doxygen block."""
        for i in range(start, min(end + 1, len(lines))):
            if f'@requirement{{{fbms_id}}}' in lines[i]:
                return True
        return False

    def add_requirement_to_block(self, lines: List[str], block_end: int, fbms_id: str) -> List[str]:
        """Add @requirement tag to existing Doxygen block before the closing */."""
        # Get the indentation from the closing line
        end_line = lines[block_end]
        indent_match = re.match(r'^(\s*)', end_line)
        indent = indent_match.group(1) if indent_match else ""

        req_line = f"{indent} * @requirement{{{fbms_id}}}\n"

        # Insert before the closing */
        new_lines = lines[:block_end]
        new_lines.append(req_line)
        new_lines.extend(lines[block_end:])

        return new_lines

    def create_doxygen_block_with_requirement(self, fbms_id: str, indent: str = "") -> List[str]:
        """Create a minimal Doxygen block with requirement tag."""
        return [
            f"{indent}/**\n",
            f"{indent} * @requirement{{{fbms_id}}}\n",
            f"{indent} */\n"
        ]

    def get_indent(self, line: str) -> str:
        """Get the indentation of a line."""
        match = re.match(r'^(\s*)', line)
        return match.group(1) if match else ""

    def process_file(self, file_path: str, requirements: List[dict]) -> bool:
        """Process a single file and add requirement tags."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            lines = content.split('\n')
            # Add newline markers for reconstruction
            lines = [line + '\n' for line in lines[:-1]] + [lines[-1]]

            modified = False

            # Find file header block
            file_header_start, file_header_end = self.find_file_header_block(lines)

            # Sort requirements by line number (descending to avoid offset issues)
            sorted_reqs = sorted(requirements,
                                 key=lambda r: self.parse_line_spec(r['line'])[0],
                                 reverse=True)

            for req in sorted_reqs:
                fbms_id = req['fbms_id']
                line_start, line_end = self.parse_line_spec(req['line'])

                if line_start == 0:
                    self.stats["requirements_skipped"] += 1
                    continue

                # Determine if this is a file-level or function-level requirement
                # File-level: extraction_type is 'config', 'interface', or line is in header area
                extraction_type = req.get('extraction_type', '')
                is_file_level = extraction_type in ['config', 'state_machine'] or line_start < 100

                if is_file_level and file_header_end != -1:
                    # Add to file header block
                    if not self.has_requirement_tag(lines, file_header_start, file_header_end, fbms_id):
                        lines = self.add_requirement_to_block(lines, file_header_end, fbms_id)
                        file_header_end += 1  # Adjust for inserted line
                        modified = True
                        self.stats["requirements_linked"] += 1
                    else:
                        self.stats["requirements_skipped"] += 1
                else:
                    # Function-level requirement
                    adjusted_line = line_start - 1  # 0-indexed

                    # Find function start
                    func_start = self.find_function_start(lines, adjusted_line)

                    # Find existing Doxygen block for function
                    block_start, block_end = self.find_function_doxygen_block(lines, func_start)

                    if block_start != -1 and block_end != -1:
                        # Check if requirement already exists
                        if not self.has_requirement_tag(lines, block_start, block_end, fbms_id):
                            lines = self.add_requirement_to_block(lines, block_end, fbms_id)
                            modified = True
                            self.stats["requirements_linked"] += 1
                        else:
                            self.stats["requirements_skipped"] += 1
                    else:
                        # Create new Doxygen block before function
                        indent = self.get_indent(lines[func_start]) if func_start < len(lines) else ""
                        new_block = self.create_doxygen_block_with_requirement(fbms_id, indent)

                        # Insert before function
                        lines = lines[:func_start] + new_block + lines[func_start:]
                        modified = True
                        self.stats["requirements_linked"] += 1

            if modified and not self.dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(''.join(lines))

            self.stats["files_processed"] += 1
            if modified:
                self.stats["files_modified"] += 1

            return True

        except Exception as e:
            self.stats["errors"].append(f"{file_path}: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def run(self, target_module: Optional[str] = None) -> Dict:
        """Run the tagging process."""
        if not self.load_requirements():
            return self.stats

        # Process each file
        for file_path, requirements in sorted(self.file_requirements.items()):
            # Filter by module if specified
            if target_module:
                if target_module not in file_path:
                    continue

            print(f"Processing: {file_path} ({len(requirements)} requirements)")
            self.process_file(file_path, requirements)

        return self.stats


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Add @requirement tags to foxBMS source files")
    parser.add_argument("--dry-run", action="store_true", help="Don't modify files, just report what would be done")
    parser.add_argument("--module", type=str, help="Only process specific module (e.g., 'algorithm', 'driver/sbc')")

    args = parser.parse_args()

    print("=" * 60)
    print("PARVIS Requirement Traceability Tag Insertion Tool")
    print("=" * 60)

    if args.dry_run:
        print("DRY RUN MODE - No files will be modified")

    tagger = RequirementTagger(dry_run=args.dry_run)
    stats = tagger.run(target_module=args.module)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Files processed:      {stats['files_processed']}")
    print(f"Files modified:       {stats['files_modified']}")
    print(f"Requirements linked:  {stats['requirements_linked']}")
    print(f"Requirements skipped: {stats['requirements_skipped']}")

    if stats['errors']:
        print(f"\nErrors ({len(stats['errors'])}):")
        for error in stats['errors']:
            print(f"  - {error}")

    return 0 if not stats['errors'] else 1


if __name__ == "__main__":
    sys.exit(main())

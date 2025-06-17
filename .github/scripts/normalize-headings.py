#!/usr/bin/env python3
"""
normalize-headings.py

Fixes Markdown heading structure:

• Promotes only the first heading to H1 (if it starts deeper)
• Demotes duplicate H1s to H2
• Closes skipped levels (e.g. H1 → H3 becomes H1 → H2)
• Ignores headings inside fenced code-blocks

Usage:
    # Quiet mode (default)
    python normalize-headings.py file1.md file2.md …

    # Verbose mode
    python normalize-headings.py -v file1.md
    python normalize-headings.py --verbose file1.md file2.md
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+")
CODE_FENCE_RE = re.compile(r"^```")

def normalize(path: Path, verbose: bool = False) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []

    in_code       = False
    first_level   = None          # depth of the very first heading
    saw_h1        = False
    last_level    = 1             # depth of previous heading
    changed       = False         # did we modify the file?

    for idx, line in enumerate(lines, start=1):
        stripped = line.lstrip()

        # ───── Detect (and toggle) code-fence context ─────
        if CODE_FENCE_RE.match(stripped):
            in_code = not in_code
            out.append(line)
            continue

        # ───── Process headings outside code fences ─────
        m = None if in_code else HEADING_RE.match(stripped)
        if not m:
            out.append(line)
            continue

        orig_hashes = m.group(1)
        level       = len(orig_hashes)

        # record depth of first heading
        if first_level is None:
            first_level = level

        # 1) Promote only the first heading
        if first_level > 1:
            level -= (first_level - 1)
            level = max(1, level)

        # 2) Ensure exactly one H1
        if level == 1:
            if saw_h1:
                level = 2          # demote duplicate H1
            else:
                saw_h1 = True

        # 3) Close skipped levels
        if level > last_level + 1:
            level = last_level + 1

        last_level = level

        # Replace hashes if level changed
        new_hashes = "#" * level
        if new_hashes != orig_hashes:
            changed = True
            line = HEADING_RE.sub(f"{new_hashes} ", line, count=1)
            if verbose:
                print(f"{path}:{idx}: {orig_hashes} → {new_hashes}")

        out.append(line)

    # ───── Write back if anything changed ─────
    if changed:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
        if verbose:
            print(f"✓ fixed {path}")
    elif verbose:
        print(f"✓ {path} already OK")

def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize Markdown heading levels.")
    parser.add_argument("files", metavar="FILE", nargs="+", help="Markdown files to process")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print details of each heading fix")
    args = parser.parse_args()

    for file_str in args.files:
        normalize(Path(file_str), verbose=args.verbose)

if __name__ == "__main__":
    main()

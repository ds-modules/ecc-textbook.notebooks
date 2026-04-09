#!/usr/bin/env python3
"""Regenerate project.toc in myst.yml from ecc-* notebook folders."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

PRETTY = {
    "ecc-biology": "Biology",
    "ecc-biotech": "Biotech",
    "ecc-statistics": "Statistics",
    "ecc-cs9": "CS 9",
    "ecc-cis": "Computer Information Systems",
    "ecc-calculus": "Calculus",
    "ecc-business": "Business",
    "ecc-sociology": "Sociology",
    "ecc-ethnic-studies": "Ethnic Studies",
    "ecc-chemistry": "Chemistry",
    "ecc-child-development": "Child Development",
    "ecc-physics": "Physics",
    "ecc-music": "Music",
    "ecc-ai": "Artificial Intelligence",
    "ecc-psychology": "Psychology",
}


def display_title(module_name: str) -> str:
    return PRETTY.get(
        module_name,
        re.sub(r"^ecc-", "", module_name).replace("-", " ").title(),
    )


def collect_toc(scan_root: Path) -> list[dict]:
    toc = [{"file": "intro.md"}]
    notebook_count = 0

    modules = sorted(
        p
        for p in scan_root.iterdir()
        if p.is_dir() and p.name.startswith("ecc-")
    )

    for module_path in modules:
        children = []
        for nb in sorted(module_path.rglob("*.ipynb")):
            if "ipynb_checkpoints" in nb.parts:
                continue
            rel = nb.relative_to(scan_root)
            children.append({"file": str(rel).replace("\\", "/")})

        if children:
            notebook_count += len(children)
            toc.append(
                {
                    "title": display_title(module_path.name),
                    "children": children,
                }
            )

    if notebook_count == 0:
        raise ValueError("No notebooks found under ecc-* folders; refusing to overwrite project.toc.")

    return toc


def update_myst_toc(myst_yml: Path, scan_root: Path) -> None:
    if not myst_yml.exists():
        raise FileNotFoundError(f"myst.yml not found: {myst_yml}")
    if not scan_root.exists():
        raise FileNotFoundError(f"scan root not found: {scan_root}")

    data = yaml.safe_load(myst_yml.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping at top level in {myst_yml}")

    project = data.get("project")
    if not isinstance(project, dict):
        project = {}
        data["project"] = project

    toc = collect_toc(scan_root)
    if toc[0].get("file") != "intro.md":
        raise ValueError("First TOC entry must be intro.md")

    project["toc"] = toc

    myst_yml.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--myst-yml",
        required=True,
        type=Path,
        help="Path to myst.yml to update",
    )
    parser.add_argument(
        "--scan-root",
        required=True,
        type=Path,
        help="Root to scan for ecc-* modules and notebooks",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        update_myst_toc(myst_yml=args.myst_yml, scan_root=args.scan_root)
    except Exception as exc:  # pragma: no cover - CLI error path
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python
"""Bundled with the ports-and-adapters skill: verify the hexagon's dependency rule.

Scans the domain files of a checkout package and reports any that import a concrete
adapter. The domain must depend only on ports — this is the check to run after adding
a capability or refactoring, before you trust the design.

Usage:
    python check_architecture.py [PACKAGE_DIR]     # default: ./checkout

Exit 0 = clean, 1 = violations found.
"""
import os
import re
import sys

DOMAIN_FILES = ["money.py", "model.py", "ports.py", "service.py"]
FORBIDDEN = re.compile(r"^\s*(from\s+\S*adapters|import\s+\S*adapters)", re.MULTILINE)


def scan_file(path):
    """Return a list of violation strings for one file, or None if it's absent."""
    try:
        with open(path, encoding="utf-8") as fh:
            source = fh.read()
    except OSError:
        return None
    return [
        f"{path}:{source[: m.start()].count(chr(10)) + 1}: {m.group().strip()}"
        for m in FORBIDDEN.finditer(source)
    ]


def find_violations(pkg):
    """Return (files_checked, violation_strings) for a package's domain files."""
    scanned = [scan_file(os.path.join(pkg, name)) for name in DOMAIN_FILES]
    present = [hits for hits in scanned if hits is not None]
    violations = [v for hits in present for v in hits]
    return len(present), violations


def report(pkg, checked, violations):
    """Print the result and return the process exit code."""
    if checked == 0:
        print(f"nothing to check: no domain files found under {pkg!r} "
              "(is the code still one tangled module?)")
        return 0
    if not violations:
        print(f"PASS — the {pkg!r} domain depends only on ports.")
        return 0
    print("VIOLATION — the domain depends on a concrete adapter (it must use ports only):")
    print("\n".join(f"  {v}" for v in violations))
    print("Fix: inject a port instead, and wire the concrete only in main.py.")
    return 1


def main():
    pkg = sys.argv[1] if len(sys.argv) > 1 else "checkout"
    checked, violations = find_violations(pkg)
    return report(pkg, checked, violations)


if __name__ == "__main__":
    sys.exit(main())

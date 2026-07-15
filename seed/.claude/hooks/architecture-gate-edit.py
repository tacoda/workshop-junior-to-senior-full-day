#!/usr/bin/env python3
"""FAST design feedback: keep the hexagon's dependencies pointing inward.

A hook is not only for values — it can guard a *design invariant*. The
ports-and-adapters rule is: the domain depends only on ports, never on a concrete
adapter. This gate greps the domain files for any import of checkout.adapters and
blocks it.

Wired as a PostToolUse hook on Edit/Write, so it fires the instant a domain file
is saved with a forbidden import. This is the *tight* loop:

  * Speed:       immediate — the agent is corrected mid-task.
  * Consequence: the coupling existed on disk for a moment, but nothing was built
                 on it yet, so the fix is cheap and local.

The shipped test suite can't see this violation — the code stays green while the
architecture rots. That gap is why a design invariant sometimes needs a gate of
its own. Compare with architecture-gate-commit.py, the *coarse* loop.
"""
import os
import re
import sys

# The core of the hexagon. None of these may import a concrete adapter.
DOMAIN_FILES = [
    "checkout/money.py",
    "checkout/model.py",
    "checkout/ports.py",
    "checkout/service.py",
]
FORBIDDEN = re.compile(r"^\s*(from\s+\S*adapters|import\s+\S*adapters)", re.MULTILINE)

sys.stdin.read()  # PostToolUse payload; we re-check the files on disk regardless

seed_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for rel in DOMAIN_FILES:
    path = os.path.join(seed_dir, rel)
    try:
        with open(path, encoding="utf-8") as fh:
            source = fh.read()
    except OSError:
        # No checkout/ package yet (the code is still the tangled checkout.py) —
        # nothing for this gate to guard until the refactor creates the domain files.
        continue
    if FORBIDDEN.search(source):
        print(
            f"architecture-gate (edit): {rel} imports a concrete adapter — the domain must "
            "depend ONLY on ports (checkout/ports.py), never on checkout.adapters.\n"
            "Caught at edit time: fix it now, before you build on it. This breaks the hexagon — "
            "the core now knows about the outside world it was meant to be insulated from. "
            "Define a port for the new concern, inject it, and wire the concrete only in main.py.",
            file=sys.stderr,
        )
        sys.exit(2)

sys.exit(0)

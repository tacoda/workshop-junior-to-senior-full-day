#!/usr/bin/env python3
"""LATE design feedback: block the commit if the domain depends on an adapter.

Same ports-and-adapters check as architecture-gate-edit.py, wired as a PreToolUse
hook on Bash and gating only `git commit`. It fires at ship time, after the agent
may have edited, tested, and built more on the coupled code. This is the *coarse*
loop:

  * Speed:       late — only when the change tries to land.
  * Consequence: nothing broken ever ships, but by now the coupling may be buried
                 under later work, so untangling it costs more than catching it on save.

Compare with architecture-gate-edit.py, the *tight* loop. Same check, later
position — that gap is the lesson about where to close a feedback loop.
"""
import json
import os
import re
import sys

data = json.load(sys.stdin)
command = data.get("tool_input", {}).get("command", "")

# PreToolUse fires on every Bash call. Only gate commits; let the rest through.
if "git commit" not in command:
    sys.exit(0)

DOMAIN_FILES = [
    "checkout/money.py",
    "checkout/model.py",
    "checkout/ports.py",
    "checkout/service.py",
]
FORBIDDEN = re.compile(r"^\s*(from\s+\S*adapters|import\s+\S*adapters)", re.MULTILINE)

seed_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
for rel in DOMAIN_FILES:
    path = os.path.join(seed_dir, rel)
    try:
        with open(path, encoding="utf-8") as fh:
            source = fh.read()
    except OSError:
        continue
    if FORBIDDEN.search(source):
        print(
            f"architecture-gate (commit): BLOCKED. {rel} imports a concrete adapter — the "
            "domain must depend ONLY on ports (checkout/ports.py), never on checkout.adapters.\n"
            "Caught at commit time: the change cannot land until the coupling is removed. "
            "Define a port for the new concern, inject it, and wire the concrete only in main.py.",
            file=sys.stderr,
        )
        sys.exit(2)

sys.exit(0)

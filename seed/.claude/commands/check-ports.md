---
description: Audit a file for ports-and-adapters violations against the charter
argument-hint: [file to audit]
---

Audit this file against the charter's ports-and-adapters rule (see CLAUDE.md and
.claude/rules/architecture-concrete.md). Do not change anything — report only.

File: $ARGUMENTS

Check, and report each as PASS or VIOLATION with the exact line:

1. **Domain depends only on ports.** Does any domain file import `checkout.adapters.*`?
2. **No business decisions in adapters.** Does any adapter make a policy choice (who is a
   member, what the tax rate is, how to discount) instead of just implementing mechanics?
3. **Concretes wired only in main.py.** Is a concrete adapter constructed anywhere but the
   composition root?
4. **New concerns enter through a port.** Is there logic that should sit behind a port
   (pricing, payment, receipts, persistence, discounts) but is inlined into the domain?

If you find a violation, name the port that *should* exist and where the logic belongs —
but do not write it. This command reports; it does not fix.

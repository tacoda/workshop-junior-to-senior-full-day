---
name: ports-and-adapters
description: >-
  Use when adding a capability to the checkout service or refactoring it — anything
  touching pricing, payment, receipts, persistence, or discounts. Loads the
  ports-and-adapters recipe so new code enters through a port instead of being
  bolted onto the domain. Triggers on "add a feature", "refactor", "new adapter",
  "where does this go".
---

# Ports and adapters — the recipe for this repo

You are working on a service whose charter requires ports and adapters. This skill is
the step-by-step for keeping to it. (The *why* is in CLAUDE.md; this is the *how*, loaded
only when you are actually changing the design — that is the point of a skill over an
always-on rule: it costs context only when it is relevant.)

## The boundary, in one line
The domain (`checkout/money.py`, `model.py`, `ports.py`, `service.py`) imports `checkout.ports`
and never `checkout.adapters`. Adapters implement ports and hold no business decisions.
Concrete adapters are constructed only in `main.py`.

## Adding a capability — the four steps
1. **Define the port.** Add a `Protocol` to `checkout/ports.py` naming the capability in
   domain terms (e.g. `DiscountPolicy.discount(subtotal, customer_id) -> Money`).
2. **Implement the adapter.** Add a concrete class in `checkout/adapters/` that satisfies the
   Protocol. Put the mechanics and any data here — never a policy decision the domain owns.
3. **Inject it.** Take the port in `CheckoutService.__init__` and use it through the interface.
4. **Wire it.** Construct the concrete adapter in `main.py` only, and pass it in.

## Verify — run the bundled checker
This skill ships a checker. After you add or refactor, run it and paste the result:

```bash
python "$CLAUDE_PROJECT_DIR/.claude/skills/ports-and-adapters/check_architecture.py" checkout
```

It scans the domain files and fails (exit 1) if any imports a concrete adapter — the cardinal
violation. `PASS` means the dependency direction is clean; `VIOLATION` names the file and line
to fix. Point it at another package with an argument (e.g. `reference/checkout`).

## The smell test before you finish
- Did a domain file gain an `import` from `checkout.adapters`? → wrong; inject a port instead.
  (The checker catches exactly this — run it.)
- Did an adapter start deciding policy (who qualifies, what rate)? → move the decision to the domain.
- Did you construct a concrete adapter outside `main.py`? → move the wiring to the composition root.

If you cannot add the feature without breaking one of these, stop and say so — that is a
design question for a human, not a thing to paper over by coupling the core to a concrete.

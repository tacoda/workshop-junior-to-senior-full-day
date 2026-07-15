# checkout — a small cash-register service

A service that settles a bill and prints a receipt. Small enough to hold in your head,
which is the point: you should be able to comprehend every line before you change it.

## Run it
    python main.py

## Test it
    pip install pytest && pytest

## Money
Money is handled as **integer cents** — see `money.py`. Formatting to dollars happens only
at the display edge, never mid-calculation.

## Architecture — ports and adapters (the load-bearing rule)

This service is meant to be built as **ports and adapters** (a.k.a. hexagonal):

- **The domain is the core** — the pricing, tax, and settlement logic. It is written against
  **ports** (interfaces) and nothing else.
- **A port** is an interface the domain depends on: *how prices are looked up*, *how a total is
  settled*, *where a receipt goes*. The domain names the port; it never names a concrete.
- **An adapter** is a concrete implementation of a port: an in-memory catalog, a cash payment,
  a console receipt printer. Adapters hold the mechanics and the I/O.
- **Wiring happens in one place** — the composition root (`main.py`) picks which adapters to
  plug into the domain. Nothing else constructs a concrete adapter.

**The rule the agent must follow:**

> The domain depends **only on ports**, never on a concrete adapter (`checkout.adapters.*`).
> Every external concern — pricing, payment, receipts, persistence, discounts — enters the
> domain through a port. Adapters implement ports and hold no business decisions. Concrete
> adapters are constructed **only** in `main.py`.
>
> When you add a capability, define its port first, implement it as an adapter, and inject it.
> Do **not** reach for a concrete inside the domain, and do **not** put business rules in an adapter.

## Preferences
- Format money for display only, at the edge — never mid-calculation.
- Prefer small, single-purpose classes over one class that does everything.

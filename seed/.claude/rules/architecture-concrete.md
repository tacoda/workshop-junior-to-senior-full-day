# Architecture rule — the concrete version (strong feedforward)

> **Ports and adapters.** The domain (`checkout/money.py`, `model.py`, `ports.py`, `service.py`)
> depends **only on ports** — it may import `checkout.ports` and never `checkout.adapters`.
> Every external concern (pricing, payment, receipts, persistence, discounts) enters through a
> port: a `Protocol` the domain names and an adapter implements. Adapters hold mechanics and I/O,
> **no business decisions**. Concrete adapters are constructed **only** in `main.py`.
>
> To add a capability: (1) define its port in `ports.py`, (2) implement it as an adapter in
> `adapters/`, (3) inject it through `CheckoutService.__init__`, (4) wire the concrete in `main.py`.
> Example — a member discount is a `DiscountPolicy` port with a `MemberDiscount` adapter, injected;
> it is **not** a member list imported into `service.py`.

**Why this steers well.** It names the exact boundary (domain imports ports, never adapters),
gives the mechanism (Protocol + adapter + injection + composition root), and pins the disputed
case with a worked example (discounts go behind a port, not inline). Left to itself — or handed a
tangled codebase to imitate — an agent bolts new logic straight onto whatever class is nearest.
This rule tells it where the seams are.

**Tradeoff.** More to author, and it only earns its keep on code with real structure. But it
decides a design question the model will otherwise answer by copying the surrounding code — which
is exactly the wrong teacher when the surrounding code has already drifted.

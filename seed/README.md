# Seed repo — Junior to Senior (full day)

A small cash-register service: it settles a bill and prints a receipt. The load-bearing fact
about this repo is a **deliberate disagreement between the charter and the code**: `CLAUDE.md`
states a good *ports-and-adapters* rule, and the shipped code (`checkout.py`) ignores it, tangling
pricing, tax, payment, and receipt-printing into one class. Everything works and the tests pass.
That gap is the whole workshop: a rule the code contradicts is a rule the agent will contradict
too, because the code is the example it imitates.

## The two states of this repo

| | Where | What it is |
|---|---|---|
| **Drifted (shipped)** | top level — `checkout.py`, `money.py`, `main.py`, `tests/` | The service as it really shipped: one tangled class. Green suite, no ports. |
| **Clean (answer key)** | `reference/` | The same service built as ports and adapters — the target of the refactor lab. Its own green suite. |

The lab reads the drift, watches an agent deepen it, then **refactors the drifted code into the
hexagon** — turning the top level into something that matches `reference/`.

## Files

- `checkout.py` — the drifted service. One `CheckoutService.checkout` does the catalog lookup, the
  tax, the cash/card branch, and the receipt printing. Contradicts the charter's architecture rule.
- `money.py` — `Money`, integer cents, rejects floats. Used by both states.
- `main.py`, `tests/` — run the drifted service; the suite checks **behavior only**, so design
  drift is invisible to it. Green means "the tests that exist passed," not "the code matches the charter."
- `reference/` — the clean ports-and-adapters build: `checkout/ports.py` (the `PricingProvider`,
  `PaymentMethod`, `ReceiptSink` Protocols), `checkout/service.py` (depends only on ports),
  `checkout/adapters/` (the concretes), `main.py` (the composition root that wires them). The answer key.
- `patches/agent-adds-discount.diff` — what an agent hands you when asked to "add a member discount
  using ports and adapters" against the *drifted* code: more inline coupling, no port. Passes the suite.
- `CLAUDE.md` — the charter, stating the good ports-and-adapters rule the code drifted from.
- `.claude/rules/architecture-vague.md`, `architecture-concrete.md` — the **feedforward** half, in
  two strengths. Same rule, different specificity: the specificity knob.
- `.claude/hooks/architecture-gate-edit.py`, `architecture-gate-commit.py` — the **feedback** half,
  at two positions. Same design check (domain must not import an adapter), edit-time vs commit-time:
  the position knob. Dormant while the code is the tangled `checkout.py`; they wake once the refactor
  creates the `checkout/` package.
- `.claude/settings.json` — wires the two hooks.
- `.claude/commands/comprehend.md`, `check-ports.md` — **commands**: reusable invocations you trigger.
- `.claude/skills/ports-and-adapters/SKILL.md` — a **skill**: on-demand guidance that loads only when
  the agent is changing the design (progressive disclosure — the contrast with an always-on rule).
- `.claude/agents/design-reviewer.md` — an **agent**: a bounded sub-context that reviews a diff for
  design drift and returns a verdict.

## The flow

```bash
pip install pytest
pytest                                   # 5 passed — the drifted code is green
python3 main.py                           # cash $11.70 (rounded down), card $11.73

git apply patches/agent-adds-discount.diff
pytest                                   # still green — the agent's inline discount passes the suite
python3 main.py                           # works; the design is worse; the tests never noticed
git apply -R patches/agent-adds-discount.diff

cd reference && pytest                   # 9 passed — the clean hexagon, the target of the refactor
```

Once the refactor turns the top level into a `checkout/` package, the two hooks stop being dormant.
Add `from .adapters.payment import CashPayment` to `checkout/service.py` and the edit gate fires:

```text
architecture-gate (edit): checkout/service.py imports a concrete adapter — the domain must depend
ONLY on ports (checkout/ports.py), never on checkout.adapters.
```

## Why the disagreement is the point

An earlier version of this seed used a value-level trap (cash rounding the wrong way). It was a
good demo of *behavioral* slop, but rounding direction is a local decision the model derives from a
rule alone — too easy. The failure that actually scales is **design drift**: the charter says "ports
and adapters," the code doesn't, and the agent imitates the code. There is no one-line answer to
copy, so the surrounding code becomes the strongest signal. This seed reproduces that on purpose,
and the fix is the senior move — make the code agree with the charter, then gate it so it can't drift again.

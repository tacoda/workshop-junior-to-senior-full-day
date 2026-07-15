"""The checkout service — as it actually shipped.

READ THIS AGAINST THE CHARTER. CLAUDE.md says: use ports and adapters — the domain
depends only on ports, adapters hold the mechanics, concretes are wired in main.py.
This code does none of that. Everything is tangled into one class:

  * the price catalog is a dict baked into the core,
  * the tax rule lives here,
  * the payment mechanics (cash rounding vs card) are an inline if/else,
  * the receipt is formatted and printed right here.

It works. The tests pass. And it flatly contradicts the rule the charter states.
That gap between the rule and the code is the whole lesson: a rule the code
ignores is a rule the agent ignores too, because the code is the example it copies.
"""

from money import Money

CATALOG = {"COFFEE": 500, "MUG": 584}  # price data baked into the core (should be behind a port)
TAX_RATE_BPS = 825  # 8.25% sales tax, in basis points — integer math only


class CheckoutService:
    def checkout(self, skus, payment_type):
        subtotal = Money(sum(CATALOG[sku] for sku in skus))
        tax = Money(subtotal.cents * TAX_RATE_BPS // 10000)
        total = subtotal + tax

        # payment mechanics, inline — no port. Cash rounds down to a nickel; card is exact.
        if payment_type == "cash":
            charged = Money(total.cents - (total.cents % 5))
        else:
            charged = total

        # receipt formatting + I/O, inline — no port
        print(f"subtotal: {subtotal}")
        print(f"tax:      {tax}")
        print(f"total:    {total}")
        print(f"{payment_type}: {charged}")
        return charged

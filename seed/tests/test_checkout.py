"""The shipped suite.

It checks BEHAVIOR — the totals come out right — and nothing else. It says nothing
about the DESIGN: whether pricing, payment, and receipts sit behind ports, or are
tangled into one class. So the suite is fully green while the code contradicts the
charter's ports-and-adapters rule. Green means "the tests that exist passed," not
"the code matches the charter." Design drift is invisible to a behavior suite —
which is exactly why the charter guards design with a rule and a hook, not a test.
"""

from checkout import CheckoutService


def test_cash_rounds_down_to_a_nickel():
    # COFFEE 500 + MUG 584 = 1084 subtotal, +89 tax = 1173 total, cash -> 1170.
    charged = CheckoutService().checkout(["COFFEE", "MUG"], "cash")
    assert charged.cents == 1170


def test_card_charges_exact():
    # COFFEE 500 subtotal, +41 tax = 541 total, card -> 541.
    charged = CheckoutService().checkout(["COFFEE"], "card")
    assert charged.cents == 541

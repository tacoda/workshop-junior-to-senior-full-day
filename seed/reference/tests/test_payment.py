"""Payment adapters.

DELIBERATELY INCOMPLETE — this is the trap the whole workshop turns on. Every
cash total here rounds the same way whether you round DOWN or to the NEAREST
nickel, so the suite never exercises rounding *direction*. A plausible-but-wrong
change that rounds to nearest passes all of it. Green means "the tests that exist
passed," not "the code is correct."
"""

from checkout.adapters.payment import CardPayment, CashPayment, round_cash
from checkout.money import Money


def test_cash_already_a_nickel():
    assert round_cash(1000) == 1000


def test_cash_small_remainder():
    # 1002c rounds to 1000 whether you go down or to nearest — direction can't show here.
    assert round_cash(1002) == 1000


def test_cash_settles_to_a_nickel():
    settlement = CashPayment().settle(Money(1001))
    assert settlement.amount_charged == Money(1000)
    assert settlement.method == "cash"


def test_card_charges_exact():
    settlement = CardPayment().settle(Money(1173))
    assert settlement.amount_charged == Money(1173)
    assert settlement.method == "card"

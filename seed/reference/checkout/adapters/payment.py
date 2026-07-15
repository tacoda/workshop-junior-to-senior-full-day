"""Payment adapters. Rounding is a payment-method concern and lives here, not in
the domain: cash settles to a nickel, card charges the exact cents.

`round_cash` is the load-bearing decision of this repo. Pennies are discontinued,
so a cash total settles to a nickel — and *which way it rounds* is the policy that
a plausible-but-wrong change quietly flips. The charter's policy: round DOWN, in
the customer's favor. They never pay more than the marked total.
"""

from ..money import Money
from ..ports import Settlement


def round_cash(total_cents: int) -> int:
    """Round a cash total DOWN to the nearest nickel (customer's favor). Integer cents.

    1083c ($10.83) settles at 1080c ($10.80), never 1085c.
    """
    return total_cents - (total_cents % 5)


class CashPayment:
    """Implements the PaymentMethod port for cash. Rounds down to a nickel."""

    def settle(self, amount: Money) -> Settlement:
        return Settlement(Money(round_cash(amount.cents)), "cash")


class CardPayment:
    """Implements the PaymentMethod port for card. Charges the exact cents."""

    def settle(self, amount: Money) -> Settlement:
        return Settlement(amount, "card")

"""The ports: the interfaces the domain depends on.

Each adapter in adapters/ implements one of these. The domain (service.py) is
written against these Protocols and never against a concrete adapter — that is
what keeps the hexagon's dependencies pointing inward.
"""

from dataclasses import dataclass
from typing import Protocol

from .model import Receipt
from .money import Money


class PricingProvider(Protocol):
    """Where line prices come from (a catalog, a remote pricing service, ...)."""

    def unit_price(self, sku: str) -> Money: ...


@dataclass(frozen=True)
class Settlement:
    amount_charged: Money
    method: str


class PaymentMethod(Protocol):
    """How a total is settled. Cash rounds to a nickel; card charges exact cents."""

    def settle(self, amount: Money) -> Settlement: ...


class ReceiptSink(Protocol):
    """Where a finished receipt goes (a console, a printer, an email, ...)."""

    def emit(self, receipt: Receipt) -> None: ...

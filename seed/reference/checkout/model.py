"""Domain values: what a checkout is made of. No behavior that needs the outside world."""

from dataclasses import dataclass

from .money import Money


@dataclass(frozen=True)
class LineItem:
    """What the customer asked for, before we know the price."""

    sku: str
    quantity: int


@dataclass(frozen=True)
class PricedLine:
    """A line item once the catalog has priced it."""

    sku: str
    quantity: int
    unit_price: Money

    @property
    def total(self) -> Money:
        return self.unit_price * self.quantity


@dataclass(frozen=True)
class Order:
    lines: tuple[LineItem, ...]


@dataclass(frozen=True)
class Receipt:
    """The settled result of a checkout, ready to print."""

    priced_lines: tuple[PricedLine, ...]
    subtotal: Money
    tax: Money
    total: Money
    amount_charged: Money
    payment_method: str

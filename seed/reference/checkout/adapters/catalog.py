"""A PricingProvider backed by an in-memory price list."""

from ..money import Money


class InMemoryCatalog:
    """Implements the PricingProvider port. Prices are integer cents."""

    def __init__(self, prices_cents: dict[str, int]):
        self._prices = {sku: Money(cents) for sku, cents in prices_cents.items()}

    def unit_price(self, sku: str) -> Money:
        try:
            return self._prices[sku]
        except KeyError:
            raise KeyError(f"unknown SKU: {sku!r}") from None

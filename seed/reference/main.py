"""Composition root: wire the adapters into the service and run one checkout.

This is the ONLY place that names concrete adapters. The service itself sees
only ports. Swap InMemoryCatalog for a database, ConsoleReceiptSink for email,
CashPayment for card — the service never changes.
"""

from checkout.adapters.catalog import InMemoryCatalog
from checkout.adapters.payment import CardPayment, CashPayment
from checkout.adapters.receipt import ConsoleReceiptSink
from checkout.model import LineItem, Order
from checkout.service import CheckoutService

CATALOG = {"COFFEE": 500, "MUG": 584}  # prices in integer cents


def main():
    catalog = InMemoryCatalog(CATALOG)
    service = CheckoutService(pricing=catalog, receipts=ConsoleReceiptSink())
    order = Order((LineItem("COFFEE", 1), LineItem("MUG", 1)))

    print("--- paying cash ---")
    service.checkout(order, CashPayment())  # total $11.73 -> cash $11.70 (rounded down)
    print("\n--- paying card ---")
    service.checkout(order, CardPayment())  # total $11.73 -> card $11.73 (exact)


if __name__ == "__main__":
    main()

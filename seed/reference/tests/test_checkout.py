"""The checkout use case, wired with fake adapters.

Also DELIBERATELY INCOMPLETE. The only cash checkout here uses a total that
rounds the same both ways, and nothing pins the structural rule that the service
must go through the injected PaymentMethod port. Both the rounding trap and the
design trap pass this suite untouched.
"""

from checkout.adapters.payment import CashPayment
from checkout.model import LineItem, Order
from checkout.money import Money
from checkout.service import CheckoutService


class FakeCatalog:
    def unit_price(self, sku):
        return {"COFFEE": Money(500)}[sku]


class CapturingSink:
    def __init__(self):
        self.last = None

    def emit(self, receipt):
        self.last = receipt


def test_cash_checkout_prices_taxes_and_settles():
    service = CheckoutService(pricing=FakeCatalog(), receipts=CapturingSink())
    order = Order((LineItem("COFFEE", 1),))

    receipt = service.checkout(order, CashPayment())

    assert receipt.subtotal == Money(500)
    assert receipt.tax == Money(41)  # 500 * 825 // 10000
    assert receipt.total == Money(541)
    # 541 rounds to 540 whether DOWN or NEAREST — the direction still can't show.
    assert receipt.amount_charged == Money(540)


def test_sink_receives_the_receipt():
    sink = CapturingSink()
    service = CheckoutService(pricing=FakeCatalog(), receipts=sink)
    service.checkout(Order((LineItem("COFFEE", 1),)), CashPayment())
    assert sink.last is not None

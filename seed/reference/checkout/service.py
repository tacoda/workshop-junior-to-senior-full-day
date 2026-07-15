"""The checkout use case. Depends only on ports — never on a concrete adapter.

If this file ever imports from checkout.adapters, the hexagon is broken: the
core now knows about the outside world it was supposed to be insulated from.
"""

from .model import Order, PricedLine, Receipt
from .money import Money
from .ports import PaymentMethod, PricingProvider, ReceiptSink

TAX_RATE_BPS = 825  # 8.25% sales tax, in basis points — integer math only


class CheckoutService:
    def __init__(self, pricing: PricingProvider, receipts: ReceiptSink):
        self._pricing = pricing
        self._receipts = receipts

    def checkout(self, order: Order, payment: PaymentMethod) -> Receipt:
        priced = tuple(
            PricedLine(line.sku, line.quantity, self._pricing.unit_price(line.sku))
            for line in order.lines
        )
        subtotal = sum((line.total for line in priced), Money(0))
        tax = Money(subtotal.cents * TAX_RATE_BPS // 10000)
        total = subtotal + tax

        settlement = payment.settle(total)

        receipt = Receipt(
            priced_lines=priced,
            subtotal=subtotal,
            tax=tax,
            total=total,
            amount_charged=settlement.amount_charged,
            payment_method=settlement.method,
        )
        self._receipts.emit(receipt)
        return receipt

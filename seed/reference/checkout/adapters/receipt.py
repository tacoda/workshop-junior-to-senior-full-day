"""A ReceiptSink that prints to a console (or any writer you inject)."""

from ..model import Receipt


class ConsoleReceiptSink:
    """Implements the ReceiptSink port. `out` defaults to print; inject a fake in tests."""

    def __init__(self, out=print):
        self._out = out

    def emit(self, receipt: Receipt) -> None:
        lines = [f"{p.sku} x{p.quantity}    {p.total}" for p in receipt.priced_lines]
        lines += [
            f"subtotal:   {receipt.subtotal}",
            f"tax:        {receipt.tax}",
            f"total:      {receipt.total}",
            f"{receipt.payment_method + ':':<11} {receipt.amount_charged}",
        ]
        self._out("\n".join(lines))

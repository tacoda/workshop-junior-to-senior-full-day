"""Run one checkout, cash and card."""

from checkout import CheckoutService


def main():
    service = CheckoutService()
    print("--- paying cash ---")
    service.checkout(["COFFEE", "MUG"], "cash")  # total $11.73 -> cash $11.70 (rounded down)
    print("\n--- paying card ---")
    service.checkout(["COFFEE", "MUG"], "card")  # total $11.73 -> card $11.73 (exact)


if __name__ == "__main__":
    main()

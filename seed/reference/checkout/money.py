"""Money as integer cents. Never float. Dollars appear only at the display edge."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    """A whole number of cents. The iron law: money is integer cents, never float."""

    cents: int

    def __post_init__(self):
        if not isinstance(self.cents, int) or isinstance(self.cents, bool):
            raise TypeError("Money is integer cents; never build it from a float.")

    def __add__(self, other: "Money") -> "Money":
        return Money(self.cents + other.cents)

    def __sub__(self, other: "Money") -> "Money":
        return Money(self.cents - other.cents)

    def __mul__(self, quantity: int) -> "Money":
        return Money(self.cents * quantity)

    def __str__(self) -> str:
        return f"${self.cents / 100:.2f}"

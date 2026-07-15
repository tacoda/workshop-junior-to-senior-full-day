"""Money value object — the integer-cents iron law."""

import pytest

from checkout.money import Money


def test_add_and_multiply():
    assert (Money(500) + Money(584)).cents == 1084
    assert (Money(499) * 3).cents == 1497


def test_rejects_float():
    with pytest.raises(TypeError):
        Money(10.5)


def test_formats_as_dollars():
    assert str(Money(1170)) == "$11.70"

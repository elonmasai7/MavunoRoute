from decimal import Decimal, ROUND_HALF_UP


def to_money(value: float) -> float:
    return float(Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

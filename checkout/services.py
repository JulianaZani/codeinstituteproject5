from decimal import Decimal


def choose_tax_rate(country_code: str) -> Decimal:
    # Exemplo simples: IE cobra 23%, outros 0%
    if (country_code or "").upper() == "IE":
        return Decimal("23.00")
    return Decimal("0.00")

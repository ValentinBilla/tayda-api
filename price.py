import dataclasses

from currency_converter import CurrencyConverter


@dataclasses.dataclass
class Price:
    tva: float = 1.2

    def __init__(self, price_usd_ht: float, quantity: int):
        self.quantity = quantity
        self.price_usd_ht = price_usd_ht

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        self._quantity = value

    @property
    def price_usd_ht(self) -> float:
        return self._price_usd_ht

    @price_usd_ht.setter
    def price_usd_ht(self, value: float):
        self._price_usd_ht = value

    @property
    def price_eur_ht(self) -> float:
        return CurrencyConverter().convert(self.price_usd_ht, 'USD', 'EUR')

    @property
    def price_eur_ttc(self) -> float:
        return self.price_eur_ht * self.tva

    @property
    def to_string(self) -> str:
        return str(self.quantity) + " - " \
               + str(round(self.price_usd_ht, 2)) + "$ H.T - " \
               + str(round(self.price_eur_ht, 2)) + "€ H.T - " \
               + str(round(self.price_eur_ttc, 2)) + "€ T.T.C"

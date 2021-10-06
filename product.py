# built-in librairies
from __future__ import annotations
from typing import List
from dataclasses import dataclass
from typing import ClassVar

# additional librairies
from currency_converter import CurrencyConverter


@dataclass
class Offer:
    _TVA: ClassVar[float] = 1.2

    quantity: int
    currency: str
    price_ht: float

    def __repr__(self) -> str:
        """We want : self = eval(repr(self))"""
        return f"Price(price_ht={self.price_ht}, currency={self.currency}" \
               f"quantity={self.quantity})"

    def __str__(self) -> str:
        """Returns a readable representation of the object"""
        # We need to use the property to access price_eur_ttc to init it
        return f"{self.quantity:>3} pcs for " \
               f"{self.price_eur_ttc:8.2f}€ TTC"

    @property
    def price_eur_ht(self) -> float:
        if self.currency == "EUR":
            return self.price_ht

        # "EUR" is the default for new_currency in convert(...)
        return CurrencyConverter().convert(self.price_ht, self.currency)

    @property
    def price_eur_ttc(self) -> float:
        return self.price_eur_ht * self._TVA


@dataclass
class Product:
    sku: str
    name: str
    description: str
    offers_list: List[Offer]

    @property
    def formatted_name(self):
        return f"{self.sku} | {self.name}"

    def __str__(self):
        offers_str = '\n'.join(map(str, self.offers_list))
        return f"{self.formatted_name}\n{offers_str}"

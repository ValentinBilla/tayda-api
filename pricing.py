# built-in librairies
from dataclasses import dataclass
from typing import ClassVar

# additional librairies
from currency_converter import CurrencyConverter


@dataclass
class Offer:
    TVA: ClassVar[float] = 1.2

    price_usd_ht: float
    quantity: int

    def __repr__(self) -> str:
        # renvoie une string qui vérifie : self = eval(repr(self))
        return f"Price(price_usd_ht={self.price_usd_ht}, " \
               f"quantity={self.quantity})"

    def __str__(self) -> str:
        # prend le rôle de ton "to_string" et permet de faire les conversions
        # plus pythoniquement
        return f"{self.quantity:>3} pcs for " \
               f"{self.price_eur_ttc:8.2f}€ TTC"

    @property
    def price_eur_ht(self) -> float:
        return CurrencyConverter().convert(self.price_usd_ht, 'USD', 'EUR')

    @property
    def price_eur_ttc(self) -> float:
        return self.price_eur_ht * self.TVA

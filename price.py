import dataclasses

from currency_converter import CurrencyConverter


@dataclasses.dataclass
class Price:
    tva: float = 1.2

    def __init__(self, price_usd_ht: str, quantity: int):
        self.quantity = quantity
        self.price_usd_ht = price_usd_ht
        
    def __str__(self) -> str:
        # prend le rôle de ton "to_string" et permet de faire les conversions plus pythoniquement
        return f"{self.quantity} pcs à \n
        str(round(self.price_usd_ht, 2)) + "$ H.T - " \
               + str(round(self.price_eur_ht, 2)) + "€ H.T - " \
               + str(round(self.price_eur_ttc, 2)) + "€ T.T.C"}"

    # En soit pas besoin de faire des methodes pour quantity \°u°/
        
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

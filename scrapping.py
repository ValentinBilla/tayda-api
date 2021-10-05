# built-in librairies
from __future__ import annotations
from typing import ClassVar, Optional
from dataclasses import dataclass
import re

# project files
from pricing import Offer

# additional librairies
import requests
import bs4


@dataclass
class Product:
    sku: str
    name: str
    description: str
    offers_list: list[Offer]

    @property
    def formatted_name(self):
        return f"{self.sku} | {self.name}"

    def __str__(self):
        offers_str = '\n'.join(map(str, self.offers_list))
        return f"{self.formatted_name}\n{offers_str}"


@dataclass
class TaydaProductList:
    _URL: ClassVar[str] = "https://www.taydaelectronics.com/" \
                         "catalogsearch/result/"
    _NAME_TAG: ClassVar[str] = ".product-info-main  .page-title"
    _DESCRIPTION_TAG: ClassVar[str] = '.wrapper-details .value'
    _PRICE_TAG: ClassVar[str] = '.product-info-main .price-box .price'
    _PRICE_LIST_TAG: ClassVar[str] = ".product-info-main ul.prices-tier li.item"

    _current_url: Optional[str] = None
    _current_request: Optional[requests.models.Response] = None
    _current_page: Optional[bs4.BeautifulSoup] = None

    def get_request(self) -> requests.models.Response:
        return requests.get(self._current_url)

    def get_page(self) -> bs4.BeautifulSoup:
        return bs4.BeautifulSoup(self._current_request.content, 'html.parser')

    @property
    def name(self) -> str:
        return self._current_page.select_one(self._NAME_TAG).text.strip()

    @property
    def description(self) -> str:
        return self._current_page.select_one(self._DESCRIPTION_TAG).text.strip()

    @property
    def offers_list(self) -> list[Offer]:
        offers_list = list()

        # The initial price is considered as an offer for 1 item
        default_price_str = self._current_page.select_one(self._PRICE_TAG).text
        default_price = float(default_price_str.strip('$'))
        offers_list.append(
            Offer(quantity=1, price_usd_ht=default_price))

        # We go through all the proposed special offers and process them
        html_offers_list = self._current_page.select(self._PRICE_LIST_TAG)
        for html_offer in html_offers_list:
            # Isolates the first decimal number in the html
            # eg. the number of items
            quantity = re.findall(r'\d+', html_offer.text)[0]
            price_str = html_offer.select_one('.price').text
            price = float(price_str.strip('$'))

            offers_list.append(
                Offer(quantity=quantity, price_usd_ht=price))

        return offers_list

    def get(self, sku: str) -> Product:
        self._current_url = f'{self._URL}?q={sku}'
        self._current_request = self.get_request()
        self._current_page = self.get_page()

        return Product(
            sku=sku,
            name=self.name,
            description=self.description,
            offers_list=self.offers_list
        )

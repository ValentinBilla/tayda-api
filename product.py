import dataclasses
import requests
import re

from bs4 import BeautifulSoup
from price import Price


@dataclasses.dataclass
class Product:
    sku: str
    name: str
    description: str
    price_list: list[Price]

    @property
    def formatted_name(self):
        return "{0} | {1}".format(self.sku, self.name)

    def to_string(self):
        results: list = [self.formatted_name]
        for price in self.price_list:
            results.append(str("\t" + price.to_string))
        return '\r\n'.join(results)

    @staticmethod
    def get(sku: str):
        product: Product = Tayda("https://www.taydaelectronics.com/catalogsearch/result/", sku).get_product()
        return product


@dataclasses.dataclass
class Tayda:
    url: str
    sku: str

    _request = None
    _page = None

    name_tag: str = ".product-info-main  .page-title"
    description_tag: str = '.wrapper-details .value'
    price_tag: str = '.product-info-main .price-box .price'
    price_list_tag: str = ".product-info-main ul.prices-tier li.item"

    @property
    def url_completed(self):
        return f'{self.url}?q={self.sku}'

    @property
    def request(self):
        if self._request is not None:
            return self._request

        self._request = requests.get(self.url_completed)
        return self._request

    @property
    def page(self) -> BeautifulSoup:
        if self._page is not None:
            return self._page

        self._page = BeautifulSoup(self.request.content, 'html.parser')
        return self._page

    @property
    def name(self) -> str:
        return self.page.select_one(self.name_tag).text.strip()

    @property
    def description(self) -> str:
        return self.page.select_one(self.description_tag).text.strip()

    @property
    def price_list(self) -> list[Price]:
        price_list: list[Price] = list()
        price = float(self.page.select_one(self.price_tag).text.strip('$'))
        price_list.append(Price(quantity=1, price_usd_ht=price))

        html_price_list = self.page.select(self.price_list_tag)
        for price in html_price_list:
            quantity = re.findall(r'\d+', price.text)[0]
            price_usd_ht = float(price.select_one('.price').text.strip('$'))
            price_list.append(Price(quantity=quantity, price_usd_ht=price_usd_ht))

        return price_list

    def get_product(self) -> Product:
        return Product(sku=self.sku, name=self.name, description=self.description, price_list=self.price_list)

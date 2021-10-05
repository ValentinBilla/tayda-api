from product import Product


def print_product(sku):
    print(Product.get(sku).to_string())


if __name__ == '__main__':
    print_product('A-5158-CST-UV1')
    print_product('A-5158')

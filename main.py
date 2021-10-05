from scrapping import TaydaProductList


if __name__ == '__main__':
    provider = TaydaProductList()

    print(provider.get('A-5158-CST-UV1'))
    print(provider.get('A-5158'))
    print(provider.get('A-5174'))

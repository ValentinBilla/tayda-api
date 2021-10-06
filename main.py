from scrapping import TaydaProductProvider


if __name__ == '__main__':
    provider = TaydaProductProvider()

    print(provider.get('A-5158-CST-UV1'))
    print(provider.get('A-5158'))
    print(provider.get('A-5174'))

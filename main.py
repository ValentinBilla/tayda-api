import scrapping

if __name__ == '__main__':
    tayda_provider = scrapping.TaydaProductProvider()
    mouser_provider = scrapping.MouserProductProvider()

    print(tayda_provider.get('A-5158-CST-UV1'))
    print(tayda_provider.get('A-5158'))
    print(tayda_provider.get('A-5174'))
    print(mouser_provider.get('584-ADA40991BUJZRL7'))

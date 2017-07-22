import osa

# открываем текстовый документ и выдаем список
def open_file(file_name):
    with open(file_name, 'r', encoding='utf8') as f:
        temp_list = [line.strip().split() for line in f]
    return temp_list


# конвертируем валюту
def convert_currency(value, from_unit, to_unit):
    client = osa.Client('http://fx.currencysystem.com/webservices/CurrencyServer4.asmx?WSDL')
    result = client.service.ConvertToNum(
        amount=value,
        fromCurrency=from_unit,
        toCurrency=to_unit,
        rounding=True
    )
    return result


# обрабатываем все
def main_func():
    file_name = 'currencies.txt'
    to_unit = 'RUB'
    print('Затраты на путешествие {} рублей'.format(
        round(sum([convert_currency(l[1], l[2], to_unit) for l in open_file(file_name)]), 2)))

main_func()

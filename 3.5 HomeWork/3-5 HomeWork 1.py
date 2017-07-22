import osa


# открываем текстовый документ и выдаем список из значений температур в F
def open_file(file_name):
    with open(file_name, 'r', encoding='utf8') as f:
        temp_list = [line.strip().split()[0] for line in f]
    return temp_list


# преобразуем фаренгейты в цельсии
def convert_temp(value, from_unit, to_unit):
    client = osa.Client('http://www.webservicex.net/ConvertTemperature.asmx?WSDL')
    result = client.service.ConvertTemp(
        Temperature=value,
        FromUnit=from_unit,
        ToUnit=to_unit
    )
    return result


# обрабатываем все
def main_func():
    file_name = 'temps.txt'
    from_unit = 'degreeFahrenheit'
    to_unit = 'degreeCelsius'
    celsium_list = [convert_temp(temperature, from_unit, to_unit) for temperature in open_file(file_name)]
    print('Средняя температура за 7 дней {:.3} градуса по Цельсию'.format(
        sum(celsium_list)/len(celsium_list)))


main_func()

import osa


# открываем текстовый документ и выдаем список из значений в милях
# также есть мусор в строке будем дальше убирать
def open_file(file_name):
    with open(file_name, 'r', encoding='utf8') as f:
        distance_list = [line.strip().split()[1] for line in f]
    return distance_list


# убираем запятую и преобразуем значение в float
def str_to_float(distance):
    new_distance = []
    for x in distance:
        new_str = ''
        for s in x:
            if s != ',':
                new_str += s
        new_distance.append(float(new_str))
    return new_distance

# убираем запятую и преобразуем значение в float реплейсом
def str_to_float2(distance):
    new_distance = []
    for x in distance:
        new_str = x.replace(',','')
        new_distance.append(float(new_str))
    return new_distance

# преобразуем мили в киллометры
def convert_length(value, from_unit, to_unit):
    client = osa.Client('http://www.webservicex.net/length.asmx?WSDL')
    result = client.service.ChangeLengthUnit(
        LengthValue=value,
        fromLengthUnit=from_unit,
        toLengthUnit=to_unit
    )
    return result


# обрабатываем все
def main_func():
    file_name = 'travel.txt'
    from_unit = 'Miles'
    to_unit = 'Kilometers'
    print('Cуммарное расстояние пути {} км'.format(round(
        convert_length(sum(str_to_float2(open_file(file_name))), from_unit, to_unit), 2)))

main_func()

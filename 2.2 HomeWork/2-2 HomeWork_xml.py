def read_cook_book_from_xml_file():
    """
    данные берем из xml файла
    """
    import xml.etree.ElementTree as ET
    tree = ET.parse('cook_book.xml')
    root = tree.getroot()
    # представляем в виде дерева и можем работать как со словарями и списками

    """
    проходимся по дочерним элементам и ищем внутри все значения с тегом
    'ingridient' далее по этому списку значений пробегам
    в данном случае это словарь и по ключу name находим имя и записываем
    в нашу книгу рецептов
    
    ищем элементы по всему дереве не взирая на глубину вложения //
    print(tree.findall('//ingridient'))
    """
    cook_book_load = {}
    for child in root:
        ingridients_list = []
        for i in child.findall('ingridient'):
            i.attrib['quantity'] = int(i.attrib['quantity'])
    # вот тут и поймал ошибку все значения были str )))
    # заменил на int
            ingridients_list.append(i.attrib)
        cook_book_load[child.attrib['name']] = ingridients_list


    return cook_book_load

def validation_cook_book(cook_book_load):
    """
    пробегаем и выравниваем высоту букв
    в названиях блюд и ингридиентов
    """
    cook_book = {}
    ingridients = []
    for dishe, ingridiets in cook_book_load.items():
        dishe_new = dishe.lower()

        for ingridient in ingridiets:
            ingridient_dict = {}
            for key, value in ingridient.items():
                if key == 'ingridient_name':
                    value_new = value.lower()
                    ingridient_dict[key] = (value_new)
                else:
                    ingridient_dict[key] = (value)
            ingridients.append(ingridient_dict)
        cook_book[dishe_new] = (ingridients)
        ingridients =[]
    return cook_book

def get_shop_list_by_dishes(dishes, person_count, cook_book):
    shop_list = {}
    for dish in dishes:
        for ingridient in cook_book[dish]:
          new_shop_list_item = dict(ingridient)
          new_shop_list_item['quantity'] *= person_count
          if new_shop_list_item['ingridient_name'] not in shop_list:
              shop_list[new_shop_list_item['ingridient_name']] = new_shop_list_item
          else:
              shop_list[new_shop_list_item['ingridient_name']]['quantity'] += new_shop_list_item['quantity']
    return shop_list

def print_shop_list(shop_list):
    for shop_list_item in shop_list.values():
        print(
            '{} {} {}'.format(shop_list_item['ingridient_name'], shop_list_item['quantity'], shop_list_item['measure']))

def create_shop_list():
    person_count = int(input('Введите количество человек: '))
    dishes = input('Введите блюда в расчете на одного человека (через запятую): ').lower().split(', ')
    cook_book_load = read_cook_book_from_xml_file()
    cook_book = validation_cook_book(cook_book_load)
    shop_list = get_shop_list_by_dishes(dishes, person_count, cook_book)
    print_shop_list(shop_list)

create_shop_list()
def read_cook_book_from_yaml_file():
    """
    данные берем из yaml файла
    """
    import yaml
    with open('cook_book.yml', encoding='utf8') as f:
        data = yaml.load(f)

    cook_book_load = data
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
    cook_book_load = read_cook_book_from_yaml_file()
    cook_book = validation_cook_book(cook_book_load)
    shop_list = get_shop_list_by_dishes(dishes, person_count, cook_book)
    print_shop_list(shop_list)

create_shop_list()
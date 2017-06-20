
# данные берем из txt файла cook_book.txt
def read_cook_book_from_txt_file():
    cook_book = {}  # пустой словарь для книгим рецептов
    ingridients_list = []  # список ингридиетнтов
    with open('cook_book.txt','r', encoding = 'utf8') as f:
        for line in f:
            dishe = line.lower().strip() # удаляет все знаки препинания
            ingridients_number = int(f.readline())
            for index in range(ingridients_number):
                ingridient = f.readline()
                ingridient = ingridient.lower().strip()
                ingridient = ingridient.split(' | ')
                ingridients_number_dict = dict(ingridient_name = ingridient[0], quantity = int(ingridient[1]), measure = ingridient[2])
                ingridients_list.append(ingridients_number_dict)
            cook_book[dishe] = ingridients_list
            ingridients_list = [] #очищяем список ингридиентво для следующей итерации
            f.readline()
    return cook_book

def get_shop_list_by_dishes(dishes, person_count):
    shop_list = {}
    cook_book = read_cook_book_from_txt_file() # вызываем функцию для импорта данных для работы программы
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
        print('{} {} {}'.format(shop_list_item['ingridient_name'], shop_list_item['quantity'],shop_list_item['measure']))

def create_shop_list():
    person_count = int(input('Введите количество человек: '))
    dishes = input('Введите блюда в расчете на одного человека (через запятую): ').lower().split(', ')
    shop_list = get_shop_list_by_dishes(dishes, person_count)
    print_shop_list(shop_list)

create_shop_list()

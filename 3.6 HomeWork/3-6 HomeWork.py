# Базовый класс животные
class Animals:
    # общий для всех метод покормить
    resource = None
    def feed_animal(self):
        print('Om-nom-nom')

    # общий для всех метод получить ресурсы ))))
    def take_resource(self):
        print('Take {}'.format(self.resource))


# подкласс млекопитающие
class Mammals(Animals):
    # атрибуты класса
    common_features = 'Have a hooves'
    resource = 'meat'


# подкласс птицы
class Birds(Animals):
    # атрибуты класса
    common_features = 'Have a wings'
    resource = 'egg'

# под классы по видам животных
class Cows(Mammals):
    # добавим конструктор чтобы обьекты были разные
    resource = 'meat and milk'
    def __init__(self, veight, nickname):
        self.veight = veight
        self.nickname = nickname



class Goats(Mammals):
    def __init__(self, veight, nickname):
        self.veight = veight
        self.nickname = nickname


class Sheeps(Mammals):
    resource = 'meat and wool'
    def __init__(self, veight, nickname):
        self.veight = veight
        self.nickname = nickname


class Pigs(Mammals):
    resource = 'beacon'
    def __init__(self, veight, nickname):
        self.veight = veight
        self.nickname = nickname


class Ducks(Birds):
    def __init__(self, veight, nickname):
        self.veight = veight
        self.nickname = nickname


class Geese(Birds):
    def __init__(self, veight, nickname):
        self.veight = veight
        self.nickname = nickname


class Chickens(Birds):
    resource = 'meat and egg'
    def __init__(self, veight, nickname):
        self.veight = veight
        self.nickname = nickname

# создаем обьект определенного класса

# обьекты класса животные подкласса млекопитающие и покласса по видам животных
cow_dusia = Cows(250, 'Дуся')
cow_irka = Cows(230, 'Ирка')

x = cow_dusia

x.take_resource()

# обьекты класса животные подкласса птицы и покласса по видам птиц

# cow_dusia.take_resource()
# cow_dusia.feed_animal()
#
# cow_irka.take_resource()
# cow_irka.feed_animal()
# print('Коровка {} весит {} кг'.format(
#     cow_dusia.nickname, cow_dusia.veight))
# print('Коровка {} весит {} кг'.format(
#     cow_irka.nickname, cow_irka.veight))

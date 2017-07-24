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


# создаем обьект определенного класса

# обьекты класса животные подкласса млекопитающие
Cows = Mammals()
Goats = Mammals()
Sheeps = Mammals()
Pigs = Mammals()

# обьекты класса животные подкласса птицы
Ducks = Birds()
Chickens = Birds()
Geese = Birds()

Geese.take_resource()

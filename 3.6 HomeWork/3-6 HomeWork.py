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
    resource = 'meat and milk'

class Goats(Mammals):
    pass

class Sheeps(Mammals):
    resource = 'meat and wool'

class Pigs(Mammals):
    pass

class Ducks(Birds):
    pass

class Geese(Birds):
    pass

class Chickens(Birds):
    resource = 'meat and egg'


# создаем обьект определенного класса

# обьекты класса животные подкласса млекопитающие и покласса по видам животных
cow_dusia = Cows()
goat_vasiya = Goats()

# обьекты класса животные подкласса птицы и покласса по видам птиц
duck_boris = Birds()
gees_ivanko = Birds()

cow_dusia.take_resource()
cow_dusia.feed_animal()

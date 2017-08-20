"""
Домашнее задание для лекции "Задачки на собеседованиях для продвинутых,
с тонкостями языка"

Описание
    1. Перестроить заданный связанный список (LinkedList) в обратном порядке.
    Для этого использовать метод `LinkedList.reverse()`, представленный
    в данном файле.
    2. Определить сложность алгоритма.
    3. Определить потребление памяти в big-O notation.

Примечание
    Проверить работоспособность решения можно при помощи тестов,
    которые можно запустить следующей командой:

    python3 -m unittest linked_list_reverse.py
"""

import unittest

from typing import Iterable


class LinkedListNode:  # описываем класс узел связанного списка
    # при создании обьекта класс LinkedListNode будем просить указать data
    def __init__(self, data):
        self.data = data
        self.next = None


# описывем класс связанный список
class LinkedList:
    '''
    конструктор обьектка класса LinkedList
    в нем же и создаем наш список из полученных данных итерируемых
    '''


    def __init__(self, values: Iterable):  # получаем дланные
        previous = None
        self.head = None
        for value in values:  # в цикле создаем узлы и форнируем ссылки вних
            current = LinkedListNode(value)
            if previous:
                previous.next = current
            self.head = self.head or current
            previous = current


    # используем чтобы можно было вывести напечать при вызове print()
    def __iter__(self):
        current = self.head         # Начинаем с Head
        while current:              # пока не упремся в None
            yield current.data      # в поток выбрасывает значения
            current = current.next  # переходит к след узлу

    # переворачиваем список
    def reverse(self):

        """
        Суть сего деяни в том чтобы переназначить ссылки у обьектов
        в обратном порядке.
        Начинаем с head и проходя по всем значения пока не упремся в None
        точнее в конец
        изменяем значения next у всех узлов

        Наприме если их 4:head 1 2 3 4
        у первого делаем ссылку на None вмето 2
        у второго меняем ссылку с 3 на 1
        у третьего меняем ссылку с 4 на 2
        у четверого меняем ссылку с None на 3
        и по достижении None у head меняем ссылку на current
        (в данном случае это четвертый элемент)
        получаем 4: head 4 3 2 1
        """

        previous = None      # в начале с тартуем с пустого
        current = self.head  # начинаем с головы )
        while current is not None:
            next = current.next      # в next определяем ссылку на значение из current.next
            current.next = previous  # изменям значение next утекушего на previous
            previous = current       # обновляем previous для следующей итерации
            current = next           # обновляем current для следующей итерации
        self.head = previous


# моя функция для проверки
def my_test_list():
    l = LinkedList([1, 2, 3, 4])  # создаем объект l класса LinkedList из списка данных
    print('Прямой лист', list(l))
    l.reverse() # переворачиваем список
    print('Обратный лист', list(l))


# собственно сам тест
class LinkedListTestCase(unittest.TestCase):

    def test_reverse(self):
        cases = dict(
            empty=dict(
                items=[],
                expected_items=[],
            ),
            single=dict(
                items=[1],
                expected_items=[1],
            ),
            double=dict(
                items=[1, 2],
                expected_items=[2, 1],
            ),
            triple=dict(
                items=[1, 2, 3],
                expected_items=[3, 2, 1],
            ),
        )
        for case, data in cases.items():
            with self.subTest(case=case):
                linked_list = LinkedList(data['items'])
                linked_list.reverse()
                self.assertListEqual(
                    data['expected_items'],
                    list(linked_list),
                )


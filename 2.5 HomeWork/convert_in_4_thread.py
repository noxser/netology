import subprocess
import os
from time import ctime
from queue import Queue
from threading import Thread

# задаем колличество потоков
num_threads = 4

def make_directories():
    """
    Функция при необходимости папку Result
    """
    if 'Result' in os.listdir(os.path.dirname(__file__)):
        print('Папка Result уже есть делаем преобразование файлов')
    else:
        print('Папка Result создана делаем преобразование файлов')
        os.makedirs('Result')

def convert_file(file_name):
    """
    Функция конвертирует файлик
    """
    subprocess.call('convert Source\\' + file_name + ' -resize 200 result\\' + file_name)
    print(' {} --> done in --> {} '.format(file_name, ctime()))
    # print('Преобразованные файлы в папке Result')

def make_convert_all():
    """
    Берем из очереди задание, отадем его функции
    и ждем выполнения
    """
    while True:
        # Получаем задание из очереди
        file_name = q.get()
        convert_file(file_name)
        # Сообщаем о выполненном задании
        q.task_done()

def file_for_convert():
    """
    Функция генерирует данные для очереди
    имена файлов для конвертации
    """
    for file_name in os.listdir('Source'):
        # выдает в поток даные
        yield file_name

# создаем папку Result
make_directories()

# Создаем FIFO очередь
q = Queue()

# Создаем и запускаем потоки колличество зависит от num_threads
for i in range(num_threads):
    t = Thread(target=make_convert_all)
    t.setDaemon(True)
    t.start()

# Заполняем очередь заданиями с помошью put
for file_name in file_for_convert():
    q.put(file_name)

# Ставим блокировку пока не будут выполнены все задания
q.join()
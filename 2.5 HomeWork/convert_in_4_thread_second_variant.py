import subprocess
import os
from time import ctime
from concurrent.futures import ThreadPoolExecutor

def make_directories():
    """
    Функция допоплнительная
    """
    if 'Result' in os.listdir(os.path.dirname(__file__)):
        print('Папка Result уже есть, делаем преобразование файлов')
    else:
        print('Папка Result создана, делаем преобразование файлов')
        os.makedirs('Result')

def convert_file(file_name):
    """
    Функция конвертирует файлик
    """
    subprocess.call('convert Source\\' + file_name + ' -resize 200 Result\\' + file_name)


# создаем папку Result или нет )))
make_directories()

# задаем колличество потоков
num_threads = 4

"""
создаем потоки в кол-е num_threads асинхронные передаем executor-у список файлов 
и функцию которая обрарбатывает их, с помошью map все это собираем в кучу
zip используем для состыковуи операции и имя файла для вывода его имени в печать)

"""
with ThreadPoolExecutor(num_threads) as executor:
    for file, funk in zip(os.listdir('Source'), executor.map(convert_file, os.listdir('Source'))):
        print(file, '  -->  done in  ', ctime())

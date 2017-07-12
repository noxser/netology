import requests
import os
from time import ctime
from concurrent.futures import ThreadPoolExecutor

# открываем файлик с текстом для перевода
def open_file(file_name):
    with open(file_name, 'r', encoding='utf8') as f:
        text = f.read()
    return text

# определяем язык текста
def detect_lang(text):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/detect ?
    key=<API-ключ>
     & text=<текст>
     & [hint=<список вероятных языков текста>]
     & [callback=<имя callback-функции>]

    :param text: <str> text for detect.
    :return: <str> lang text.
    """

    url = 'https://translate.yandex.net/api/v1.5/tr.json/detect'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'

    params = {
        'key': key,
        'text': text,
    }
    response = requests.get(url, params=params).json()
    return response.get('lang')

# получаем перевод текста из open_file() язык текста получили из detect_lang()
def translate_it(text, lang_sourse):
    """
    YANDEX translation plugin

    docs: https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/

    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]

    :param text: <str> text for translation.
    :return: <str> translated text.
    """
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
    key = 'trnsl.1.1.20161025T233221Z.47834a66fd7895d0.a95fd4bfde5c1794fa433453956bd261eae80152'
    # формируем параметр lang из имени оригинала
    lang = lang_sourse + '-ru'

    # парметры передаваемые яндексу для перевода.
    params = {
        'key': key,
        'lang': lang,
        'text': text,
    }
    response = requests.get(url, params=params).json()
    return ' '.join(response.get('text', []))

# создаем файлик txt с название оригинал + RU и пишем перевод в него
def write_to_file(text, file_name):
    with open(file_name, 'w', encoding='utf8') as f:
        f.write(text)


def main_function(file_name):
    name, extension = os.path.splitext(file_name)
    text = open_file(file_name)
    lang_sourse = detect_lang(text)
    text_translate = translate_it(text, lang_sourse)
    name_result = name + '_RU.txt'
    write_to_file(text_translate, name_result)


# задаем колличество потоков
num_threads = 4

"""
создаем потоки в кол-е num_threads асинхронные передаем executor-у список файлов 
и функцию которая обрарбатывает их, с помошью map все это собираем в кучу
zip используем для состыковуи операции и имя файла для вывода его имени в печать)
"""
print('Начало работы скрипта', ctime())

file_list = ['DE.txt', 'EN.txt','ES.txt', 'FR.txt']
with ThreadPoolExecutor(num_threads) as executor:
    for file, funk in zip(file_list, executor.map(main_function, file_list)):
        print(file, '  -->  done in  ', ctime())

print('Конец работы скрипта', ctime())

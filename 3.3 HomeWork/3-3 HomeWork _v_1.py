import requests
import os
from time import ctime

# открываем файлик с текстом для перевода
def open_file(file_name):
    with open(file_name, 'r', encoding='utf8') as f:
        text = f.read()
    return text

# получаем перевод язык оригинала берем из названия файла
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
    lang = lang_sourse.lower() + '-ru'

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

# собираем в кучу все
def main_function():
    file_list = ['DE.txt', 'EN.txt','ES.txt', 'FR.txt' ]
    for file_name in file_list:
        name, extension = os.path.splitext(file_name)
        text = open_file(file_name)
        text_translate = translate_it(text, name)
        name_result = name + '_RU.txt'
        write_to_file(text_translate, name_result)


print('Начало работы скрипта', ctime())
main_function()
print('Конец работы скрипта', ctime())

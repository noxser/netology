import chardet
import json

# добавил через вебморду гитхаба для проверки ))) IDE PyCharm

# основная фун-я для сбора всего в кучу и обработки файлов
def main_function():
    file_list = ['newsafr.json', 'newscy.json', 'newsfr.json', 'newsit.json']
    for file_name in file_list:
        encoding_type = decoding_file(file_name)
        count_dict = open_file(file_name, encoding_type)
        print_sort_words(count_dict)


# Открывает файл для декодирования выдает тип кодировки документа
def decoding_file(file):
    with open(file, 'rb') as f:
        data = f.read()
        result = chardet.detect(data)
    return result['encoding']


# окрываем файл уже с нужно кодировкой и обрабатываем его как json
def open_file(file_name, encoding_type):
    with open(file_name, encoding=encoding_type) as f:
        data = json.load(f)
        list_words = []
        count_dict = {}
        # собираем в кучу весь текст из 'title' и 'description'
        # преобразуем все всписок слов
        # далее отбрасываем мелоч
        # создаем словарик ключ это слово значение кол-во повторений
        for text_news in data['rss']['channel']['items']:
            list_words += (text_news['title']).split()
            list_words += (text_news['description']).split()
        for word in list_words:
            if len(word) < 6:
                continue
            else:
                if word.lower() not in count_dict:
                    count_dict[word.lower()] = int(list_words.count(word))
        print('В файле {} * {} * обработано:'.format(f.name, (data['rss']['channel']['title'])))
        print('Cлов {} шт. '.format(len(list_words)))
        print('Уникальных слов {} шт. длиной более 5 символов'.format(len(count_dict)))
        print('Новостей {} шт обработанно.'.format(len(data['rss']['channel']['items'])))
    return count_dict


# для удорбства отдельно вынес печать 10 наиболее встречаемых слов
def print_sort_words(count_dict):
    # отсортировали по значения словарь и перевернул чтобы самое большое было первым
    # циклом почистил его оставив 10 значений с начала
    # пока придумал так можно и лучше ))) но пока знаний нехватает )
    reves_count_dict = (dict(reversed((sorted(count_dict.items(), key=lambda item: item[1])))))
    reves_count_dict_sorted = {}
    for key, value in reves_count_dict.items():
        if len(reves_count_dict_sorted) < 10:
            reves_count_dict_sorted[key] = value
    for key, value in reves_count_dict_sorted.items():
        print('{1} - {0}'.format(key, value))
    print('\n')


main_function()

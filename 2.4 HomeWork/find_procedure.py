# # находим файлы с расширение sql в папке migration с помощью glob
# import glob
# new_list = glob.glob(os.path.join(Migration_abs_path, '*.sql'))
# new_list = glob.glob("*.sql")

# # находим файлы с расширение sql в папке migration с помощью endswith
#
# file_list = os.listdir(Migration_abs_path)
# new_list = []
# for file in file_list:
#     if file.endswith('.sql') == True:
#         new_list.append(file)

# # находим файлы с расширение sql в папке migration с помощью path.splitext
#
# files = os.listdir(Migration_abs_path)
# new_list = []
# for file in files:
#     name, extension = os.path.splitext(file)
#     if extension == '.sql':
#         new_list.append(file)


import os.path

def find_migrations():
    ''' Генерируем абсолютный путь до папки Migrations '''
    tree = os.walk(os.getcwd())
    for d in tree:
        if d[0].find('Migrations') >= 0:
            # можно .count() > 0
            migration_abs_path = d[0]
    return migration_abs_path

def sort_for_extension():
    ''' Находим файлы с расширение sql в папке migration с помощью path.splitext '''
    migration_abs_path = os.path.abspath(os.path.dirname(__file__))
    files = os.listdir(migration_abs_path)
    new_list = []
    for file in files:
        name, extension = os.path.splitext(file)
        if extension == '.sql':
            new_list.append(file)
    return new_list, migration_abs_path

def loop(new_list, migration_abs_path):
    comand = input('Введите ключевое слово или значение\nq для завершения\n')
    if comand == 'q':
        exit()
    sort_list = []
    path, dir_name = os.path.split(migration_abs_path)
    for new_file in new_list:
        with open((os.path.join(migration_abs_path, new_file)), encoding='utf8') as f:
            s = f.read()
            if comand in s:
                sort_list.append(new_file)
                print(os.path.join(dir_name, new_file))
    print('Всего: {}\n'.format(len(sort_list)))
    # используем рекурсию для вызова функции саму собой
    # передаем ей отсортированный список в предедущей итерации и
    # так далее выход по q
    return loop(sort_list, migration_abs_path)

def my_main():
    # migration_abs_path = find_migrations()
    new_list, migration_abs_path = sort_for_extension()
    loop(new_list, migration_abs_path)

my_main()

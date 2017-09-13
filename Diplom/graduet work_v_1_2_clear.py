from time import sleep, ctime
import requests
import json


TOKEN = ''
VERSION = '5.68'


def check_input_ids():
    """
    Получает айди или идентификатор неважно отправляет get запрос на vk
    и обрабатывает ответ на валидность есть юзер, нет тактого или деактивирован
    если юзер Валиден то возврашает id и отдает в процесс
    """
    while True:
        params = {'access_token': TOKEN, 'v': VERSION}
        params['user_ids'] = input('Введите ID для поиска ')
        response = requests.get('https://api.vk.com/method/users.get', params)
        if response.json().get('error', 'active') == 'active':
            if response.json()['response'][0].get('deactivated', 'yes') == 'yes':
                valid_id = response.json()['response'][0]['id']
            else:
                print('Пользователь с таким id деактивирован\n')
                continue
            break
        else:
            print('Пользователя с таким id не существует\n')
    return valid_id


def get_get(**kwargs):
    """
    Принимает url для get Запроса и параметры, формирует запрос
    и возврашает ответ, а дальше уже его другие функции разбирают
    """
    params = {'access_token': TOKEN, 'v': VERSION}
    urls = kwargs['url']
    kwargs.pop('url')
    for key, value in kwargs.items():
        params[key] = value
    response = requests.get(urls, params)
    return response


def friends_list(user_id):
    """
    Вызываем get_json скармливаем ей url и параметры передаваемые в запросе.
    Только список друзей возврашает ID пользователей
    """
    response = get_get(url='https://api.vk.com/method/friends.get', user_id=user_id)
    return (response.json())['response']['items']


def user_groups(user_id):
    """
    Вызываем get_json скармливаем ей url и параметры передаваемые в запросе.
    Формирует список групп.
    """
    response = get_get(url='https://api.vk.com/method/groups.get', count='1000', extended='0', user_id=user_id)
    return response.json()


def personal_group(friends_list, user_id_glob):
    """
    запрашиваем группы внешней функцией и ищем уникальные
    группы которые есть только у юзера чей айди ввели в начале
    """
    us_gr = set(user_groups(user_id_glob)['response']['items'])
    i = 0
    for user in friends_list:
        sleep(0.35)
        i += 1
        gr = user_groups(user)  # список групп друга
        if gr.get('error', 'active') == 'active':  # делаем проверку на error
            fr_gr = set(gr['response']['items'])  # преобразуем во множество
        # находим уникальные группы из 2-х множеств которые принадлежат только 1
            us_gr = us_gr - fr_gr
        # нарыл клевую штуку для печати процесса работы )
        print('\rПроверенно друзей {} из {}'.format(i, len(friends_list)), end='', flush=True)
    return us_gr


def group_info(group_ids):
    """
    Вызываем get_json скармливаем ей url и параметры передаваемые в запросе.
    Получаем информацию о группах и тут уже формируем для выгрузки в json.
    """
    response = get_get(
        url='https://api.vk.com/method/groups.getById',
        group_ids=','.join(map(str, group_ids)),
        fields='members_count'
    )
    gr_lst = []
    for gr in (response.json())['response']:
        if gr.get('deactivated', 'active') == 'active':
            gr_dict = {'name': gr['name'], 'gid': gr['id'], 'members_count': gr['members_count']}
            gr_lst.append(gr_dict)
    return gr_lst


def write_json(data):
    """
    формируем json
    """
    with open('groups.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1, ensure_ascii=0)


# собираем все в кучу
if __name__ == '__main__':
    user_id_glob = check_input_ids()
    print()
    print('Начало работы скрипта', ctime())
    print('----------------------------------------------')
    fr_lst = friends_list(user_id_glob)
    us_gr = user_groups(user_id_glob)['response']['items']
    print('Список друзей и групп пользователя сформирован')
    print('Друзей {}\nГрупп {}'.format(len(fr_lst), len(us_gr)))
    print('----------------------------------------------')
    print('Идет шпионаж, сидите тихо')
    sleep(1)
    a = (personal_group(fr_lst, user_id_glob))
    print()
    print('----------------------------------------------')
    sleep(1)
    print('У пользователя уникальных групп {} из {}'
          .format(len(a), len(us_gr))
          )
    sleep(1)
    write_json(group_info(a))
    print('----------------------------------------------')
    print('Список групп находиться в файле groups.json')
    print('----------------------------------------------')
    print('Конец работы скрипта', ctime())
from time import sleep, ctime
import requests
import json

#  для проверок
#  5030613 из заданимя 835 друга 122 группы
#  4556271 мой 72 друга 56 групп

TOKEN = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'
VERSION = '5.68'
params = {'access_token': TOKEN, 'v': VERSION}


def friends_list(params, user_id):
    """
    только список друзей возврашает ID пользователей
    """
    params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/friends.get', params)
    return (response.json())['response']['items']


def user_groups(params, user_id):
    """
    формирует ответ от groups.get
    """
    params['count'] = '1000'
    params['extended'] = '0'
    params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/groups.get', params)
    return response.json()


def personal_group(params, friends_list, user_id_glob):
    """
    запрашиваем группы внешней функцией и ищем уникальные
    группы которые есть только у юзера чей айди ввели в начале
    """
    us_gr = set(user_groups(params, user_id_glob)['response']['items'])
    i = 0
    for user in friends_list:
        sleep(0.35)
        i += 1
        gr = user_groups(params, user)  # список групп друга
        if gr.get('error', 'active') == 'active':  # делаем проверку на error
            fr_gr = set(gr['response']['items'])  # преобразуем во множество
        # находим уникальные группы из 2-х множеств которые принадлежат только 1
            us_gr = us_gr - fr_gr
        # нарыл клевую штуку для печати процесса работы )
        print('\rПроверенно друзей {} из {}'.format(i, len(friends_list)), end='', flush=True)
    return us_gr


def group_info(params, group_ids):
    """
    получаем информацию о группах и тут уже формируем для выгрузки в json
    """
    params['group_ids'] = ','.join(map(str, group_ids))
    params['fields'] = 'members_count'
    response = requests.get('https://api.vk.com/method/groups.getById', params)
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
    user_id_glob = int(input('Введите ID для поиска '))
    print()
    print('Начало работы скрипта', ctime())
    print('----------------------------------------------')
    fr_lst = friends_list(params, user_id_glob)
    us_gr = user_groups(params, user_id_glob)['response']['items']
    print('Список друзей и групп пользователя сформирован')
    print('Друзей {}\nГрупп {}'.format(len(fr_lst), len(us_gr)))
    print('----------------------------------------------')
    print('Идет шпионаж, сидите тихо')
    sleep(1)
    a = (personal_group(params, fr_lst, user_id_glob))
    print()
    print('----------------------------------------------')
    sleep(1)
    print('У пользователя уникальных групп {} из {}'
          .format(len(a), len(us_gr))
          )
    sleep(1)
    write_json(group_info(params, a))
    print('----------------------------------------------')
    print('Список групп находиться в файле groups.json')
    print('----------------------------------------------')
    print('Конец работы скрипта', ctime())


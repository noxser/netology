from time import sleep, ctime, time
from pprint import pprint
import requests
import json
import sys


TOKEN = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'
VERSION = '5.67'
params = {'access_token': TOKEN, 'v': VERSION}


# только список друзей возврашает ID пользователей
# для ускорения френдлист режу на 10
def friends_list(params, user_id):
    params['user_id'] = user_id
    params['count'] = '10'
    response = requests.get('https://api.vk.com/method/friends.get', params)
    return (response.json())['response']['items']


# формирует ответ от groups.get

def user_groups(params, user_id):
    params['count'] = '1000'
    params['extended'] = '0'
    params['user_id'] = user_id
    response = requests.get('https://api.vk.com/method/groups.get', params)
    return response.json()


#запрашиваем группы внешней функцией и ищем уникальные
# тут же обрабатываем ответ на запрос group.get
# и проверяем валидность запроса если все ок делаем сравнение списков
# если бэд то переходим к след итерации

def personal_group(params, friends_list, user_id_glob):
    # список групп User-а
    a = set(user_groups(params, user_id_glob)['response']['items'])
    i = 0
    b = None
    for user in friends_list:
        i += 1
        try:  # на случай падения падает на узере у которго 2800 групп и не помогает
              # ограничние на 1000
            x = user_groups(params, user) # список групп друга
            if x.get('error', 'active') == 'active': # делаем проверку на error
                b = set(x['response']['items']) # преобразуем в множество
        except BaseException:
            continue
        # находим уникальные группы из 2-х множеств которые принадлежат только 1
        a = a - b
        # нарыл клевую штуку для печати процесса работы )
        print('\rПроверенно друзей {} из {}'.format(i, len(friends_list)), end='', flush=True)

    return a


# получаем информацию о группах и тут уже формируем для выгрузки в json
def group_info(params, group_ids):
    params['group_ids'] = ','.join(map(str, group_ids))
    params['fields'] = 'members_count'
    response = requests.get('https://api.vk.com/method/groups.getById', params)
    gr_lst = []
    for gr in (response.json())['response']:
        if gr.get('deactivated', 'active') == 'active':
            gr_dict = {}
            gr_dict['name'] = gr['name']
            gr_dict['gid'] = gr['id']
            gr_dict['members_count'] = gr['members_count']
            gr_lst.append(gr_dict)
    return gr_lst


# собираем все в кучу
def main_script(user_id_glob):
    print('Начало работы скрипта', ctime())
    print('-------------------------')
    fr_lst = friends_list(params, user_id_glob)
    print('Список друзей сформирован', ctime())
    print('Друзей', len(fr_lst))
    print('-------------------------')
    print('Идет шпионаж')
    a = (personal_group(params, fr_lst, user_id_glob))
    print()
    print('-------------------------')
    print('У данного пользователя {} уникальных групп из {}'
          .format(len(a), len(user_groups(params, user_id_glob)['response']['items']))
        )
    b = group_info(params, a)
    with open('groups.json', 'w', encoding='utf-8') as f:
        json.dump(b, f, indent=1, ensure_ascii=0)
    print('-------------------------')
    print('Список групп находиться в файле groups.json')
    print('-------------------------')
    print('Конец работы скрипта', ctime())


user_id_glob = '4556271' # мой адишник
# user_id_glob = '5030613' # препода адишник
main_script(user_id_glob)

# pprint(len(friends_list(params, user_id_glob)))
# print(user_groups(params, 4556271))


# 179265 айдишник на котором все лмаеться 2880 групп у него
# 326161 нет групп тоже ломалось
# 178919029 удален узер

# мой 4556271
# из задания 5030613



from time import sleep, ctime
import requests


TOKEN = ''
VERSION = '5.67'
params = {'access_token': TOKEN, 'v': VERSION}


# Список друзей ID ид берем из токена тоесть мои друзья
# только список ID друзей возврашает
def my_friends(params):
    response = requests.get('https://api.vk.com/method/friends.get', params)
    return (response.json())['response']['items']


# убираем деактивированных пользователей
def sort_my_friend(params, my_friends_list):
    my_friends_list_new = []
    params['user_ids'] = ','.join(map(str, my_friends_list))
    response = requests.get('https://api.vk.com/method/users.get', params)
    for friend in response.json()['response']:
        if friend.get('deactivated', 'active') == 'active':
             my_friends_list_new.append(friend['id'])
    return my_friends_list_new


# получаем инофрмацию по ID пользователя
def user_ifo(params, user_id):
    params['user_ids'] = user_id
    response = requests.get('https://api.vk.com/method/users.get', params)
    return response.json()['response'][0]['last_name'] + ' ' + response.json()['response'][0]['first_name']

# ищем общих друзей friends.getMutual в помощь используем dict
def mutual_friends_dict(params, my_friends_list_new):
    i = 0
    mutual_friends_dict = {}
    for user in my_friends_list_new:
        # sleep(0.1) не нужен вроде гудворк и так
        if len(my_friends_list_new[i+1:]) == 0:
            continue
        params['source_uid'] = user
        params['target_uids'] = ','.join(map(str, my_friends_list_new[i+1:]))
        response = requests.get('https://api.vk.com/method/friends.getMutual', params)
        i += 1
        for k in list(response.json()['response'][0]['common_friends']):
            if k not in mutual_friends_dict:
                mutual_friends_dict[k] = 1
            else:
                mutual_friends_dict[k] += 1
    for key in mutual_friends_dict:
        if mutual_friends_dict[key] == len(my_friends_list_new)-1:
            print('Общий друг id {} {}'.format(key, user_ifo(params, key)))


# ищем общих друзей friends.getMutual в помощь используем set
def mutual_friends_set(params, my_friends_list_new):
    i = 0
    mutual_friends_list = set()
    for user in my_friends_list_new:
        # sleep(0.1)
        if len(my_friends_list_new[i + 1:]) == 0:
            continue
        params['source_uid'] = user
        params['target_uids'] = ','.join(map(str, my_friends_list_new[i + 1:]))
        response = requests.get('https://api.vk.com/method/friends.getMutual', params)
        i += 1
        x = set((response.json()['response'][0]['common_friends']))
        if len(mutual_friends_list) == 0:
            mutual_friends_list = mutual_friends_list | x
        else:
            mutual_friends_list = mutual_friends_list & x
    print('Общий друг id {} {}'.format((list(mutual_friends_list))[0], user_ifo(params, mutual_friends_list)))


# собираем все в кучу
def main_script():
    print('Начало работы скрипта', ctime())
    print('-------------------------')
    my_friends_list = my_friends(params)
    print('Список друзей сформирован', ctime())
    print('Друзей', len(my_friends_list))
    print('-------------------------')
    my_friends_list_new = sort_my_friend(params, my_friends_list)
    print('Список друзей обработан', ctime())
    print('Друзей в новом списке', len(my_friends_list_new))
    print('-------------------------')
    print('Идет поиск общих друзей ожидайте')
    mutual_friends_set(params, my_friends_list_new)
    print('-------------------------')
    print('Конец работы скрипта', ctime())

main_script()

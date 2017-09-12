from pprint import pprint
from urllib.parse import urlencode, urljoin
import requests


def get_token():
    AUTHORIZE_URL = 'https://oauth.yandex.ru/authorize'
    APP_ID = '299b4ed77d554b7bbe6d743e4d0a928e'

    auth_data = {
        'response_type': 'token',
        'client_id': APP_ID
    }

    print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))


TOKEN = ''


class YMmain:
    '''
    Базовый класс с урлами и хидерами )
    '''
    MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1/counters/'
    DATA_URL = 'https://api-metrika.yandex.ru/stat/v1/data'

    def get_headers(self):
        return {
            'Authorization': 'OAuth {}'.format(self.token),
            'Content-Type': 'application/x-yametrika+json',
            'User-Agent': 'asdasdasd'
        }


class YandexMetrika(YMmain):
    """
    формируем словарик с id и названием счетчика
    можно больше параметров передать но уже в списке
    """
    def __init__(self, token):
        self.token = token

    def get_counters(self):
        url = self.MANAGEMENT_URL
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        counters = response.json()['counters']
        return dict(zip([counter['id'] for counter in counters],
                        [counter['name'] for counter in counters]))


class Counter(YMmain):
    '''
    Информация по счетчику по отдельности по метрикам
    '''
    def __init__(self, token, count_id):
        self.token = token
        self.id = count_id


    def get_visits(self):
        headers = self.get_headers()
        params = {
            'id': self.id,
            'metrics': 'ym:s:visits'

        }
        response = requests.get(self.DATA_URL, params, headers=headers)
        return response.json()['totals']


    def get_pageviews(self):
        headers = self.get_headers()
        params = {
            'id': self.id,
            'metrics': 'ym:s:pageviews'

        }
        response = requests.get(self.DATA_URL, params, headers=headers)
        return response.json()['totals']


    def get_users(self):
        headers = self.get_headers()
        params = {
            'id': self.id,
            'metrics': 'ym:s:users'

        }
        response = requests.get(self.DATA_URL, params, headers=headers)
        return response.json()['totals']


# сам скрипт
if __name__ == "__main__":
    ym = YandexMetrika(TOKEN)
    for key, value in ym.get_counters().items():
        c = Counter(TOKEN, key)
        print('Наименование счетчика: {}\n'
              'Идентификатор счетчика: {}\n'
              'Визитов: {}\n'
              'Просмотров {}\n'
              'Пользователей {}\n'.format(
            value,
            key,
            c.get_visits()[0],
            c.get_pageviews()[0],
            c.get_users()[0])
        )

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


TOKEN = 'AQAAAAAAgX7SAARxH30zPEAhW047muFOlPvfcc4'


class YandexMetrika:
    MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1/counters/'
    headers = {
        'Authorization': 'OAuth {}'.format(TOKEN),
        'Content-Type': 'application/x-yametrika+json',
    }

    def __init__(self, token):
        self.token = token

    def get_counters(self):
        """
        формируем словарик с id и названием счетчика
        можно больше параметров передать но уже в списке
        """
        url = self.MANAGEMENT_URL
        headers = self.headers
        response = requests.get(url, headers=headers)
        counters = response.json()['counters']
        return dict(zip([counter['id'] for counter in counters],
                        [counter['name'] for counter in counters]))

    def get_visits_pageviews_users(self, count_id):
        """
        запрашиваем информацию по счетчику v, p, u
        """
        url = 'https://api-metrika.yandex.ru/stat/v1/data'
        headers = self.headers
        params = {
            'id': count_id,
            'metrics': 'ym:s:visits, ym:s:pageviews, ym:s:users'

        }
        response = requests.get(url, params, headers=headers)
        vpu = response.json()['totals']
        print(
            'Визитов {}\nПросмотров {}\nПользователей {}\n'.format(
                vpu[0], vpu[1], vpu[2]
            ))

    def get_counters_info(self):
        """
        Выводим всю информацию по счетчикам YM
        """
        for key, value in ym.get_counters().items():
            print('Наименование счетчика: {}\n'
                  'Идентификатор счетчика: {}\n'.format(value, key))
            ym.get_visits_pageviews_users(key)


ym = YandexMetrika(TOKEN)
ym.get_counters_info()

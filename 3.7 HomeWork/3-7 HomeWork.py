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


class YandexMetrika:
    MANAGEMENT_URL = 'https://api-metrika.yandex.ru/management/v1/counters/'
    headers = {
        'Authorization': 'OAuth {}'.format(TOKEN),
        'Content-Type': 'application/x-yametrika+json',
    }

    visits = None
    pageviews = None
    users = None

    def __init__(self, token):
        self.token = token

    def get_counters(self):
        url = self.MANAGEMENT_URL
        headers = self.headers
        response = requests.get(url, headers=headers)
        counters = response.json()['counters']
        return counters[0]['id']

    def get_visits_pageviews_users(self, count_id):
        url = 'https://api-metrika.yandex.ru/stat/v1/data'
        headers = self.headers
        params = {
            'id': count_id,
            'metrics': 'ym:s:visits, ym:s:pageviews, ym:s:users'

        }
        response = requests.get(url, params, headers=headers)
        # разбираем ответ и пишем в атрибуты
        self.visits = response.json()['totals'][0]
        self.pageviews = response.json()['totals'][1]
        self.users = response.json()['totals'][2]


ym = YandexMetrika(TOKEN)

print(ym.visits)
print(ym.pageviews)
print(ym.users)

counter = ym.get_counters()
ym.get_visits_pageviews_users(counter)

print('Визитов', ym.visits)
print('Просмотров', ym.pageviews)
print('Пользователе', ym.users)

import json
from requests import get


class ApiHH:
    _url = 'https://api.hh.ru/vacancies/'

    def __init__(self):
        pass

    def __str__(self):
        return 'HeadHunter.ru'

    def get_vacancies_api(self, company):
        params = {'employer_id': str(company)}
        response = get(self._url, params=params)

        if response.status_code == 200:
            data = response.json()['items']
            return data
        else:
            print(response.status_code)
            return None

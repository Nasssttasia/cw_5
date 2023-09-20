import json


def get_companies(filename='companies.json'):
    with open(filename, encoding='utf-8') as file:
        companies = json.load(file)
    return companies
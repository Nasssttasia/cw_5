from api_hh import ApiHH
from db_manager import DBManager
from utils import get_companies


def main():
    print('начало')
    db = DBManager()
    db.create_database()
    db.create_tables()
    companies = get_companies()
    db.insert_into_companies(companies)
    vacancies = []
    hh = ApiHH()
    for company in companies.values():
        vacancies.extend(hh.get_vacancies_api(company))
    db.insert_into_vacancies(vacancies)


if __name__ == '__main__':
    main()
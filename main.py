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

    db.get_companies_and_vacancies_count()
    db.get_all_vacancies()
    db.get_avg_salary()
    db.get_vacancies_with_higher_salary()
    db.get_vacancies_with_keyword('python')

if __name__ == '__main__':
    main()
from api_hh import ApiHH
from db_manager import DBManager
from utils import get_companies


def main():
    print('Начало работы! :)\n')
    db = DBManager()
    db.create_database()
    print('База данных создана!\n')
    db.create_tables()
    print('Таблицы созданы!\n')
    companies = get_companies()
    db.insert_into_companies(companies)
    print('Компании записаны!')
    vacancies = []
    hh = ApiHH()
    for company in companies.values():
        vacancies.extend(hh.get_vacancies_api(company))
    db.insert_into_vacancies(vacancies)
    print('Вакансии тоже!\n')

    print(db.get_companies_and_vacancies_count())
    print(db.get_all_vacancies())
    print(db.get_avg_salary())
    print(db.get_vacancies_with_higher_salary())
    print(db.get_vacancies_with_keyword('Менеджер'))

    print('\nКонец работы! :(')


if __name__ == '__main__':
    main()

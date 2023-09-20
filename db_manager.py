import psycopg2
from config import config


class DBManager:

    def __init__(self):
        self.params = config()
        self.db_name = "headhunter"

    def create_database(self) -> None:
        """Создает новую базу данных."""
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f'DROP DATABASE IF EXISTS {self.db_name}')
        cur.execute(f'CREATE DATABASE {self.db_name}')
        conn.close()

    def create_tables(self):
        with psycopg2.connect(**self.params, dbname=self.db_name) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE employers (
                        employer_id INT PRIMARY KEY,
                        title VARCHAR(100)
                    )
               """)

                cur.execute("""
                    CREATE TABLE vacancies (
                        vacancy_id INT PRIMARY KEY,
                        title VARCHAR(100),
                        employer_id INT REFERENCES employers (employer_id),
                        url VARCHAR,
                        salary_from INT,
                        requirement VARCHAR
                    )
               """)

                conn.commit()

    def insert_into_companies(self, values):
        companies = [(value, key) for key, value in values.items()]
        with psycopg2.connect(**self.params, dbname=self.db_name) as conn:
            with conn.cursor() as cur:
                cur.executemany('INSERT INTO employers ("employer_id", "title") VALUES (%s, %s)', companies)
            conn.commit()

    def insert_into_vacancies(self, values):
        vacancies = []
        for vacancy in values:
            salary_min = vacancy['salary']['from'] if vacancy['salary'] and vacancy['salary']['from'] else None
            vacancies.append((
                vacancy['id'],
                vacancy['name'],
                vacancy['employer']['id'],
                vacancy['alternate_url'],
                salary_min,
                vacancy['snippet']['requirement'],
            ))
        with psycopg2.connect(**self.params, dbname=self.db_name) as conn:
            with conn.cursor() as cur:
                cur.executemany('INSERT INTO vacancies ("vacancy_id", "title", "employer_id", "url", "salary_from", "requirement") VALUES (%s, %s, %s, %s, %s, %s)', vacancies)
            conn.commit()

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""
        with psycopg2.connect(**self.params, dbname=self.db_name) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT employers.title, COUNT(*) '
                            'FROM vacancies '
                            'JOIN employers USING(employer_id) '
                            'GROUP BY employers.title')
            conn.commit()

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        with psycopg2.connect(**self.params, dbname=self.db_name) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT b.title, a.title, a.salary_from, a.url '
                            'FROM vacancies a'
                            'JOIN employers b USING(employer_id)')
            conn.commit()

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        with psycopg2.connect(**self.params, dbname=self.db_name) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT AVG(salary_from) as средняя_зарплата'
                            'FROM vacancies')
            conn.commit()

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with psycopg2.connect(**self.params, dbname=self.db_name) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT *'
                            'FROM vacancies'
                            'WHERE salary_from > AVG(salary_from)')
            conn.commit()

    def get_vacancies_with_keyword(self, word):
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        with psycopg2.connect(**self.params, dbname=self.db_name) as conn:
            with conn.cursor() as cur:
                cur.executemany('SELECT *'
                            'FROM vacancies'
                            'WHERE title LIKE "%s%"', word)
            conn.commit()


'''
"""--получает список всех компаний и количество вакансий у каждой компании."""
SELECT employers.title, COUNT(*) 
FROM vacancies
JOIN employers USING(employer_id)
GROUP BY employers.title


--получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
SELECT b.title, a.title, a.salary_from, a.url 
FROM vacancies a
JOIN employers b USING(employer_id)

--получает среднюю зарплату по вакансиям."""
SELECT AVG(salary_from) as средняя_зарплата
FROM vacancies

--получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
SELECT *
FROM vacancies
WHERE salary_from > AVG(salary_from)
????????????????

--получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
SELECT *
FROM vacancies
WHERE title LIKE '%word%'

'''
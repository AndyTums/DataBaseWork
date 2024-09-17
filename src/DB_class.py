import psycopg2

from params import conns


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(dbname="course", **conns())
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """ Возвращает наименование работодателя и кол-во его вакансий """

        self.cur.execute("SELECT employ_name, count_vacancies FROM employees")

        return self.cur.fetchall()

    def get_all_vacancies(self):
        """ Получает список всех вакансий с указанием названия компании,
                названия вакансии и зарплаты и ссылки на вакансию """

        self.cur.execute("SELECT employ_name, vacancy_name, vacancy_salary, vacancy_url FROM vacancies "
                         "JOIN employees USING(employ_id)")

        return self.cur.fetchall()

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям """

        self.cur.execute("SELECT AVG(vacancy_salary) FROM vacancies")

        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """ Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям. """

        self.cur.execute("SELECT vacancy_id, vacancy_name, vacancy_salary, vacancy_url, employ_id "
                         "FROM vacancies GROUP BY vacancy_id "
                         "HAVING vacancy_salary > (SELECT AVG(vacancy_salary) FROM vacancies)")

        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, word):
        """ Получает список всех вакансий, в названии которых содержатся переданные в метод слова """

        self.cur.execute(f"SELECT * FROM vacancies "
                         f"WHERE vacancy_name LIKE '%{word}%'")

        return self.cur.fetchall()

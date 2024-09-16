import psycopg2
from work_db import conns


class DBManager:
    def __init__(self, dbname):

        self.params = conns()
        self.conn = psycopg2.connect(dbname=dbname, **self.params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """ Возвращает наименование работодателя и кол-во его вакансий """

        self.cur.execute("SELECT employ_name, count_vacancies FROM employees")

        return self.cur.fetchall()

    def get_companies_and_vacancies_count(self):
        """ Возвращает наименование работодателя и кол-во его вакансий """

        self.cur.execute("SELECT employ_name, count_vacancies FROM employees")

        return self.cur.fetchall()



work_with_BD = DBManager("test1")
print(work_with_BD.get_companies_and_vacancies_count())

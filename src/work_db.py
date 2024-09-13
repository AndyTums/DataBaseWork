import psycopg2
import configparser
from API_info import get_info_api, get_info_vacancies


def conns(filename="../database.ini"):
    """ Считывание данных для подключения к БД """

    config = configparser.ConfigParser()
    config.read(filename)
    params = {"user": config["postgresql"]["user"],
              "password": config["postgresql"]["password"],
              "port": config["postgresql"]["port"]}

    return params


def create_db(dbname: str) -> None:
    """ Принимает наименование и создает БД """

    params = conns()  # Получаем данные для подключения к БД

    conn = psycopg2.connect(dbname="postgres", **params)
    cur = conn.cursor()
    conn.autocommit = True

    cur.execute(f'DROP DATABASE IF EXISTS {dbname}')
    cur.execute(f'CREATE DATABASE {dbname}')

    print("База данных успешно создана")

    cur.close()
    conn.close()


def work_in_db(dbname: str) -> None:
    """ Создает две таблицы в POSTGRESQL: employees, vacancies """

    params = conns()  # Собираем данные для соединения с БД

    with psycopg2.connect(dbname=dbname, **params) as conn:  # Подключаемся к БД
        with conn.cursor() as cur:  # Создаем таблицу employees
            cur.execute("CREATE TABLE employees("
                        "employ_id INT PRIMARY KEY,"
                        "employ_name VARCHAR NOT NULL,"
                        "count_vacancies INT,"
                        "vacancies_url TEXT)")
            print("Таблица employees успешно создана!")

        with conn.cursor() as cur:  # Создаем таблицу vacancies
            cur.execute("""
                            CREATE TABLE vacancies(
                            vacancy_id INT PRIMARY KEY,
                            vacancy_name VARCHAR NOT NULL,
                            vacancy_salary INT,
                            vacancy_url TEXT,
                            employ_id INT REFERENCES employees(employ_id))
                            """)
            print("Таблица vacancies успешно создана!")

        conn.commit()  # Делаем сохранение изменений


def add_info_table(list_info: list, dbname: str, table: str) -> None:
    params = conns()  # Собираем данные для соединения с БД

    with psycopg2.connect(dbname=dbname, **params) as conn:  # Подключаемся к БД
        if table.lower() == "employees":  # Работа с таблицей employees
            with conn.cursor() as cur:  # Заполняем таблицу employees
                for i in list_info:
                    query = (f"INSERT INTO employees (employ_id, employ_name, count_vacancies, vacancies_url) "
                             f"VALUES {i["id"], i["name"], i["open_vacancies"], i["vacancies_url"]}")
                    cur.execute(query, i)

        elif table.lower() == "vacancies":  # Работа с таблицей vacancies
            with conn.cursor() as cur:  # Заполняем таблицу vacancies
                for i in list_info:
                    query = (f"INSERT INTO vacancies (vacancy_id, vacancy_name, vacancy_salary)"
                             f"VALUES {i["vacancies"]["id"], i["vacancies"]["name"], i["vacancies"]["salary"]["from"]}")
                    cur.execute(query, i)

    conn.commit()
    print("Информация успешна добавлена в БД и сохранена!")

import psycopg2

from params import conns


def create_db(dbname: str) -> None:
    """ Принимает наименование и создает БД """

    print("Создаем базу данных...")

    params = conns()  # Получаем данные для подключения к БД

    conn = psycopg2.connect(dbname="postgres", **params)
    cur = conn.cursor()
    conn.autocommit = True

    cur.execute(f'DROP DATABASE IF EXISTS {dbname}')
    cur.execute(f'CREATE DATABASE {dbname}')

    print("База данных успешно создана.\n")

    cur.close()
    conn.close()


def create_table(dbname: str) -> None:
    """ Создает две таблицы в POSTGRESQL: employees, vacancies """

    print("Настраиваем таблицы...")

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
                            vacancy_id INT,
                            vacancy_name VARCHAR NOT NULL,
                            vacancy_salary INT,
                            vacancy_url TEXT,
                            employ_id INT, 
                            FOREIGN KEY (employ_id) REFERENCES employees(employ_id))
                            """)
            print("Таблица vacancies успешно создана!\n")

        conn.commit()  # Делаем сохранение изменений


def add_info_table(list_info: list, dbname: str, table: str) -> None:
    """ Принимает список информации, имя БД, имя таблицы и добавляет информацию в БД """

    params = conns()  # Собираем данные для соединения с БД

    with psycopg2.connect(dbname=dbname, **params) as conn:  # Подключаемся к БД
        if table.lower() == "employees":
            with conn.cursor() as cur:  # Заполняем таблицу employees
                for i in list_info:
                    query = (f"INSERT INTO employees (employ_id, employ_name, count_vacancies, vacancies_url) "
                             f"VALUES {i["id"], i["name"], i["open_vacancies"], i["vacancies_url"]}")
                    cur.execute(query, i)
        elif table.lower() == "vacancies":

            with conn.cursor() as cur:  # Заполняем таблицу vacancies
                for i in list_info:
                    if i["vacancies"]["salary"] is None or i["vacancies"]["salary"]["from"] is None:
                        query = (f"INSERT INTO vacancies "
                                 f"VALUES {i["vacancies"]["id"], i["vacancies"]["name"], 0, i["vacancies"]["url"], i["employees"]}")
                        cur.execute(query, i)

                    else:
                        query = (f"INSERT INTO vacancies "
                                 f"VALUES {i["vacancies"]["id"], i["vacancies"]["name"], i["vacancies"]["salary"]["from"], i["vacancies"]["url"], i["employees"]}")
                    cur.execute(query, i)

    conn.commit()

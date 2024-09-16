import psycopg2
import configparser
from API_info import get_info_api, get_info_vacancies
from API_info import info_api


def conns(filename="../database.ini"):
    """ Считывание данных для подключения к БД """

    config = configparser.ConfigParser()
    config.read(filename)
    params = {"user": config["postgresql"]["user"],
              "password": config["postgresql"]["password"],
              "port": config["postgresql"]["port"]}

    return params


re = conns()


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
                    if i["vacancies"]["salary"]:
                        query = (f"INSERT INTO vacancies "
                                 f"VALUES {i["vacancies"]["id"], i["vacancies"]["name"], i["vacancies"]["salary"]["from"], i["vacancies"]["url"], i["employees"]}")

                    else:
                        query = (f"INSERT INTO vacancies"
                                 f"VALUES {i["vacancies"]["id"], i["vacancies"]["name"], 0, i["vacancies"]["url"], i["employees"]}")
                    cur.execute(query, i)

    conn.commit()
    print("Информация успешна добавлена в БД и сохранена!")


info_1_vacanc = [{'employees': '3786259', 'vacancies': {'id': '107222544', 'premium': False,
                                                        'name': 'Региональный менеджер по оптовым продажам (продвижение ТМ DCK)',
                                                        'department': None, 'has_test': False,
                                                        'response_letter_required': False,
                                                        'area': {'id': '54', 'name': 'Красноярск',
                                                                 'url': 'https://api.hh.ru/areas/54'},
                                                        'salary': {'from': 90000, 'to': 200000, 'currency': 'RUR',
                                                                   'gross': False},
                                                        'type': {'id': 'open', 'name': 'Открытая'},
                                                        'address': None, 'response_url': None,
                                                        'sort_point_distance': None,
                                                        'published_at': '2024-09-13T07:12:44+0300',
                                                        'created_at': '2024-09-13T07:12:44+0300', 'archived': False,
                                                        'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=107222544',
                                                        'branding': {'type': 'MAKEUP', 'tariff': None},
                                                        'show_logo_in_search': True, 'insider_interview': None,
                                                        'url': 'https://api.hh.ru/vacancies/107222544?host=hh.ru',
                                                        'alternate_url': 'https://hh.ru/vacancy/107222544',
                                                        'relations': [],
                                                        'employer': {'id': '3786259', 'name': '100ДЕЛ',
                                                                     'url': 'https://api.hh.ru/employers/3786259',
                                                                     'alternate_url': 'https://hh.ru/employer/3786259',
                                                                     'logo_urls': {
                                                                         'original': 'https://img.hhcdn.ru/employer-logo-original/1062676.png',
                                                                         '90': 'https://img.hhcdn.ru/employer-logo/5871337.png',
                                                                         '240': 'https://img.hhcdn.ru/employer-logo/5871338.png'},
                                                                     'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=3786259',
                                                                     'accredited_it_employer': False, 'trusted': True},
                                                        'snippet': {
                                                            'requirement': 'Желательно знание продукта (инструмент и оборудование), опыт продаж. Знание рынка сбыта (опыт развития дилерской и дистрибьюторской сети, крупный опт, оптовые...',
                                                            'responsibility': 'Поиск и привлечение новых клиентов на закрепленной территории. Личное участие в переговорах с ключевыми партнерами. Проведение переговоров и заключение контрактов...'},
                                                        'contacts': None,
                                                        'schedule': {'id': 'fullDay', 'name': 'Полный день'},
                                                        'working_days': [], 'working_time_intervals': [],
                                                        'working_time_modes': [], 'accept_temporary': False,
                                                        'professional_roles': [
                                                            {'id': '129', 'name': 'Торговый представитель'}],
                                                        'accept_incomplete_resumes': True,
                                                        'experience': {'id': 'between1And3',
                                                                       'name': 'От 1 года до 3 лет'},
                                                        'employment': {'id': 'full', 'name': 'Полная занятость'},
                                                        'adv_response_url': None, 'is_adv_vacancy': False,
                                                        'adv_context': None}}, {'employees': '3786259',
                                                                                'vacancies': {'id': '106948140',
                                                                                              'premium': False,
                                                                                              'name': 'Оператор 1С в торговом зале',
                                                                                              'department': None,
                                                                                              'has_test': False,
                                                                                              'response_letter_required': False,
                                                                                              'area': {'id': '4',
                                                                                                       'name': 'Новосибирск',
                                                                                                       'url': 'https://api.hh.ru/areas/4'},
                                                                                              'salary': {'from': 50000,
                                                                                                         'to': None,
                                                                                                         'currency': 'RUR',
                                                                                                         'gross': False},
                                                                                              'type': {'id': 'open',
                                                                                                       'name': 'Открытая'},
                                                                                              'address': {
                                                                                                  'city': 'Новосибирск',
                                                                                                  'street': 'Троллейная улица',
                                                                                                  'building': '52',
                                                                                                  'lat': 54.984827,
                                                                                                  'lng': 82.857817,
                                                                                                  'description': None,
                                                                                                  'raw': 'Новосибирск, Троллейная улица, 52',
                                                                                                  'metro': None,
                                                                                                  'metro_stations': [],
                                                                                                  'id': '14618906'},
                                                                                              'response_url': None,
                                                                                              'sort_point_distance': None,
                                                                                              'published_at': '2024-09-16T02:18:23+0300',
                                                                                              'created_at': '2024-09-16T02:18:23+0300',
                                                                                              'archived': False,
                                                                                              'apply_alternate_url': 'https://hh.ru/applicant/vacancy_response?vacancyId=106948140',
                                                                                              'branding': {
                                                                                                  'type': 'MAKEUP',
                                                                                                  'tariff': None},
                                                                                              'show_logo_in_search': True,
                                                                                              'insider_interview': None,
                                                                                              'url': 'https://api.hh.ru/vacancies/106948140?host=hh.ru',
                                                                                              'alternate_url': 'https://hh.ru/vacancy/106948140',
                                                                                              'relations': [],
                                                                                              'employer': {
                                                                                                  'id': '3786259',
                                                                                                  'name': '100ДЕЛ',
                                                                                                  'url': 'https://api.hh.ru/employers/3786259',
                                                                                                  'alternate_url': 'https://hh.ru/employer/3786259',
                                                                                                  'logo_urls': {
                                                                                                      'original': 'https://img.hhcdn.ru/employer-logo-original/1062676.png',
                                                                                                      '90': 'https://img.hhcdn.ru/employer-logo/5871337.png',
                                                                                                      '240': 'https://img.hhcdn.ru/employer-logo/5871338.png'},
                                                                                                  'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=3786259',
                                                                                                  'accredited_it_employer': False,
                                                                                                  'trusted': True},
                                                                                              'snippet': {
                                                                                                  'requirement': None,
                                                                                                  'responsibility': 'Вести учетные операции по движению товара в магазине, оформление безналичных продаж товаров. Контроль, учет денежной наличности. Кассовая отчетность, оформление документации. '},
                                                                                              'contacts': None,
                                                                                              'schedule': {
                                                                                                  'id': 'fullDay',
                                                                                                  'name': 'Полный день'},
                                                                                              'working_days': [],
                                                                                              'working_time_intervals': [],
                                                                                              'working_time_modes': [],
                                                                                              'accept_temporary': False,
                                                                                              'professional_roles': [
                                                                                                  {'id': '97',
                                                                                                   'name': 'Продавец-консультант, продавец-кассир'}],
                                                                                              'accept_incomplete_resumes': True,
                                                                                              'experience': {
                                                                                                  'id': 'noExperience',
                                                                                                  'name': 'Нет опыта'},
                                                                                              'employment': {
                                                                                                  'id': 'full',
                                                                                                  'name': 'Полная занятость'},
                                                                                              'adv_response_url': None,
                                                                                              'is_adv_vacancy': False,
                                                                                              'adv_context': None}}]

add_info_table(info_api, "test1", "employees")
add_info_table(info_1_vacanc, "test1", "vacancies")

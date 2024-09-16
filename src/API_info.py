import requests


def get_info_api():
    """ Функция собирает информацию по всем возможным страницам сервиса HH работодателей, отбирает с самым большим
            кол-вом вакансий и сортирует их в порядке убывания по вакансиям, выводит список id работодатлей """

    list_employee = []
    for i in range(1):  #  Для сбора данных со всех страниц - указать 100!
        params = {"page": i, "per_page": 100}
        try:
            response = requests.get("https://api.hh.ru/employers", params=params).json()["items"]

            for resp in response:
                if resp["open_vacancies"] > 50:
                    list_employee.append(resp)
        except:  # Останавливает итерацию в случае конца страниц
            break

    sort_top_employee = sorted(list_employee, key=lambda x: x["open_vacancies"], reverse=True)[:10]  # Сортируем данные

    return sort_top_employee  # Выводим ТОП-10 ссылок на вакансии


def get_info_vacancies(list_info: list) -> list:
    """ Функция принимает список работодателей и выводит список с информацией по их вакансиям """

    id_list = [vac["id"] for vac in list_info]  # Достаем отдельно id работодателей
    vacancies_list = []
    for vac in id_list:
        response = requests.get(f'https://api.hh.ru/vacancies?employer_id={vac}').json()["items"]  # Достаем инфо по id
        for i in response:  # Создаем новый список
            vacancies_list.append({"employees": vac,
                                   "vacancies": i})
    return vacancies_list


top_employees = ['2676125', '1327757', '3857386', '71895', '3643187', '2058312', '5224495', '5066511', '54794',
                 '4242730']


info_api = [{'id': '3786259', 'name': '100ДЕЛ', 'url': 'https://api.hh.ru/employers/3786259',
             'alternate_url': 'https://hh.ru/employer/3786259',
             'logo_urls': {'original': 'https://img.hhcdn.ru/employer-logo-original/1062676.png',
                           '240': 'https://img.hhcdn.ru/employer-logo/5871338.png',
                           '90': 'https://img.hhcdn.ru/employer-logo/5871337.png'},
             'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=3786259', 'open_vacancies': 69}]


# vacancies_list = []
# response = requests.get(f'https://api.hh.ru/vacancies?employer_id=3786259').json()["items"]  # Достаем инфо по id
# for i in response:  # Создаем новый список
#     vacancies_list.append(i)
# print(vacancies_list)


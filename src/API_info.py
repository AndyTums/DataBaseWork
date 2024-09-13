import requests


def get_info_api():
    """ Функция собирает информацию по всем возможным страницам сервиса HH работодателей, отбирает с самым большим
            кол-вом вакансий и сортирует их в порядке убывания по вакансиям, выводит список URL на вакансии """

    list_employee = []
    for i in range(100):
        params = {"page": i, "per_page": 100}
        try:
            response = requests.get("https://api.hh.ru/employers", params=params).json()["items"]

            for resp in response:
                if resp["open_vacancies"] > 50:
                    list_employee.append(resp)
        except:  # Останавливает итерацию в случае конца страниц
            break

    sort_top_employee = sorted(list_employee, key=lambda x: x["open_vacancies"], reverse=True)[:10]  # Сортируем данные
    top_employee = [vac["id"] for vac in sort_top_employee]
    return top_employee  # Выводим ТОП-10 ссылок на вакансии


def get_info_vacancies(list_employees: list) -> list:
    """ Функция принимает список id работодателей и выводит список с информацией по их вакансиям """

    vacancies_list = []
    for vac in list_employees:
        response = requests.get(f'https://api.hh.ru/vacancies?employer_id={vac}').json()["items"]
        for i in response:
            vacancies_list.append({"employees": vac,
                                   "vacancies": i})
    return vacancies_list


# print(get_info_api())



top_employees = ['2676125', '1327757', '3857386', '71895', '3643187', '2058312', '5224495', '5066511', '54794',
                 '4242730']
# print(get_info_vacancies(top_employees))


info_api = [{'id': '3786259', 'name': '100ДЕЛ', 'url': 'https://api.hh.ru/employers/3786259',
             'alternate_url': 'https://hh.ru/employer/3786259',
             'logo_urls': {'original': 'https://img.hhcdn.ru/employer-logo-original/1062676.png',
                           '240': 'https://img.hhcdn.ru/employer-logo/5871338.png',
                           '90': 'https://img.hhcdn.ru/employer-logo/5871337.png'},
             'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=3786259', 'open_vacancies': 69},
            {'id': '2676125', 'name': '1000 Сотрудников', 'url': 'https://api.hh.ru/employers/2676125',
             'alternate_url': 'https://hh.ru/employer/2676125',
             'logo_urls': {'original': 'https://img.hhcdn.ru/employer-logo-original/626166.jpg',
                           '240': 'https://img.hhcdn.ru/employer-logo/2945817.jpeg',
                           '90': 'https://img.hhcdn.ru/employer-logo/2945816.jpeg'},
             'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=2676125', 'open_vacancies': 40},
            {'id': '3503705', 'name': '100балльный репетитор', 'url': 'https://api.hh.ru/employers/3503705',
             'alternate_url': 'https://hh.ru/employer/3503705',
             'logo_urls': {'original': 'https://img.hhcdn.ru/employer-logo-original/1328315.png',
                           '240': 'https://img.hhcdn.ru/employer-logo/6933283.png',
                           '90': 'https://img.hhcdn.ru/employer-logo/6933282.png'},
             'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=3503705', 'open_vacancies': 34},
            {'id': '1327757', 'name': '1000 и одна туфелька', 'url': 'https://api.hh.ru/employers/1327757',
             'alternate_url': 'https://hh.ru/employer/1327757',
             'logo_urls': {'original': 'https://img.hhcdn.ru/employer-logo-original/688035.jpg',
                           '240': 'https://img.hhcdn.ru/employer-logo/3193273.jpeg',
                           '90': 'https://img.hhcdn.ru/employer-logo/3193272.jpeg'},
             'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=1327757', 'open_vacancies': 26},
            {'id': '3857386', 'name': '1000 ДЛЯ УДОБНОЙ ЖИЗНИ', 'url': 'https://api.hh.ru/employers/3857386',
             'alternate_url': 'https://hh.ru/employer/3857386',
             'logo_urls': {'original': 'https://img.hhcdn.ru/employer-logo-original/742325.png',
                           '240': 'https://img.hhcdn.ru/employer-logo/3410262.png',
                           '90': 'https://img.hhcdn.ru/employer-logo/3410261.png'},
             'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=3857386', 'open_vacancies': 14},
            {'id': '71895', 'name': '1001 Тур', 'url': 'https://api.hh.ru/employers/71895',
             'alternate_url': 'https://hh.ru/employer/71895',
             'logo_urls': {'original': 'https://img.hhcdn.ru/employer-logo-original/1183085.jpg',
                           '240': 'https://img.hhcdn.ru/employer-logo/6352767.jpeg',
                           '90': 'https://img.hhcdn.ru/employer-logo/6352766.jpeg'},
             'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=71895', 'open_vacancies': 13},
            {'id': '3643187', 'name': '001KZ (001КЗ)', 'url': 'https://api.hh.ru/employers/3643187',
             'alternate_url': 'https://hh.ru/employer/3643187',
             'logo_urls': {'original': 'https://img.hhcdn.ru/employer-logo-original/1099094.png',
                           '240': 'https://img.hhcdn.ru/employer-logo/6016990.png',
                           '90': 'https://img.hhcdn.ru/employer-logo/6016989.png'},
             'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=3643187', 'open_vacancies': 6},
            {'id': '3488257', 'name': '100-Дверей', 'url': 'https://api.hh.ru/employers/3488257',
             'alternate_url': 'https://hh.ru/employer/3488257',
             'logo_urls': {'original': 'https://img.hhcdn.ru/employer-logo-original/858281.jpg',
                           '240': 'https://img.hhcdn.ru/employer-logo/3874000.jpeg',
                           '90': 'https://img.hhcdn.ru/employer-logo/3873999.jpeg'},
             'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=3488257', 'open_vacancies': 5},
            {'id': '2058312', 'name': '0250', 'url': 'https://api.hh.ru/employers/2058312',
             'alternate_url': 'https://hh.ru/employer/2058312',
             'logo_urls': {'original': 'https://img.hhcdn.ru/employer-logo-original/1126656.png',
                           '240': 'https://img.hhcdn.ru/employer-logo/6127214.png',
                           '90': 'https://img.hhcdn.ru/employer-logo/6127213.png'},
             'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=2058312', 'open_vacancies': 4},
            {'id': '5224495', 'name': '1001 Крепеж', 'url': 'https://api.hh.ru/employers/5224495',
             'alternate_url': 'https://hh.ru/employer/5224495',
             'logo_urls': {'original': 'https://img.hhcdn.ru/employer-logo-original/827458.png',
                           '240': 'https://img.hhcdn.ru/employer-logo/3750716.png',
                           '90': 'https://img.hhcdn.ru/employer-logo/3750715.png'},
             'vacancies_url': 'https://api.hh.ru/vacancies?employer_id=5224495', 'open_vacancies': 4}]

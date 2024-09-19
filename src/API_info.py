import requests


def get_info_api():
    """ Функция собирает информацию по всем возможным страницам сервиса HH работодателей, отбирает с самым большим
            кол-вом вакансий и сортирует их в порядке убывания по вакансиям, выводит список id работодатлей """

    print("Получаем информацию по работодателям..")

    list_employee = []
    for i in range(10):  # Для сбора данных со всех страниц - указать 100!
        params = {"page": i, "per_page": 100}
        try:
            response = requests.get("https://api.hh.ru/employers", params=params).json()["items"]

            for resp in response:
                if resp["open_vacancies"] > 5:  # Ввести кол-во вакансий которое необходимо у работодателя
                    list_employee.append(resp)
        except:  # Останавливает итерацию в случае конца страниц
            break

    sort_top_employee = sorted(list_employee, key=lambda x: x["open_vacancies"], reverse=True)[:10]  # Сортируем данные

    return sort_top_employee  # Выводим ТОП-10 ссылок на вакансии


def get_info_vacancies(list_info: list) -> list:
    """ Функция принимает список работодателей и выводит список с информацией по их вакансиям """

    print("Получаем информацию по вакансиям..")

    id_list = [vac["id"] for vac in list_info]  # Достаем отдельно id работодателей
    vacancies_list = []
    for vac in id_list:
        response = requests.get(f'https://api.hh.ru/vacancies?employer_id={vac}').json()["items"]  # Достаем инфо по id
        for i in response:  # Создаем новый список
            vacancies_list.append({"employees": vac,
                                   "vacancies": i})
    return vacancies_list

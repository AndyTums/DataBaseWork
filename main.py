from src.API_info import get_info_api, get_info_vacancies
from src.DB_class import DBManager
from src.work_db import create_db, create_table, add_info_table


def main() -> None:
    print("Начинаем работу с БД...\n")

    create_db("course")  # Создаем БД
    create_table("course")  # Создаем таблицы
    info_api = get_info_api()  # Получаем данные по работодателям через API
    info_vacancies = get_info_vacancies(info_api)  # Получаем информацию по вакансиям через API
    add_info_table(info_api, "course", "employees")  # Добавляем информацию в БД таблицы EMPLOYEES
    add_info_table(info_vacancies, "course", "vacancies")  # Добавляем информацию в БД таблицы VACANCIES
    print("Информация успешна добавлена в БД и сохранена!")

    class_work_db = DBManager()
    print("""Выберите данные которые хотели бы получить:
      1. Наименование работодателя и кол-во его вакансий.
      2. Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
      3. Среднюю зарплату по вакансиям.
      4. Список всех вакансий, у которых зарплата выше средней по всем вакансиям.
      5. Список всех вакансий, в названии которых содержатся переданные в метод слова.""")
    score = 0
    while score < 3:
        try:  # В случае ввода типа не INT
            create_bd_answer = int(input("Ввод: "))  # Запрос у пользователя

            if create_bd_answer == 1:  # Обработка вопроса №1
                answer_1 = class_work_db.get_companies_and_vacancies_count()
                print("\nВот что удалось найти:\n")
                for i in answer_1:
                    print(f"Имя работодателя: {i[0]}, кол-во вакансий: {i[1]}.")
                break
            elif create_bd_answer == 2:  # Обработка вопроса №2
                answer_2 = class_work_db.get_all_vacancies()
                print("\nВот что удалось найти:\n")
                for i in answer_2:
                    print(f"Имя работодателя: {i[0]}, название вакансии: {i[1]}, заплата: {i[2]}, ссылка: {i[3]}.")
                break
            elif create_bd_answer == 3:  # Обработка вопроса №3
                answer_3 = class_work_db.get_avg_salary()
                print("\nВот что удалось найти:\n")
                for i in answer_3:
                    print(f"Средняя зарплата по вакансиям: {round(i[0])}.")
                break
            elif create_bd_answer == 4:  # Обработка вопроса №4
                answer_4 = class_work_db.get_vacancies_with_higher_salary()
                print("\nВот что удалось найти:\n")
                for i in answer_4:
                    print(f"Номер вакансии: {i[0]}, название вакансии: {i[1]}, заплата: {i[2]}, ссылка: {i[3]},"
                          f" личный номер работодателя: {i[4]}.")
                break
            elif create_bd_answer == 5:  # Обработка вопроса №5
                word = input("Введите слово для поиска: ")
                answer_5 = class_work_db.get_vacancies_with_keyword(word)
                print("\nВот что удалось найти:\n")
                for i in answer_5:
                    print(f"Номер вакансии: {i[0]}, название вакансии: {i[1]}, заплата: {i[2]}, ссылка: {i[3]},"
                          f" личный номер работодателя: {i[4]}.")
                break
            else:
                if score == 2:  # Конец работы после 3 неверных запросов
                    print("Превышен лимит запроса.")
                    return f"\nКонец работы программы"
                else:
                    print("Попробуйте еще раз")
                    score += 1
        except:
            print("Неверный выбор, попробуйте еще раз!")
            score += 1
        continue

    return f"\nКонец работы программы"


main()

from src.api import get_vacancies_by_company
from src.db_manager import DBManager
from src.utils import parse_vacancy_data, save_json


def main():
    # Запрос имени проекта
    project_name = input("Введите название проекта: ")
    print(f"Проект {project_name} запущен!")

    # ID 10 компаний с hh.ru
    companies = ["827187", "1942330", "4869287", "2751781", "3529",
                 "2495333", "4944119", "52511", "956196", "10602050"]

    all_vacancies = []
    for company in companies:
        vacancies = get_vacancies_by_company(company)
        if vacancies:
            parsed = parse_vacancy_data(vacancies)
            all_vacancies.extend(parsed)

    # Сохранение данных
    save_json(all_vacancies, f"{project_name}_vacancies.json")

    # Создание базы и подключение
    db = DBManager()

    print("\nКомпании и количество вакансий:")
    print(db.get_companies_and_vacancies_count())

    print("\nВсе вакансии:")
    print(db.get_all_vacancies())

    print("\nСредняя зарплата:")
    print(db.get_avg_salary())

    print("\nВакансии с зарплатой выше средней:")
    print(db.get_vacancies_with_higher_salary())

    keyword = input("\nВведите ключевое слово для поиска вакансий: ")
    print(f"\nВакансии с ключевым словом '{keyword}':")
    print(db.get_vacancies_with_keyword(keyword))

    db.close_connection()

if __name__ == "__main__":
    main()

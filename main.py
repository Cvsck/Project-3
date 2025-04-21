from src.api import get_vacancies_by_company
from src.db_manager import DBManager
from src.utils import parse_vacancy_data, save_json


def main():
    # Ввод названия проекта
    project_name = input("Введите название проекта: ")
    print(f"Проект {project_name} запущен!")

    # ID компаний с hh.ru
    companies = ["827187", "1942330", "4869287", "2751781", "3529",
                 "2495333", "4944119", "52511", "956196", "10602050"]

    all_vacancies = []

    # Подключение к БД
    db = DBManager()

    for company in companies:
        vacancies = get_vacancies_by_company(company)
        if vacancies:
            parsed_vacancies = parse_vacancy_data(vacancies)
            all_vacancies.extend(parsed_vacancies)

            # Добавление компании в БД
            db.cursor.execute("INSERT INTO companies (company_name) VALUES (%s) ON CONFLICT DO NOTHING RETURNING id;",
                              (company,))
            company_id = db.cursor.fetchone()
            company_id = company_id[0] if company_id else None

            # Добавление вакансий в БД
            for vacancy in parsed_vacancies:
                db.cursor.execute("""
                    INSERT INTO vacancies (title, salary, url, company_id) 
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, (vacancy["name"], vacancy["salary"], vacancy["url"], company_id))

    db.conn.commit()  # Сохранение изменений

    # Сохранение данных в JSON
    save_json(all_vacancies, f"{project_name}_vacancies.json")

    db.close_connection()
    print("Данные успешно записаны в БД и сохранены в JSON!")


if __name__ == "__main__":
    main()

from src.api import get_vacancies_by_company
from src.db_manager import DBManager
from src.utils import parse_vacancy_data, save_json


def main():
    """Основной процесс сбора данных и сохранения в БД."""
    project_name = input("Введите название проекта: ")
    print(f"🚀 Проект {project_name} запущен!")

    # ✅ Создаём БД перед подключением
    DBManager.create_database()

    # ID компаний с hh.ru
    company_ids = ["827187", "1942330", "4869287", "2751781", "3529",
                   "2495333", "4944119", "52511", "956196", "10602050"]

    all_vacancies = []

    # ✅ Подключение к БД и создание таблиц
    db = DBManager()
    db.create_tables()

    for company_id in company_ids:
        vacancies = get_vacancies_by_company(company_id)
        if vacancies:
            parsed_vacancies = parse_vacancy_data(vacancies)
            all_vacancies.extend(parsed_vacancies)

            # ✅ Проверяем, есть ли компания в БД
            db.cursor.execute("SELECT id FROM companies WHERE company_name = %s;", (company_id,))
            company_row = db.cursor.fetchone()

            # ✅ Если компании нет, добавляем её
            if not company_row:
                db.cursor.execute("""
                    INSERT INTO companies (company_name) VALUES (%s)
                    ON CONFLICT (company_name) DO NOTHING RETURNING id;
                """, (company_id,))
                company_row = db.cursor.fetchone()

            company_db_id = company_row[0] if company_row else None

            for vacancy in parsed_vacancies:
                salary_value = vacancy["salary"] if vacancy["salary"] is not None else 0
                if company_db_id:
                    db.cursor.execute("""
                        INSERT INTO vacancies (title, salary, url, company_id) 
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT DO NOTHING;
                    """, (vacancy["name"], salary_value, vacancy["url"], company_db_id))

    db.conn.commit()
    save_json(all_vacancies, f"{project_name}_vacancies.json")

    # ✅ Вызовы методов для получения данных из БД
    print("\n📊 Статистика по вакансиям:\n")

    print("🔹 Средняя зарплата по всем вакансиям:")
    print(db.get_avg_salary())

    print("\n🔹 Компании и количество их вакансий:")
    for company, count in db.get_companies_and_vacancies_count():
        print(f"{company}: {count} вакансий")

    print("\n🔹 Вакансии с зарплатой выше средней:")
    for vacancy in db.get_vacancies_with_higher_salary():
        print(vacancy)

    db.close_connection()
    print("✅ Данные записаны в БД, сохранены в JSON и статистика выведена!")


if __name__ == "__main__":
    main()

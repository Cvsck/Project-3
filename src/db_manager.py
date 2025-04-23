import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DBManager:
    def __init__(self):
        """Инициализация подключения к PostgreSQL."""
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        self.conn.set_client_encoding("UTF8")
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Удаляет старые таблицы и создаёт новые."""
        self.cursor.execute("DROP TABLE IF EXISTS vacancies CASCADE;")
        self.cursor.execute("DROP TABLE IF EXISTS companies CASCADE;")

        self.cursor.execute("""
            CREATE TABLE companies (
                id SERIAL PRIMARY KEY,
                company_name TEXT NOT NULL UNIQUE
            );
        """)

        self.cursor.execute("""
            CREATE TABLE vacancies (
                id SERIAL PRIMARY KEY,
                title TEXT NOT NULL,
                salary INTEGER,
                url TEXT,
                company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE
            );
        """)

        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой."""
        self.cursor.execute(
            """
            SELECT c.company_name, COUNT(v.id)
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.company_name
            ORDER BY COUNT(v.id) DESC;
        """
        )
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий, исключая NULL в salary и company_id."""
        self.cursor.execute(
            """
            SELECT c.company_name, v.title, v.salary, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE v.salary IS NOT NULL AND v.company_id IS NOT NULL
            ORDER BY v.salary DESC;
        """
        )
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату."""
        self.cursor.execute(
            """
            SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL;
        """
        )
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Получает вакансии с зарплатой выше средней."""
        avg_salary = self.get_avg_salary()
        self.cursor.execute(
            """
            SELECT c.company_name, v.title, v.salary, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE v.salary > %s
            ORDER BY v.salary DESC;
        """,
            (avg_salary,),
        )
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Поиск вакансий по ключевому слову."""
        self.cursor.execute(
            """
            SELECT c.company_name, v.title, v.salary, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE LOWER(v.title) LIKE %s
            ORDER BY v.salary DESC NULLS LAST;
        """,
            ("%" + keyword.lower() + "%",),
        )
        return self.cursor.fetchall()

    def close_connection(self):
        """Закрывает соединение с БД."""
        self.cursor.close()
        self.conn.close()

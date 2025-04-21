import psycopg2
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
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
            client_encoding="UTF8"
        )
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой."""
        self.cursor.execute("""
            SELECT c.company_name, COUNT(v.id)
            FROM companies c
            LEFT JOIN vacancies v ON c.id = v.company_id
            GROUP BY c.company_name
            ORDER BY COUNT(v.id) DESC;
        """)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием компании, названия вакансии, зарплаты и ссылки."""
        self.cursor.execute("""
            SELECT c.company_name, v.title, v.salary, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            ORDER BY v.salary DESC NULLS LAST;
        """)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по всем вакансиям."""
        self.cursor.execute("""
            SELECT AVG(salary)
            FROM vacancies
            WHERE salary IS NOT NULL;
        """)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Получает список вакансий с зарплатой выше средней."""
        avg_salary = self.get_avg_salary()
        self.cursor.execute("""
            SELECT c.company_name, v.title, v.salary, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE v.salary > %s
            ORDER BY v.salary DESC;
        """, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список вакансий, содержащих переданное слово."""
        self.cursor.execute("""
            SELECT c.company_name, v.title, v.salary, v.url
            FROM vacancies v
            JOIN companies c ON v.company_id = c.id
            WHERE LOWER(v.title) LIKE %s
            ORDER BY v.salary DESC NULLS LAST;
        """, ('%' + keyword.lower() + '%',))
        return self.cursor.fetchall()

    def close_connection(self):
        """Закрывает соединение с БД."""
        self.cursor.close()
        self.conn.close()

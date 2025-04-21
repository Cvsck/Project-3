import psycopg2
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class DBManager:
    def __init__(self):
        """Инициализация подключения и создание таблиц."""
        self.conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        self.create_database()
        self.create_tables()

    def create_database(self):
        """Удаляет существующую БД и создает новую."""
        self.cursor.execute(f"DROP DATABASE IF EXISTS {os.getenv('DB_NAME')}")
        self.cursor.execute(f"CREATE DATABASE {os.getenv('DB_NAME')}")

    def create_tables(self):
        """Создает таблицы организаций и вакансий с FK."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            company_name TEXT NOT NULL
        );
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
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
        query = """
        SELECT company_name, COUNT(*) 
        FROM vacancies 
        GROUP BY company_name;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        """Получает список всех вакансий с названием компании, вакансии, зарплатой и ссылкой."""
        query = """
        SELECT v.title, c.company_name, v.salary, v.url 
        FROM vacancies v
        JOIN companies c ON v.company_id = c.id;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        query = "SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL;"
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Получает список вакансий, зарплата которых выше средней."""
        avg_salary = self.get_avg_salary()
        query = """
        SELECT v.title, c.company_name, v.salary, v.url 
        FROM vacancies v
        JOIN companies c ON v.company_id = c.id
        WHERE v.salary > %s;
        """
        self.cursor.execute(query, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список вакансий, содержащих указанное слово."""
        query = """
        SELECT v.title, c.company_name, v.salary, v.url 
        FROM vacancies v
        JOIN companies c ON v.company_id = c.id
        WHERE v.title ILIKE %s;
        """
        self.cursor.execute(query, ('%' + keyword + '%',))
        return self.cursor.fetchall()

    def close_connection(self):
        """Закрывает соединение с БД."""
        self.cursor.close()
        self.conn.close()

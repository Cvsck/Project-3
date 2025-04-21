# Project-3
"""
Реализован проект позволяющий пользователю 
получить данные о работодателях и их вакансиях с сайта hh.ru.
Можно выбрать не менее 10 интересных вам компаний, от которых вы 
будете получать данные о вакансиях по API.
Будут спроектированы таблицы в БД PostgreSQL для 
хранения полученных данных о работодателях и их вакансиях.
"""
# Создан класс 
"""
DBManager
для работы с данными в БД
"""

# Установлены необходимые зависимости для проекта
"""
python -m venv my_env  # Создание виртуальной среды
my_env\Scripts\Activate.ps1  # Активация среды
pip install poetry
poetry init
python.exe -m pip install --upgrade pip
pip install isort black flake8 pep8
python.exe -m pip install --upgrade pip
pip install requests
pip install mypy
"""
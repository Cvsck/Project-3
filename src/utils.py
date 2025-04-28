import json
import os

# Папка для JSON-файлов
DATA_DIR = "C:\\Users\\Макс\\my_prj\\Project-3\\data"
os.makedirs(DATA_DIR, exist_ok=True)


def save_json(data: list[dict], filename: str):
    """Сохраняет JSON в 'data'."""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Файл сохранен: {filepath}")


def parse_vacancy_data(vacancies: dict) -> list[dict]:
    """Извлекает важные данные из ответа API."""
    return [
        {"name": v["name"], "salary": v["salary"]["from"] if v["salary"] else None, "url": v["alternate_url"]}
        for v in vacancies["items"]
    ]

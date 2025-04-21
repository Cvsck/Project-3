import json

def save_json(data, filename):
    """Сохраняет данные в JSON-файл."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def parse_vacancy_data(vacancies):
    """Извлекает важные данные из ответа API."""
    return [{
        "name": v["name"],
        "salary": v["salary"]["from"] if v["salary"] else None,
        "url": v["alternate_url"]
    } for v in vacancies["items"]]

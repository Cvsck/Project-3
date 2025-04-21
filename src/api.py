import requests

BASE_URL = "https://api.hh.ru/vacancies"

def get_vacancies_by_company(employer_id):
    """Получает список вакансий компании по её ID."""
    params = {"employer_id": employer_id, "per_page": 100, "area": 113}  # Россия
    response = requests.get(BASE_URL, params=params)
    return response.json() if response.status_code == 200 else None

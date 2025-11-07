# services/job_api.py
import requests
import traceback

def get_vacancies(query: str, salary: int = 0, per_page: int = 5):
    """
    Возвращает list вакансий в виде словарей:
    { "title", "location", "url", "salary", "experience" }
    """
    url = "https://api.hh.ru/vacancies"
    params = {
        "text": query,
        "area": 40,         # Казахстан
        "per_page": per_page,
        "salary": salary
    }

    try:
        print(f"[job_api] Query: {query!r} params: {params}")
        resp = requests.get(url, params=params, timeout=10)
        print(f"[job_api] HTTP {resp.status_code}")
        if resp.status_code != 200:
            return []

        data = resp.json()
        result = []
        for item in data.get("items", []):
            # salary
            s = item.get("salary")
            if s:
                if s.get("from") and s.get("to"):
                    salary_text = f"{s['from']}–{s['to']} {s.get('currency','')}".strip()
                elif s.get("from"):
                    salary_text = f"от {s['from']} {s.get('currency','')}".strip()
                elif s.get("to"):
                    salary_text = f"до {s['to']} {s.get('currency','')}".strip()
                else:
                    salary_text = "Не указана"
            else:
                salary_text = None  # None чтобы фильтр only_with_salary работал

            experience = item.get("experience", {}).get("name") if item.get("experience") else None

            result.append({
                "title": item.get("name"),
                "location": item.get("area", {}).get("name"),
                "url": item.get("alternate_url"),
                "salary": salary_text,
                "experience": experience
            })
        print(f"[job_api] Found {len(result)} items")
        return result

    except Exception as e:
        print("[job_api] Exception:", e)
        traceback.print_exc()
        return []


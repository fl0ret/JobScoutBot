# database/db.py



user_settings = {}  # { user_id: {city: str, salary: int, employment: str, experience: str, only_with_salary: bool} }

favorites = {}  # { user_id: [ {title, url, salary, location, experience} ] }


def get_user_settings(user_id: int):
    """Возвращает настройки пользователя (или пустые по умолчанию)."""
    return user_settings.get(user_id, {
        "city": None,
        "salary": None,
        "employment": None,
        "experience": None,
        "only_with_salary": False,
    })


def save_user_settings(user_id: int, settings: dict):
    """Сохраняет пользовательские настройки."""
    user_settings[user_id] = settings


def clear_user_settings(user_id: int):
    """Удаляет настройки пользователя."""
    if user_id in user_settings:
        del user_settings[user_id]


def add_favorite(user_id: int, vacancy: dict):
    """Добавляет вакансию в избранное."""
    if user_id not in favorites:
        favorites[user_id] = []
    favorites[user_id].append(vacancy)


def get_favorites(user_id: int):
    """Возвращает список избранных вакансий."""
    return favorites.get(user_id, [])


def clear_favorites(user_id: int):
    """Очищает список избранного."""
    favorites[user_id] = []

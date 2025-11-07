from aiogram import Router, types, F
from aiogram.filters import Command
import json
import os
from keyboards.main_menu_kb import main_menu_kb


router = Router()
FAV_FILE = "favorites.json"

def load_favorites():
    if os.path.exists(FAV_FILE):
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_favorites(data):
    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@router.message(Command("favorites"))
@router.message(F.text == "⭐ Избранное")
async def show_favorites(message: types.Message):
    user_id = str(message.from_user.id)
    favorites = load_favorites().get(user_id, [])

    if not favorites:
        await message.answer("⭐ У вас пока нет сохранённых вакансий.", reply_markup=main_menu_kb())
        return

    for job in favorites[-10:]:
        text = (
            f"💼 <b>{job['name']}</b>\n"
            f"🏢 {job['employer']}\n"
            f"📍 {job['city']}\n"
            f"💰 {job['salary']}\n"
            f"🔗 <a href='{job['url']}'>Смотреть на HH</a>"
        )
        await message.answer(text, parse_mode="HTML", reply_markup=main_menu_kb())

@router.callback_query(F.data.startswith("save_favorite:"))
async def save_favorite_callback(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)
    job_json = callback.data.split("save_favorite:")[1]

    try:
        job = json.loads(job_json)
    except Exception:
        await callback.answer("Ошибка сохранения 😔", show_alert=True)
        return

    favorites = load_favorites()
    favorites.setdefault(user_id, [])

    if job not in favorites[user_id]:
        favorites[user_id].append(job)
        save_favorites(favorites)
        await callback.answer("✅ Добавлено в избранное")
    else:
        await callback.answer("⭐ Уже в избранном")

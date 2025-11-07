import json
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from keyboards.vacancy_kb import vacancy_kb
from keyboards.main_menu_kb import main_menu_kb

router = Router()
FAV_FILE = "database/favorites.json"

# --- Добавление вакансии в избранное ---
@router.callback_query(lambda c: c.data.startswith("save_favorite"))
async def save_favorite(call: types.CallbackQuery, state: FSMContext):
    user_id = str(call.from_user.id)
    vacancy_id = call.data.split(":")[-1]  # формат callback_data: save_favorite:<id>

    data = await state.get_data()
    vacancies = data.get("vacancies", [])

    vacancy = next((v for v in vacancies if v["id"] == vacancy_id), None)
    if not vacancy:
        await call.answer("❌ Не удалось добавить в избранное.", show_alert=True)
        return

    # загружаем текущие избранные
    try:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            all_favorites = json.load(f)
    except FileNotFoundError:
        all_favorites = {}

    user_favs = all_favorites.get(user_id, [])
    # проверяем, есть ли уже
    if any(v["id"] == vacancy_id for v in user_favs):
        await call.answer("⚠ Вакансия уже в избранном.", show_alert=True)
        return

    user_favs.append(vacancy)
    all_favorites[user_id] = user_favs

    with open(FAV_FILE, "w", encoding="utf-8") as f:
        json.dump(all_favorites, f, ensure_ascii=False, indent=4)

    await call.answer("✅ Вакансия добавлена в избранное.", show_alert=True)

# --- Показ избранного ---
async def show_favorites_menu(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)

    try:
        with open(FAV_FILE, "r", encoding="utf-8") as f:
            all_favorites = json.load(f)
    except FileNotFoundError:
        all_favorites = {}

    user_favs = all_favorites.get(user_id, [])

    if not user_favs:
        await message.answer("⭐ У вас пока нет избранных вакансий.", reply_markup=main_menu_kb)
        return

    for v in user_favs:
        text = (
            f"💼 <b>{v['title']}</b>\n"
            f"🏙 Город: {v['location']}\n"
            f"💰 Зарплата: {v.get('salary', 'Не указана')}\n"
            f"🕒 Опыт: {v.get('experience', 'Не указан')}\n"
        )
        await message.answer(text, reply_markup=vacancy_kb(v["id"], v["url"]), parse_mode="HTML")

    await message.answer("🔙 Главное меню", reply_markup=main_menu_kb)

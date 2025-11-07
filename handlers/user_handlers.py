from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states.job_filters import JobFilter
from services.job_api import get_vacancies
from services.settings_storage import load_settings
from keyboards.filters_kb import employment_kb
from keyboards.main_menu_kb import main_menu_kb
from keyboards.experience_kb import experience_kb
from keyboards.vacancy_kb import vacancy_kb
from handlers.favorites_handler import show_favorites_menu

router = Router()

# ---------- /start ----------
@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "👋 Привет! Я бот по поиску работы в Казахстане.\n\n"
        "Выбери действие ниже 👇",
        reply_markup=main_menu_kb
    )

# ---------- Универсальный обработчик главного меню ----------
@router.message(lambda m: m.text in ["🔍 Найти работу", "⭐ Избранное", "⚙️ Настройки", "ℹ️ Помощь"])
async def handle_main_menu(message: types.Message, state: FSMContext):
    await state.clear()  # сбрасываем текущее состояние

    if message.text == "🔍 Найти работу":
        await start_filtering(message, state)

    elif message.text == "⭐ Избранное":
        await show_favorites_menu(message, state)  # вот исправлено

    elif message.text == "⚙️ Настройки":
        from handlers.settings_handler import show_settings_menu
        await show_settings_menu(message, state)

    elif message.text == "ℹ️ Помощь":
        await cmd_help(message)

# ---------- /find ----------
@router.message(Command("find"))
async def start_filtering(message: types.Message, state: FSMContext):
    await message.answer("📍 Введи название города в Казахстане:", reply_markup=main_menu_kb)
    await state.set_state(JobFilter.city)

# ---------- /help ----------
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "ℹ️ <b>Помощь по боту</b>\n\n"
        "1️⃣ Нажми '🔍 Найти работу' — я помогу подобрать вакансии.\n"
        "2️⃣ Введи город, минимальную зарплату и специальность.\n"
        "3️⃣ Получи актуальные вакансии из hh.kz\n\n"
        "Если нужно изменить параметры — открой ⚙️ Настройки.",
        parse_mode="HTML",
        reply_markup=main_menu_kb
    )

# ---------- Ввод города ----------
@router.message(JobFilter.city)
async def enter_city(message: types.Message, state: FSMContext):
    if message.text in ["⭐ Избранное", "⚙️ Настройки", "ℹ️ Помощь", "🔍 Найти работу"]:
        await handle_main_menu(message, state)
        return

    city = message.text.strip()
    valid_cities = [
        "Алматы", "Астана", "Шымкент", "Караганда", "Тараз", "Павлодар",
        "Усть-Каменогорск", "Семей", "Актау", "Актобе", "Костанай",
        "Кызылорда", "Талдыкорган", "Петропавловск", "Уральск", "Кокшетау"
    ]

    if city not in valid_cities:
        await message.answer("❌ Такой город не найден. Попробуй ещё раз.", reply_markup=main_menu_kb)
        return

    await state.update_data(city=city)
    await message.answer("💰 Укажи минимальную зарплату (в тенге):", reply_markup=main_menu_kb)
    await state.set_state(JobFilter.salary)

# ---------- Ввод зарплаты ----------
@router.message(JobFilter.salary)
async def enter_salary(message: types.Message, state: FSMContext):
    if message.text in ["⭐ Избранное", "⚙️ Настройки", "ℹ️ Помощь", "🔍 Найти работу"]:
        await handle_main_menu(message, state)
        return

    if not message.text.isdigit():
        await message.answer("Введите число.", reply_markup=main_menu_kb)
        return

    await state.update_data(salary=int(message.text))
    await message.answer("💼 Выбери тип занятости:", reply_markup=employment_kb)
    await state.set_state(JobFilter.employment)

# ---------- Ввод типа занятости ----------
@router.message(JobFilter.employment)
async def enter_employment(message: types.Message, state: FSMContext):
    if message.text in ["⭐ Избранное", "⚙️ Настройки", "ℹ️ Помощь", "🔍 Найти работу"]:
        await handle_main_menu(message, state)
        return

    await state.update_data(employment=message.text)
    await message.answer("🧑‍💻 Введи специальность (например, Разработчик, Дизайнер и т.д.):", reply_markup=main_menu_kb)
    await state.set_state(JobFilter.specialty)

# ---------- Ввод специальности ----------
@router.message(JobFilter.specialty)
async def enter_specialty(message: types.Message, state: FSMContext):
    if message.text in ["⭐ Избранное", "⚙️ Настройки", "ℹ️ Помощь", "🔍 Найти работу"]:
        await handle_main_menu(message, state)
        return

    specialty = message.text.strip()
    await state.update_data(specialty=specialty)
    await message.answer("💼 Укажи уровень опыта:", reply_markup=experience_kb)
    await state.set_state(JobFilter.experience)

# ---------- Ввод опыта и поиск ----------
@router.message(JobFilter.experience)
async def enter_experience(message: types.Message, state: FSMContext):
    if message.text in ["⭐ Избранное", "⚙️ Настройки", "ℹ️ Помощь", "🔍 Найти работу"]:
        await handle_main_menu(message, state)
        return

    experience = message.text.strip()
    await state.update_data(experience=experience)

    data = await state.get_data()
    await state.clear()

    user_id = str(message.from_user.id)
    settings = load_settings().get(user_id, {})

    city = settings.get("city", data.get("city"))
    salary = settings.get("salary", data.get("salary"))
    employment = settings.get("employment", data.get("employment"))
    specialty = data["specialty"]
    experience = settings.get("experience", data.get("experience"))
    vacancies_per_page = settings.get("vacancies_per_page", 5)
    only_with_salary = settings.get("only_with_salary", False)

    await message.answer("🔎 Ищу вакансии...", reply_markup=main_menu_kb)

    query = f"{specialty} {employment} {city} {experience}"
    vacancies = get_vacancies(query, salary)

    for i, v in enumerate(vacancies):
        v["id"] = str(i)

    if only_with_salary:
        vacancies = [v for v in vacancies if v.get("salary")]

    vacancies = vacancies[:vacancies_per_page]

    if not vacancies:
        await message.answer("❌ Вакансий не найдено.", reply_markup=main_menu_kb)
        return

    # сохраняем вакансии в state для избранного
    await state.update_data(vacancies=vacancies, index=0)

    for v in vacancies:
        text = (
            f"💼 <b>{v['title']}</b>\n"
            f"🏙 Город: {v['location']}\n"
            f"💰 Зарплата: {v.get('salary', 'Не указана')}\n"
            f"🕒 Опыт: {v.get('experience', 'Не указан')}\n"
        )
        await message.answer(text, reply_markup=vacancy_kb(v["id"], v["url"]), parse_mode="HTML")

    await message.answer("🔙 Главное меню", reply_markup=main_menu_kb)

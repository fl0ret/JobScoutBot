from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types
from keyboards.main_menu_kb import main_menu_kb

router = Router()


class SettingsState(StatesGroup):
    city = State()
    salary = State()
    employment = State()
    experience = State()
    limit = State()


# --- Клавиатура меню настроек ---
settings_kb = ReplyKeyboardMarkup(
    keyboard=[
        # фильтры
        [
            KeyboardButton(text="🏙 Город по умолчанию"),
            KeyboardButton(text="💰 Минимальная зарплата")
        ],
        [
            KeyboardButton(text="💼 Тип занятости"),
            KeyboardButton(text="🧑‍💻 Опыт работы")
        ],
        # отображение вакансий
        [
            KeyboardButton(text="📊 Количество вакансий"),
            KeyboardButton(text="📉 Только с зарплатой")
        ],
        # действия
        [
            KeyboardButton(text="🔄 Сбросить настройки"),
            KeyboardButton(text="⬅ Назад в меню")
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Выберите, что хотите изменить ⚙️"
)


# --- Открытие раздела настроек ---
@router.message(Command("settings"))
@router.message(lambda m: m.text == "⚙ Настройки")
async def open_settings(message: types.Message):
    await message.answer("⚙ Выберите параметр для изменения:", reply_markup=settings_kb)

async def show_settings_menu(message: types.Message, state: FSMContext):
    await state.clear()
    from keyboards.settings_kb import settings_kb
    await message.answer("⚙ Выберите параметр для изменения:", reply_markup=settings_kb)


# --- Настройка города ---
@router.message(lambda m: m.text == "🏙 Город по умолчанию")
async def set_default_city(message: types.Message, state: FSMContext):
    await message.answer("✏ Введите город по умолчанию:")
    await state.set_state(SettingsState.city)


@router.message(SettingsState.city)
async def save_city(message: types.Message, state: FSMContext):
    city = message.text.strip()
    await state.update_data(city=city)
    await state.clear()
    await message.answer(f"✅ Город по умолчанию сохранён: {city}", reply_markup=settings_kb)


# --- Минимальная зарплата ---
@router.message(lambda m: m.text == "💰 Минимальная зарплата")
async def set_default_salary(message: types.Message, state: FSMContext):
    await message.answer("✏ Введите минимальную зарплату в тенге:")
    await state.set_state(SettingsState.salary)


@router.message(SettingsState.salary)
async def save_salary(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Введите число.")
        return
    salary = int(message.text)
    await state.update_data(salary=salary)
    await state.clear()
    await message.answer(f"✅ Минимальная зарплата сохранена: {salary} ₸", reply_markup=settings_kb)


# --- Тип занятости ---
@router.message(lambda m: m.text == "💼 Тип занятости")
async def set_default_employment(message: types.Message, state: FSMContext):
    await message.answer("✏ Введите тип занятости (Полная / Частичная / Удалённая):")
    await state.set_state(SettingsState.employment)


@router.message(SettingsState.employment)
async def save_employment(message: types.Message, state: FSMContext):
    employment = message.text.strip()
    await state.update_data(employment=employment)
    await state.clear()
    await message.answer(f"✅ Тип занятости сохранён: {employment}", reply_markup=settings_kb)


# --- Опыт работы ---
@router.message(lambda m: m.text == "🧑‍💻 Опыт работы")
async def set_default_experience(message: types.Message, state: FSMContext):
    await message.answer("✏ Введите опыт (Без опыта / 1–3 года / 3–6 лет):")
    await state.set_state(SettingsState.experience)


@router.message(SettingsState.experience)
async def save_experience(message: types.Message, state: FSMContext):
    exp = message.text.strip()
    await state.update_data(experience=exp)
    await state.clear()
    await message.answer(f"✅ Опыт сохранён: {exp}", reply_markup=settings_kb)


# --- Количество вакансий за раз ---
@router.message(lambda m: m.text == "5 / 10 / 20 вакансий за раз")
async def set_vacancy_limit(message: types.Message, state: FSMContext):
    await message.answer("✏ Введите, сколько вакансий показывать (5 / 10 / 20):")
    await state.set_state(SettingsState.limit)


@router.message(SettingsState.limit)
async def save_limit(message: types.Message, state: FSMContext):
    if message.text not in ["5", "10", "20"]:
        await message.answer("❌ Введите одно из чисел: 5, 10 или 20.")
        return
    limit = int(message.text)
    await state.update_data(limit=limit)
    await state.clear()
    await message.answer(f"✅ Будет показываться {limit} вакансий за раз.", reply_markup=settings_kb)


# --- Только с зарплатой ---
@router.message(lambda m: m.text == "📉 Только с зарплатой")
async def toggle_salary_only(message: types.Message):
    await message.answer("✅ Фильтр 'только с зарплатой' включён.", reply_markup=settings_kb)


# --- Сброс всех настроек ---
@router.message(lambda m: m.text == "🔄 Сбросить все настройки")
async def reset_settings(message: types.Message):
    await message.answer("♻ Все настройки сброшены до стандартных.", reply_markup=settings_kb)


# --- Назад в главное меню ---
@router.message(lambda m: m.text == "⬅ Назад в меню")
async def back_to_menu(message: types.Message):
    await message.answer("🔙 Возврат в главное меню.", reply_markup=main_menu_kb)





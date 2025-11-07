from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

settings_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Город"), KeyboardButton(text="Зарплата")],
        [KeyboardButton(text="Тип занятости"), KeyboardButton(text="Опыт")],
        [KeyboardButton(text="Кол-во вакансий на страницу"), KeyboardButton(text="Только с зарплатой")],
        [KeyboardButton(text="Сбросить все настройки"), KeyboardButton(text="⬅ Назад в меню")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False
)

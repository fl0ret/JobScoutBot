from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

employment_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Полная занятость")],
        [KeyboardButton(text="Частичная занятость")],
        [KeyboardButton(text="Удалённая работа")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)


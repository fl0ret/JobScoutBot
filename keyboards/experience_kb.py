from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

experience_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Без опыта")],
        [KeyboardButton(text="От 1 до 3 лет")],
        [KeyboardButton(text="От 3 до 6 лет")],
        [KeyboardButton(text="Более 6 лет")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

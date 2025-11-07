from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def vacancy_kb(url: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Подробнее", url=url)],
            [InlineKeyboardButton(text="💾 Сохранить", callback_data="save_favorite")],
            [InlineKeyboardButton(text="⏭ Следующая", callback_data="next_vacancy")]
        ]
    )
    return keyboard


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def vacancy_kb(vacancy_id: str, url: str):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔗 Подробнее", url=url)],
            [InlineKeyboardButton(text="⭐ В избранное", callback_data=f"save_favorite:{vacancy_id}")]
        ]
    )
    return keyboard

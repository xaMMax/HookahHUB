from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.callback_data import strength_callback

strength_menu = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Легкий",
            callback_data=strength_callback.new(grade="Легкий")
        )
    ],
    [
        InlineKeyboardButton(
            text="Середній",
            callback_data=strength_callback.new(grade="Середній")
        )
    ],
    [
        InlineKeyboardButton(
            text="Міцний",
            callback_data=strength_callback.new(grade="Міцний")
        )
    ]
])

taste_menu = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Свіжий",
            callback_data=strength_callback.new(grade="Свіжий")
        ),
        InlineKeyboardButton(
            text="Солодкий",
            callback_data=strength_callback.new(grade="Солодкий")
        ),
        InlineKeyboardButton(
            text="Пряний",
            callback_data=strength_callback.new(grade="Пряний")
        )
    ],
    [
        InlineKeyboardButton(
            text="Фруктовий",
            callback_data=strength_callback.new(grade="Фруктовий")
        ),
        InlineKeyboardButton(
            text="Цитрус",
            callback_data=strength_callback.new(grade="Цитрус")
        ),
        InlineKeyboardButton(
            text="Свій варіант",
            callback_data=strength_callback.new(grade="Свій варіант")
        )
    ],
    [
        InlineKeyboardButton(
            text="Назад",
            callback_data=strength_callback.new(grade="Назад")
        ),
        InlineKeyboardButton(
            text="Закінчити замовлення",
            callback_data=strength_callback.new(grade="Закінчити замовлення")
        )
    ]
])


order_end = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Закінчити замовлення",
            callback_data=strength_callback.new(grade="Закінчити замовлення"))
    ]
])

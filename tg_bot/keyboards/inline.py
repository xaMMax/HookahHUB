from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from tg_bot.keyboards.callback_data import strength_callback

strength_menu = InlineKeyboardMarkup(row_width=3, inline_keyboard=[[
        InlineKeyboardButton(text="Легкий", callback_data=strength_callback.new(data="Легкий"))], [
        InlineKeyboardButton(text="Середній", callback_data=strength_callback.new(data="Середній"))], [
        InlineKeyboardButton(text="Міцний", callback_data=strength_callback.new(data="Міцний"))
                                    ]])
taste_list: list = ["Свіжий", "Солодкий", "Пряний", "Фруктовий", "Цитрус", "Медовий"]

taste_menu = InlineKeyboardMarkup(row_width=2, inline_keyboard=[[
        InlineKeyboardButton(text="Свіжий", callback_data=strength_callback.new(data="Свіжий")),
        InlineKeyboardButton(text="Солодкий", callback_data=strength_callback.new(data="Солодкий")),], [
        InlineKeyboardButton(text="Пряний", callback_data=strength_callback.new(data="Пряний")),
        InlineKeyboardButton(text="Фруктовий", callback_data=strength_callback.new(data="Фруктовий")),], [
        InlineKeyboardButton(text="Цитрус", callback_data=strength_callback.new(data="Цитрус")),
        InlineKeyboardButton(text="Медовий", callback_data=strength_callback.new(data="Медовий"))],
    [
        InlineKeyboardButton(
            text="Назад",
            callback_data=strength_callback.new(data="Назад")
        ),
        InlineKeyboardButton(
            text="Закінчити замовлення",
            callback_data=strength_callback.new(data="Закінчити замовлення")
        )
    ]
])


order_end = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Закінчити замовлення",
            callback_data=strength_callback.new(data="Закінчити замовлення"))
    ]
])

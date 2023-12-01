from aiogram import types, Dispatcher

from tg_bot.keyboards.callback_data import strength_callback
from tg_bot.keyboards.inline import strength_menu, taste_menu


async def admin_start(message: types.Message):
    await message.reply(f'Hello {message.from_user.full_name} you\'re admin\n'
                        f'Choose the smoke strength', reply_markup=strength_menu)
    await message.delete()


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, commands=["start"], is_admin=True)


async def menu_callback(call: types.CallbackQuery):
    choice = call.data[7:]
    await call.message.answer(f"Ви вибрали {choice} димок\n"
                              "а тепер можете вибрати смак\n"
                              "<i>в кожному меню можна вибрати один смак,\n"
                              " загалом це може бути три комбінації</i>", reply_markup=taste_menu)
    await call.message.delete()


def register_menu_callback_admin(dp: Dispatcher):
    dp.register_callback_query_handler(menu_callback,
                                       strength_callback.filter(data="Легкий"),
                                       state=None, is_admin=True)
    dp.register_callback_query_handler(menu_callback,
                                       strength_callback.filter(data="Середній"),
                                       state=None, is_admin=True)
    dp.register_callback_query_handler(menu_callback,
                                       strength_callback.filter(data="Міцний"),
                                       state=None, is_admin=True)


async def taste_menu_callback(call: types.CallbackQuery):
    choice = call.data[7:]
    await call.message.answer(f"Ваш вибір №1 це {choice}, тепер можете вибрати наступний смак,\n"
                              f" повернутись назад, або закінчити замовлення", reply_markup=taste_menu)


def register_taste_menu_callback_admin(dp: Dispatcher):
    dp.register_callback_query_handler(taste_menu_callback,
                                       strength_callback.filter(data="fresh"),
                                       state=None, is_admin=True)

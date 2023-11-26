import json, os
import aiofiles
from datetime import datetime

from aiogram import types, Dispatcher
import asyncio

from tg_bot.keyboards.callback_data import strength_callback
from tg_bot.keyboards.inline import strength_menu, taste_menu, order_end
from tg_bot.models.database_model import Database

db = Database()

async def start_user(message: types.Message):
    user_full_name = message.from_user.full_name

    time_now = datetime.now().time()
    time_now = str(time_now).replace(":", "_")[:8]

    user_id = str(message.from_user.id)
    user_id_to_short = str(user_id)
    order_name = str(user_id_to_short[6:] + "_" + time_now)

    await message.reply(
        text=f"Привіт {user_full_name} Ви знаходитесь в нашому Хабі\n"
             "завдяки мені Ви зможете легко та швидко зробити замовлення"
             " давайте ж розпочнемо з міцності кал\'ьяну",
        reply_markup=strength_menu
    )
    # Create user order
    order = {}
    order[user_id] = {"user_full_name": user_full_name}
    # print(order)

    #Delete exists filkenames
    try:
        os.remove(f'static/orders/{user_id}.json')
        # print(f'static/orders/{user_id}.json was deleted')
    except OSError:
        pass
    #Open and save the json file
    with open(f'static/orders/{user_id}.json', 'w') as json_file:
        json.dump(order, json_file)
        # print("order was created, and dumped to a json file")

async def menu_callback_user(call: types.CallbackQuery):
    choice = call.data[7:]
    user_id = str(call.from_user.id)

    await call.message.answer(
        text=f"Ви вибрали {choice} димок\n"
            "а тепер можете вибрати смак\n"
            "<i>в кожному меню можна вибрати один смак,\n"
            " загалом це може бути три комбінації</i>",
        reply_markup=taste_menu
    )

    #Open json file
    with open(f'static/orders/{user_id}.json', 'r+') as json_file:
        order = json.load(json_file)
        # print("json file was opened and loaded as just file")
        # print(order, type(order))
        order[str(user_id)]['smoke_strength'] = choice

    #Save the json file
    with open(f'static/orders/{user_id}.json', 'r+') as json_file:
        json.dump(order, json_file)
        # print("json file was opened and dumped as json file")
        # print(order, type(order))

async def taste_menu_callback_user(call: types.CallbackQuery):
    choice = call.data[7:]
    user_id = str(call.from_user.id)

    #Open json file
    with open(f'static/orders/{user_id}.json', 'r+') as json_file:
        order = json.load(json_file)

    if 'taste_choice' not in order[user_id]:
        await call.message.answer(
            text=f"Ваш вибір №1 це {choice}, тепер можете вибрати наступний смак,\n"
            " а також повернутись назад, або закінчити замовлення",
            reply_markup=taste_menu)
        order[user_id]['taste_choice'] = choice

        # Save the json file
        with open(f'static/orders/{user_id}.json', 'r+') as json_file:
            json.dump(order, json_file)
            # print("json file was opened and dumped as json file")
            # print(order, type(order))

    elif 'second_taste_choice' not in order[user_id]:
        await call.message.answer(
            text=f"Ваш вибір №2 це {choice}, тепер можете вибрати наступний смак,\n"
            " а також повернутись назад, або закінчити замовлення",
            reply_markup=taste_menu)
        order[user_id]['second_taste_choice'] = choice

        # Save the json file
        with open(f'static/orders/{user_id}.json', 'r+') as json_file:
            json.dump(order, json_file)
            # print("json file was opened and dumped as json file")
            # print(order, type(order))

    elif 'third_taste_choice' not in order[user_id]:
        await call.message.answer(
            text=f"Ваш вибір №3 це {choice}, тепер можете"
            " закінчити замовлення",
            reply_markup=order_end)
        order[user_id]['third_taste_choice'] = choice

        # Save the json file
        with open(f'static/orders/{user_id}.json', 'r+') as json_file:
            json.dump(order, json_file)
            # print("json file was opened and dumped as json file")
            # print(order, type(order))

async def end_menu_callback_user(call: types.CallbackQuery):
    user_name = call.from_user.full_name
    user_id = str(call.from_user.id)
    order_name = str(user_id)
    # print(order_name)

    #Open the json file
    with open(f'static/orders/{user_id}.json', 'r') as json_file:
        order = json.load(json_file)
        print("json file was opened and loaded as json file")
        print(order, type(order))

    await call.message.delete()
    # await call.message.answer("Ви замовили:\n"
    #                           f"Міцність: <b>{order[user_id]['smoke_strength']}</b>\n"
    #                           f"Перший смак: <b>{order[user_id]['taste_choice']}</b>\n"
    #                           f"Другий смак: <b>{order[user_id]['second_taste_choice']}</b>\n"
    #                           f"Третій смак: <b>{order[user_id]['third_taste_choice']}</b>\n"
    #                           f"Дякуємо за користання нашими послугами. Замовлення невдовзі буде виконано.")
    await call.message.answer("Ваше замовлення надіслано,\n "
                              "дякуємо за користання нашими послугами.\n"
                              " виконуємо....")

    #Save data from json to database table
    db.add_order(
        name=order[user_id]['user_full_name'],
        order_name=order_name,
        smoke_strength_choice=order[user_id]['smoke_strength'],
        taste_choice=order[user_id]['taste_choice'],
        second_taste_choice=order[user_id]['second_taste_choice'],
        third_taste_choice=order[user_id]['third_taste_choice']
    )

def register_user_start(dp: Dispatcher):
    dp.register_message_handler(start_user, commands=["start"])

def register_menu_callback_user(dp: Dispatcher):
    dp.register_callback_query_handler(menu_callback_user,
                                       strength_callback.filter(grade="Легкий"),
                                       state=None)
    dp.register_callback_query_handler(menu_callback_user,
                                       strength_callback.filter(grade="Середній"),
                                       state=None)
    dp.register_callback_query_handler(menu_callback_user,
                                       strength_callback.filter(grade="Міцний"),
                                       state=None)

def register_taste_menu_callback_user(dp: Dispatcher):
    dp.register_callback_query_handler(taste_menu_callback_user,
                                       strength_callback.filter(grade="Свіжий"),
                                       state=None)
    dp.register_callback_query_handler(taste_menu_callback_user,
                                       strength_callback.filter(grade="Солодкий"),
                                       state=None)
    dp.register_callback_query_handler(taste_menu_callback_user,
                                       strength_callback.filter(grade="Пряний"),
                                       state=None)
    dp.register_callback_query_handler(taste_menu_callback_user,
                                       strength_callback.filter(grade="Фруктовий"),
                                       state=None)
    dp.register_callback_query_handler(taste_menu_callback_user,
                                       strength_callback.filter(grade="Цитрус"),
                                       state=None)

def register_own_choice_menu_callback_user(dp: Dispatcher):
    dp.register_callback_query_handler(taste_menu_callback_user,
                                       strength_callback.filter(grade="Свій варіант"),
                                       state=None)

def register_end_menu_callback_user(dp: Dispatcher):
    dp.register_callback_query_handler(end_menu_callback_user,
                                       strength_callback.filter(grade="Закінчити замовлення"),
                                       state=None)

# def register_empty_callback(dp: Dispatcher):
#     dp.register_callback_query_handler(empty_callback, state=None,)
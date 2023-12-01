import json
import os

from aiogram import types, Dispatcher
from tg_bot.keyboards.callback_data import strength_callback
from tg_bot.keyboards.inline import strength_menu, taste_menu, order_end
from tg_bot.models.database_model import Database

db = Database()


async def start_user(message: types.Message):
    user_full_name = message.from_user.full_name
    user_id = str(message.from_user.id)

    await message.reply(
        text=f"Привіт {user_full_name} Ви знаходитесь в нашому Хабі\n"
             "завдяки мені Ви зможете легко та швидко зробити замовлення"
             " давайте ж розпочнемо з міцності кал\'ьяну",
        reply_markup=strength_menu
    )
    # Create user order

    order: dict = {user_id: {
                        'name': user_full_name,
                        'order_name': '',
                        'smoke_strength_choice': '',
                        'taste_choice': '',
                        'second_taste_choice': '',
                        'third_taste_choice': ''
                        }
                   }

    # Delete exists filenames
    try:
        os.remove(f'static/orders/{user_id}.json')
    except OSError:
        pass
    # Open and save the json file
    save_to_json(user_id=user_id, function='dump', order=order, method='w')


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

    # Open json file
    order = save_to_json(user_id, 'load', 'r+')
    order[str(user_id)]['smoke_strength_choice'] = choice

    # Save the json file
    save_to_json(user_id, 'dump', 'r+', order)
    await call.message.delete()


async def taste_menu_callback_user(call: types.CallbackQuery):
    choice = call.data[7:]
    print(choice)
    user_id = str(call.from_user.id)

    # Open json file
    order = save_to_json(user_id, 'load', 'r+')

    if order[user_id]['taste_choice'] == '' and choice != "Закінчити замовлення":
        await call.message.answer(
            text=f"Ваш вибір №1 це {choice}, тепер можете вибрати наступний смак,\n"
                 " а також повернутись назад, або закінчити замовлення",
            reply_markup=taste_menu)

        order[user_id]['taste_choice'] = choice
        # Save the json file
        save_to_json(user_id, 'dump', 'r+', order)
        await call.message.delete()

    elif order[user_id]['second_taste_choice'] == '' and choice != "Закінчити замовлення":
        await call.message.answer(
            text=f"Ваш вибір №2 це {choice}, тепер можете вибрати наступний смак,\n"
                 " а також повернутись назад, або закінчити замовлення",
            reply_markup=taste_menu)

        order[user_id]['second_taste_choice'] = choice
        # Save the json file
        save_to_json(user_id, 'dump', 'r+', order)
        await call.message.delete()

    elif order[user_id]['third_taste_choice'] == '' and choice != "Закінчити замовлення":
        await call.message.answer(
            text=f"Ваш вибір №3 це {choice}, тепер можете"
                 " закінчити замовлення",
            reply_markup=order_end)

        order[user_id]['third_taste_choice'] = choice
        # Save the json file
        save_to_json(user_id, 'dump', 'r+', order)
        await call.message.delete()


async def end_menu_callback_user(call: types.CallbackQuery):
    user_id = str(call.from_user.id)
    order_name = str(user_id)
    # Open the json file
    order: dict = save_to_json(user_id, 'load', 'r+')

    await call.message.answer("Ваше замовлення надіслано,\n "
                              "дякуємо за користання нашими послугами.\n"
                              " виконуємо....")
    await call.message.delete()

    # Save data from json to database table
    db.add_order(
        name=order[user_id]['name'],
        order_name=order_name,
        smoke_strength_choice=order[user_id]['smoke_strength_choice'],
        taste_choice=order[user_id]['taste_choice'],
        second_taste_choice=order[user_id]['second_taste_choice'],
        third_taste_choice=order[user_id]['third_taste_choice'],
        chatID=call.message.chat.id.__str__()
    )


def save_to_json(user_id: str, function: str, method: str, order=None, ):

    if function == 'load':
        with open(f'static/orders/{user_id}.json', method) as json_file:
            order = json.load(json_file)
            print(
                f"""
                _________________ from save_to_json______________
                !!!!!!!!{user_id}.json successfully updated!!!!!!
                """
            )
            return order

    elif function == 'dump':
        with open(f'static/orders/{user_id}.json', method) as json_file:
            json.dump(order, json_file)
            print(
                f"""
                _________________ from save_to_json______________
                !!!!!!!!{user_id}.json returns a string!!!!!!
                """
            )

    else:
        print("data was not read or dump")


def register_user_start(dp: Dispatcher):
    dp.register_message_handler(start_user, commands=["start"])


def register_menu_callback_user(dp: Dispatcher):
    dp.register_callback_query_handler(menu_callback_user,
                                       strength_callback.filter(data="Легкий"),
                                       state=None)
    dp.register_callback_query_handler(menu_callback_user,
                                       strength_callback.filter(data="Середній"),
                                       state=None)
    dp.register_callback_query_handler(menu_callback_user,
                                       strength_callback.filter(data="Міцний"),
                                       state=None)


def register_taste_menu_callback_user(dp: Dispatcher):
    taste_list: list = ["Свіжий", "Солодкий", "Пряний", "Фруктовий", "Цитрус", "Медовий"]
    for taste in taste_list:
        dp.register_callback_query_handler(taste_menu_callback_user,
                                           strength_callback.filter(data=taste), state=None)
    # dp.register_callback_query_handler(taste_menu_callback_user,
    #                                    strength_callback.filter(data="Свіжий"),
    #                                    state=None)
    # dp.register_callback_query_handler(taste_menu_callback_user,
    #                                    strength_callback.filter(data="Солодкий"),
    #                                    state=None)
    # dp.register_callback_query_handler(taste_menu_callback_user,
    #                                    strength_callback.filter(data="Пряний"),
    #                                    state=None)
    # dp.register_callback_query_handler(taste_menu_callback_user,
    #                                    strength_callback.filter(data="Фруктовий"),
    #                                    state=None)
    # dp.register_callback_query_handler(taste_menu_callback_user,
    #                                    strength_callback.filter(data="Цитрус"),
    #                                    state=None)


def register_own_choice_menu_callback_user(dp: Dispatcher):
    dp.register_callback_query_handler(taste_menu_callback_user,
                                       strength_callback.filter(data="Свій варіант"),
                                       state=None)


def register_end_menu_callback_user(dp: Dispatcher):
    dp.register_callback_query_handler(end_menu_callback_user,
                                       strength_callback.filter(data="Закінчити замовлення"),
                                       state=None)


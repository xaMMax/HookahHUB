from bot_main import bot


async def send_message_to_user(data: dict):
    # chat = await bot.get_chat(chat_id=data['userID'])
    await bot.send_message(data['userID'], text=f'Дякую за ваше замовлення, вже готую.\n'
                                                f'а ось основні деталі:\n'
                                                f'Замовлення:<b> №{data["orderID"]}\n </b>'
                                                f'Міцність:<b> {data["strength"]}\n </b>'
                                                f'Основний смак:<b> {data["flavour"]}\n </b>'
                                                f'Додатковий смак 1:<b> {data["flavour1"]}\n </b>'
                                                f'Додатковий смак 2:<b> {data["flavour2"]}\n </b>', parse_mode='html')

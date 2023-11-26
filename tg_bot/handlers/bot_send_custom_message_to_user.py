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

#
# 'data': 'CONFIRMED',
# 'orderID': parseInt(buttonIdSlise),
# 'userID': data[2],
# 'strength': data[3],
# 'flavour': data[4],
# 'flavour1': data[5],
# 'flavour2': data[6]},
# var order_header = document.createElement("h5");
#     order_header.innerHTML = "id замовлення: " + data[0];
#     var name = document.createElement("p");
#     name.innerHTML = 'Імя користувача: <b> '+ data[1] +'</b>';
#     var strength = document.createElement("li");
#     strength.innerHTML = "Міцність: <b>" + data[3] +'</b>';
#     var flavor1 = document.createElement("li");
#     flavor1.innerHTML = "Основний смак: <b>" + data[4] +"</b>";
#     var flavor2 = document.createElement("li");
#     flavor2.innerHTML = "Додатковий смак 1: <b>" + data[5] +"</b>";
#     var flavor3 = document.createElement("li");
#     flavor3.innerHTML = "Додатковий смак 2: <b>" + data[6] +"</b>";
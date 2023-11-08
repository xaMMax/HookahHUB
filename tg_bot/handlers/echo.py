# from aiogram import types, Dispatcher
# from aiogram.dispatcher import FSMContext
# from aiogram.utils.markdown import hcode
#
#
# async def bot_echo(message: types.Message):
#     text = [
#         "Це ехохендлєр без состоянія",
#         "Повідомлення",
#         message.text
#     ]
#     await message.answer(text='\n'.join(text))
#
#
# async def bot_echo_all(message: types.Message, state: FSMContext):
#     state_name = await state.get_state()
#     text = [
#         f"Це ехохендлєр в состоянії {hcode(state_name)}",
#         "Повідомлення",
#         message.text
#     ]
#     await message.answer(text='\n'.join(text))
#
#
# def register_echo(dp: Dispatcher):
#     dp.register_message_handler(bot_echo, state=None)
#     dp.register_message_handler(bot_echo_all, state='*', content_types=types.ContentType.ANY)

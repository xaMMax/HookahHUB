import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tg_bot.config import load_config
from tg_bot.filters.admin import AdminFilter
from tg_bot.filters.menu_one import MenuOne
from tg_bot.handlers.admin import register_admin, register_menu_callback_admin, register_taste_menu_callback_admin
from tg_bot.handlers.menu import register_menu_callback_user, register_taste_menu_callback_user, register_user_start, \
    register_end_menu_callback_user, register_own_choice_menu_callback_user
from tg_bot.middlewares.db import DbMiddleware
from main import db

loger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    dp.setup_middleware(DbMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(MenuOne)


def register_all_handlers(dp):
    register_admin(dp)
    # register_echo(dp)
    register_menu_callback_admin(dp)
    register_taste_menu_callback_admin(dp)
    register_user_start(dp)
    register_menu_callback_user(dp)
    register_taste_menu_callback_user(dp)
    register_end_menu_callback_user(dp)
    register_own_choice_menu_callback_user(dp)
    pass


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    config = load_config(".env")

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    db.create_table_orders()
    dp = Dispatcher(bot, storage=storage)
    bot["config"] = config

    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        loger.error("Bot stopped!")

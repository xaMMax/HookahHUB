from aiogram.dispatcher.filters import BoundFilter

from tg_bot.config import Config


class MenuOne(BoundFilter):
    # key = 'is_admin'

    # def __init__(self, is_admin=None):
    #     self.is_admin = is_admin

    async def check(self, obj) -> bool:
        return True if obj == "strength_menu" else False

from aiogram.dispatcher.filters import BoundFilter


class MenuOne(BoundFilter):
    # key = 'is_admin'

    # def __init__(self, is_admin=None):
    #     self.is_admin = is_admin

    async def check(self, obj) -> bool:
        return True if obj == "strength_menu" else False

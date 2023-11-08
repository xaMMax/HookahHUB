from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    async def pre_process(self, obj, data, *args):
        db_session = obj.bot.get('db')
        # data['same_model'] = await Model.get()
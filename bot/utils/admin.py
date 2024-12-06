from config.config_reader import config

class IsAdmin:
    @staticmethod
    async def check_user(tg_id: int):
        print([config.cwc, config.owner, ])
        return tg_id in [config.cwc, config.owner, ]
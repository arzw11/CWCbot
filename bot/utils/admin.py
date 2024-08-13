from config.config_reader import config

class IsAdmin:
    def __init__(self):
        pass

    def check_user(self, tg_id: int):
        return tg_id in [config.cwc, config.owner, ]

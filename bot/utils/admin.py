from config.config_reader import config

class IsAdmin:
<<<<<<< HEAD
    @staticmethod
    async def check_user(tg_id: int):
        print([config.cwc, config.owner, ])
        return tg_id in [config.cwc, config.owner, ]
=======
    def __init__(self):
        pass

    def check_user(self, tg_id: int):
        return tg_id in [config.cwc, config.owner, ]
>>>>>>> 57f8029b15298888eb1acee5db4795b6ff004bb6

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
<<<<<<< HEAD
    bot_token: SecretStr
    owner: str
    cwc: str
    db_lite: str
=======
>>>>>>> 57f8029b15298888eb1acee5db4795b6ff004bb6
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    bot_token: SecretStr
    owner: int
    cwc: int
    db_lite: str

config = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    bot_token: SecretStr
    owner: SecretStr
    cwc: SecretStr
    db_lite: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

config = Settings()

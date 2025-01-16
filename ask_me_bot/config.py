import dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


dotenv.load_dotenv()


class Settings(BaseSettings):
    BOT_TOKEN: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    model_config = SettingsConfigDict()

    def get_db_url() -> str:
        pass


settings = Settings()

import redis
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USER: str
    REDIS_PASS: str

    OPEN_WEATHER_BASE_URL: str
    OPEN_WEATHER_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def rd(self):
        return redis.Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=0,
            username=self.REDIS_USER,
            password=self.REDIS_PASS,
            decode_responses=True,
        )


settings = Settings()

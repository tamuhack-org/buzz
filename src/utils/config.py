from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    DISCORD_BOT_TOKEN: str
    MENTOR_CHANNEL_ID: int  # discord.py expects channel ID to be int
    MENTOR_ROLE_ID: int
    HMAC_SECRET: str
    HELPR_URL: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env"
    )
    PROJECT_NAME:str = "Expense Tracker API"
    API_V1_STR:str = "/api/v1"
    DATABASE_URL:str
settings = Settings()
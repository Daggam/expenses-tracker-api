from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env"
    )
    PROJECT_NAME:str = "Expense Tracker API"
    API_V1_STR:str = "/api/v1"
    DATABASE_URL:str
    SECRET_KEY:str
    ALG_JWT:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
settings = Settings()
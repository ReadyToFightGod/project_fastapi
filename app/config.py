from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    secret_key: str
    algo: str
    access_token_expire_minutes: int
    db_path: str
    admin_username: str
    admin_real_name: str
    admin_email: str
    admin_password: str


settings = Settings()

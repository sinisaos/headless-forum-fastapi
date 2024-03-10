from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int

    secret_key: str

    algorithm: str
    access_token_expire_minutes: int


settings = Settings(_env_file=".env")  # type: ignore

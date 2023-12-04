from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    sqlalchemy_database_url: str = (
        "postgresql+psycopg2://user:password@localhost:5432/postgres"
    )
    postgres_db: str = "postgres"
    postgres_user: str = "user"
    postgres_password: str = "password"
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    secret_key: str = "secret_key"
    algorithm: str = "HS256"
    mail_username: str = "example@ex.ua"
    mail_password: str = "password"
    mail_from: str = "example@meta.ua"
    mail_port: int = 465
    mail_server: str = "smtp.meta.ua"
    redis_host: str = "localhost"
    redis_port: int = 6379
    cloudinary_name: str = "cloudinary"
    cloudinary_api_key: int = 999999999999999
    cloudinary_api_secret: str = "top_secret"
    cloudinary_pics_folder: str = "folder_name"


settings = Settings()

import os
from dotenv import load_dotenv
load_dotenv()


class Settings:
    DB_NAME: str = os.getenv("DB_NAME", "products")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    API_KEY: str = os.getenv("OPENAI_KEY")
    DATABASE_URL: str = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    MODEL: str = os.getenv("MODEL")

settings = Settings()
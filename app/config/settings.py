from pydantic import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str
    chroma_persist_dir: str = "./chroma_data"

    class Config:
        env_file = ".env"

settings = Settings()
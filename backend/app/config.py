import os
from dotenv import load_dotenv
from pymongo import MongoClient  # ✅ Add this import

# Load environment variables from .env file
load_dotenv()

class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_secret_key")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    MONGO_URI: str = os.getenv("MONGO_URI")
    REDIS_URL: str = os.getenv("REDIS_URL")
    HF_API_KEY: str = os.getenv("HF_API_KEY")
    HF_MODEL_NAME: str = os.getenv("MODEL_NAME", "google/flan-t5-base")

    @property
    def is_valid(self) -> bool:
        return all([self.DATABASE_URL, self.MONGO_URI, self.REDIS_URL])

settings = Settings()

# Optional: Warning if env vars are incomplete
if not settings.is_valid:
    print("[WARNING] Some environment variables are missing! Check your .env file.")

# ✅ Define mongo_client here
mongo_client = MongoClient(settings.MONGO_URI)

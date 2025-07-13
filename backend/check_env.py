import os
from dotenv import load_dotenv

load_dotenv()

print("PostgreSQL URL:", os.getenv("DATABASE_URL"))
print("MongoDB URL:", os.getenv("MONGO_URI"))
print("Secret Key:", os.getenv("SECRET_KEY"))
print("OpenAI API Key:", os.getenv("OPENAI_API_KEY"))

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

settings = Config()
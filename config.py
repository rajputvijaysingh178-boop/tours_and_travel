import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    MONGO_URI = os.getenv(
        "MONGO_URI",
        "mongodb://localhost:27017"
    )

    DB_NAME = "travel_management"

    
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "VIJAYSINGHRAJPUT"
    )

    JWT_ALGORITHM = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    REFRESH_TOKEN_EXPIRE_DAYS = 7


settings = Settings()
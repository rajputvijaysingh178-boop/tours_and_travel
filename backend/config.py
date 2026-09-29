import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    MONGO_URI = os.getenv("MONGO_URI", "").strip()
    DB_NAME = os.getenv("DB_NAME", "travel_management").strip() or "travel_management"

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "").strip()
    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "").strip()
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "").strip()
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "").strip()

    PAYMENT_PROVIDER = os.getenv("PAYMENT_PROVIDER", "razorpay").strip().lower()
    PAYMENT_KEY_ID = os.getenv("PAYMENT_KEY_ID", "").strip()
    PAYMENT_KEY_SECRET = os.getenv("PAYMENT_KEY_SECRET", "").strip()

    CART_TTL_MINUTES = int(os.getenv("CART_TTL_MINUTES", "180"))
    HOLD_TTL_MINUTES = int(os.getenv("HOLD_TTL_MINUTES", "30"))
    TAX_RATE = float(os.getenv("TAX_RATE", "0.05"))


settings = Settings()

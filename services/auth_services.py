from datetime import timedelta

from database import users_collection, customers_collection
from security import (hash_password,verify_password,create_jwt_token,utc_now,)
from config import settings


def register_user(
    name: str,
    email: str,
    password: str,
    phone: str,
    address: str,
    emergency_contact: str,
):
   
    existing_user = users_collection.find_one(
        {"email": email}
    )

    if existing_user:
        raise ValueError("Email already registered")

    
    user_document = {
        "name": name,
        "email": email,
        "password_hash": hash_password(password),
        "role": "customer",
        "is_active": True,
        "created_at": utc_now(),
    }

    
    user_result = users_collection.insert_one(
        user_document
    )

    user_id = str(user_result.inserted_id)

    
    customer_document = {
        "user_id": user_id,
        "phone": phone,
        "address": address,
        "emergency_contact": emergency_contact,
        "created_at": utc_now(),
    }

    customers_collection.insert_one(
        customer_document
    )

    return {
        "message": "Registration successful",
        "user_id": user_id,
    }


def login_user(
    email: str,
    password: str,
):
    # Find user
    user = users_collection.find_one(
        {"email": email}
    )

    if not user:
        raise ValueError("Invalid email or password")

    # Check whether account is active
    if not user.get("is_active", True):
        raise ValueError("User account is inactive")

    # Verify password
    if not verify_password(
        password,
        user["password_hash"],
    ):
        raise ValueError("Invalid email or password")

    user_id = str(user["_id"])

    # Create access token
    access_token = create_jwt_token(
        user_id=user_id,
        token_type="access",
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    # Create refresh token
    refresh_token = create_jwt_token(
        user_id=user_id,
        token_type="refresh",
        expires_delta=timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        ),
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
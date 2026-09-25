from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from database import users_collection
from security import decrypt_jwt_token
from bson import ObjectId


security = HTTPBearer()


<<<<<<< HEAD
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security),):
=======
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)):
>>>>>>> origin/anil
    token = credentials.credentials
    try:
        payload = decrypt_jwt_token(token)
        if payload.get("token") != "access":
<<<<<<< HEAD
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid access token",)
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token",)
        user = users_collection.find_one(
            {"_id": ObjectId(user_id)})

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found",)

        if not user.get("is_active", True):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User account is inactive",)
=======
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid access token")
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token")

        user = users_collection.find_one(
            {"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found")

        if not user.get("is_active", True):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive")
>>>>>>> origin/anil

        user["id"] = str(user["_id"])

        return user

    except HTTPException:
        raise

    except Exception:
<<<<<<< HEAD
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token",)
=======
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token")


def get_admin_user(
    current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user
>>>>>>> origin/anil

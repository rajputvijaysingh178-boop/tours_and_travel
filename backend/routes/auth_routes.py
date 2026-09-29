from fastapi import APIRouter, HTTPException
from schemas.auth_schema import RegisterSchema,LoginSchema,TokenResponse
from services.auth_services import register_user,login_user


router = APIRouter(prefix="/auth",tags=["Authentication"],)


@router.post("/register")
def register(data: RegisterSchema):
    try:
        return register_user(
            name=data.name,
            email=data.email,
            password=data.password,
            phone=data.phone,
            address=data.address,
            emergency_contact=data.emergency_contact, )
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e),)


@router.post("/login",response_model=TokenResponse,)
def login(data: LoginSchema):
    try:
        return login_user(email=data.email,password=data.password,)

    except ValueError as e:
        raise HTTPException(status_code=401,detail=str(e),)
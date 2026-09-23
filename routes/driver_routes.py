from fastapi import APIRouter

router = APIRouter(prefix="/drivers",tags=["Drivers"])


@router.post("")
def create_driver():
    pass
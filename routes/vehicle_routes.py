from fastapi import APIRouter

router = APIRouter(prefix="/vehicles",tags=["Vehicles"])


@router.post("")
def create_vehicle():
    pass


@router.get("/available")
def get_available_vehicles():
    pass
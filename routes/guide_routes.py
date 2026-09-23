from fastapi import APIRouter

router = APIRouter(prefix="/guides",tags=["Guides"])


@router.post("")
def create_guide():
    pass


@router.get("/available")
def get_available_guides():
    pass


@router.post("/{guide_id}/assign")
def assign_guide(guide_id: str):
    pass


@router.get("/{guide_id}/tours")
def get_guide_tours(guide_id: str):
    pass
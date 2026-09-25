<<<<<<< HEAD
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
=======
from fastapi import APIRouter, HTTPException

from schemas.guide_schema import GuideCreateSchema

from services.guide_service import (
    create_guide,
    get_available_guides,
    assign_guide,
    get_guide_tours
)


router = APIRouter(
    prefix="/guides",
    tags=["Guides"]
)


@router.post("")
def create_guide_route(data: GuideCreateSchema):
    return create_guide(data)


@router.get("/available")
def get_available_guides_route():
    return get_available_guides()


@router.post("/{guide_id}/assign")
def assign_guide_route(
    guide_id: str,
    departure_id: str
):
    try:
        return assign_guide(
            guide_id,
            departure_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get("/{guide_id}/tours")
def get_guide_tours_route(
    guide_id: str
):
    return get_guide_tours(guide_id)
>>>>>>> origin/anil

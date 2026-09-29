from fastapi import APIRouter, HTTPException

from schemas.guide_schema import (
    GuideCreateSchema,
    GuideUpdateSchema,
)

from services.guide_service import (
    create_guide,
    get_guides,
    get_guide,
    update_guide,
    delete_guide,
)


router = APIRouter(
    prefix="/guides",
    tags=["Guides"]
)


@router.post("")
def create_guide_route(
    data: GuideCreateSchema
):
    try:
        return create_guide(data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("")
def get_guides_route(
    destination_id: str | None = None
):
    return get_guides(destination_id)


@router.get("/{guide_id}")
def get_guide_route(guide_id: str):
    try:
        return get_guide(guide_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.put("/{guide_id}")
def update_guide_route(
    guide_id: str,
    data: GuideUpdateSchema
):
    try:
        return update_guide(
            guide_id,
            data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.delete("/{guide_id}")
def delete_guide_route(
    guide_id: str
):
    try:
        return delete_guide(guide_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
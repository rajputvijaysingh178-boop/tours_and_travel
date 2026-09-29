from fastapi import APIRouter, HTTPException

from schemas.activity_schema import (
    ActivityCreateSchema,
    ActivityUpdateSchema,
)

from services.activity_service import (
    create_activity,
    get_activities,
    get_activity,
    update_activity,
    delete_activity,
)


router = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)


@router.post("")
def create_activity_route(data: ActivityCreateSchema):
    try:
        return create_activity(data)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("")
def get_activities_route(
    destination_id: str | None = None
):
    return get_activities(destination_id)


@router.get("/{activity_id}")
def get_activity_route(activity_id: str):
    try:
        return get_activity(activity_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.put("/{activity_id}")
def update_activity_route(
    activity_id: str,
    data: ActivityUpdateSchema
):
    try:
        return update_activity(
            activity_id,
            data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.delete("/{activity_id}")
def delete_activity_route(
    activity_id: str
):
    try:
        return delete_activity(activity_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
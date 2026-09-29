from fastapi import APIRouter, HTTPException

from schemas.itinerary_schema import (
    ItineraryCreateSchema,
    ItineraryUpdateSchema
)

from services.itinerary_service import (
    create_itinerary,
    get_package_itinerary,
    update_itinerary,
    delete_itinerary
)


router = APIRouter(
    tags=["Itinerary"]
)


@router.post("/packages/{package_id}/itinerary")
def create_itinerary_route(
    package_id: str,
    data: ItineraryCreateSchema
):
    try:
        return create_itinerary(
            package_id,
            data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/packages/{package_id}/itinerary")
def get_itinerary_route(
    package_id: str
):
    try:
        return get_package_itinerary(
            package_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.put("/itinerary/{itinerary_id}")
def update_itinerary_route(
    itinerary_id: str,
    data: ItineraryUpdateSchema
):
    try:
        return update_itinerary(
            itinerary_id,
            data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.delete("/itinerary/{itinerary_id}")
def delete_itinerary_route(
    itinerary_id: str
):
    try:
        return delete_itinerary(
            itinerary_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
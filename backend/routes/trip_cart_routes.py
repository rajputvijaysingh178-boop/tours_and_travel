from fastapi import APIRouter, HTTPException, Depends

from services.aut_dependency import get_current_user

from schemas.trip_cart_schema import (
    TripCartCreateSchema,
    HotelSelectionSchema,
    RoomSelectionSchema,
    ActivitiesSelectionSchema,
    GuideSelectionSchema,
    VehicleSelectionSchema,
    PassengerDetailsSchema,
    ReviewSchema,
)

from services.trip_cart_service import (
    create_trip_cart,
    get_trip_cart,
    select_hotel,
    select_room,
    select_activities,
    select_guide,
    select_vehicle,
    confirm_review,
    add_passengers,
)


router = APIRouter(
    prefix="/trip-carts",
    tags=["Trip Carts"]
)


@router.post("")
def create_trip_cart_route(
    data: TripCartCreateSchema,
    current_user: dict = Depends(get_current_user),
):
    try:
        return create_trip_cart(
            current_user["id"],
            data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/{cart_id}")
def get_trip_cart_route(
    cart_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        return get_trip_cart(
            cart_id,
            current_user["id"],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.patch("/{cart_id}/hotel")
def select_hotel_route(
    cart_id: str,
    data: HotelSelectionSchema,
    current_user: dict = Depends(get_current_user),
):
    try:
        return select_hotel(
            cart_id,
            current_user["id"],
            data.hotel_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.patch("/{cart_id}/room")
def select_room_route(
    cart_id: str,
    data: RoomSelectionSchema,
    current_user: dict = Depends(get_current_user),
):
    try:
        return select_room(
            cart_id,
            current_user["id"],
            data.room_id,
            data.room_quantity,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.patch("/{cart_id}/activities")
def select_activities_route(
    cart_id: str,
    data: ActivitiesSelectionSchema,
    current_user: dict = Depends(get_current_user),
):
    try:
        return select_activities(
            cart_id,
            current_user["id"],
            data.activity_ids,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.patch("/{cart_id}/guide")
def select_guide_route(
    cart_id: str,
    data: GuideSelectionSchema,
    current_user: dict = Depends(get_current_user),
):
    try:
        if not data.guide_id:
            raise ValueError(
                "guide_id is required"
            )

        return select_guide(
            cart_id,
            current_user["id"],
            data.guide_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.patch("/{cart_id}/vehicle")
def select_vehicle_route(
    cart_id: str,
    data: VehicleSelectionSchema,
    current_user: dict = Depends(get_current_user),
):
    try:
        if not data.vehicle_id:
            raise ValueError(
                "vehicle_id is required"
            )

        return select_vehicle(
            cart_id,
            current_user["id"],
            data.vehicle_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/{cart_id}/review")
def confirm_review_route(
    cart_id: str,
    data: ReviewSchema,
    current_user: dict = Depends(get_current_user),
):
    try:
        if not data.confirmed:
            raise ValueError(
                "Review must be confirmed"
            )

        return confirm_review(
            cart_id,
            current_user["id"],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.put("/{cart_id}/passengers")
def add_passengers_route(
    cart_id: str,
    data: PassengerDetailsSchema,
    current_user: dict = Depends(get_current_user),
):
    try:
        return add_passengers(
            cart_id,
            current_user["id"],
            data.passengers,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
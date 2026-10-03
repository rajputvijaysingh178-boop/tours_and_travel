from fastapi import APIRouter, HTTPException

from services.inventory_hold_service import (
    create_hold,
    get_cart_holds,
    release_hold,
    release_cart_holds,
    expire_old_holds,
)


router = APIRouter(
    prefix="/inventory-holds",
    tags=["Inventory Holds"]
)


@router.post("")
def create_hold_route(
    cart_id: str,
    resource_type: str,
    resource_id: str,
    travel_date: str,
    end_date: str | None = None,
    quantity: int = 1,
):
    try:
        return create_hold(
            cart_id,
            resource_type,
            resource_id,
            travel_date,
            end_date,
            quantity,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/cart/{cart_id}")
def get_cart_holds_route(
    cart_id: str
):
    return get_cart_holds(cart_id)


@router.delete("/{hold_id}")
def release_hold_route(
    hold_id: str
):
    try:
        return release_hold(hold_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.delete("/cart/{cart_id}")
def release_cart_holds_route(
    cart_id: str
):
    return release_cart_holds(cart_id)


@router.post("/expire")
def expire_old_holds_route():
    return expire_old_holds()
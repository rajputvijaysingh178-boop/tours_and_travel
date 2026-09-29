from fastapi import APIRouter, HTTPException, Depends

from services.aut_dependency import get_current_user

from services.payment_order_service import (
    create_payment_order,
    get_payment_order,
)


router = APIRouter(
    prefix="/payment-orders",
    tags=["Payment Orders"]
)


@router.post("")
def create_payment_order_route(
    cart_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        return create_payment_order(
            cart_id,
            current_user["id"],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get("/{payment_order_id}")
def get_payment_order_route(
    payment_order_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        return get_payment_order(
            payment_order_id,
            current_user["id"],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
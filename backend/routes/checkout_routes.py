from fastapi import APIRouter, HTTPException, Depends

from services.aut_dependency import get_current_user

from schemas.checkout_schema import (
    PaymentVerificationSchema,
)

from services.checkout_service import (
    lock_cart,
    create_payment_order,
    verify_payment,
)


router = APIRouter(
    prefix="/checkout",
    tags=["Checkout"]
)


@router.post("/{cart_id}/lock")
def lock_cart_route(
    cart_id: str,
    current_user: dict = Depends(get_current_user),
):
    try:
        return lock_cart(
            cart_id,
            current_user["id"],
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/{cart_id}/payment")
def create_payment_route(
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


@router.post("/{cart_id}/verify")
def verify_payment_route(
    cart_id: str,
    data: PaymentVerificationSchema,
    current_user: dict = Depends(get_current_user),
):
    try:
        return verify_payment(
            cart_id,
            current_user["id"],
            data.payment_id,
            data.payment_signature,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
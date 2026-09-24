from fastapi import APIRouter, Depends, HTTPException

from schemas.customer_schema import (
    CustomerUpdateSchema,
    CustomerResponseSchema
)

from services.aut_dependency import get_current_user

from services.customer_service import (
    get_customer_profile,
    update_customer_profile,
    get_customer_bookings
)


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.get("/me", response_model=CustomerResponseSchema)
def get_my_profile(
    current_user: dict = Depends(get_current_user)
):
    try:
        return get_customer_profile(current_user["id"])
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.put("/me", response_model=CustomerResponseSchema)
def update_my_profile(
    data: CustomerUpdateSchema,
    current_user: dict = Depends(get_current_user)
):
    try:
        update_data = data.model_dump(exclude_none=True)

        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No fields provided for update"
            )

        return update_customer_profile(
            current_user["id"],
            update_data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get("/{customer_id}/bookings")
def get_customer_bookings_route(
    customer_id: str
):
    try:
        return get_customer_bookings(customer_id)
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
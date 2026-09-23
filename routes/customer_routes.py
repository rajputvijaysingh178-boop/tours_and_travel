from fastapi import APIRouter, Depends, HTTPException
from database import customers_collection
from schemas.customer_schema import CustomerUpdateSchema, CustomerResponseSchema
from services.aut_dependency import get_current_user

router = APIRouter(prefix="/customers", tags=["Customers"])
@router.get("/me", response_model=CustomerResponseSchema)
def get_my_profile(current_user: dict = Depends(get_current_user)):
    customer = customers_collection.find_one({"user_id": current_user["id"]})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer profile not found")
    return {
        "id": str(customer["_id"]),
        "user_id": customer["user_id"],
        "phone": customer["phone"],
        "address": customer["address"],
        "emergency_contact": customer["emergency_contact"],
    }
@router.put("/me", response_model=CustomerResponseSchema)
def update_my_profile(data: CustomerUpdateSchema,
                      current_user: dict = Depends(get_current_user)):
    customer = customers_collection.find_one({"user_id": current_user["id"]})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer profile not found")
    update_data = data.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    customers_collection.update_one({"_id": customer["_id"]}, {"$set": update_data})
    updated_customer = customers_collection.find_one({"_id": customer["_id"]})
    return {
        "id": str(updated_customer["_id"]),
        "user_id": updated_customer["user_id"],
        "phone": updated_customer["phone"],
        "address": updated_customer["address"],
        "emergency_contact": updated_customer["emergency_contact"]}
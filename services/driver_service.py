from database import drivers_collection
def create_driver(driver_data):
    driver = {
        "name": driver_data.name,
        "phone": driver_data.phone,
        "license_number": driver_data.license_number,
        "availability": driver_data.availability}

    result = drivers_collection.insert_one(driver)
    return {
        "driver_id": str(result.inserted_id),
        "message": "Driver created successfully"}
from database import vehicles_collection
def create_vehicle(vehicle_data):
    vehicle = {
        "vehicle_type": vehicle_data.vehicle_type,
        "capacity": vehicle_data.capacity,
        "status": vehicle_data.status,
        "maintenance_details": vehicle_data.maintenance_details}
    result = vehicles_collection.insert_one(vehicle)
    return {
        "vehicle_id": str(result.inserted_id),
        "message": "Vehicle created successfully"}


def get_available_vehicles():
    vehicles = vehicles_collection.find({
        "status": "available"})

    result = []

    for vehicle in vehicles:
        result.append({
            "vehicle_id": str(vehicle["_id"]),
            "vehicle_type": vehicle["vehicle_type"],
            "capacity": vehicle["capacity"],
            "status": vehicle["status"],
            "maintenance_details": vehicle.get("maintenance_details")})

    return result
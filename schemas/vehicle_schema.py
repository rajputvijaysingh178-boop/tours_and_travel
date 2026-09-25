from pydantic import BaseModel

<<<<<<< HEAD
class VehiclecreateSchema(BaseModel):
    vehicle_id : str
    vehicle_type : str
    capacity : str 
    status : str 
    mantainance_details : str | None = None
    
class VehicleUpdateSchema(BaseModel):
     vehicle_type: str | None = None
     capacity: int | None = None
     status: str | None = None
     maintenance_details: str | None = None
     
class VehicleResponseSchema(BaseModel):
     vehicle_id: str
     vehicle_type: str
     capacity: int
     status: str
     maintenance_details: str | None = None
    
    
    
=======

class VehicleCreateSchema(BaseModel):
    vehicle_type: str
    capacity: int
    status: str
    maintenance_details: str | None = None


class VehicleUpdateSchema(BaseModel):
    vehicle_type: str | None = None
    capacity: int | None = None
    status: str | None = None
    maintenance_details: str | None = None


class VehicleResponseSchema(BaseModel):
    vehicle_id: str
    vehicle_type: str
    capacity: int
    status: str
    maintenance_details: str | None = None
>>>>>>> origin/anil

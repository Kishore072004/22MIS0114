from pydantic import BaseModel

class DepotBase(BaseModel):
    name: str
    location: str

class DepotCreate(DepotBase):
    pass

class Depot(DepotBase):
    id: int
    class Config:
        from_attributes = True

class VehicleBase(BaseModel):
    name: str
    depot_id: int

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    class Config:
        from_attributes = True

class MaintenanceTaskBase(BaseModel):
    vehicle_id: int
    task_name: str
    impact_score: int
    duration_hours: float

class MaintenanceTaskCreate(MaintenanceTaskBase):
    pass

class MaintenanceTask(MaintenanceTaskBase):
    id: int
    class Config:
        from_attributes = True

class ScheduleRequest(BaseModel):
    available_machine_hours: float

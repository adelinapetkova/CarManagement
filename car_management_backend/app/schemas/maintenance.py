from pydantic import BaseModel
from typing import Optional


class MaintenanceRequestCreate(BaseModel):
    carId: int
    serviceType: str
    scheduledDate: str
    garageId: int

    class Config:
        orm_mode = True


class MaintenanceRequestUpdate(BaseModel):
    carId: Optional[int]
    serviceType: Optional[str]
    scheduledDate: Optional[str]
    garageId: Optional[int]


class MaintenanceRequestResponse(BaseModel):
    id: int
    carId: int
    carName: str
    serviceType: str
    scheduledDate: str
    garageId: int
    garageName: str

    class Config:
        orm_mode = True

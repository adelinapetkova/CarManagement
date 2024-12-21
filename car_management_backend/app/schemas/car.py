from pydantic import BaseModel
from typing import List, Optional


class GarageReference(BaseModel):
    id: int
    name: str
    location: str
    city: str
    capacity: int


class CarBase(BaseModel):
    make: str
    model: str
    productionYear: int
    licensePlate: str


class CarCreate(CarBase):
    garageIds: List[int]


class CarUpdate(BaseModel):
    make: Optional[str]
    model: Optional[str]
    productionYear: Optional[int]
    licensePlate: Optional[str]
    garageIds: Optional[List[int]]
    garages: Optional[List[dict]]


class CarResponse(CarBase):
    id: int
    garages: List[GarageReference]

    class Config:
        orm_mode = True

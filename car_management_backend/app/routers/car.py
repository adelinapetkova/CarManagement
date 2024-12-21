from typing import List, Optional
from sqlalchemy.orm import Session, class_mapper
from fastapi import APIRouter, HTTPException, Depends
from car_management_backend.app.schemas.car import CarCreate, CarUpdate, CarResponse
from car_management_backend.app.crud_operations import cars as cars_crud
from car_management_backend.app.models.database import SessionLocal

router = APIRouter()


def sqlalchemy_to_dict(model_instance):
    """ Map the model fields to the response model ones """
    result = {column.name: getattr(model_instance, column.name) for column in
              class_mapper(model_instance.__class__).columns}

    # Map garages relationship
    garages = [
        {
            "id": garage.id,
            "name": garage.name,
            "location": garage.location,
            "city": garage.city,
            "capacity": garage.capacity
        }
        for garage in model_instance.garages
    ]

    return {
        "id": result.get("id"),
        "make": result.get("make"),
        "model": result.get("model"),
        "productionYear": result.get("production_year"),
        "licensePlate": result.get("license_plate"),
        "garages": garages
    }


# Get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/cars", response_model=CarResponse)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    db_car = cars_crud.create_car(db=db, car=car)
    return sqlalchemy_to_dict(db_car)


@router.get("/cars", response_model=List[CarResponse])
def list_cars(carMake: Optional[str] = None, garageId: Optional[int] = None, fromYear: Optional[int] = None, toYear: Optional[int] = None,
              db: Session = Depends(get_db)):
    cars = cars_crud.get_cars(db=db, make=carMake, garage_id=garageId, from_year=fromYear, to_year=toYear)
    return [sqlalchemy_to_dict(car) for car in cars]


@router.get("/cars/{id}", response_model=CarResponse)
def get_car(id: int, db: Session = Depends(get_db)):
    car = cars_crud.get_car(db=db, car_id=id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return sqlalchemy_to_dict(car)


@router.put("/cars/{id}", response_model=CarResponse)
def update_car(id: int, car: CarUpdate, db: Session = Depends(get_db)):
    updated_car = cars_crud.update_car(db=db, car_id=id, car=car)
    if not updated_car:
        raise HTTPException(status_code=404, detail="Car not found")
    return sqlalchemy_to_dict(updated_car)


@router.delete("/cars/{id}")
def delete_car(id: int, db: Session = Depends(get_db)):
    deleted_car = cars_crud.delete_car(db=db, car_id=id)
    if not deleted_car:
        raise HTTPException(status_code=404, detail="Car not found")
    return {"message": "Car deleted successfully"}

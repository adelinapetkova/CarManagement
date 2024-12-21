from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from car_management_backend.app.models.car import Car
from car_management_backend.app.models.garage import Garage
from car_management_backend.app.schemas.car import CarCreate, CarUpdate


def create_car(db: Session, car: CarCreate):
    """ Add a new car to the DB """
    # Validate that the production year is not in the future
    current_year = datetime.now().year
    if car.productionYear > current_year:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid production year: {car.productionYear}."
        )

    # Create car in the DB
    db_car = Car(
        make=car.make,
        model=car.model,
        production_year=car.productionYear,
        license_plate=car.licensePlate
    )

    # Retrieve the Garage objects using the provided IDs and set them for the car
    if car.garageIds:
        garages = db.query(Garage).filter(Garage.id.in_(car.garageIds)).all()
        if len(garages) != len(car.garageIds):
            raise ValueError("Some garage IDs are invalid")
        db_car.garages = garages

    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def get_car(db: Session, car_id: int):
    """ Get a car from the DB via its ID """
    return db.query(Car).filter(Car.id == car_id).first()


def get_cars(db: Session, make: str = None, garage_id: int = None, from_year: int = None, to_year: int = None):
    """ Get all cars from the DB with filter options """
    query = db.query(Car)
    if make:
        query = query.filter(Car.make.ilike(f"%{make}%"))
    if garage_id:
        query = query.filter(Car.garages.any(Garage.id == garage_id))
    if from_year:
        query = query.filter(Car.production_year >= from_year)
    if to_year:
        query = query.filter(Car.production_year <= to_year)
    return query.all()


def update_car(db: Session, car_id: int, car: CarUpdate):
    """ Update info about a car in the DB """
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car:
        if car.make:
            db_car.make = car.make
        if car.model:
            db_car.model = car.model
        if car.productionYear:
            # Validate that the production year is not in the future
            current_year = datetime.now().year
            if car.productionYear > current_year:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid production year: {car.productionYear}."
                )
            db_car.production_year = car.productionYear
        if car.licensePlate:
            db_car.license_plate = car.licensePlate

        # If the garages have been updated we will receive a list with garage IDs
        # If the user didn't change the garages we should receive a list with garage objects
        # In both cases we need to extract the garage IDs and create the relationships with the car in the DB
        garage_ids = car.garageIds
        if not garage_ids and car.garages:
            garage_ids = [garage.id for garage in car.garages]
        if garage_ids:
            garages = db.query(Garage).filter(Garage.id.in_(garage_ids)).all()
            db_car.garages = garages

        db.commit()
        db.refresh(db_car)
        return db_car
    return None


def delete_car(db: Session, car_id: int):
    """ Delete a car from the DB """
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if db_car:
        db.delete(db_car)
        db.commit()
        return db_car
    return None

from fastapi import HTTPException
from sqlalchemy.orm import Session
from car_management_backend.app.models.garage import Garage
from car_management_backend.app.schemas.garage import GarageCreate, GarageUpdate


def create_garage(db: Session, garage: GarageCreate):
    """ Add a new garage to the DB """
    # Validate that the capacity is a positive number
    if garage.capacity <= 0:
        raise HTTPException(
            status_code=400,
            detail=f"Capacity should be a positive number: {garage.capacity}."
        )

    # Add the new garage to the DB
    db_garage = Garage(**garage.dict())
    db.add(db_garage)
    db.commit()
    db.refresh(db_garage)
    return db_garage


def get_garage(db: Session, garage_id: int):
    """ Get a garage from the DB via its ID """
    return db.query(Garage).filter(Garage.id == garage_id).first()


def get_garages(db: Session, city: str = None):
    """ Get all garages from the DB with filter options """
    query = db.query(Garage)
    if city:
        query = query.filter(Garage.city.ilike(f"%{city}%"))
    return query.all()


def update_garage(db: Session, garage_id: int, garage: GarageUpdate):
    """ Update info about a garage in the DB """
    # Validate that the capacity is a positive number
    if garage.capacity <= 0:
        raise HTTPException(
            status_code=400,
            detail=f"Capacity should be a positive number: {garage.capacity}."
        )

    db_garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if db_garage:
        for key, value in garage.dict(exclude_unset=True).items():
            setattr(db_garage, key, value)
        db.commit()
        db.refresh(db_garage)
        return db_garage
    return None


def delete_garage(db: Session, garage_id: int):
    """ Delete a garage from the DB """
    db_garage = db.query(Garage).filter(Garage.id == garage_id).first()
    if db_garage:
        db.delete(db_garage)
        db.commit()
        return db_garage
    return None

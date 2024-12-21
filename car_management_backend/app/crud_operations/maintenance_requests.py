from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from car_management_backend.app.models.car import Car
from car_management_backend.app.models.garage import Garage
from car_management_backend.app.models.maintenance import MaintenanceRequest
from car_management_backend.app.schemas.maintenance import MaintenanceRequestCreate, MaintenanceRequestUpdate


def create_maintenance_request(db: Session, maintenance_request: MaintenanceRequestCreate):
    """ Add a new maintenance request to the DB """
    # Validate that the scheduled date is not in the past
    scheduled_date = datetime.strptime(maintenance_request.scheduledDate, "%Y-%m-%d")
    if scheduled_date < datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Scheduled date cannot be in the past."
        )

    # Add the new maintenance request to the DB
    car = db.query(Car).filter(Car.id == maintenance_request.carId).first()
    garage = db.query(Garage).filter(Garage.id == maintenance_request.garageId).first()

    db_request = MaintenanceRequest(
        car_id=maintenance_request.carId,
        car_name=car.make,
        service_type=maintenance_request.serviceType,
        scheduled_date=maintenance_request.scheduledDate,
        garage_id=maintenance_request.garageId,
        garage_name=garage.name
    )

    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def get_maintenance_request(db: Session, request_id: int):
    """ Get a maintenance request from the DB via its ID """
    return db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()


def get_maintenance_requests(db: Session, car_id: int = None, garage_id: int = None, start_date: str = None,
                             end_date: str = None):
    """ Get all maintenance requests from the DB with filter options """
    query = db.query(MaintenanceRequest)
    if car_id:
        query = query.filter(MaintenanceRequest.car_id == car_id)
    if garage_id:
        query = query.filter(MaintenanceRequest.garage_id == garage_id)
    if start_date:
        query = query.filter(MaintenanceRequest.scheduled_date >= start_date)
    if end_date:
        query = query.filter(MaintenanceRequest.scheduled_date <= end_date)
    return query.all()


def update_maintenance_request(db: Session, request_id: int, maintenance_request: MaintenanceRequestUpdate):
    """ Update info about a maintenance request in the DB """
    db_request = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()
    if db_request:
        if maintenance_request.carId:
            db_request.car_id = maintenance_request.carId
            car = db.query(Car).filter(Car.id == maintenance_request.carId).first()
            db_request.car_name = car.make
        if maintenance_request.serviceType:
            db_request.service_type = maintenance_request.serviceType
        if maintenance_request.scheduledDate:
            scheduled_date = datetime.strptime(maintenance_request.scheduledDate, "%Y-%m-%d")
            if scheduled_date < datetime.now():
                raise HTTPException(
                    status_code=400,
                    detail="Scheduled date cannot be in the past."
                )

            db_request.scheduled_date = maintenance_request.scheduledDate
        if maintenance_request.garageId:
            db_request.garage_id = maintenance_request.garageId
            garage = db.query(Garage).filter(Garage.id == maintenance_request.garageId).first()
            db_request.garage_name = garage.name

        db.commit()
        db.refresh(db_request)
        return db_request
    return None


def delete_maintenance_request(db: Session, request_id: int):
    """ Delete a garage from the DB """
    db_request = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()
    if db_request:
        db.delete(db_request)
        db.commit()
        return db_request
    return None

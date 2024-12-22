from calendar import isleap
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm import class_mapper
from car_management_backend.app.crud_operations import maintenance_requests as maintenance_crud
from car_management_backend.app.crud_operations import reports as reports_generator
from car_management_backend.app.schemas.maintenance import MaintenanceRequestCreate, MaintenanceRequestUpdate, \
    MaintenanceRequestResponse, RequestsPerMonthResponse, YearMonth
from car_management_backend.app.models.database import SessionLocal

router = APIRouter()


def sqlalchemy_to_dict(model_instance):
    """ Map the model fields to the response model ones """
    result = {column.name: getattr(model_instance, column.name) for column in
              class_mapper(model_instance.__class__).columns}

    return {
        "id": result.get("id"),
        "carId": result.get("car_id"),
        "carName": result.get("car_name"),
        "serviceType": result.get("service_type"),
        "scheduledDate": result.get("scheduled_date"),
        "garageId": result.get("garage_id"),
        "garageName": result.get("garage_name")
    }


# Get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/maintenance", response_model=MaintenanceRequestResponse)
def create_maintenance_request(request: MaintenanceRequestCreate, db: Session = Depends(get_db)):
    db_maintenance_request = maintenance_crud.create_maintenance_request(db=db, maintenance_request=request)
    if not db_maintenance_request:
        raise HTTPException(status_code=400, detail="Failed to create maintenance request")
    return sqlalchemy_to_dict(db_maintenance_request)


@router.get("/maintenance", response_model=list[MaintenanceRequestResponse])
def list_maintenance_requests(carId: int = None, garageId: int = None, startDate: str = None, endDate: str = None,
                              db: Session = Depends(get_db)):
    requests = maintenance_crud.get_maintenance_requests(db=db, car_id=carId, garage_id=garageId, start_date=startDate,
                                                         end_date=endDate)

    return [sqlalchemy_to_dict(request) for request in requests]


@router.get("/maintenance/{id:int}", response_model=MaintenanceRequestResponse)
def get_maintenance_request(id: int, db: Session = Depends(get_db)):
    request = maintenance_crud.get_maintenance_request(db=db, request_id=id)
    if not request:
        raise HTTPException(status_code=404, detail="Maintenance request not found")
    return sqlalchemy_to_dict(request)


@router.put("/maintenance/{id}", response_model=MaintenanceRequestResponse)
def update_maintenance_request(id: int, request: MaintenanceRequestUpdate, db: Session = Depends(get_db)):
    updated_request = maintenance_crud.update_maintenance_request(db=db, request_id=id, maintenance_request=request)
    if not updated_request:
        raise HTTPException(status_code=404, detail="Maintenance request not found")
    return sqlalchemy_to_dict(updated_request)


@router.delete("/maintenance/{id}", response_model=MaintenanceRequestResponse)
def delete_maintenance_request(id: int, db: Session = Depends(get_db)):
    deleted_request = maintenance_crud.delete_maintenance_request(db=db, request_id=id)
    if not deleted_request:
        raise HTTPException(status_code=404, detail="Maintenance request not found")
    return sqlalchemy_to_dict(deleted_request)


@router.get("/maintenance/monthlyRequestsReport", response_model=list[RequestsPerMonthResponse])
def get_monthly_requests_report(garageId: int, startMonth: str, endMonth: str, db: Session = Depends(get_db)):
    print("here")
    requests_per_month = reports_generator.get_requests_per_month(db=db, garage_id=garageId, start_month=startMonth,
                                                                  end_month=endMonth)

    # Transform the result into the response schema format
    response = []
    for year_month, count in requests_per_month.items():
        year, month_value = map(int, year_month.split("-"))
        month_name = datetime(year, month_value, 1).strftime("%B").upper()
        leap_year = isleap(year)

        response.append(
            RequestsPerMonthResponse(
                yearMonth=YearMonth(
                    year=year,
                    month=month_name,
                    leapYear=leap_year,
                    monthValue=month_value,
                ),
                requests=count,
            )
        )

    return response

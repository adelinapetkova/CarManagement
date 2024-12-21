from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from car_management_backend.app.crud_operations import garages as garage_crud
from car_management_backend.app.schemas.garage import GarageCreate, GarageUpdate, GarageResponse
from car_management_backend.app.models.database import SessionLocal

router = APIRouter()


# Get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/garages", response_model=GarageResponse)
def create_garage(garage: GarageCreate, db: Session = Depends(get_db)):
    return garage_crud.create_garage(db=db, garage=garage)


@router.get("/garages", response_model=list[GarageResponse])
def list_garages(city: str = None, db: Session = Depends(get_db)):
    return garage_crud.get_garages(db=db, city=city)


@router.get("/garages/{id}", response_model=GarageResponse)
def get_garage(id: int, db: Session = Depends(get_db)):
    garage = garage_crud.get_garage(db=db, garage_id=id)
    if not garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    return garage


@router.put("/garages/{id}", response_model=GarageResponse)
def update_garage(id: int, garage: GarageUpdate, db: Session = Depends(get_db)):
    updated_garage = garage_crud.update_garage(db=db, garage_id=id, garage=garage)
    if not updated_garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    return updated_garage


@router.delete("/garages/{id}", response_model=GarageResponse)
def delete_garage(id: int, db: Session = Depends(get_db)):
    deleted_garage = garage_crud.delete_garage(db=db, garage_id=id)
    if not deleted_garage:
        raise HTTPException(status_code=404, detail="Garage not found")
    return deleted_garage

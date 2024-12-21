from sqlalchemy import Table, Column, Integer, ForeignKey
from car_management_backend.app.models.database import Base

# Association table for relationship between Car and Garage
car_garage = Table(
    'car_garage', Base.metadata,
    Column('car_id', Integer, ForeignKey('cars.id'), primary_key=True),
    Column('garage_id', Integer, ForeignKey('garages.id'), primary_key=True)
)

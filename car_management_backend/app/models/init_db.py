# Script for initial creation of the DB
from car_management_backend.app.models.database import Base, engine
from car_management_backend.app.models.garage import Garage
from car_management_backend.app.models.car import Car
from car_management_backend.app.models.maintenance import MaintenanceRequest


Base.metadata.create_all(bind=engine)


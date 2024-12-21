from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from car_management_backend.app.models.database import Base
from car_management_backend.app.models.car_garage import car_garage


class Car(Base):
    """ Car Model """
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True, nullable=False)
    model = Column(String, nullable=False)
    production_year = Column(Integer, nullable=False)
    license_plate = Column(String, nullable=False)

    garages = relationship("Garage", secondary=car_garage, back_populates="cars")
    maintenance_requests = relationship("MaintenanceRequest", backref="car",
                                        lazy="dynamic", cascade="all, delete-orphan")


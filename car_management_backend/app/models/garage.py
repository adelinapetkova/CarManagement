from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from car_management_backend.app.models.database import Base
from car_management_backend.app.models.car_garage import car_garage


class Garage(Base):
    """ Garage Model """
    __tablename__ = "garages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    location = Column(String, nullable=False)
    city = Column(String, index=True, nullable=False)
    capacity = Column(Integer, nullable=False)

    cars = relationship("Car", secondary=car_garage, back_populates="garages")

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from car_management_backend.app.models.database import Base


class MaintenanceRequest(Base):
    """ Maintenance request model """
    __tablename__ = "maintenance_requests"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    car_name = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    scheduled_date = Column(String, nullable=False)
    garage_id = Column(Integer, ForeignKey("garages.id"), nullable=False)
    garage_name = Column(String, nullable=False)

    garage = relationship("Garage")



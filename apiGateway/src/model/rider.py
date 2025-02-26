from sqlalchemy import Column, Integer, String
from src.data.init import Base
class Rider(Base):
    __tablename__ = "Rider"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    password = Column(String, index=True)
    rider_status = Column(bool, index=True) # available = 1 ; not available = false
    rating = Column(String, index=True)
    vehicle_type = Column(String, index=True)
    license_plate = Column(String, index=True)
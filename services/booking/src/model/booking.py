from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from src.data.init import Base, engine

class Booking(Base):
    __tablename__ = "bookings"  

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True)  # canceled, assigned, pending, completed
    fare_estimate = Column(Float, index=True)

    user_id = Column(Integer, index=True)
    rider_id = Column(Integer, index=True, nullable=True)

Base.metadata.create_all(bind=engine)

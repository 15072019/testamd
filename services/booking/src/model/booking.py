from sqlalchemy import Column, Integer, String, ForeignKey
from src.data.init import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Booking(Base):
    __tablename__ = "Booking"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True) # canceled, assigned, pending, completed
    phone = Column(String,index=True)
    fare_estimate = Column(float,index=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    rider_id = Column(Integer, ForeignKey('rider.id'))

    user = relationship("User", back_populates="bookings")
    rider = relationship("Rider", back_populates="bookings")



    

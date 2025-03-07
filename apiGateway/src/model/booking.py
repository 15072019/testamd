from sqlalchemy import Column, Integer, String, ForeignKey, Float
from src.data.init import Base
from sqlalchemy.orm import relationship
from src.model.user import User
from src.model.rider import Rider   


class Booking(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True) # canceled, assigned, pending, completed
    phone = Column(String,index=True)
    fare_estimate = Column(Float,index=True)

    user_id = Column(Integer, ForeignKey('users.id'),index=True, nullable=False)
    user = relationship(User)

    rider_id = Column(Integer, ForeignKey('riders.id'),index=True, nullable=False)
    rider = relationship(Rider)



    

from sqlalchemy import Column, Integer, String, ForeignKey
from src.data.init import Base
from src.model.rider import Rider
from src.model.user import User
from sqlalchemy.orm import relationship, Mapped, mapped_column

class Booking(Base):
    __tablename__ = "Booking"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    rider_id = Column(String, index=True)
    status = Column(String, index=True) # canceled, assigned, pending, completed
    phone = Column(String,index=True)
    fare_estimate = Column(float,index=True)

    user_id = Column(Integer, ForeignKey('user.id'))
    rider_id_id = Column(Integer, ForeignKey('rider.id'))

    user = relationship(User)
    rider = relationship(Rider)


    

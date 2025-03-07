from sqlalchemy import Column, Integer, String
from src.data.init import Base,engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_number = Column(String, unique=True, index=True)
    password = Column(String) 

    # bookings = relationship("Booking", back_populates="user")

        
Base.metadata.create_all(bind=engine)
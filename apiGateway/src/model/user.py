from sqlalchemy import Column, Integer, String
from src.data.init import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column

class User(Base):
    __tablename__ = "User"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    bookings = relationship("Booking", back_populates="user")
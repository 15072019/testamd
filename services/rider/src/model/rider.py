from sqlalchemy import Column, Integer, String, Boolean, Float
from src.data.init import Base, engine
from sqlalchemy.orm import relationship


class Rider(Base):
    __tablename__ = "riders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_number = Column(String, unique=True, nullable=False)  
    password = Column(String, nullable=False) 
    status = Column(Boolean, default=True, nullable=False)
    rating = Column(Float, default=5.0)
    type = Column(String)
    license_plate = Column(String, unique=True)

Base.metadata.create_all(bind=engine)

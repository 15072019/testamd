from sqlalchemy import Column, Integer, String, Boolean, Float
from src.data.init import Base, engine

class Rider(Base):
    __tablename__ = "riders"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone_number = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    status = Column(Boolean, default=True, nullable=False)
    type = Column(String)
    license_plate = Column(String, unique=True)

Base.metadata.create_all(bind=engine)
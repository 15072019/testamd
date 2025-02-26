from sqlalchemy import Column, Integer, String
from src.data.init import Base

class User(Base):
    __tablename__ = "User"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    username = Column(String, index=True)
    password = Column(String, index=True)
    phone = Column(String,index=True)
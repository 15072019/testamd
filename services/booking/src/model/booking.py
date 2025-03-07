from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.data.init import Base, engine
from services.user.src.model.user import User
from services.rider.src.model.rider import Rider


class Booking(Base):
    __tablename__ = "bookings"  

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True)  # canceled, assigned, pending, completed
    fare_estimate = Column(Float, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    rider_id = Column(Integer, ForeignKey("riders.id"), index=True, nullable=True)

    # Thiết lập quan hệ
    user = relationship(User)
    rider = relationship(Rider)

Base.metadata.create_all(bind=engine)

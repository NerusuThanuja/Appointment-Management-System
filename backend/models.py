from sqlalchemy import Column, Integer, String
from pydantic import BaseModel
from database import Base

# ---------- SQLAlchemy Table ----------
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    appointment_date = Column(String)
    appointment_time = Column(String)


# ---------- Pydantic Schema ----------
class AppointmentCreate(BaseModel):
    name: str
    email: str
    appointment_date: str
    appointment_time: str
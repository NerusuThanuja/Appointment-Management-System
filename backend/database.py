from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./appointments.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def appointment_exists(db, email: str, appointment_date: str, appointment_time: str):
    return db.query(Appointment).filter(
        Appointment.email == email,
        Appointment.appointment_date == appointment_date,
        Appointment.appointment_time == appointment_time
    ).first()
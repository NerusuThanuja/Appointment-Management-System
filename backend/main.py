from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import Appointment, AppointmentCreate

app = FastAPI(title="Appointment Management System")

# Create DB tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "MESSAGE": "APPOINTMENT MANAGEMENT SYSTEM API IS RUNNING"
    }


@app.post("/appointments")
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db)
):
    new_appointment = Appointment(
        name=appointment.name.upper(),
        email=appointment.email.upper(),
        appointment_date=appointment.appointment_date.upper(),
        appointment_time=appointment.appointment_time.upper()
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return {
        "MESSAGE": "APPOINTMENT CREATED SUCCESSFULLY",
        "NAME": new_appointment.name,
        "EMAIL": new_appointment.email,
        "APPOINTMENT_DATE": new_appointment.appointment_date,
        "APPOINTMENT_TIME": new_appointment.appointment_time
    }
@app.get("/appointments")
def get_appointments(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()

    return [
        {
            "NAME": a.name,
            "EMAIL": a.email,
            "APPOINTMENT_DATE": a.appointment_date,
            "APPOINTMENT_TIME": a.appointment_time
        }
        for a in appointments
    ]
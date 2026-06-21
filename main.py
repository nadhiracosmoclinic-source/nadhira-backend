from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import engine, SessionLocal
from models import (
    Base,
    Patient,
    Prescription,
    SessionLog,
    Appointment
)
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


class PatientCreate(BaseModel):
    id: str
    name: str
    age: int
    gender: str
    phone: str
    address: str = ""
    concern: str = ""
    payment: str = ""
    amount: float = 0
    followupDate: str = ""
    dateOfVisit: str = ""
    registeredAt: str = ""
    
class PrescriptionCreate(BaseModel):

    id: str

    patientId: str

    date: str

    diagnosis: str = ""

    medicines: str = ""

    advice: str = ""

    followup: str = ""

    createdAt: str = ""
    
class SessionCreate(BaseModel):

    id: str

    patientId: str

    date: str

    sessionType: str = ""

    notes: str = ""

    createdAt: str = ""
    
class AppointmentCreate(BaseModel):

    id: str

    patientId: str

    date: str

    time: str = ""

    reason: str = ""

    status: str = ""

    createdAt: str = ""


Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "status": "running",
        "app": "Nadhira Skin Clinic"
    }

@app.get("/fixdb")
def fixdb():
    db = SessionLocal()

    db.execute(text('ALTER TABLE patients ADD COLUMN IF NOT EXISTS "dateOfVisit" VARCHAR'))
    db.execute(text('ALTER TABLE patients ADD COLUMN IF NOT EXISTS "followupDate" VARCHAR'))
    db.execute(text('ALTER TABLE patients ADD COLUMN IF NOT EXISTS "registeredAt" VARCHAR'))

    db.commit()
    db.close()

    return {"status": "fixed"}

@app.get("/patients")
def get_patients():

    db: Session = SessionLocal()

    patients = db.query(Patient).all()

    data = []

    for p in patients:
        data.append({
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "gender": p.gender,
            "phone": p.phone,
            "address": p.address,
            "concern": p.concern,
            "dateOfVisit": p.dateOfVisit,
            "payment": p.payment,
            "amount": p.amount,
            "followupDate": p.followupDate,
            "registeredAt": p.registeredAt
        })

    db.close()

    return data


@app.post("/patients")
def create_patient(patient: PatientCreate):

    db = SessionLocal()

    new_patient = Patient(
        id=patient.id,
        name=patient.name,
        age=patient.age,
        gender=patient.gender,
        phone=patient.phone,
        address=patient.address,
        concern=patient.concern,
        dateOfVisit=patient.dateOfVisit,
        payment=patient.payment,
        amount=patient.amount,
        followupDate=patient.followupDate,
        registeredAt=patient.registeredAt
    )

    db.add(new_patient)
    db.commit()

    db.close()

    return {
        "message": "Patient created successfully"
    }


@app.put("/patients/{patient_id}")
def update_patient(patient_id: str, patient: PatientCreate):

    db = SessionLocal()

    p = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not p:
        db.close()
        return {"error": "Patient not found"}

    p.name = patient.name
    p.age = patient.age
    p.gender = patient.gender
    p.phone = patient.phone
    p.address = patient.address
    p.concern = patient.concern
    p.payment = patient.payment
    p.amount = patient.amount
    p.followupDate = patient.followupDate
    p.registeredAt = patient.registeredAt

    db.commit()
    db.close()

    return {
        "message": "Patient updated successfully"
    }


@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: str):

    db = SessionLocal()

    p = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not p:
        db.close()
        return {"error": "Patient not found"}

    db.delete(p)
    db.commit()
    db.close()

    return {
        "message": "Patient deleted successfully"
    }
    
@app.get("/patients/{patient_id}")
def get_patient(patient_id: str):

    db = SessionLocal()

    p = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    db.close()

    if not p:
        return {"error": "Patient not found"}

    return {
        "id": p.id,
        "name": p.name,
        "age": p.age,
        "gender": p.gender,
        "phone": p.phone,
        "address": p.address,
        "concern": p.concern,
        "payment": p.payment,
        "amount": p.amount,
        "followupDate": p.followupDate,
        "registeredAt": p.registeredAt
    }
    
    
@app.get("/prescriptions")
def get_prescriptions():

    db = SessionLocal()

    rows = db.query(Prescription).all()

    data = []

    for r in rows:
        data.append({
            "id": r.id,
            "patientId": r.patientId,
            "date": r.date,
            "diagnosis": r.diagnosis,
            "medicines": r.medicines,
            "advice": r.advice,
            "followup": r.followup,
            "createdAt": r.createdAt
        })

    db.close()

    return data


@app.post("/prescriptions")
def create_prescription(rx: PrescriptionCreate):

    db = SessionLocal()

    new_rx = Prescription(
        id=rx.id,
        patientId=rx.patientId,
        date=rx.date,
        diagnosis=rx.diagnosis,
        medicines=rx.medicines,
        advice=rx.advice,
        followup=rx.followup,
        createdAt=rx.createdAt
    )

    db.add(new_rx)

    db.commit()

    db.close()

    return {
        "message": "Prescription created successfully"
    }
    
@app.get("/prescriptions/{patient_id}")
def get_patient_prescriptions(patient_id: str):

    db = SessionLocal()

    rows = db.query(Prescription).filter(
        Prescription.patientId == patient_id
    ).all()

    data = []

    for r in rows:
        data.append({
            "id": r.id,
            "patientId": r.patientId,
            "date": r.date,
            "diagnosis": r.diagnosis,
            "medicines": r.medicines,
            "advice": r.advice,
            "followup": r.followup,
            "createdAt": r.createdAt
        })

    db.close()

    return data
    
    
@app.post("/sessions")
def create_session(session: SessionCreate):

    db = SessionLocal()

    row = SessionLog(
        id=session.id,
        patientId=session.patientId,
        date=session.date,
        sessionType=session.sessionType,
        notes=session.notes,
        createdAt=session.createdAt
    )

    db.add(row)

    db.commit()

    db.close()

    return {
        "message": "Session created successfully"
    }


@app.get("/sessions/{patient_id}")
def get_sessions(patient_id: str):

    db = SessionLocal()

    rows = db.query(
        SessionLog
    ).filter(
        SessionLog.patientId == patient_id
    ).all()

    data = []

    for s in rows:

        data.append({

            "id": s.id,

            "patientId": s.patientId,

            "date": s.date,

            "sessionType": s.sessionType,

            "notes": s.notes,

            "createdAt": s.createdAt

        })

    db.close()

    return data
    
    
@app.post("/appointments")
def create_appointment(appt: AppointmentCreate):

    db = SessionLocal()

    row = Appointment(

        id=appt.id,

        patientId=appt.patientId,

        date=appt.date,

        time=appt.time,

        reason=appt.reason,

        status=appt.status,

        createdAt=appt.createdAt
    )

    db.add(row)

    db.commit()

    db.close()

    return {
        "message": "Appointment created successfully"
    }


@app.get("/appointments")
def get_appointments():

    db = SessionLocal()

    rows = db.query(
        Appointment
    ).all()

    data = []

    for a in rows:

        data.append({

            "id": a.id,

            "patientId": a.patientId,

            "date": a.date,

            "time": a.time,

            "reason": a.reason,

            "status": a.status,

            "createdAt": a.createdAt

        })

    db.close()

    return data
    

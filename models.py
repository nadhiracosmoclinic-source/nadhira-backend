from sqlalchemy import Column, String, Integer, Float
from database import Base

class Patient(Base):

    __tablename__ = "patients"

    id = Column(String, primary_key=True)

    name = Column(String)
    age = Column(Integer)
    gender = Column(String)

    phone = Column(String)
    address = Column(String)

    concern = Column(String)

    payment = Column(String)
    amount = Column(Float)

    followupDate = Column(String)
    registeredAt = Column(String)
    
class Prescription(Base):

    __tablename__ = "prescriptions"

    id = Column(String, primary_key=True)

    patientId = Column(String)

    date = Column(String)

    diagnosis = Column(String)

    medicines = Column(String)

    advice = Column(String)

    followup = Column(String)

    createdAt = Column(String)
    
class SessionLog(Base):

    __tablename__ = "sessions"

    id = Column(String, primary_key=True)

    patientId = Column(String)

    date = Column(String)

    sessionType = Column(String)

    notes = Column(String)

    createdAt = Column(String)
    
class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(String, primary_key=True)

    patientId = Column(String)

    date = Column(String)

    time = Column(String)

    reason = Column(String)

    status = Column(String)

    createdAt = Column(String)
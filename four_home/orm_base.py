from sqlmodel import SQLModel, Field, Session, create_engine, Relationship
from datetime import date
from typing import Optional, List

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str = Field(index=True, unique=True)
    birth_date: Optional[date] = None
    hashed_password: str

class Doctor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str = Field(index=True, unique=True)
    birth_date: Optional[date] = None
    specialization: str
    experience: int
    hashed_password: str

class Visit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    patient_id: int = Field(foreign_key="patient.id")
    doctor_id: int = Field(foreign_key="doctor.id")
    visit_date: date
    complaints: Optional[str] = None
    diagnosis: Optional[str] = None

class Prescription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    visit_id: int = Field(foreign_key="visit.id")
    medicine: str
    dose: str
    instructions: Optional[str] = None



sqlite_file_name = "four_home/dentistry.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

# создаём таблицы
SQLModel.metadata.create_all(engine)
